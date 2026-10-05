---
name: rnafold
description: Use when predicting RNA secondary structures, calculating minimum free energy (MFE) folds, or computing partition functions and base pairing probabilities for RNA sequences.
disable-model-invocation: true
user-invocable: true
---

# rnafold

## Quick Start
- **Command:** `RNAfold [OPTIONS] [<input.fa>]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNAfold`
- **Reference:** See `references/help.md` for complete options and details

## When To Use This Tool

- Predict RNA secondary structure from sequence.
- Compute minimum free energy structure and, optionally, partition-function summaries.
- Generate base-pair probability dot plots when structural uncertainty matters.
- Apply simple constraints or probing-guided folding for focused analyses.

## Common Patterns

```bash
# 1) Fold a FASTA file and report MFE structures
RNAfold sequences.fa
```

```bash
# 2) Compute partition function and pairing probabilities
RNAfold -p sequences.fa
```

```bash
# 3) Suppress PostScript outputs in batch workflows
RNAfold --noPS sequences.fa
```

```bash
# 4) Constrained folding
RNAfold -C --enforceConstraint constrained.fa
```

## Recommended Workflow

1. Provide RNA sequences in one-sequence-per-line or FASTA format.
2. Start with the default MFE run, then add `-p` if ensemble information is needed.
3. Capture stdout together with any generated plot files so sequence/structure pairs stay linked.
4. Use temperature or probing options only when the experimental context justifies them.

## Guardrails

- Existing `rna.ps` and `dot.ps`-style outputs are overwritten if you reuse filenames.
- Once FASTA input is used, subsequent sequences must also be FASTA-formatted.
- `-p` changes the calculation and emits additional ensemble statistics and plot files.
- Use `--noPS` or `--noDP` in batch jobs that do not need PostScript artifacts.
