---
name: bug-triage
description: Triage and fix GitHub bug reports for Aries AI. Use when a GitHub issue is classified as a bug, regression, defect, outage, broken flow, or runtime failure that should be reproduced, fixed on a branch, validated before/after, deployed to staging, and tracked in data/feedback-processing-log.json.
---

# Bug Triage

Use this skill for GitHub issues that represent defects in `DeliciousHouse/aries-app`.

## Read this when needed
- Severity rubric: `references/severity-rubric.md`

## Required inputs
- GitHub issue number
- Repo root: `/app/aries-app`
- Feedback log: `data/feedback-processing-log.json`

## Required procedure
1. Confirm the issue record is pending in the feedback log:
   - Inspect `data/feedback-processing-log.json` for the issue entry.
2. Inspect the issue in GitHub:
   - `gh issue view <number> --repo DeliciousHouse/aries-app --json title,body,labels,comments,url`
3. Classify severity using the rubric.
4. Reproduce the bug before changing code.
   - Prefer an existing failing test.
   - If none exists, add the smallest targeted regression test that fails first.
   - If automation is impossible, record the exact manual repro steps and expected/actual behavior.
5. Locate the likely root cause in the checked-in code.
6. Create a branch named `bugfix/issue-<number>-<slug>`.
7. Implement the smallest safe fix.
8. Run validation in this order:
   - targeted regression test(s)
   - nearest related test file(s)
   - broader repo validation only as needed for confidence
9. Deploy the branch to staging:
   - Use the project's staging deploy process; if none is configured, record `staging: missing-config` and continue.
10. Verify the bug is reproducible before the fix and not reproducible after the fix.
11. Update `data/feedback-processing-log.json` so the record includes:
   - `severity`
   - `rootCause`
   - `branch`
   - `validationBefore`
   - `validationAfter`
   - `stagingUrl`
   - `status`
   - `summaryPending`
12. If severity is `critical`, make the result explicit in your final output so the caller can alert immediately.

## Guardrails
- Do not claim a fix without before/after evidence.
- Do not skip staging verification unless the staging deploy hook is missing; if it is missing, fail loudly with the exact missing env/config.
- Prefer minimal, reversible fixes over broad refactors.
- Keep unsupported scope creep out of the bug fix.

## Output format
Return only:
- `status:` success or failed
- `issue:` `#<number>`
- `severity:` critical/high/medium/low
- `root_cause:` short phrase
- `branch:` branch name or `none`
- `validation_before:` one line
- `validation_after:` one line
- `staging:` URL or `failed` or `missing-config`
- `alert:` `critical` or `none`
- `next_step:` short operator follow-up or `none`
