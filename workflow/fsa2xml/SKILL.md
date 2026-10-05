---
name: fsa2xml
description: Use when converting FASTA sequence records into XML for downstream EDirect or XML-based sequence processing.
disable-model-invocation: true
user-invocable: true
---

# fsa2xml

## Quick Start

- **Command:** `fsa2xml < sequences.fasta > sequences.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fsa2xml`
- **Reference:** See [references/help.md](references/help.md) for full usage details

## When To Use This Tool

- Wrap FASTA records in XML so they can be inspected or transformed with `xtract`.
- Preserve sequence IDs, optional titles, sequence length, and sequence text in a structured form.
- Bridge plain-text FASTA inputs into XML-centric EDirect workflows.

## Common Patterns

```bash
# 1) Convert FASTA records into XML
fsa2xml < sequences.fasta > sequences.xml
```

```bash
# 2) Convert and inspect record-level fields immediately
fsa2xml < sequences.fasta | xtract -pattern FASTA -element ID Title Length Seq
```

## Recommended Workflow

1. Start with one-record-per-header FASTA input.
2. Run `fsa2xml` via stdin redirection or as part of a pipe.
3. Confirm that the emitted XML contains the expected `<FASTA>` blocks and sequence metadata.
4. Hand the XML off to `xtract`, `xml2json`, or other XML-side tools only after that quick inspection.

## Guardrails

- This is a thin wrapper around `transmute -f2x`, so `transmute` must also be on `PATH`.
- The current build does not expose a real `--help` or `--version` response.
- The emitted XML is record-oriented: each FASTA entry becomes its own `<FASTA>` block rather than a single enclosing document.
- Prefer stdin or pipes over relying on undocumented positional-file behavior.
