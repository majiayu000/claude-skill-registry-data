---
name: issue-create
description: File a new GitHub issue in the checked-out repo — search first for duplicates/adjacent issues to update or reference, detect the repo's issue template if any, then compose title/body/labels/milestone matching house style. Use when asked to file, create, open, report, or track an issue.
---

# Issue create

Don't file first. Search and inspect before composing.

## Dedup pre-flight

Open *and* closed — omitting `--state` searches both:

```bash
gh search issues "<keywords>" --repo <owner>/<repo> --limit 20
```

Read near-matches with `gh api repos/:owner/:repo/issues/<N>`. Decide:

- **Same outcome already open** — update the existing one
  (`mcp__github__issue_write` with `method: update` for the body,
  `mcp__github__add_issue_comment` for new context). Don't file a new
  one.
- **Same outcome closed for stale reasons** — reopen it
  (`mcp__github__issue_write`, `method: update`, `state: open`) with a
  comment citing what changed. Don't file a new one.
- **Adjacent** (same area, different angle) — file new, cite the
  existing in *Additional context*; consider an `issue-links` edge.
- **Partially covers** — narrow the new issue to the uncovered
  slice; cross-reference both ways.
- **Nothing close** — file new.

If torn, surface the call rather than silently pick.

## Detect repo conventions

```bash
ls .github/ISSUE_TEMPLATE/ 2>/dev/null

# REST reads — see ~/.claude/CLAUDE.md "GitHub API budget".
gh api 'repos/:owner/:repo/labels?per_page=100' --jq '.[].name'
gh api repos/:owner/:repo/milestones \
  --jq '.[] | "\(.number)\t\(.title)"'   # open only — can't assign a closed one
gh api 'repos/:owner/:repo/issues?per_page=5&state=all' \
  --jq '.[].title'                       # skim recent house style
```

Template present → read it and fill its fields into the body.
Templates encode the project's required fields; don't bypass with a
freeform body.

## Standard structure (no template)

- **Title** — statement true when done. Active voice, outcome.
  *"Profile writes persist across API restarts in Firestore"*,
  not *"Fix profile persistence"*.
- **Summary** — 1-2 sentences. What this delivers.
- **Motivation** — what problem, dependency, or opportunity drives
  it. Cite the trigger (PR review, incident, related issue).
- **Scope** — concrete changes, specific enough to start without
  guessing. Bullets, not prose.
- **Acceptance criteria** — measurable conditions, `- [ ]` task-list.
- **Additional context** — links, screenshots, related issues, only
  when they help. Skip the section if empty.

## Labels and milestones

- Pick existing labels. Don't invent inline — if nothing fits, skip
  or raise the label question separately.
- Milestone: assign if one fits the outcome (convergence test —
  closing the issue advances the milestone's description). Unset
  otherwise. Never use milestones as labels.
- Creating a new milestone → `milestones` skill.
- Relating to other issues/PRs → `issue-links` skill, after submit.

## Submit

Filing creates shared state — propose the body before submitting on
any non-obvious choice (scope, label call, dedup verdict).

File with `mcp__github__issue_write` (`method: create`):

- `labels` — array of existing label names.
- `milestone` — the *number* from the listing above, not the title.

## Procedure

1. Search open + closed; decide update / reopen / new / link.
2. Detect template; else prepare standard structure.
3. Fetch labels and milestones; pick fitters or skip.
4. Compose; surface non-obvious choices.
5. Submit; capture URL.
6. Apply cross-edges via `issue-links` if related.
