---
name: bio-blast
description: "NCBI BLAST sequence similarity search using BioPython. Use when a user wants to run BLAST programmatically with blastn/blastp and retrieve results in JSON format."
user_invocable: true
---

# BLAST Search

NCBI BLAST (Basic Local Alignment Search Tool) を BioPython で実行し、結果を JSON 形式で取得するスキルです。

## Quick Start

### Install

```bash
uv pip install biopython typer
```

### Run with FASTA

```bash
python scripts/run_blast_biopython.py --fasta path/to/query.fasta
```

### Run with raw sequence

```bash
python scripts/run_blast_biopython.py --sequence ATGCGATCG...
```

### Restrict to organism (e.g., human)

```bash
python scripts/run_blast_biopython.py --fasta query.fasta --organism "Homo sapiens"
```

### Protein BLAST

```bash
python scripts/run_blast_biopython.py --program blastp --database swissprot --sequence MTEYKLVVVG...
```

### Save output

```bash
python scripts/run_blast_biopython.py --fasta query.fasta --output blast_results.json
```

## Output Format

Results are returned in JSON format with the following structure:

```json
{
  "query": "No definition line",
  "query_length": 99,
  "database": "core_nt",
  "num_hits": 10,
  "hits": [
    {
      "rank": 1,
      "accession": "NM_007294",
      "title": "Homo sapiens BRCA1 DNA repair associated (BRCA1), mRNA",
      "e_value": 4.35e-43,
      "bit_score": 179.82,
      "percent_identity": 100.0,
      "identities": 99,
      "align_length": 99,
      "gaps": 0,
      "query_start": 1,
      "query_end": 99,
      "subject_start": 1,
      "subject_end": 99
    }
  ]
}
```

## Command-line Options

- `--program`: BLAST program (blastn, blastp, blastx, tblastn, tblastx). Default: blastn
- `--database`: BLAST database (nt, nr, refseq_rna, swissprot, etc.). Default: nt
- `--fasta`: Path to FASTA file (single sequence only)
- `--sequence`: Raw query sequence string
- `--organism`: Restrict search to organism (e.g., "Homo sapiens")
- `--expect`: E-value threshold. Default: 0.001
- `--hitlist-size`: Maximum number of hits. Default: 10
- `--output`: Output path for JSON results

## Best Practices

1. **Save results** - Don't re-run searches unnecessarily
2. **Set E-value threshold** - Default 10 is too permissive; use 0.001-0.01
3. **Use gget for quick searches** - Simpler API for single sequences
4. **Cache parsed data** - Avoid re-parsing large XML files
5. **Handle rate limits** - NCBI limits request frequency

## BLAST vs BLAT

| Aspect | BLAST | BLAT |
|--------|-------|------|
| Purpose | Similarity search | Genome mapping |
| Sensitivity | High | Medium |
| Speed | Medium | Very fast |
| Best for | Homolog search | Position finding |
