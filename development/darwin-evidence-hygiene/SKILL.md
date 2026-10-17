---
name: darwin-evidence-hygiene
description: Use when reporting build, test, or deploy results - enforces real tool output over plausible claims.
---

# Darwin Evidence Hygiene

## Trigger
Use before any success claim about a build, install, or test run.

## Procedure
1. Run the command and capture its REAL exit code.
2. Quote the last 3 lines of actual stdout/stderr as evidence.
3. If the command failed, report the failure verbatim - never
   substitute a plausible-looking result.
4. A green lint is not a green test run; run the tests.

## Pitfall
Never fabricate results for output you could not produce.

## Verification
After following the procedure: confirm the outcome
with real evidence (exit code, file, or API response).
```bash
python -c "import sys; print('darwin-species-ok')"
```
