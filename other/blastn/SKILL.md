---
name: blastn
description: Use when performing nucleotide-nucleotide similarity searches to identify homologs, annotate sequences, or compare query sequences against nucleotide databases.
disable-model-invocation: true
user-invocable: true
---

# blastn

## Quick Start
- **Command:** `blastn`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blastn`
- **Version:** 2.17.0+
- **Full reference:** `references/help.md`

## When To Use This Tool

- Search nucleotide queries against nucleotide databases.
- Prefer `blastn` for genome fragments, amplicons, contigs, or transcript sequences.
- Use `-task megablast` for close matches and `-task blastn-short` for short primers or probes.
- Use `tblastn` instead when the query is protein and the target is nucleotide.

## Common Patterns

```bash
# 1) Standard local database search with tabular output
blastn \
  -query query.fa \
  -db nt_db \
  -outfmt "6 qaccver saccver pident length qstart qend sstart send evalue bitscore" \
  -evalue 1e-10 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Primer or short oligo search
blastn \
  -task blastn-short \
  -query primers.fa \
  -db nt_db \
  -word_size 7 \
  -outfmt 6
```

```bash
# 3) Query-vs-subject search without a prebuilt BLAST database
blastn \
  -query query.fa \
  -subject subject.fa \
  -outfmt 7
```

## Recommended Workflow

1. Decide whether you are searching a local BLAST database (`-db`) or a one-off FASTA subject (`-subject`).
2. Set `-task` first, because it changes defaults and search behavior materially.
3. Emit machine-readable output with `-outfmt 6` or `7` unless you explicitly want pairwise text.
4. Interpret hits using e-value, percent identity, query coverage, and biological context together.

## Guardrails
- Use `-help` rather than `--help`; BLAST+ distinguishes those forms.
- `-db` and `-subject` are mutually exclusive.
- The default task is `megablast`, which is fast but less sensitive for divergent homologs.
- Always specify `-outfmt` explicitly for reproducible downstream parsing.
- `-remote` changes execution mode and is usually not what you want for bulk local workflows.
