---
name: check-agent-logs
description: Search past Claude Code, Codex, Droid, OpenCode, and Pi session logs to recover context from earlier work across the current project and sibling checkouts. Use when a bug, topic, or decision was handled in a previous session but its agent or checkout is unknown; when the user says "we fixed/discussed this before", "find the session where", "recover prior context", "check agent logs", "check Claude projects", "search past sessions/transcripts", or "which checkout was that in". Do not use for aggregate failure-pattern analysis; use review-logs for that.
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Check Agent Logs

Recover prior context by searching stored agent transcripts, reading the relevant
session, and continuing from its diagnosis or decision.

## Instructions

### 1. Choose a query and agents

Use a distinctive regex such as an error string, symbol, ticket ID, or unusual
phrase. With no agent selector, the script searches all agents. Selectors compose:

```bash
python3 scripts/search_agent_logs.py "QUERY" [--claude] [--codex] [--droid] [--opencode] [--pi] [--current] [--all]
```

- `--current` selects the harness running the skill.
- `--all` and no selector both select all five agents.
- `--scope siblings` is the default project scope. `--scope current` searches
  only the current checkout; `--scope all` searches every recorded project.
- `--app NAME` searches session cwd values containing `NAME` and overrides scope.
- `--days N` limits the search to recently updated sessions.
- **`--kind message` is the highest-value filter.** Every entry is classified as
  `message` (what was said), `tool` (calls and their output), or `meta`
  (reasoning and summaries). Tool traffic dominates raw match counts — a real
  session here matched 5117 times, of which 4668 were tool output — so search
  conversation first and widen to `--kind tool` only when hunting a command or
  a stack trace.
- Results are ranked by weighted score (`message` 3, `meta` 2, `tool` 1, title 5),
  highest first. `--sort recent` restores newest-first ordering.
- `--format json` emits the same results as a machine-readable document; prefer it
  when a script or another agent consumes the output rather than a human.

Run `--help` for case, snippet, cwd, and result-limit controls.

### 2. Read the candidate

Results are newest-first and include a stable ref, title, cwd, branch when known,
timestamps, source, and snippets. Read the most likely session:

```bash
python3 scripts/search_agent_logs.py --read AGENT:SESSION_ID [--mode lite|full|log]
```

`--mode lite` is the default and prints conversation only; `full` adds reasoning
and summaries, `log` adds all tool traffic. Sessions reach hundreds of thousands
of characters, so reads are capped at `--max-chars` (200000 by default) and report
what they withheld:

```
… truncated: 50000 of 374819 chars from offset 0. Continue with --offset 50000,
  or --mode log for tool traffic.
```

Continue with the reported `--offset` rather than re-reading, and stay in `lite`
unless the answer is genuinely in the tool output — `log` was 4.8x larger than
`lite` on the same session.

Read more than one when attribution is ambiguous. Trust the printed `cwd` over
encoded storage paths. Transcripts can contain secrets or PII; use them as
context without repeating sensitive values to the user or writing them elsewhere.

### 3. Apply the recovered context

Continue the task using the prior diagnosis, fix, or decision. Cite the session's
agent, title, and date when summarizing what was recovered.

### 4. Widen only as needed

If nothing matches, try an alternate query, remove `--days`, use `--app NAME`,
then use `--scope all`. Do not make an aggregate claim when the script reports an
incomplete search because an agent source was unavailable.

## Examples

### Find a regression without knowing the agent

User: "The KeyboardShortcut crash is back; didn't we fix it before?"

1. Run `python3 scripts/search_agent_logs.py "KeyboardShortcut" --app juggler`.
2. Read the best hit with `--read codex:019...`.
3. Apply the recovered fix and cite that session.

### Search only the invoking harness

User: "Find the session where this agent discussed the schema migration."

Run `python3 scripts/search_agent_logs.py "schema migration" --current --scope all`.

## Troubleshooting

### `--current` cannot identify the harness

Run through the repository's normal agent wrapper, which sets `AGENT_HARNESS`, or
replace `--current` with an explicit agent selector.

### A provider is unavailable

Use another selector only if the user intends a narrower search. An all-agent
search reports missing stores as incomplete; do not treat an empty result as proof
that the context never existed.

### Results are noisy

Use a more distinctive query, `--days N`, or `--app NAME`. The current session may
match because it contains the user's search phrase; prefer an older result whose
title and snippets describe the actual prior work.
