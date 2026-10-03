---
name: bug-reproduction
description: Turn a reported defect into a reliable, minimal, evidence-backed reproduction with exact environment, preconditions, steps, frequency, expected behavior, actual behavior, and scope clues.
---
# Bug Reproduction

Use when a defect report is vague, intermittent, environment-specific, or not yet actionable by the team that must fix it.

## Procedure
1. Capture the report without rewriting uncertainty into fact. Record the user goal, observed behavior, expected behavior, original evidence, affected account/data if safe to reference, and any claimed frequency or timing.
2. Record the environment precisely enough to compare runs: application/version or commit, platform/OS/browser/device, configuration or feature flags, locale/timezone, network conditions, user role/permissions, and relevant dataset state.
3. Reproduce the original path as faithfully as possible before simplifying it. Confirm whether the issue occurs and how often; distinguish deterministic, intermittent, timing-dependent, data-dependent, and environment-dependent behavior.
4. Capture strong evidence at the failure point: exact UI state, error text, logs or console/network evidence, screenshots/video when useful, timestamps, request/job identifiers, and persisted side effects. Avoid collecting unnecessary sensitive data.
5. Reduce the reproduction one variable at a time. Remove irrelevant steps, use smaller data, change one environmental factor, and identify the minimum preconditions that still trigger the defect.
6. Test nearby controls to bound scope: another user/role, data shape, browser/device, prior version, clean state, slow network, repeated action, or alternate path when those comparisons can isolate the condition.
7. Distinguish the first observable defect from later consequences. A broken final screen may be caused by an earlier failed request or state transition.
8. Write reproduction steps another person can follow from a known starting state, including setup/seed data and cleanup when necessary.
9. If the issue cannot be reproduced, document exactly what was attempted, what differs from the reporter's environment, and what evidence would most efficiently resolve the gap. Do not close the report merely because one environment is clean.
10. Hand off the confirmed reproduction with severity/impact evidence, scope clues, artifacts, and known non-reproducing controls without guessing at root cause unless the evidence actually supports it.

## Decision rules
- Reproduction establishes the defect; diagnosis explains it. Do not mix unsupported root-cause guesses into the reproduction record.
- "Works for me" is a data point, not a resolution.
- Minimize variables without changing the behavior being reported.
- Exact version and state matter more than a long narrative.

## Quality gate
The reproduction is ready when another person can trigger the same failure from documented preconditions or, for intermittent defects, observe a measured failure pattern with captured evidence; expected and actual behavior are unambiguous; scope clues are separated from speculation; and non-reproduction attempts are documented.