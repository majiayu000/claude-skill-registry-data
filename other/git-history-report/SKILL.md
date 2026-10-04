---
name: git-history-report
description: 'Build one standalone HTML commit-history dashboard for one or several project working trees. It exports each repo with git log, aggregates by day, week, type, scope, weekday, hour, author and project, and writes one data.json plus a self-contained dashboard.html with in-page project, type and date filters, a contributor leaderboard, and a light/dark toggle. It also writes a regenerated analysis.generated.md and one hand-editable analysis.notes.<project>.md per project (created once, never overwritten). With no path it reports the current project into <project>/docs/git_history_dashboard/; several paths require --out-dir and produce one combined report. Use when the user asks for a git-history report or a commit dashboard across one or more repos.'
user-invocable: true
argument-hint: 'Give the repo paths and an output folder, for example "git-history-report ../alpha ../beta --out-dir /tmp/report". With no path it reports the current project; several paths require --out-dir. Pass --no-open to keep the browser shut.'
---

[Instruction](../../../instructions/git-history-report.md)

Implementation is mutualized across the shared directories:

- [`../instructions/git-history-report.md`](../../../instructions/git-history-report.md)
  — the full resolve-targets, build, and keep-the-notes workflow.
- [`../tools/git_history_dashboard/build.py`](../../../tools/git_history_dashboard/build.py)
  — the entry point; delegates to `cli.py` for target resolution and the run loop.
- [`../tools/git_history_dashboard/README.md`](../../../tools/git_history_dashboard/README.md)
  — the tool reference: flags, output files, and what the dashboard shows.

Inputs: zero, one, or several repo paths, an optional `--out-dir` (required for a
multi-project run), and an optional `--no-open`. The skill resolves the targets,
runs `build.py`, and follows the analysis workflow: `analysis.generated.md` is
rewritten from the figures on every run, while each `analysis.notes.<project>.md`
is created once and then left for hand editing — a rebuild never overwrites it.
The rendered `dashboard.html` and `data.json` are versioned in the output folder;
`git_history.csv` is a git-ignored scratch export.
