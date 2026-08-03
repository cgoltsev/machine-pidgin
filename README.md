# Machine Pidgin

**How do you speak constructively with an intelligence 100x more capable than you - without losing your agenda? Imagine a three-year-old trying to be understood by an adult.**

Machine Pidgin is an open research program for preserving human intent, constraints, and authority across human-AI intelligence gaps. This repository is deliberately narrow: it contains foundational papers, the SPEAR protocol, reproducible experiments, raw results, governance foundations, and research code. The production website, forum service, infrastructure, organizational records, and private operations live elsewhere.

## First held-out result

In Benchmark 001, 16 held-out synthetic tasks were run in ordinary prose and SPEAR/0.2 across four model tiers. Exact on-task adherence rose from **46/64 (71.9%)** to **57/64 (89.1%)**, an absolute lift of **17.2 percentage points**. The held-out run cost $0.0935 as reported by the provider.

This is a small synthetic pilot, not evidence that SPEAR solves alignment or recovers unexpressed human values. Exact JSON scoring is intentionally strict, and the development audit includes invalidated runs.

| Model | Prose | SPEAR/0.2 | Lift |
|---|---:|---:|---:|
| GPT-4o mini | 31.3% | 68.8% | +37.5 points |
| GPT-5.6 Luna | 87.5% | 93.8% | +6.3 points |
| GPT-5.6 Terra | 81.3% | 93.8% | +12.5 points |
| GPT-5.6 Sol | 87.5% | 100.0% | +12.5 points |

Read [Benchmark 001](experiments/BENCHMARK_001.md), the [empirical note](papers/SPEAR_Empirical_Note_001.pdf), or inspect the [raw held-out record](experiments/results/20260802T184929Z-held_out-spear-0.2.json).

Citation metadata for versioned releases is available in
[`CITATION.cff`](CITATION.cff). Published releases are intended for archival in Zenodo so
that protocol, code, data, and negative results remain citable independently of GitHub.

## Second held-out result: notation alone

Benchmark 002 isolated strict mathematical notation from the rest of SPEAR. The preregistered 20-task aggregate was 83.8% exactly on task in vernacular and 86.3% with notation, an apparent +2.5-point effect. A post-run prompt-equivalence audit found one formal prompt that supplied the exact answer label omitted from its vernacular pair. That task accounts for more than the apparent gain.

Across the remaining 19 equivalent tasks, vernacular scored **134/152 (88.2%)** and notation scored **130/152 (85.5%)**: **-2.6 percentage points**. The defensible conclusion is that notation alone did not establish an improvement. The raw and audited estimates are both retained.

| Model | Audited vernacular | Audited formal | Lift |
|---|---:|---:|---:|
| GPT-4o mini | 63.2% | 50.0% | -13.2 points |
| GPT-5.6 Luna | 94.7% | 94.7% | 0.0 points |
| GPT-5.6 Terra | 94.7% | 100.0% | +5.3 points |
| GPT-5.6 Sol | 100.0% | 97.4% | -2.6 points |

Read [Benchmark 002](experiments/BENCHMARK_002.md), inspect the [audit record](experiments/results/SPEAR_Benchmark_002_Audit.json), or download the [tidy rows](experiments/results/SPEAR_Benchmark_002_Rows.csv). This result motivates a factorial follow-up separating dual-register explanation, parser, verifier, and solver support. The first prospective design is published as a [Benchmark 003 preregistration draft](experiments/BENCHMARK_003_PREREGISTRATION_DRAFT.md); it is not yet registered and cannot trigger paid calls without the listed human gates.

## Repository map

- [`papers/`](papers/) - founding theoretical preprint and empirical research notes
- [`protocol/`](protocol/) - SPEAR/0.2 quick reference and portable LLM interpretation prompt
- [`experiments/`](experiments/) - paired task corpus, evaluation runner, audit trail, raw responses, and tidy outcomes
- [`animation/`](animation/) - Manim source and rendered two-minute conceptual primer
- [`CONSTITUTION.md`](CONSTITUTION.md) and [`GOVERNANCE.md`](GOVERNANCE.md) - public-interest and human-override foundations

## Reproduce the benchmarks

The runner uses only the Python standard library and an OpenRouter key supplied through the environment.

```bash
export OPENROUTER_API_KEY='your-key'
python3 experiments/run_openrouter_eval.py \
  --split held_out \
  --spear-version 0.2 \
  --repetitions 1

python3 experiments/run_formal_notation_eval.py \
  --split held_out \
  --repetitions 2
```

Do not rerun the held-out set as if it remains unseen after reading its results. New confirmatory work should preregister a fresh task set.

## Contribute

We want replications, counterexamples, alternative schemas, natural tasks, human authoring-time studies, cross-vendor evaluations, long-horizon tool-use tests, and arguments that could falsify the program. See [CONTRIBUTING.md](CONTRIBUTING.md).

Project website: [machinepidgin.org](https://machinepidgin.org)  
Public forum: [machinepidgin.org/forum](https://machinepidgin.org/forum)
