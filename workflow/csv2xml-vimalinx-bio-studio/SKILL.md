---
name: csv2xml
description: Use when converting CSV-style tabular data into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# csv2xml

## Quick Start

- **Command:** `csv2xml < table.csv > table.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/csv2xml`
- **Full reference:** See `references/help.md` for detailed usage and options

## When To Use This Tool

- Turn comma-separated tables into XML so they can be handled with `xtract` and other XML-aware tools.
- Move spreadsheet-like metadata into the same XML-oriented processing path used elsewhere in EDirect.
- Normalize tabular annotations before merging them with XML-centric records or reports.

## Common Patterns

```bash
# 1) Convert a CSV file into XML
csv2xml < table.csv > table.xml
```

```bash
# 2) Convert and inspect the first XML records immediately
csv2xml < table.csv | sed -n '1,40p'
```

## Recommended Workflow

1. Make sure the upstream file really is comma-delimited and structurally consistent.
2. Run `csv2xml` through stdin redirection or an explicit pipe.
3. Inspect the first emitted records before converting a large batch.
4. Feed the XML into downstream `xtract` or archive-building steps only after that smoke test passes.

## Guardrails

- This wrapper simply calls `transmute -c2x`, so `transmute` must be available on `PATH`.
- The installed wrapper does not provide a real `--help` / `--version` surface.
- In this environment, a trivial CSV smoke test produced no output rather than a format-specific error, so validate on representative data first.
- Prefer stdin/pipes over relying on undocumented positional-file behavior.
