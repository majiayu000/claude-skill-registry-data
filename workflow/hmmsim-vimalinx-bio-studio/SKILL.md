---
name: hmmsim
description: Use when you need to characterize score distributions of a profile HMM on random sequences, such as calibration checks, benchmarking, or filter-behavior experiments.
disable-model-invocation: true
user-invocable: true
---

# hmmsim

## Quick Start

- **Command:** `hmmsim [options] <hmmfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmsim`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Measure how a profile HMM scores random sequences.
- Explore score and E-value behavior under different random-sequence lengths and sample counts.
- Benchmark HMM filtering or calibration behavior before deploying a profile in larger search pipelines.
- Generate score-distribution outputs for debugging or method development around HMMER models.

## Common Patterns

```bash
# 1) Collect a basic score distribution for one profile HMM
hmmsim \
  mymodel.hmm
```

```bash
# 2) Increase the number and length of random targets
hmmsim \
  -N 10000 \
  -L 300 \
  mymodel.hmm
```

```bash
# 3) Write verbose scores and an E-value calibration plot payload
hmmsim \
  -v \
  --efile hmmsim.eplot.tsv \
  -o hmmsim.out \
  mymodel.hmm
```

## Recommended Workflow

1. Prepare a valid profile HMM file and decide whether you need a quick default run or a larger calibration experiment with explicit `-N` and `-L`.
2. Choose the scoring/alignment mode (`--vit`, `--fwd`, `--hyb`, `--msv`, `--fs`, `--sw`, `--ls`, `--s`) if you are studying a specific HMMER behavior.
3. Run `hmmsim` and direct outputs to files with `-o`, `--efile`, `--ffile`, or related options when you want reusable diagnostic artifacts.
4. Interpret the result as a random-sequence score-distribution study, not as a biologically realistic sequence-generation workflow.

## Guardrails

- `hmmsim` evaluates an HMM against random sequences; it is not a general simulator for generating biologically realistic sequences from a model.
- Use `-h` for help; `--help` and `--version` are not supported.
- The input must be a valid HMMER profile HMM file.
- Defaults are relatively small (`-N 1000`, `-L 100`), so set them explicitly for serious calibration or benchmarking work.
