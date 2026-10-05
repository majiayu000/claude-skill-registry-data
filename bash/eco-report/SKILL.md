---
name: eco-report
description: Show where the tokens actually went - per-session output, thinking, input and cache accounting read from this machine's Claude Code transcripts. Use when the user asks what they spent, which sessions were expensive, how their prompt cache is doing, or whether /eco is helping. Works in any language.
argument-hint: "[--days <n>] [--limit <n>] [--json]"
allowed-tools: Bash(node "${CLAUDE_PLUGIN_ROOT}/scripts/report.mjs" *), Bash(node *report.mjs *)
---

# Eco Report - measured token accounting

Every number comes from the local JSONL transcript store. Read them; never estimate them.

## Run it

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/report.mjs"
```

If `${CLAUDE_PLUGIN_ROOT}` did not expand (personal or project install rather than a plugin), run
`report.mjs` from this skill's own directory - the installer stages it there - and fall back to
`scripts/report.mjs` in the claude-code-eco checkout.

Pass the user's arguments straight through:

- `--days <n>` window, default 7, `0` for all history
- `--limit <n>` session rows to print (totals always cover every session)
- `--dir <path>` a transcript store other than `$CLAUDE_CONFIG_DIR/projects`
- `--json` machine-readable output

## Present it

- The script's table is already on screen as the command's output. **Do not reprint it** - it is a finished report, and repeating it burns tokens on something the user is already looking at. Do not re-format
  it, re-order it, re-tally it, or drop lines to save space.
- Then add at most three lines of your own: the biggest cost driver visible in the table and one
  concrete action (for example a session with a high out/turn, or a cache write/read ratio above
  ~0.3, which means the prompt prefix keeps being rebuilt).
- Keep the "Observational, NOT a controlled A/B" disclaimer. The eco-armed vs not gap is not a
  measured saving - the user chose when to run `/eco`, so difficulty is a confound. State it as a
  correlation or not at all; the controlled numbers live in `benchmarks/results.md`.
- Never quote a cost in currency. Transcripts record tokens, not prices. If asked for money, say the
  price is not in the data and point at the published rates for the models listed.
- `turns` are API requests, deduped by `requestId`; `thinking` is a subset of `output`, not an
  addition to it. Say so if the user reads the columns as additive.
- On "No sessions ...", the window is simply empty: offer `--days 0`. Do not go hunting through
  other files.

This skill only reads. It never edits transcripts, settings, or project files.
