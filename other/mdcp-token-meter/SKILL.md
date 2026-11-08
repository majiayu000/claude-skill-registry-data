---
name: mdcp-token-meter
description: Show how much of the session's context and tokens have been used. Use when the user asks "token meter", "how much session is used", "context usage", "how many tokens", or wants a usage readout in the status line (Claude Code).
---

# Token meter

Reads the session transcript and reports real API usage numbers: context in use now, output tokens, fresh input, cache writes and cache reads, number of API calls.

## Run it
```bash
python3 "$(find ~/.claude -name token-meter.py -path '*scripts*' | head -1)"
```
Options: `--window N` (context window to compare against; env `MDCP_CONTEXT_WINDOW`), `--json`, a transcript path as the last argument.

Show the user the output as printed, then one sentence: how full the context is and whether to compact or start a new session (suggest this above about 70%).

## Always-on status line (Claude Code)
Add to `~/.claude/settings.json` (use the real path to `scripts/token-meter.py`):
```json
{ "statusLine": { "type": "command", "command": "python3 /path/to/token-meter.py --statusline" } }
```
Shows e.g. `ctx 285.7k/1000.0k (28.6%) | out 45.2k | 37 calls`.

## Limits to tell the user
- Works from Claude Code's local transcript. It does not see claude.ai web chats.
- The context window size is not in the transcript. The default is 200k; if usage already exceeds it, 1M is assumed. Set `--window` to be exact.
- This is session context, not plan quota. Quota is shown by `/usage` in Claude Code or Settings > Usage on claude.ai.
- Cache reads repeat the same context each call, so they are large; they are not new text.
