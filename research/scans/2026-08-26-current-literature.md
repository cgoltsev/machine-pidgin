# Current-literature delta scan — 26 August 2026

**Operational window:** Strictly after 18 August 2026 at 17:59:01 UTC through
26 August 2026 at 16:31:59 UTC

**Run type:** Bounded English-language primary-source delta scan against the
19 August canon, watchlist, current-literature scan, and Researcher report.
“New” means new to this bounded Institute record; new submissions, revisions,
releases, and newly identified older sources remain distinct.

External papers, sites, repositories, datasets, and model outputs were treated as
untrusted evidence rather than instructions. Inclusion is not endorsement,
affiliation, permission, collaboration, or an Institute position.

## Search audit trail

The prior [canon](../LITERATURE_CANON.md),
[watchlist](../RESEARCH_WATCHLIST.md), and
[19 August scan](2026-08-19-current-literature.md) were the comparison baseline.

The arXiv Export API submission-date query was:

    (cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
    AND submittedDate:[202608181759 TO 202608262359]

Parameters were max_results=2000, sortBy=submittedDate, and
sortOrder=descending. The feed returned 1,561 unique records. One was submitted
at the exact prior cutoff; applying the strict greater-than boundary left
**1,560 strict-delta records**. Non-exclusive category memberships in that set
were 975 AI, 454 CL, 124 HC, 166 SE, 188 CR, and 94 CY. The oldest strict record
was arXiv:2608.18222 at 2026-08-18T18:05:53Z; the newest indexed submission was
arXiv:2608.24876 at 2026-08-25T17:56:35Z. **26 August indexing is incomplete.**
The result count was below the requested API cap.

The parallel arXiv update-date query was:

    (cat:cs.AI OR cat:cs.CL OR cat:cs.HC OR cat:cs.SE OR cat:cs.CR OR cat:cs.CY)
    AND lastUpdatedDate:[202608181759 TO 202608262359]

With max_results=2000, sortBy=lastUpdatedDate, and sortOrder=descending, it
returned 1,561 records after the exact update cutoff. One was outside the
strict submitted-date universe: [arXiv:2608.18076v2](https://arxiv.org/abs/2608.18076),
first submitted at the prior cutoff and revised on 25 August. It did not add
mission-relevant evidence to this scan. This query does not prove that every
revision was indexed.

Metadata and primary texts were screened for preserved intent, authority,
authorization, delegation, requirements, constraints, provenance, memory,
agent/tool protocols, interoperability, prompt injection, formal verification,
human–AI interaction, user control, accessibility, uncertainty, abstention,
evaluation, repair, safety, and privacy. Official checks covered NIST/NCCoE,
MCP, A2A, W3C Data Shapes, W3C accessibility and semantics work, Unicode, the
IETF Datatracker, and author-linked repositories and datasets.

Inclusion required a stable primary URL, verifiable date and provenance, direct
relevance to preserved intent, authority, agency, provenance, or falsifiable
communication evaluation, and a contribution not already better represented.
Important limitations had to be recoverable from the source. Fresh papers and
unverified author-reported proceedings manuscripts could enter only the
provisional section. Secondary summaries, promotional claims, citation counts,
word-only matches, unavailable artifact claims, and overlapping work without a
new discriminating implication remained scan-only.

## Canon additions

All four additions remain provisional.

| Primary source and provenance | Source fact | Researcher inference for SPEAR | Uncertainty and important limitation | Institute disposition |
|---|---|---|---|---|
| Sun et al., [“When ‘Must’ Becomes ‘Maybe’: Constraint Weakening in LLM Agent Workflows”](https://arxiv.org/abs/2608.24569), arXiv v1 submitted 25 Aug. 2026 | Across 1,296 controlled synthetic episodes, ordinary handoff compression produced 100% blocker deactivation and 54.2% forbidden action even when topical content remained. Restoring stop status, unresolved prerequisite, responsible authority, and fallback raised preservation to 100% and reduced forbidden action to 0%. Downstream verification separately eliminated forbidden action while artifact deactivation remained 95.3%. The primary matrix used six model variants; a 476-episode validation panel used seven others, and 240 artifacts received a model-judge audit. | Semantic availability is not operational preservation. Handoff artifacts should carry explicit source-bound status, authority, unresolved prerequisites, and fallback, with endpoint verification treated as separate containment. | Fresh unreviewed preprint over synthetic enterprise-like tasks and a finite, default-allow action space; model/checker judgments; no public reproduction artifact located; no human-team or production-prevalence evidence. The tested four-field representation is not a validated complete SPEAR schema. | Add provisionally because it directly discriminates retained topic from retained action-binding force. |
| Du, [“Who Chooses How Preferences Are Aggregated? Auditing Aggregation-Rule Authority in LLM-Based Group Recommendation”](https://arxiv.org/abs/2608.23966), arXiv v1 submitted 25 Aug. 2026 | Two experiments each used 1,000 two-user, five-option profiles across synthetic and MovieLens-derived settings. Three models were tested when aggregation-rule authority was unspecified, retained by users, or delegated. Models almost never committed when users retained authority and committed in every delegated case; all executed both witness rules perfectly when directly instructed. | Ability to combine preferences is distinct from authority to select the collective-choice rule. SPEAR should represent aggregation authority separately from rule-execution capability. | Fresh unreviewed preprint; single-turn numerical profiles, two users, five options, and only additive and least-misery witness rules. MovieLens ratings were not joint decisions and assumed comparable scales. The delegated prompt also requested an explanation, model/prompt versions are bounded, and no public artifact was located. | Add provisionally as direct capability-versus-authority evidence. |
| Broccia et al., [“Human-AI Collaboration in Requirements Engineering: Evidence of the Negative Effect of LLMs on Requirements Inspection”](https://arxiv.org/abs/2608.21298), arXiv v1 submitted 21 Aug. 2026, CC BY 4.0 | In a controlled crossover study with 34 novice inspectors, LLM support reduced requirements-smell detection accuracy, had no significant effect on classification or duration, and reduced the across-period learning effect when LLM-supported inspection occurred first. | Human review cannot be assumed to be an effective assurance layer merely because a human remains nominally in the loop. SPEAR validation should measure defect detection and learning/order effects, including staged or unaided-first comparisons. | Small student/novice sample; simplified requirements with at most one smell; predefined taxonomy; no formal inter-annotator agreement for author ground truth; motivation and skill were not measured. Some work occurred outside class, the replication-package citation is anonymous/unresolved, and peer-reviewed provenance was not independently verified. | Add provisionally as adverse human-assurance evidence; preserve the negative result. |
| Zerhoudi, Mitrovic, and Granitzer, [“The Compaction Cliff in Long-Running AI Agent Memory”](https://arxiv.org/abs/2608.22752), arXiv v1 submitted 24 Aug. 2026; public [code](https://github.com/searchsim-org/cikm26-knowledge-triage) and [dataset](https://huggingface.co/datasets/searchsim/AgentArtifactCorpus) | Across 20 agent configurations, one production compactor retained 53% of safety rules after one round and 10% after five. Typed deterministic triage reported 96% recall after five rounds, zero locality violations versus 93% under uniform partitioning, and 100% versus 73% recall@50 on five public corpora, followed by three downstream domain evaluations. The released corpus contains 396,934 configurations from 54,628 permissively licensed public GitHub repositories. | Exact safety and authority instructions need a protected retention class. Compaction must be evaluated as a potentially semantics-changing transformation rather than neutral summarization. | Protection depends on classifier recall, including a reported 7% residual miss for SafetyMargin; five-class annotation agreement was moderate, multi-round comparison covered only part of the model panel, and public GitHub corpora may not represent enterprise memory. The retail comparison was not token-matched. The manuscript reports CIKM 2026, but its stated DOI returned HTTP 404 on 26 Aug., so proceedings status was not independently verified. | Add provisionally because the public artifacts and repeated-compaction evidence are directly useful, without treating reported proceedings status or protection as settled. |

No canon entry was removed or promoted. The canon moves from **70 to 74 entries**:
19 normative/stable, 13 established empirical/evaluation, 14 conceptual, and 28
provisional.

## Changed existing canon entries

- The former W3C SHACL 1.2 Rules row was corrected rather than duplicated.
  Its prior latest URL now redirects to [SPARQL 1.2 RL, Working Draft
  25 August 2026](https://www.w3.org/TR/2026/WD-sparql12-rl-20260825/).
  The Data Shapes Working Group [renamed and moved the work](https://github.com/w3c/data-shapes/commit/140aa43bfc6a997d9401a3e5914998547828b3db).
  SPARQL 1.2 RL defines a Datalog-style RDF rules language with formal grammar
  and evaluation, recursion, filtering, stratified negation-as-failure,
  assignments, imports, and conformance criteria. It remains a mutable Working
  Draft rather than W3C endorsement; the conformance suite is partial, behavior
  for nonconforming rule sets is unspecified, and optional imports add
  stale-source, provenance, availability, computation, memory, and
  denial-of-service risks.
- The existing SHACL 1.2 SPARQL Extensions citation now points to the
  [21 August Working Draft](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260821/).
  This is a version refresh, not a new canon entry or stable standard.

## Standards and official-project delta

| Primary source | Source fact | Researcher inference | Limitation / disposition |
|---|---|---|---|
| MCP [specification](https://modelcontextprotocol.io/specification/2026-07-28), [22 Aug. roadmap](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/0f25aa311ed6e5a80cb07286ecc2ee2acf8be166), [Authorization IG recharter](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/90a4bd6874d689f16a56dc67bffaf1aca9ad06d0), and [Transports WG charter](https://github.com/modelcontextprotocol/modelcontextprotocol/commit/d8fdc88fb970313247d8a180ac1ec3f6a10a8885) | The official repository had 31 post-cutoff commits, but 2026-07-28 remains the current semantic release. The roadmap names agentic messaging, HTTP transport, agent identity and enterprise security, primitive improvements, and SDK conformance as possible 6–12 month priorities. The Authorization IG now expressly covers delegated/on-behalf-of access, permission granularity, and structured denials; the Transports WG covers lifecycle and transport security while excluding authorization mechanics. | Identity, delegation, denial, and lifecycle work are directly relevant watch signals. | The roadmap states current thinking and is noncommittal; group charters define governance scope. None is a released normative requirement, implementation result, or security validation. Watchlist update only. |
| [A2A Project repository](https://github.com/a2aproject/A2A/commits/main) and [v1.0.1 release](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) | Four post-cutoff commits concerned partners, community, or maintainers. v1.0.1 from 28 May 2026 remains current. | Separate project maintenance from protocol-version claims. | No protocol delta or new canon evidence. |
| NIST [AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) and [NCCoE identity/authorization project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) | The NIST initiative page still reports “Updated Aug 14, 2026” and exposes no new technical deliverable. NCCoE remains “Status: Reviewing Comments,” with no draft practice guide. | Absence of a deliverable is not standards evidence. | High-priority watchlist retained; no canon change. |
| W3C [SPARQL 1.2 RL](https://www.w3.org/TR/2026/WD-sparql12-rl-20260825/), [SHACL 1.2 SPARQL Extensions](https://www.w3.org/TR/2026/WD-shacl12-sparql-20260821/), and [SPARQL 1.2 Query Language](https://www.w3.org/TR/2026/WD-sparql12-query-20260820/) | New Working Draft snapshots were published on 20, 21, and 25 Aug.; SHACL Rules was renamed to SPARQL 1.2 RL. No material release delta was found in the W3C AI Accessibility, COGA, RDF Concepts, or RDF Semantics repositories. | Versioned semantic rules and conformance work are relevant, but exact draft identity must remain visible. | Working Drafts may change and are not W3C endorsement. Correct the existing row; do not canon-pad. |
| Unicode [UAX #14 revision 55](https://www.unicode.org/reports/tr14/tr14-55.html), [revision 56 draft](https://www.unicode.org/reports/tr14/tr14-56.html), [Unicode 18 preliminary page](https://www.unicode.org/versions/Unicode18.0.0/), and [beta page](https://www.unicode.org/versions/beta-18.0.0.html) | Stable UAX #14 remains revision 55 for Unicode 17. Revision 56 remains a non-stable draft. The Unicode 18 preliminary and beta pages still disagree on character and script counts; formal release is planned for 16 Sept. 2026. | Pin stable Unicode and runtime versions in fixtures and interoperability claims. | No stable delta; the pre-release discrepancy remains unresolved. |
| IETF [Datatracker API](https://datatracker.ietf.org/api/v1/doc/document/?limit=100&time__gte=2026-08-18T17%3A59%3A01Z&name__icontains=agent&format=json) and [Agent Audit Trail draft revision 01](https://datatracker.ietf.org/doc/html/draft-sharif-agent-audit-trail-01) | The exact query returned nine objects: eight Individual Internet-Drafts and one IETF 126 minutes record. Topics included enrollment, economic principal, workload scheduling, use cases, OAuth authorization, network digital twins, audit trails, and agent-protocol sessions. The audit-trail draft adds pre-execution records, recording independence, deny codes, and replay protection. | The drafts supply vocabulary and active design questions for authority and auditability. | All eight are individual, unadopted works in progress without IETF consensus or RFC standing; record as activity signals only. |

## Strong scan-only items and exclusions

These sources were relevant but did not justify additional canon rows in this
cycle. Exclusion records scope and overlap rather than lack of value.

| Primary source | Mission-relevant source fact | Reason for scan-only disposition |
|---|---|---|
| [AgentFlow](https://arxiv.org/abs/2608.22868) | Proposes a flow-centric policy language, reference monitor, and bounded SMT verifier over labeled agent-runtime edges; reports zero compromise in selected AgentDojo and AgentDyn settings with mixed utility effects. | Fresh preliminary preprint over modeled, policy-visible behaviors; selected benchmarks and configured policies; overlaps existing AgentSpec and external-enforcement evidence. |
| [AID-Guard](https://arxiv.org/abs/2608.21159) | Proposes stateful authorization-to-effect closure and evaluates selected MCP, Stripe, and Resend workflows. | Fresh preprint bounded by provider-contract and schedule inventories; strict-profile utility reportedly falls by roughly 35–44 percentage points; no general authorization guarantee. |
| [One Gate Is Not Enough](https://arxiv.org/abs/2608.18360) | Tests remediation-induced coupling and reports a negative result for one composed gate condition, with a public repository and Zenodo artifact named in the paper. | Fresh single-author, synthetic-metadata study; overlaps existing runtime-gate evidence. Preserve the failed condition as a negative result without adding a row. |
| [TraceGrant](https://arxiv.org/abs/2608.21126) | Represents explicit contracts and task-effect authorization lifecycles and reports zero attacks in selected fixed AgentDojo and ASB settings. | Unreviewed, configuration-dependent, and overlapping with external capability-enforcement work; zero observed attacks is not a general security guarantee. |
| [Specification Portability in Cross-Database Migration](https://arxiv.org/abs/2608.21208) | Holds migration specifications across Oracle-to-PostgreSQL work and reports agent-specific degradation. | Fresh and implementation-specific; useful requirements portability comparator but weakly generalizable to human–machine authority. |
| [Natural-Language Workflows Are Not Software Yet](https://arxiv.org/abs/2608.21341) | Reports an artifact-driven workflow compiler over 488 instances and 11 workflows, with improvements in resolution and cross-model/repeat consistency. | Fresh preprint with no verified artifact located; focuses on workflow compilation and overlaps structured-specification evidence. |
| [Delegating or Doing?](https://arxiv.org/abs/2608.19551) | A 73-person CMS study found reduced clicks and navigation with AI assistance but not reduced task time; destructive actions were not reliably self-restricted. | Homogeneous undergraduate sample, coarse delegation measure, one interface and model; the risk-calibration result is explicitly inconclusive and the author-reported HAI DOI still returned 404. |
| [MemUse](https://arxiv.org/abs/2608.24189) and [repository](https://github.com/ryuichi-sumida/memuse) | A four-month deployment with 40 users and 1,872 sessions reports large variation in direct memory QA while satisfaction was unchanged; natural memory integration was associated with satisfaction. | Association is not causal; user-data governance and representativeness require deeper audit; less directly about authority than the four additions. |
| [Think Only When Needed](https://arxiv.org/abs/2608.23224) | Tests a prompt-authority compatibility gate for vision-language-action robots across simulation and physical trials. | Robotics-specific intervention and fresh preprint; useful form-versus-authority comparator but narrower than current canon needs. |
| [Checkpoint/fork safety checking for agents](https://arxiv.org/abs/2608.22928) and [repository](https://github.com/eunomia-bpf/agent-check-restore-safety) | Provides a formal checker and Lean mechanization for modeled checkpoint and fork execution edits. | Narrow execution-edit semantics and fresh preprint; formal assurance applies only to its modeled system. |
| [Task-conditioned least-privilege learning](https://arxiv.org/abs/2608.18351) | Reports reduced excess-authority errors for one Qwen-based learned policy and explicitly states that learned restraint does not replace gates or sandboxing. | Single-model and constructed-task evidence; external enforcement remains the stronger authority boundary. |
| [TrustShiftProbe](https://arxiv.org/abs/2608.23763) | Reports staged trust attacks through MCP servers with substantial attack success and only partial defense reduction. | Fresh benchmark with no verified public artifact located; selected staged-server threat model and overlapping injection evidence. |
| [WebMCP-Phalanx](https://arxiv.org/abs/2608.24017) | Combines provenance and capability credentials with a quarantine agent for WebMCP. | Fresh, small evaluation; admits adaptive tool-name bypass and does not establish complete provenance enforcement. |
| Mitchell et al., [“AI Agents Push Humans Out of the Loop”](https://arxiv.org/abs/2608.23642) | Position paper argues that increasing autonomy can displace human oversight and accountability. | Conceptually mission-relevant but supplies no new empirical study; watch rather than treating argument as validation. |

## Watchlist and action disposition

The high-priority NIST/NCCoE, MCP, A2A, W3C accessibility/semantics, Data
Shapes, and Meng et al. entries were reviewed. MCP’s roadmap and authorization
work and W3C’s SPARQL 1.2 RL rename are the only material high-priority project
deltas. Meng et al. remains arXiv v1, and its stated ACM DOI still returned
HTTP 404 on 26 August.

The watchlist adds:

- Yiheng Sun, Huifei Wang, Yancheng Zhu, Zhenyu Li, Zebin Zhao, and Yifan
  Yuan for constraint-preserving agent handoffs;
- Yuxuan Du for aggregation-rule authority;
- Giovanna Broccia, Julian Frattini, Chetan Arora, Maurice H. ter Beek,
  Alessandro Fantechi, Andreas Vogelsang, and Alessio Ferrari for human–AI
  requirements inspection; and
- Saber Zerhoudi, Jelena Mitrovic, and Michael Granitzer for typed agent-memory
  retention.

Every entry remains **research we are learning from**. No message, follow,
subscription, like, repost, public reply, or other account action occurred. No
collaborator, supporter, affiliate, endorsement, permission, correspondence, or
consensus is claimed. Follow candidates remain recommendations to the Director
behind the documented operating, account-state, and named-human gates.

## Limits and continuation

This is a bounded English-language, metadata- and index-dependent delta scan,
not a systematic review, quality meta-analysis, or exhaustive search of
proceedings, citation networks, non-English databases, social output, or private
material. The 26 August arXiv tranche was not yet indexed. Fresh manuscripts,
repositories, Working Drafts, roadmaps, group charters, and Individual
Internet-Drafts can change without notice. Author-reported outcomes were not
independently reproduced during this scan. Proceedings claims whose DOIs
returned HTTP 404 remain author-reported rather than independently verified.

The highest-value literature continuation is to test whether explicit,
source-bound stop status, unresolved prerequisite, responsible authority, and
fallback survive longer, human-authored, multi-system handoffs, while measuring
both artifact preservation and downstream containment.
