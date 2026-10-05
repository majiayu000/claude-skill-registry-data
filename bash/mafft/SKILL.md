---
name: mafft
description: Use when performing multiple sequence alignment on nucleotide or protein sequences, such as preparing alignments for phylogenetic analysis or comparative genomics.
disable-model-invocation: true
user-invocable: true
---

# mafft

## Quick Start
- **Command:** `mafft [options] input.fasta > output.fasta`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/mafft`
- **Version:** 7.526
- **Full reference:** See `references/help.md` for complete options and documentation

## When To Use This Tool

- Build a multiple-sequence alignment for nucleotide or protein FASTA input.
- Use it before phylogenetic inference, motif comparison, or profile building.
- Start with `--auto` when you are unsure which alignment strategy fits the dataset.
- Switch to high-accuracy iterative modes for smaller, harder alignments.

## Common Patterns

```bash
# 1) Let MAFFT choose the strategy
mafft --auto input.fasta > aligned.fasta
```

```bash
# 2) High-accuracy local-pair alignment
mafft --maxiterate 1000 --localpair input.fasta > aligned.fasta
```

```bash
# 3) Use all available threads
mafft --auto --thread -1 input.fasta > aligned.fasta
```

```bash
# 4) Output CLUSTAL format
mafft --auto --clustalout input.fasta > aligned.aln
```

## Recommended Workflow

1. Check that the input sequences are homologous enough to align meaningfully.
2. Start with `--auto` unless you already know the dataset requires a specific mode.
3. Move to `--localpair` or related high-accuracy modes only for smaller, biologically difficult alignments.
4. Inspect the alignment before sending it to `iqtree`, `hmmbuild`, or downstream comparative analyses.

## Guardrails
- High-accuracy iterative modes are not the default answer for large datasets.
- The MAFFT help text explicitly suggests the expensive iterative modes mainly for smaller inputs.
- Changing `--op` and `--ep` without a biological reason can degrade alignments quickly.
- MAFFT writes alignment to stdout by default, so remember shell redirection.
