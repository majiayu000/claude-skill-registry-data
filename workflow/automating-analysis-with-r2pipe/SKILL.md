---
name: automating-analysis-with-r2pipe
description: 'Automates radare2/rizin analysis through r2pipe to script function enumeration, string
  and import extraction, and cross-reference queries across samples programmatically. Activates for
  requests to automate radare2 with r2pipe, script rizin analysis, or batch-extract functions and
  xrefs from binaries.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - radare2
  - rizin
  - r2pipe
  - automation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059
  - T1587.001
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'radare2 r2pipe documentation — https://github.com/radareorg/radare2-r2pipe'
  - 'radare2 command reference — https://book.rada.re/'
---

# Automating Analysis With r2pipe

## When to Use

- You want to script radare2/rizin to extract functions, imports, strings, and cross-references
  programmatically, across one or many samples.
- You are building a repeatable triage pipeline on top of r2's analysis commands.

**Do not use** r2 to debug/run the sample here — this skill drives static analysis commands
(`aaa`, `aflj`, `izj`, `iij`). Run inside an isolated environment.

## Prerequisites

- radare2 (or rizin) installed and the `r2pipe` Python package (the script degrades gracefully and
  reports unavailability if absent).

## Safety & Handling

- r2 static analysis does not execute the sample; keep the working directory isolated.

## Workflow

### Step 1: Confirm r2pipe availability

```bash
python scripts/analyst.py check
```

Reports whether `r2pipe` and an `r2`/`rizin` binary are available.

### Step 2: Extract an analysis summary

```bash
python scripts/analyst.py summary sample.bin
```

Opens the binary, runs analysis (`aaa`), and collects functions (`aflj`), imports (`iij`), and
strings (`izj`) as structured JSON.

### Step 3: Query cross-references

For a function of interest, gather xrefs to/from to map call relationships.

### Step 4: Aggregate

Combine per-sample summaries for comparison and signature development.

## Validation

- The summary returns non-empty functions/imports for a normal binary.
- JSON commands (`*j`) are parsed, not screen-scraped text.
- Missing r2pipe/r2 is reported clearly rather than crashing.

## Pitfalls

- Forgetting to run `aaa` before querying functions (empty results).
- Mixing radare2 and rizin command differences in scripted output.
- Very large binaries making `aaa` slow — scope analysis as needed.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the automation wrapper.
- r2pipe and radare2 command references (linked in frontmatter).
