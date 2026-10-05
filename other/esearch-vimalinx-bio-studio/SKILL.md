---
name: esearch
description: Use when searching NCBI Entrez databases (pubmed, gene, protein, nuccore, snp, geoprofiles) with query strings and field qualifiers to retrieve record UIDs for downstream processing.
disable-model-invocation: true
user-invocable: true
---

# esearch

## Quick Start
- **Command:** `esearch -db <database> -query "<query string>"`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esearch`
- **Full reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Start an Entrez Direct pipeline by searching for record IDs.
- Search PubMed, Gene, Protein, Nuccore, SRA, and related NCBI databases with field-qualified queries.
- Hand off matching IDs to `efetch`, `esummary`, `elink`, or `xtract`.
- Use this whenever you need database-specific search syntax, not a free-form web search.

## Common Patterns

```bash
# 1) PubMed literature search
esearch -db pubmed -query 'ebola virus[Title/Abstract] AND 2024[pdat]'
```

```bash
# 2) Gene search with field qualifiers
esearch -db gene -query 'TP53[gene] AND human[orgn]'
```

```bash
# 3) Search and immediately fetch document summaries
esearch -db assembly -query 'GCF_000001405.40[accn]' | efetch -format docsum
```

## Recommended Workflow

1. Pick the Entrez database first, because query fields and sort modes are database-specific.
2. Write the query with field tags whenever possible instead of relying on broad keywords.
3. Run `esearch`, then immediately pipe IDs into `efetch`, `esummary`, or `elink`.
4. Use `xtract` only after you know what XML structure the downstream command emits.

## Guardrails
- `-db` and `-query` are both required.
- Wildcards and unqualified terms can explode result counts; narrow with fields like `[AUTH]`, `[GENE]`, or `[orgn]`.
- Sort options are database-specific, so do not assume the same `-sort` values work everywhere.
- `esearch` gives you IDs, not the final report; plan the next pipeline step before running it at scale.
