---
name: token-economy
description: Milo's in-session operating discipline for maximizing useful work per token and preventing context/credit drain — the compaction-and-context-preservation practice OpenCode/Codex/Claude Code use, adapted to Town's tools. Use this WHENEVER a task involves reading large data (emails, files, session history, transcripts, web pages, MCP payloads), multi-step work, fan-out, or anything that could balloon context — before deciding what to read, what to load, whether to delegate, and how much to write back. It governs retrieval discipline, tool-loading discipline, externalized scratchpad/compaction, delegation routing, and output economy. Pairs with thread-checkpoint (WHEN to cut a thread) and finish-discipline (closing work); this one is the moment-to-moment throughput layer that runs on almost every non-trivial task.
category: How Milo works
blurb: Milo's discipline for getting the most useful work per token — what to read, what to delegate, and when to compact, so big tasks stay affordable.
example: How do you keep a huge research task from ballooning in cost?
---

# Token Economy — maximize useful work per token

Purpose: get the most done per token billed, and stop context from ballooning. This is the moment-to-moment layer OpenCode/Codex/Claude Code implement as "compaction + context preservation" — externalize state, read the minimum, hand off heavy work — expressed in Town's tools.

Optimize `throughput = useful outcome / tokens billed`. Not "spend less" (that starves the task) and not "read everything to be safe" (that drains credits). Read exactly what the decision needs, externalize the rest, and let the answer be terse.

## The mechanism you are fighting (why this matters)
- **Every byte in context is re-billed on every subsequent turn.** A big tool result read on turn 3 is paid for again on turns 4, 5, 6... A long thread re-pays for its whole history each turn. So the cost of reading something is not one-time — it compounds for the rest of the thread.
- There is **no live per-turn meter** to poll. `get_credit_usage` is a nightly, retrospective rollup. Govern by the proxy signals you can see: how much you're about to pull in, how long the thread has run, whether a compaction has already fired.
- Therefore the highest-leverage move is almost always **not loading the payload in the first place** — summarize it, page it, delegate it, or write it to a file and carry the pointer.

## Six disciplines

### 1. Retrieval discipline — read the minimum that changes the decision
- Locate before you load: `town_grep` (regex across VFS/Content Library, or over a `toolresult://` in place) to find the lines, then `town_read` only those with `offset`/`limit`. Never `town_read` a whole large file to find one section.
- Page big tool results where they live: search a truncated result with `town_grep uri:"toolresult://<id>"` or read a slice with `town_read uri:"toolresult://<id>", offset, limit` instead of copying it to the VFS first.
- Prefer tools that return pre-computed / structured answers over raw dumps you then parse (see substitution table).
- `search_emails` returns only snippets — but that means `read_email` only the one(s) you must act on, not the whole result set.
- Batch independent reads in a single turn (parallel tool calls) rather than serial round-trips; each round-trip re-bills the growing context.
- Never re-fetch data already in context.

### 2. Tool-loading discipline — this session lazy-loads tools
- Tools are not free to surface. Run the **narrow** intent tool-search for the step at hand; don't bulk-load a whole tool family "just in case."
- Reuse tools already loaded this session; don't re-run the search for them.

### 3. Externalized scratchpad — compaction, Town-style
- Working state, extracted lists, and intermediate artifacts go to a file, not into your prose. Cheap + session-scoped: `vfs:///session/files/...`. Durable + shareable: a plan/state doc or Content Library file.
- Carry the **pointer** (path / documentId), not the payload. Re-read a narrow slice when you actually need it.
- Keep a running compaction block for any long task — a dated `state now / open loops / next` — so you can resume from the file instead of re-reading the whole history. This is the same move as OpenCode summarizing a session before it grows too large.
- For any multi-session or heavy task, promote this to a permanent **runbook** (see the runbook-protocol): a per-task markdown artifact at `content://collections/milo-operations/runbooks/<task-slug>` that holds objective, dated decisions, the live `state now / open loops / next` block, an actions log, and pointers. Refer back to the runbook instead of re-reading thread scrollback (the doc does not burn credits). At task closure, push the finalized runbook to git so the record is permanent.
- When a thread is genuinely long or a milestone is hit, this hands off to the **thread-checkpoint** skill to cut losslessly.

### 4. Delegation routing — keep the orchestrator's context lean
- Push heavy, large-context, or multi-step work to a sub-agent (`delegate_to_subagent`, or a named specialist via `invoke_routine`). The child burns its own context and returns a compact result; the parent thread never eats the raw data. This is the single biggest lever for "summarize my unread inbox" / "read this transcript and pull actions" style tasks — the payload lands in the child, not here.
- Default rule: any task with a large read OR 3+ distinct steps is delegated (or routed to the box) unless it's small, single-step, or needs live back-and-forth.
- Fan-out independent items as **async** delegates and gather with `wait_for_runs`, instead of doing them sequentially in this context.
- **Heavy coding/builds go to OpenCode-on-Aetheris (the box).** It does not spend Town credits at all. Town stays orchestrator/planner; the box does the implementation. (Standing rule — see build-lane-failover / opencode-usage.)

### 5. Output economy — terse, decision-first, copy-pasteable
- Lead with the answer or the next action. No restating the request back, no long preamble, no narrating tool calls.
- Never echo a large tool output into the reply — link or point to it.
- Hand-offs to another agent/OpenCode are a copy-pasteable instruction block, not an essay.

### 6. Rework avoidance
- Sequence edits to the same file so you don't re-read between them; verify once at the end.
- Plan the read/act path before pulling data, so you don't pull twice.

## Cheaper-substitute table (prefer the left)
| Instead of | Use | Why |
| --- | --- | --- |
| `read_email` on every hit | `read_email_summary_batch` | one compact pass, not N full bodies |
| `query_session_history` (raw calls) | `query_session_summary` | AI summary, not the full event stream |
| counting auto-inbox tool calls by hand | `get_auto_inbox_activity_summary` | pre-computed counts |
| several calendar read tools | `get_calendar_context` | events + known context in one call |
| `town_read` whole large file | `town_grep` then `town_read offset/limit` | locate, then load only the slice |
| copy a big tool result to VFS to grep | `town_grep`/`town_read` on `toolresult://<id>` | search/read it in place |
| `web_fetch` a Town/Drive/Docs URL | the native tool (`read_document`, Drive tools) | authenticated, structured, no re-parse |
| reading raw data into THIS thread to summarize | `delegate_to_subagent` | payload stays in the child's context |
| heavy build/codegen in Town | OpenCode on the box | zero Town credits |

## Pre-flight (before pulling data)
1. What decision am I about to make, and what is the **minimum** I must read to make it?
2. Can a summary/batch/structured tool answer it without the raw payload?
3. Should this whole sub-task be delegated so the payload never lands here?
4. Which single narrow tool-search do I need — not a family?

## Post-flight (before replying)
1. Did anything land in context I didn't actually use? Note it so next time I don't pull it.
2. Should any working state be written to a file/pointer instead of held in prose?
3. Is the reply as short as the outcome allows?
4. Is the thread long enough or at a clean milestone that I should invoke **thread-checkpoint** and recommend a cut?

## Anti-patterns (stop doing these)
- Reading an entire file/inbox/transcript to use one paragraph of it.
- Re-fetching something already in context "to be sure."
- Bulk-loading tool families you might use later.
- Echoing large tool results back into the reply.
- Grinding a big multi-step or large-read task inside this thread when a sub-agent or the box should carry it.
- Letting a thread run for dozens of turns without checkpointing and cutting.

## Where this fits with the other skills
- **thread-checkpoint** — WHEN and HOW to cut a long thread losslessly. This skill keeps each turn cheap; that one ends the thread cheaply.
- **finish-discipline** — closing a task out completely. Token economy is about the path there being cheap.
- **build-lane-failover / opencode-usage** — the mechanics of routing heavy work to the box.
- **runbook-protocol** — the permanent, git-backed form of the externalized scratchpad for multi-session tasks.
