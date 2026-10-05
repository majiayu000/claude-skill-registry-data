---
name: rnaplot
description: Use when visualizing RNA secondary structures from dot-bracket notation or Stockholm alignments, generating structure diagrams, or creating annotated consensus structure plots.
disable-model-invocation: true
user-invocable: true
---

# rnaplot

## Quick Start

- **Command**: `RNAplot`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplot`
- **Full reference**: See [references/help.md](references/help.md) for detailed options

## When To Use This Tool

- Render RNA secondary structures from RNAfold-style sequence/structure input.
- Convert one structure drawing into EPS, SVG, GML, XRNA, or SSV output.
- Plot consensus structures from Stockholm alignments.
- Add covariance or alignment annotation for comparative displays.

## Common Patterns

```bash
# 1) Draw a structure from an RNAfold-style input file
RNAplot -i fold.txt
```

```bash
# 2) Switch the output format to SVG
RNAplot -i fold.txt -f svg
```

```bash
# 3) Plot a consensus structure from an alignment with covariance annotation
RNAplot -a --covar --aln -i family.stk
```

## Recommended Workflow

1. Prepare input in RNAfold output format or Stockholm 1.0 alignment format with secondary structure
2. Run `RNAplot -i <input_file>` for basic structure visualization
3. Specify output format with `-f` option (eps, svg, gml, xrna, ssv) if non-default needed
4. Adjust layout algorithm with `--layout-type` (0-4) or add covariance annotation with `--covar` for consensus structures

## Guardrails

- Input must include secondary structure notation (not just sequences)
- Existing output files of the same name will be overwritten without warning
- Use `-a` flag when providing Stockholm format multiple sequence alignments
