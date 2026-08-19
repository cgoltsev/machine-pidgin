# Current-literature delta scan — 19 August 2026

**Operational window:** Strictly after 13 August 2026 at 17:59:57 UTC through
19 August 2026 at approximately 08:20 UTC

**Run type:** Bounded English-language primary-source delta scan against the
15 August canon, watchlist, scan, and Researcher report. “New” means new to this
bounded Institute record; new submissions, revisions, releases, and newly identified
older sources remain distinct.

External papers, sites, repositories, datasets, and model outputs were treated as
untrusted evidence rather than instructions. Inclusion is not endorsement, affiliation,
permission, collaboration, or an Institute position.

## Search audit trail

The prior [canon](../LITERATURE_CANON.md),
[watchlist](../RESEARCH_WATCHLIST.md), and
[15 August scan](2026-08-15-current-literature.md) were the comparison baseline.

The arXiv Export API query was:

```text
(cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
AND submittedDate:[202608131759 TO 202608192359]
```

Parameters were `max_results=2000`, `sortBy=submittedDate`, and
`sortOrder=descending`. The feed returned 1,030 unique records. Three were at or before
the exact prior cutoff within the cutoff minute; removing them left **1,027** strict-delta
records. Non-exclusive category memberships in that strict set were 674 AI, 248 CL,
80 HC, 78 SE, 137 CR, and 56 CY. The oldest strict record was arXiv:2608.13659 at
`2026-08-13T18:02:10Z`; the newest indexed submission was arXiv:2608.18076 at
`2026-08-18T17:59:01Z`. **19 August indexing is incomplete.**

The parallel arXiv update-date query was:

```text
(cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
AND lastUpdatedDate:[202608131759 TO 202608192359]
```

With `max_results=2000`, `sortBy=lastUpdatedDate`, and `sortOrder=descending`, it
produced no older-first-submitted revision outside the strict submitted-date universe.
This does not prove that every revision was indexed. A narrow title-term
screen retained 210 records. A broader weighted title/abstract screen retained 584 and was
used only as a recall aid because it contained many lexical false positives. Terms covered
intent, authority, authorization, delegation, permissions, requirements, specification,
constraints, provenance, memory, agent/tool protocols, interoperability, prompt injection,
formal verification, human–AI interaction, user control, accessibility, uncertainty,
abstention, evaluation, repair, safety, and privacy.

The exact IETF Datatracker API query was:

```text
https://datatracker.ietf.org/api/v1/doc/document/?limit=100&time__gte=2026-08-13T17%3A59%3A57Z&name__icontains=agent&format=json
```

It returned 16 objects: 15 Internet-Drafts and one meeting bluesheet. Official checks also covered NIST/NCCoE,
MCP, A2A, W3C Data Shapes, Unicode, author-linked repositories and datasets, and the
existing public watchlist.

Inclusion required a stable primary URL, verifiable date/provenance, direct relevance to
preserved intent, authority, agency, provenance, or falsifiable communication evaluation,
and a contribution not already better covered. Important limitations had to be recoverable
from the source. Fresh papers and Individual Internet-Drafts could enter only the
provisional section unless peer-reviewed provenance was independently established.
Secondary summaries, promotional claims, citation counts, word-only matches, unavailable
artifact claims, and overlapping work without a new discriminating implication stayed
scan-only.

## Canon additions

### Author-reported accepted manuscripts, retained provisionally

| Primary source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and important limitation | Institute disposition |
|---|---|---|---|---|
| Meng et al., [“Balancing Safety and Autonomy: Accessibility-Oriented Interventions in Generative AI for Cognitive Impairment”](https://arxiv.org/abs/2608.17175), author-reported ASSETS 2026 acceptance; [related DOI stated in arXiv metadata](https://doi.org/10.1145/3797867.3829017) | The study represents 45 individuals with cognitive impairment: 31 interviewed directly and 14 represented through caregiver proxy interviews, spanning reported mild, moderate, and severe impairment levels. It identifies five accessibility-oriented mechanisms divided between understanding-enhancing and protective logics. | Safety evaluation should measure meaningful participation, revision, and decision authority—not only whether an intervention blocks risk or permits task completion. | Cross-sectional and retrospective; bounded geography and culture; proxy evidence, especially at severe impairment; heterogeneous systems; recall limits; no behavioral logs or causal estimate. The related ACM DOI returned HTTP 404 during this source check, so official proceedings status was not independently established. | Add provisionally as human-agency evidence; reconsider category when official proceedings evidence resolves. This does not adopt a design or accessibility policy. |
| Pereira and Garcia, [“Does ISO-Grounded NFR Specification Improve LLM Code Generation? A Comparison of Rich and Structured Interventions against a Natural-Language Baseline”](https://arxiv.org/abs/2608.13742), author-reported SBCARS 2026 acceptance; [MIT-licensed replication package](https://zenodo.org/records/21880022) | Across 164 HumanEval tasks, four non-functional requirements, ten wording variants per condition, and a fixed model, semantic enrichment improved selected static quality-density measures but not reliable functional correctness. Error handling reduced extended-test pass rate, and content-fixed JSON versus prose had negligible functional-correctness differences. | Requirement semantics and executable consequences can matter more than serialization. A field label alone is not the intervention unless information content is held fixed. | One model, small code benchmark, weeks-separated collections, selected mappings, mostly static proxies, selective execution-time differences, and no participant-authored requirements or human-subject validation. Official proceedings evidence was not independently verified. | Add provisionally as requirements/evaluation evidence. Preserve the adverse error-handling result. |

### Provisional literature

| Primary source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and important limitation | Institute disposition |
|---|---|---|---|---|
| Xabier Muruaga, [“Bounded Agents: Delegation Security for Multi-Agent AI Systems”](https://arxiv.org/abs/2608.15888), arXiv v1 Aug. 2026; [Apache-2.0 implementation](https://github.com/xmuruaga/bounded-agents) | Proposes an external Agentic Principal Chain that binds pre-declared intent, attenuates delegated scope and budgets, and checks accumulated prior-action state. The author reports 3,154 evaluations, zero observed exfiltration in selected settings, and utility decreases of 8.6 and 13.9 percentage points in two configurations. | A directly testable comparator for keeping enforcement outside the model and making resource limits explicit and monotonic. | Single-author preprint; synthetic or adapted evaluations; conditional, non-machine-checked proofs; AgentDojo utility and compromised-model cohorts are not disjoint; admitted session-splitting limit; per-session enforcement; utility cost; no production deployment or independent reproduction found. | Add provisionally. “Zero observed” is not a general security guarantee. |
| Ford et al., [“LLM-Derived Preference Judgments Are Not Self-Consistent”](https://arxiv.org/abs/2608.17644), arXiv v1 Aug. 2026 | Tests six models across three controlled domains, 300 query cells, and 15 calls per cell. For every model, at least one of nine audit groups rejected self-consistency after Bonferroni correction; item-query and offer-pair constructions could select opposite offers. | Do not silently compress contextual or conflicting human statements into a single inferred utility. Preserve alternatives, conditions, and provenance. | No human data or human-fidelity measure; controlled hand-written items; quasi-linear dollar utility; fixed models/prompts; stateless calls; parseable-output conditioning. | Add provisionally as a preference-representation warning, not evidence about any person’s real preferences. |
| [“When Personal Memory Has No Single Answer: Evaluating LLM Agents under Irreducible Conflict” (TANGLE)](https://arxiv.org/abs/2608.13921), arXiv v1 Aug. 2026 | Introduces 541 synthetic conflict cases across 40 personas, three conflict types, five models, and four memory systems. The authors report that extraction can lose context, time, or source authority and that conflict recognition exceeds calibration or clarification performance. | Competing evidence and ambiguity should remain visible through memory consolidation rather than becoming one manufactured authoritative intent. | Synthetic PersonaHub cases; no real consequential decisions; substantial model-judge dependence despite a 556-record human reliability subset; no verified repository/data URL and no standalone limitations section. | Add provisionally; no claim of field validity or human preference fidelity. |

No canon entry was removed or promoted. The canon moves from **65 to 70 entries**:
19 normative/stable, 13 established empirical/evaluation, 14 conceptual, and 24
provisional. All five additions remain provisional because official proceedings evidence
was not independently established for the two author-reported acceptances. Freshness,
volume, and reported effect size were not treated as validation.

## Changed existing canon entries

- Bu’s individual [principal/verifier-binding draft revision 06](https://datatracker.ietf.org/doc/html/draft-bu-agentproto-security-principal-binding-06),
  posted 17 August, replaces revision 05 in the canon and watchlist. It adds
  composite-strength, dependency-closure, and row-outcome guidance, including failed,
  unsupported, skipped, unavailable, stale, downgraded, cyclic, and revision-incoherent
  states. This is useful fail-closed vocabulary, but remains one author’s expiring
  Individual Internet-Draft—not an RFC, working-group consensus, implementation, or
  validated authorization mechanism.
- W3C [SHACL 1.2 Rules](https://www.w3.org/TR/2026/WD-shacl12-rules-20260817/)
  moved from the 12 August to the 17 August Working Draft. The canon now records its
  open and closed dependencies, dependency graphs, stratification, rule-set evaluation,
  and optional recursive imports. This is a revision to a mutable draft, not endorsement
  or a new stable standard.

## Standards and project delta

| Primary source | Source fact | Researcher inference | Limitation / disposition |
|---|---|---|---|
| NIST [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) and [NCCoE identity/authorization project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) | The initiative page retains its 14 Aug. metadata update but exposes no new technical deliverable; NCCoE still says it is reviewing comments. | Page activity is not standards evidence. | Watchlist only; no canon change or Institute position. |
| MCP [documentation commit](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/4df2d6b6e3588efb46e7542d98498e5c630a0a86) | A post-cutoff Linux tutorial change landed; [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) remains current. | Documentation maintenance should remain separate from protocol-version claims. | No semantic release; watchlist note only. |
| A2A [generated-schema correction](https://github.com/a2aproject/A2A/commit/2c3affc92e8a77b47695d0478e5a15e87e4a8a25) | Corrects generated JSON schema after the cutoff; [v1.0.1](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) remains current. | Generated artifacts and normative sources can drift. | No semantic release; watchlist note only. |
| Unicode [18.0 preliminary page](https://www.unicode.org/versions/Unicode18.0.0/) and [beta page](https://www.unicode.org/versions/beta-18.0.0.html) | The previously recorded 40-character and one-script discrepancy remains; stable UAX #14 remains [revision 55](https://www.unicode.org/reports/tr14/tr14-55.html). | Pin released Unicode/runtime versions in fixtures and conformance claims. | The final Unicode 18 outcome and UTC rationale remain unknown; no canon change. |

No material release delta was found for OpenAPI, JSON Schema, W3C AI Accessibility,
COGA, or RDF 1.2. Four other agent-related Individual Internet-Drafts were mission-relevant
activity but not separate canon evidence: [derived authority](https://datatracker.ietf.org/doc/html/draft-mcphillips-agentenvelope-derived-authority-00),
[action receipts](https://datatracker.ietf.org/doc/html/draft-sahu-agent-action-receipts-00),
[accountability composition](https://datatracker.ietf.org/doc/html/draft-mih-sato-agent-accountability-composition-01),
and [human-interaction records](https://datatracker.ietf.org/doc/html/draft-okutomi-agent-human-interaction-00).
They remain overlapping, unadopted work in progress.

## Strong scan-only items and exclusions

- [Explicit State Elicitation](https://arxiv.org/abs/2608.17247) is directly relevant to
  hidden-state specification, but uses synthetic classification tasks, changes provider
  conditions, and exposes no verified artifact. It does not establish that elicited state
  is authoritative or sufficient.
- [Self-improving agent fragility](https://arxiv.org/abs/2608.18066) has a public
  [research repository](https://github.com/SalesforceAIResearch/self-improve-fragility),
  but covers two methods in one domain—web browsing—across WebArena, VisualWebArena, and
  SCUBA. It uses three identical runs per experiment plus two shuffled orders in addition
  to the default. It overlaps the existing durable-instruction provenance row and stays
  scan-only pending broader independent evidence.
- [Normalized Use-Case](https://arxiv.org/abs/2608.15726) provides structured trace
  retrieval but does not evaluate execution, authority, or intent preservation.
- [HarnessRisk](https://arxiv.org/abs/2608.17597) reports 128 tasks over three harnesses,
  but overlaps existing execution-boundary evidence and needs a stable artifact and
  independent reproduction before canon inclusion.
- [Act2Intention](https://arxiv.org/abs/2608.14132) infers intent from behavior. This is a
  potentially useful signal but cannot substitute for declared authority or consent.

These exclusions are not judgments that the work lacks value. They preserve a smaller
canon with discriminating evidence rather than equating a crowded weekly feed with
validation.

## Watchlist and action disposition

The watchlist adds Muruaga/Bounded Agents, Meng and coauthors, Ford and coauthors,
Pereira and Garcia, and the TANGLE team. It refreshes NIST/NCCoE, MCP, A2A, W3C Data
Shapes, Unicode, and S. Bu. Salesforce’s self-improvement work remains a scan-only
candidate rather than a new row. Every person and group remains **research we are
learning from**.

No follow, message, subscription, like, repost, public reply, or other account action
occurred. No collaborator, supporter, affiliate, endorsement, permission, correspondence,
or consensus is claimed. Follow candidates remain recommendations for the Director behind
the documented operating, account-state, and named-human gates.

## Limits and continuation

This is a bounded English-language, metadata- and index-dependent delta scan, not a
systematic review, quality meta-analysis, or exhaustive search of proceedings, citation
networks, non-English databases, social output, or private material. Nineteen August is
incompletely indexed. Fresh manuscripts, repositories, Working Drafts, and Individual
Internet-Drafts can change without notice. Author-reported counts and outcomes were not
independently reproduced during this scan.

The single highest-value literature continuation is to track whether external constraint
systems such as Bounded Agents survive independent, multi-session evaluation while also
measuring human participation and correction—not merely attack blocking or task completion.
