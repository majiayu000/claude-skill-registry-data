---
name: epost
description: Use when you need to post unique identifiers or accession numbers to NCBI Entrez databases for subsequent retrieval operations
disable-model-invocation: true
user-invocable: true
---

# epost

## Quick Start
- **Command:** `epost`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/epost`
- **Full reference:** See [references/help.md](references/help.md) for complete options and examples

## When To Use This Tool

- Post a list of Entrez IDs or accessions for subsequent retrieval steps.
- Feed identifiers from stdin or file into the Entrez history workflow.
- Use this when IDs are already known and search is unnecessary.
- Chain directly into `efetch` or `esummary` for the actual human-usable output.

## Common Patterns

```bash
# 1) Post a protein accession from stdin and fetch FASTA
echo 3OQZ_a | epost -db protein | efetch -format fasta
```

```bash
# 2) Post an assembly accession directly
epost -db assembly -id GCF_000001405.38 | efetch -format docsum
```

```bash
# 3) Post IDs from a file
epost -db bioproject -input bioproject_ids.txt | efetch -format docsum
```

## Recommended Workflow

1. Choose the correct database before posting identifiers.
2. Decide whether the identifiers are UIDs or accessions and set `-format` if needed.
3. Use `epost` as the staging step, then immediately chain to retrieval or summarization.
4. Prefer file or stdin posting for long identifier lists instead of huge shell argument strings.

## Guardrails
- Always specify `-db`.
- Make sure the identifiers match the target database and `-format` semantics.
- Standalone `epost` output is mainly machine-oriented; it is not the end-user deliverable.
- Use stdin or `-input` for long lists rather than stuffing thousands of IDs into `-id`.
