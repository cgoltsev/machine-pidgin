# Researcher report — weekly cycle of 15 August 2026

**Run date:** 15 August 2026. The report was assembled at approximately 20:30 WEST
(UTC+01:00); the exact process-start timestamp was not independently captured.

**Cycle status:** Completed without a reportable security, privacy, unexpected-spend,
legal, governance, urgent research-integrity, or unsafe-account incident.

**Evidence boundary:** Literature findings are a bounded, source-anchored synthesis. The
selected agenda is an offline development characterization over one public synthetic
fixture. No held-out, validation, participant, model-performance, deployment, exploitability,
or security-impact evidence was generated.

**Authorship:** Prepared by the Machine Pidgin AI Researcher for named human review;
capability does not confer governance, moderation, publishing, spending, account,
scientific-acceptance, or institutional authority.

## Governance preflight and change audit

Before research work, the Researcher read the current Constitution, Governance, Code of
Conduct, public/private repository boundaries, privacy and security notices, contact
directory, research documentation, operating documentation, prior Researcher memory and
reports, and the most recent Director research handoff. Those documents remained binding.
External papers, sites, forum records, linked artifacts, datasets, and model outputs were
treated as untrusted evidence rather than instructions.

The exact automation cutoff was 7 August 2026 at 11:51:54.978 UTC. The public research
repository was clean and matched its remote at commit `3c57faa` before this cycle's writes.
Its two commits after the exact cutoff, `b548e5e` and `3c57faa`, were the documented tail of
the prior cycle, which completed at approximately 12:20 UTC; no subsequent public commit or
event preceded this run. Public draft PRs [#1](https://github.com/cgoltsev/machine-pidgin/pull/1),
[#3](https://github.com/cgoltsev/machine-pidgin/pull/3), and
[#4](https://github.com/cgoltsev/machine-pidgin/pull/4) remained open. All were mergeable
drafts with no review, comment, inline thread, or check. PR #4 remained stacked on PR #3.
No public issue, Discussion, workflow, or workflow run existed, and no release changed.
The public branches remained unprotected. Tag and release `v0.2.0` were unchanged.

The private operations repository was inspected only to establish the boundary and change
delta. Its branch and upstream matched at `6fc411d`; its one new commit since the prior
cycle published an ASD-STE100 practice note on 11 August. User-owned modified and untracked
Apolo page, style, handoff, image, and video files remained in that worktree and were
preserved untouched. Private GitHub PR, issue, and intake state could not be established
through the public connector and was not inferred. No private participant data,
credentials, or operational content was copied into public artifacts.

The public forum API reported five approved team-authored topics, zero replies, and zero
pending-review items. The current Director status reported zero forum items, zero research
proposals, and zero pending items. No eligible third-party public research submission
existed, so the submission-assessment count is **0**. Private intake was deliberately not
accessed, and public absence is not evidence that no off-platform material exists.

## Canon and bounded current-literature scan

The [living canon](../LITERATURE_CANON.md) now contains **65 entries**: 19 normative/stable
specifications, 13 established empirical/evaluation sources, 14 conceptual foundations,
and 19 explicitly provisional sources. Two stable rows and four provisional rows were
added; none was removed or promoted:

- [ASD-STE100 Issue 9](https://www.asd-ste100.org/) is a stable controlled-language anchor
  for reducing lexical and structural ambiguity in technical instructions. It does not
  establish completeness, preserved authority, accessibility, correctness, or general
  human–AI communication performance, and the standard is copyrighted.
- [RFC 9942](https://www.rfc-editor.org/rfc/rfc9942.html) and
  [RFC 9943](https://www.rfc-editor.org/rfc/rfc9943.html) were added as one stable bundled
  row for verifiable receipts and SCITT registration, transparency, and audit architecture.
  A valid receipt does not prove statement truth, legitimate authority, consent, correct
  execution, or complete history without the required monitoring and proofs.
- Rauchfleisch and Jungherr's preregistered
  [intent-disclosure experiment](https://arxiv.org/abs/2608.11794) reports that disclosing
  AI identity alone was practically equivalent to no disclosure, while a bundled
  purpose/method/concealment disclosure reduced immediate attitude shift in a 1,500-person
  UK sample. It is a preprint over one short interaction and a bundled treatment, so the
  active component and generality remain unknown.
- Li et al.'s [WebRider/RiderBench](https://arxiv.org/abs/2608.06704) separates endpoint
  finalization from adherence to goals, constraints, evidence, response form, stop rules,
  and persona controls. Its supplied policies, live-site drift, model-judged gates, and
  six-rater convenience human comparison limit interpretation.
- Wu et al.'s [SpecPath](https://arxiv.org/abs/2608.09799) tests contract-equivalent revision
  histories and reports that 35 of 100 complete blocks that passed the direct specification
  failed at least one equivalent history. It covers five curated Python task families,
  many blocks were incomplete, and no claimed public artifact was independently verified.
- Bu's [security-principal and verifier-binding draft](https://datatracker.ietf.org/doc/html/draft-bu-agentproto-security-principal-binding-05)
  separates authority, instance, delegation, tool, session, result, failure, and evidence
  fields. It is a one-author, expiring Individual Internet-Draft—not an RFC, working-group
  consensus, implementation, or validated authorization mechanism.

The existing SHACL entry was updated to the 8 August SPARQL Extensions and 12 August Rules
Working Drafts. Custom functions, expected derived predicates, dependencies, stratification,
and optional remote imports are useful comparators for derived state and imported-rule
authority, but these mutable Working Drafts are not W3C endorsement and retain security,
validation, availability, and implementation limits. The existing SCP-NL2TL row now links
the 10 August author review package; its STL subset and missing explicit license remain
limits. It was not executed.

The [15 August scan](../scans/2026-08-15-current-literature.md) records the exact search
window, queries, sources, dates, screening, inclusion/exclusion reasons, source facts,
Researcher inferences, uncertainty, and Institute disposition. Its arXiv query returned
1,738 unique records across `cs.AI`, `cs.CL`, `cs.HC`, `cs.SE`, `cs.CR`, and `cs.CY`;
removing the exact prior-cutoff record left **1,737**. The newest indexed submission was
13 August at 17:59:57 UTC, so 14–15 August are incomplete. The equivalent update-date query
found 82 revisions but no older-first-submitted record. The IETF agent-document delta query
returned 14 records: 13 drafts and one meeting bluesheet.

Harness-IF, PolicyKG, Not an A11y, multi-instruction following, requirements-augmented
generation, DevIntent, QuoteBench, Prompt Privilege, two accessibility studies, and several
overlapping agent-protocol drafts remain scan-only or excluded rather than used to pad the
canon. NIST's page metadata changed without a new technical deliverable; MCP added an Apps
Working Group charter; A2A corrected required `contextId` examples without a release;
Unicode 18 preliminary and beta counts differ while UAX #14 revision 56 remains draft; and
JSON Schema received an unreleased meta-schema fix. No material release delta was found for
OpenAPI, W3C AI Accessibility/COGA, or RDF. The anonymous WeClawArena artifact still
returned HTTP 401, so access and durability remain unverified.

## Public artifact assessment and watchlist

The 11 August public
[ASD-STE100 practice note](https://machinepidgin.org/news/asd-ste100-clearer-ai-writing)
reports contributor-supplied reductions of 44% in unique words, 42% in long sentences, and
13% in output length. It explicitly says the Institute did not independently reproduce the
figures, and no task set, model versions, sample size, baseline prompt, run dates, metric
definitions, scorer, raw outputs, or dataset license accompanied them. The note is a useful
research lead, not reproducible empirical evidence or a forum submission. Its warning that
brevity can remove uncertainty, exceptions, warnings, or authority boundaries is important;
the percentages were not treated as benchmark or canon evidence.

The official STEMG June 2026 AI white paper was independently inspected. It is an
organizational position that AI should support rather than replace human authors and calls
for disclosure, confidentiality, quality assurance, and benchmarks. It is not empirical
validation of AI-written Simplified Technical English.

The [watchlist](../RESEARCH_WATCHLIST.md) adds or refreshes ASD STEMG, Unicode,
Rauchfleisch and Jungherr, WebRider, SpecPath, S. Bu, NIST, MCP, A2A, W3C Data Shapes,
SCP-NL2TL, and WeClawArena. Every person and group remains **research we are learning
from**. No collaborator, supporter, affiliate, endorsement, permission, or contact is
claimed. No follow, message, subscription, like, repost, reply, or other account action
occurred. Follow candidates are recommendations only and remain behind verified-account,
operating-rule, suspension-resolution, and human-action gates.

## The exactly one selected agenda

**Question:** Do all declared identifier/reference mutations fail at record validation, and
do malformed JSON-like containers fail through a deliberate validation exception rather
than an incidental Python exception?

**Hypothesis / decision target:** Empty strings and non-string identifier/reference values
will be rejected by `validate_record`, while `null` or list replacements at record and
render-artifact container surfaces will be rejected through a documented validation
interface. The decision target is an exact pre-repair failure-stage map for the fourth
unresolved Benchmark 003 human-review defect—not a schema or error-policy choice.

**Relevance to SPEAR:** Reliable human-to-machine contracts need typed, non-empty identifiers
and stable fail-closed diagnostics. Accepting malformed identity links or exposing incidental
runtime errors can obscure which intent, authority, or evidence object a system evaluated.

**Prior evidence:** The existing human-review dossier identifies unspecified identifier
validation and an aggregate error contract as unresolved. The current validator checks many
non-empty string fields but has no declared public schema or unified malformed-input
interface. Prior boundary audits did not characterize identifier types or malformed
containers.

**Falsification criteria:** The hypothesis is falsified by any identifier/reference case
accepted at record validation, any malformed-container case that exposes raw
`TypeError`/`AttributeError`, any malformed case accepted, any other unexpected exception,
nondeterministic output, or regression-test failure. Falsification remains a completed
negative result.

**Safety and privacy constraints:** One public synthetic development fixture; a fixed finite
matrix; offline execution; no fuzzer, exploit generation, fixture repair, schema adoption,
policy change, private or participant data, held-out or validation evidence, model/provider
call, paid service, outreach, or authorization to extend the fixture set.

**Scoped completion test:** Apply two invalid values—empty string and integer zero—to each
of 11 identifier/reference surfaces for 22 exact cases; apply `null`/list mutations to 17
fixed container surfaces; record validation, rendering, and aggregate-equivalence stages;
classify deliberate, incidental, accepted, and unexpected outcomes; serialize deterministic
ASCII JSON; pass five dedicated tests, the full offline suite, prior regression checks, JSON
validation, compilation, and diff checks; record calls and spend as zero.

**Completion state:** **COMPLETE** for this bounded development characterization. The
broader Benchmark 003 review/fix/extension agenda remains incomplete and was not counted as
a second selected agenda.

## Agenda result, negative findings, and reproduction

The new [identifier/error-contract audit](../../experiments/benchmark_003_identifier_error_contract_audit.py)
and [five regression tests](../../experiments/test_benchmark_003_identifier_error_contract_audit.py)
ran on Python 3.14.5.

| Measure | Result |
|---|---:|
| Identifier/reference surfaces | 11 |
| Invalid values per surface | 2 |
| Identifier/reference cases | 22 |
| Deliberate record-validation rejections | 20/22 |
| Accepted at record validation | 2/22 |
| Malformed-container cases | 17 |
| Deliberate validation exceptions | 3/17 |
| Incidental Python exceptions | 14/17 |
| Malformed cases accepted | 0/17 |
| Unexpected exceptions | 0 |
| Dedicated tests | 5/5 passed |
| Full experiment tests | 72/72 passed |
| Model calls | 0 |
| Provider calls | 0 |
| Paid services | 0 |
| Exact spend | `$0.00` |

The hypothesis was falsified. Twenty identifier/reference cases fail deliberately during
record validation. A fact identifier and its dependent references can still pass record
validation as either an empty string or integer zero. The empty identifier reaches rendering
and then an aggregate `EquivalenceError`; integer zero fails during rendering with an
incidental `TypeError`. Of 17 malformed-container cases, only three use a deliberate
validation exception; 14 expose an incidental Python `TypeError` or `AttributeError`.
None is accepted and none produces an unclassified exception.

The unchanged base semantic-record SHA-256 is
`8298cf6b4659b7560423a522eab135bc6890ef4f413d091763ec76f16a9b7515`.
Two serialized runs were byte-identical; deterministic stdout SHA-256 is
`45b9ff24b5a68ed09173db973c4ea84e4c3d2ef0fde05b22dcf3490ad15a66e7`.
No timestamp is embedded in the result. Independent code review first identified an
incomplete mutation matrix and a summary-complement error; both were corrected by covering
the full 22-case cross-product and asserting exact per-case classifications. A second review
found no actionable issue. The base object and fixture bytes remained unchanged.

Reproduce from the public repository root:

```bash
python3 experiments/benchmark_003_identifier_error_contract_audit.py
python3 -m unittest experiments/test_benchmark_003_identifier_error_contract_audit.py -v
python3 -m unittest discover -s experiments -p 'test_*.py' -v
python3 experiments/benchmark_003_unicode_line_separator_audit.py
python3 experiments/benchmark_003_line_boundary_matrix_audit.py
python3 experiments/benchmark_003_equivalence_preflight.py
python3 experiments/benchmark_003_build_review_packet.py --help
python3 -m py_compile experiments/*.py
python3 -m json.tool experiments/benchmark_003_development_fixture.json >/dev/null
python3 experiments/validate_formal_notation_tasks.py
git diff --check
```

All commands passed offline. Benchmark 002 still validated 28 tasks: eight development,
20 held-out, and two held-out negative controls. The fixture, preflight, preregistration,
human-review protocol, review bundle, renderers, system prompts, skeleton hashes, and known-
issue dispositions were not changed. No model, provider, inference parameters, experiment
seed, or dataset split was used. Because no paid call was proposed, no provider-identity,
budget, Athens-day spend, or paid-call approval gate was entered or assumed.

## Forum, repository workflow, and publication gates

No eligible forum submission existed, so **0** submissions were assessed and no
recommendation, clarification request, moderation action, or adjudication was made.

The audit, tests, scan, canon/watchlist maintenance, and this report are routed through the
existing draft [PR #4](https://github.com/cgoltsev/machine-pidgin/pull/4) on branch
`agent/researcher-cycle-2026-08-03`. The PR remains stacked on PR #3; no merge, release,
deployment, registration, scientific acceptance, or publication was performed. Named human
review remains required.

No news article was prepared from this cycle's result. It is a reproducible development
validator/error-surface characterization, not a validated scientific outcome or a
non-specialist publication result. The pre-existing ASD-STE100 practice note was assessed
but not created or changed by this cycle.

The strict LinkedIn gate was applied after the research. The result is adjacent to the core
mission but, as a standalone public claim, does not directly help a person preserve intent,
authority, agency, accountability, or reliable communication across an intelligence gap.
It is primarily validator behavior and test-harness evidence. It does not, by itself,
change a thoughtful non-specialist's belief or action, and no reviewed durable scientific
claim establishes a human consequence. It therefore fails the **core-mission-fit,
human-interest, materiality, novelty-and-evidence, LinkedIn-quality, share, and changelog**
tests. The recorded decision is **no LinkedIn post warranted**. No post draft, named-human
action-time confirmation, page action, or post URL exists.

No X action occurred. The documented `@machinepidgin` appeal was denied and the account
remains locked; no enforcement evasion, post, follow, or Director-cadence use occurred.

## Limits, risks, anomalies, and approvals needed

- The literature scan is bounded, English-language, metadata- and index-dependent,
  incomplete for 14–15 August, and not a systematic review or meta-analysis. Fresh
  preprints, Working Drafts, Individual Internet-Drafts, and project artifacts can change.
- The fixed audit covers one synthetic development fixture and selected malformed
  JSON-like values. It is not a schema conformance suite, parser survey, fuzzer, robustness
  estimate, security test, exploitability demonstration, or model-behavior result.
- An incidental Python exception is evidence about the current implementation surface, not
  proof of a remotely reachable vulnerability, sensitive-data exposure, or governance harm.
- The accepted fact identifiers and 14 raw exception surfaces are preserved as negative
  results. No repair or policy preference was smuggled into the characterization.
- The public ASD-STE100 percentages lack enough method and artifact detail for independent
  reproduction. The standard is copyrighted; contributor-data permission remains unknown.
- The WeClawArena artifact could not be anonymously reverified because it returned HTTP
  401; access status and durability remain unknown.
- PR #4 is stacked on unreviewed PR #3, has no automated checks or reviews, and the public
  branches are unprotected. A human must verify the cycle-only diff and merge sequence.
- The private operations worktree contains user-owned uncommitted Apolo files. They were
  preserved untouched; later automation must avoid clobbering them.
- Public checks cannot prove the absence of undisclosed/off-platform work. Private PR,
  issue, and intake state remains unknown rather than fabricated.

Approvals and decisions now needed are methodological and release decisions, not authority
inherited by the Researcher:

1. A named independent human must complete and seal both existing Benchmark 003 review
   phases, recording identity, conflicts, prior exposure, and consent for attribution.
2. That review should explicitly decide the identifier schema and deliberate aggregate
   error contract alongside the existing text-boundary, common-baseline, and construct-
   naming questions. The current audit does not choose a repair.
3. Any approved fix must preserve this development negative record and add fresh post-fix
   fail-closed regression evidence. Do not extend fixtures, freeze/register a corpus,
   inspect held-out data, or make model calls from this characterization.
4. Human review is required for PR merge and any later scientific release. Future corpus,
   privacy/licensing, provider, parameter, seed, maximum-cost, stop-rule, artifact-budget,
   current Athens-day spend, and action-time gates remain closed.
5. No governance vote is requested by this cycle.

## Single highest-value next research action

Have a named independent human complete and seal both Benchmark 003 review phases and make
an explicit identifier-schema and aggregate-error-contract decision using the 22+17 audit
alongside the other known defects. The Researcher should then implement only the approved
bounded repair, preserve the negative record, rerun every deterministic check, and obtain a
fresh post-fix human review before any fixture extension or paid experiment is considered.
