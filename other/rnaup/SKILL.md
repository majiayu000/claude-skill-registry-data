---
name: rnaup
description: Use when calculating thermodynamics of RNA-RNA interactions, including accessibility and binding energy predictions for RNA duplex formation.
disable-model-invocation: true
user-invocable: true
---

# rnaup

## Quick Start

- **Command**: `RNAup [OPTIONS]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAup`
- **Reference**: See `references/help.md` for full option details

## When To Use This Tool

- Use `RNAup` when you need RNA-RNA interaction predictions that include **site accessibility**, not just duplex energy.
- It is appropriate for interaction screens where opening energy of the binding site matters, such as small RNA target accessibility analyses.
- Use `-w` to cap the maximum interaction length when looking for short local interactions.
- Use `-b` when you want unpaired-region probabilities reported for both molecules instead of the default target-focused view.

## Common Patterns

```bash
# Basic accessibility-aware interaction calculation
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAup

# Increase the maximal interaction length
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAup -w 40

# Report unpaired-region probabilities for both RNAs
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAup -b

# Change the unstructured output region length
printf 'GGGAAAUCC\nGGAUUUCCC\n' | RNAup -u 8
```

## Recommended Workflow

1. Prepare input sequences in FASTA or plain text format (T automatically converted to U unless `--noconv` is set)
2. Run `RNAup` with appropriate options (e.g., `-w` for max interaction length, `-b` for both RNAs)
3. Review output for binding energies and unpaired probabilities
4. Adjust parameters like `-T` for temperature or `--salt` for salt concentration if needed

## Guardrails

- Default interaction window is 25 nucleotides; increase with `-w` for longer interactions
- Use `-C` for structure constraints only if you have reliable constraint data
- Verify energy parameters are appropriate for your organism or use `-P` to provide custom parameters
