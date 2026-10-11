---
name: bug-investigation
description: Diagnose and fix software bugs through evidence-based investigation. Use when Codex needs to handle runtime errors, failed API calls, broken UI behavior, incorrect database results, failed tests, deployment issues, build failures, auth/authorization bugs, form submission problems, missing or duplicate data, performance regressions, crashes, client-reported defects, intermittent behavior, or any software defect that requires root-cause analysis before applying a fix.
---

# Bug Investigation

Use this skill to trace symptoms to root cause before changing code.

## Core Rule

Do not patch randomly. Gather evidence, identify the affected code path, reproduce when possible, fix the root cause with the smallest safe change, and verify honestly.

## Workflow

1. Gather bug information:
   - error message, stack trace, logs, screenshot or behavior
   - user action, expected behavior, actual behavior
   - affected page, API, role, feature, workflow, environment
   - frequency and recent related changes
2. Classify the bug type.
3. Trace the affected code path across relevant layers:
   - frontend, backend, database, auth, integration, deployment, tests
4. Reproduce the issue safely when possible.
5. Compare expected vs actual behavior.
6. Identify the root cause with evidence:
   - file/path involved
   - wrong assumption
   - why the issue happened
   - proof supporting the conclusion
7. Choose the smallest safe fix.
8. Implement focused changes only.
9. Add or update regression tests when practical.
10. Run relevant checks discovered from project files/docs.
11. Search for the same pattern nearby and list related issues.
12. Produce a bug investigation summary.

Read `references/investigation-checklist.md` for bug categories, code-path tracing guidance, verification rules, and final report format.

## Behavior Rules

- Do not edit files before understanding the bug.
- Do not assume root cause without evidence.
- Do not make unrelated refactors.
- Do not hide errors without solving the cause.
- Do not rely only on frontend fixes for backend security or permission bugs.
- Do not expose secrets from logs or environment files.
- Do not claim the bug is fixed unless it was verified or the verification limitation is clearly stated.
- Add a regression test when practical.

## Output Contract

When using this skill, provide:

1. Bug report, expected behavior, and actual behavior.
2. Affected area and reproduction steps.
3. Evidence found.
4. Root cause.
5. Fix applied.
6. Files changed.
7. Tests/checks run and results.
8. Related issues, risks, and follow-up recommendations.
