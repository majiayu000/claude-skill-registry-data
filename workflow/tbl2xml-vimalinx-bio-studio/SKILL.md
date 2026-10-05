---
name: tbl2xml
description: Use when converting tabular text into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# tbl2xml

## Quick Start

- **Command:** `tbl2xml < table.tsv > table.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/tbl2xml`
- **Full reference:** See [references/help.md](references/help.md) for complete options and usage

## When To Use This Tool

- Turn table-like text into XML so it can be processed with XML-side tools.
- Bridge text-table intermediate files into the XML-centric parts of an EDirect workflow.
- Normalize tabular annotations before downstream extraction or archiving.

## Common Patterns

```bash
# 1) Convert a tabular text file into XML
tbl2xml < table.tsv > table.xml
```

```bash
# 2) Convert and inspect the first emitted XML blocks
tbl2xml < table.tsv | sed -n '1,40p'
```

## Recommended Workflow

1. Make sure the upstream table really matches the format expected by your workflow.
2. Feed it to `tbl2xml` through stdin redirection or a pipe.
3. Inspect a small sample before converting an entire dataset.
4. Use the resulting XML with downstream `xtract` or reporting steps after that smoke test passes.

## Guardrails

- This wrapper simply runs `transmute -t2x`, so `transmute` must be on `PATH`.
- The installed wrapper does not provide a real `--help` / `--version` interface.
- In this environment, a trivial tabular smoke test produced no output rather than a schema error, so validate on representative data first.
- Prefer stdin/pipes over undocumented positional-file behavior.
