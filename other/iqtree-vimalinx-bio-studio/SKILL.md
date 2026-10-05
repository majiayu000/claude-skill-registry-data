---
name: iqtree
description: Use when inferring maximum-likelihood phylogenies from aligned sequences, performing automated model selection, or assessing branch support with bootstrap or aLRT methods
disable-model-invocation: true
user-invocable: true
---

# iqtree

## Quick Start
- **Command:** `iqtree -s ALIGNMENT -m MODEL`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/iqtree`
- **Version:** 3.0.1
- **Full options:** see [references/help.md](references/help.md)

## When To Use This Tool

- Infer a maximum-likelihood phylogeny from an existing alignment.
- Run ModelFinder to choose a substitution model.
- Estimate branch support with ultrafast bootstrap or SH-aLRT.
- Use partition-aware analyses when the dataset contains multiple loci or predefined partitions.

## Common Patterns

```bash
# 1) ModelFinder plus tree inference
iqtree -s alignment.fasta -m MFP
```

```bash
# 2) Tree inference with support values
iqtree -s alignment.fasta -m GTR+F+R4 -B 1000 --alrt 1000 -T AUTO
```

```bash
# 3) Partitioned analysis
iqtree -s alignment.fasta -p partitions.nex -m MFP -T AUTO
```

## Recommended Workflow

1. Start from a trustworthy multiple-sequence alignment.
2. Run model selection unless a justified model is already fixed by protocol.
3. Add branch support estimation in the same run or a well-documented follow-up run.
4. Inspect `.iqtree`, `.treefile`, and support values before making biological claims.

## Guardrails
- IQ-TREE does not align sequences; garbage alignments produce garbage trees.
- `-B` ultrafast bootstrap is intended for large replicate counts, commonly `>=1000`.
- Use `-T AUTO` and `--mem` thoughtfully on shared machines.
- Model choice, support values, and partition strategy are part of the inference, not optional cosmetics.
