---
name: flow-tracker-update
description: Update the flow tracker issue for a UC. Reads current issue statuses from GitHub and updates the tracker's phase checklists. Used after any ticket closes.
---

# Flow tracker update

Update the flow tracker issue to reflect current ticket statuses.

## Input

- The UC identifier (e.g., UC-001).
- The flow tracker issue number.
- The version (milestone `vN`), from the tracker's scope or `dev/versions/README.md`.

## Process

### 1. Get current ticket statuses

A milestone holds every build of the version, so filter by the UC label too, and keep
only the tickets the tracker body lists (several builds of one UC can coexist).

```bash
gh issue list --milestone "vN" --label "uc:XXX" --state all --json number,title,state,labels,assignees
```

### 2. Group by phase

Using the `phase:*` labels, group tickets into their phases. Show the tier of test
tickets (`tier:*`) and the test author of implementation tickets.

### 3. Update the flow tracker issue

For each ticket:
- `[x]` if the issue state is `closed`
- `[ ]` if the issue state is `open`

```bash
gh issue edit TRACKER_NUMBER --body "..."
```

### 4. Check phase gates

The gates are defined in WORKFLOW.md "Phases". This skill reports whether their
ticket-based parts hold; it never closes a gate (the PO does).

- **Phase 1:** all `phase:research` tickets closed.
- **Phase 2:** all `phase:test-stubs` tickets closed (each test approved by the PO).
- **Phase 3:** the implementation plan is approved by the PO.
- **Phase 4:** every implementation ticket exists and names a test author who is not
  its assignee. Report any separation-rule conflict.
- **Phase 5:** all `phase:impl` and `phase:post-impl` tickets closed.
- **Phase 6:** every row in `dev/versions/vN/builds/UC-XXX-label/traceability-matrix.md`
  has Verified ticked; `eval-runs/` has a run for every eval-tier AC; `as-built.md` has
  a prediction, an actual flow and a drift section. Mirror the per-AC checklist under
  "Verified per AC" from the matrix rows.

Report a gate as "ready for the PO" rather than "complete".

### 5. Update the local mirror

Update `dev/versions/vN/builds/UC-XXX-label/flow-tracker.md` to match the GitHub issue.

## Linking convention

All `#N` references in local plan files must be clickable Markdown links (see
WORKFLOW.md "Linking convention"). At the start, derive the repo base URL:

```bash
git remote get-url origin
# https://github.com/{owner}/{repo}.git → base = https://github.com/{owner}/{repo}
```

When updating `dev/versions/vN/builds/UC-XXX-label/flow-tracker.md`, write every ticket reference as
`[#N]({base}/issues/N)`. The GitHub issue body uses bare `#N` (auto-linked).

## Rules

- Do not close tickets — only update the tracker display.
- Do not change ticket labels or assignments.
- Report the current phase and any blocked tickets in the output.
