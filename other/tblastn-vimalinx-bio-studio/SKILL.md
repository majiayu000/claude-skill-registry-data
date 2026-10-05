---
name: tblastn
description: Use when searching protein query sequences against a translated nucleotide database to identify protein-coding regions or homologs in genomic data.
disable-model-invocation: true
user-invocable: true
---

# tblastn

## Quick Start

- **Command:** `tblastn -query <protein.fa> -db <nucl_db> -out <results.txt>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/tblastn`
- **Version:** 2.17.0+
- **Full reference:** See [references/help.md](references/help.md) for complete option documentation

## When To Use This Tool

- Search protein queries against nucleotide databases translated in six frames.
- Find coding regions or protein homologs in genomes, contigs, or transcript assemblies.
- Use this when protein-level sensitivity is useful but the target is still nucleotide.
- Prefer `blastp` when both query and target are already protein.

## Common Patterns

```bash
# 1) Search proteins against a nucleotide database
tblastn \
  -query proteins.fa \
  -db transcripts_db \
  -outfmt "6 qaccver saccver pident length evalue bitscore" \
  -evalue 1e-5 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Use an alternative genetic code
tblastn \
  -query proteins.fa \
  -db bacterial_db \
  -db_gencode 11 \
  -outfmt 6
```

```bash
# 3) Allow gapped translated hits across longer introns
tblastn \
  -query proteins.fa \
  -db genome_db \
  -max_intron_length 10000 \
  -outfmt 7
```

## Recommended Workflow

1. Build or select a nucleotide BLAST database first.
2. Choose the correct translation table with `-db_gencode` if the organism is non-standard.
3. Emit tabular output unless manual pairwise inspection is explicitly needed.
4. Confirm top hits make biological sense before inferring annotation from translated matches.

## Guardrails
- The database or subject must be nucleotide, not protein.
- `-db_gencode` affects translation, so set it explicitly for mitochondrial or non-standard codes.
- `-max_intron_length` matters when searching genomic targets with interrupted coding sequence.
- For anything larger than a toy example, pre-format the target with `makeblastdb` instead of using `-subject`.
