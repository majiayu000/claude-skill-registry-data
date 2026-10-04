---
name: context-audit
description: Post-hoc token-waste audit of a Claude Code session transcript. Scans a .jsonl session log for bloated tool outputs, redundant Reads, Read-after-Edit, cat/head/tail via Bash, repeated Grep/Glob, raw WebFetch, verbose Agent dispatches, and long Bash output. Emits a ranked markdown report with estimated tokens wasted per pattern; optionally emits hookify-style rule seeds to prevent recurrence. Use when the user asks "what could've been smaller", "audit this chat for token waste", "where did context go", "analyze a transcript for context savings", or runs /context-audit.
---

# Context Audit

Audit a Claude Code session transcript for context-spend patterns. Report only — does not modify settings.

## When to invoke

User asks any of:

- "audit this chat for token/context waste"
- "what could have been smaller"
- "analyze a session for context savings"
- "where did context go"
- "show me wasted context in <session>"

## How to run

Self-contained Python 3 analyzer at `scripts/audit.py` (stdlib only).

```bash
# default: newest jsonl under ~/.claude/projects/
python3 ~/.claude/skills/context-audit/scripts/audit.py

# specific transcript file
python3 ~/.claude/skills/context-audit/scripts/audit.py --file /path/to/session.jsonl

# by session id
python3 ~/.claude/skills/context-audit/scripts/audit.py --session <session-id>

# also emit hookify-style rule seeds
python3 ~/.claude/skills/context-audit/scripts/audit.py --file <path> --emit-rules

# tune thresholds
python3 ~/.claude/skills/context-audit/scripts/audit.py --file <path> --threshold-bytes 6000 --top 15
```

Resolution order for transcript path:
1. `--file <path>`
2. `--session <id>` → glob under `~/.claude/projects/**`
3. fallback: newest `.jsonl` under `~/.claude/projects/`

## Output shape

Markdown to stdout:

1. Overview (transcript, tool-call count, user/assistant chars, estimated total waste in tokens)
2. Findings table (pattern, count, est tokens, suggested swap)
3. Exemplars (one per pattern, with turn index + file/command)
4. (Optional with `--emit-rules`) Hookify-style YAML rule seeds

Token estimate uses `bytes // 4` — conservative approximation.

## Patterns detected

| Pattern | Default trigger | Suggested swap |
|---|---|---|
| Bloated tool outputs | Read/Bash/Grep/Glob/WebFetch result ≥4000 bytes | `ctx_execute_file` / `ctx_batch_execute` |
| cat/head/tail via Bash | `cat\|head\|tail\|sed\|awk` in Bash command | `Read` (one-shot) or `ctx_execute` (processing) |
| Redundant Reads | Same `file_path` Read >1× with no intervening Edit/Write | Cache in scratch / skip |
| Read after Edit | Read of file just Edited/Written | Trust harness file-state tracking |
| Repeated Grep/Glob | Identical signature within 20-call window | Batch into one broader search |
| Raw WebFetch | `WebFetch` result ≥2000 bytes | `ctx_fetch_and_index` + `ctx_search` |
| Verbose Agent dispatch | Agent/Task `prompt` ≥4000 chars | Pass bundled file paths; brief, don't re-summarize |
| Long Bash output | Bash result ≥4000 bytes | `ctx_execute(language='shell', ...)` |

Detailed pattern catalog (including rationale and false-positive notes): see `references/patterns.md`.

## Hookify rule emission

When `--emit-rules` is set, the report appends a `## Hookify rule seeds` section with YAML stubs that follow the hookify rule shape (id, trigger, match, guidance, observed_count, est_tokens_saved).

These are **seeds**, not finished rules — the user reviews, adjusts the `match` expression to fit hookify's DSL, then feeds to `/hookify:hookify` or `/hookify:writing-rules`.

See `references/hookify-rules.md` for the full mapping from audit-pattern → hookify rule template.

## After running

Present the report verbatim to the user. Highlight:

- Total estimated waste in tokens.
- Top 1-3 patterns by tokens-saved (highest-leverage targets).
- Whether `--emit-rules` would be useful (yes if top patterns look like they recur).

Do not auto-install hooks. Rule seeds are advisory; user must approve before wiring them into `~/.claude/settings.json` via `/hookify:configure` or `update-config`.

## Limitations

- Token estimate is byte-based; real Anthropic tokenization may differ ±15%.
- "Redundant Read" flags same `file_path`. Different `offset`/`limit` reads of the same file still flagged — filter manually if intentional.
- "Bloated tool output" doesn't know whether the bytes were *used* — a 10k Read may be necessary. Findings are candidates, not verdicts.
- Subagent transcripts (under `subagents/`) analyzed in isolation. To audit parent + children, run script on each and sum.
