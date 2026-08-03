# Benchmark 001: paired on-task adherence

**Date:** 2026-08-02  
**Protocol tested:** SPEAR/0.2  
**Status:** small synthetic held-out pilot; reproducible, not confirmatory evidence for open-world alignment

## Question

When the same task facts are expressed in ordinary prose or through a SPEAR interpretation contract and field structure, how often does a model return the exact requested result and output contract?

## Result

Across four model tiers and 16 held-out tasks per tier, ordinary prose was exactly on task in **46/64 cases (71.9%)**. SPEAR/0.2 was exactly on task in **57/64 cases (89.1%)**: an absolute lift of **17.2 percentage points**, or **23.9% more exact successes relative to the prose baseline**.

| OpenRouter model | Ordinary prose | SPEAR/0.2 | Absolute lift |
|---|---:|---:|---:|
| GPT-4o mini | 5/16 (31.3%) | 11/16 (68.8%) | +37.5 points |
| GPT-5.6 Luna | 14/16 (87.5%) | 15/16 (93.8%) | +6.3 points |
| GPT-5.6 Terra | 13/16 (81.3%) | 15/16 (93.8%) | +12.5 points |
| GPT-5.6 Sol | 14/16 (87.5%) | 16/16 (100.0%) | +12.5 points |
| **All observations** | **46/64 (71.9%)** | **57/64 (89.1%)** | **+17.2 points** |

The mean expected-field constraint score rose from **80.1%** to **92.1%**. Among the 15 model-task pairs where the two conditions differed, SPEAR repaired 13 prose failures and introduced 2 failures. This aggregate paired count is descriptive: observations share tasks and model families, so it should not be treated as 64 independent human-AI interactions.

The held-out run’s provider-reported cost was **$0.0935**: $0.0364 for prose and $0.0571 for SPEAR. The structured condition used a longer system instruction, so the intervention was about reliability rather than token or dollar efficiency.

## Design

- 16 synthetic held-out tasks spanning selection, ordering, allocation, unit conversion, authority, source precedence, stop conditions, nested exceptions, value of information, and exact output contracts.
- Four progressively capable operational tiers: `openai/gpt-4o-mini`, `openai/gpt-5.6-luna`, `openai/gpt-5.6-terra`, and `openai/gpt-5.6-sol`.
- Every model received every task in both conditions. Task facts were held constant; the intervention was the SPEAR/0.2 interpretation prompt plus structured fields.
- GPT-5.6 models used low reasoning effort; GPT-4o mini used provider defaults. A fixed seed was requested. There was one observation per condition after development because deterministic repeats in the pilot duplicated outputs.
- Every answer was requested as JSON. “On task” required exact equality with preregistered expected JSON. A recursive expected-leaf score captured partial constraint adherence. No model graded another model.
- Raw responses, model/provider metadata, token usage, provider-reported cost, errors, latency, and the task-file SHA-256 are retained.

## What changed between SPEAR/0.1 and 0.2

The first development run made SPEAR/0.1 look worse than prose. Audit found both genuine protocol failures and benchmark defects. Version 0.2 added:

1. **AUTHORITY** — explicit allowed, approval-required, and prohibited actions; semantic equivalents inherit the same rule.
2. **PRECEDENCE & VOCABULARY** — exception, source, objective, and tie-break order plus canonical labels that should be copied rather than paraphrased.
3. **STOP** — non-compensatory gates and consequential actions that require a pause.
4. **CHECK** — an independent pass over constraints, sums, units, order, schema, labels, and authority before output.

The development process also caught an impossible expected schedule, two incorrect held-out answer keys before any held-out calls, a non-equivalent source label across paired prompts, and an OpenRouter new-account Sol rate limit. These were corrected or rate-limited before the held-out run. The invalidated runs remain in `experiments/results/`.

## Limits

This pilot measures exact synthetic instruction following. It does not measure whether a model inferred a person’s latent values, resisted strategic manipulation, preserved authority during tool use, or behaved safely in an open world. Several “failures” were semantically correct answers with a wrong key or canonical phrase; that strictness is relevant to machine-readable contracts but should not be confused with total task failure.

The task author also designed SPEAR, the tasks, and the scoring rules. The sample is small, contains one response per final condition, and uses related model families. The result needs independent replication, more natural tasks, blinded task authors, human authoring-time measures, adversarial prompts, tool-use environments, and preregistered statistical analysis.

## Artifacts

- `tasks.json` — paired task corpus and expected JSON
- `run_openrouter_eval.py` — runner and mechanical scorer
- `results/20260802T184929Z-held_out-spear-0.2.json` — raw held-out record
- `results/SPEAR_Benchmark_001_Rows.csv` — tidy row-level outcomes
