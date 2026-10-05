---
name: gff2xml
description: Use when converting GFF or GFF3 feature annotations into structured XML for downstream EDirect-style processing.
disable-model-invocation: true
user-invocable: true
---

# gff2xml

## Quick Start

- **Command:** `gff2xml [options] < input.gff > output.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gff2xml`
- **Full reference:** See `references/help.md` for detailed usage and options

## When To Use This Tool

- Turn GFF/GFF3 feature lines into structured XML with explicit fields and parsed attributes.
- Preserve the common columns (`SeqID`, `Source`, `Type`, `Start`, `End`, `Score`, `Strand`, `Phase`) in a machine-friendly XML layout.
- Split semicolon-delimited `Attributes` into nested XML tags for downstream extraction.

## Common Patterns

```bash
# 1) Convert a GFF3 file into structured XML
gff2xml < annotations.gff3 > annotations.xml
```

```bash
# 2) Convert and inspect parsed attributes immediately
gff2xml < annotations.gff3 | xtract -pattern GFF -element SeqID Type Start End ID Name
```

## Recommended Workflow

1. Confirm the input really is 9-column GFF/GFF3 with semicolon-delimited attributes.
2. Run `gff2xml` via stdin redirection so the wrapper can process the stream.
3. Inspect a few output records to confirm the expected XML tags and attribute splitting.
4. Use the XML with `xtract` or downstream reporting steps once the structure looks right.

## Guardrails

- This is not a single binary conversion primitive; it chains `tbl2xml`, `xtract`, and `transmute`, and all of those helpers must be on `PATH`.
- The wrapper has no real `--help` / `--version` path; probing it outside a working EDirect environment mostly yields missing-command noise.
- Attributes are split on semicolons into nested XML tags, so unusual attribute encodings may need spot-checking.
- Because the wrapper does not pass through positional filenames, stdin redirection is the safest invocation pattern.
