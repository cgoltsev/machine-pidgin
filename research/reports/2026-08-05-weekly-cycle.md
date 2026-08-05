# Researcher report — weekly cycle of 5 August 2026

**Run window:** 5 August 2026, 12:15:59 EEST (UTC+03:00) through the final
verification time recorded in the automation handoff

**Cycle status:** Completed without a reportable security, privacy, unexpected-spend,
legal, governance, urgent research-integrity, or unsafe-account incident.

**Evidence boundary:** Literature findings are exploratory synthesis. The Benchmark 003
work is research-method instrumentation over one synthetic development fixture. No
validation, held-out, human-review, or model-performance evidence was generated.

**Authorship:** Prepared by the Machine Pidgin AI Researcher for named human review;
capability does not confer governance, publishing, spending, moderation, account, or
scientific-acceptance authority.

## Governance preflight and change audit

Before research work, the Researcher read the current Constitution, Governance, Code of
Conduct, public/private repository boundaries, privacy and security notices, contact
directory, research documentation, operating documentation, prior Researcher memory and
report, and the most recent Director research handoff. The public research repository
contains only research, protocol, experiment, governance, and public-source artifacts. No
private intake, participant data, credentials, or private operational material was copied
into it.

The completed 3 August cycle, not merely the automation wake timestamp, is the substantive
delta baseline. Before this cycle's writes, read-only checks found no external public-research
commit, push, issue, pull request, review, comment, check, workflow run, release, Discussion,
or public forum research submission after that cycle closed. For timestamp completeness, the
only events after the automation's earlier `2026-08-03T13:54:50Z` marker were the already
documented prior-cycle Researcher commits and creation/update of draft
[PR #4](https://github.com/cgoltsev/machine-pidgin/pull/4).

Both repositories were inspected under their public/private boundaries; no private content
or operational metadata was copied into this report. Public PR #4 had received no human
review, comment, request, or check before this cycle's writes. The publicly visible forum
contained no eligible third-party research submission; private intake was not accessed.
The eligible public-submission count for this cycle is therefore **0**.

## Canon and bounded current-literature scan

The [living canon](../LITERATURE_CANON.md) now contains 54 entries: 16 normative or stable
specifications, 13 empirical/evaluation sources, 14 conceptual foundations, and 11
explicitly provisional sources. Four provisional entries were added and none removed:

- W3C's 3–4 August 2026 SHACL 1.2 Core and SHACL 1.2 SPARQL Extensions Working Drafts. The Core draft
  adds non-validating `sh:intent` and `sh:agentInstruction` annotations alongside formal
  constraints. It explicitly says intent cannot affect validation or conformance and warns
  that graphs assembled from outside a trust boundary can alter intended semantics. This is
  a useful dual-register precedent, not an authority mechanism or finished standard.
- Zhan et al.'s [AuthMem-Bench](https://arxiv.org/abs/2608.01679), arXiv v2, which reports
  authority collapse in 48 of 49 consolidator/backbone configurations and directly models
  source authority as use-specific durable state. It is a fresh unreviewed preprint built
  from controlled/synthetic transformations; its reported mitigation is not a field-safety
  guarantee.
- Mercado and Lomuscio's [STEAD](https://arxiv.org/abs/2608.03609), an unreviewed preprint
  formalizing temporal verification over persistent relational state. Its finite-domain
  preservation and verification result depends on boundedness, tool/interface equivariance,
  and tool-uniform semantics; canonicalization is graph-isomorphism-hard in general, and the
  method is illustrated rather than deployment-validated.
- Wang et al.'s [WeClawArena](https://arxiv.org/abs/2608.03499), an unreviewed 620-variant
  multi-owner workspace benchmark that separates utility from attack success and records
  authority/privacy/governance evidence. It uses simulated environments and a headline LLM
  judge; its 200-row human pilot was author-annotated, and the initial artifact location is
  anonymous and potentially unstable.

The [5 August scan](../scans/2026-08-05-current-literature.md) also preserves Xu and Wu's
[TRIO-20](https://arxiv.org/abs/2608.03169) as a bounded negative result: zero unauthorized
tool calls in 840 trajectories under explicit system-level prohibitions. The paper itself
limits inference to one model family, two tiers, 14 workplace scenarios, endpoint effort
levels, fixed collection order, and moving provider aliases. It is not evidence for
ambiguous, adversarial, stale, or conflicting authority conditions and was not added to the
canon merely for reporting a clean result.

The delta scan reviewed official/versioned W3C, NIST/NCCoE, MCP, A2A, and tracked project
sources, plus 672 candidate arXiv records across `cs.AI`, `cs.CL`, `cs.HC`, `cs.SE`,
`cs.CR`, and `cs.CY`. No material change was found for NIST agent standards/identity work,
MCP (2026-07-28 remains current), A2A (v1.0.1 remains latest), W3C AI accessibility/COGA,
or RDF 1.2. August 5 arXiv indexing had only reached 4 August 17:59:58 UTC at the
cutoff, so same-day coverage is explicitly incomplete. Two additional fresh preprints on
requirements elicitation and durable authorization state were screened out for material
confounding or missing standalone reproducibility evidence. Marketing, secondary summaries
where a primary source existed, duplicates, unverifiable claims, and citation padding were
excluded.

Source claims, Researcher inferences, uncertainty, and Institute position are separated in
the scan. No Institute position, endorsement, collaboration, or affiliation was adopted.

## Public research watchlist

The [watchlist](../RESEARCH_WATCHLIST.md) was refreshed only from public research output.
The W3C Data Shapes Working Group is now explicit within the high-priority W3C standards
watch, and the AuthMem-Bench, STEAD, and WeClawArena teams/projects are medium-priority
Director candidates. Every entry remains “research we are learning from.” No follow,
message, like, repost, subscription, unsolicited contact, or other account action occurred.

## The exactly one selected agenda

**Question:** Can a named independent human assess the current Benchmark 003 A–D prompts,
factor isolation, and mutation oracle from a deterministic, provenance-bound two-stage
bundle while the first-stage review withholds condition labels, the expected-output oracle,
prior automated verdicts, and mutation answers?

**Hypothesis / decision target:** Identical pinned inputs and the same secret, unpredictable
coordinator nonce produce byte-identical Phase 1 packets, reveal cores, and keyed source,
reveal, and allocation commitments; changing an input changes or invalidates the bound
provenance. A structured response requires independent semantic extractions, mutation
observations, explicit `PASS`, `REVISE`, or `UNCERTAIN` judgments, identity and
conflict/prior-exposure disclosures, and rationales. Any uncertainty or unresolved defect
yields `REVISE`. Success means **ready for human review**, not equivalent, validated,
frozen, or authorized to proceed.

**Why it matters to SPEAR:** Benchmark 002's apparent notation benefit changed after one
answer-cue asymmetry was found. A credible factorial estimate for representation and an
interpretation contract requires both equivalent task semantics and a clean manipulation of
the intended constructs.

**Prior evidence:** The Benchmark 002 audit; the 3 August deterministic preflight and its
explicit human-review limitation; requirements traceability, constraint-interaction,
fail-safe, and formal-validation sources in the canon; and the absence of any review or
comment on draft PR #4.

**Falsification criteria:** The agenda fails if repeated packet construction differs; an
input mutation leaves provenance unchanged; Phase 1 structurally leaks condition tags,
expected output, audit surfaces, traces, prior verdicts, or the allocation mapping; the
reveal cannot open the allocation commitment; required reviewer fields can be omitted; an
uncertain/unresolved item can yield readiness; or the tooling implies that a human review
has already occurred.

**Safety and privacy constraints:** One public synthetic development fixture only; no
held-out or participant data, private material, secrets, external model/provider call,
spend, outreach, or publication decision. Reviewer identity, conflicts, prior exposure, and
public attribution require the reviewer's consent. The treatment itself is visually
inferable, so this is accurately called **condition-label-masked and oracle-withheld**, not
fully blinded.

**Scoped completion test:** Provide an offline deterministic builder, review protocol,
response/reveal validation, and test-generated bundles for the fixed synthetic source, with
tests for determinism, commit/file provenance, oracle-hash leakage, exact schemas, mapped
prompt integrity, reveal-core tampering, required semantic/disclosure fields, exclusive
private output, conservative disposition, and known limitations. The tooling milestone is
complete when those checks pass. No live coordinator nonce, reviewer packet, or reveal was
created. The named human review and broader Benchmark 003 agenda remain **INCOMPLETE**.

## Development result, negative findings, and reproduction

The new review tooling packages the existing fixture without its `expected` object, assigns
four opaque profile identifiers from a secret nonce, supplies exact system/user prompt pairs
and hashes, and requires an independent semantic extraction and mutation observation for
each profile. Phase 1 exposes a redacted-source digest and keyed hiding commitments, not a
reusable raw digest over the low-entropy oracle-bearing source. The coordinator reveal opens
those commitments, restores the A–D/factor mapping, and exposes commit-bound source hashes
and mandatory issue dossiers. The verifier independently rebuilds every sensitive reveal
field, requires the executing working-tree bytes to match their recorded commit blobs, and
checks each prompt against its revealed condition. Live nonce/reveal files must be
user-only, are created without putting the nonce in process arguments, and cannot overwrite
an existing file. Public source code cannot blind a reviewer who inspects it or independently
infers visible treatment factors; the separation is an auditable procedure.

Adversarial tests falsified several earlier draft assumptions before any live packet existed:
raw full-source hashes allowed low-entropy oracle checking; mutable response schemas and
resealable reveal fields were trusted; Phase 2 did not bind the exact reveal; prompt payloads
could be swapped across fixed opaque IDs; an arbitrary string could pose as a source commit;
Python boolean/integer equality could mask source or accounting changes; and ordinary reveal
writes could be world-readable or overwritten. All were corrected in the
development tooling and retained as regression tests. The conservative validator also makes
the present unresolved/reproduced-negative dossiers deterministically yield `REVISE`, even
if every reviewer-supplied verdict says `PASS`. This is a tooling negative result, not evidence
that cryptographic commitments confer reviewer independence or scientific validity.

The agenda preserved four material negative findings rather than repairing around them:

1. The “contract present” system prompt currently replaces the common baseline instead of
   appending to it, so the contract estimand also removes/rewords baseline instruction.
2. The purported “ordinary prose” renderer is highly fielded, while the bespoke field
   renderer and compact contract do not instantiate the published SPEAR/0.2 schema and
   interpretation prompt. A human must decide whether to rename the constructs or redesign
   them.
3. The preflight accepts arbitrary non-empty strings and renders several strings raw in
   prose but JSON-escaped in fields. Newline/reserved-heading mutations to task text, entity
   labels, fact attributes, and authority actions still receive automated `PASS`, despite
   materially different prompt grammar. The present pass is therefore fixture-specific and
   cannot authorize extension.
4. An empty fact identifier can pass record validation when references are changed with it,
   and malformed artifact/surface inputs can raise raw `AttributeError` or `TypeError`
   instead of the aggregate `EquivalenceError` interface.

These are development-method defects, not evidence of a security incident in a deployed
system. No held-out corpus exists, no paid run occurred, and no public scientific result was
invalidated. They do reverse the prior expectation that a passing single fixture alone
justifies immediate fixture extension.

Reproduce from the public repository root:

```bash
python3 experiments/benchmark_003_equivalence_preflight.py
python3 experiments/benchmark_003_build_review_packet.py --help
python3 -m unittest discover -s experiments -p 'test_*.py' -v
python3 -m py_compile experiments/*.py
python3 -m json.tool experiments/benchmark_003_development_fixture.json >/dev/null
python3 experiments/validate_formal_notation_tasks.py
git diff --check
```

The clean fixture continues to produce the prior development-only preflight `PASS`, 52
source-bound atoms per condition, and semantic-record SHA-256
`8298cf6b4659b7560423a522eab135bc6890ef4f413d091763ec76f16a9b7515`.
That result is retained for reproducibility but narrowed by the new negative probes. The
35 dedicated review-bundle tests and all 62 discovered experiment tests passed offline;
compilation, fixture parsing, the existing 28-task Benchmark 002 validator, and diff checks
also passed.

**Calls and spend:** model calls `0`; provider calls `0`; paid services `0`; exact spend
`$0.00`. No model, provider, inference parameters, or experiment seed were used. Because no
paid call was proposed, no provider identity, artifact budget, Athens-day spend, or paid-call
approval gate was entered or assumed. Those checks remain mandatory immediately before any
future authorized paid call.

## Forum, publication, and review workflow

No eligible forum submission existed, so **0** submissions were assessed and no
recommendation, clarification request, moderation action, or adjudication was made. The
absence of a public submission is a recorded negative result; undisclosed/off-platform and
private-intake material remain unknown.

The source-anchored scan, canon/watchlist changes, weekly report, and review tooling are a
material development-method update, so they were routed through the existing public draft
[PR #4](https://github.com/cgoltsev/machine-pidgin/pull/4). The PR remains stacked on draft
PR #3 and remains a human-review draft. No merge, release, deployment, OSF registration,
scientific acceptance, or publication was performed. Repository labels `codex` and
`codex-automation` were unavailable and were not invented.

No news article was prepared: a review instrument and newly exposed limitations are not a
scientific outcome. The strongest platform copy is therefore held for the Director and not
posted:

> New W3C SHACL 1.2 drafts separate non-validating intent/agent instructions from formal
> validation. Our Benchmark 003 audit found a parallel boundary: a deterministic prompt
> preflight can preserve source atoms yet still miss delimiter-induced pragmatic changes.
> We prepared a condition-label-masked, oracle-withheld [review protocol and deterministic
> builder](https://github.com/cgoltsev/machine-pidgin/blob/agent/researcher-cycle-2026-08-03/experiments/BENCHMARK_003_HUMAN_REVIEW_PROTOCOL.md)
> for one synthetic fixture and blocked corpus extension pending review. No live reviewer
> packet exists yet. Development evidence only; reproduction and critique welcome.
> AI-assisted draft.

There is no post URL because nothing was posted.

## Limitations, risks, and approvals needed

- The literature scan was bounded, English-language, index-dependent, and incomplete for
  August 5; the four canon additions are provisional preprints or Working Drafts.
- The review bundle provides procedural masking, not treatment blindness. Prompt content,
  public source, this report, or prior exposure may reveal factors or hypotheses. The
  reviewer must disclose exposure and seal Phase 1 before receiving the reveal.
- The current preflight is limited to one synthetic fixture. It does not establish
  arbitrary paraphrase equivalence, construct validity, extension safety, or model behavior.
- PR #4 is stacked on unreviewed PR #3. A human must later merge updated `main` into the head
  without rewriting history, retarget the draft, and verify the cycle-only diff.
- Public checks cannot prove the absence of undisclosed or off-platform work. Private intake
  was not inspected, and no private operational material was transferred here.

Approvals and decisions now needed are methodological, not governance votes:

1. Name an independent human reviewer; record identity, conflicts, prior exposure, consent
   for any public attribution, and sealed Phase 1 and Phase 2 responses.
2. Decide whether Benchmark 003 should rename its constructs as narrative-versus-field
   templates or redesign them to instantiate published SPEAR/0.2, and make the contract
   factor additive over a common baseline.
3. Require `REVISE` until the delimiter/identifier/exception robustness gaps are fixed and
   reviewed; do not extend fixtures, freeze a corpus, register, or make model calls from the
   present single-fixture `PASS`.
4. Retain all later corpus, privacy/licensing, model/provider, randomization, external
   registration, maximum-cost, stop-rule, and current-spend gates. No governance vote is
   requested by this cycle.

## Single highest-value next research action

Have a named independent human complete and seal both review phases, recording the expected
`REVISE` disposition and explicit decisions on the four known defects, including the
rename-versus-redesign choice. The Researcher should then harden the renderer and validator,
rerun the deterministic checks, and obtain a fresh post-fix human review. Only a post-fix
`PASS` with no unresolved or uncertain item can precede consideration of a tiny diverse
development fixture set.
