---
name: milestones
description: Create, name, scope, assign, and close GitHub milestones. Use when adding a milestone, deciding whether work belongs in one, or naming the next one. One axis per project (release / date / theme); never as labels.
---

# Milestones

A milestone is a *finite, scoped* group of issues converging on a
shipping or closing event. If it doesn't converge, it's a label.

## Pick one axis per project

- **Release-anchored** — name = the version it targets: `v1.0.0`,
  `v1.1.0` (semver), or `1.0.0.0` (PVP). Best when the project ships
  releases. Pre-stable work collapses to one placeholder — `v0.1.0`
  (semver) or `0.0.1.0` (PVP) — since those names already mean "not
  yet production-ready"; don't fan out across pre-1.0 versions.
- **Date-anchored** — name = the calendar window: `2026-Q2`,
  `2026-05`, `Sprint 23`. Best when work is time-bounded.
- **Theme-anchored** — name = the outcome: `Auth overhaul`,
  `Public beta`. Best for project phases not pegged to a release or
  window.

Don't mix axes within one project — `v1.1.0` and `2026-Q2` and
`Auth overhaul` together leaves contributors guessing where to file.
Pick one and inherit it for the next milestone.

## Description: outcome, not inventory

The description states the user-visible outcome the milestone
delivers — present-tense, the way you'd phrase an OKR objective.
Issues are the actions; the milestone is what those actions add up to.

- Outcome-shaped: "Auth flows can be configured without code
  changes." "Cold-start latency under 200ms on the free tier."
- Not outcome-shaped: "Refactor auth middleware." (That's a task —
  file as an issue.) "All v1.1 work." (Restates the title — adds
  nothing.) A list of issue links. (Readers can see those.)
- Optional: a short *non-goals* line to bound scope.

The description is the contract the convergence test runs against —
"does closing this issue advance *this outcome*?"

## When *not* to use a milestone

- Categorical tag (area, type, priority) → label.
- Ongoing planning surface across many issues → Project board.
- Ad-hoc "see also" between two issues → plain `#N` mention or the
  `issue-links` skill.

## Due dates

- Release- / date-anchored: set the due date to the release date or
  window end. Slipping the date is fine; missing data is worse than
  imprecise data — the rollup needs a horizon.
- Theme-anchored: skip unless there's a real deadline.

## Closing

A milestone closes when both:

1. Every issue inside is closed, AND
2. The convergent event happened (release cut, window ended, theme
   shipped).

If the event didn't happen yet, leave it open even with an empty
issue list — it's still expecting work. If issues remain when the
event hits, move spillover to the next milestone (or unset) before
closing; don't close with open issues — it falsifies the rollup.

Closed milestones are immutable history. Don't reopen to slot in
late work; create the next milestone.

## Operations

```bash
# List — closed ones show which axis is in use
gh api 'repos/:owner/:repo/milestones?state=all' \
  --jq '.[] | "\(.number)\t\(.title)\t\(.state)"'

# Create
gh api repos/:owner/:repo/milestones \
  -f title='v1.1.0' \
  -f due_on='2026-06-01T00:00:00Z' \
  -f description='...'

# Close
gh api -X PATCH repos/:owner/:repo/milestones/<num> -f state=closed
```

Assign with `mcp__github__issue_write` (`method: create` or `update`).
Its `milestone` param takes the milestone *number* from the listing
above, not the title.

## Procedure

1. Read existing milestones; identify the project's axis. If none is
   set and a milestone is being created, surface the choice (release
   / date / theme); don't silently pick.
2. New milestone: name in the axis; outcome-shaped description; due
   date if release- or date-anchored.
3. "Does this issue belong here?" — convergence test: will closing
   it advance the description's outcome? If not, leave it unassigned.
4. Closing: confirm the event happened and spillover is moved.
