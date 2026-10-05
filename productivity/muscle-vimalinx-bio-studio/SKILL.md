---
name: muscle
description: Use when performing multiple sequence alignment of FASTA inputs, generating alignment ensembles, or calculating alignment confidence metrics.
disable-model-invocation: true
user-invocable: true
---

# muscle

## Quick Start
- **Command:** `muscle -align input.fa -output aln.afa`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/muscle`
- **Version:** 5.3
- **Full reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Align FASTA sequences with MUSCLE 5.
- Use `-super5` for larger inputs when plain `-align` becomes too expensive.
- Generate alignment ensembles and confidence summaries, not just one alignment.
- Prefer MUSCLE when ensemble-based confidence analysis is part of the task.

## Common Patterns

```bash
# 1) Standard alignment
muscle -align input.fa -output aln.afa
```

```bash
# 2) Large-input alignment with Super5
muscle -super5 input.fa -output aln.afa
```

```bash
# 3) Generate a stratified ensemble
muscle -align input.fa -stratified -output ensemble.efa
```

```bash
# 4) Extract the highest-confidence replicate
muscle -maxcc ensemble.efa -output maxcc.afa
```

## Recommended Workflow

1. Start with `-align` for ordinary datasets.
2. Switch to `-super5` when sequence count makes ordinary alignment too slow or memory-heavy.
3. If alignment confidence matters, generate an ensemble and summarize it rather than trusting one run.
4. Inspect the final alignment before phylogeny or profile construction.

## Guardrails
- `-super5` is the recommended path for larger inputs.
- Input is FASTA; output is usually aligned FASTA or EFA depending on the mode.
- `-super5` does not directly emit EFA output.
- Ensemble workflows are more informative, but they also produce more files and more interpretation work.
