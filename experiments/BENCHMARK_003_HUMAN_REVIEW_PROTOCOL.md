# Benchmark 003 two-stage human-review protocol

**Status:** Development-method protocol; draft, not reviewed

**Prepared:** 5 August 2026

**Scope:** The single public synthetic development fixture only

This protocol prepares evidence for a named independent human. It does not establish
equivalence, validate Benchmark 003, authorize fixture or corpus extension, freeze a corpus,
register a study, permit model calls, or approve spending. Capability is not authority; all
scientific and operational gates in the preregistration draft remain human-controlled.

## Review question

Can the current A–D prompt set, factor isolation, and mutation oracle be challenged from a
provenance-bound two-stage bundle while Phase 1 withholds condition labels, the stored
expected-output oracle, prior automated verdicts, and the mutation answers?

The bundle is **condition-label-masked and oracle-withheld**, not fully blinded. Prompt
content makes the representation and system-contract factors visually inferable. The public
source, prior reports, or independent task solving can expose the hypothesis or likely answer.
The reviewer must disclose prior exposure. Procedural separation cannot prevent a reviewer
from inspecting public material; it makes the sequence and evidence auditable.

## Roles and authority

- The Researcher builds and verifies the packet, records hashes, preserves negative results,
  and reports uncertainty. The Researcher does not select a favorable reviewer verdict or
  treat a tooling PASS as scientific acceptance.
- The coordinator holds the nonce and reveal until the Phase 1 response is sealed. The
  coordinator may not alter either packet after seeing a review outcome.
- A named independent human reviewer records qualifications, conflicts, prior exposure,
  independence, and public-attribution consent. The reviewer may return `PASS`, `REVISE`, or
  `UNCERTAIN` for every required item.
- The AI Director and named humans decide whether defects are resolved and whether later
  research gates may be entered. This protocol grants no publishing, spending, moderation,
  account, registration, or merge authority.

Reviewer identity, conflicts, and any public attribution must be handled under the Institute
privacy notice. Do not publish a reviewer name or disclosure without the reviewer's consent.

## Bound inputs and construction

The builder binds the exact bytes of:

- `benchmark_003_development_fixture.json`;
- `BENCHMARK_003_PREREGISTRATION_DRAFT.md`;
- `benchmark_003_equivalence_preflight.py`;
- `test_benchmark_003_equivalence_preflight.py`;
- the published `protocol/SPEAR_Protocol_Quick_Reference.md` and
  `protocol/SPEAR_LLM_PROMPT.md` definitions used by the construct-validity dossier;
- this protocol; and
- `benchmark_003_build_review_packet.py` and its offline test suite.

The coordinator reveal records the source commit at construction, exact file hashes, and the
canonical semantic-record hash. Phase 1 exposes only the bound path list, a digest of the
source after removing `expected`, and nonce-keyed HMAC-SHA256 commitments to the full source
context, reveal core, and allocation. It deliberately does not publish a reusable raw digest
over the low-entropy expected object or the oracle-bearing fixture. The coordinator-held nonce
also drives profile ordering and opaque labels. This hiding property depends on an unpredictable,
secret nonce; byte length alone is not enough. Full hashes become visible only in Phase 2.

Identical inputs and nonce must reproduce byte-identical canonical Phase 1 and reveal
objects. Changing any bound file, prompt, or nonce must change a bound digest or fail
verification. The builder uses only the Python standard library and the existing offline
preflight. It performs zero model calls, zero provider calls, and exact spend of `$0.00`.

## Phase 1 — masked prompt and oracle review

The coordinator gives the reviewer only the fixed Phase 1 packet, preferably as a direct
artifact without requiring repository navigation. Before opening it, the reviewer records
whether they have read the preregistration, renderer, tests, prior reports, pull request, or
other material that may reveal factors, expected output, prior results, or known defects.

Phase 1 contains:

- the canonical semantic source with the stored `expected` object removed;
- four opaque profile IDs in nonce-derived order;
- the exact system and user prompts plus their SHA-256 hashes;
- the bound input path list, redacted-source hash, and unopened keyed commitments;
- four explicit reserved-heading mutation inputs, without their prior outcomes;
- the structured response requirements; and
- explicit development-only, no-authority, zero-call, and zero-spend labels.

Phase 1 structurally omits A–D condition labels, representation/contract tags, the mapping
and nonce, traces, audit surfaces, expected oracle, prior preflight result, and known-issue
dossiers. The facts can still make the answer independently derivable; the protocol withholds
the stored oracle, not the reviewer's ability to reason.

For every profile, the reviewer independently records extracted task, facts, gates, order,
authority, canonical labels, output contract, and answer cues. They record a `PASS`, `REVISE`,
or `UNCERTAIN` judgment with a non-empty rationale for the profile and for every supplied
mutation probe. The reviewer also judges:

1. semantic equivalence across profiles;
2. factor isolation;
3. answer-cue balance; and
4. adequacy of the mutation oracle.

The response must identify the exact packet hash and include all identity, qualifications,
conflict, prior-exposure, independence, and attribution-consent fields. Missing or malformed
fields fail closed. The canonical JSON SHA-256 of the complete response is recorded before
the reveal is released. If any Phase 1 item is `REVISE` or `UNCERTAIN`, the derived Phase 1
disposition is `REVISE`.

## Phase 2 — reveal and adversarial challenge

Only after the Phase 1 response hash is sealed does the coordinator provide the reveal. The
reviewer verifies that it opens the source-context, reveal-core, and allocation commitments
and matches every Phase 1 profile, source hash, prompt hash, and packet hash. The verifier
independently reconstructs the record, rendered prompts, preflight result, source manifest,
factor metadata, stored oracle, and known-issue dossiers from the bound local source; a
resealed but altered reveal fails closed.

Phase 2 reveals:

- the nonce and opaque-profile-to-A–D mapping;
- representation and contract metadata;
- the stored expected-output oracle;
- the prior automated development preflight result; and
- four mandatory known-issue dossiers.

The reviewer must disposition every dossier with `PASS`, `REVISE`, or `UNCERTAIN` plus a
rationale:

### 1. Common system baseline is replaced

The current contract-present system prompt replaces rather than appends to the no-contract
baseline. The intended contract estimand therefore also removes or rewords a shared baseline
instruction. The reviewer must decide whether an additive common baseline is required and
whether affected hashes and evidence must be invalidated and re-audited.

### 2. SPEAR construct mismatch

The implemented “ordinary prose” template remains highly fielded. The bespoke “SPEAR
fields” template and compact contract do not instantiate the published SPEAR/0.2 schema and
interpretation prompt. The reviewer must choose and justify either renaming the constructs as
narrative-versus-field templates or redesigning them to test published SPEAR/0.2.

### 3. Raw-string structural-injection false PASS

The development schema accepts arbitrary non-empty strings, while some atoms are raw in one
or both renderers and others are JSON-escaped only in the field renderer. Newline and
reserved-heading mutations to task text, entity labels, fact attributes, and authority
actions receive the current automated `PASS`; entity-label and authority-action probes also
produce raw-versus-escaped prompt grammar. The current PASS is fixture-specific and cannot
support extension until these boundaries fail closed and are reviewed.

### 4. Schema and error-contract gaps

An empty fact identifier can pass `validate_record` when its references change with it.
Malformed non-object artifacts or audit surfaces can raise raw `AttributeError` or
`TypeError` rather than the documented aggregate `EquivalenceError`. The reviewer must decide
the typed/non-empty identifier constraints and fail-closed public error contract required
before extension.

The Phase 2 response binds the exact Phase 1 packet, sealed Phase 1 response, reveal hash,
and response-schema version, covers all four issue IDs, records an overall verdict and
rationale, and must set
`authorizes_fixture_extension=false`. Any non-`PASS`, uncertainty, unresolved defect, hash
mismatch, or incomplete disclosure produces `REVISE`. Even a fully passing response is only a
human methodological input; it cannot override a dossier whose bound status remains
unresolved or reproduced-negative. The current reveal therefore derives `REVISE` even if a
reviewer marks every response item `PASS`. A future `PASS` requires a newly bound bundle in
which every defect is `resolved-and-reverified`, followed by fresh review. The AI Director
and named humans retain later decisions.

## Completion and stop rules

This tooling milestone is complete when:

- deterministic construction and byte identity are tested;
- file/prompt tampering changes provenance or fails verification;
- Phase 1 matches exact top-level and nested schemas, exposes no oracle-bearing raw digest,
  compares canonical JSON bytes (including boolean/number distinctions), and has no forbidden
  structural key;
- the reveal opens every keyed commitment and exactly matches independently recomputed
  source, mapping, metadata, oracle, preflight, and issue evidence;
- response validators derive fixed requirements from code and require independent semantic
  extractions, mutation observations, disclosures, judgments, rationales, and exact hashes;
- uncertainty and unresolved items conservatively derive `REVISE`;
- the four negative findings are reproduced and retained;
- offline tests pass with zero calls and zero spend; and
- the public changes remain in a draft human-review workflow.

Stop immediately and report to the Director if source hashes differ unexpectedly, a reveal
is released before Phase 1 sealing, reviewer consent or privacy is unclear, an external call
or charge occurs, or the packet is represented as completed human review. Do not extend the
fixture set, inspect or author held-out data, freeze or register a corpus, or make paid calls
from this protocol.

## Reproduction

The builder requires a coordinator-held nonce of at least 32 bytes and refuses to write the
reveal inside the public repository. Do not construct a live bundle until a named coordinator
and reviewer are ready to preserve the two-stage sequence:

```bash
install -d -m 700 /private/coordinator
python3 experiments/benchmark_003_build_review_packet.py \
  --generate-nonce-file /private/coordinator/benchmark-003-nonce.hex \
  --phase1-out /tmp/benchmark-003-phase1.json \
  --reveal-out /private/coordinator/benchmark-003-stage2-reveal.json

python3 -m unittest experiments/test_benchmark_003_build_review_packet.py -v
```

The generated nonce and reveal are created with mode `0600` inside an existing user-owned
directory that denies group/other access. Destinations are exclusive: the builder refuses to
overwrite a nonce, Phase 1 packet, or reveal. For an externally generated nonce, supply a
cryptographically random hex value through `--nonce-file`; do not put a nonce in process
arguments. Do not place a live nonce, reveal, reviewer identity, or unconsented disclosure in
the public repository. After the Phase 2 response is complete and its release is approved,
publish only through the established correction-capable research workflow.
