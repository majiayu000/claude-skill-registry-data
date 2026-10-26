---
name: gap-scan
description: Survey one or more repos (code, commits, docs, tests, issues) and return a ranked, evidence-cited list of gaps, bugs, and extension ideas as issue-ready items. Read-only apart from its report. Use for "what's missing", "find gaps", "what should I work on in this repo".
argument-hint: "[repo path | owner/repo, ...] [--commits N]"
---

Read-only. The one write is the report under `skilleddocs/gaps/`. Issues, comments, labels, and board changes each need an explicit yes for that action. Every `gh` call targets the repo resolved per the `next` skill's `BOARD.md`, Target repo section (`-R <o>/<r>`); on a fork, the yes for a write also names the repo it goes to.

No argument: current repo. Several: §1–3 per repo, one combined report. `--commits N` (default 20).

## 1. Sync

- Dirty = tracked changes, or untracked files outside `skilleddocs/` (`git status --porcelain -- . ':!skilleddocs'`), so this skill's own report never makes the next run dirty. Dirty → skip the pull and say so; survey as-is.
- No upstream (`git rev-parse --abbrev-ref @{u}` fails) or no remote (`git remote` prints nothing) → skip the pull, say so (`no upstream, pull skipped`); never set one yourself.
- Clean with an upstream → `git pull --ff-only`; diverged → report it like dirty.
- Fork → `git fetch upstream`; report ahead/behind; also list the parent's open `good first issue`s (`gh issue list -R <parent> --label "good first issue"`; reading the parent is fine).

## 2. Survey

- **Docs vs code**: every README/docs/roadmap claim the code contradicts (or code the docs miss), cited `doc:line` beside `code:line`.
- **Commits**: reverts, repeated fixes to one area (fragile spot), messages admitting shortcuts.
- **`TODO|FIXME|XXX`** in code, by `file:line`.
- **Tests**: find the command. Cheap (no network, GPU, paid calls, credentials) → run it, report failures. Otherwise "tests not run: <why>".
- **Open issues**: `gh issue list -R <o>/<r> --state open --json number,title,labels`. A gap matching one is **already tracked: #n**, listed but not re-proposed. `gh` can't reach issues (non-GitHub remote, not authed, no remote) → `Issues: not checked (<why>)`, and every item's status is `new (issues unchecked)`.
- **UI apps only** (frontend, served site, dashboard), with the `run` skill or a screenshot tool: screenshot the main views and note layout, spacing, style, and dead-link problems, citing screenshot + component. Otherwise "visual pass: skipped (<not a UI app | no tool>)".

## 3. Rank

Value for effort, highest first; the trade-off in one clause. Size `S` (one session, one area) or `L` (multi-area or needs a design call → `divide` candidate). **Evidence or drop it**: every item cites `file:line`, a SHA, or `#n`. A secret is cited by `file:line` or SHA only, never its value, in the report and the reply.

## 4. Report

`skilleddocs/gaps/<local-date>.md`, uncommitted unless asked. Untracked → exclude `skilleddocs/` per [TRACKING.md](../handoff-auto/TRACKING.md) so the next run's tree is clean and `pip install .` isn't broken by it. Per item:

```markdown
### <title>
- Why: <what's missing/broken and why it matters>
- Evidence: <file:line | SHA | #n>
- Size: S | L
- Suggested labels: <bug, enhancement, ...>
- Status: new | new (issues unchecked) | already tracked: #<n>
```

Chat reply:

```
Scanned <repo> (synced clean | dirty, pull skipped | no upstream, pull skipped). 12 candidates → 5 after filters.
Report: skilleddocs/gaps/<date>.md
1. [S] <title> — <why> (path/file.py:42)
2. [L] <title> — <why> (a1b2c3d)
Issues: <N open, M matched | not checked (why)>
Tests: <N passed/failed | not run: why>   Visual: <findings | skipped: why>
```

Then offer, don't run: `kanban-setup` (user-only: tell them to type `/kanban-setup`; board from this list), `divide` (split an `L`), `grill-docs` (stress-test a big call).
