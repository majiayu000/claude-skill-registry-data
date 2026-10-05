---
name: efilter
description: Use when filtering Entrez search results by date, organism, publication type, sequence features, or other database-specific criteria in bioinformatics pipelines.
disable-model-invocation: true
user-invocable: true
---

# efilter

## Quick Start
- **Command**: `efilter`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/efilter`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Narrow an existing Entrez result set by date, organism, publication type, sequence feature, SNP class, or assembly status.
- Add database-specific shortcuts after `esearch` or `elink` without rewriting the whole query string.
- Prototype filters interactively before folding them back into a single `esearch` command.

## Common Patterns

```bash
# 1) Keep only recent PubMed hits from a pipeline
esearch -db pubmed -query "opsin gene conversion" \
  | efilter -mindate 2015 \
  | efetch -format docsum
```

```bash
# 2) Restrict sequence results to mammalian RefSeq entries
esearch -db protein -query hemoglobin \
  | efilter -organism mammals -source refseq
```

```bash
# 3) Keep only latest assemblies
esearch -db assembly -query "Escherichia coli" \
  | efilter -status latest
```

## Recommended Workflow

1. Start with an `esearch` or `elink` pipeline that already identifies the right Entrez database.
2. Apply only the shortcut family that matches that database category, such as `-pub` for PubMed or `-organism` for sequence databases.
3. Inspect counts or summaries if the filter logic is non-obvious.
4. Fetch full records only after the filter stage is stable.

## Guardrails

- The local executable is just a wrapper around `esearch -filter`, so it depends on valid Entrez pipeline state and is not an offline post-processor.
- Shortcut families are database-specific; mixing incompatible groups produces confusing or empty results.
- Many `efilter` shortcuts can also be expressed directly in `esearch`, which is often cleaner once you know the final query.
- In this local install, help output can still emit network-version-check noise from EDirect before printing the real usage text.
