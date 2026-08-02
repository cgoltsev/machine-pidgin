# Benchmark 002 preregistration: mathematical notation versus vernacular

**Frozen:** 2026-08-03, before any paid model calls for this study  
**Status:** small paired synthetic experiment; exploratory evidence, not a safety guarantee

Development calls then exposed two contract defects before any held-out calls: an English prompt described both output fields as arrays even though one was Boolean, and a symbolic provenance prompt introduced abbreviations that models copied instead of the canonical source names. Both paired conditions were clarified where relevant, and `lexmax` received a one-sentence operational definition. These development-driven edits are recorded here; no held-out response or score had been observed.

## Question and hypothesis

When facts, objective, constraints, and output are held constant, does a compact typed mathematical representation improve exact on-task performance relative to ordinary vernacular instructions?

The directional hypothesis is that notation will help most on constraint composition, precedence, sets, intervals, and lexicographic decisions. The corpus also contains direct-lookup and direct-classification negative controls, where notation is not expected to help and may make interpretation harder.

## Intervention

- **Vernacular:** ordinary concise English.
- **Formal notation:** the same facts and requested result expressed with typed variables, sets, Boolean formulas, inequalities, functions, and explicit output types.
- The system instruction, requested JSON-only response, model, reasoning effort, seed, and mechanical scorer are identical between conditions.
- No external solver, chain-of-thought instruction, SPEAR system prompt, or model grader is used. This isolates representation format rather than the full SPEAR protocol.

## Corpus and analysis

- Eight development tasks are available for runner validation and debugging. They are not included in the primary result.
- Twenty held-out tasks span constrained selection, allocation, precedence, Boolean gates, provenance, exceptions, units, sets, intervals, schemas, scoring, state transitions, and arithmetic, including two negative controls.
- Four model tiers are evaluated: GPT-4o mini, GPT-5.6 Luna, GPT-5.6 Terra, and GPT-5.6 Sol through OpenRouter.
- The held-out run uses two repetitions per task, model, and condition. A fixed seed is requested; provider determinism is not assumed.
- Primary endpoint: exact equality with preregistered expected JSON ("on task").
- Secondary endpoints: recursive expected-leaf constraint score, valid JSON rate, latency, tokens, and provider-reported cost.
- Primary descriptive estimate: formal on-task rate minus vernacular on-task rate in percentage points, overall and by model.
- Paired discordances are reported: formal repairs and formal regressions on the same model, task, and repetition.
- A two-sided exact McNemar test is reported descriptively over discordant paired observations. Repeated tasks and related model families violate simple independence, so this p-value is not treated as confirmatory.
- Results are also split between notation-friendly tasks and negative controls.

## Integrity and stop rules

- `formal_notation_tasks.json` is SHA-256 hashed into the output record.
- Expected answers are validated before calls with a local deterministic validator.
- Provider errors remain in the raw record and are excluded from rate denominators; the number of errors is reported.
- The runner stops scheduling new calls if provider-reported spend for this study reaches USD 5.00.
- Prompts, raw responses, metadata, scorer, and task-level rows will be published, including null or adverse results.

## Limits stated in advance

This study tests exact synthetic instruction following, not latent-value inference, corrigibility, strategic behavior, open-world agency, or control over a superintelligent system. Any improvement may reflect familiarity with benchmark-like notation or more compact statements, and any regression may reflect autoformalization errors. The investigator designed the intervention, corpus, and scorer; independent replication and human-authored natural tasks are required.
