---
name: esummary
description: Use when fetching document summaries from NCBI Entrez databases by database name and identifier or accession
disable-model-invocation: true
user-invocable: true
---

# esummary

## Quick Start
- **Command:** `esummary`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esummary`
- **Full reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Retrieve lightweight metadata summaries without fetching the full record.
- Summarize Assembly, BioProject, BioSample, SRA, ClinVar, and many other Entrez objects.
- Use `-mode json` when downstream parsing prefers JSON over XML.
- Prefer `esummary` over `efetch` when you only need metadata, not the full payload.

## Common Patterns

```bash
# 1) Assembly summary
esummary -db assembly -id GCF_000001405.40
```

```bash
# 2) SRA summary in JSON
esummary -db sra -id SRR5437876 -mode json
```

```bash
# 3) Search then summarize
esearch -db biosample -query 'SAMN03737421' | esummary
```

## Recommended Workflow

1. Use `esearch` or known accessions to get the relevant record IDs.
2. Fetch summaries first to inspect metadata before pulling full records.
3. Switch to `-mode json` only if your downstream tooling benefits from it.
4. Use `xtract` on XML summaries when you need a quick tabular extract.

## Guardrails
- `esummary` returns summaries, not full records or raw sequence payloads.
- Database names and accession styles are database-specific; validate them with `einfo` or `esearch` if unsure.
- Use `-raw` only when you know the database-specific XML rewriting is getting in your way.
- Network connectivity to NCBI is required for all operations.
