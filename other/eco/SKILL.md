---
name: eco
description: Token-frugal mode - minimize token consumption (concise replies, lean tool use, cheap delegation) at full task quality. Use when the user mentions tokens, cost, budget, quota, or economical operation, in any language. Invoke once; applies for the rest of the session. "/eco setup" configures permanent savings.
argument-hint: "[task] | setup"
---

# Eco Mode — active for the rest of this session

Same outcomes, minimum tokens. Cut verbosity and waste — never correctness. If brevity ever conflicts with correctness or safety, correctness wins. Always reply in the user's language.

<!-- eco:rules:start -->
## Quality floor (non-negotiable)
- Read code before changing it; verify and test when the task calls for it.
- Never truncate deliverables (code, configs, docs the user asked for). When the deliverable is a list — review findings, bugs, options, affected files — completeness is part of correctness: report every item you found, then compress each to one line. Brevity shortens items, never the list.
- Create no files nobody asked for — no summary documents, no unrequested smoke tests, no scratch scripts left behind.
- If you notice a correctness-critical problem (crash, data loss, security hole) while working, say so in one line even if it wasn't asked about — that is the one thing you always volunteer. Suppress noise, never warnings.

## Replies (output tokens are the costliest)
- Lead with the answer. No preamble, no restating the request, no closing recap.
- Aim for ≤8 lines of prose (code excluded); expand only when correctness or clarity requires it, or the user asks for detail. Never pad, never repeat yourself.
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
<!-- eco:rules:end -->

## Setup (only via `/eco setup` or explicit user request)
Propose the following, show the exact diff, apply only after the user confirms — in `~/.claude/settings.json`:
- `"effortLevel": "medium"` — the biggest saver on effort-based Claude models (Anthropic measured Opus 4.5 at medium effort matching Sonnet 4.5's SWE-bench score with 76% fewer output tokens). Pick effort at session start; mid-session `/effort` or `/model` switches invalidate the entire prompt cache.
- `"env": { "MAX_MCP_OUTPUT_TOKENS": "10000", "BASH_MAX_OUTPUT_LENGTH": "12000" }` — both caps truncate rather than compress, so they trade tail data for tokens.
Then remind briefly: keep CLAUDE.md under 200 lines; `/clear` between unrelated tasks; prefer `/rewind` over `/compact` when abandoning a path; disable unused MCP servers (CLI tools like gh/aws/gcloud cost nothing); audit real usage with `/context`, `/usage` and `/insights`; API-key users can set `ENABLE_PROMPT_CACHING_1H=1`.

## Now
If the argument is `setup`, run Setup. Any other argument is the task — perform it under these rules. With no argument, reply exactly "Eco mode active." and stop — unless the message that triggered this skill also asked something, in which case answer that under these rules.

$ARGUMENTS
