---
name: gbf2xml
description: Use when converting GenBank flatfiles into XML for downstream EDirect or XML-based sequence annotation workflows.
disable-model-invocation: true
user-invocable: true
---

# gbf2xml

## Quick Start

- **Command:** `gbf2xml < records.gbf > records.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gbf2xml`
- **Full reference:** See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Convert GenBank flatfiles into XML so they can be queried with XML tools.
- Bridge annotated sequence records from flatfile form into EDirect pipelines that expect XML.
- Normalize GenBank content before further extraction, transformation, or archiving.

## Common Patterns

```bash
# 1) Convert a GenBank flatfile into XML
gbf2xml < records.gbf > records.xml
```

```bash
# 2) Convert and inspect the resulting XML structure quickly
gbf2xml < records.gbf | sed -n '1,40p'
```

## Recommended Workflow

1. Start from a representative GenBank flatfile sample.
2. Run `gbf2xml` through stdin redirection or a pipe.
3. Check that non-empty XML is produced before processing a large dataset.
4. Feed the XML into `xtract` or other downstream tools only after that smoke test passes.

## Guardrails

- This wrapper simply runs `transmute -g2x`, so the companion `transmute` binary must be on `PATH`.
- The installed wrapper does not provide a real `--help` / `--version` interface.
- Prefer stdin/pipes over relying on undocumented positional-file behavior.
- Malformed flatfiles can yield empty output, so inspect a small sample before batching.
