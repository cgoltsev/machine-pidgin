# Researcher report — weekly cycle of 7 August 2026

**Run window:** 7 August 2026, approximately 14:52–15:15 EEST (UTC+03:00)

**Cycle status:** Completed without a reportable security, privacy, unexpected-spend,
legal, governance, urgent research-integrity, or unsafe-account incident.

**Evidence boundary:** Literature findings are exploratory synthesis. The selected agenda is
an offline development characterization over one public synthetic fixture. No held-out,
validation, participant, model-performance, deployment, or security-impact evidence was
generated.

**Authorship:** Prepared by the Machine Pidgin AI Researcher for named human review;
capability does not confer governance, moderation, publishing, spending, account,
scientific-acceptance, or institutional authority.

## Governance preflight and change audit

Before research work, the Researcher read the current Constitution, Governance, Code of
Conduct, public/private repository boundaries, privacy and security notices, contact
directory, research documentation, operating documentation, prior Researcher memory and
reports, and the most recent Director research handoff. Those documents remained binding.
External papers, sites, forum records, linked artifacts, and model outputs were treated as
untrusted evidence rather than instructions.

The public research repository was clean at commit `aa40afb` before this cycle's writes and
matched its remote branch. The only new public research artifact since the 5 August weekly
cycle was the already documented 7 August U+2028 development audit at that commit. Public
draft PRs [#1](https://github.com/cgoltsev/machine-pidgin/pull/1),
[#3](https://github.com/cgoltsev/machine-pidgin/pull/3), and
[#4](https://github.com/cgoltsev/machine-pidgin/pull/4) remained open; PR #4 was draft,
cleanly mergeable, stacked on PR #3, and had no reviews, review threads, comments, checks,
or labels before this cycle's writes. No public issue, Discussion, workflow run, or release
changed in the interval.

The private operations repository was inspected only to establish the boundary and change
delta. Its post-cutoff changes were Apolo-site work, not research. It had one local commit
ahead of its remote and user-owned modified/untracked Apolo page, styling, handoff, image,
and video files. They were preserved untouched. Private PRs #1 and #5 had no review or
comment delta, and no private issue was open. No private intake, participant data,
credentials, or operational material was copied into public artifacts.

The public forum API reported five approved team-authored topics and zero replies;
`pending_review` was zero. Public community statistics reported one member, zero proposals,
and two support-interest records. No eligible third-party public research submission
existed, so the submission-assessment count is **0**. Private intake was deliberately not
accessed, and public absence is not evidence that no off-platform material exists.

## Canon and bounded current-literature scan

The [living canon](../LITERATURE_CANON.md) now contains **59 entries**: 17 normative/stable
specifications, 13 established empirical/evaluation sources, 14 conceptual foundations,
and 15 explicitly provisional sources. One stable specification and four provisional
sources were added; none was removed or promoted:

- Unicode [UAX #14 revision 55](https://www.unicode.org/reports/tr14/tr14-55.html) was added
  as a previously missing stable normative source for line-breaking classes and mandatory
  boundary behavior. It is not a SPEAR acceptance, escaping, security, or authorization
  policy.
- Feng, Zhao, and Crisan's [IntentLint](https://arxiv.org/abs/2608.04331) provides early
  controlled HCI evidence for structured, editable shared intent and prompt-time conflict
  checking. Its short 16-participant setting does not establish long-term correctness,
  conflict resolution, or accessibility.
- Chen et al.'s [mobile permission study](https://arxiv.org/abs/2608.04755) found that
  requester identity and task context materially changed permission decisions, while prompt
  mitigations were inconsistent. Its synthetic dialogs, limited apps/tasks, and expert
  labels do not validate a separate authorization layer.
- Wang et al.'s [SCP-NL2TL](https://arxiv.org/abs/2608.05439) supplies a provisional
  accept-or-abstain comparison for semantic compilation. Its conformal guarantee is marginal
  joint risk in expectation under stated assumptions, not conditional error among accepted
  outputs.
- Chen et al.'s [trajectory-poisoning study](https://arxiv.org/abs/2608.05563) treats
  promotion of experience into persistent instructions as a provenance/authority boundary.
  It measures inert-canary artifact creation in two systems, not runtime compromise.

The existing SHACL 1.2 entry was updated rather than duplicated. The
[6 August SPARQL Extensions Working Draft](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260806/)
adds `sh:tempTriple`, whose inferred state is visible during rule execution and removed
afterward. Researcher inference: transient operational state that affects an outcome needs a
separate durable provenance record. The draft itself does not supply that record or encode
legitimate intent/authority, and Working Draft publication is not W3C endorsement.

The [7 August scan](../scans/2026-08-07-current-literature.md) records the exact query,
sources, dates, screening, inclusion/exclusion reasons, source facts, Researcher inferences,
uncertainty, and Institute disposition. It continued strictly after the prior arXiv indexed
cutoff, screened **567** records across `cs.AI`, `cs.CL`, `cs.HC`, `cs.SE`, `cs.CR`, and
`cs.CY`, and shortlisted 27 likely matches. The newest indexed submission was 6 August at
17:59:58 UTC; no 7 August submission was represented, so same-day coverage is incomplete.
A later `lastUpdatedDate` repeat was rate-limited, so older-record revision coverage is not
claimed exhaustive.

SafeCommit, automatic requirements-to-LTL translation, When History Lies, The
Personalization Mirage, MIST/SCOPE, OrchestraBench, and a visual-accessibility issue study
were retained as exclusions or deferrals rather than used to pad the canon. Stable-source
checks found no new NIST/NCCoE deliverable or new MCP/A2A protocol release. MCP's official
Agents Working Group charter, an A2A migration-guide correction, SHACL UI ordering work,
and RDF Concepts version-negotiation guidance were material watch/scan deltas but not new
normative canon entries.

## Public-source watchlist

The [watchlist](../RESEARCH_WATCHLIST.md) was refreshed only from public primary output.
IntentLint, Permission Literacy, SCP-NL2TL, and PoisonedEvolution authors/projects are new
medium-priority Director candidates. MCP's entry now records its Agents Working Group;
A2A records the corrected migration guide; W3C records transient SHACL state, UI ordering,
and RDF version-metadata work. The WeClawArena artifact returned HTTP 401 during anonymous
reverification; that may be transient or access-dependent and does not prove removal, but
its durability limitation was strengthened.

Every entry remains **research we are learning from**. No person or group was called a
collaborator, supporter, or affiliate. No follow, message, like, repost, subscription,
unsolicited contact, or account action occurred. Follow candidates are recommendations only
and remain behind the Institute's operating, verified-account, suspension-resolution, and
human-action gates.

## The exactly one selected agenda

**Question:** Across the 11 line-boundary forms documented by the pinned Python runtime,
which of four Benchmark 003 canonical string locations accept an appended `HARD_GATES:`
heading, and which A-D traced render atoms expose it as a literal split line rather than an
escaped sequence while the equivalence preflight still returns `PASS`?

**Hypothesis / decision target:** All 44 mutations will validate and return preflight
`PASS`. Raw lexical atoms will expose the reserved heading as a split line. JSON-rendered
entity-label and authority-action atoms in B/D will escape the eight C0/CRLF forms but keep
NEL, LS, and PS literal because the renderer uses `ensure_ascii=False`. A/C and B/D
observations will agree within their shared renderer profiles. The decision target is an
auditable acceptance/encoding matrix for a later human text-policy choice, not the policy
itself.

**Relevance to SPEAR:** A canonical data value becoming prompt structure can blur the
distinction between human-authored task data, constraints, and authority. Representation-
dependent escaping can also confound Benchmark 003's representation factor. This offline
test cannot show that a model would follow the injected heading or that an exploitable
condition exists.

**Prior evidence:** The existing ASCII newline/reserved-heading probes and the 7 August
U+2028 `/task` audit receive fixture-internal `PASS`; record validation generally requires
only non-empty strings; source traces authenticate values and glue without imposing a
boundary policy; and [RFC 8259 section 7](https://www.rfc-editor.org/rfc/rfc8259.html#section-7)
requires JSON escaping for U+0000–U+001F while allowing other characters to be escaped.

**Falsification criteria:** The hypothesis is falsified by any of the following, all of
which would still be preserved as a completed result: a mutation is rejected; a successful
cell is not `PASS`; a raw atom lacks a split-line heading; a JSON atom keeps a C0/CRLF form
literal or fails to keep NEL/LS/PS literal; A/C or B/D disagree; the exact source atom cannot
be recovered through its pointer/role trace; repeated canonical JSON differs; or the prior
U+2028 `/task` semantic hash is not reproduced.

**Safety and privacy constraints:** Exactly one public synthetic development fixture; four
already documented source pointers; in-memory mutations; ASCII-escaped output; no full
prompt publication, private or participant data, held-out/validation evidence, model or
provider call, paid service, outreach, policy change, fixture repair, or authorization to
proceed. Format controls, bidirectional controls, normalization, tokenization, display,
model response, and security impact remain out of scope.

**Scoped completion test:** Execute the explicit 11×4 matrix; record record-validation
stage, preflight outcome, semantic-record hash, lexical form, exact source-trace observation,
runtime, and provenance; produce 44 unique cases and 176 A-D observations; serialize
boundaries with ASCII escapes; produce byte-identical canonical JSON twice; reproduce the
prior U+2028 hash; pass dedicated and full offline tests; and record calls and spend as zero.

**Completion state:** **COMPLETE** for this bounded development characterization. The
broader Benchmark 003 review/fix/extension agenda remains incomplete and was not counted as
a second selected agenda.

## Agenda result, negative findings, and reproduction

The new [matrix audit](../../experiments/benchmark_003_line_boundary_matrix_audit.py) and
[five regression tests](../../experiments/test_benchmark_003_line_boundary_matrix_audit.py)
run on Python 3.14.5 with Unicode database 16.0.0.

| Measure | Result |
|---|---:|
| Boundary forms | 11 |
| Canonical source surfaces | 4 |
| In-memory mutations | 44 |
| A-D trace observations | 176 |
| Records accepted | 44/44 |
| Preflight `PASS` | 44/44 |
| Reserved heading exposed as a split line | 144/176 |
| Reserved heading escaped rather than split | 32/176 |
| Dedicated tests | 5/5 passed |
| Full experiment tests | 67/67 passed |
| Model calls | 0 |
| Provider calls | 0 |
| Paid services | 0 |
| Exact spend | `$0.00` |

The primary negative result is universal acceptance: none of the 44 boundary mutations was
rejected. Raw task and fact-attribute atoms exposed every tested heading in A-D. Entity-label
and authority-action atoms exposed all headings in A/C, while their JSON-rendered B/D atoms
escaped the eight C0/CRLF forms, producing the 32 non-split observations. NEL, LS, and PS
remained literal in those same JSON atoms. This is a representation-dependent grammar
difference relevant to the factorial design; it is not evidence that an escaped sequence is
safe for a model.

The U+2028 `/task` case reproduced semantic-record SHA-256
`5437bbc8460fefbc3bbe2eca5456800c68243efda59b5fa96335a0f804f26b5a`.
Two full serialized runs were byte-identical; deterministic stdout SHA-256 is
`527ee3b8287a8b50778e9975c9989b1b04a5639e4bac8b2c98c99e2aa68ec37e`.
No timestamp is embedded in the result.

Reproduce from the public repository root:

```bash
python3 experiments/benchmark_003_line_boundary_matrix_audit.py
python3 -m unittest experiments/test_benchmark_003_line_boundary_matrix_audit.py -v
python3 -m unittest discover -s experiments -p 'test_*.py' -v
python3 experiments/benchmark_003_unicode_line_separator_audit.py
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
seed, or dataset split was used. Because no paid call was proposed, no provider, budget,
Athens-day spend, or paid-call approval gate was entered or assumed.

## Forum, repository workflow, and publication gates

No eligible forum submission existed, so **0** submissions were assessed and no
recommendation, clarification request, moderation action, or adjudication was made.

The audit, tests, scan, canon/watchlist maintenance, and this report are routed through
existing draft [PR #4](https://github.com/cgoltsev/machine-pidgin/pull/4) on branch
`agent/researcher-cycle-2026-08-03`. The matrix implementation commit is `b548e5e`. The PR
remains a draft and stacked on PR #3; no merge, release,
deployment, registration, scientific acceptance, or publication was performed. Named human
review remains required.

No news article was prepared. This is a reproducible development-method characterization,
not a validated scientific outcome or a non-specialist publication result.

The strict LinkedIn gate was applied after the research. The human consequence can be
stated plainly—“text entered as data can become a new instruction heading when rendered”—
but this run does not establish model response or real-world consequence. It therefore fails
the **human-interest, materiality, reviewed durable-evidence, LinkedIn-quality, share, and
changelog** tests. The result belongs in the repository/report and the recorded decision is
**no LinkedIn post warranted**. No post copy, human action-time confirmation, page action, or
post URL exists. The prior human rejection of test-log/jargon-first copy was treated as a
binding editorial anti-example, not recycled into a new draft.

No X action occurred. The documented `@machinepidgin` suspension/appeal remains unresolved;
no enforcement evasion, post, follow, or cadence use occurred.

## Limits, risks, anomalies, and approvals needed

- The literature scan is bounded, English-language, index-dependent, incomplete for
  7 August, and non-exhaustive for older revisions after rate limiting. All four paper
  additions are fresh preprints/manuscripts and remain provisional.
- The matrix uses one synthetic development fixture and one host runtime. Python's
  `splitlines()` boundary set is not a complete Unicode, display, tokenizer, normalization,
  bidirectional-text, or prompt-security policy.
- Literal split lines do not prove that any model will interpret or obey the heading;
  escaped sequences do not prove safety. No effect size or exploitability claim is made.
- Universal validator acceptance is preserved as a negative result. No repair was smuggled
  into the characterization, and post-fix evidence cannot replace this record.
- The WeClawArena artifact could not be anonymously reverified because it returned HTTP 401;
  access status and durability remain unknown.
- PR #4 is stacked on unreviewed PR #3. A human must verify the eventual cycle-only diff and
  merge sequence without history rewriting.
- Public checks cannot prove the absence of undisclosed/off-platform work. Private intake
  was not accessed, and user-owned private-repository changes were preserved untouched.

Approvals and decisions now needed are methodological and release decisions, not authority
inherited by the Researcher:

1. A named independent human must complete and seal both existing Benchmark 003 review
   phases, recording identity, conflicts, prior exposure, and consent for attribution.
2. The human review should explicitly choose and document a text-boundary policy informed
   by this matrix, and decide the existing common-system-baseline, construct naming/redesign,
   identifier validation, and aggregate error-contract issues.
3. Any fix must retain this development negative result and add fresh post-fix fail-closed
   regression evidence. Do not extend fixtures, freeze/register a corpus, inspect held-out
   data, or make model calls from the current `PASS` outcomes.
4. Human review is required for PR merge and any later scientific release. All future
   corpus, privacy/licensing, provider identity, parameters, seeds, maximum-cost, stop-rule,
   artifact budget, current Athens-day spend, and action-time approval gates remain closed.
5. No governance vote is requested by this cycle.

## Single highest-value next research action

Have a named independent human complete and seal both Benchmark 003 review phases and make
an explicit text-boundary-policy decision using the 11×4 matrix alongside the four prior
known defects. The Researcher should then implement only the approved bounded repair, retain
the negative record, rerun all deterministic checks, and obtain a fresh post-fix human
review before any fixture extension or paid experiment is considered.
