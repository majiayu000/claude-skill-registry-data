---
name: rnados
description: Use when summarizing an RNA folding landscape by counting how many structures fall into each energy band, rather than enumerating individual folds one by one.
disable-model-invocation: true
user-invocable: true
---

# rnados

## Quick Start

- **Command:** `RNAdos -s SEQUENCE`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNAdos`
- **Full reference:** See `references/help.md` for complete options and details

## When To Use This Tool

- Use `RNAdos` when you want a compact view of the folding landscape as counts per energy band instead of explicit suboptimal structures.
- It is useful for judging how broad or narrow the accessible energy landscape is around the MFE.
- Use `-e` when the default 0 kcal/mol ceiling truncates energy bands you care about.
- Use `-j` when the build supports OpenMP and the calculation is large enough to benefit from more threads.

## Common Patterns

```bash
# Density of states for a single RNA sequence
RNAdos -s GGGAAAUCC

# Count structures up to a higher energy threshold
RNAdos -s GGGAAAUCC -e 5

# Run with multiple threads when available
RNAdos -s GGGAAAUCC -j 4

# Recompute the landscape under a different temperature
RNAdos -s GGGAAAUCC -T 25
```

## Recommended Workflow

1. Prepare your RNA sequence in ACGU format
2. Run `RNAdos -s SEQUENCE` with optional parameters like `-T` for temperature or `--salt` for salt concentration
3. Adjust `--max-energy` threshold if you need to count structures beyond the default 0 kcal/mol
4. Interpret the density of states output to understand the energy distribution of possible structures

## Guardrails

- Input sequence must contain only valid RNA nucleotides (A, C, G, U)
- Default max-energy threshold is 0 kcal/mol; increase with `-e` if higher energy states are relevant
- Temperature defaults to 37°C; specify `-T` if working under different conditions
