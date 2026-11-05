---
name: verify
description: Run full verification on recent code changes — tests, LLD compliance, and security review. Claude MUST run this automatically after building any feature. Do not wait for user to ask.
---

Run a full verification pass on the code changes just made. Launch these 3 agents IN PARALLEL:

1. **test-writer agent** — Write tests for any new services/routes that don't have tests yet. Run all tests. Report pass/fail.

2. **lld-checker agent** — Validate that the new code matches docs/LLD.md — check API shapes, data models, error formats, component boundaries.

3. **security-reviewer agent** — Check for SQL injection, hardcoded secrets, missing input validation, unsafe deserialization, credentials in logs.

After all 3 agents complete, synthesize their results into a single report:

## Verification Report
- **Tests:** X passed, Y failed (list failures)
- **LLD Compliance:** matches / mismatches found (list each)
- **Security:** issues found / clean (list each)
- **Overall:** PASS or FAIL

If any agent reports issues, list them clearly so the user can decide what to fix.
