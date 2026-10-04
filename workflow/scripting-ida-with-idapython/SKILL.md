---
name: scripting-ida-with-idapython
description: 'Automates IDA Pro analysis with IDAPython by generating scripts that enumerate
  functions, decode strings, rename by signature, and export analysis results, and by documenting
  the headless idat batch invocation. Activates for requests to script IDA Pro, write IDAPython
  automation, or run IDA in batch/headless mode.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - ida-pro
  - idapython
  - automation
  - batch-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059
  - T1620
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'Hex-Rays IDAPython API documentation — https://hex-rays.com/products/ida/support/idapython_docs/'
  - 'IDA batch/headless (idat -A -S) usage — https://hex-rays.com/products/ida/'
---

# Scripting IDA Pro With IDAPython

## When to Use

- You use IDA Pro and want to automate repetitive analysis — enumerate functions, decode strings,
  apply signature-based renames, and export results — via IDAPython.
- You need a headless `idat` batch invocation to process many samples.

**Do not use** IDA's debugger (`-r`) on untrusted samples on your host — these scripts drive
*static* analysis. Work in an isolated environment.

## Prerequisites

- IDA Pro with IDAPython, and the samples to analyze.

## Safety & Handling

- IDA static analysis does not execute the sample; keep the input directory isolated.

## Workflow

### Step 1: Generate an analysis script

```bash
python scripts/analyst.py script --emit functions,strings --out ida_export.py
```

Emits an IDAPython script using the real API (`idautils.Functions`, `idc.get_func_name`,
`idautils.Strings`) that writes results to JSON next to the IDB.

### Step 2: Generate the headless batch command

```bash
python scripts/analyst.py batch --script ida_export.py --input sample.exe
```

Builds the `idat -A -S"script" input` invocation (auto-mode, run script, no UI) for batch runs.

### Step 3: Run and collect

Execute the batch command per sample and aggregate the JSON exports.

### Step 4: Iterate

Extend the generated script with signature renames (FLIRT) and decompiler (`ida_hexrays`) output
as needed.

## Validation

- The generated script uses real IDAPython API calls.
- The batch command uses `-A` (auto) and `-S` (script) correctly.
- JSON output is produced per processed IDB.

## Pitfalls

- IDAPython API drift between IDA 7.x and 9.x — target your version.
- Forgetting `-A` leaves IDA waiting for interactive input in batch.
- Decompiler calls require a licensed Hex-Rays decompiler.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the generator.
- IDAPython and idat batch references (linked in frontmatter).
