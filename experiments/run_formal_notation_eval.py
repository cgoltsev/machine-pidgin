#!/usr/bin/env python3
"""Paired vernacular-vs-formal-notation evaluation through OpenRouter."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import math
import os
import statistics
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "experiments" / "formal_notation_tasks.json"
RESULTS_DIR = ROOT / "experiments" / "results"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-5.6-luna",
    "openai/gpt-5.6-terra",
    "openai/gpt-5.6-sol",
]
CONDITIONS = ("vernacular", "formal")
SYSTEM = (
    "Solve the user's task from the information provided. Return one valid JSON object only, "
    "with exactly the requested keys and no markdown or commentary."
)

_print_lock = threading.Lock()
_sol_lock = threading.Lock()
_budget_lock = threading.Lock()
_sol_last_request = 0.0
_reported_spend = 0.0


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
            for chunk in text.split("```"):
                candidate = chunk.removeprefix("json").strip()
                try:
                    return json.loads(candidate), False
                except json.JSONDecodeError:
                    pass
        return None, False


def request_completion(api_key, model, prompt, max_study_spend, attempt=1):
    global _reported_spend, _sol_last_request
    with _budget_lock:
        if _reported_spend >= max_study_spend:
            raise RuntimeError(f"study budget stop reached at ${_reported_spend:.6f}")
    if model == "openai/gpt-5.6-sol":
        with _sol_lock:
            remaining = 6.25 - (time.monotonic() - _sol_last_request)
            if remaining > 0:
                time.sleep(remaining)
            _sol_last_request = time.monotonic()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
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
            "X-Title": "Machine Pidgin Formal Notation Benchmark",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.load(response)
        with _budget_lock:
            _reported_spend += float((data.get("usage") or {}).get("cost") or 0)
        return data
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        if attempt < 5:
            time.sleep(8 if getattr(error, "code", None) == 429 else 2**attempt)
            return request_completion(api_key, model, prompt, max_study_spend, attempt + 1)
        body = error.read().decode(errors="replace") if hasattr(error, "read") else str(error)
        raise RuntimeError(f"OpenRouter request failed: {body[:500]}") from error


def run_one(api_key, model, task, condition, repetition, max_study_spend):
    started = time.monotonic()
    data = request_completion(api_key, model, task[condition], max_study_spend)
    raw = data["choices"][0]["message"].get("content", "")
    parsed, strict_json = parse_json(raw)
    total, matched = leaves(task["expected"], parsed)
    return {
        "task_id": task["id"],
        "split": task["split"],
        "category": task["category"],
        "notation_expected_to_help": task["notation_expected_to_help"],
        "model": model,
        "condition": condition,
        "repetition": repetition,
        "valid_json": strict_json,
        "on_task": parsed is not None and canonical(parsed) == canonical(task["expected"]),
        "constraint_score": matched / total,
        "expected": task["expected"],
        "response": parsed,
        "raw_response": raw,
        "usage": data.get("usage") or {},
        "provider": data.get("provider"),
        "latency_seconds": round(time.monotonic() - started, 3),
        "error": None,
    }


def rate_block(subset):
    valid = [row for row in subset if not row["error"]]
    return {
        "n": len(valid),
        "errors": len(subset) - len(valid),
        "on_task_count": sum(row["on_task"] for row in valid),
        "on_task_rate": sum(row["on_task"] for row in valid) / len(valid) if valid else None,
        "mean_constraint_score": statistics.fmean(row["constraint_score"] for row in valid) if valid else None,
        "valid_json_rate": sum(row["valid_json"] for row in valid) / len(valid) if valid else None,
        "reported_cost_usd": sum(float((row["usage"] or {}).get("cost") or 0) for row in valid),
        "mean_latency_seconds": statistics.fmean(row["latency_seconds"] for row in valid) if valid else None,
    }


def paired_block(rows):
    keyed = {}
    for row in rows:
        if not row["error"]:
            keyed[(row["model"], row["task_id"], row["repetition"], row["condition"])] = row
    repairs = regressions = concordant_success = concordant_failure = 0
    for model in MODELS:
        pairs = {(task, rep) for m, task, rep, _ in keyed if m == model}
        for task, rep in pairs:
            v = keyed.get((model, task, rep, "vernacular"))
            f = keyed.get((model, task, rep, "formal"))
            if not v or not f:
                continue
            if not v["on_task"] and f["on_task"]:
                repairs += 1
            elif v["on_task"] and not f["on_task"]:
                regressions += 1
            elif v["on_task"] and f["on_task"]:
                concordant_success += 1
            else:
                concordant_failure += 1
    discordant = repairs + regressions
    if discordant:
        tail = sum(math.comb(discordant, k) for k in range(0, min(repairs, regressions) + 1)) / (2**discordant)
        p_exact = min(1.0, 2 * tail)
    else:
        p_exact = 1.0
    return {
        "formal_repairs": repairs,
        "formal_regressions": regressions,
        "concordant_success": concordant_success,
        "concordant_failure": concordant_failure,
        "mcnemar_exact_two_sided_descriptive_p": p_exact,
    }


def summarize(rows):
    summary = {"overall": {}, "by_model": {}, "by_expected_effect": {}}
    for condition in CONDITIONS:
        summary["overall"][condition] = rate_block([row for row in rows if row["condition"] == condition])
    summary["overall"]["absolute_lift"] = (
        summary["overall"]["formal"]["on_task_rate"] - summary["overall"]["vernacular"]["on_task_rate"]
    )
    for model in MODELS:
        summary["by_model"][model] = {}
        for condition in CONDITIONS:
            summary["by_model"][model][condition] = rate_block(
                [row for row in rows if row["model"] == model and row["condition"] == condition]
            )
        summary["by_model"][model]["absolute_lift"] = (
            summary["by_model"][model]["formal"]["on_task_rate"]
            - summary["by_model"][model]["vernacular"]["on_task_rate"]
        )
    for label, expected in (("notation_friendly", True), ("negative_controls", False)):
        summary["by_expected_effect"][label] = {}
        subset = [row for row in rows if row["notation_expected_to_help"] is expected]
        for condition in CONDITIONS:
            summary["by_expected_effect"][label][condition] = rate_block(
                [row for row in subset if row["condition"] == condition]
            )
        summary["by_expected_effect"][label]["absolute_lift"] = (
            summary["by_expected_effect"][label]["formal"]["on_task_rate"]
            - summary["by_expected_effect"][label]["vernacular"]["on_task_rate"]
        )
    summary["paired"] = paired_block(rows)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["development", "held_out", "all"], default="held_out")
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--max-study-spend", type=float, default=5.0)
    args = parser.parse_args()
    if args.repetitions < 1 or args.workers < 1 or args.max_study_spend <= 0:
        raise SystemExit("repetitions, workers, and max-study-spend must be positive")
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
        for condition in CONDITIONS
        for repetition in range(1, args.repetitions + 1)
    ]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / f"{timestamp}-{args.split}-formal-notation.json"
    rows = []
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_one, api_key, model, task, condition, repetition, args.max_study_spend):
            (model, task, condition, repetition)
            for model, task, condition, repetition in jobs
        }
        for future in concurrent.futures.as_completed(futures):
            model, task, condition, repetition = futures[future]
            try:
                rows.append(future.result())
            except Exception as error:
                rows.append({
                    "task_id": task["id"], "split": task["split"], "category": task["category"],
                    "notation_expected_to_help": task["notation_expected_to_help"], "model": model,
                    "condition": condition, "repetition": repetition, "valid_json": False,
                    "on_task": False, "constraint_score": 0, "expected": task["expected"],
                    "response": None, "raw_response": "", "usage": {}, "provider": None,
                    "latency_seconds": None, "error": str(error),
                })
            completed += 1
            if completed % 16 == 0 or completed == len(jobs):
                with _print_lock:
                    print(f"completed {completed}/{len(jobs)}; reported spend ${_reported_spend:.6f}", flush=True)
    rows.sort(key=lambda row: (MODELS.index(row["model"]), row["task_id"], row["condition"], row["repetition"]))
    document = {
        "study": "Machine Pidgin Benchmark 002: mathematical notation versus vernacular",
        "timestamp_utc": timestamp,
        "design": {
            "split": args.split,
            "repetitions": args.repetitions,
            "models": MODELS,
            "conditions": list(CONDITIONS),
            "system_instruction_identical": SYSTEM,
            "reasoning_effort": "low for GPT-5.6 family; provider default for GPT-4o mini",
            "temperature": "provider default; fixed seed requested",
            "scoring": "Exact equality with preregistered JSON is on-task; recursive expected-leaf match is constraint score.",
            "tasks_sha256": hashlib.sha256(tasks_raw).hexdigest(),
            "max_study_spend_usd": args.max_study_spend,
        },
        "summary": summarize(rows),
        "rows": rows,
    }
    output_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    print(output_path)
    print(json.dumps(document["summary"], indent=2))


if __name__ == "__main__":
    main()
