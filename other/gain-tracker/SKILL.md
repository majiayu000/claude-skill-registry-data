---
name: gain-tracker
description: Track daily git productivity or broader output gains against a historical baseline and a target multiplier, then turn the numbers into a gain scorecard or reminder story. Use when Codex needs to measure current pace, compare it to an older baseline like 2013, credit the systems driving the lift such as GStack, and keep momentum visible day to day.
---

# Gain Tracker

Use this skill when the user wants to quantify an improvement arc and keep it emotionally visible instead of letting the gains blur together.

Default product shape: a compact but premium macOS `MenuBarExtra` utility with a live daily pulse, a motivating reminder story, baseline comparison, and exportable scorecards.

## Quick Start

1. Define one stable output metric before comparing time periods.
2. Start with `bash scripts/run_gain_tracker.sh doctor` to confirm Python, git, `gh`, config state, and the current repo context.
3. Use `bash scripts/run_gain_tracker.sh status` to check saved GitHub identity and tracked repos without making network changes.
4. If GitHub is available, connect once with `bash scripts/run_gain_tracker.sh connect --track-cwd` or `bash scripts/run_gain_tracker.sh connect --repo "/path/to/repo"`.
5. If you want to pick up several repos at once, run `bash scripts/run_gain_tracker.sh track-dir --dir "~/Desktop" --max-depth 2`.
6. If a repo is available, prefer git-backed measurement first.
7. Capture the baseline total and the number of days in that baseline period.
8. Capture the current total, the current time window, and the target multiplier.
9. Use `bash scripts/run_gain_tracker.sh daily` for a daily repo pulse and reminder story, `bash scripts/run_gain_tracker.sh compare` for baseline-versus-current comparisons, or `bash scripts/run_gain_tracker.sh math` for manual totals.
10. Run `bash scripts/run_gain_tracker.sh validate` after changing the helper scripts.
11. Produce either a `daily-gain-story` or a `gain-scorecard`, depending on whether the user wants a daily motivational check-in or a broader baseline comparison.

## Accepted Inputs

- a baseline period such as 2013 output totals and the number of days those totals cover
- a current period such as the last 30, 80, or 90 days of output and the number of days in that window
- a target multiplier such as `10x`, `25x`, or `90x`
- a repo path and date windows when the user wants git-backed measurement
- a workspace folder when the user wants the skill to discover and track multiple local repos at once
- a connected GitHub account through `gh` when the user wants saved identity and tracked repos
- the metric definition, such as git commits, lines changed, files changed, active days, merged PRs, features delivered, or a weighted output score
- notes on what changed, such as GStack, tooling upgrades, workflow changes, or team support
- optional checkpoints over time so the gain curve can be tracked, not just a single before and after
- whether the output should feel like a scorecard, a daily reminder story, or both

## Output Artifact

Primary artifacts:
- `gain-scorecard`
- `daily-gain-story`

Default `gain-scorecard` sections:
- Metric definition and comparison rules
- Baseline period versus current period
- Current multiplier, goal progress, and pace delta
- Systems driving the gain, such as GStack or workflow changes
- Next checkpoint, confidence notes, and what to keep stable

Default `daily-gain-story` sections:
- Today's work at a glance
- Seven-day and thirty-day momentum
- Commit or churn highlights
- Why today still matters in the longer climb
- One short reminder that pushes the user back toward focused work

## Workflow

### Normalize The Comparison

- Use one metric definition across both time windows.
- Convert totals into daily or weekly rates before computing a multiplier.
- Flag missing context when the baseline and current periods are not actually comparable.

### Prefer Repo-Backed Mode

- If the user wants the tool to remember who they are and what repos matter, start with `bash scripts/run_gain_tracker.sh status` or `bash scripts/run_gain_tracker.sh connect`.
- If the user has a git repo, start with `bash scripts/run_gain_tracker.sh compare`.
- If the user wants a daily snapshot or motivation loop, start with `bash scripts/run_gain_tracker.sh daily`.
- Treat `commits` as the default productivity metric only when the user explicitly wants commit productivity.
- Offer `lines-changed`, `files-changed`, or `active-days` when commit counts alone feel too noisy.
- Keep author filtering explicit when the repo has multiple contributors.

### Connect GitHub

- Use `bash scripts/run_gain_tracker.sh connect --repo "/path/to/repo"` to detect the logged-in GitHub identity from `gh`, capture the default git author info, and save tracked repos under `~/.codex/gain-tracker/config.json`.
- Use `bash scripts/run_gain_tracker.sh track-dir --dir "~/Desktop" --max-depth 2` to scan a common workspace root and automatically track GitHub repos found inside it.
- Use `bash scripts/run_gain_tracker.sh status` to confirm the connected account and tracked repos.
- After connection, `scripts/daily_git_story.py` can run without `--repo` and aggregate all tracked repos automatically.
- After connection, `scripts/git_gain.py` can default to the current repo or first tracked repo and use the saved author filter.
- When a scanned folder includes non-GitHub repos or empty directories, keep the skips visible instead of silently pretending they were added.

### Calculate The Gain

- Start with `bash scripts/run_gain_tracker.sh math` when the user has numeric totals and day counts.
- Start with `bash scripts/run_gain_tracker.sh compare` when the user wants the comparison grounded in commit history.
- Start with `bash scripts/run_gain_tracker.sh daily` when the user wants a today-focused check-in with trend context.
- Report current multiplier, rate delta, target progress, and remaining gap to the goal.
- Keep the math visible enough that the user can trust the result.

### Build The Artifact

- Turn the math into a short scorecard, not just a raw number dump.
- Credit the systems and habits that appear to be responsible for the lift.
- Call out if the gain seems real but the metric is still too noisy to treat as a hard KPI.
- When writing the daily story, stay grounded in actual stats first and use motivation second.
- Use a reminder tone that feels proud, specific, and steady rather than hype-heavy or guilt-heavy.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Connect`
  - `Scan Folder`
  - `Today`
  - `Story`
  - `Compare`
- Keep `Trend` and `Export` as secondary actions in the footer or history window instead of top-level primary tabs.
- Keep the popover between 340 pt and 390 pt wide with today's headline stat and reminder story visible above the fold.
- Use an optional history window for checkpoints, notes, exports, and trend comparisons.
- The first glance should answer:
  - am I connected
  - what did I do today
  - how strong is the recent streak
  - why should I keep going today

### Safety Boundaries

- Do not treat output as a proxy for human worth.
- Avoid advice that pushes unsafe schedules, burnout, or deceptive metric inflation.
- Do not fabricate historical baselines or overstate causality from a single tool change.
- If the metric definition changed over time, say so clearly before presenting the multiplier as settled.
- Remind the user that commit count is a proxy, not a complete measure of real value shipped.

## Example Prompts

- `Use $gain-tracker to compare my coding output from 2013 to my last 80 days, calculate my current multiplier, and show progress toward a 90x goal.`
- `Use $gain-tracker to turn these baseline and current output totals into a gain scorecard, and note that GStack is the main system behind the lift.`
- `Use $gain-tracker to compare my git commit productivity in this repo against my 2013 baseline and show how far I am toward 90x.`
- `Use $gain-tracker to read this repo, tell me what code I shipped today from commits and file churn, and write a short reminder story that keeps me productive.`
- `Use $gain-tracker to connect to my GitHub account, track my repos automatically, and give me a daily reminder story from my actual git activity.`
- `Use $gain-tracker to scan my workspace folder for GitHub repos, track them, and give me one combined daily story across everything I touched today.`

## Resources

- `scripts/run_gain_tracker.sh`: repo-native doctor, status, connect, compare, daily-story, math, and validation entrypoint.
- `scripts/github_connect.py`: connect through `gh`, save the GitHub identity, and manage tracked repos.
- `scripts/daily_git_story.py`: summarize today's git work, recent momentum, and a motivating reminder story.
- `scripts/git_gain.py`: compare two git windows by commits, lines changed, files changed, or active days.
- `scripts/gain_math.py`: deterministic multiplier, pace, and goal-progress calculator.
- `scripts/tracker_config.py`: shared config helpers for saved identity and tracked repos.
- `references/product-spec.md`: menu bar product shape, artifact template, first-run UX, and icon direction.
