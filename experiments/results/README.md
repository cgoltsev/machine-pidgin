# Result audit trail

All runs are retained, including invalidated development pilots.

## `20260802T184223Z-development-spear-0.1.json`

Invalidated for outcome claims. One development task asked for a schedule with no feasible slot while its answer key expected `10:00`. Twelve Sol observations also hit a documented new-account rate limit. The apparent condition differences were used only to find protocol and benchmark problems.

## `20260802T184712Z-development-spear-0.2.json`

Development-only. The impossible schedule and two answer-key arithmetic errors were corrected before this run. Inspection found that the SPEAR version of one provenance task named a source `contract` while the prose condition and exact answer named it `signed contract`; four identical semantic answers were therefore counted wrong only in the SPEAR condition. The mismatch was corrected before held-out evaluation. This run informed the canonical-vocabulary rule and is not a confirmatory result.

## `20260802T184929Z-held_out-spear-0.2.json`

Primary held-out pilot. Sixteen untouched held-out task prompts were run once per condition on each of four models after the protocol and scorer were fixed. No request errors occurred. See `../BENCHMARK_001.md` for methods, results, and limits.

## `20260802T221708Z-held_out-formal-notation.json`

Complete Benchmark 002 held-out record: 20 tasks, two paired conditions, two repetitions, and four model tiers (320 calls, no request errors). The preregistered aggregate showed a +2.5-point formal effect. A post-run equivalence audit found that `test-math-14-workflow` supplied the expected canonical label only in the formal prompt. The raw record is unchanged.

`SPEAR_Benchmark_002_Audit.json` reports the full and 19-task audited sensitivity estimates, the exclusion reason, and paired discordances. `SPEAR_Benchmark_002_Rows.csv` marks every row with `audit_included`. `20260802T222904Z-benchmark-002-model-panel.json` contains prompted critiques from four model instances; it is not evidence of persistent awareness or independent authorship. See `../BENCHMARK_002.md`.

## `20260802T221234Z-development-formal-notation.json`

Development-only, one repetition per condition across eight tasks and four model tiers. Vernacular scored 26/32 and formal notation 23/32, an observed -9.375-point difference, with no request errors. The recorded task hash is `3912786ed9c2aae6ba7c647c1f046478dc6c734165a063ee6fb02bff1edd5bae`; that exact corpus version is no longer present, so this run is not fully reproducible from the current tree. The original bytes are retained as audit evidence and the result is not confirmatory.

## `20260802T221505Z-development-formal-notation.json`

Development-only, one repetition per condition across the current eight-task development corpus and four model tiers. Vernacular scored 28/32 and formal notation 26/32, an observed -6.25-point difference, with no request errors. Its task hash matches the retained corpus. This run preceded held-out execution, may have informed debugging, and is not a confirmatory estimate.

## Model-panel audit artifacts

`20260802T222812Z-benchmark-002-model-panel.json` is the first prompted model-panel run. It used the unaudited all-task aggregate because no audit file was available to the runner, and is superseded by `20260802T222904Z-benchmark-002-model-panel.json`, which includes the post-run equivalence audit. Both are retained as prompted critiques rather than scientific evidence. `../run_model_panel.py` is the generator for these artifacts.
