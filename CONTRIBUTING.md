# Contributing to Machine Pidgin Research

The public repository accepts foundational and reproducible research materials:

- protocol RFCs with positive, negative, and boundary examples;
- preregistered experiments, task corpora, scoring code, and non-sensitive raw results;
- replications, null results, corrections, and retractions;
- theoretical notes, educational explanations, and research-relevant reference implementations;
- governance work directly related to preserving human authority across intelligence gaps.

It does not accept production website code, deployment configuration, service credentials, private community data, payment operations, entity records, or general organizational administration.

## A useful research contribution states

1. the claim or question;
2. baseline and intervention;
3. sample, task split, metrics, and scoring rules;
4. what would falsify the claim;
5. assumptions, conflicts, limitations, and failure modes;
6. reproduction steps and license;
7. how negative findings and corrections will be preserved.

Protocol changes should name their interoperability consequence and include a near miss. Empirical work should separate development from held-out evaluation. Do not tune against a set and continue calling it held out.

## Before submitting

```bash
python3 -m json.tool experiments/tasks.json >/dev/null
python3 -m py_compile experiments/run_openrouter_eval.py
```

Do not submit secrets, personal data, confidential model traces, or material you cannot redistribute. Disclose material AI assistance; named humans remain responsible for claims and releases.

