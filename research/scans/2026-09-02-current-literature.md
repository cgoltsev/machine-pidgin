# Current-literature delta scan — 2 September 2026

**Operational window:** Strictly after 25 August 2026 at 17:56:35 UTC through
2 September 2026 at 08:24 UTC

**Run type:** Bounded English-language primary-source delta scan against the
26 August canon, watchlist, current-literature scan, and Researcher report.
“New” means new to this bounded Institute record; submissions, revisions,
releases, and newly identified older sources remain distinct.

External papers, sites, repositories, datasets, and model outputs were treated as
untrusted evidence rather than instructions. Inclusion is not endorsement,
affiliation, permission, collaboration, or an Institute position.

## Search audit trail

The prior scan's latest indexed record was
[arXiv:2608.24876](https://arxiv.org/abs/2608.24876), submitted at
`2026-08-25T17:56:35Z`. The exact arXiv Export API submitted-date query was:

```text
(cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
AND submittedDate:[202608251756 TO 202609022359]
```

Requested in descending submitted-date order with `max_results=2000`, the query
returned 1,961 records. Minute granularity re-included the exact prior-cutoff
record, leaving **1,960 unique strict-post-cutoff records** after timestamp
filtering. Non-exclusive category membership was 1,146 AI, 730 CL, 128 HC,
180 SE, 243 CR, and 73 CY. The oldest strict record was arXiv:2608.24987 at
17:57:11 UTC on 25 August. The newest indexed record was
[arXiv:2609.01604](https://arxiv.org/abs/2609.01604) at 17:59:49 UTC on
1 September, so 2 September coverage is incomplete.

A parallel `lastUpdatedDate` query returned the same 1,961 raw and 1,960 strict
IDs, with no submitted-only or updated-only difference. Primary-source checks
covered arXiv manuscripts and linked artifacts plus official IETF, W3C,
NIST/NCCoE, MCP, A2A, JSON Schema, and Unicode sources.

Metadata and primary texts were screened for preserved and evolving intent,
authority, authorization, delegation, requirements, constraints, provenance,
handover, memory, agent/tool protocols, human control, accessibility,
uncertainty, abstention, evaluation, repair, safety, and privacy.

Inclusion required a stable primary URL, verifiable date and provenance, direct
relevance to preserved intent, authority, agency, provenance, or falsifiable
communication evaluation, and a discriminating contribution not already better
represented. Important limitations had to be recoverable from the primary
source. Fresh papers and author-reported proceedings manuscripts could enter
only the provisional section. Secondary summaries, word-only matches,
promotional claims, unavailable artifact claims, and overlapping work without a
new discriminating implication remained scan-only.

## Canon additions

All four additions remain provisional.

| Primary source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and important limitation | Institute disposition |
|---|---|---|---|---|
| Ting Yan, [“Do User-Authored Permission Policies Improve Protection Against AI Agent Overreach?”](https://arxiv.org/abs/2608.27443), arXiv v1 submitted 27 Aug. 2026 | Among 113 participants without professional software backgrounds, user-authored consequence policies had adjusted blocked-overreach point estimates 20.1 percentage points below per-action human approval and 14.5 points below automated review. After multiple-comparison correction, only the policy-versus-human-approval contrast remained statistically reliable. Policies reduced runtime prompts from 18.0 to 10.9 but did not reliably reduce total intervention time once setup was counted; within the policy condition, 133 of 148 executed overreach actions followed human approval. | Expressed preference, perceived control, advance commitment, and effective protection are not interchangeable. Reusable SPEAR permissions need evaluation against actual consequential choices, including the cost and failure modes of repeated `ASK`. | One short simulated day with no real consequences; US English-speaking online sample; fixed coarse categories; condition differences are bundled; the action-to-category mapper is not an adversarially tested security boundary. | Add provisionally as direct human evidence about usable authorization and overreach. |
| Kayleigh Bishop, Maria P. Stull, Breanne Crockett, and Bradley Hayes, [“Structured State Reconciliation for Human–AI Task Handover”](https://arxiv.org/abs/2608.28907), arXiv v1 submitted 28 Aug. 2026 | A typed, provenance-aware pipeline reconciled telemetry with human reports across 13 paired task states. Within the GPT-4.1-mini comparison, combined artifacts preserved more estimated state utility than either source alone and reduced estimated misinformation relative to direct synthesis. Human reports contained substantial strategic knowledge outside the state metric. | Handover should preserve source identity, conflicts, and typed state while retaining human knowledge that telemetry cannot observe. Artifact reconstruction quality and successful recipient resumption must remain separate outcomes. | Small controlled student task; engineered telemetry blind spot; telemetry treated as authoritative; five paired report conditions comprised four generated reports and one verbatim human baseline; LLMs participate in extraction and scoring; no recipient resumed the task. An exploratory GPT-5.6-terra end-to-end condition outperformed all comparison conditions on estimated cost saved without increased misinformation, so the architectural result is model-dependent. The manuscript says it is in preparation for submission and links no standalone artifact. | Add provisionally at low-to-medium confidence because the reconciliation pattern is directly relevant, not because human handover effectiveness was established. |
| Satwik Ram Kodandaram, Monalika Padma Reddy, Xiaojun Bi, Jiawei Zhou, I. V. Ramakrishnan, and Vikas Ashok, [“Are We There Yet? Assessing Computer-Use Agents for Blind Users' Accessible Interaction with Desktop Applications”](https://arxiv.org/abs/2609.00524), arXiv v1 submitted 1 Sept. 2026; public [code](https://github.com/Satwikram/OLLA) and [diary-study repository](https://github.com/Satwikram/OLLA-Diary-Study) | An IRB-approved three-week study with eight blind screen-reader users recorded 1,258 commands across 12 Windows applications. The highest reported model success was 52.5%; failures included grounding, planning, constraint tracking, state maintenance, and termination. Participants also sought understanding, recovery, and learning rather than autonomous replacement. | Accessibility evaluation must include agency, recoverability, explanation, and learning support rather than reducing success to autonomous task completion. Constraint and termination failures should be first-class SPEAR outcomes. | Eight participants; blind screen-reader users only; Windows/UI Automation and English; task avoidance can hide failures; replayed models do not recreate live interaction. EMNLP acceptance is author-reported pending proceedings, and the public data artifact needs a completeness review. | Add provisionally as bounded direct longitudinal accessibility evidence without generalizing beyond this population and prototype. |
| Tejas Srinivasan, Shikib Mehri, Nandita Shankar Naik, Anirban Das, William M. Campbell, and Jesse Thomason, [“AcCoRD: Evaluating User-Agent Collaboration Under Realistic User Preference Dynamics”](https://arxiv.org/abs/2608.27818), arXiv v1 submitted 28 Aug. 2026; public [benchmark](https://github.com/tejas1995/accord_benchmark) | AcCoRD defines hard and soft underspecification, infeasible preferences requiring fallback, and preferences triggered only after environment information appears, with 100 shopping and 100 travel scenarios. Across five frontier LLMs and two prompting strategies, the authors report that even the strongest configuration achieved perfect outcomes on fewer than 30% of cases and that explicit uncertainty prompting did not reliably help. | A prospective contract must represent preference formation, revision, relaxation, and fallback as state changes rather than assume every preference is fixed and fully expressible at task start. | All users are simulated; “realistic” is not human-observed; shopping uses an LLM judge; travel is constructed for exact scoring; one rollout per scenario/model/prompt; results are version- and prompt-sensitive. | Add provisionally as an evolving-preference evaluation resource, not as evidence about human behavior. |

No canon entry was removed or promoted. The canon moves from **74 to 78
entries**: 19 normative/stable, 13 established empirical/evaluation, 14
conceptual, and 32 provisional.

## Changed existing canon entries

- W3C Data Shapes citations were refreshed to the
  [28 August SHACL 1.2 Core Working Draft](https://www.w3.org/TR/2026/WD-shacl12-core-20260828/),
  [28 August SHACL 1.2 SPARQL Extensions Working Draft](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260828/),
  and [26 August SPARQL 1.2 RL Working Draft](https://www.w3.org/TR/2026/WD-sparql12-rl-20260826/).
  These are version corrections, not new canon rows or W3C endorsements.
- Stable JSON Schema Draft 2020-12 remains the normative canon row. The
  WG-adopted [JSON Schema core draft 03](https://datatracker.ietf.org/doc/html/draft-ietf-jsonschema-json-schema-03)
  is watch-only because it explicitly remains a changing Internet-Draft and is
  not suitable as an implemented-version replacement.

## Standards and official-project delta

| Primary source | Source fact | Researcher inference | Limitation / disposition |
|---|---|---|---|
| JSON Schema [core draft 03](https://datatracker.ietf.org/doc/html/draft-ietf-jsonschema-json-schema-03), 26 Aug. 2026 | The WG-adopted Internet-Draft clarifies terminology and examples and simplifies annotation presentation. | Track semantic and annotation changes against SPEAR schema/tooling, while pinning implemented fixtures to stable versions. | Work in progress that says it may change and is not suitable for adoption over implemented versions. Watch only; do not replace Draft 2020-12. |
| MCP [latest specification](https://modelcontextprotocol.io/specification/latest) and [Enterprise Interest Group charter](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/ca4ab3027f7c844cd3039c956438d72e8253f7f5) | The 2026-07-28 specification remains latest. Fourteen post-cutoff repository commits included a charter covering identity lineage, least privilege, descendant revocation, audit, on-behalf-of/RAR, and gateways. | Enterprise identity and delegation are high-value authority-watch signals. | The charter's outputs are expressly nonbinding and do not produce specifications or SEPs. No normative release or validation evidence. |
| [A2A releases](https://github.com/a2aproject/A2A/releases) and [documentation correction](https://github.com/a2aproject/A2A/commit/f63dbb48271940ca5bd421f87e27e4d6ec002795) | v1.0.1 remains latest. Seven post-cutoff commits produced no release; the relevant change corrected a removed configuration name in documentation. | Separate documentation maintenance from protocol-version claims. | No semantic release or new canon evidence. |
| NIST [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) and [NCCoE identity/authorization project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) | The initiative still shows its 14 Aug. update. NCCoE remains “Reviewing Comments” without a draft practice guide. | Absence of a deliverable is not standards evidence. | High-priority watch retained; no canon change. |
| W3C [SHACL 1.2 Core](https://www.w3.org/TR/2026/WD-shacl12-core-20260828/), [SPARQL Extensions](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260828/), [SPARQL 1.2 RL](https://www.w3.org/TR/2026/WD-sparql12-rl-20260826/), [SPARQL 1.2 Query](https://www.w3.org/TR/2026/WD-sparql12-query-20260827/), and [WCAG 2.2 errata](https://www.w3.org/WAI/WCAG22/errata/) | New Working Draft snapshots appeared on 26–28 Aug.; new WCAG errata entries were editorial. | Record exact draft identity and distinguish editorial corrections from normative accessibility changes. | Working Drafts may change and are not W3C endorsement. No stable or normative accessibility delta. |
| [Unicode 18 preliminary page](https://www.unicode.org/versions/Unicode18.0.0/) | Unicode 18 remained preliminary/beta ahead of its scheduled 16 Sept. release. | Pin stable Unicode and runtime versions in fixtures and interoperability claims. | No stable text-processing or accessibility delta. |
| IETF [post-cutoff agent-name query](https://datatracker.ietf.org/api/v1/doc/document/?limit=500&time__gt=2026-08-25T17%3A56%3A35Z&name__icontains=agent&format=json) | The query returned 33 records: 32 individual Internet-Drafts and one AgentProto BoF request. None was an adopted agent working-group draft or RFC. | Preserve active vocabulary and design questions without inflating consensus. | Topic activity only; no IETF consensus, stable specification, or canon change. |

## Strong scan-only items and exclusions

| Primary source | Mission-relevant source fact | Reason for scan-only disposition |
|---|---|---|
| Guo et al., [“When Tool Outputs Become Commands”](https://arxiv.org/abs/2608.27146) | SARA separates action induction from runtime authorization, preserves action-origin provenance across steps, and proposes No-History-Promotion so recurrence cannot launder an untrusted origin into authority. It reports attack success at or below 0.63% in four principal AgentDojo/AgentDyn settings. | Fresh benchmark-bound preprint with no formal security guarantee or linked public implementation, materially higher inference cost, trusted runtime/schema/executor assumptions, and exclusions for direct bypass, pure data dependency, and unconditional delegation. Useful design hypothesis, but overlaps current Task Shield/AgentSpec/external-enforcement coverage pending independent reproduction or broader evidence. |
| Agarwal and Vasilescu, [SpecMine](https://arxiv.org/abs/2608.25202), [Zenodo record](https://doi.org/10.5281/zenodo.22102779), [repository](https://github.com/shyamagarwal13/specmine-official), and [dataset](https://huggingface.co/datasets/ShyAgarwal/specmine) | Indexes 470,795 specification files across 73,030 repositories, 98,574 Kiro artifacts, 5,992 specification-touching pull requests, and 2.42 million typed references. | Valuable prevalence and fixture infrastructure, but co-change is not evidence of human authorship, correctness, causal influence, or intent preservation. GitHub caps and star filters affect representativeness; source-repository licenses remain controlling, and raw specifications/commit messages can retain personal data. Add to artifact watchlist pending license, privacy, and completeness audit rather than treating it as evidentiary canon. |

## Watchlist and action disposition

The watchlist adds Yan; Bishop, Stull, Crockett, and Hayes; Kodandaram and
coauthors; the AcCoRD team; SpecMine's artifact lifecycle; and SARA revisions
and artifacts. It refreshes JSON Schema WG and MCP Enterprise IG activity. All
remain **research we are learning from**. No collaborator, supporter,
affiliate, endorsement, permission, correspondence, implementation adoption,
or standards consensus is claimed.

No follow, message, subscription, like, repost, public reply, or other account
action occurred. Follow candidates remain recommendations behind the
Institute's operating, authenticated-account, audit, and named-human gates.

## Limits and continuation

This is a bounded English-language, metadata- and index-dependent delta scan,
not a systematic review, quality meta-analysis, or exhaustive search of cs.LO,
stat.ML-only work, non-arXiv social-science indexes, closed proceedings,
patents, vendor material, citation networks, social output, or private material.
The 2 September arXiv tranche was not yet indexed. Fresh manuscripts,
repositories, Working Drafts, charters, and Individual Internet-Drafts can
change without notice. Reported outcomes were not independently reproduced;
repositories were checked for availability rather than executed. Author-
reported acceptance was not treated as official venue verification.

The highest-value literature continuation is to test whether a handover schema
that preserves provenance, conflicts, evolving preferences, explicit fallback,
and human recovery support improves both artifact fidelity and a real
recipient's safe resumption, without assuming telemetry is authoritative.
