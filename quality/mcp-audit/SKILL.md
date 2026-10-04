---
name: mcp-audit
description: 'Read-only diagnostic that scans Claude Code session transcripts to surface which MCP servers and tools you actually use, ranked by call frequency, with zero-use servers flagged for removal. Use when planning an MCP cleanup, evaluating whether to keep a newly-added server, deciding which servers warrant token cost in the catalog, or before authoring an MCP-removal PR. Outputs a markdown report (last N days) — does not modify any settings. Pair with the manual `claude mcp remove <name>` step once findings are reviewed.'
triggers:
  - mcp audit
  - which mcp servers do I use
  - audit mcp usage
  - find unused mcp
  - mcp cleanup
  - mcp removal candidates
---

# mcp-audit

Read-only inventory of MCP-server tool usage from Claude Code session transcripts.

## When to run

- Before removing an MCP server (confirm zero use)
- Periodic cleanup (suggest monthly via `plugin-audit` cron)
- After adding a server, ~2 weeks in (validate it's earning its catalog spot)

## How

```
bash ~/.claude/skills/mcp-audit/audit.sh [days]
```

`days` defaults to 30. Scans `~/.claude/projects/*/*.jsonl` for `mcp__<server>__<tool>` invocations within the window, prints:

1. **By server**: count of tool calls per server, sorted desc
2. **By tool**: top 20 individual tools by call count
3. **Zero-use servers**: connected MCP servers (from `claude mcp list`) with no calls in window
4. **Single-use servers**: warning band (used 1–3 times — possibly tested-and-forgotten)

## Output

Plain markdown to stdout. No mutations. No settings touched. Pipe to a file if you want history:

```
bash ~/.claude/skills/mcp-audit/audit.sh > ~/.claude/plans/mcp-audit-$(date +%Y-%m-%d).md
```

## Acting on results

- Zero-use server, ≥30 days connected → strong remove candidate. Confirm with `claude mcp remove <name> -s user`.
- Single-use server, recent → leave in place (maybe newly added).
- High-use server with low-quality tools → consider whether to disable specific tools rather than the whole server.

## Limits

- Counts tool *invocations*, not tokens or wall time. A single `gh issue create` call may be more valuable than 100 `playwright_snapshot` calls.
- Doesn't see deferred tools that were never `ToolSearch`-loaded. If a server's tools are lazy and never reached, it shows as zero-use even if relevant.
- Doesn't infer intent — a server may be unused because the workflow it supports hasn't come up recently, not because it's redundant.
