---
name: session-export
description: Export the current (or a specified) Claude Code or OpenAI Codex session to a single self-contained HTML file, including any subagent transcripts. Use when the user asks to "export this session", "save the chat as HTML", "share this conversation", or wants an offline-readable record of a coding-agent session.
license: MIT
metadata:
  author: Vincent Bruijn
  author-url: https://www.vincentbruijn.nl
---

# session-export

Produces a one-page, fully offline HTML view of a Claude Code or OpenAI Codex session — user/assistant turns, thinking/reasoning, tool calls and results, and any subagent transcripts rendered inline.

## When to invoke

- User asks to "export the current session", "save this chat", "make an HTML of this conversation".
- User wants to share a session with someone who doesn't have the CLI installed.

## How to run

Two exporters sit next to this `SKILL.md` — use the one matching the CLI you're
running in. Use that directory's path (it may be project-local or under
`~/.claude/` or `~/.codex/`, so don't hardcode a project-relative path):

```
# Claude Code
node <this-skill-dir>/export.js [session-id-or-path] [--no-redact]
# OpenAI Codex
node <this-skill-dir>/codex-export.js [session-id-or-path] [--no-redact]
```

Run from the working directory of the session you want to export. Auto-detection:

- **Claude Code** (`export.js`): newest main session jsonl under
  `<configDir>/projects/<encoded-cwd>/`, where configDir is `$CLAUDE_CONFIG_DIR`
  if set, else `~/.claude` (skips `agent-*.jsonl` siblings and empty stubs).
- **OpenAI Codex** (`codex-export.js`): newest `rollout-*.jsonl` under
  `<codexHome>/sessions/`, where codexHome is `$CODEX_HOME` if set, else `~/.codex`.

Both accept a session id or an explicit path as the argument, and `--no-redact`
to disable the secret-redaction pass (see below).

The script writes `claude-session-…` / `codex-session-…_<sessionId>.html` to the current working directory and prints the absolute path. When secrets are redacted, a one-line summary is also written to stderr.

## Secret redaction

Before the HTML is written, every message text/thinking block, every tool input (recursively), and every tool result is scanned for well-known credential shapes and matches are replaced with `[REDACTED:<kind>]`:

- `sk-ant-…` (Anthropic), `sk-…` / `sk-proj-…` (OpenAI), `sk_live_…` / `pk_live_…` / `sk_test_…` (Stripe)
- `AKIA…` / `ASIA…` / `AIDA…` (AWS access keys)
- `ghp_…` / `ghs_…` / `gho_…` / `ghu_…` / `ghr_…` (GitHub PATs)
- `xoxb-…` / `xoxp-…` / `xoxa-…` / `xoxs-…` (Slack)
- `AIza…` (Google API keys), `eyJ…eyJ….…` (JWTs)
- `-----BEGIN … PRIVATE KEY-----` blocks

Counts per kind are stored on `header.redactions` and surfaced as a yellow `redacted:<n>` chip in the exported header (hover for the breakdown). This is a heuristic pass — review your exports before sharing.

## Output

Single HTML file with:
- Embedded JSON payload (`<script id="session-data" type="application/json">`), no base64.
- Inline CSS supporting light + dark themes (16px base, em-based), respects `prefers-color-scheme`, manual toggle persisted in localStorage.
- Sidebar tree of turns with live search and filter chips.
- Collapsible thinking blocks, collapsible tool outputs.
- Subagent (Task/Agent) cards that expand to show the nested subagent transcript (loaded from sibling `agent-<id>.jsonl` files when present, falls back to inline `progress` records).
- Keyboard shortcuts: `/` focus search, `t` toggle thinking, `o` toggle tool outputs, `b` toggle sidebar, `a`/`z` expand/collapse all, `Esc` clear search, `[`/`]` navigate entries.

No network access required to view.
