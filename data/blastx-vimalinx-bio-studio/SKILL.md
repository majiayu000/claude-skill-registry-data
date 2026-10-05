---
name: blastx
description: Use when comparing translated nucleotide query sequences against protein databases to identify homologous proteins and potential protein-coding regions.
disable-model-invocation: true
user-invocable: true
---

# blastx

## Quick Start
- **Command:** `blastx`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/blastx`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Search nucleotide queries against protein databases by translating the query in six frames.
- Annotate transcripts, contigs, ORF candidates, or metagenomic nucleotide fragments against known proteins.
- Prefer `blastp` if the query is already protein, or `tblastn` if the query is protein and the target is nucleotide.
- Use `-task blastx-fast` when you want speed over maximum sensitivity.

## Common Patterns

```bash
# 1) Standard translated search with tabular output
blastx \
  -query contigs.fa \
  -db prot_db \
  -outfmt "6 qaccver saccver pident length qstart qend sstart send evalue bitscore qcovhsp frames" \
  -evalue 1e-5 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Faster search mode for large screens
blastx \
  -task blastx-fast \
  -query contigs.fa \
  -db prot_db \
  -outfmt 6
```

```bash
# 3) One-off translated search against a protein FASTA subject and a nonstandard code
blastx \
  -query contigs.fa \
  -subject proteins.fa \
  -query_gencode 11 \
  -outfmt 7
```

## Recommended Workflow

1. Confirm the query FASTA is nucleotide and the target is protein, either as a BLAST DB or a one-off subject FASTA.
2. Set `-task` and `-query_gencode` deliberately before comparing output across projects.
3. Emit tabular output with explicit fields for pipelines.
4. Interpret hits using e-value, coverage, frame, and biological plausibility together.

## Guardrails

- `-db` and `-subject` are mutually exclusive.
- Use `-help` rather than `--help`; `--version` also errors in this BLAST+ build.
- Translated searches are expensive and can explode into many HSPs, so set `-outfmt`, `-evalue`, and `-max_target_seqs` explicitly.
- `-remote` changes execution semantics and is incompatible with local threading.
