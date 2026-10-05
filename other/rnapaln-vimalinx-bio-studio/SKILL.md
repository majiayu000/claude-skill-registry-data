---
name: rnapaln
description: Use when performing pairwise structural alignments of RNA sequences that incorporate both sequence and structure information through base pair propensity vectors.
disable-model-invocation: true
user-invocable: true
---

# rnapaln

## Quick Start

- **Command**: `RNApaln`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNApaln`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Align two RNAs using both sequence identity and structural propensity.
- Compare related RNAs when plain sequence alignment misses conserved structure.
- Tune gap penalties and sequence-vs-structure weighting explicitly.
- Use semi-local alignment with free end gaps rather than strict end-to-end matching.

## Common Patterns

```bash
# 1) Align two RNAs from stdin
printf 'AUGCUA\nAUGUUA\n' | RNApaln
```

```bash
# 2) Print the alignment with gaps
printf 'AUGCUA\nAUGUUA\n' | RNApaln -B
```

```bash
# 3) Use free end-gaps and custom gap penalties
printf 'AUGCUA\nAUGUUA\n' | RNApaln --endgaps --gapo=8 --gape=1 --seqw=0.5
```

## Recommended Workflow

1. Prepare input RNA sequences for pairwise comparison
2. Run `RNApaln` with gap penalties (`--gapo`, `--gape`) and sequence weight (`--seqw`) as needed
3. Use `-B` to output the alignment with gaps; add `--endgaps` for semi-local alignment
4. Review alignment output; adjust energy parameters (`-T`, `--salt`, `-P`) for non-standard conditions

## Guardrails

- True local alignment mode is not implemented; only semi-local (free end gaps) is supported
- Performs pairwise alignments only; for multiple alignment consider StraL
- Nucleotide T is automatically converted to U unless `--noconv` is specified
