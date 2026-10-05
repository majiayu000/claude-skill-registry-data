---
name: gbf2info
description: Use when converting GenBank Flat files to structured info output for downstream parsing or analysis.
disable-model-invocation: true
user-invocable: true
---

# gbf2info

## Quick Start

- **Command**: `gbf2info`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/gbf2info`
- **Reference**: See [references/help.md](references/help.md) for detailed documentation

## When To Use This Tool

- Convert GenBank flatfiles into structured `GenBankInfo` XML.
- Expose accession, locus, organism, feature, qualifier, sequence, transcription, and translation content in a machine-friendly XML layout.
- Provide a richer intermediate representation for downstream `xtract`-based extraction than raw GenBank text.

## Common Patterns

```bash
# 1) Convert a GenBank flatfile into structured GenBankInfo XML
gbf2info < records.gbf > records.info.xml
```

```bash
# 2) Convert and inspect feature-level content immediately
gbf2info < records.gbf | xtract -pattern feature -element feature_key gene product protein_id
```

## Recommended Workflow

1. Start from real GenBank flatfile content, typically from `efetch`.
2. Pipe it into `gbf2info` and inspect a small sample first.
3. Confirm that the emitted `GenBankInfo` structure contains the features and qualifiers you expect.
4. Feed that XML into downstream `xtract`, CDS extraction, or reporting steps.

## Guardrails

- The wrapper is an `xtract`-heavy pipeline over GenBank XML, so the broader EDirect toolchain must be on `PATH`.
- `--help` / `--version` do not provide custom documentation; with no input the wrapper falls through to xtract-style “no data supplied” errors.
- Feature names that would collide with qualifier names or invalid XML tags are remapped internally (for example `3'UTR` becomes `3_UTR`), so do not assume raw GenBank feature names survive unchanged.
