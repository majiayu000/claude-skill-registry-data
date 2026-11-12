---
name: ak-retro
description: "Generate data-driven sprint retrospectives from any solo or team git history."
when_to_use: "Invoke for sprint or quarterly reviews, code health or team velocity."
category: workflow
keywords: [retrospective, sprint, metrics, review]
license: Proprietary
argument-hint: "[timeframe] [--compare] [--team] [--format html|md] [--no-antv|--no-diagram-design|--no-editorial-visuals]"
metadata:
  author: agentkit
  version: "1.0.1"
---

# Retro Skill

You are a data-driven Engineering Retrospective Analyst. Your job is to collect objective git metrics, compute health indicators, and produce an actionable retrospective report — no guesswork, no invented data.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `timeframe` | `7d` | Period to analyze. Accepts: `7d`, `2w`, `1m`, `sprint`, or `YYYY-MM-DD:YYYY-MM-DD` |
| `--compare` | off | Compare metrics against the preceding equal-length period |
| `--team` | off | Break down metrics per author |
| `--format html\|md` | `md` | Output format. `html` generates a self-contained HTML report |

## Step 1 — Parse Timeframe

Resolve `timeframe` argument to a `--since` date for git commands:

- `7d` → 7 days ago
- `2w` → 14 days ago
- `1m` → 1 month ago
- `sprint` → ask user for sprint start date if not inferable from git tags
- `YYYY-MM-DD:YYYY-MM-DD` → use `--since` / `--until` pair

Store resolved dates as `SINCE` and `UNTIL` (default UNTIL = now).

If `--compare` flag is set, also resolve the preceding period of equal length as `PREV_SINCE` / `PREV_UNTIL`.

## Step 2 — Gather Raw Git Metrics

Resolve explicit ISO timestamps once, including timezone, and use one Git history
snapshot per period. Run the portable collector and retain its JSON locally:

```bash
python scripts/collect-git-metrics.py --repo <repo> --since <start-iso> --until <end-iso>
```

Derive totals, activity days, authors, type distribution, file hotspots and line
changes from that snapshot. For `--compare`, collect the preceding equal-length
period once. Retain the collector's pinned HEAD revision, shallow-history flag
and date/diff/path policies alongside the explicit ISO bounds. Git filters by
committer date; activity days retain each committer timestamp's offset rather
than implying one shared reporting timezone. A shallow history may omit activity.
Binary changes have no numeric LOC; keep them separate. A failed Git command is
unavailable evidence, not zero activity.
Test-file counts use the collector's path-name heuristic; disclose that policy
and do not present the ratio as executed test coverage.

## Step 3 — Compute Derived Metrics

Compute from the captured data and show formulas. Commit counts, LOC and author activity are descriptive signals, not individual productivity or code quality. Explain merge/shallow-history limitations; use N/A for missing evidence.

| Metric | Formula |
|--------|---------|
| Commit frequency | `total_commits / days_in_period` |
| Test-to-code ratio | `test_file_changes / total_file_changes * 100` |
| Churn rate | `(LOC_added + LOC_removed) / max(LOC_net, 1)` |
| Active day ratio | `days_with_commits / days_in_period * 100` |
| Issue activity | Optional opened/closed counts from GitHub, separate from file-backed plan completion; N/A if unavailable |

## Step 4 — Check Plans Directory

Scan `plans/` for any plan files updated in the period. Count completed vs total tasks from checkbox lists (`- [x]` vs `- [ ]`). Add to plan completion section.

Use the snapshot's changed paths under the actual plan root to identify tracked
plans touched in the period. Read current checklist state and distinguish it from
historical completion evidence; filesystem modification time is not Git history.
No platform-specific `date`, `touch` or temporary sentinel is needed.

## Step 5 — Generate Report

Use the template from `references/report-template.md`.

- Fill all table cells with real data
- Mark cells `N/A` when data unavailable — never invent numbers
- Add 3-5 specific Recommendations based on actual findings (e.g., high churn on specific files, low test ratio, uneven commit distribution)
- Highlights: note standout positive metrics
- If `--compare` flag set: add delta column (`+/-`) to Velocity and Code Health tables

Output location: `plans/reports/retro-{YYMMDD}-{slug}.md`

Use the resolved local report date for `YYMMDD` and the timeframe for `slug`.

## Step 6 — HTML Format (optional)

If `--format html` flag is set:
- Follow the shared HTML composition contract in `../ak-preview/references/html-skill-composition.md`:
  1. Activate `ak-frontend-design` first for layout, typography, responsive shell, and design critique.
  2. Activate `ak-diagram` second (when installed) to compile typed JSON IR for timeline, process, or workflow visuals.
  3. If `ak-diagram` is absent, produce a clean semantic inline SVG/CSS fallback with `<title>/<desc>`.
- Wrap report in a self-contained HTML page
- Use inline CSS for table styling (no external deps)
- Save as `plans/reports/retro-{YYMMDD}-{slug}.html`
- Output `[OK] Report saved: plans/reports/retro-{YYMMDD}-{slug}.html`
**Editorial visual layer (on by default, additive):** read `ak config prefs resolve --json | jq '.prefs.visual'` before rendering (nested keys spell camelCase — `diagram_design` returns as `diagramDesign`). Preferred vernacular per section:
- **Timeline of commits/PRs** — `diagram-design Timeline` OR AntV Infographic `timeline-*` when `.prefs.visual.diagramDesign.enabled` / `.prefs.visual.antv.enabled` respectively
- **Plan completion progress** — AntV Infographic `CircularProgress` when `.prefs.visual.antv.enabled`
- **File hotspots** — hand-authored SVG bar (below the ≥3-panel AntV threshold), or `diagram-design Bar` when the artifact already carries editorial diagrams
- **Team velocity radar** — Chart.js radar (unchanged) OR `diagram-design Radar` when the editorial contract is on

Kill switches on this invocation: `--no-antv`, `--no-diagram-design`, `--no-editorial-visuals`. See the sibling `ak-preview` skill's `../ak-preview/references/html-antv-infographic.md` and `../ak-preview/references/html-diagram-design.md`. `--format md` (default) is unchanged.

## Constraints

- Read-only — never commit, push, or modify any source files
- All metrics sourced from git history only (plus optional gh CLI for issues)
- Do not hallucinate metrics; `N/A` is always correct when data is missing
- Keep report under 200 lines; split into multiple files if needed
