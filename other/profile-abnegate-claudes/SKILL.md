---
name: profile
description: Build a comprehensive developer profile from git activity and Claude Code session history. Covers commit patterns, velocity, streaks, time-of-day habits, repo focus, tool usage, AI spend, model preferences, and session themes. Use whenever the user asks about their stats, coding patterns, what they've been working on, their Claude usage, or anything related to their developer profile.
---

# Developer Profile

Build a comprehensive developer profile by combining git commit activity with Claude Code session data. The result paints a full picture: what you build, when you build it, how you use AI assistance, and where your focus goes.

## How it works

A collection script at `scripts/collect.py` in the plugin root scans git repos for commit metadata and reads the Claude Code session files of every profile. It outputs a single JSON payload with two top-level sections: `git` and `claude`. It needs Python 3.9 or later and nothing outside the standard library.

- **Commits**: the window starts at local midnight on the `--since` day, and each commit is dated by its author date, so rebased commits keep their original day. A commit is counted once across clones (by hash) and once within a repository (by author email, author date and subject, which drops rebased copies). Stashes are not commits. Repositories that share a directory name are counted together.
- **Profiles**: `~/.claude`, every `~/.claude-*` directory and `$CLAUDE_CONFIG_DIR`, each only when it has a `projects/` directory, deduplicated by physical path. `--config-dir PATH` (repeatable, `~` expanded) scans only the given directories instead, and warns on stderr about any without `projects/`. `claude.profiles_scanned` always lists the profiles read; when the window has no sessions it is the only `claude` key.
- **Copied sessions**: profiles often hold copies of the same session file. Copies are grouped by their path relative to `projects/`. The largest copy is read, plus any copy of a different size (a session resumed in another profile), and `user`/`assistant` entries are unioned by `uuid`, so every message counts once. Copies last modified before `--since` are skipped.
- **Titles**: a session's title is its last `custom-title` entry; when copies disagree, the largest copy wins.
- **Local time**: every date, hour, weekday and week in both sections is in the machine's local time zone, so git and Claude patterns line up.

## Step 1: Collect the data

The script is `<skill base dir>/../../scripts/collect.py`, where the skill base directory is the one printed when this skill loads.

Run it on `~/Local/` unless the user names another directory. The script auto-detects the git author and defaults to the last 90 days, which takes about 30 seconds; give wider `--since` ranges a longer Bash timeout.

```bash
python3 <skill base dir>/../../scripts/collect.py ~/Local/ --format json
```

Override if the user asks for a different time range, author or profile. `--since` takes an ISO date such as `2025-01-01` (relative dates like `3 months ago` are rejected):

```bash
python3 <skill base dir>/../../scripts/collect.py ~/Local/ --since 2025-01-01 --author 'Someone Else' --config-dir ~/.claude-work
```

## Step 2: Interpret and present

The JSON output has two top-level keys: `git` and `claude`. Use **both** to build a unified profile. Cross-reference them — the most interesting insights come from correlating the two (e.g., "You use Claude most heavily on the repos where you commit the most fixes" or "Your Claude sessions peak at 22:00, exactly when your commit volume spikes").

### Git section (`git`)

#### Summary
- Total commits, active repos, date range, commits per day
- Weekend vs weekday split — surface this if skewed
- Busiest single day — call it out with context

#### Streaks
- Current streak and longest streak
- If the current streak is strong, celebrate it. If it broke recently, note when.

#### Repo breakdown (`by_repo`)
- Rank by commit volume. Group into tiers: heavy focus, moderate, light touch.
- Call out repos that appeared suddenly (new projects) or went silent.

#### Weekly/monthly trends (`by_week`, `by_month`)
- Spot acceleration or deceleration. Which weeks were peak output?
- Correlate spikes with specific repos using `by_repo_week`.

#### Time-of-day patterns (`by_hour`, `by_time_bucket`)
- Early bird or night owl?
- Distinct work sessions (morning burst, evening push)?
- Use `by_repo_hour` to see if different repos get worked on at different times.

#### Day-of-week patterns (`by_day_of_week`)
- Which days are heaviest? Weekend work?
- Surprising gaps?

#### Commit types (`by_type`)
- Features vs fixes vs refactors vs chores?
- Use `by_repo_type` to show how work type varies by project.

#### Vocabulary (`top_words`)
- Domain themes from commit messages.

#### Repo context (`repo_context`)
Every repository with commits in the window has an entry, including a clone whose commits all count toward an earlier clone, so `repo_context` can name repositories that `by_repo` leaves out.
- **branch**: Current branch name — reveals active work.
- **recent_subjects**: Last 20 commit subjects — summarize themes in plain language.
- **uncommitted**: modified, added, deleted, renamed and untracked paths — hints at active WIP.

### Claude section (`claude`)

Automated runs are sessions started through the Agent SDK that have no typed prompt: their main entries carry `entrypoint` `sdk-py`, `sdk-ts` or `sdk-cli` (the CLI run non-interactively, as with `claude -p`), which is how scripts and pipelines drive Claude Code. They count toward the cost keys (`total_cost_usd`, `cost_by_model`, `unpriced_models` and `cost_by_week`) and are summarised in `automated_sessions`. Every other key, from `total_sessions` to `top_session_words`, covers interactive sessions only.

#### Summary
- Total sessions, **estimated cost** (pay-as-you-go rates, not actual spend on flat-rate plans — note this when presenting). `total_cost_usd` includes automated runs; `average_cost_per_session` is per interactive session.
- Total turns, average turns per session. A turn is a prompt typed into a main session; tool results, meta and compact-summary entries, harness messages (task notifications, command output, CI events, interrupt markers), prompts sent to subagents and prompts a program sends through the Agent SDK (`promptSource` is `sdk` and `origin.kind` isn't `human`) don't count.
- Total tool calls, average tools per session
- Active days and sessions per active day. With only automated runs in the window, `total_sessions` is 0 and `date_range` is null.

#### Automated runs (`automated_sessions`)
- `sessions` counts the automated runs and `cost` is their share of `total_cost_usd`.
- When there are any, report them on one line of their own (how many runs, what they cost, their share of spend) and keep them out of the habits you describe.

#### Cost by model (`cost_by_model`, `unpriced_models`)
Costs use the list prices from the pricing page (`PRICING_SOURCE` in the script):
- Cache writes are billed at the 5-minute or 1-hour rate from the `cache_creation` breakdown; without a breakdown, all `cache_creation_input_tokens` are billed at the 5-minute rate.
- Fast mode (`usage.speed` is `fast`) uses the fast rates for Opus 5.5, Opus 5 and Opus 4.8. US-only inference (`usage.inference_geo` is `us`) costs 1.1×.
- Claude Code writes one entry per content block of an API response, and only the last one carries the final `usage`; earlier ones hold a running output count and no `speed`. So each response is priced once per `message.id` (the entry's `uuid` when there is none), from its entry with the most output tokens (the later one on a tie) across every copy read, while message counts stay per entry.
- `cost_by_model` maps each canonical model (such as `claude-opus-5-5`, with `[1m]` and date suffixes stripped) to USD, most expensive first.
- `unpriced_models` maps each model without a known price, by raw name, to its assistant-message count. Such models are never priced as another model, so a non-empty map means the total understates spend — say so.
- `<synthetic>` costs nothing and appears in neither.

#### Duration (`duration`)
- Median, average, and max active minutes per interactive session. Active time adds up the gaps between a session's entries, subagents included, and counts any gap longer than 15 minutes as 15, so a session left open or resumed days later only counts the time it was in use.
- `total_hours`: wall-clock active time across interactive sessions, so parallel sessions count once.

#### Data sources (`data_sources`)
Each session is tagged with how its data survived:
- **main+subagent** — both parent session file and subagent data present (recent sessions)
- **main-only** — only the parent session file
- **subagent-only** — parent was cleaned up by Claude Code's retention, only subagent data survived

A high `subagent-only` count for older periods (Jan–Feb 2026 and earlier) is **expected** — Claude Code silently cleans up older `projects/*.jsonl` files but leaves `subagents/` subdirs alone. For periods before the subagent feature started persisting (~Jan 9, 2026), neither survives, which is why you may see gaps in Nov–Dec 2025 even though `history.jsonl` has entries for that range.

If the user asks about gaps in the timeline, explain this cleanup behavior. Don't pretend the gap is because they weren't using Claude — they were, the data just got purged.

#### Models (`models`)
- Which models are used and how often. Is the user an Opus user, a Sonnet user, or do they switch based on context?
- `<synthetic>` entries are Claude Code's internal messages (hooks, system events) — not real API calls. Note their share but don't attribute cost to them.

#### Tool usage (`tools`)
- Ranked tool counts. Which tools dominate (Bash, Read, Edit, Grep, Glob, Agent, etc.)?
- High Bash usage suggests scripting-heavy workflows; high Agent usage suggests delegation patterns; high Edit vs Write suggests iterative refinement.

#### Skills (`skills`)
- Which slash commands / skills are invoked. Shows workflow preferences.

#### By project (`by_project`)
- Sessions, cost, turns, and tool calls per project, named after the session's working directory. A session in a worktree under `<repo>/.claude/worktrees/` counts toward `<repo>`.
- Cross-reference with git `by_repo` — which repos get the most AI assistance relative to their commit volume? A repo with many commits but few Claude sessions is "manual" work; one with few commits but many sessions is "AI-assisted" or exploratory.

#### By project hour (`by_project_hour`)
- Do different projects get Claude help at different times? Covers the 10 projects with the most sessions.

#### Hourly / daily / weekly patterns (`by_hour`, `by_day_of_week`, `by_week`)
- Compare with git patterns. Do Claude sessions happen at the same hours as commits, or different?
- Claude-heavy weeks vs commit-heavy weeks — do they correlate or alternate?

#### Cost trends (`cost_by_week`)
- Spending trajectory. Increasing, stable, or decreasing?
- Correlate spikes with specific projects or high-commit weeks. Automated runs are in these totals but not in `by_project`.

#### Session vocabulary (`top_session_words`)
- What themes emerge from session titles? Domain terms, action words.
- Compare with git commit vocabulary — are the same themes present, or does Claude get used for different work than what gets committed?

## Presentation guidelines

Lead with 3-5 bold headline insights. The best insights **cross-reference** git and Claude data:
- "You spent $X on Claude this month, mostly on [project] — which is also your highest-commit repo"
- "Your Claude sessions peak at 1am but your commits peak at 10pm — you research late, commit earlier"
- "You use Opus for [project] but Sonnet for [project] — the complex backend gets the big model"
- "[Project] has 3x more Claude sessions per commit than any other repo — heavy AI assistance there"

Spend figures include automated runs, while session, project and timing figures are interactive only, so when a headline pairs spend with sessions or projects, say how much of the spend was automated.

After the headlines, present two detailed sections (Git Activity, Claude Usage) with tables and plain language analysis. Then a combined "Cross-reference" section that ties the two together.

If the user asks for CSV output, run the script with `--format csv` instead — this outputs the git repo-weekly grid only, one row per ISO week such as `2026-W53`.

Keep it concrete. Reference specific repos, weeks, numbers, and dollar amounts. Avoid filler.
