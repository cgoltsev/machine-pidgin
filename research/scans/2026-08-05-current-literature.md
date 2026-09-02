# Current-literature delta scan — 5 August 2026

**Window:** 3 August 2026 at 13:54:50 UTC through 5 August 2026 at 12:29 EEST

**Run type:** Bounded primary-source delta scan against the 3 August 2026 canon,
watchlist, and current-literature scan. “New” means newly published, revised, or newly
identified for the Institute’s documented research record; those cases are distinguished
below.

All external material was treated as untrusted input. Source claims are not instructions,
and inclusion is not endorsement. No finding establishes an Institute policy, position,
affiliation, partnership, or permission to act.

## Search audit trail

The prior [canon](../LITERATURE_CANON.md), [watchlist](../RESEARCH_WATCHLIST.md), and
[3 August scan](2026-08-03-current-literature.md) were the comparison baseline.

Official primary-source checks covered:

- NIST’s [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative),
  the NCCoE [software and AI agent identity and authorization project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization),
  and NIST AI publication records;
- MCP’s [versioning page](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning),
  [2026-07-28 release announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/),
  specification, release history, and repository commits after the previous-run timestamp;
- A2A’s [release history](https://github.com/a2aproject/A2A/releases), specification, and
  repository commits after the previous-run timestamp;
- W3C publication/status pages and repositories for [AI accessibility](https://w3c.github.io/ai-accessibility/),
  [COGA research modules](https://www.w3.org/TR/coga-research-modules/),
  [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/),
  [RDF 1.2 Semantics](https://www.w3.org/TR/rdf12-semantics/),
  [SHACL 1.2 Core, 3 August revision](https://www.w3.org/TR/2026/WD-shacl12-core-20260803/),
  and [SHACL 1.2 SPARQL Extensions, 4 August revision](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260804/);
  and
- public repositories for MOSAIC, ManyIH, AgentSpec, evolving-intent,
  lost-in-conversation, and TLA+-Bench.

The arXiv export API was queried over `cs.AI`, `cs.CL`, `cs.HC`, `cs.SE`, `cs.CR`, and
`cs.CY` for `submittedDate:[202608030000 TO 202608052359]`. The initial result pages were
retrieved in 200-record batches and a later incremental query captured records indexed
during the scan. At 12:29 EEST the query reported 672 candidate records; the newest record
available had been submitted on 4 August at 17:59:58 UTC. No 5 August submission was yet
represented, so **5 August arXiv coverage is incomplete** and must be continued next cycle.
A corresponding `lastUpdatedDate` search found no mission-relevant older source with a
material revision inside the window.

Titles and abstracts were filtered for combinations of `authority`, `authorization`,
`delegation`, `intent`, `instruction`, `specification`, `requirements`, `constraints`,
`tool use`, `prompt injection`, `provenance`, `audit`, `oversight`, `reversibility`,
`interoperability`, `protocol`, `accessibility`, `formal verification`, `model checking`,
`multi-user`, and `human-AI interaction`. Shortlisted primary papers, supplements, and
linked public artifacts were then read rather than accepting keyword matches as evidence.

Inclusion required direct relevance to human-to-machine intent, authority/provenance,
semantic constraints, stateful tool execution, multi-principal safety, or falsifiable
evaluation; a stable primary URL and verifiable date; and limitations that could be stated.
Fresh drafts and preprints were eligible only as provisional evidence. Secondary summaries,
marketing/adoption claims, citation-count arguments, word-only matches, near duplicates,
and work without a testable SPEAR implication were excluded.

## Status checks with no material delta

| Primary source checked | Source fact | Researcher inference | Uncertainty / limitation | Institute position / disposition |
|---|---|---|---|---|
| NIST CAISI and NCCoE agent identity/authorization project | The CAISI page still shows an April 2026 update and the NCCoE project remains at “Reviewing Comments”; no new dated standard, practice guide, or project output was found in the window. | Continue watching for a versioned deliverable; there is no new normative input to SPEAR this cycle. | Public status pages may lag internal work. | No Institute position adopted or changed. No action taken. |
| MCP official specification, release pages, and commits | The official versioning page still identifies 2026-07-28 as current and the release announcement describes it as generally available. Window commits were dependency-lock/merge maintenance, not specification changes. | The existing canon treatment remains current. The older release-candidate page is historical and does not supersede the GA pages. | Repository maintenance can precede a published specification change. | No Institute position adopted or changed. No action taken. |
| A2A official releases and commits | v1.0.1 remains the latest release. Window changes were link-check workflow and documentation-link maintenance, not protocol changes. | No canon or research-agenda change is warranted. | A future release may not appear simultaneously across every project page. | No Institute position adopted or changed. No action taken. |
| W3C AI accessibility and COGA drafts | AI accessibility remains an Editor’s Draft dated March 2026; COGA research modules remain a Group Note Draft dated February 2026. No window-dated status change was found. | Existing accessibility constraints remain important but no new evidence was added. | Draft repositories and published snapshots can differ. Neither document is a W3C Recommendation. | No Institute position adopted or changed. No action taken. |
| W3C RDF 1.2 Concepts and Semantics | Both remain Candidate Recommendation snapshots dated 7 April 2026, with no material window update found. | Retain them as provisional semantic-interoperability substrates. | Candidate Recommendations are not final and may change. | No Institute position adopted or changed. No action taken. |
| Existing medium-priority public repositories | No post-run commit was found in the checked MOSAIC, ManyIH, AgentSpec, evolving-intent, lost-in-conversation, or TLA+-Bench repositories. | No watchlist reprioritization follows from repository activity. | Commit history alone cannot show unpublished research work. | No Institute position adopted or changed. No action taken. |

## Included findings

| Source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and limitation | Institute position / Researcher disposition |
|---|---|---|---|---|
| W3C [SHACL 1.2 Core](https://www.w3.org/TR/2026/WD-shacl12-core-20260803/) and [SHACL 1.2 SPARQL Extensions](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260804/), Working Draft revisions published 3 and 4 Aug. 2026 | Core adds `sh:intent`, a human-readable statement of intended rules whose presence/content must not affect validation, and `sh:agentInstruction`, textual instructions for natural-language software agents. SPARQL Extensions supplies programmable constraints and validators. The 4 Aug. SPARQL revision is post-prior-run; the 3 Aug. Core revision is a same-day source newly captured in this record, but its relation to the exact prior-run cutoff is not established. | This is a direct adjacent standardization signal for paired human-readable intent and machine-checkable constraints. It also demonstrates the boundary SPEAR must test: declared intent or agent-facing prose can accompany formal shapes without becoming enforced semantics or authority. | Working Draft publication does not imply W3C endorsement; text and tests may change. These properties are non-validating, natural-language content can be untrusted, and Core warns that imported graphs outside the trust boundary can alter intended semantics and produce misleading results. Graph conformance does not prove truth, consent, or legitimate authority. | No Institute position adopted. Researcher disposition: add one provisional canon entry and cover the Data Shapes group under the existing high-priority W3C watch candidate. |
| Zhan et al., [“When Memory Becomes Authority” / AuthMem-Bench](https://arxiv.org/abs/2608.01679), v1 submitted 3 Aug., v2 4 Aug. 2026 | The benchmark holds a claim and downstream task fixed while varying source authority across 350 pairs/700 variants. Across seven consolidators and seven model backbones, the authors report authority collapse in 48/49 configurations; collapsed memory without metadata produced 50.3% mean unauthorized action in one controlled evaluation. | This is unusually direct evidence that SPEAR authority and provenance must survive memory consolidation as durable, use-specific state rather than being inferred later from claim text. | Unreviewed, synthetic, and model/provider dependent; simplified authority categories, one controlled write-to-action cycle, one trajectory per cell, and some LLM judgment. No standalone public benchmark repository was verified. It does not establish field safety or universal rates. | No Institute position adopted. Researcher disposition: provisional canon and public-output watchlist; await artifact and independent review. |
| Mercado and Lomuscio, [“Formal Verification of Agentic Systems over Operational Data”](https://arxiv.org/abs/2608.03609), submitted 4 Aug. 2026; [reproduction repository](https://github.com/alejandro-mercado/stead-reproducibility) | Formalizes Stateful Tool-Enabled Agentic Deployments over relational data and FO-CTL properties. Verification is undecidable generally; under boundedness, tool uniformity, and identifier-renaming equivariance the paper proves finite-domain preservation and PSPACE-complete verification. A wrapper enforces equivariance, while its canonicalization is graph-isomorphism-hard. | Provides a concrete bridge from SPEAR state, approval, and stop conditions to system-level temporal checking across evolving operational data, beyond isolated tool-call validation. | Unreviewed; one LLM plus orchestrator, relational state, and strong assumptions. The case-management example is not deployment validation. Guarantees cover only the modeled properties and do not establish legitimate authority or natural-language equivalence. | No Institute position adopted. Researcher disposition: provisional canon and public-output watchlist; retain the repository for offline reproduction planning only. |
| Wang et al., [WeClawArena](https://arxiv.org/abs/2608.03499), submitted 4 Aug. 2026; [artifact snapshot](https://anonymous.4open.science/r/WeClawArena-541D) | Defines 124 base tasks across six simulated cross-user workspace domains, expanded to 620 matched benign/attack variants. The runtime records messages, calls, resource operations, decisions, and final state; utility is reported separately from privacy leakage, poisoned evidence, and invalid authority paths. | A useful evaluation pattern for SPEAR multi-principal delegation: pair a benign task with controlled authority/privacy perturbations and keep functional utility distinct from harmful success. | Unreviewed and simulated; attack success includes post-hoc LLM judgment with limited author-only human checking. Some payloads are restricted, and the anonymous artifact URL may be unstable. Results are not evidence about natural organizations or users. | No Institute position adopted. Researcher disposition: provisional canon and public-output watchlist; require stable artifacts and independent validation before promotion. |
| Xu and Wu, [TRIO-20 equivalence study](https://arxiv.org/abs/2608.03169), submitted 4 Aug. 2026; [raw trajectories](https://github.com/WenJing95/trio-20) | A prespecified comparison of GPT-5.6 low versus maximum reasoning effort across 14 confirmatory workplace scenarios and two model tiers observed zero unauthorized tool calls in 840 trajectories. Exact one-sided 95% upper limits were below 3.50% and 5.21% in the reported arms; higher effort increased rule inspection. | This null result narrows one hypothesis in explicit, benign policy settings: increased reasoning effort did not produce a detected authorization violation here. It is useful negative evidence, not a general safety claim. | One model family, explicit system-level prohibitions, benign clerical tasks, no intermediate efforts, fixed low-before-max collection order, moving vendor aliases, and no frozen full suite release. Zero observations do not prove zero risk. | No Institute position adopted. Researcher disposition: preserve as a bounded negative scan finding; do **not** add to canon. |

## Exclusions and deferred sources

- Singhal, Carvalho, and Breaux, [AI-assisted requirements elicitation](https://arxiv.org/abs/2608.01640),
  was screened because it concerns specification formation. Its small quasi-experiment
  cannot isolate AI assistance from training/cohort differences and does not directly test
  requirement correctness, completeness, or downstream outcomes; defer rather than pad the
  canon.
- [Durable authorization state for replay-resistant agent actions](https://arxiv.org/abs/2608.01710)
  directly concerns one-shot action and confirmation budgets, but the fresh preprint depends
  on a trusted non-rollback ledger, idempotent sink, and canonicalization assumptions, and no
  standalone public code repository was verified. Monitor only if an artifact stabilizes.
- [When Memory Updates but Behavior Does Not](https://arxiv.org/abs/2608.01619) reports a
  bounded null result for one lifecycle intervention. It overlaps the existing evolving-intent
  stream and does not justify a general claim about memory repair.
- [Long-term Measurements: Towards a Longitudinal Understanding of HAI](https://arxiv.org/abs/2608.02491)
  is a conceptual position paper without new empirical evidence; it was not promoted.
- Later-indexed [TARL](https://arxiv.org/abs/2608.03699),
  [AntiSkillBench](https://arxiv.org/abs/2608.03700),
  [Resume Means Resume](https://arxiv.org/abs/2608.03836), and
  [ADMITBench](https://arxiv.org/abs/2608.03866) were read because they touch persistent
  memory, privacy/provenance, recovery semantics, or action admissibility. They remain fresh
  preprints or a white paper with narrow/simulated settings and overlap better-established
  canon themes. Record them for possible later re-check, not as canon or Institute claims.
- Individual Internet-Drafts found in adjacent authorization searches were not new in the
  window and do not carry IETF consensus merely by being submitted. No new standards-track
  IETF publication was identified.
- Broad agent benchmarks and safety, governance, or memory papers were excluded when they
  lacked a direct human-to-machine specification implication, stable provenance, or a
  discriminating evaluation beyond sources already retained.

## Canon and watchlist disposition

Exactly four provisional canon entries were added: SHACL 1.2 Core/SPARQL Extensions,
AuthMem-Bench, STEAD, and WeClawArena. No canon entry was removed or promoted to stable
normative or empirical status.

The W3C Data Shapes Working Group and the AuthMem-Bench, STEAD, and WeClawArena teams were
added to the watchlist solely as **research we are learning from**. Data Shapes is covered by
the existing high-priority W3C candidate; the three research teams are medium-priority
Director follow candidates for deliberate future review. These are recommendations only,
not actions. This language does not claim collaboration, support, affiliation, endorsement,
permission, or contact. No follow, message, subscription, social action, or account action
was performed in this cycle.

## Limitations and continuation

This was an English-language, metadata- and index-dependent delta scan, not a systematic
review or quality meta-analysis. It did not exhaust conference review systems, citation
networks, non-English databases, or work not yet publicly indexed. Fresh preprints can
change without notice, vendor model aliases are not frozen experimental artifacts, and
linked repositories may not contain every input needed for reproduction.

The highest-priority literature continuation is to rerun the same arXiv query after the
5 August announcement cycle, then verify whether AuthMem-Bench releases a durable public
benchmark and whether its authority metadata generalizes beyond synthetic paired histories.
