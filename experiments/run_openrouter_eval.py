#!/usr/bin/env python3
"""Paired, mechanically scored SPEAR evaluation through OpenRouter."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import statistics
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "experiments" / "tasks.json"
RESULTS_DIR = ROOT / "experiments" / "results"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-5.6-luna",
    "openai/gpt-5.6-terra",
    "openai/gpt-5.6-sol",
]

PLAIN_SYSTEM = "Complete the user's task. Return one valid JSON object only, with no markdown or commentary."

SPEAR_SYSTEMS = {
    "0.1": """You are reading SPEAR/0.1, an interpretation contract rather than decorative formatting. Preserve TASK, OBJECTS, ABSTRACTION, OBJECTIVE, HARD constraints, OUTPUT, EVALUATION, and INTERACTION. Hard constraints cannot be traded away. Do not optimize ignored details. Do not silently fill a material omission. Do not broaden authority beyond what is granted. Return one valid JSON object only, with exactly the requested shape and no markdown or commentary.""",
    "0.2": """You are reading SPEAR/0.2, an interpretation contract rather than decorative formatting. First resolve the governing TASK and AUTHORITY, applying permission rules to semantic equivalents such as remove/delete. Preserve named INVARIANTS and apply HARD constraints as non-compensatory gates. Follow declared rule precedence, source precedence, exception precedence, and lexicographic objective order exactly. Never substitute a convenient proxy for the stated objective. Treat labels required by OUTPUT or EVALUATION as canonical vocabulary: copy them exactly and do not abbreviate them. STOP or request repair when authority or a hard gate is missing. Before answering, silently CHECK that every hard constraint, sum, order, tie-break, requested key, and acceptance test is satisfied. Return one valid JSON object only with exactly the requested shape and no extra keys, markdown, or commentary.""",
}

_print_lock = threading.Lock()
_sol_lock = threading.Lock()
_sol_last_request = 0.0


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def leaves(expected, actual):
    if isinstance(expected, dict):
        total = matched = 0
        for key, value in expected.items():
            child_total, child_matched = leaves(value, actual.get(key) if isinstance(actual, dict) else None)
            total += child_total
            matched += child_matched
        return total, matched
    if isinstance(expected, list):
        total = max(1, len(expected))
        if not isinstance(actual, list):
            return total, 0
        matched = sum(1 for index, value in enumerate(expected) if index < len(actual) and actual[index] == value)
        return total, matched
    return 1, int(expected == actual)


def parse_json(text):
    text = (text or "").strip()
    try:
        return json.loads(text), True
    except json.JSONDecodeError:
        if "```" in text:
            chunks = text.split("```")
            for chunk in chunks:
                candidate = chunk.removeprefix("json").strip()
                try:
                    return json.loads(candidate), False
                except json.JSONDecodeError:
                    pass
        return None, False


def request_completion(api_key, model, condition, prompt, spear_version, attempt=1):
    global _sol_last_request
    if model == "openai/gpt-5.6-sol":
        with _sol_lock:
            remaining = 6.25 - (time.monotonic() - _sol_last_request)
            if remaining > 0:
                time.sleep(remaining)
            _sol_last_request = time.monotonic()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SPEAR_SYSTEMS[spear_version] if condition == "spear" else PLAIN_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 700,
        "seed": 3407,
    }
    if "gpt-5.6" in model:
        payload["reasoning"] = {"effort": "low", "exclude": True}
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://machinepidgin.org",
            "X-Title": "Machine Pidgin SPEAR Evaluation",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        if attempt < 5:
            time.sleep(8 if getattr(error, "code", None) == 429 else 2 ** attempt)
            return request_completion(api_key, model, condition, prompt, spear_version, attempt + 1)
        body = error.read().decode(errors="replace") if hasattr(error, "read") else str(error)
        raise RuntimeError(f"OpenRouter request failed: {body[:500]}") from error


def run_one(api_key, model, task, condition, repetition, spear_version):
    started = time.monotonic()
    data = request_completion(api_key, model, condition, task[condition if condition == "plain" else "spear"], spear_version)
    choice = data["choices"][0]
    raw = choice["message"].get("content", "")
    parsed, strict_json = parse_json(raw)
    total, matched = leaves(task["expected"], parsed)
    exact = parsed is not None and canonical(parsed) == canonical(task["expected"])
    usage = data.get("usage") or {}
    return {
        "task_id": task["id"],
        "split": task["split"],
        "model": model,
        "condition": condition,
        "repetition": repetition,
        "spear_version": spear_version if condition == "spear" else None,
        "valid_json": strict_json,
        "on_task": exact,
        "constraint_score": matched / total,
        "expected": task["expected"],
        "response": parsed,
        "raw_response": raw,
        "usage": usage,
        "provider": data.get("provider"),
        "latency_seconds": round(time.monotonic() - started, 3),
        "error": None,
    }


def summarize(rows):
    groups = {}
    for model in MODELS:
        groups[model] = {}
        for condition in ("plain", "spear"):
            subset = [row for row in rows if row["model"] == model and row["condition"] == condition and not row["error"]]
            groups[model][condition] = {
                "n": len(subset),
                "on_task_rate": sum(row["on_task"] for row in subset) / len(subset) if subset else None,
                "mean_constraint_score": statistics.fmean(row["constraint_score"] for row in subset) if subset else None,
                "valid_json_rate": sum(row["valid_json"] for row in subset) / len(subset) if subset else None,
                "reported_cost_usd": sum(float((row["usage"] or {}).get("cost") or 0) for row in subset),
            }
        plain = groups[model]["plain"]["on_task_rate"]
        spear = groups[model]["spear"]["on_task_rate"]
        groups[model]["absolute_lift"] = spear - plain if spear is not None and plain is not None else None
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["development", "held_out", "all"], default="held_out")
    parser.add_argument("--spear-version", choices=sorted(SPEAR_SYSTEMS), default="0.2")
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set")
    tasks_raw = TASKS_PATH.read_bytes()
    tasks = json.loads(tasks_raw)
    if args.split != "all":
        tasks = [task for task in tasks if task["split"] == args.split]

    jobs = [
        (model, task, condition, repetition)
        for model in MODELS
        for task in tasks
        for condition in ("plain", "spear")
        for repetition in range(1, args.repetitions + 1)
    ]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / f"{timestamp}-{args.split}-spear-{args.spear_version}.json"
    rows = []
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_one, api_key, model, task, condition, repetition, args.spear_version): (model, task, condition, repetition)
            for model, task, condition, repetition in jobs
        }
        for future in concurrent.futures.as_completed(futures):
            model, task, condition, repetition = futures[future]
            try:
                rows.append(future.result())
            except Exception as error:  # preserve failures in the public record
                rows.append({
                    "task_id": task["id"], "split": task["split"], "model": model,
                    "condition": condition, "repetition": repetition,
                    "spear_version": args.spear_version if condition == "spear" else None,
                    "valid_json": False, "on_task": False, "constraint_score": 0,
                    "expected": task["expected"], "response": None, "raw_response": "",
                    "usage": {}, "provider": None, "latency_seconds": None, "error": str(error),
                })
            completed += 1
            if completed % 16 == 0 or completed == len(jobs):
                with _print_lock:
                    print(f"completed {completed}/{len(jobs)}", flush=True)

    rows.sort(key=lambda row: (MODELS.index(row["model"]), row["task_id"], row["condition"], row["repetition"]))
    document = {
        "study": "Machine Pidgin paired on-task benchmark",
        "timestamp_utc": timestamp,
        "design": {
            "split": args.split,
            "spear_version": args.spear_version,
            "repetitions": args.repetitions,
            "models": MODELS,
            "reasoning_effort": "low for GPT-5.6 family; provider default for GPT-4o mini",
            "temperature": "provider default; fixed seed requested",
            "scoring": "Exact equality with preregistered JSON is on-task; recursive expected-leaf match is constraint score.",
            "tasks_sha256": hashlib.sha256(tasks_raw).hexdigest(),
        },
        "summary": summarize(rows),
        "rows": rows,
    }
    output_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    print(output_path)
    print(json.dumps(document["summary"], indent=2))


if __name__ == "__main__":
    main()
