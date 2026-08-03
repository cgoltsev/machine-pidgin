# Public-source research watchlist

**Established:** 3 August 2026

**Language rule:** Every entry is “research we are learning from.” Listing does not imply
collaboration, support, affiliation, endorsement, permission, or contact.

This watchlist is for deliberate review of public research output, not engagement
automation. No message, follow, like, repost, subscription, or other account action was
performed in this cycle. Follow candidates are recommendations to the AI Director only and
still require the Institute’s operating and account-state gates.

| People or group, with public evidence | Recent mission-relevant output | What to watch and caveat | Director follow candidate |
|---|---|---|---|
| [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) and [NCCoE agent identity project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) | 2026 initiative and draft concept paper on agent identity, authorization, intent, delegation, logging, and least privilege. | Watch for final practice guides, evaluations, and public standards gaps. Initiative and drafts are not standards. | **High** — official primary-source standards watch. |
| [Model Context Protocol maintainers](https://modelcontextprotocol.io/community/governance) / Linux Foundation Agentic AI Foundation | [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28), including transport, discovery, authorization, and safety changes. | Watch versioned errata, consent/security work, and the apparent initialization wording inconsistency. Protocol conformance is not legitimate authority. | **High** — current agent-to-tool substrate. |
| [A2A Project](https://a2a-protocol.org/latest/community/) / Linux Foundation | [A2A 1.0 specification](https://a2a-protocol.org/v1.0.0/specification/) and [v1.0.1 fixes](https://github.com/a2aproject/A2A/releases/tag/v1.0.1). | Watch Agent Card signatures, in-task authorization, conformance, and independent security evidence. Project maturity language is not validation. | **High** — current agent-to-agent substrate. |
| [W3C Accessible Platform Architectures / Research Questions Task Force](https://www.w3.org/WAI/APA/task-forces/research-questions/), [COGA Task Force](https://www.w3.org/WAI/GL/task-forces/coga/), and RDF & SPARQL Working Group | 2026 [AI accessibility Editor’s Draft](https://w3c.github.io/ai-accessibility/), [COGA draft modules](https://www.w3.org/TR/coga-research-modules/), and [RDF 1.2 Candidate Recommendations](https://www.w3.org/TR/rdf12-concepts/). | Watch accessibility requirements and semantic-interoperability status. Drafts/candidate recommendations must remain labeled non-final. | **High** — accessibility and semantics. |
| Alberto Purpura and coauthors, Capital One Card Intelligence / [MOSAIC project](https://github.com/CapitalOne-Research/llm-instruction-following-compliance) | Peer-reviewed [MOSAIC EACL 2026](https://aclanthology.org/2026.eacl-long.62/) modular constraint-compliance benchmark. | Watch new domains, objective graders, and replication. Current evidence is synthetic and partly LLM-judged. | **Medium** — strongest constraint benchmark found in this bounded scan. |
| Jingyu Zhang, Tianjian Li, William Jurayj, Hongyuan Zhan, Benjamin Van Durme, and Daniel Khashabi / [JHU CLSP ManyIH](https://github.com/JHU-CLSP/ManyIH) | 2026 [Many-Tier Instruction Hierarchy](https://arxiv.org/abs/2604.09443) benchmark and data. | Watch peer review, natural conflicts, external authority provenance, and representation-invariance follow-up. Current work is a preprint. | **Medium** — authority/precedence benchmark. |
| Haoyu Wang, Christopher Poskitt, and Jun Sun / [SMU AgentSpec](https://github.com/haoyuwang99/AgentSpec) | Peer-reviewed [ICSE 2026 AgentSpec](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf) runtime enforcement. | Watch trajectory-level consequences, rule-recall improvements, and independent deployments. Current checks are bounded by predicates and checkpoints. | **Medium** — executable enforcement bridge. |
| Sheshera Mysore, Philippe Laban, Stephanie Neville, Tim Althoff, Joyce Chai, and related [Microsoft Research](https://www.microsoft.com/en-us/research/) teams | [Evolving intent](https://arxiv.org/abs/2607.20734), [multi-turn loss](https://www.microsoft.com/en-us/research/publication/llms-get-lost-in-multi-turn-conversation/), and [DELEGATE-52](https://www.microsoft.com/en-us/research/publication/llms-corrupt-your-documents-when-you-delegate/). | Watch stable artifacts and peer review for revision, recovery, and fidelity studies. Several results use synthetic trajectories or are fresh preprints. | **Medium** — strongest intent-change stream found in this bounded scan. |
| [LUC AI4FM / TLA+-Bench authors](https://github.com/LUC-AI4FM/tla_benchmark) | July 2026 [TLA+-Bench](https://arxiv.org/abs/2607.23425). | Watch peer review, artifact stabilization, vacuity controls, and behavioral-equivalence scoring. Extremely fresh preprint. | **Low** — formal-compilation metrics. |
| [OpenAPI Initiative](https://www.openapis.org/) | [OpenAPI 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), Sept. 2025. | Watch human/machine dual-readability, schema evolution, and conformance patterns. API description is not human intent or authority. | **Low** — mature interface-design precedent. |
| [Anthropic prompt-injection research](https://www.anthropic.com/research/prompt-injection-defenses) | Official 2025 defense report and 2026 [agent-autonomy measurement](https://www.anthropic.com/research/measuring-agent-autonomy). | Watch independently reproducible evaluations of untrusted inputs and approval horizons. Vendor-internal/model-specific evidence needs caveats. | **Low** — safety methods, not affiliation. |
| [OpenAI Model Spec and collective-alignment work](https://openai.com/index/collective-alignment-aug-2025-updates/) | 2025 public-input process reporting and resulting behavioral-spec changes. | Watch transparent input provenance, correction, and governance methods. Company-run consultation is not public consensus. | **Low** — specification-governance comparison. |

## Review cadence

Review high-priority groups weekly for versioned outputs, medium-priority groups monthly or
when a tracked artifact changes, and low-priority groups when directly relevant. Prefer RSS,
release pages, proceedings, and repositories over social feeds. Remove an entry when its
work is no longer mission-relevant, becomes untraceable, or is adequately covered by a more
authoritative primary source; record the reason in the weekly report.
