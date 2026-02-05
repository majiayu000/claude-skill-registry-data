---
name: github-insights
description: |
  Provides team GitHub activity insights including merged PRs, contributor
  leaderboards, merge velocity, review participation, and PR size analysis.
  Use when users ask about team productivity, who merged PRs, code contribution
  stats, review patterns, or developer activity.
---

# GitHub Insights Skill

Analyze team GitHub activity for the current repository.

## Available Actions

| Action | Description |
|--------|-------------|
| `prs-merged` | List all PRs merged in a time period |
| `leaderboard` | Rank contributors by PR count and lines changed |
| `activity` | Summary stats + leaderboard + day/hour breakdown |
| `time-to-merge` | Merge velocity per developer (avg/median) |
| `reviews` | Who reviews whose code |
| `pr-size` | Size distribution and bottleneck detection |
| `first-review` | Time to first review per developer |
| `review-balance` | Reviews given vs received ratio |
| `reverts` | Track reverts and hotfixes |
| `review-depth` | Detect rubber stamp reviews |
| `review-cycles` | Rounds of feedback before merge |
| `all` | Run all reports with visual separators |

## Usage

Run the script from the skill's scripts directory:

```bash
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action <ACTION> [OPTIONS]
```

### Options

- `--action` (required): One of the actions above
- `--days N`: Look back N days (default: 30)
- `--start YYYY-MM-DD`: Start date for custom range
- `--no-stats`: Skip line count fetching (faster for large repos)

### Examples

```bash
# PRs merged in last 30 days
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action prs-merged

# Leaderboard for last week
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action leaderboard --days 7

# Time to merge analysis
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action time-to-merge --days 30

# Review participation
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action reviews --days 30

# PR size analysis with bottleneck detection
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action pr-size --days 30

# Time to first review
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action first-review --days 30

# Review balance (given vs received)
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action review-balance --days 30

# Reverts and hotfixes tracking
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action reverts --days 30

# Rubber stamp detection
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action review-depth --days 30

# Review cycles (rounds of feedback)
python {baseDir}/skills/github-insights/scripts/gh_stats.py --action review-cycles --days 30
```

## Interpreting User Requests

| User Says | Action | Options |
|-----------|--------|---------|
| "show PRs merged" | `prs-merged` | default 30 days |
| "who merged the most PRs" | `leaderboard` | - |
| "team activity last week" | `activity` | `--days 7` |
| "how long do PRs take to merge" | `time-to-merge` | - |
| "who is reviewing code" | `reviews` | - |
| "are big PRs slowing us down" | `pr-size` | - |
| "PR bottlenecks" | `pr-size` | - |
| "how long until first review" | `first-review` | - |
| "is review load balanced" | `review-balance` | - |
| "any reverts or hotfixes" | `reverts` | - |
| "are reviews thorough" | `review-depth` | - |
| "rubber stamp reviews" | `review-depth` | - |
| "how many review rounds" | `review-cycles` | - |
| "run all reports" | `all` | - |
| "full team analysis" | `all` | - |

## Output

The script outputs markdown tables ready for display. No additional formatting needed.

## Prerequisites

- Must be run from within a git repository
- Requires `gh` CLI authenticated (`gh auth status`)
