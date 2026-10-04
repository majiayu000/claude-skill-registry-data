---
name: git-weekly-report
description: Use when summarizing git commit history into a structured daily or weekly work report.
---

# Git Weekly Report

## Overview

Extract git commit logs and generate a structured daily or weekly report. The output groups recent work into completed items, in-progress work, highlights, plans, and risks so commit history can be reused for standups, daily reports, weekly reports, or project summaries.

## When to Use

Use this skill when the user asks for:
- Generating a weekly report or daily report from git commits
- Summarizing yesterday's or today's git activity
- Summarizing recent git activity across one or more repositories
- Reviewing what work was done over a date range
- Compiling commit history into a categorized report
- Preparing a daily standup summary from commits

## Do not use

Do not use this skill for:
- Code review of specific changes (use code-reviewer instead)
- Inspecting a single commit in detail
- Git operations other than log extraction (branching, merging, etc.)
- Non-git-related report generation

## Instructions

1. Determine the date range and report type:
   - **Daily report**: if user says "yesterday", "today", or "daily report", default `--since` to yesterday and `--until` to today.
   - **Weekly report**: if user says "this week" or "weekly report", default `--since` to last Monday and `--until` to today.
   - Otherwise: default to last 7 days. Accept user overrides.
2. Determine the author filter if the user specifies one. Default: all authors.
3. Determine repository path(s). Default: current working directory. If the user mentions multiple projects, collect all paths.
4. Run the script:

```bash
python3 scripts/git_weekly_report.py --since <YYYY-MM-DD> --until <YYYY-MM-DD> [--author <name>] [--repo <path1> <path2> ...]
```

5. Read the JSON output. The script provides structured commit data grouped by repository.
6. Use [weekly-report-format.md](references/weekly-report-format.md) as the categorization guide to classify commits by type.
7. Use [weekly-report-template.md](assets/templates/weekly-report-template.md) as the output structure when generating the final report.
8. For "next-week plans" and "risks" sections: ask the user if they have items to add, since these are not derivable from git logs. For daily reports, omit these sections unless the user requests them.
9. Present the final Markdown report. Save to a file if the user requests it.

## Script Usage

```bash
# Default: last 7 days, current directory
python3 scripts/git_weekly_report.py

# Specific date range
python3 scripts/git_weekly_report.py --since 2026-04-21 --until 2026-04-28

# With author filter
python3 scripts/git_weekly_report.py --since 2026-04-21 --author "Yang"

# Multiple repositories
python3 scripts/git_weekly_report.py --since 2026-04-21 --repo /path/to/project-a /path/to/project-b

# Save output to file
python3 scripts/git_weekly_report.py --since 2026-04-21 --output /tmp/weekly.json

# Include merge commits
python3 scripts/git_weekly_report.py --since 2026-04-21 --merges
```

## JSON Output Structure

The script outputs JSON with this structure:

- `date_range`: `{ since, until }` — the queried date range
- `author_filter`: string or null — applied author filter
- `repositories`: array of `{ path, name, commit_count, commits }`
- `total_commits`: total across all repositories

Each commit has: `hash`, `short_hash`, `author`, `date`, `subject`, `body`, `refs`.

## Report Generation

When commits exceed 50 per repository, summarize by category rather than listing every commit individually. Always preserve short hashes for traceability.

For the "In Progress" section, look for signals like: WIP, TODO, partial implementations, or incomplete feature branches.

For the "Highlights" section, identify: breaking changes, security fixes, major features, or commits touching critical paths.
