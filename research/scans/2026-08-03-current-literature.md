# Current-literature scan — 3 August 2026

**Window:** 3 August 2025 through 3 August 2026, inclusive  
**Run type:** First Researcher cycle; “new” below means published or materially updated
inside this window and new to the Institute’s documented canon. It does not claim a delta
from an undocumented earlier Researcher scan.

This is a bounded, primary-source scan rather than a systematic review. Each finding keeps
source claims separate from Researcher interpretation. No row establishes an Institute
endorsement, affiliation, partnership, policy, or adopted position.

## Search audit trail

Primary sources searched were official/versioned standards and specification registries
(ISO, W3C, RFC Editor, NIST/NCCoE, JSON Schema, OpenAPI, MCP, A2A); peer-reviewed
proceedings and author manuscripts (ACL Anthology, EACL, ICSE, NeurIPS, CHI, ICLR);
author/project code and datasets; and official research-lab publication indexes.

Query families actually used included:

- `ISO 29148`, `ISO 9241-210`, `WCAG 2.2`, `NIST AI RMF`, `RFC 2119 8174`;
- `JSON Schema 2020-12`, `SHACL`, `Common Logic`, `OpenAPI 3.2`, `OAuth rich authorization`;
- `EARS requirements syntax`, `Alloy specification`, `TLA+`, `CIRL`, `inverse reward design`;
- `human AI interaction guidelines`, `overreliance explanations`, `IFEval`, `DSPy`, `LMQL`;
- `MCP latest 2026 changelog`, `A2A 1.0 releases`, `MOSAIC EACL 2026`;
- `Many-Tier Instruction Hierarchy`, `AgentSpec runtime enforcement ICSE`,
  `Open Agent Specification Oracle`;
- `NIST AI Agent Standards Initiative`, `agent identity authorization`,
  `automated benchmark evaluations`;
- `W3C accessibility machine learning generative AI`, `cognitive accessibility`;
- `evolving user intent`, `multi-turn conversation`, `delegation document fidelity`, and
  `TLA+-Bench`.

Inclusion required a primary source with verifiable provenance/date/status, direct relevance
to intent, constraints, authority, interoperability, evaluation, safety/control, or
accessibility, and a material limitation that could be stated. Secondary summaries, social
claims where a paper existed, adoption marketing, citation-count padding, near duplicates,
unverifiable sources, and broad AI work without a direct specification implication were
excluded. Preprints and drafts were admitted only when unusually direct and are labeled.

## Included current findings

| Source and status | Source fact | Researcher inference for SPEAR | Uncertainty and limitation | Institute position / Researcher disposition |
|---|---|---|---|---|
| Purpura et al., [MOSAIC](https://aclanthology.org/2026.eacl-long.62/) ([code/data](https://github.com/CapitalOne-Research/llm-instruction-following-compliance)), peer-reviewed EACL 2026 | Uses 4,000 synthetic prompts with 1–20 constraints from 21 types; reports interactions among type, count, and order plus model-specific primacy/recency. Some semantic constraints use an LLM judge checked against a 250-response human sample. | Benchmark 003 should randomize condition order and score modular constraints separately from task success. | Synthetic writing domains, limited models, and judge-dependent qualitative constraints; generalization to science, code, or natural user instructions is untested. | No Institute position adopted. Researcher assessment: strongest peer-reviewed constraint-compliance method found in this bounded scan. |
| Zhang et al., [Many-Tier Instruction Hierarchy](https://arxiv.org/abs/2604.09443) ([code](https://github.com/JHU-CLSP/ManyIH)), preprint v3 Apr. 2026 | Tests 853 coding/instruction tasks with up to 12 privilege tiers and reports falling performance as tiers increase plus sensitivity to equivalent hierarchy representations. | Nearly direct evidence for testing SPEAR AUTHORITY/PRECEDENCE and representation invariance separately from functional correctness. | Unreviewed; privileges are assigned rather than legitimately established; composed English conflicts appear within one message. | No Institute position adopted. Researcher disposition: provisional high-priority benchmark input. |
| Wang, Poskitt, and Sun, [AgentSpec](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf) ([program](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/29/AgentSpec-Customizable-Runtime-Enforcement-for-Safe-and-Reliable-LLM-Agents), [code](https://github.com/haoyuwang99/AgentSpec)), peer-reviewed ICSE 2026 | Defines rules as trigger, predicates, and enforcement actions such as inspect, self-examine, invoke, or stop; evaluated across code, embodied, and vehicle scenarios. Generated rules had strong precision but missed material cases. | A bounded SPEAR subset could compile to auditable runtime checks and human approval stops. | Discrete checkpoints and hand-authored predicates define the safety envelope; limited trajectory analysis and domain simulations do not establish deployment safety. | No Institute position adopted. Researcher disposition: useful enforcement comparison, not proof of safety. |
| Oracle, [Open Agent Specification](https://arxiv.org/abs/2510.04173) ([spec/code](https://github.com/oracle/agent-spec)), project report Oct. 2025 with 2026 releases | Defines JSON/YAML representations for agents, flows, resources, and multi-agent compositions with framework adapters. | Possible interchange target for carrying SPEAR metadata. | Oracle-led project/technical report rather than consensus standard or independent interoperability evidence; no legitimate-authority semantics. | No Institute position adopted. Researcher disposition: adjacent only; kept distinct from the ICSE AgentSpec system. |
| [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) and [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog), official versioned specification | Makes requests stateless and self-contained, adds per-request version/capability information and discovery, and moves Tasks to an extension; retains explicit consent/control principles and untrusted tool annotations. | SPEAR should layer semantic intent, provenance, and authority atop MCP rather than duplicate transport/discovery. | MCP cannot establish legitimate authority or enforce every safety principle. Its overview still refers to extension negotiation “during initialization” although the release removes initialization; upstream clarification is warranted. | No Institute position adopted. Researcher disposition: track as current transport standard; no claim that MCP solves intent preservation. |
| [A2A Protocol 1.0](https://a2a-protocol.org/v1.0.0/specification/) and [v1.0.1 release](https://github.com/a2aproject/A2A/releases/tag/v1.0.1), official project spec, v1.0.0 Mar. and v1.0.1 fixes May 2026 | Defines Agent Cards, discovery, messages, tasks, artifacts, multiple bindings, authentication, and in-task authorization. | Possible carrier for SPEAR task contracts and provenance between agents. | Project maturity language is not independent adoption/security evidence; identity and capabilities do not establish legitimate authority or goal correctness. | No Institute position adopted. Researcher disposition: track for interoperability; no safety or governance endorsement. |
| [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), official project specification Sept. 2025 | Defines a language-neutral description for HTTP interfaces intended for human and machine use, with explicit version and schema behavior. | A mature comparison for dual-readable, versioned SPEAR interfaces. | Describes API surfaces, not human goals, legitimate authority, or semantic preservation. | No Institute position adopted. Researcher disposition: retain as a stable interface-design precedent. |
| [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative), official initiative launched Feb. and updated Apr. 2026; related [identity/authorization concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf) | Organizes work around industry standards, open protocols, and research on agent identity, authentication, and security; the concept paper asks how agents prove authority, convey intent, delegate “on behalf of,” log intent, and apply least privilege. | Map SPEAR authority fields against these open questions and existing OAuth mechanisms before inventing identity infrastructure. | Initiative and draft concept paper, not a final standard; proposed work and future deliverables remain uncertain. | No Institute position adopted. Researcher disposition: convergence signal only, not an institutional or policy position. |
| [NIST AI 800-2 initial public draft](https://doi.org/10.6028/NIST.AI.800-2.ipd), Jan. 2026 | Proposes staged practices for targeting, implementing/running, and analyzing/reporting automated model benchmarks. | Useful checklist for Benchmark 003 freezing, execution, and reporting gates. | Initial public draft, explicitly preliminary; not a final guideline. | No Institute position adopted. Researcher disposition: method input only; human review controls adoption. |
| W3C, [Accessibility of Machine Learning and Generative AI](https://w3c.github.io/ai-accessibility/), Editor’s Draft Mar. 2026; [COGA Research Modules](https://www.w3.org/TR/coga-research-modules/) and [conversational-interface module](https://www.w3.org/TR/coga-voice/), Group Note Drafts Feb. 2026 | Collects emerging benefits, risks, and user needs including memory load, sufficient time, progress visibility, undo, human help, and short steps. | SPEAR authoring needs progressive disclosure, alternatives, correction/undo, and low-memory interaction; compactness alone is not accessibility. | Early, incomplete work in progress with no conformance requirements and no W3C endorsement. | No Institute position adopted. Researcher disposition: accessibility questions are required research constraints; these drafts are informative, not normative. |
| Mysore et al., [“LLMs Get Lost in Evolving User Intent”](https://arxiv.org/abs/2607.20734) ([code](https://github.com/microsoft/evolving-intent)), preprint July 2026 | Converts established benchmarks into multi-turn argument-reveal, revision, and function-switch trajectories while retaining original evaluators. | Closest current template for testing SPEAR revision, cancellation, precedence, and current-state recovery. | Very recent preprint; synthetic/model-naturalized trajectories, no peer review or stable release; full reproduction may require paid APIs. | No Institute position adopted. Researcher disposition: defer to an offline fixture design; no paid reproduction authorized. |
| Laban et al., [“LLMs Get Lost in Multi-Turn Conversation”](https://www.microsoft.com/en-us/research/publication/llms-get-lost-in-multi-turn-conversation/) ([code](https://github.com/microsoft/lost_in_conversation)), ICLR 2026 | Across 200,000+ simulated conversations, the authors report a large mean drop from single-turn to multi-turn task performance and weak recovery from premature assumptions. | Compare a complete contract against fragmented disclosure while scoring repair and current-state summaries. | Simulated English conversations, selected tasks and models; not natural user behavior or high-risk validation. | No Institute position adopted. Researcher disposition: empirical design input only. |
| Microsoft Research, [DELEGATE-52](https://www.microsoft.com/en-us/research/publication/llms-corrupt-your-documents-when-you-delegate/) ([data](https://huggingface.co/datasets/microsoft/delegate52)), preprint Apr. 2026 | Uses transform-and-invert stress tests across 52 domains; authors report semantic-fidelity loss in long workflows and clarify this is not a task-completion or user-outcome measure. | Supports PRESERVE fields, diffs, checkpoints, reversibility, and long-horizon regression tests. | Adversarial synthetic harness, preprint, and a fidelity metric that should not be generalized to overall usefulness. | No Institute position adopted. Researcher disposition: research-learning source only; no generalized “corruption” claim. |
| [TLA+-Bench](https://arxiv.org/abs/2607.23425) ([code](https://github.com/LUC-AI4FM/tla_benchmark)), preprint July 2026 | Builds model-checked and parse-only TLA+ corpora and reports large score sensitivity to vacuity, property quality, and interface naming. | Any SPEAR-to-formal compiler evaluation should separate parsing, model checking, vacuity, interface fidelity, and behavioral equivalence. | Extremely recent and unreviewed; bounded checking is not semantic equivalence and some metadata appears preliminary. | No Institute position adopted. Researcher disposition: deferred; informs metrics, not current SPEAR claims. |

“MOSAIC” above refers only to Purpura et al.’s EACL 2026 instruction-compliance
benchmark, not other 2026 systems with the same name.

## Exclusions and negative search results

- Three window-dated sources were screened into the canon’s **provisional** section rather
  than promoted to key findings: [Programmable Prompting Structure](https://arxiv.org/abs/2603.25379)
  because condition content, temperature, judge family, and analysis-unit choices confound
  a structure-only interpretation; [Intent-Governed Tool Authorization](https://arxiv.org/abs/2606.22916)
  because it is a project-linked preprint without independent evaluation; and W3C
  [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) / [Semantics](https://www.w3.org/TR/rdf12-semantics/)
  because they remain Candidate Recommendations and are a substrate rather than intent or
  authority evidence.
- No source was included merely because it reported a higher model ranking or used the word
  “intent.”
- Broad safety, manipulation, or preference papers without a reusable task-specification
  method were deferred.
- W3C’s Natural Language Interface Accessibility User Requirements remains useful canon,
  but its latest group draft predates this window; it is not a 2026 finding.
- Several 2026 AgentSpec/AgentSPEX preprints were deferred because the peer-reviewed ICSE
  AgentSpec and the separately named Oracle interchange project covered the highest-value
  enforcement and representation angles this cycle.
- No independent evidence was found that protocol conformance alone establishes legitimate
  human authority, preserved intent, or safe tool action. This negative result is central:
  interoperability and authorization metadata remain necessary but insufficient.

## Scan limitations

The scan was English-language and index-dependent. It did not perform a formal database
export, citation-network snowball, quality meta-analysis, or exhaustive multilingual search.
Some 2026 sources are preprints, working drafts, or project specifications. Dates and source
status were checked against primary pages on 3 August 2026; future revisions may change them.
