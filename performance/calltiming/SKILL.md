---
name: callTiming
description: Find where a log call spends its time from stored timings, never a guess (rule 165). Every MCP tool call and terminal run has a call id and stores each stage as a span in log.db; `timing` reports p50, p95 and p99 per tool and per stage, and `timing` { call } shows one call as a waterfall. Use when the owner asks why something is slow, whether we hit p99 or p95, or before and after any change made to speed something up.
---

# callTiming

## The loop

1. **Read the numbers first.** Run `timing` (MCP), or `timing { tool, hours }` for one tool. Note the tool's p50, p95 and p99, and the stages with the largest share.
2. **Open a slow call.** Take a call id from a `■` line in the live log, or pick a slow call, and run `timing { call }`. The waterfall shows which stage took the time.
3. **Name the cause from the span.**
   - `python.start` or `python.imports`: the cost of starting Python for each call.
   - `host.connect` with `started=true`: the account's session host was started cold.
   - `host.queue` or `account.lock`: another call held the account.
   - `spacing` or `governor`: pacing, which is there on purpose.
   - `inbox.waitCaughtUp`: the account was behind.
   - `voice.*` or `fetch …`: SubQ, Jina or Twenty.
   - `http …`: the platform itself.
   - `unaccounted`: our own code with no span yet. Add one.
4. **Go deeper only when a span can't explain it.** Run `py-spy record --native --pid <host pid>` on the Python host, or `bun --cpu-prof` on Bun, to see which function and library the time is in.
5. **Fix, then measure again.** Run the same `timing` report after the change and give the owner both numbers. Never call something faster without them.

## Hard boundaries

- Timing never changes what a call sends. A span holds no cookie, token or message text.
- Pacing (`spacing`, `governor`) protects the accounts. It is never cut to win a benchmark unless the owner says so.
- Commands go through the MCP (rule 163). `timing` is read-only.

Docs: `docs/callTiming.md`. Spec: `docs/specs/callTiming.md`.
