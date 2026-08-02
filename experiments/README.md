# SPEAR paired benchmark

This benchmark asks whether a compact interpretation contract and SPEAR field structure improve exact task adherence relative to ordinary prose containing the same task facts.

## Design

- Four OpenRouter-hosted model tiers are tested: GPT-4o mini, GPT-5.6 Luna, Terra, and Sol.
- Each model receives every task in both `plain` and `spear` conditions.
- Outputs are scored mechanically against preregistered JSON. No model grades another model.
- Development tasks may be used to revise the protocol. Held-out tasks are not inspected until the protocol version is fixed.
- Exact equality is the strict “on task” outcome. Recursive expected-field agreement is reported as a softer constraint score.
- The fixed seed is requested and raw outputs, token usage, provider attribution, errors, task-file hash, and reported cost are retained.

This is a synthetic instruction-following pilot, not evidence that SPEAR solves alignment or preserves human intent in open-world settings. Its purpose is to expose failure modes and make the next experiment more rigorous.

## Run

```bash
export OPENROUTER_API_KEY='...'
python3 experiments/run_openrouter_eval.py --split development --spear-version 0.1 --repetitions 2
python3 experiments/run_openrouter_eval.py --split held_out --spear-version 0.2 --repetitions 2
```

The secret is read from the environment and is never written into results.
