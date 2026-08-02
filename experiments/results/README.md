# Result audit trail

All runs are retained, including invalidated development pilots.

## `20260802T184223Z-development-spear-0.1.json`

Invalidated for outcome claims. One development task asked for a schedule with no feasible slot while its answer key expected `10:00`. Twelve Sol observations also hit a documented new-account rate limit. The apparent condition differences were used only to find protocol and benchmark problems.

## `20260802T184712Z-development-spear-0.2.json`

Development-only. The impossible schedule and two answer-key arithmetic errors were corrected before this run. Inspection found that the SPEAR version of one provenance task named a source `contract` while the prose condition and exact answer named it `signed contract`; four identical semantic answers were therefore counted wrong only in the SPEAR condition. The mismatch was corrected before held-out evaluation. This run informed the canonical-vocabulary rule and is not a confirmatory result.

## `20260802T184929Z-held_out-spear-0.2.json`

Primary held-out pilot. Sixteen untouched held-out task prompts were run once per condition on each of four models after the protocol and scorer were fixed. No request errors occurred. See `../BENCHMARK_001.md` for methods, results, and limits.

