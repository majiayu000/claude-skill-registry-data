---
name: standup
description: |
  Generates a morning standup from Claude Code conversation history for the
  current project. Use this skill whenever the user asks for a "standup",
  "morning standup", "daily standup", "EOD notes", "status update", "yesterday's
  progress", "what did I do yesterday", "what did I work on last week", "weekly
  recap", "summarize my CC work", or any variant. Default window is yesterday;
  also accepts a specific date, an interval, or last N days. Pulls activity
  from ~/.claude/projects for the current working directory, reconciles against
  the past week of standups (carrying forward unresolved questions and
  blockers), and produces 3 to 5 polished corporate-style bullets that read
  human, not AI. Saves the result to `.standups/YYYY-MM-DD.md` and ensures
  `.standups/` is in `.gitignore`. Never emits em dashes or AI-tell vocabulary.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Standup generator

Pulls Claude Code activity for the current project, reconciles it with the past week of standups, and writes a corporate-grade morning standup that does not read like AI generated it.

## When to run

Trigger phrases (not exhaustive): standup, morning standup, daily standup, EOD notes, weekly recap, "what did I do yesterday", "summarize my last week", "status update for the team".

If the user gives no window, default to **yesterday**. If they say "last week", interpret as the last 7 calendar days inclusive of today. If they give a specific date or range, honor it.

## Pipeline (run in order)

### 1. Collect raw activity

Run the collection script from the user's current working directory. Pass exactly one window flag.

```bash
python3 ~/.claude/skills/standup/scripts/collect.py [WINDOW_FLAGS]
```

Window flag mapping:

- "yesterday" / no window given → `--yesterday`
- "today" → `--today`
- specific date like "2026-04-30" or "April 30" → `--day 2026-04-30`
- "last 3 days" / "past week" → `--last N` (week = 7)
- "from X to Y" → `--from YYYY-MM-DD --to YYYY-MM-DD`

The script prints structured markdown with sessions and turns. Read the output. If it prints "No conversations found", stop and tell the user, do not fabricate activity.

### 2. Read prior standups for carry-forward

```bash
ls -1 .standups/ 2>/dev/null | sort | tail -n 7
```

For each of the last up to 7 standup files in `.standups/`, read it and extract:

- Items under `## Open questions` or `## Pending` or `## Blockers`
- Anything tagged "carrying from" or "still open"

Hold these as **candidate carry-forwards**. The script output from step 1 will tell you which ones got resolved (look for explicit closure signals: PR merged, decision made, question answered) and which are still hanging. Be conservative. If a question was open yesterday and today's activity does not mention it, assume it is still open and carry it forward with the original date stamp.

### 3. Synthesize bullets

Produce **3 to 5 bullets total**, not more. Mix of these slots, in this priority order:

1. **Shipped** (yesterday's most material delivery, the headline)
2. **In flight** (today's planned focus, only if obvious from the conversation)
3. **Blocker / open question** (the thing the team needs to know)
4. **Decision or alignment** (only if a real decision was made or sought)
5. **Risk flagged** (only if something concrete needs attention)

Use the corporate bluff vocabulary at `references/corporate-bluff.md` for translation. The point of the bluff is **defensible vagueness**, not lying. Every bullet must map back to something that actually happened in the JSONL. If a bullet cannot be defended in a question from a manager, drop it.

### 4. Anti-AI pass (mandatory)

Before writing the file, scrub the bullets for AI tells. The full rule set lives at `references/anti-ai-rules.md`. The non-negotiables:

- **Zero em dashes (—)**. None. Use a comma, a period, or a regular dash with spaces.
- **Zero "—" character anywhere in the output**, including in lists or section breaks.
- **No "delve", "leverage", "robust", "seamless", "comprehensive", "ensure", "facilitate", "in the realm of", "in today's fast-paced", "it's worth noting", "moreover", "furthermore"**.
- **No "rule of three" parallels** (e.g. "fast, scalable, and reliable"). Pick one.
- **No "not just X but Y" constructions**.
- **No -ing summary clauses at the end of a bullet** ("...landing the migration, paving the way for...").
- **No vague attributions** ("studies show", "experts agree", "best practices suggest").
- **No bold-italic emphasis on emotionally loaded words** for drama.

If a bullet violates any of the above, rewrite it. Do a second pass if needed.

### 5. Build the output file

Use the template at `references/template.md`. Fill in:

- Date header (the **end** of the window, or "today" if today)
- The 3-5 bullets
- A short "Carrying forward" section if any items survived from prior standups
- A short "Resolved this cycle" section if today's activity closed any prior open items
- An "Open questions" section listing what is still unresolved as of this standup

### 6. Write and gitignore

Write to `.standups/YYYY-MM-DD.md` where the date is the standup's effective date.

- If `.standups/` does not exist, create it.
- Check `.gitignore`. If `.standups/` is not listed, append it on its own line. If `.gitignore` does not exist, create it with `.standups/` as the first line.
- Do not commit anything. The user controls git.

After writing, print the bullets to chat in plain text so the user can copy-paste into Slack or wherever, with **no markdown formatting** (no `-`, no `*`, no bullets), one item per line. Most standup channels render markdown poorly; raw lines paste cleanly.

## Hard rules

- **Never invent activity.** If yesterday had no real progress, say so. The user's preference is direct over polished.
- **Never use em dashes anywhere.** This is a global ban for this skill, including in carry-forward sections, in chat output, and in file content.
- **Never write "AI-flavored" qualifiers** like "leveraging", "thoughtfully", "carefully crafted", "elegant solution".
- **Always run the collection script.** Do not synthesize from memory of the conversation, even if you remember it. The JSONL is the source of truth.
- **Never write a standup file longer than 30 lines.** Standups are not reports.
- **Never reformat or edit prior standup files.** They are append-only history.

## What good looks like

A bullet that is good:

> Landed the HMM regime detector OOS backtest at 14.1% CAGR. Numbers held under the 2014-2026 window. Moving the options layer spec to v3.0 today.

A bullet that is bad (AI-flavored, vague, em dash, rule of three):

> Successfully delivered a robust, scalable, and reliable HMM regime detection system — a critical milestone enabling the next phase of our journey.

If the output reads like the second one, redo it.
