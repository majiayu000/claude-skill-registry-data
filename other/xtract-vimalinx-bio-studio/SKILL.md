---
name: xtract
description: Use when parsing, extracting, or converting XML data from NCBI Entrez or other bioinformatics sources into tab-delimited tables. Use for selecting specific elements, filtering records, and restructuring hierarchical XML into flat formats for downstream analysis.
disable-model-invocation: true
user-invocable: true
---

# xtract

## Quick Start
- **Command:** `xtract`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xtract`
- **Full reference:** See `references/help.md` for complete argument list and examples

## When To Use This Tool

- Convert Entrez XML into tab-delimited tables.
- Extract selected elements or nested values from `efetch`, `esummary`, or `elink` XML output.
- Filter records conditionally while flattening XML into rows.
- Use this after you already know the XML structure you are parsing.

## Common Patterns

```bash
# 1) Turn document summaries into a simple two-column table
esearch -db assembly -query 'GCF_000001405.40[accn]' | \
  efetch -format docsum | \
  xtract -pattern DocumentSummary -element Id AssemblyAccession
```

```bash
# 2) Extract PubMed summary IDs and titles
esearch -db pubmed -query 'ebola virus[Title/Abstract]' | \
  efetch -format docsum | \
  xtract -pattern DocumentSummary -element Id Title
```

```bash
# 3) Conditional extraction from linked records
elink -db pubmed -id 20210808 -cmd score | \
  xtract -pattern LinkSet -max Link/Score
```

## Recommended Workflow

1. Feed XML from stdin or `-input`; `xtract` is not useful without structured input.
2. Define rows first with `-pattern`.
3. Add `-element` fields incrementally before reaching for `-group`, `-block`, or `-if`.
4. Save the exact extraction command alongside the analysis so XML-to-table logic remains reproducible.

## Guardrails
- `xtract` requires XML input from stdin or `-input`; otherwise it errors immediately.
- `-pattern` defines row boundaries; choosing the wrong pattern is the fastest way to get nonsense tables.
- Start with a minimal extraction and expand, rather than writing a huge one-liner blind.
- Use `-strict` when embedded HTML or MathML is polluting the text you want to extract.
