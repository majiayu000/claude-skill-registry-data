---
name: scripting-ghidra-headless-analysis
description: 'Automates batch reverse engineering by generating Ghidra analyzeHeadless commands and
  post-analysis script skeletons to import, auto-analyze, and export results for many samples
  without the GUI. Activates for requests to script Ghidra headless analysis, batch-analyze samples
  with Ghidra, or generate an analyzeHeadless command and post-script.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - ghidra
  - automation
  - headless
  - batch-analysis
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
  - 'Ghidra analyzeHeadless documentation — https://ghidra-sre.org/'
  - 'Ghidra API (FlatProgramAPI) — https://ghidra.re/ghidra_docs/api/'
---

# Scripting Ghidra Headless Analysis

## When to Use

- You need to auto-analyze many samples (or re-run a consistent analysis) without the Ghidra GUI.
- You want to generate the `analyzeHeadless` command and a post-script that exports functions,
  strings, or decompiled output.

**Do not use** this to run untrusted samples — Ghidra analyzes binaries statically and never
executes them, but keep the import directory isolated. This skill prepares automation, it does not
run the binary.

## Prerequisites

- A Ghidra installation (`analyzeHeadless` in `support/`) and the samples to import.

## Safety & Handling

- Ghidra does not execute the sample; still store imports in an isolated, defanged directory.

## Workflow

### Step 1: Generate the headless command

```bash
python scripts/analyst.py command --project /proj --name Batch --import ./samples --script export.py
```

Builds an `analyzeHeadless` invocation with project path, import directory, post-script, and common
flags (`-recursive`, `-overwrite`, `-deleteProject` optional).

### Step 2: Generate a post-analysis script skeleton

```bash
python scripts/analyst.py postscript --out export.py --emit functions,strings
```

Emits a Ghidra Python (Jython) script that iterates functions/strings and writes JSON next to the
program.

### Step 3: Run and collect

Execute the generated command, then aggregate the per-sample JSON exports.

### Step 4: Review

Spot-check a few exports to confirm analysis completeness before scaling up.

## Validation

- The generated command references a valid project path, import dir, and existing post-script.
- The post-script uses real Ghidra API calls (`currentProgram`, `getFunctionManager`).
- Output JSON is produced per imported program.

## Pitfalls

- Forgetting `-overwrite`/`-recursive`, causing skipped or duplicate imports.
- Jython 2 syntax constraints in post-scripts (no f-strings).
- Project lock conflicts when running multiple headless jobs on one project.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the generator.
- Ghidra analyzeHeadless and API docs (linked in frontmatter).
