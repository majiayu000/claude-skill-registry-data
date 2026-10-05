---
name: efetch
description: Use when you need to fetch records or data from NCBI Entrez databases (PubMed, nucleotide, protein, gene, SRA, etc.) by ID or accession
disable-model-invocation: true
user-invocable: true
---

# efetch

## Quick Start
- **Command:** `efetch`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/efetch`
- **Full reference:** [references/help.md](references/help.md)

## When To Use This Tool

- Retrieve full records or sequence data after `esearch` or `epost`.
- Fetch records by ID or accession from PubMed, Nucleotide, Protein, Gene, SRA, Assembly, and related databases.
- Export in FASTA, abstract, docsum, XML, JSON, or native record formats.
- Pull sequence subranges when you only need a locus, not the entire accession.

## Common Patterns

```bash
# 1) Fetch PubMed abstracts from a search result
esearch -db pubmed -query 'ebola virus[Title/Abstract]' | efetch -format abstract
```

```bash
# 2) Fetch a nucleotide record in FASTA
efetch -db nucleotide -id NM_000546.6 -format fasta
```

```bash
# 3) Fetch only a sequence subrange
efetch \
  -db nucleotide \
  -id NC_000001.11 \
  -format fasta \
  -seq_start 100000 \
  -seq_stop 101000
```

```bash
# 4) Fetch summaries in JSON-compatible mode
efetch -db assembly -id GCF_000001405.40 -format docsum -mode json
```

## Recommended Workflow

1. Get stable IDs first with `esearch` or `epost`.
2. Choose `-format` deliberately, because downstream parsing depends on it.
3. Save raw outputs for reproducibility when the fetched record is part of an analysis result.
4. Pipe XML-style outputs into `xtract` only after verifying the record shape.

## Guardrails
- Always specify `-db` and usually specify `-format`; implicit defaults are easy to misread.
- Large fetches should be chunked with `-start` and `-stop`, or handled through batched EDirect pipelines.
- `-seq_start`, `-seq_stop`, and strand options only apply to sequence-style retrieval.
- Invalid or mismatched IDs often yield empty output, so validate the upstream search first.
