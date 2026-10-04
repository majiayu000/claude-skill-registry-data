---
name: triage-issue
description: Triage OpenDataSuite GitHub issues — assign milestone and labels per docs/ROADMAP.md, detect duplicates, and check acceptance criteria are testable. Use for new issues, backlog grooming, or when asked to update milestones.
---

# Triage

1. Fetch the issue(s). Search for duplicates by title/topic (`search_issues`), and check
   ROADMAP §5.
2. Pick the milestone using ROADMAP §4 — the earliest milestone whose release needs it.
   Anything not required by M0–M6 goes to M7/M8/M9.
3. Pick labels from `.github/labels.json`: exactly one `type:*`, one or more `area:*`,
   `provider:*` if vendor-specific, `priority:critical-path` if it blocks a release.
4. Check acceptance criteria are verifiable; if not, draft sharper criteria.
5. **Write changes to the repo files first** (`.github/milestones.json`, ROADMAP tables),
   then apply to GitHub with `scripts/sync-milestones.sh` (or MCP `issue_write`) —
   **only when the user has asked you to modify GitHub**. Otherwise present the proposal.
6. Closing duplicates: comment `Duplicate of #N`, close with `state_reason: duplicate`, and
   only with user approval.
