---
name: opsin
description: Use when a prompt contains systematic or IUPAC-like chemical names that need deterministic name-to-structure parsing through OPSIN, with structured diagnostics and optional RDKit validation.
---

# OPSIN

## Overview

Resolve systematic organic names with the EMBL-EBI OPSIN web service. This skill is for name-to-structure parsing, not synonym search or general compound facts.

## When to Use

Use this skill when:
- the prompt contains a clear systematic or IUPAC-like chemical name
- multiple systematic names need consistent structure resolution
- OPSIN parse failures need normalized diagnostics
- a successful OPSIN structure should be checked locally with RDKit

Prefer `pubchem` instead for trivial names, trade names, abbreviations, or broad synonym lookup.

## Scripts

- `name_to_structure.py`
- `batch_name_to_structure.py`
- `parse_diagnostics.py`
- `validate_with_rdkit.py`

## Standard Command

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/opsin/scripts/<capability>.py -- \
  --request-json /path/to/request.json \
  --output-dir /tmp/<skill-out> \
  --json
```

Each script writes `result.json` in `--output-dir` and prints the same payload when `--json` is set.

Read [references/contracts.md](references/contracts.md) for request and response details.
