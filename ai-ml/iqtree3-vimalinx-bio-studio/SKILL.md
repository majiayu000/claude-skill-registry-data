---
name: iqtree3
description: Use when inferring maximum-likelihood phylogenetic trees, selecting substitution models, running bootstrap support analyses, or performing partitioned phylogenetic analyses on sequence alignments.
disable-model-invocation: true
user-invocable: true
---

# iqtree3

## Quick Start
- Command: `iqtree3 -s ALIGNMENT [-m MODEL] [-B 1000]`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/iqtree3`
- Full reference: `references/help.md`

## When To Use This Tool

- Infer maximum-likelihood phylogenetic trees from aligned DNA, protein, codon, morphology, or partitioned data.
- Select substitution models with ModelFinder before or during tree search.
- Add branch support with ultrafast bootstrap, non-parametric bootstrap, SH-aLRT, or related support tests.
- Run partitioned analyses, topology tests, likelihood mapping, or concordance-factor workflows in one phylogenetic engine.

## Common Patterns

```bash
# 1) Model selection plus ML tree with ultrafast bootstrap support
iqtree3 \
  -s alignment.fasta \
  -m MFP \
  -B 1000 \
  --alrt 1000 \
  -T AUTO
```

```bash
# 2) Partitioned phylogeny with a partition file
iqtree3 \
  -s concatenated.phy \
  -p partitions.nex \
  -m MFP \
  -B 1000 \
  -T AUTO
```

```bash
# 3) Likelihood mapping to inspect phylogenetic signal
iqtree3 \
  -s alignment.fasta \
  --lmap 10000
```

## Recommended Workflow

1. Prepare input alignment in a supported format (PHYLIP, FASTA, NEXUS, CLUSTAL, or MSF)
2. Run ModelFinder to identify best-fit model: `iqtree3 -s alignment.fasta -m MF`
3. Infer tree with branch support: `iqtree3 -s alignment.fasta -m MODEL -B 1000 --alrt 1000`
4. Examine output files (`.treefile`, `.iqtree`, `.log`) and checkpoint options (`--redo`, `--undo`) if re-running

## Guardrails

- Always specify an alignment via `-s`; IQ-TREE requires input data to run
- Use `-T AUTO` or explicit thread count to avoid oversubscribing CPUs
- `-B` ultrafast bootstrap is intended for large replicate counts; `1000` is the usual minimum practical setting
- Check the `.iqtree` report and `.log` for convergence, composition, or numerical warnings before trusting the tree
