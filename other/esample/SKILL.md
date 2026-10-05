---
name: esample
description: Use when printing canned sample NCBI XML, JSON, flatfile, or GFF documents for testing, parser development, or xtract query prototyping.
disable-model-invocation: true
user-invocable: true
---

# esample

## Quick Start
- **Command**: `esample -docsum|-article|-book|-protein|-gene|-taxon|-blast|-snp|-hgvs|-bioc|-flatfile|-gff|-gencode`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/esample`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Get a representative sample document for `xtract`, parser, or schema debugging without making a live Entrez request.
- Create fixtures for tests or documentation that need stable example records.
- Learn the structure of a supported output type before switching to real `efetch` or `xfetch` data.

## Common Patterns

```bash
# 1) Prototype an xtract expression against a sample PubMed docsum
esample -docsum | xtract -pattern DocumentSummary -element Id Title
```

```bash
# 2) Save a sample GenBank flatfile or GFF3 record as a fixture
esample -flatfile > example.gb
esample -gff > example.gff3
```

```bash
# 3) Inspect sample genetic code output for parser work
esample -gencode
```

## Recommended Workflow

1. Choose the sample mode that matches the structure you need to inspect.
2. Pipe it into `xtract`, `transmute`, or your parser until the transformation is correct.
3. Save the output as a stable fixture if you need repeatable tests.
4. Replace the sample source with real `efetch`, `xfetch`, or archived data once the downstream logic is proven.

## Guardrails

- `esample` prints hard-coded example documents; it does not fetch live records from NCBI.
- Output goes to standard output, so redirect to a file if you want to keep the sample.
- Use one mode flag per invocation; this is a selector for canned examples, not a general conversion engine.
- The documented help entry point is `-help`, not `--help`.
