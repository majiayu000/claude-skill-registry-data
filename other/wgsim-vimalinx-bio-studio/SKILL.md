---
name: wgsim
description: Use when simulating paired-end short reads from a reference FASTA for testing, benchmarking, or pipeline validation
disable-model-invocation: true
user-invocable: true
---

# wgsim

## Quick Start
- Command: `wgsim [options] <in.ref.fa> <out.read1.fq> <out.read2.fq>`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/wgsim`
- Full options: see [references/help.md](references/help.md)

## When To Use This Tool

- Simulate paired-end short reads from a reference FASTA.
- Benchmark aligners, variant callers, or mapping/QC pipelines with controlled synthetic data.
- Stress-test workflows under chosen read lengths, insert sizes, mutation rates, and indel settings.
- Produce reproducible test read sets by fixing the random seed.

## Common Patterns

```bash
# 1) Generate one million paired-end read pairs with a fixed seed
wgsim \
  -N 1000000 \
  -S 42 \
  ref.fa \
  sim_R1.fq \
  sim_R2.fq
```

```bash
# 2) Simulate 150 bp reads with a 350 bp insert size
wgsim \
  -1 150 \
  -2 150 \
  -d 350 \
  -s 30 \
  ref.fa \
  sim_R1.fq \
  sim_R2.fq
```

```bash
# 3) Increase mutation and indel rates for a tougher benchmark
wgsim \
  -r 0.005 \
  -R 0.20 \
  -X 0.50 \
  -e 0.01 \
  ref.fa \
  sim_R1.fq \
  sim_R2.fq
```

## Recommended Workflow

1. Choose the reference FASTA and decide how many read pairs, what read lengths, and what insert-size distribution best match the target assay.
2. Set mutation (`-r`), indel (`-R`, `-X`), and sequencing error (`-e`) parameters explicitly instead of relying on remembered defaults.
3. Fix the random seed with `-S` whenever you need reproducible benchmarks.
4. Verify the emitted FASTQ pair count and use the simulated reads to evaluate alignment, calling, or QC behavior downstream.

## Guardrails

- Input must be a valid FASTA reference file.
- `wgsim` requires two FASTQ output paths; it is a paired-end simulator.
- `-h` enables haplotype mode, it is not a help flag.
- GNU-style `--help` / `--version` print usage with invalid-option noise; use `references/help.md` or a no-argument invocation to inspect usage instead.
- Reads with too many ambiguous bases are discarded according to `-A`, so reference composition can affect realized output yield.
