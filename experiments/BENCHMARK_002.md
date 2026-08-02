# Benchmark 002: mathematical notation versus vernacular

**Date:** 2026-08-03  
**Status:** paired synthetic pilot with a disclosed post-run prompt-equivalence exclusion

## Question

When facts, model, system instruction, output contract, seed request, and mechanical scoring are held constant, does adding typed mathematical notation improve exact on-task performance over concise vernacular?

## Result

On the preregistered 20-task set, vernacular was exactly on task in **134/160 (83.8%)** observations and formal notation in **138/160 (86.3%)**: **+2.5 points**.

A post-run prompt-equivalence audit found one asymmetric task (`test-math-14-workflow`). The formal condition put the exact expected phrase `open the vote` inside its output template; the vernacular condition did not define that canonical string. That task contributed eight formal repairs and no regressions—more than the entire aggregate lift. It is retained in the raw record and excluded only in the clearly labeled audit sensitivity.

On the remaining 19 equivalent tasks, vernacular was exactly on task in **134/152 (88.2%)** and formal notation in **130/152 (85.5%)**: **-2.6 points**. The defensible conclusion is that **notation alone did not establish an improvement**.

| Model | All-task vernacular | All-task formal | All-task lift | Audited vernacular | Audited formal | Audited lift |
|---|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini | 60.0% | 52.5% | -7.5 points | 63.2% | 50.0% | -13.2 points |
| gpt-5.6-luna | 90.0% | 95.0% | +5.0 points | 94.7% | 94.7% | +0.0 points |
| gpt-5.6-terra | 90.0% | 100.0% | +10.0 points | 94.7% | 100.0% | +5.3 points |
| gpt-5.6-sol | 95.0% | 97.5% | +2.5 points | 100.0% | 97.4% | -2.6 points |

Across the audited set there were 4 formal repairs and 8 formal regressions. The descriptive exact McNemar p-value is 0.388; repeated tasks and related model families mean it is not a confirmatory significance test.

## What the capability pattern suggests

The smallest model lost 13.2 points under notation. Luna was unchanged, Terra gained 5.3 points, and Sol lost 2.6 points on the audited set. This non-monotonic interaction is descriptive and needs a larger, independently authored replication. It argues against a universal "more symbols is better" rule.

## Design

- 20 held-out synthetic tasks, two repetitions, two paired conditions, and four model tiers; 320 total API calls and no provider errors.
- The same JSON-only system instruction was used in both conditions. GPT-5.6 models used low reasoning effort; GPT-4o mini used provider defaults.
- Exact equality with preregistered JSON was the primary endpoint; recursive expected-leaf match was secondary.
- Two direct tasks served as negative controls. Both conditions scored 16/16 on them.
- Provider-reported held-out cost was $0.1620.

## Interpretation for SPEAR

Mathematical notation should be a selectively compiled layer, not a universal surface language. A stronger next test is a three-way comparison: plain vernacular; a dual-register SPEAR contract with typed fields and plain-language gloss; and the same contract compiled to executable checks or a solver. Translation fidelity must be scored separately from task execution.

## Limits

This pilot tests exact synthetic instruction following. It does not test latent human values, strategic deception, corrigibility, open-world tool use, or control of a system much more capable than its overseer. The investigator designed the language, corpus, and audit. The post-run exclusion is scientifically necessary but not preregistered; both the original and audited estimates are therefore reported. Independent replication, blinded prompt-equivalence review, more model families, human authoring-time measurement, and natural tasks are required.

## Artifacts

- `formal_notation_tasks.json` — paired corpus
- `FORMAL_NOTATION_PREREGISTRATION.md` — frozen design and development-driven edits
- `run_formal_notation_eval.py` — model runner and mechanical scorer
- `20260802T221708Z-held_out-formal-notation.json` — complete raw held-out record
- `SPEAR_Benchmark_002_Audit.json` — full and audited summaries with exclusion reason
- `SPEAR_Benchmark_002_Rows.csv` — tidy rows with `audit_included`
