# Researcher report — weekly cycle of 3 August 2026

**Cycle status:** Completed without a reportable security, privacy, spend, legal,
governance, research-integrity, or account incident.

**Evidence boundary:** Literature findings are exploratory synthesis. The code result is
development evidence. No validation or held-out evidence was generated.

**Authorship:** Prepared by the Machine Pidgin AI Researcher for human review; capability
does not confer governance, publishing, spending, moderation, or account authority.

## Baseline and change audit

Before research work, the Researcher read the current Constitution, Governance,
Code of Conduct, repository boundaries, privacy and security notices, contact and operating
documents, research protocols, prior Director memory, and the available founding preprint.
This was the first completed Researcher cycle, so the most recent AI Director automation
memory available at the start of the run was used as the delta baseline; no separate
Director research-handoff file was present.

Both repositories were inspected under their documented boundaries; no private operational
content is reproduced here. Read-only public-state checks found no later change in the
public repository, its open issue/PR/review state, GitHub Discussions, approved public
forum topics/replies, or aggregate public proposal count.
The public repository had no issues and two pre-existing draft PRs, [#1](https://github.com/cgoltsev/machine-pidgin/pull/1)
and [#3](https://github.com/cgoltsev/machine-pidgin/pull/3), with no reviews or checks that
resolve their human-review gates. The unauthenticated public forum reported five approved
topics, zero replies, zero pending-review items, and no public proposal content. No public
research submission was therefore available to assess. Private intake content was not read
or copied.

## Canon and current literature

The first living [literature canon](../LITERATURE_CANON.md) now contains 16 normative or
stable specifications, 13 empirical/evaluation sources, 14 conceptual foundations, and 7
explicitly provisional adjacent sources. There were no removals because this is the initial
canon. Each entry records a primary citation, provenance/status, a Researcher inference for
SPEAR, and a limitation. Citation count is not used as validation.

The bounded [current-literature scan](../scans/2026-08-03-current-literature.md) covered
3 August 2025–3 August 2026. Highest-value additions were:

- peer-reviewed MOSAIC evidence that constraint type, number, order, and model interact;
- peer-reviewed AgentSpec runtime-enforcement results and their rule-recall limits;
- provisional Many-Tier Instruction Hierarchy evidence about authority-tier and
  representation sensitivity;
- MCP 2026-07-28 and A2A 1.0.x as current transport/interoperability substrates that do
  not establish legitimate authority;
- the NIST agent identity/authorization initiative and evaluation-practice draft, both
  correctly retained as unfinished work rather than standards;
- W3C AI and cognitive-accessibility drafts, retained as non-normative work in progress;
- evolving-intent, multi-turn, fidelity, and TLA+ benchmark work that suggests future
  revision, recovery, preservation, and formal-compilation tests.

The strongest negative literature result was conceptual rather than numerical: no primary
source found in this bounded scan showed that protocol interoperability, a signed identity,
or authorization metadata alone establishes legitimate human authority, preserved intent,
or safe action.

## Public research watchlist

The [watchlist](../RESEARCH_WATCHLIST.md) records twelve public groups or author teams as
“research we are learning from,” never as collaborators, supporters, or affiliates. The
highest-priority Director follow candidates are NIST CAISI/NCCoE, MCP maintainers, the A2A
Project, and W3C accessibility/semantic-web groups. No follow, message, like, repost,
subscription, or other account action was taken.

## The one selected agenda

**Question:** Can deterministic rendering plus fail-closed equivalence validation catch
task-fact and answer-cue asymmetries among Benchmark 003 conditions A–D before a corpus is
frozen?

**Hypothesis / decision target:** One canonical development record will render A–D
byte-deterministically and pass equivalence validation, while changing any task fact,
numeric literal, named entity, canonical label, output key, expected answer, or answer cue
will fail closed. Passing would justify extending this control to a small reviewed
development corpus; failure would require redesign before any registration or model call.

**Why it matters to SPEAR:** Benchmark 002’s apparent notation gain was explained by one
formal condition containing an exact answer label absent from its pair. Benchmark 003
cannot credibly estimate field or interpretation-contract effects unless task semantics and
answer cues are prospectively equivalent.

**Prior evidence:** Benchmark 002’s audit, ISO/IEC/IEEE 29148 traceability principles,
MOSAIC’s constraint-interaction findings, and fail-safe/default and formal-validation work
in the canon.

**Falsification criteria:** Any required mutation passes; a clean repeated render differs;
factor isolation fails; artifact/source integrity or oracle checks can be bypassed; or a
condition carries a different controlled semantic surface or answer-cue count.

**Safety and privacy constraints:** Synthetic development data only; no participant or
private data; no secrets; no external API or model call; no held-out inspection; no claim of
arbitrary natural-language equivalence; no spend; human review remains mandatory.

**Scoped completion test:** Deterministic clean A–D render and equivalence PASS, plus
fail-closed tests for all listed mutation classes, runnable offline from a documented
command. This test was met for one development fixture.

## Development result and reproduction

Created one synthetic [canonical record](../../experiments/benchmark_003_development_fixture.json),
a [deterministic renderer and validator](../../experiments/benchmark_003_equivalence_preflight.py),
and a [27-test mutation suite](../../experiments/test_benchmark_003_equivalence_preflight.py).
The validator independently traverses the validated canonical source and binds 52 ordered
source atoms in each condition to exact prompt spans. It covers task, entities, facts,
constraints, authority (including empty levels), labels, and output schema, plus the
deterministic expected answer, counterfactual answer-cue counts, frozen system prompts,
independently frozen prompt skeletons, factor isolation, provenance, duplicate-key
rejection, source immutability at both the single- and four-condition render boundaries,
and integrity hashes. The frozen, development-audited skeleton profiles cover the base
fixture and an all-empty-authority variant; other prompt structures fail closed.

```bash
python3 experiments/benchmark_003_equivalence_preflight.py
python3 -m unittest experiments/test_benchmark_003_equivalence_preflight.py -v
python3 -m py_compile \
  experiments/benchmark_003_equivalence_preflight.py \
  experiments/test_benchmark_003_equivalence_preflight.py
git diff --check
```

Observed result: CLI `PASS`; repeated renders byte-identical; factor isolation `true`;
27/27 tests `OK`; compilation, fixture parsing, the existing Benchmark 002 task validator,
and diff checks pass. Canonical semantic-record SHA-256:
`8298cf6b4659b7560423a522eab135bc6890ef4f413d091763ec76f16a9b7515`.
An AI-assisted adversarial review first produced a false `PASS` by changing a rendered fact
while refreshing its hashes, then found false passes in untraced template grammar, renderer
mutation of the shared source, and task-specific system-contract leakage. Those blockers
were closed with source-bound atom validation, independently frozen prompt skeletons and
system contracts, per-condition source copies with immutability checks, and recursive
source-derived leak detection. An independent AI-assisted re-review reproduced 18 historical
attacks without a pass. This was not independent human review.

**Calls and spend:** model calls `0`; provider calls `0`; paid services `0`; exact spend
`$0.00`. No provider, budget, or approval state was assumed. The Institute-wide ceiling was
not treated as spending authorization.

This is a successful independently useful milestone, but the broader Benchmark 003 agenda
remains **incomplete**. The fixture is narrow, its cue check is lexical rather than
pragmatic, and its frozen skeletons cover only two development-audited structural profiles.
Externally frozen raw-source hashes still belong in the future registration pipeline. There
is no held-out result and no evidence about model performance.

## Public submissions and community value

No eligible public forum research submission, public proposal text, GitHub issue, or
Discussion existed at check time, so none could be scored for relevance, method,
reproducibility, safety, licensing, or public value. This is a negative result, not missing
fabricated work.

The code and literature artifacts are material enough for a draft review, but not for a
scientific news claim. Suggested Director-routed copy, held until a reviewed public artifact
URL exists:

> Constraint following is not one capability. EACL 2026’s MOSAIC found model-specific
> interactions and order effects across prompts with up to 20 constraints. Our first
> offline Benchmark 003 milestone now checks condition equivalence and deliberately mutates
> facts, labels, keys, entities, numerics, static prompt grammar, source state, expected
> answers, and answer cues before any model call. Development evidence only; reproduction
> and critique welcome. AI-assisted draft.

No media or forum post was made.

## Limitations, anomalies, and required review

- The literature scan was bounded, English-language, and index-dependent rather than a
  systematic database review; several highly relevant 2026 sources are drafts or preprints.
- MCP 2026-07-28’s overview appears to retain wording about extension negotiation “during
  initialization” although the same release removes initialization. This is a non-urgent
  documentation anomaly, not a security incident.
- Public checks cannot establish the existence or absence of undisclosed or off-platform
  submissions. Private intake content was not accessed.
- Human review is still required for the existing draft PRs and for this cycle’s draft.
- Before Benchmark 003 registration or any paid execution: name a human scientific
  reviewer; disclose conflicts; finalize task families and authoring; freeze corpus,
  templates, scorer, analysis, model/provider manifest, seed, and hashes; approve a maximum
  cost and stop; externally timestamp the OSF registration; and complete privacy,
  licensing, and release review. Immediately before a paid call, separately verify the
  exact provider identity, artifact-specific named human approval, remaining approved
  artifact budget, and current Europe/Athens-day spend across every known provider.
- No governance vote is requested by this development-only cycle.

## Highest-value next research action

Have a named, blinded human reviewer challenge the canonical-record schema and mutation
oracle, then extend the same offline preflight to a tiny, diverse development fixture set
crossing constraint order, authority tiers, and evolving-intent revisions. Do not design the
held-out corpus or make paid calls until that review is recorded.
