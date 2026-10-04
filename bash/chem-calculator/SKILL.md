---
name: chem-calculator
description: Use for local, reproducible chemistry calculations that need deterministic numeric checking rather than web lookup.
---

# Chem Calculator

## Overview

`chem-calculator` is a local first-batch chemistry calculation toolbox. It covers common molar-mass, stoichiometry, concentration, Ksp, acid/base, gas-law, thermodynamics, redox, electrochemistry, unit-conversion, and answer-check tasks with structured JSON output. Unit parsing and conversion use Pint through a small chemistry-oriented alias layer; symbolic expression equivalence helpers use SymPy for deterministic formula checks.

## When to Use

Use this skill when:
- a chemistry question is primarily numerical
- a candidate numeric answer needs verification
- unit handling or tolerance checks matter
- the calculation can be handled with bounded local models instead of free-form reasoning

Do not use this skill for structure lookup, nomenclature resolution, or literature search.

## Execution

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/chem-calculator/scripts/<capability>.py -- \
  --request-json /path/to/request.json \
  --output-dir /tmp/<skill-out> \
  --json
```

- `--output-dir` is required and will be created if missing.
- Every script writes `result.json` in the output directory.
- `--json` prints the same top-level payload written to `result.json`.

Read [contracts.md](references/contracts.md) for supported request modes and failure semantics.
