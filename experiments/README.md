# SPEAR paired benchmark

This benchmark asks whether a compact interpretation contract and SPEAR field structure improve exact task adherence relative to ordinary prose containing the same task facts.

## Design

- Four OpenRouter-hosted model tiers are tested: GPT-4o mini, GPT-5.6 Luna, Terra, and Sol.
- Each model receives every task in both `plain` and `spear` conditions.
- Outputs are scored mechanically against preregistered JSON. No model grades another model.
- Development tasks may be used to revise the protocol. Held-out tasks are not inspected until the protocol version is fixed.
- Exact equality is the strict “on task” outcome. Recursive expected-field agreement is reported as a softer constraint score.
- The fixed seed is requested and raw outputs, token usage, provider attribution, errors, task-file hash, and reported cost are retained.

This is a synthetic instruction-following pilot, not evidence that SPEAR solves alignment or preserves human intent in open-world settings. Its purpose is to expose failure modes and make the next experiment more rigorous.

## Run

```bash
export OPENROUTER_API_KEY='...'
python3 experiments/run_openrouter_eval.py --split development --spear-version 0.1 --repetitions 2
python3 experiments/run_openrouter_eval.py --split held_out --spear-version 0.2 --repetitions 1
```

The secret is read from the environment and is never written into results.

## Benchmark 002: notation versus vernacular

Benchmark 002 holds facts, system instruction, output contract, and mechanical scoring constant while changing the task representation. It isolates typed mathematical notation rather than testing the full SPEAR protocol.

```bash
python3 experiments/validate_formal_notation_tasks.py
python3 experiments/run_formal_notation_eval.py --split held_out --repetitions 2
```

The preregistered aggregate appeared to favor notation by 2.5 points. A post-run equivalence audit found one asymmetric canonical-answer cue. On the remaining equivalent tasks, notation scored 2.6 points below vernacular. See [`BENCHMARK_002.md`](BENCHMARK_002.md) for both estimates, limits, and the next design.

## Benchmark 003: development equivalence preflight

Benchmark 003 remains a preregistration draft with no paid execution authorization. Its first development-only milestone renders conditions A-D deterministically from isolated copies of one canonical semantic record. Ordered atom traces bind exact prompt spans to independently resolved JSON Pointers for task, entity, fact, constraint, authority, label, and output-schema content. Independently frozen user-prompt skeleton and system-prompt hashes cover untraced glue and system constants. The validator also rejects duplicate JSON keys and compares semantic surfaces and exact canonical/expected output-cue counts. Corruption tests refresh offsets, trace hashes, and artifact hashes after changing representative atoms or untraced relations; the independent controls must still fail closed.

```bash
python3 experiments/benchmark_003_equivalence_preflight.py
python3 -m unittest experiments/test_benchmark_003_equivalence_preflight.py -v
```

This fixture is exploratory development evidence, not a frozen corpus, held-out result, or proof of arbitrary natural-language equivalence. Human equivalence review and every gate in [`BENCHMARK_003_PREREGISTRATION_DRAFT.md`](BENCHMARK_003_PREREGISTRATION_DRAFT.md) remain required.

The 5 August audit narrowed that claim further. Newline and reserved-heading strings in
task text, entity labels, fact attributes, and authority actions can still receive a
fixture-internal `PASS`; the contract factor also replaces rather than adds to the common
baseline, and the implemented templates need a human construct-validity decision. A
two-stage, condition-label-masked and oracle-withheld review bundle now packages those
negative findings for a named independent human:

```bash
python3 experiments/benchmark_003_build_review_packet.py --help
python3 -m unittest experiments/test_benchmark_003_build_review_packet.py -v
```

See [`BENCHMARK_003_HUMAN_REVIEW_PROTOCOL.md`](BENCHMARK_003_HUMAN_REVIEW_PROTOCOL.md).
The coordinator nonce and A–D reveal must remain outside this public repository until the
Phase 1 response is sealed. This tooling means “ready for human review,” not equivalence
established, and cannot authorize fixture extension, registration, model calls, or spend.

### Unicode line-separator boundary audit

One additional offline development audit appends U+2028 LINE SEPARATOR plus a reserved
`HARD_GATES` heading to the canonical task field. The current validator preserves the marker
in all A–D prompts and still returns `PASS`; in this audit, that `PASS` is the negative result.

```bash
python3 experiments/benchmark_003_unicode_line_separator_audit.py
```

This is one synthetic boundary test, not model-behavior or held-out evidence. See the
[`7 August audit report`](../research/reports/2026-08-07-on-demand-unicode-boundary-audit.md).
