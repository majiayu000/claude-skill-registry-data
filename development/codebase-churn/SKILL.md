---
name: codebase-churn
category: codebase-build
description: Analyze a git repository's history and produce an SVG treemap of file churn — area = lines changed, color = commit frequency. Use when user wants to find unstable areas of a codebase, predict bug-prone files, see "where do we change the most", spot refactor candidates, or invokes /codebase-churn.
codex-short-description: "SVG treemap of git churn to find unstable, bug-prone files"
related-skills:
  - debug
  - codebase-improve-architecture
loop-eligible: false

compatibility: claude-code codex opencode
---
# codebase-churn

Generate a churn treemap from git history. Premise: files changed often (high commits) and heavily (high line churn) tend to harbor more bugs. Stable files are usually safer. Big + hot tiles are where to look first.

## Quick start

From the target repo:

```bash
python3 ~/.claude/skills/codebase-churn/scripts/churn_treemap.py \
  -o churn-treemap.svg --report churn-report.md
```

Open `churn-treemap.svg` in a browser. Hover any tile for path, commit count, lines added/deleted.

## Output

- **SVG treemap** — area = total lines changed (added + deleted); color = commit count on a log scale (blue = stable → red = volatile).
- **Markdown report** (`--report PATH`) — ranked table of top files for tracking over time or pasting into a doc.

## How to read it

| Tile | Meaning | Action |
| :--- | :--- | :--- |
| Big + red | Frequent and heavy edits | Refactor candidate. Likely under-tested. Bug-prone. |
| Big + blue | One large rewrite, then quiet | Probably stabilized. Verify it has tests. |
| Small + red | Many tiny touches (configs, version bumps) | Often a noisy interface or fragile contract. |
| Small + blue | Stable | Safe to leave alone. |

## Common flags

- `--since "6 months ago"` — restrict the window. Defaults to all history.
- `--until "2026-01-01"` — pair with `--since` to compare windows.
- `--top 100` — limit how many files appear (default 200).
- `--exclude REGEX` — repeatable. Lockfiles, `node_modules/`, `dist/`, `*.min.*` are excluded by default.
- `--no-default-excludes` — keep them in.
- `-C path/to/repo` — analyze a different repo than the cwd.
- `paths...` — restrict to subpaths (forwarded to `git log -- ...`).

## Workflow

1. Run from the repo root with default settings.
2. Open the SVG. Identify the 3–5 hottest (largest red) tiles.
3. For each, ask: do they have tests? Are they touched by many people, or one? Have recent bugs landed there?
4. Re-run with `--since "3 months ago"` and compare to the all-history view to spot newly-volatile areas.
5. Capture `--report` snapshots at intervals to track whether refactors actually lower churn.

## Notes

- Pure Python 3 stdlib. No `pip install`.
- Renames are normalized (`{old => new}` collapses to the new path).
- Binary files are skipped (git reports `-` for their numstat).
- Squarified treemap layout (Bruls/Huijing/van Wijk) keeps tile aspect ratios near 1.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/codebase-churn.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
