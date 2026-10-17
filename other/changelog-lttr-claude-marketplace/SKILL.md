---
name: changelog
description: Show recent Claude Code changes personalized to user's setup. Trigger when user asks about changelog, "what's new", "cc changelog", "claude code updates", "recent changes", or wants to know what changed in Claude Code.
disable-model-invocation: true
allowed-tools: Bash(deno:*)
---

# CC Changelog

Show recent Claude Code changes, scored by relevance to the user's installed skills, commands, plugins, hooks, and usage patterns.

## Prerequisites

- `deno`
- `gh`, authenticated (`gh auth login`)

## Workflow

1. Run the data collection script:

```bash
deno run --allow-run --allow-env --allow-read --allow-net ${CLAUDE_SKILL_DIR}/scripts/cc-changelog.ts 2>/dev/null
```

To force a date-based lookback (ignoring lastVersion state), pass `--lookback-days=N`:

```bash
deno run --allow-run --allow-env --allow-read --allow-net ${CLAUDE_SKILL_DIR}/scripts/cc-changelog.ts --lookback-days=14 2>/dev/null
```

Use `--lookback-days` when the user asks for changes from a specific time period (e.g. "last 14 days", "last week" = 7 days).

2. Parse the JSON output and present a **concise, themed** summary:

### Format rules

- **Hard cap: 10 bullets.** The whole report is a flat, ranked list of at most 10 items — no matter how many candidates the script returns. A window with 200 entries still gets 10 bullets. Never scale the count to the input size; "there was a lot this week" is not a reason to print more. Score each candidate by combined weight (high → low):
  1. Personal relevance — matches user's installed skills, commands, plugins, hooks, usage patterns
  2. User-facing surface changes — visible message/UI text, prompts, output format, defaults the user reads or types
  3. Parameter / flag / config / API / schema changes — anything the user invokes or configures (CLI flags, settings keys, hook events, tool schemas, command args)
  4. New features / capabilities — net-new things user can do
  5. Behavioral changes — different output for same input, removed/changed defaults, breaking changes
  6. Internal / perf / refactor — deprioritize unless user-observable. A perf win that doesn't change behavior or UX ranks low.
     Sort by this combined score and keep only the top 10.
- **Drop cosmetic items and routine bug fixes entirely** (before ranking). Skip typo/wording tweaks, UI polish, and fixes for bugs the user never hit. Include a bug fix only with strong evidence it affects the user — e.g. their CLAUDE.md/settings/hooks mention a workaround for it, or it breaks a feature they demonstrably use.
- **Drop what the user's settings rule out.** Check `userContext.settings` first: a disabled feature (e.g. `disableRemoteControl`) means every item about it scores zero. Same for other platforms — Windows, VS Code, self-hosted runner, unused git hosts.
- **Merge near-duplicates into one bullet.** Several fixes to the same surface (permission dialogs, MCP connections, TUI redraw) are one line, not one line each. Lead with the strongest and fold the rest in, or drop them.
- **No duplicates.** Each item appears exactly once. Before finishing, reread the output and remove any repeated bullet.
- **Flat list, no theme headings.** At 10 bullets, grouping is overhead — rank hardest-hitting first and let the list run.
- **Each item = 1 short line.** Rewrite verbose changelog entries into punchy summaries (5-15 words). Append version+date tag: `(2.1.47, Feb 18)`
- **Lead with a 1-2 sentence TL;DR** of the most impactful changes for this user.
- **Explain WHY it's relevant** by referencing what the user uses. Don't just say "matches: Bash" - say things like "you use hooks" or "affects your StatusLine setup".
- **Offer the rest, don't print it.** Close with one line giving the skipped count and noting you can show the second tier on request. Produce that second tier only if the user actually asks — and cap it at 15 bullets too.

```
## Claude Code changelog - {version range} ({date range})

{1-2 sentence TL;DR of biggest changes relevant to user}

- {Punchy summary} (2.1.47, Feb 18) — {why it matters to you}
- ...
- {at most 10 bullets total}

**System prompt:** {1-3 sentences — see rules below}

{N} lower-ranked items skipped — ask if you want the second tier. [Full changelog]({url})
```

3. If the `versions` array is empty, say: "You're up to date! No new changes since {currentVersion}." Do NOT advance the watermark.

4. **After presenting results to the user**, advance the watermark so the same changes aren't shown again:

```bash
deno run --allow-run --allow-env --allow-read --allow-write ${CLAUDE_SKILL_DIR}/scripts/cc-changelog-advance.ts 2>/dev/null
```

Only run this AFTER the changelog summary is fully rendered. Never run it if the versions array was empty.

### System prompt diff rules

When `systemPromptDiff.prompt` or `systemPromptDiff.flags` is non-null, summarize the unified diff in **at most 3 bullets** (or a single sentence when nothing meaningful changed — say so plainly and move on; a diff of duplicated boilerplate stanzas is not a change). Categorize changes:

**Prompt changes** - summarize each meaningful hunk as one bullet:

- New sections/blocks added (e.g. "New `currentDate` context block added")
- Instructions changed (e.g. "Auto memory guidelines expanded with what to/not to save")
- Tool schema changes (e.g. "AskUserQuestion got `markdown` preview field")
- Model/version bumps (e.g. "Knowledge cutoff Jan 2025 -> Aug 2025")
- Removed content (e.g. "Agent Teams 'not available' disclaimer removed")

**Flag changes** - list added/removed flags:

- Added: `flag_name`
- Removed: `flag_name`

Skip cosmetic changes (typo fixes, whitespace, path changes in test environments). Focus on behavioral changes that affect how Claude works.

## Notes

- The script handles all data fetching, parsing, and relevance scoring
- State is persisted at `~/.claude/custom-cache/cc-changelog-state.json`
- First run uses a 14-day lookback window; subsequent runs check from last version
- Requires `gh` CLI authenticated with GitHub
