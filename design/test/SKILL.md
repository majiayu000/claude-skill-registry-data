---
name: test
description: Use this skill during Phase 5 to execute functional tests, record results, log defects, and validate UX conformance. Logs defects to Git Issues when available, otherwise to markdown (or JSON, per config) under .claude/sdlc/defects/. Reports code coverage against the configured threshold. Triggered after build is signed off and before deploy. Also trigger when the user says "run tests", "report coverage", "log defects", or "validate UX".
next_suggestions:
  - when: test_gate_signed
    suggest: "run /deploy to produce a deployment proposal"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /deploy when all roles are covered"
---

# Test (Phase 5)

Execute the tests defined in Design, report results, route defects.

## Prerequisite

`.claude/sdlc/gates/build-<task-slug>.md` must exist and be signed.

## Step 1 — Execute functional tests

Run the test runner configured in `config/tools.json`. Capture:

- Pass/fail per test case (tied back to REQ IDs via the test-case metadata)
- Coverage (vs. configured threshold; default 80% on modified code)
- Duration, flakiness if observed

Write the execution report to `.claude/sdlc/test/<task-slug>-report.md`.

## Step 2 — Log defects

For each failure, create a defect record:

- **If Git + Issues detected** (per `.claude/sdlc/env.json`): create an issue with labels `defect`, `severity:<level>`, `phase:test`, and link to the test case and REQ IDs.
- **Otherwise:** write `.claude/sdlc/defects/<task-slug>/<defect-id>.md` using `templates/defect.md`. Use JSON if `artifact_format_fallback` is set to `json`.

Every defect references at least one REQ ID and at least one test case.

## Step 3 — UX conformance

If the build produced frontend output, run the UX conformance checklist:

- Visual comparison against mockups (screenshots under `.claude/sdlc/test/ux/<task-slug>/`)
- Spacing, palette, typography, component usage, state handling
- Accessibility basics (contrast, keyboard nav, ARIA)

Record pass/fail items in the report. UX failures are defects, logged the same way.

## Step 4 — Coverage gate

If coverage on modified code is below threshold, the phase fails. Either:

- Add missing tests (but *only* for modified functions — see Phase 4 rule), or
- Record an explicit waiver in the report with justification, requiring human gate to accept.

## Human gate

Summarize: tests run, pass/fail, coverage on modified code, defects logged, UX status. Sign-off → `.claude/sdlc/gates/test-<task-slug>.md`.

## What this skill must NOT do

- Do not silently skip failing tests.
- Do not inflate coverage by adding tests for unmodified code.
- Do not mark a UX failure as "cosmetic" without human confirmation.

## References

- `templates/defect.md`
- `templates/gate.md`
- `docs/SDLC.md` Test

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'test_gate_signed|run /deploy to produce a deployment proposal' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /deploy when all roles are covered' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
