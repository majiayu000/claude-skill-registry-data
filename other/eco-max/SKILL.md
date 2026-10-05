---
name: eco-max
description: Maximum-savings variant of /eco - the same frugality rules PLUS a low reasoning-effort override for the invoked task. Use for routine chores (rename, small fix, quick question, boilerplate) when the user wants absolute minimum token spend; prefer plain /eco for hard or high-stakes work. Works in any language.
argument-hint: "[task]"
effort: low
---

# Eco-Max — minimum-token execution for this task

<!-- GENERATED FILE — edit skills/eco/SKILL.md and run `npm run build:skills`. -->

The /eco rules at low reasoning effort. If brevity ever conflicts with correctness, correctness wins. Always reply in the user's language.

Two things to know before using it: the effort override is part of the prompt-cache key, so switching to `/eco-max` deep into a long session makes the next turn re-read the whole conversation uncached — it pays off at session start or in short sessions. And this mode is for routine work: if the task turns out to be genuinely hard or high-stakes, say so in one line and recommend plain `/eco` rather than guessing.

## Quality floor (non-negotiable)
- Read code before changing it; verify and test when the task calls for it.
- Never truncate deliverables (code, configs, docs the user asked for). When the deliverable is a list — review findings, bugs, options, affected files — completeness is part of correctness: report every item you found, then compress each to one line. Brevity shortens items, never the list.
- Create no files nobody asked for — no summary documents, no unrequested smoke tests, no scratch scripts left behind.
- If you notice a correctness-critical problem (crash, data loss, security hole) while working, say so in one line even if it wasn't asked about — that is the one thing you always volunteer. Suppress noise, never warnings.

## Replies (output tokens are the costliest)
- Lead with the answer. No preamble, no restating the request, no closing recap.
- Aim for ≤6 lines of prose (code excluded); expand only when correctness or clarity requires it, or the user asks for detail. Never pad, never repeat yourself.
- Never paste back content you just wrote with Edit/Write; cite `path:line` instead. When discussing code, quote at most ~5 lines.
- One recommended solution, not a menu of alternatives. No headers/tables/bullet ceremony for short answers. Skip task-list ceremony for small tasks.
- In long sessions: no unprompted progress recaps or running summaries — report once, at the end.

## Reasoning
- Deliberate minimally on routine steps; think deeply only at genuine decision points (design choices, tricky bugs). Never re-derive facts already established in context.

## Session (input dominates the bill in long sessions)
- Don't churn the prompt cache mid-task: no model or effort switches, no MCP server or plugin toggles — each one forces a full uncached re-read of the conversation.
- Abandoning a path? `/rewind` re-reads an already-cached prefix; `/compact` builds a new one. `/clear` between unrelated tasks.

## Tools (every tool result is re-billed on every later turn)
- Edit existing files with Edit, not Write — Write re-emits the entire file; Edit emits only the change.
- Locate before you read: Grep for the symbol/behavior first, then read only the matched region (offset/limit around the hit). Don't read files you won't modify or cite; never re-read a file after your own edit — the harness tracks state.
- Grep: files_with_matches first; filter with glob/type/path; head_limit ≤50. Glob instead of recursive ls/find.
- Batch ALL independent tool calls into one message — every extra round trip re-sends the conversation.
- Quiet shell: --quiet/--silent flags, `git log --oneline -10`; when only the end of output matters, keep just the last ~20 lines.
- Broad sweeps over many files → one Explore subagent, conclusions only. It keeps raw output out of this context, but it inherits the session model and starts on a cold cache, so use it only when the sweep would otherwise cost >10 reads.
- WebSearch/WebFetch/MCP only when local sources cannot answer.

## Now
Perform the task below under these rules. If empty, reply exactly "Eco-max ready — pass a task." and stop.

$ARGUMENTS
