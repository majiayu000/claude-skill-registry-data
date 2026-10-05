---
name: scn2xml
description: Use when converting SCN-format records into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# scn2xml

## Quick Start

- **Command**: `scn2xml < input.scn > output.xml`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/scn2xml`
- **Full reference**: See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Convert SCN-format content into XML so it can be processed with XML-side tools.
- Bridge SCN-oriented intermediate files into the rest of an EDirect XML pipeline.
- Normalize SCN payloads before extraction or archiving.

## Common Patterns

```bash
# 1) Convert SCN input into XML
scn2xml < input.scn > output.xml
```

```bash
# 2) Convert and inspect the first emitted XML blocks
scn2xml < input.scn | sed -n '1,40p'
```

## Recommended Workflow

1. Confirm the upstream payload is really in the SCN form expected by your workflow.
2. Run `scn2xml` via stdin redirection or a pipe.
3. Check that non-empty XML is produced on a small sample first.
4. Only then send the XML to downstream `xtract` or archiving steps.

## Guardrails

- This wrapper simply runs `transmute -s2x`, so `transmute` must be on `PATH`.
- The installed wrapper does not expose a meaningful `--help` / `--version` response.
- Prefer stdin or pipes over undocumented positional-file behavior.
- If conversion yields no output, re-check the upstream SCN payload on a representative sample before scaling up.
