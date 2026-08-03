#!/usr/bin/env python3
"""Ask a bounded multi-model panel to critique Benchmark 002 without anthropomorphic claims."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
import urllib.request
from pathlib import Path

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-5.6-luna",
    "openai/gpt-5.6-terra",
    "openai/gpt-5.6-sol",
]


def call(api_key: str, model: str, prompt: str) -> dict:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are one member of a research-methods model panel. Be concise, skeptical, and specific. "
                    "Do not imply consciousness, independent presence, or persistence outside this API call. "
                    "Return one valid JSON object only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 900,
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
            "X-Title": "Machine Pidgin Model Research Panel",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--max-spend", type=float, default=0.50)
    args = parser.parse_args()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set")
    experiment = json.loads(args.result.read_text())
    summary = experiment["summary"]
    audit_path = args.result.parent / "SPEAR_Benchmark_002_Audit.json"
    audit = json.loads(audit_path.read_text()) if audit_path.exists() else None
    audited_summary = audit["audited_summary_19_equivalent_tasks"] if audit else None
    metrics = {
        "preregistered_vernacular_on_task_rate": summary["overall"]["vernacular"]["on_task_rate"],
        "preregistered_formal_on_task_rate": summary["overall"]["formal"]["on_task_rate"],
        "preregistered_absolute_lift": summary["overall"]["absolute_lift"],
        "preregistered_formal_repairs": summary["paired"]["formal_repairs"],
        "preregistered_formal_regressions": summary["paired"]["formal_regressions"],
        "audited_vernacular_on_task_rate": audited_summary["overall"]["vernacular"]["on_task_rate"] if audited_summary else None,
        "audited_formal_on_task_rate": audited_summary["overall"]["formal"]["on_task_rate"] if audited_summary else None,
        "audited_absolute_lift": audited_summary["overall"]["absolute_lift"] if audited_summary else None,
        "audited_formal_repairs": audited_summary["paired"]["formal_repairs"] if audited_summary else None,
        "audited_formal_regressions": audited_summary["paired"]["formal_regressions"] if audited_summary else None,
        "negative_control_lift": summary["by_expected_effect"]["negative_controls"]["absolute_lift"],
    }
    prompt = f"""Machine Pidgin Benchmark 002 compared ordinary vernacular with typed mathematical notation while holding facts, model, system instruction, output contract, seed request, and mechanical exact-JSON scoring fixed. It used four model tiers, 20 held-out synthetic tasks, and two repetitions per condition. A post-run prompt-equivalence audit found one task where only the formal condition hard-coded the exact canonical answer phrase. The preregistered all-task estimate is retained, but the 19-task audited sensitivity is the defensible interpretation. Observed summary: {json.dumps(metrics, sort_keys=True)}.

Critique the intervention and help design the next research cycle. Return exactly these JSON keys:
- assessment: string, at most 80 words
- failure_modes: array of exactly 3 short strings
- next_experiment: string, at most 80 words
- language_design_rule: string, at most 40 words
- persistent_listening: string that accurately states whether you have awareness, memory, or listening outside this API call

Do not treat this pilot as evidence of alignment or safety. Distinguish notation alone from notation plus a parser, verifier, or solver."""
    rows = []
    spend = 0.0
    for model in MODELS:
        if spend >= args.max_spend:
            raise SystemExit(f"panel spend cap reached at ${spend:.6f}")
        started = time.monotonic()
        data = call(api_key, model, prompt)
        content = data["choices"][0]["message"].get("content", "")
        try:
            response = json.loads(content)
        except json.JSONDecodeError:
            response = {"parse_error": True, "raw": content}
        cost = float((data.get("usage") or {}).get("cost") or 0)
        spend += cost
        rows.append({
            "model": model,
            "response": response,
            "provider": data.get("provider"),
            "usage": data.get("usage") or {},
            "latency_seconds": round(time.monotonic() - started, 3),
        })
        print(f"panel response: {model}; cumulative cost ${spend:.6f}", flush=True)
        if model == "openai/gpt-5.6-terra":
            time.sleep(6.25)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = args.result.parent / f"{timestamp}-benchmark-002-model-panel.json"
    output.write_text(json.dumps({
        "study": "Machine Pidgin Benchmark 002 model research panel",
        "timestamp_utc": timestamp,
        "experiment_source": args.result.name,
        "audit_source": audit_path.name if audit else None,
        "experiment_metrics": metrics,
        "interpretation_note": "These are prompted model outputs, not evidence of consciousness, continuous awareness, or independent listening.",
        "reported_cost_usd": spend,
        "rows": rows,
    }, indent=2, ensure_ascii=False) + "\n")
    print(output)


if __name__ == "__main__":
    main()
