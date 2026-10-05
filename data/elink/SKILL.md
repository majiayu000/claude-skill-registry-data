---
name: elink
description: Use when you need to navigate relationships between records in NCBI Entrez databases, find related articles, track citations, or link records across different databases such as PubMed to Protein.
disable-model-invocation: true
user-invocable: true
---

# elink

## Quick Start
- **Command:** `elink`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/elink`
- **Full reference:** See [references/help.md](references/help.md) for complete options and examples

## When To Use This Tool

- Traverse relationships between Entrez records after you already have IDs.
- Jump from PubMed to linked genes, proteins, assemblies, or other database objects.
- Follow citations with `-cited` or `-cites`.
- Discover which link types exist before building a larger EDirect workflow.

## Common Patterns

```bash
# 1) Find related PubMed records, then linked proteins
esearch -db pubmed -query 'lycopene cyclase' | \
  elink -related | \
  elink -target protein
```

```bash
# 2) Follow citation links
esearch -db pubmed -query 'Beadle GW [AUTH] AND Tatum EL [AUTH]' | \
  elink -cited | \
  efetch -format abstract
```

```bash
# 3) Inspect a specific link provider URL
elink -db pubmed -id 19880848 -cmd prlinks
```

## Recommended Workflow

1. Start with a defined source database and record IDs.
2. Decide whether you want same-database neighbors, cross-database links, or citation relations.
3. Use `-cmd` and `-name` to narrow the link mode when many link types exist.
4. Feed the linked IDs into `efetch`, `esummary`, or `xtract` rather than reading raw XML by eye.

## Guardrails
- `elink` needs valid database names and IDs from Entrez, not arbitrary external identifiers.
- `-related`, `-target`, `-cited`, and `-cites` solve different problems; pick the right one before chaining.
- Use `-name` when multiple link relationships exist between the same databases.
- Link traversal is network-dependent and can fail independently of your local pipeline logic.
