# Benchmark 003: Fields × Interpretation Contract

## Preregistration draft for named human review

**Status:** Draft only; not yet registered and not authorized for paid execution

**Prepared:** 3 August 2026

**Intended registry:** Open Science Framework

This document specifies a prospective factorial experiment motivated by Benchmarks 001
and 002. It must receive named human methodological review, a frozen corpus hash, a
model-and-provider manifest, and an approved maximum-cost gate before it is submitted as
an immutable registration or used for paid model calls.

## Development equivalence preflight (not registration evidence)

A single synthetic development fixture now exercises the proposed canonical-record path:
deterministic A-D renderers, condition-level semantic inventories, and source-bound atom
traces. Each trace binds an exact rendered span and source role to an independently resolved
JSON Pointer. Traversal-derived coverage includes task text; entity identifiers and labels;
fact identifiers, entity links, attributes, and values; constraint kinds, operators, targets,
failure labels, and outcome labels; authority levels and actions; canonical-label identifiers
and values; and output keys and types. Duplicate JSON keys are rejected. Exact
canonical/expected output-cue counts and fail-closed renderer-corruption tests remain separate
checks. Independently frozen prompt-skeleton hashes cover untraced relation words, field names,
negation, and output imperatives for the frozen development-audited base and empty-authority
profiles; other structures fail closed pending a new human-reviewed hash. Frozen system-prompt
hashes and source-derived lexeme counts
guard the interpretation contract. Each condition renders from an isolated source snapshot, and
the prompts bind `blocking=[]` on pass plus gate-then-condition failure ordering. It runs offline:

```bash
python3 experiments/benchmark_003_equivalence_preflight.py
python3 -m unittest experiments/test_benchmark_003_equivalence_preflight.py -v
```

This is an exploratory development control only. It makes no model calls, spends nothing,
does not create or inspect a held-out corpus, and does not satisfy the unchecked freeze or
registration gate below. The validator can bind controlled source atoms to exact prompt spans,
establish equality of its controlled semantic surfaces, and detect exact scalar cues. It cannot
prove equivalence of arbitrary paraphrases, validate pragmatic emphasis, or rule out every
answer cue. Blinded human review remains required.

## Research question

Benchmark 001 combined structured SPEAR fields with a system-level interpretation
contract. Benchmark 002 found no benefit from strict mathematical notation alone after a
prompt-equivalence audit. Benchmark 003 asks which of two components changes exact
on-task adherence:

1. expressing equivalent task information in explicit SPEAR fields; and
2. supplying the SPEAR interpretation contract at system level.

## Design

The experiment is a preregistered 2 × 2 factorial design.

| Condition | Task representation | System interpretation contract |
|---|---|---|
| A | ordinary prose | absent |
| B | SPEAR fields | absent |
| C | ordinary prose | present |
| D | SPEAR fields | present |

All four conditions must contain the same task facts, constraints, authority boundaries,
canonical output labels, and output schema. The interpretation contract may explain how
to read fields, but it may not add task-specific facts or answer cues. The prose conditions
must not receive weaker output instructions.

## Corpus and freezing

- Create 40 previously unused tasks across at least eight task families, with no task
  copied from Benchmarks 001 or 002.
- Include authority, precedence, exception, constrained optimization, stop-gate,
  information-value, reconciliation, and exact-output tasks.
- Keep a development set separate from the 40-task held-out set.
- Author each task once in a canonical machine-readable semantic record. Render conditions
  A–D deterministically from that record; do not maintain four independently edited held-out
  prompts.
- Run an automated equivalence preflight before freezing. It must compare condition-level
  facts, numeric literals, constraints, authority boundaries, canonical labels, output keys and
  types, named entities, and expected-answer cues, with every exception documented and reviewed.
- Mutation-test both rendered spans and semantic surfaces. Change fact values and attributes,
  entity links and labels, constraint kinds/operators/targets/failure and outcome labels,
  authority levels/actions, task text, output keys/types, and answer cues in turn; every mutation
  must fail closed even if trace and artifact integrity hashes are refreshed. Repeated renders of
  the unmodified source must be byte-identical.
- Freeze the corpus, expected answers, scorer, condition templates, and analysis script;
  record their SHA-256 hashes in the registration before any held-out call.
- Publish an externally timestamped registration containing those hashes before any held-out
  request. A repository commit made after execution is not sufficient evidence of preregistration.
- Anyone who has read held-out expected answers may not alter the prompts after freezing.

## Model panel and repetitions

- Include models from at least three independent provider families.
- Freeze exact model identifiers, provider routing, inference settings, and repetition count
  in the registration update before execution.
- Use identical settings across the four conditions wherever the provider permits.
- Randomize condition order within each task-model-repetition block using a recorded seed.
- Do not begin paid execution until a human approves a maximum total cost and a stop rule.

## Outcomes

### Primary outcome

Exact normalized equality with the preregistered expected output, scored deterministically
without an LLM judge.

### Secondary outcomes

- recursive expected-field agreement;
- deterministic semantic decision correctness reported separately from schema, key, and
  canonical-label adherence, so serialization repairs are not counted as reasoning repairs;
- parse validity and exact output-schema validity;
- unauthorized-action and hard-constraint violation counts;
- prompt and completion tokens, latency, and provider-reported cost;
- condition-specific refusal or clarification behavior.

## Estimands and analysis

Report raw counts and percentages for every condition, model, and task family. The primary
estimands are:

1. the average effect of field structure: `(B + D) / 2 − (A + C) / 2`;
2. the average effect of the interpretation contract: `(C + D) / 2 − (A + B) / 2`;
3. the interaction: `(D − C) − (B − A)`.

Compute paired differences within task-model-repetition blocks. Report a task-clustered
bootstrap 95% interval for each estimand using a preregistered random seed, plus exact
discordant-pair counts for transparent sensitivity analysis. Do not treat calls sharing a
task or model as independent observations. Correct any family of confirmatory p-values with
Holm's method. Label all task-family and individual-model comparisons exploratory.

## Audit and exclusion rules

- Preserve every API response, error, retry, invalid output, and provider-routing record.
- Use an append-only raw ledger. The strict JSON parser must reject duplicate keys and
  non-standard `NaN`/`Infinity` values, and the frozen scorer must define empty-list and
  empty-object behavior before execution.
- Exclude a call only for a preregistered infrastructure failure such as a transport error
  that produced no model response. Retry rules must be mechanical and condition-blind.
- Never exclude a syntactically invalid, refused, or incorrect model response from outcome
  scoring.
- If any condition pair contains unequal task facts or an answer cue, publish the defect and
  report both the full preregistered result and an audited sensitivity analysis. Do not
  silently repair held-out prompts and rerun them as though they remain unseen.

## Interpretation boundaries

A positive result would show that a particular representation or interpretation contract
improved exact adherence in this bounded task suite. It would not establish recovery of
latent human values, alignment, deception resistance, political legitimacy, or safety in
open-world deployment. A null or negative result narrows the protocol claim and remains a
publishable outcome.

## Required human gates before registration

- [ ] Named human scientific reviewer and conflict disclosure
- [ ] Final task-family allocation and authoring procedure
- [ ] Frozen model/provider manifest and repetition count
- [ ] Approved maximum-cost and budget stop
- [ ] Frozen corpus, scorer, templates, hashes, and randomization seed
- [ ] Passing mutation-tested equivalence preflight and externally timestamped OSF registration
- [ ] Privacy, licensing, and public-release review
