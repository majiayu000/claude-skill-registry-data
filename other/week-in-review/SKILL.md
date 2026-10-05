---
name: week-in-review
description: End-of-week reflection report. Mines your Claude Code transcripts from the last 7 days to produce a self-contained HTML file with (1) the topics/areas you explored, (2) distilled key learnings with live-searched further-reading links, and (3) a token/command/skill/ctx-stack usage summary. Use when the user says "week in review", "weekly review", "what did I learn this week", "my week", or runs /week-in-review.
---

# Week in Review

A Friday ritual: you stayed *in the flow* all week — this skill surfaces what you
were curious about so you can learn/deep-dive later, and shows how you spent your
tokens, commands, skills, and ctx-stack usage.

Three deterministic scripts + one synthesis subagent. Do NOT reimplement the
parsing by hand — the scripts already handle the Claude Code transcript format,
cache-token accounting, and harness-wrapper stripping.

## Paths (resolve these first)
```bash
# Where this skill is installed. Global install (default):
SKILL=~/.claude/skills/week-in-review
# ...or if installed as a PROJECT skill, use: SKILL="$(git rev-parse --show-toplevel)/.claude/skills/week-in-review"

# Where reports go. Override with WEEK_IN_REVIEW_OUT to point into a repo you sync/commit.
DAY=$(date +%F); OUT="${WEEK_IN_REVIEW_OUT:-$HOME/week-in-review}/$DAY"; mkdir -p "$OUT"
```

## Inputs / defaults
- **Window:** defaults to **this week** (since Monday). Pick the flag that matches what the user asked for:
  - `--last-week` — the previous calendar week
  - `--days N` — a rolling last-N-days window ("the last 10 days")
  - `--since YYYY-MM-DD [--until YYYY-MM-DD]` — a specific date range or a named past week (omit `--until` for "since X until now"; a bare `--until` date counts through end of that day)
  - `--week-start sun` — treat the week as Sunday-started (applies to this-week / last-week)
  - When targeting a past range, name the output dir after it (e.g. `.../week-in-review/2026-07-20_to_2026-07-26/`) instead of today.
- **Scope:** all projects under `~/.claude/projects` (override: `--project-filter <substr>`).
- **Output:** `$OUT/report.html` — a self-contained, theme-aware HTML file (its header shows the window it covers).

## Steps

### 1. Collect the deterministic stats
```bash
python3 "$SKILL/scripts/collect.py" --out "$OUT/week-data.json"   # default: this week
# past week / range examples:
#   python3 "$SKILL/scripts/collect.py" --last-week --out "$OUT/week-data.json"
#   python3 "$SKILL/scripts/collect.py" --since 2026-07-20 --until 2026-07-26 --out "$OUT/week-data.json"
```
This prints a summary and writes `week-data.json` (token usage by model, slash
commands, skills, ctx-stack subcommands, tools, projects, and your cleaned typed
prompts). Read the printed summary so you know roughly what the week held.

### 2. Synthesise learning areas (subagent, live web search)
Spawn ONE subagent to do the clustering + link-finding — this is a search/clustering
task, not frontier reasoning, so a mid-tier model (e.g. Sonnet) is the right call;
don't burn the top session model on it. Give it this brief, substituting the real
`$OUT` path:

> Read `$OUT/week-data.json`. The `prompts` array is a week of the user's real
> typed prompts to Claude Code across their projects. Your job:
> 1. Cluster them into **3–8 coherent "learning areas"** — topics the user asked
>    about, explored, or seemed curious about. Ignore pure command/glue noise;
>    focus on things worth learning more about later.
> 2. For each area write: a `title`, a one-line `why_it_came_up`, and 2–4
>    concise `key_learnings` bullets (what someone would take away).
> 3. For each area, run **web searches** to find 1–3 current, authoritative
>    `links` (official docs, canonical references, high-quality articles).
>    Prefer primary sources. Only include links whose URL you actually saw in
>    search results — never invent URLs.
> 4. Also produce a short `week_summary` (1–2 sentences) and a `curiosities`
>    list: things the user flagged wanting to explore later.
>
> Write the result to `$OUT/learnings.json` with exactly this schema:
> `{ "week_summary": str, "areas": [ { "title": str, "why_it_came_up": str,
>   "key_learnings": [str], "links": [ {"title": str, "url": str} ] } ],
>   "curiosities": [str] }`
> Output only valid JSON to the file. Confirm the path when done.

If the subagent cannot search (offline), it should still cluster and distil,
omitting links — the report degrades gracefully.

### 3. Render the HTML report
```bash
python3 "$SKILL/scripts/render.py" \
  --data "$OUT/week-data.json" --learnings "$OUT/learnings.json" --out "$OUT/report.html"
```
`render.py` is defensive: if `learnings.json` is missing or partial it still
renders the usage dashboard plus a raw-prompt fallback, so always run it.

### 4. Hand off
Tell the user the path (`$OUT/report.html`) — a self-contained, theme-aware file
they can open in any browser — with a one-line highlight from the summary.

## Guardrails
- The report quotes your prompts — treat it as personal. By default it lives
  outside any repo; don't publish it to an external/hosted service unless asked.
- Token totals are dominated by `cache_read` (context re-served from cache) — the
  report deliberately separates fresh Output/Input from cache reads so the
  numbers aren't misleading. Don't "correct" this by summing everything.
- "ctx-stack usage" refers to the `ctx` CLI from the AI Codebase Semantics
  toolkit; on machines without it that section is simply empty.
