---
name: timesheet
description: Builds a monthly timesheet draft from local git history, maps repo work to timesheet project codes, and fills the browser timesheet UI. Use when the user asks to compile, derive, or enter a timesheet from commits, git history, repo slugs, author names, or Crew Portal.
---

# Timesheet

Turn local commit evidence into a draft timesheet. Never submit the final timesheet unless the user explicitly asks.

## Inputs To Collect

Ask only for missing inputs:

- target month and year;
- repos root, default `~/Desktop/repos`;
- git author identities, including author names and email fragments;
- mapping from timesheet project code to repo slugs or paths;
- target timesheet URL and whether Browser plugin control is available.

When the user gives project labels but not mappings, ask for a compact mapping prompt:

```text
Map each Crew project code to repo slugs/paths:
- DPINTA-DEV -> wearedevpunks-multiplai, devpunks-mkt-tool
- DPAICL-FD -> harness-intelligence, wearedevpunks-skills
- DUKAPP-FD -> traevolution-app
```

If the Crew page is visible, read available project codes from the browser first, then ask the user to map unmatched repo slugs.

## Git Evidence

Use the helper script for first-pass evidence:

```bash
node skills/misc/timesheet/scripts/git-timesheet-evidence.mjs \
  --month 2026-06 \
  --repos-root ~/Desktop/repos \
  --authors "stefan-garofalo,Stefan Garofalo,simosabba" \
  --map "DPINTA-DEV=wearedevpunks-multiplai,devpunks-mkt-tool;DPAICL-FD=harness-intelligence,wearedevpunks-skills;DUKAPP-FD=traevolution-app"
```

Rules:

- Fetch target repos first when network/auth is available; continue from local refs if fetch fails.
- Use author date for workday allocation; keep commit date visible when it differs.
- Match authors case-insensitively against author name and email.
- Deduplicate duplicate clones by `(project code, commit hash)`.
- Keep nearby identities visible but separate unless the user confirms they count.
- Report codes/repos with zero matching commits.

## Allocation

Build a day-by-day ledger from evidence:

1. For one project on a day, assign `1d`.
2. For two projects on a day, assign `1/2d` each.
3. If three or more projects appear but the sheet only supports `1d` and `1/2d`, propose a practical carry-forward or adjacent-day allocation and mark it as a timesheet-entry adjustment.
4. Skip weekends if the UI disables them; fold weekend-only work into adjacent weekdays with matching project continuity.
5. Verify each filled day totals exactly `1d`.
6. Verify project totals and month total before browser entry.

## Browser Fill

Use the `Browser` plugin when available. If it cannot attach to the user's external browser, open the same URL in the in-app browser and ask the user to sign in there.

Workflow:

1. Open the timesheet URL and navigate to the target month.
2. Read available project options and confirm they match the mapping.
3. Turn on batch mode when the UI supports it.
4. Fill larger groups first: project + duration + selected days + apply.
5. After each apply, verify the logged total increased as expected.
6. Do a final grid verification and project-total verification.
7. Stop before `Submit timesheet` unless explicitly authorized.

Prefer stable DOM/role locators. If snapshots fail, use visible DOM or coordinate clicks only after a screenshot confirms the target.

## Output

Report:

- exact days and project codes entered;
- project totals and month total;
- any zero-evidence projects;
- any adjusted days, such as weekend folding or three-project carry-forward;
- whether the sheet remains draft or was submitted by explicit request.
