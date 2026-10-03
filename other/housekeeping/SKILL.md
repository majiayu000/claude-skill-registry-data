---
name: housekeeping
layer: method
description: Generate the weekly "🧹 Housekeeping" digest — a render-only report of repo drift that needs a human eye (stale unmerged branches, mislabeled issues, stuck in-progress tickets, epics ready to close, idle PRs, label-coverage gaps). Reports only, never mutates. Use when asked for a "housekeeping report", "repo drift", "what's stale", or to run the weekly sweep by hand.
---

# Housekeeping digest

A weekly, **report-only** sweep that catches the drift the event-driven jobs miss — the
periodic backstop behind epic #633. It posts one rolling comment to a standing
"🧹 Housekeeping" issue listing everything that needs judgment but is too risky to auto-fix.
**It never deletes a branch, changes a label, or edits an issue** — the digest issue body is
the only thing it writes.

## What it reports (each section omitted when empty)

- **🌿 Stale unmerged branches** — not contained in `main` (still hold unmerged commits) and
  untouched for >N days. Merged-into-`main` branches are *out of scope* (lossless, not a
  human-eye item).
- **🏷️ Issues missing labels** — open issues without a `type:*` and/or a component
  (`pkg:`/`app:`/`worker:`/`poc:`) label.
- **🏗️ Label coverage** — `packages/*`·`apps/*`·`pocs/*`·`workers/*` dirs with no matching
  label declared in `.github/labels.yml` (CLAUDE.md treats a missing label as a build
  failure). Report-only — never auto-prune (a destructive label sync strips the label from
  every issue).
- **⏳ Stuck in-progress** — `status:in-progress` issues with no activity in >N days.
- **✅ Epics ready to close** — all sub-issues closed but the epic still open, split by the
  action each needs (read from the `status:ready-to-close` / `status:needs-postmortem` label
  the labeller stamps — see below): *run the postmortem then close* vs *postmortem done, just
  close*. Any entry whose `epic/<number>-*` branch still carries commits not on `main`
  (`git cherry origin/main origin/<branch>` non-empty) is annotated with a ⚠️ warning line —
  the exact failure mode from #1976, where four deliverables went missing because an epic
  branch was never merged (#1982). Report-only: it never blocks closing, it just says so.
- **🚧 Epics with active work but not marked in-progress** — a sub-issue is
  `status:in-progress` but the epic isn't, so it reads as "open, not started" (#980). The
  labeller reconciles this (see below); the digest just surfaces it.
- **🧭 In-progress under a non-open-epic parent** — `status:in-progress` issues whose parent
  isn't a currently-open epic: a closed epic left with unfinished work, or a parent missing
  the `epic` label (#980).
- **🔀 Idle PRs** — open PRs with no activity in >N days.
- **📚 Skill freshness** — knowledge skills (the `verified:` provenance contract, #1073/#1091)
  whose citations drifted or whose stamp aged out, via `scripts/skill-freshness.mjs` (fs+git, no
  LLM): a cited path that **vanished** (🔴), a cited file with commits **newer than the stamp**
  (🟡 possibly-stale), or a stamp **> 90d old** (🔵 re-verify due). Report-only — a re-verified,
  re-stamped skill drops off next run (#1100 WS3). Section dropped if the checker can't run.
- **🗑 Retired projects** — `retired/` dirs with a `.retired.json` stamp, showing age and flagging entries past 60 days for full deletion via `/retire-delete`.

## Pipeline (deterministic — no LLM, no secrets)

Mirrors `.claude/skills/epic-digest/`:

```
gather.mjs  → housekeeping.data.json   (git for branches + GitHub REST for issues/PRs/labels)
render.mjs  → housekeeping-<date>.md   (JSON → Markdown, sections dropped when empty)
post-comment.sh                        (upsert the one standing "🧹 Housekeeping" issue)
schedule.mjs                           (cadence-as-data: is today a send day per .github/digests.yml?)
```

### Run it by hand

```bash
GITHUB_TOKEN=$(gh auth token) node .claude/skills/housekeeping/gather.mjs > housekeeping.data.json
node .claude/skills/housekeeping/render.mjs housekeeping.data.json --out-dir .
cp housekeeping-*.md housekeeping.md
GH_TOKEN=$(gh auth token) DIGEST_BODY_FILE=housekeeping.md bash .claude/skills/housekeeping/post-comment.sh
```

Branch data needs a full checkout with remote branches present (`git fetch origin
'+refs/heads/*:refs/remotes/origin/*'`); without it the branch section is skipped, not guessed.

## Scheduling & delivery — `.github/digests.yml`

Cadence and delivery channel are **config-as-data**, not workflow plumbing (#637). The
workflow cron fires **daily** (cheap wake-up); `schedule.mjs` reads `digests.yml` and exits
early when today isn't a send day — so changing "weekly → daily" or "Wed → Mon" is a one-line
edit, never a `cron` change. Delivery is selection over rails that already exist: `issue`
(this standing-issue path) and `email` (Resend, mirrors `red-team-daily.yml`; degrades to a
green no-op when `RESEND_API_KEY` is unset).

```yaml
housekeeping:
  schedule: daily        # daily | weekly:<dow> ; dow = mon|tue|wed|thu|fri|sat|sun
  deliver: [issue]       # issue | email
  # to: [you@example.com]  # required only when deliver includes email
```

## Lossless branch sweep (separate workflow — the only auto-delete)

The digest is **report-only**. The one auto-destructive action lives in its own workflow
(`.github/workflows/cleanup-merged-branches.yml` → `prune-merged-branches.mjs`), split off by
blast radius so a digest bug can never delete a branch. It deletes a branch **only** if it is
provably contained in `main` (`git branch -r --merged origin/main`, 0 commits ahead) — lossless
by construction. It also skips any branch with an **open PR**, anything newer than
`BRANCH_MIN_AGE_DAYS` (default 1), and `main`/protected refs.

**Report-only until enabled:** it runs dry-run (lists what it *would* delete) unless `APPLY` is
on — set the repo variable `CLEANUP_BRANCHES_APPLY=true`, or run it via `workflow_dispatch` with
`apply: true`. Confirm a dry-run looks right before flipping the variable. Complements
`cleanup-epic-branches.yml` (which deletes `epic/*` on PR merge) by sweeping whatever slipped
past an event trigger.

```bash
GITHUB_TOKEN=$(gh auth token) node .claude/skills/housekeeping/prune-merged-branches.mjs        # dry-run
GITHUB_TOKEN=$(gh auth token) APPLY=true node .claude/skills/housekeeping/prune-merged-branches.mjs  # delete
```

## Epic status labels (separate workflow — the only auto-label) (#763 / #980)

The epic sections above read labels the digest does **not** set: `status:ready-to-close`,
`status:needs-postmortem`, and `status:in-progress`. They're reconciled by a separate daily
workflow (`.github/workflows/label-ready-epics.yml` → `scripts/label-ready-epics.mjs`), split
off by blast radius exactly like the branch janitor — it's the **only** auto-*label* mutation,
and the digest stays report-only. The labeller **derives** each open epic's status from its
children (mutually-exclusive, at most one):
- all sub-issues closed → `status:ready-to-close` if a `<!-- postmortem:done -->` marker exists
  on a comment (left by the `postmortem` skill), else `status:needs-postmortem`;
- ≥1 sub-issue `status:in-progress` → `status:in-progress` (the opening side, #980);
- otherwise (open-but-idle or no children) → none.
It removes any managed label the epic no longer qualifies for. The same labels drive the daily
epic-digest email's bands, so both digests agree. Dry-run by default; set repo var
`LABEL_READY_EPICS_APPLY=true` to write.

## Tuning

- `HOUSEKEEPING_STALE_DAYS` (env, default `14`) — the "no activity in N days" threshold.
- `HOUSEKEEPING_ISSUE_TITLE` (env, default `🧹 Housekeeping`) — the standing issue title.

The scheduled run lives in `.github/workflows/housekeeping.yml`.
