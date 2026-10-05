---
name: einfo
description: Use when you need to discover available NCBI Entrez databases, explore searchable fields within a specific database, or identify cross-database links for building EDirect queries.
disable-model-invocation: true
user-invocable: true
---

# einfo

## Quick Start
- **Command:** `einfo [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/einfo`
- **Full reference:** See `references/help.md` for complete options and XML output examples

## When To Use This Tool

- Discover which Entrez databases exist.
- Inspect searchable fields before writing a nontrivial `esearch` query.
- Enumerate cross-database link names before using `elink`.
- Use this as the schema-discovery step for EDirect pipelines.

## Common Patterns

```bash
# 1) List all available databases
einfo -dbs
```

```bash
# 2) Inspect searchable fields for PubMed
einfo -db pubmed -fields
```

```bash
# 3) Inspect available link names from PubMed
einfo -db pubmed -links
```

## Recommended Workflow

1. Use `-dbs` when you are unsure which Entrez database holds the data you want.
2. Use `-fields` before constructing advanced `esearch` expressions.
3. Use `-links` before writing `elink -name ...` pipelines.
4. Keep a copy of useful field or link names in the project docs if the workflow will be reused.

## Guardrails
- `einfo` is metadata discovery, not record retrieval.
- The `-db` argument accepts a specific database or `all`, but using `-dbs` first is usually safer.
- Output is XML-oriented; use `xtract` if you need structured extraction.
- Field and link names are authoritative here, so rely on them instead of guessing Entrez syntax.
