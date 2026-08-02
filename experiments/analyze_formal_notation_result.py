#!/usr/bin/env python3
"""Create the transparent Benchmark 002 audit record, tidy rows, and report."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from run_formal_notation_eval import MODELS, summarize

EXCLUSIONS = {
    "test-math-14-workflow": (
        "Post-run prompt-equivalence audit: the formal condition hard-coded the canonical "
        "next_action value 'open the vote' inside its output template, while the vernacular "
        "condition named the action in prose but did not define that exact canonical value. "
        "All eight paired observations failed vernacular exact-match and passed formal, so this "
        "single asymmetric output-label cue accounts for the preregistered aggregate lift."
    )
}


def pct(value: float) -> str:
    rounded = Decimal(str(100 * value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{rounded}%"


def pp(value: float) -> str:
    return f"{100 * value:+.1f} points"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    rows = document["rows"]
    audited_rows = [row for row in rows if row["task_id"] not in EXCLUSIONS]
    full = summarize(rows)
    audited = summarize(audited_rows)
    audit_record = {
        "study": "Machine Pidgin Benchmark 002 post-run prompt-equivalence audit",
        "raw_result": args.result.name,
        "status": "preregistered result retained; asymmetric task excluded in audited sensitivity",
        "exclusions": [{"task_id": task_id, "reason": reason} for task_id, reason in EXCLUSIONS.items()],
        "preregistered_summary_all_20_tasks": full,
        "audited_summary_19_equivalent_tasks": audited,
        "interpretation": (
            "The preregistered all-task aggregate shows a +2.5 percentage-point formal lift, "
            "but the audited equivalent-task set shows a -2.6-point formal change. Mathematical "
            "notation alone therefore did not establish an on-task improvement in this pilot."
        ),
    }
    audit_path = args.result.parent / "SPEAR_Benchmark_002_Audit.json"
    audit_path.write_text(json.dumps(audit_record, indent=2, ensure_ascii=False) + "\n")

    csv_path = args.result.parent / "SPEAR_Benchmark_002_Rows.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "task_id", "model", "condition", "repetition", "category",
            "notation_expected_to_help", "on_task", "constraint_score", "valid_json",
            "latency_seconds", "reported_cost_usd", "provider", "error", "audit_included",
        ])
        for row in rows:
            writer.writerow([
                row["task_id"], row["model"], row["condition"], row["repetition"], row["category"],
                row["notation_expected_to_help"], row["on_task"], row["constraint_score"], row["valid_json"],
                row["latency_seconds"], (row.get("usage") or {}).get("cost", 0), row.get("provider"),
                row.get("error"), row["task_id"] not in EXCLUSIONS,
            ])

    by_model = []
    for model in MODELS:
        full_model = full["by_model"][model]
        audit_model = audited["by_model"][model]
        by_model.append(
            f"| {model.removeprefix('openai/')} | {pct(full_model['vernacular']['on_task_rate'])} | "
            f"{pct(full_model['formal']['on_task_rate'])} | {pp(full_model['absolute_lift'])} | "
            f"{pct(audit_model['vernacular']['on_task_rate'])} | {pct(audit_model['formal']['on_task_rate'])} | "
            f"{pp(audit_model['absolute_lift'])} |"
        )
    report = f"""# Benchmark 002: mathematical notation versus vernacular

**Date:** 2026-08-03  
**Status:** paired synthetic pilot with a disclosed post-run prompt-equivalence exclusion

## Question

When facts, model, system instruction, output contract, seed request, and mechanical scoring are held constant, does adding typed mathematical notation improve exact on-task performance over concise vernacular?

## Result

On the preregistered 20-task set, vernacular was exactly on task in **{full['overall']['vernacular']['on_task_count']}/{full['overall']['vernacular']['n']} ({pct(full['overall']['vernacular']['on_task_rate'])})** observations and formal notation in **{full['overall']['formal']['on_task_count']}/{full['overall']['formal']['n']} ({pct(full['overall']['formal']['on_task_rate'])})**: **{pp(full['overall']['absolute_lift'])}**.

A post-run prompt-equivalence audit found one asymmetric task (`test-math-14-workflow`). The formal condition put the exact expected phrase `open the vote` inside its output template; the vernacular condition did not define that canonical string. That task contributed eight formal repairs and no regressions—more than the entire aggregate lift. It is retained in the raw record and excluded only in the clearly labeled audit sensitivity.

On the remaining 19 equivalent tasks, vernacular was exactly on task in **{audited['overall']['vernacular']['on_task_count']}/{audited['overall']['vernacular']['n']} ({pct(audited['overall']['vernacular']['on_task_rate'])})** and formal notation in **{audited['overall']['formal']['on_task_count']}/{audited['overall']['formal']['n']} ({pct(audited['overall']['formal']['on_task_rate'])})**: **{pp(audited['overall']['absolute_lift'])}**. The defensible conclusion is that **notation alone did not establish an improvement**.

| Model | All-task vernacular | All-task formal | All-task lift | Audited vernacular | Audited formal | Audited lift |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(by_model)}

Across the audited set there were {audited['paired']['formal_repairs']} formal repairs and {audited['paired']['formal_regressions']} formal regressions. The descriptive exact McNemar p-value is {audited['paired']['mcnemar_exact_two_sided_descriptive_p']:.3f}; repeated tasks and related model families mean it is not a confirmatory significance test.

## What the capability pattern suggests

The smallest model lost {abs(100 * audited['by_model']['openai/gpt-4o-mini']['absolute_lift']):.1f} points under notation. Luna was unchanged, Terra gained {100 * audited['by_model']['openai/gpt-5.6-terra']['absolute_lift']:.1f} points, and Sol lost {abs(100 * audited['by_model']['openai/gpt-5.6-sol']['absolute_lift']):.1f} points on the audited set. This non-monotonic interaction is descriptive and needs a larger, independently authored replication. It argues against a universal "more symbols is better" rule.

## Design

- 20 held-out synthetic tasks, two repetitions, two paired conditions, and four model tiers; 320 total API calls and no provider errors.
- The same JSON-only system instruction was used in both conditions. GPT-5.6 models used low reasoning effort; GPT-4o mini used provider defaults.
- Exact equality with preregistered JSON was the primary endpoint; recursive expected-leaf match was secondary.
- Two direct tasks served as negative controls. Both conditions scored 16/16 on them.
- Provider-reported held-out cost was ${full['overall']['vernacular']['reported_cost_usd'] + full['overall']['formal']['reported_cost_usd']:.4f}.

## Interpretation for SPEAR

Mathematical notation should be a selectively compiled layer, not a universal surface language. A stronger next test is a three-way comparison: plain vernacular; a dual-register SPEAR contract with typed fields and plain-language gloss; and the same contract compiled to executable checks or a solver. Translation fidelity must be scored separately from task execution.

## Limits

This pilot tests exact synthetic instruction following. It does not test latent human values, strategic deception, corrigibility, open-world tool use, or control of a system much more capable than its overseer. The investigator designed the language, corpus, and audit. The post-run exclusion is scientifically necessary but not preregistered; both the original and audited estimates are therefore reported. Independent replication, blinded prompt-equivalence review, more model families, human authoring-time measurement, and natural tasks are required.

## Artifacts

- `formal_notation_tasks.json` — paired corpus
- `FORMAL_NOTATION_PREREGISTRATION.md` — frozen design and development-driven edits
- `run_formal_notation_eval.py` — model runner and mechanical scorer
- `{args.result.name}` — complete raw held-out record
- `SPEAR_Benchmark_002_Audit.json` — full and audited summaries with exclusion reason
- `SPEAR_Benchmark_002_Rows.csv` — tidy rows with `audit_included`
"""
    report_path = args.result.parents[1] / "BENCHMARK_002.md"
    report_path.write_text(report)
    print(report_path)
    print(audit_path)
    print(csv_path)
    print(json.dumps({"full": full["overall"], "audited": audited["overall"], "paired": audited["paired"]}, indent=2))


if __name__ == "__main__":
    main()
