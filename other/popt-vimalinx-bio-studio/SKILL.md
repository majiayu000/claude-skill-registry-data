---
name: popt
description: Use when filtering `RNAsubopt -s` output to keep p-optimal RNA structures in a ViennaRNA post-processing pipeline.
disable-model-invocation: true
user-invocable: true
---

# popt

## Quick Start

- **Command:** `RNAsubopt -s < seq.fa | popt`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/popt`
- **Observed usage string:** `p-optimal filter to subopt output. usage: RNAsubopt -s < seq | popt`

## When To Use This Tool

- Filter an `RNAsubopt` structure ensemble down to p-optimal structures.
- Keep the workflow inside ViennaRNA-style shell pipelines.
- Post-process suboptimal RNA secondary structures without writing custom selection code.

## Common Patterns

```bash
# 1) Directly filter RNAsubopt output
RNAsubopt -s < sequences.fa | popt
```

```bash
# 2) Keep the raw ensemble and the filtered subset
RNAsubopt -s < sequences.fa | tee all_subopt.txt | popt > p_optimal.txt
```

## Recommended Workflow

1. Generate compatible input with `RNAsubopt -s`.
2. Pipe that output directly into `popt`.
3. Save the filtered subset separately if you will compare it against the full suboptimal ensemble.
4. Continue with downstream ViennaRNA analysis only after confirming the filtered output still matches your expected sequence set.

## Guardrails

- `popt` is a stdin filter; it is not a standalone predictor.
- The live binary does not expose a clean `-h` / `--help` interface in this environment, so the usable contract comes from the embedded usage string and ViennaRNA context.
- The intended input format is specifically `RNAsubopt -s` output, not arbitrary dot-bracket text.
- Current documentation here is grounded in the binary usage string and surrounding ViennaRNA conventions, because the local executable is an ELF binary rather than a short inspectable script.
