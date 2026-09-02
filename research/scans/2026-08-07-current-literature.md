# Current-literature delta scan — 7 August 2026

**Operational window:** 5 August 2026 at 08:07:43 UTC through 7 August 2026 at
approximately 12:00 UTC

**arXiv continuation cutoff:** strictly after 4 August 2026 at 17:59:58 UTC, the newest
submission indexed in the prior scan

**Run type:** Bounded English-language primary-source delta scan against the 5 August canon,
watchlist, and scan. “New” means newly published, revised, or newly identified for the
Institute record; those categories are distinguished below.

All external material was treated as untrusted input. Source claims are not instructions,
and inclusion is not endorsement. No finding establishes an Institute policy, position,
affiliation, partnership, permission, or authority to act.

## Search audit trail

The prior [canon](../LITERATURE_CANON.md), [watchlist](../RESEARCH_WATCHLIST.md), and
[5 August scan](2026-08-05-current-literature.md) were the comparison baseline.

The arXiv export API query was:

```text
(cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
AND submittedDate:[202608041759 TO 202608072359]
```

Parameters were `max_results=1000`, `sortBy=submittedDate`, and `sortOrder=descending`.
The feed was pulled around 7 August 14:57 EEST and carried timestamp
`2026-08-07T11:57:19Z`. The minute-granularity query returned **567 records**; records at or
before the prior second-precision cutoff were removed during filtering. The newest indexed
submission was `2026-08-06T17:59:58Z`. No 7 August submission had yet been indexed, so
**7 August arXiv coverage is incomplete** and must continue next cycle. A comparison
`lastUpdatedDate` query yielded the same record set; a later repeat received HTTP 429.
Accordingly, this report does not claim exhaustive coverage of revisions to older records.

Keywords covered authority, authorization, delegation, provenance, intent, instruction,
specification, requirements, constraints, tool use, prompt injection, memory, protocols,
interoperability, accessibility, formal verification, model checking, human-AI interaction,
oversight, audit, contestability, reversibility, and safety. Twenty-seven likely matches were
shortlisted from titles and abstracts; the strongest papers, manuscripts, supplements, and
linked public project pages were read rather than accepting keyword matches as evidence.

Official primary-source checks covered:

- NIST's [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)
  and the NCCoE [agent identity and authorization project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization);
- MCP's [2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28),
  release history, repository, and new [Agents Working Group charter](https://modelcontextprotocol.io/community/working-groups/agents);
- A2A's [specification](https://a2a-protocol.org/latest/specification/), releases, repository,
  and v1 migration guide;
- W3C publication and repository records for SHACL 1.2, SHACL UI, RDF 1.2, AI
  accessibility, and COGA; and
- tracked repositories or project pages for AuthMem-Bench, STEAD, WeClawArena, MOSAIC,
  ManyIH, AgentSpec, evolving intent, lost-in-conversation, TLA+-Bench, and OpenAPI.

Inclusion required direct relevance to preserved human intent, authority or provenance,
semantic constraint compilation, stateful tool use, human-AI interaction, or a falsifiable
evaluation method; a stable primary URL and verifiable date; a contribution not already
better covered by the canon; and limitations that could be stated. Fresh preprints were
eligible only as provisional evidence. Secondary summaries, marketing/adoption claims,
citation-count arguments, word-only matches, near duplicates, and sources without a
discriminating SPEAR implication were excluded.

## Included new literature

| Source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and limitation | Institute position / disposition |
|---|---|---|---|---|
| Feng, Zhao, and Crisan, [IntentLint](https://arxiv.org/abs/2608.04331), v1 submitted 5 Aug. 2026 at 01:17:45 UTC | IntentLint infers analytic intent from shared notebooks, represents it as structured editable rules, and checks later prompts for conflicts. The paper reports a five-analyst formative study and 16-participant within-subject lab study. For 860 prompt-rule pairs, inter-coder agreement was κ=0.92 and mean LLM-human agreement 0.86; participants made 75 prompt edits with IntentLint versus 40 in baseline and reported clarity medians of 6 versus 3. The manuscript identifies itself as UIST 2026 and supplies a venue DOI; an ACM proceedings record was not independently verified. | This is the most direct HCI evidence in the window for making intent explicit, persistent, human-editable, and available again when a new action is proposed. | Twenty-minute controlled conditions, individuals rather than sustained teams, pre-populated notebooks, flat roles, no longitudinal test of stale/conflicting rules, and documented false positives. It evaluates collaboration experience rather than analytic correctness. | No Institute position adopted. Add as provisional HCI evidence; medium-priority watch candidate only. |
| Chen et al., [“Allow” to Achieve, Over-Privileged Inadvertently](https://arxiv.org/abs/2608.04755), v1 submitted 5 Aug. 2026 at 12:23:16 UTC | Four multimodal models were evaluated over 1,072 Android-style permission-dialog trials. Twenty-four scenarios use a four-level relevance/privacy taxonomy validated by three blinded experts; allow-versus-deny/defer agreement was κ=0.869. In one controlled Calendar task, changing only the visible requester from Calendar to PiMusic changed grants from 26/32 to 0/32. Prompt mitigations reduced excess grants inconsistently and sometimes suppressed legitimate grants. | Task completion can silently broaden permissions; task context and requester identity should be evidence presented to an authorization gate, not substitutes for a separate authority decision. | One agent framework, five applications, synthetic popups, limited permissions/tasks, expert labels rather than diverse user preferences, and no evaluation of the proposed separate authorization layer. | No Institute position adopted. Add as provisional empirical authority evidence; medium-priority watch candidate only. |
| Wang et al., [SCP-NL2TL](https://arxiv.org/abs/2608.05439), v1 submitted 5 Aug. 2026 at 22:17:09 UTC; [project page](https://sites.google.com/ucr.edu/scpnl2tl) | The method adds a black-box accept-or-abstain layer to natural-language-to-temporal-logic translation, combining back-translation, repeated semantic-equivalence checks, conformal risk control, and an embedding-based anomaly screen. Evaluation covers STL, LTL, and SpaTiaL, with 200 calibration and 150 test examples per tier over 100 resplits. | This is a useful fail-closed comparison for SPEAR compilation: a machine-checkable output should be withheld when evidence for semantic preservation cannot support acceptance. | The guarantee is marginal joint risk `E[gZ] <= alpha`, not the conditional error among accepted outputs; it requires exchangeability, holds in expectation, and individual runs may exceed the target. Calibration can yield full abstention; the OOD screen is incomplete; model-based back-translation/judgment and a 114-instruction benchmark remain assumptions. | No Institute position adopted. Add as provisional formal/evaluation work with the narrower guarantee explicit; medium-priority watch candidate only. |
| Chen et al., [“When Experience Becomes Instruction”](https://arxiv.org/abs/2608.05563), v1 submitted 6 Aug. 2026 at 03:32:43 UTC | The paper treats trajectory-to-skill promotion as a trust boundary. With inert canary payloads and 10% attacker support, it reports target behavior entering 546/600 SkillClaw artifacts and 369/600 Trace2Skill artifacts across six evolvers. Deterministic rules define the main artifact-success metric. | Provenance must capture not only where evidence came from but whether that source was authorized to shape durable instructions. Repeated, workflow-aligned evidence can appear legitimate while crossing that authority boundary. | Measures artifact creation, not runtime compromise; uses inert canaries, two trajectory-based systems, one evolution cycle, and excludes user-scoped, verifier-only, and parameter-training systems. No standalone public reproduction repository was verified. | No Institute position adopted. Add as provisional security/authority evidence; medium-priority watch candidate only. |

## Standards and project delta

| Primary source | Source fact | Researcher inference | Uncertainty / limitation | Institute position / disposition |
|---|---|---|---|---|
| W3C [SHACL 1.2 SPARQL Extensions Working Draft](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260806/), published 6 Aug. 2026; [source change](https://github.com/w3c/data-shapes/commit/327f840b24f0288f50fa8f3a6be262271eaeb590) | The revision adds `sh:tempTriple`: inferred triples visible during rule execution and automatically removed afterward, including their reifiers. | Operational reasoning state can affect an outcome without remaining in the final graph, so accountable use needs a distinct durable provenance/event record. | Mutable Working Draft, not a Recommendation; it does not represent intent, authority, consent, or guaranteed audit retention. | Update the existing provisional SHACL canon row; do not add a duplicate. No Institute position changed. |
| W3C [SHACL UI editor draft](https://w3c.github.io/data-shapes/shacl12-ui/), [ordering change](https://github.com/w3c/data-shapes/commit/ae99300e2e2c16a39dae0160a057158e81ef2050), 5 Aug. 2026 | The editor draft gained deterministic presentation-order rules using `sh:order`, `sh:group`, and `shui:defaultOrder`. | Deterministic ordering is relevant to human-facing consistency and representation-invariance tests. | Immature editor draft; accessibility is outside its normative scope. | Watchlist note only; no canon row. |
| MCP [Agents Working Group charter](https://modelcontextprotocol.io/community/working-groups/agents), [merged](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/3f8b0993485373e953d14616527921e71d254550) 5 Aug. 2026 | The group stewards Tasks as a durable asynchronous foundation and considers agent-as-tool, remote-agent, supervisor/subagent, delegation, authorization, metadata, and a possible Agents Extension. The current protocol release remains 2026-07-28. | This is a material standardization direction for durable delegation and agent execution, not yet a normative protocol change. | A charter sets work scope; it does not establish interoperable semantics or implementation conformance. | Update the MCP watchlist note; no canon addition or Institute position. |
| A2A [v1 migration-guide correction](https://github.com/a2aproject/A2A/commit/08b42ebda1490900d1eb560cd67eb77d497d01b3), 6 Aug. 2026 | The correction aligns streaming member names with canonical protobuf definitions and removes nonexistent task/push-configuration fields. A2A v1.0.1 remains the latest release. | This is evidence of documentation/specification drift risk; it is not a change to v1 semantics. | Corrected documentation does not itself establish implementation behavior. | Update the A2A watchlist note; no canon addition or Institute position. |
| W3C RDF Concepts [editor-draft change](https://github.com/w3c/rdf-concepts/commit/ef5a69c6699b1696c776484e79aeee3f71355d39), 6 Aug. 2026 | Version-announcement, content-negotiation, mismatch, downgrade, and absent/inconsistent metadata guidance was revised. Published RDF 1.2 Candidate Recommendation snapshots remain dated 7 Apr. 2026. | SPEAR implementations should not infer semantic capability solely from absent version metadata or assume every consumer fails the same way. | Editor-draft guidance with implementation discretion; no new Recommendation. | Scan/watch note only; keep the April Candidate Recommendation canon anchor. |
| Unicode [UAX #14 revision 55](https://www.unicode.org/reports/tr14/tr14-55.html), stable normative annex for Unicode 17.0 dated 5 Sept. 2025 | Defines mandatory line-break handling, including BK characters and CR, LF, and NL functions, and keeps CRLF together. | This newly identified stable source anchors a portable line-boundary taxonomy for the selected offline agenda. | Not new in the scan window. It does not prescribe input acceptance, escaping, authorization, display, or model behavior. | Add to the normative canon as a previously missing stable specification; no policy is adopted. |

## Status checks with no material delta

- NIST's agent initiative still showed an April 2026 update; the NCCoE identity and
  authorization project remained “Reviewing Comments,” with no new practice guide.
- MCP 2026-07-28 and A2A v1.0.1 remained their current published protocol releases.
- W3C AI accessibility remained an Editor's Draft dated 28 March 2026; COGA research
  modules remained a draft dated 5 February 2026; RDF 1.2 Concepts and Semantics remained
  7 April Candidate Recommendation snapshots.
- OpenAPI remained version 3.2.0. No post-cutoff material repository change was found for
  MOSAIC, ManyIH, AgentSpec, STEAD, evolving intent, lost-in-conversation, or TLA+-Bench.
- AuthMem remained arXiv v2 from 4 August; STEAD and WeClawArena remained v1 from 4 August.
- No dated mission-relevant primary research delta was found on the official Anthropic or
  OpenAI research indexes during the bounded check.

Public pages and repository default branches can lag unpublished work; these are verified
public no-delta findings, not proof that no off-platform work exists.

## Explicit exclusions, deferrals, and negative findings

- [SafeCommit](https://arxiv.org/abs/2608.04289) directly models side-effect authorization
  over plausible latent worlds, but its controlled simulator, assumed world support, and
  representation/calibration dependence overlap stronger existing memory-authority work.
  Monitor; do not add merely for attractive rates.
- [Automatic NL requirements to LTL](https://arxiv.org/abs/2608.06287) covers only 15
  requirements and 450 generations with manual semantic evaluation. SCP-NL2TL provides a
  more discriminating fail-closed contribution.
- [When History Lies](https://arxiv.org/abs/2608.06057) and
  [The Personalization Mirage](https://arxiv.org/abs/2608.04570) are useful bounded evidence
  but overlap the existing memory/evolving-intent stream.
- [MIST / SCOPE](https://arxiv.org/abs/2608.06377) supplies matched context-quality data but
  is less directly tied to legitimate authority than the included sources.
- [OrchestraBench](https://arxiv.org/abs/2608.05263) is a narrow, templated orchestration
  diagnostic without enough distinct evidence for canon promotion.
- [Visual accessibility issues in AI developer tools](https://arxiv.org/abs/2608.05116) is
  mission-relevant for a later accessibility scan, but its 600-report corpus was selected
  primarily by unanimous model classification and only 100 records received manual sanity
  checking. Issue closure does not establish remediation or user impact.
- Broad agent benchmarks, secondary summaries, undated vendor claims, and work with no
  direct specification/authority implication or stable primary source were excluded.
- The prior WeClawArena artifact URL returned HTTP 401 during an anonymous 7 August check.
  This does not prove removal; it may be transient or session-dependent. Independent artifact
  re-verification therefore failed and the durability caveat was strengthened.

## Canon and watchlist disposition

The canon now contains **59 entries**: 17 normative/stable specifications, 13 established
empirical/evaluation sources, 14 conceptual foundations, and 15 explicitly provisional
sources. One stable normative source and four provisional sources were added; no entry was
removed or promoted. The existing SHACL row was updated in place to avoid duplication.

IntentLint, Permission Literacy, SCP-NL2TL, and PoisonedEvolution were added to the public
watchlist at medium priority solely as **research we are learning from**. MCP, A2A, W3C Data
Shapes/RDF, and WeClawArena notes were refreshed. No follow, message, subscription, social
action, or account action was performed. Listing does not claim collaboration, support,
affiliation, endorsement, permission, or contact.

## Limits and continuation

This was an English-language, metadata- and index-dependent delta scan, not a systematic
review, quality meta-analysis, or exhaustive standards search. It did not exhaust conference
review systems, citation networks, non-English databases, work not yet indexed, or older
records whose revisions were not returned before rate limiting. Fresh preprints and mutable
drafts can change without notice.

The highest-priority literature continuation is to repeat the same arXiv window after
7 August indexing, verify proceedings/artifact claims for the four provisional additions,
and remove rather than accumulate entries if stronger primary evidence supersedes them.
