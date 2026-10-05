---
name: co-scientist-validate
description: Validate one Co-Scientist run directory from Codex.
---

# co-scientist-validate

Goal:

- Validate one Co-Scientist run directory against the canonical artifact contracts.

Expected input:

- one run directory such as `runs/test1`

Execution steps:

1. Run:

   ```bash
   python -m tools.validation.contract_validation <run-dir> --skill co-scientist-pipeline
   ```

2. For resumed runs, include:

   ```bash
   --resume
   ```

3. Report validation errors with artifact paths and issue messages.

Rules:

- This entry skill is a thin validation surface over `tools.validation.contract_validation`.
- Do not declare a run valid without calling the validator.
