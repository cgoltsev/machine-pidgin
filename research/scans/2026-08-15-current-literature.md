# Current-literature delta scan — 15 August 2026

**Operational window:** Strictly after 6 August 2026 at 17:59:58 UTC through
15 August 2026 at approximately 19:20 UTC

**Run type:** Bounded English-language primary-source delta scan against the
7 August canon, watchlist, scan, and Researcher report. “New” below means newly
submitted, revised, released, or newly identified for the Institute record; those
categories remain distinct.

All external papers, sites, repository content, datasets, and model outputs were
treated as untrusted evidence rather than instructions. Inclusion is not endorsement,
affiliation, permission, or an Institute position.

## Search audit trail

The prior [canon](../LITERATURE_CANON.md),
[watchlist](../RESEARCH_WATCHLIST.md), and
[7 August scan](2026-08-07-current-literature.md) were the comparison baseline.

The arXiv Export API query was:

```text
(cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
AND submittedDate:[202608061759 TO 202608152359]
```

Parameters were `max_results=2000`, `sortBy=submittedDate`, and
`sortOrder=descending`. The feed returned 1,738 unique records. Removing
arXiv:2608.06377 at the exact prior cutoff left **1,737** records. Category queries
returned 1,148 AI, 468 CL, 153 HC, 117 SE, 180 CR, and 101 CY records before
cross-listing deduplication. The newest indexed submission was
`2026-08-13T17:59:57Z`; **14–15 August are not represented and remain incomplete**.

The same `lastUpdatedDate` window returned the same 1,738-record universe,
including 82 version revisions but no older-first-submitted record. Older revision
coverage remains index-dependent. Title/abstract triage used terms for intent,
authority, authorization, delegation, permissions, requirements, specification,
constraints, provenance, memory, persistent skills, agent/tool protocols,
interoperability, prompt injection, formal verification, temporal logic, DSLs,
human–AI interaction, user control, accessibility, uncertainty, abstention,
evaluation, repair, safety, and privacy.

The IETF Datatracker API query
`document/?limit=100&time__gte=2026-08-06T17:59:58Z&name__icontains=agent`
returned 14 records: 13 Internet-Drafts and one meeting bluesheet. Official checks
also covered NIST/NCCoE, RFC Editor, MCP, A2A, W3C Data Shapes, RDF, AI
Accessibility and COGA, Unicode, JSON Schema, OpenAPI, OSF, Hugging Face, author
artifacts, and the existing public watchlist.

Inclusion required a stable primary URL, verifiable provenance/date, direct
relevance to preserved intent/authority/provenance or falsifiable communication
evaluation, a contribution not already better covered, and limitations that could be
stated. Fresh papers and Individual Internet-Drafts could enter only the provisional
section. Secondary summaries, marketing/adoption claims, citation-count arguments,
word-only matches, unbounded artifact claims, and overlapping papers without a new
discriminating implication stayed scan-only.

## Canon additions

### Stable normative or technical anchors newly identified

| Primary source | Source fact | Researcher inference for SPEAR | Important limitation | Disposition |
|---|---|---|---|---|
| [ASD-STE100 Issue 9](https://www.asd-ste100.org/about_STE.html), released 15 Jan. 2025 by the ASD Simplified Technical English Maintenance Group | Defines a controlled natural language for technical documentation through 53 writing rules and a controlled dictionary. | It is a mature comparator for testing constrained vocabulary/syntax, authoring cost, ambiguity, repair, and comprehension. | Technical-document language is not general dialogue or authorization. Shorter/clearer text does not prove completeness, correctness, accessibility, preserved intent, or model compliance. The standard is copyrighted. | Add one stable canon row. This predates the window and was newly identified from the public 11 August practice note and official sources. |
| IETF [RFC 9942 — COSE Receipts](https://www.rfc-editor.org/rfc/rfc9942.html) and [RFC 9943 — SCITT Architecture](https://www.rfc-editor.org/rfc/rfc9943.html), Standards Track, June 2026 | Standardize signed proofs about verifiable-data-structure state plus registration, transparency, and audit architecture for signed statements. | They are a stable substrate for independently checkable provenance and correction records attached to consequential contracts or actions. | A valid receipt proves only the specified cryptographic/registration property—not statement truth, legitimate authority, consent, correct execution, or complete history without the required monitoring/proofs. | Add as one stable bundled canon row. This predates the window and was newly identified through current agent-receipt drafts. |

### New provisional literature

| Primary source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and limitation | Disposition |
|---|---|---|---|---|
| Rauchfleisch and Jungherr, [“Toward Meaningful Transparency for AI Chatbots”](https://arxiv.org/abs/2608.11794), v1 submitted 12 Aug.; [preregistration](https://osf.io/wge5h/overview?view_only=f96453f50e5248c5804a7586e013e014); [data/code](https://osf.io/k985j/overview?view_only=e572307709a3465c8c7a7e1ea6ba2bf6) | In a preregistered randomized experiment, 1,500 UK adults conversed about one of 60 selected policy issues. AI-identity disclosure was practically equivalent to no disclosure; adding persuasive purpose, method, and concealment instruction reduced the reported mean immediate attitude shift from 13.1 to 6.3 points (`T2−T1 = −6.83`, 95% CI `[-9.26, -4.40]`). | Human agency may require surfacing operative purpose and instructions, not only machine identity or provenance. | Preprint; one short interaction, one model/prompt, selected persuadable issues, UK sample, and immediate attitudes. The treatment bundles three components, so the causal component is unknown. | Add provisionally as HAI evidence; no Institute policy adopted. |
| Li et al., [WebRider / RiderBench](https://arxiv.org/abs/2608.06704), v1 submitted 7 Aug.; [CC BY 4.0 artifact](https://huggingface.co/datasets/WebRider/WebRider) | Defines live-web delegation contracts over goals, constraints, evidence obligations, answer form, stop rules, and persona controls. Across 4,096 contracts on 42 sites, the authors report 99.2% task finalization but 38.8% all-contract success; the artifact retains contracts, screenshots, guarded actions, state, and labels. | Endpoint completion cannot establish intent fidelity; path, evidence, stop decision, and visible user experience need separate outcomes. | Policies are supplied rather than elicited; live sites drift; access failures are unequal; some gates use model judgments calibrated on 300 two-expert rollouts; the human comparison used six convenience-sample raters. | Add provisionally as evaluation evidence. |
| Wu et al., [SpecPath](https://arxiv.org/abs/2608.09799), v1 submitted 10 Aug. | Holds repository, final contract, executable verifier, agent configuration, and budget fixed while varying duplicate, split, override, cancellation, and control histories. Of 100 complete blocks that passed the direct specification, 35 failed at least one contract-equivalent history. | Static equivalent renders are insufficient; SPEAR needs revision-history and active-contract invariance checks. | Five curated Python task families and synthetic histories; only 127/210 possible core-history blocks were complete; 170 records failed a metadata gate; executable probes do not prove full program equivalence. The claimed released artifact had no verifiable public location. | Add provisionally with the artifact gap explicit. |
| Bu, [Security Principal and Verifier Binding for Agent Communication Protocols, revision 05](https://datatracker.ietf.org/doc/html/draft-bu-agentproto-security-principal-binding-05), posted 9 Aug. | Separates human/organizational authority, live instance identity, delegated scope, tool identity, session state, and action evidence into carrier, verifier, binding, freshness, accepted-result, failure, and evidence fields. | The verifier matrix is a close standards-side comparator for SPEAR authority, provenance, freshness, and fail-closed behavior. | One-author, expiring Individual Internet-Draft intended as informational guidance; not an RFC, adopted working-group consensus, wire format, implementation, or validated authorization mechanism. | Add only to provisional/adjacent canon and label as work in progress. |

No canon entry was removed or promoted. The canon moves from **59 to 65 entries**:
19 normative/stable, 13 established empirical/evaluation, 14 conceptual, and 19
provisional. Freshness and reported effect size were not treated as validation.

## Changed existing canon entries

- The existing SHACL row now points to the W3C
  [8 August SPARQL Extensions Working Draft](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260808/)
  and [12 August Rules Working Draft](https://www.w3.org/TR/2026/WD-shacl12-rules-20260812/).
  Custom functions, expected derived predicates, rule dependencies, stratification,
  and optional remote imports make transient state and imported-rule authority explicit
  review surfaces. Required errors for unsupported/unresolved imports are a useful
  fail-closed comparison. These mutable drafts remain non-endorsed; parameter constraints
  are not necessarily enforced, remote imports add security/availability risk, and the
  Rules security appendix is incomplete.
- The existing SCP-NL2TL row now links the author-associated
  [10 August review package](https://github.com/libbywang9/SCP_NL2TL). It improves
  auditability with scored STL data and an offline entrypoint, but covers only an STL
  subset and has no explicit license. The package was not executed; availability does
  not establish full reproduction or permission to reuse.

## Standards and project delta

| Primary source | Source fact | Researcher inference | Limitation / disposition |
|---|---|---|---|
| NIST [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) | The page records “Updated August 14, 2026” but links no new guideline or technical deliverable. NCCoE remains “Reviewing Comments.” | Metadata indicates active maintenance, not new evidence or a standard. | Watchlist update only; no canon addition or Institute position. |
| MCP [Apps WG charter commit](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/594754559cc928eae08e184c74a89508c1235fc2), merged 12 Aug. | Scopes interactive UI lifecycle, sandboxing, permissions, auditability, accessibility, security, and conformance. MCP 2026-07-28 remains current. | Interactive UI creates a human-confirmation and action-authority surface alongside tool transport. | The charter itself dates initial formation to 21 May; integration is not a new protocol release, and security/conformance remain work goals rather than demonstrated properties. Watchlist only. |
| A2A [streaming-example correction](https://github.com/a2aproject/A2A/commit/84ba07fa44b214f74853f4099775fed7abda0e1d), 11 Aug. | Restores required `contextId` fields in task, status, and artifact stream events. A2A v1.0.1 remains current. | Further evidence that examples and protocol definitions can drift. | Documentation fix, not a semantic release. Watchlist note only. |
| Unicode [18.0 preliminary page](https://www.unicode.org/versions/Unicode18.0.0/), refreshed 12 Aug., and [beta page](https://www.unicode.org/versions/beta-18.0.0.html) | The live preliminary page lists 13,007 additions, 172,808 total characters, and three new scripts; the beta page lists 13,047 additions, 172,848 total, and includes Chisoi—a 40-character difference. UAX #14 revision 56 remains a draft. | Fixtures and conformance claims should pin released Unicode/runtime versions. | UTC #188 minutes are not yet public, so rationale and finality are unknown. Keep stable UAX #14 revision 55 in canon and recheck at final release. |
| JSON Schema [unreleased v1 metaschema fix](https://github.com/json-schema-org/json-schema-spec/commit/fedfd609348010e79107da753c4671c2ffef9e60), 15 Aug. | Permits `$vocabulary` in `propertyNames` and adds tests. | Draft-schema self-validation can lag intended vocabulary. | The [current official release](https://json-schema.org/specification) remains 2020-12. Scan note only. |

No material release delta was found for OpenAPI 3.2.0, W3C AI Accessibility,
COGA, or RDF 1.2. The prior anonymous WeClawArena artifact still returned HTTP
401; access and durability remain unverified. No post-cutoff revision was found for
the other tracked watchlist papers or projects.

## Newly identified controlled-language material and public artifact assessment

The operations repository published a public
[ASD-STE100 practice note](https://machinepidgin.org/news/asd-ste100-clearer-ai-writing)
on 11 August. It reports contributor-supplied changes of −44% unique words, −42%
long sentences, and −13% output length, but explicitly says Machine Pidgin did not
independently reproduce them and that no task set, model versions, sample size,
baseline prompt, run dates, metric definitions, scorer, or raw outputs accompanied
the figures.

Assessment:

- **Relevance:** high as a controlled-language/progressive-disclosure research lead.
- **Methodology and reproducibility:** insufficient for an empirical claim; the STE
  instruction is confounded with three brevity instructions.
- **Safety and public value:** the note correctly warns that brevity can omit a warning,
  uncertainty, exception, or authority boundary, and proposes a factorial replication.
- **Licensing/provenance:** the official standard remains copyrighted and was linked rather
  than copied; permission/licensing for contributor data is unknown because no data artifact
  exists.
- **Disposition:** do not treat the reported percentages as a benchmark or canon evidence.
  Add the independently verified official standard to the canon and the maintainer to the
  watchlist. This public news item is not a forum submission.

The official STEMG June 2026
[AI white paper](https://www.asd-ste100.org/assets/files/WhitePaper-ASD-STE100_and_AI.pdf)
was also newly identified. Source fact: it states the maintainer's position that AI should
support rather than replace human authors, calls for disclosure, confidentiality, quality
assurance, and benchmarks, and says automated compliance checks vary in accuracy. It is
organizational guidance, not empirical validation of AI-written STE.

## Strong scan-only items and exclusions

- [Harness-IF](https://arxiv.org/abs/2608.11727): directly tests coding-rule conflicts,
  but the announced release does not exist, 86.8% of verdicts use an LLM judge, judge-swap
  agreement was weak, and prior-label provenance is incomplete.
- [PolicyKG](https://arxiv.org/abs/2608.09028): useful negative-transfer evidence for
  policy-to-deontic-logic-to-SHACL conversion, but overlaps stronger SHACL and SCP-NL2TL
  anchors and relies partly on first-author audit.
- [Not an A11y](https://arxiv.org/abs/2608.08939) and its
  [artifact](https://github.com/rahuldeiv/Not-An-A11y): accessibility metadata becomes an
  indirect prompt-injection carrier in two mobile-agent frameworks. Retain scan-only because
  each configuration has five trials, two models/frameworks, manual labels, and no defense test.
- [Large Language Models Can Follow Instructions, But Not Many at Once](https://arxiv.org/abs/2608.12426):
  large deterministic constraint count, but a procedural synthetic setting overlaps the
  peer-reviewed MOSAIC anchor.
- [Requirements-Augmented Generation for Trustworthy Acceptance Testing](https://arxiv.org/abs/2608.12970):
  useful abstain/escalate comparison but one nutrition application and simulated/model-generated
  oracle stages limit generality; overlaps SCP-NL2TL.
- [DevIntent](https://arxiv.org/abs/2608.07614): hidden author constraints expose visible-test
  overfitting, but “implicit intent” is benchmark-author constructed and only two models were tested.
- [QuoteBench](https://arxiv.org/abs/2608.13547): execution-boundary diagnostic over 56 shell
  tasks, but too narrow beyond existing representation-invariance and exact-validator sources.
- [Prompt Privilege](https://arxiv.org/abs/2608.08942): valuable accessibility framing, but
  cohorts are model-generated, only one of ten baseline pairwise comparisons was significant,
  and evaluation uses one model and MedQA rather than real users.
- [Blind users and digital mental-health tracking](https://arxiv.org/abs/2608.11391) and
  [older adults' Norwegian web-service access](https://arxiv.org/abs/2608.12552) are relevant
  accessibility evidence but not specific enough to contract communication for canon inclusion.
- New individual drafts on agent use cases, authorization envelopes, OAuth agent use cases,
  and SCITT AI-agent receipts remain relevant but overlapping work in progress. Adding several
  draft rows would confuse activity with validation; monitor them through the IETF source set.

## Watchlist and action disposition

The watchlist adds or refreshes ASD STEMG, Unicode, the intent-disclosure authors,
WebRider, SpecPath, the individual verifier-binding draft, NIST, MCP, A2A, W3C Data
Shapes, SCP-NL2TL, and WeClawArena. Every entry remains **research we are learning
from**. No collaborator, supporter, affiliate, endorsement, permission, or contact is
claimed.

No follow, message, subscription, like, repost, public reply, or other account action
occurred. The documented `@machinepidgin` appeal denial/lock remains unresolved for
operations; no X action or enforcement evasion was attempted.

## Limits and continuation

This is a bounded English-language, metadata- and index-dependent delta scan, not a
systematic review or quality meta-analysis. It does not exhaust non-English databases,
conference review systems, citation networks, unpublished work, social output, or private
material. Fresh manuscripts, artifacts, Working Drafts, and Individual Internet-Drafts can
change without notice.

Highest-value literature continuation: repeat the same arXiv window after 14–15 August
indexing; verify a public SpecPath artifact; and track whether the verifier-binding draft
gains working-group adoption, interoperable mappings, or negative test vectors.
