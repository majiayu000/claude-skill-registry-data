---
name: history-search
description: "Use when you need to recall past work - before saying I don't know, what did we decide about X, has anyone seen this error, last time we, do you remember, why did we choose Z, how did we fix this before, what did agent X say or do about Y, search the history of one agent, a group of agents or every agent on the box. Dispatches the cheap history-search sub-agent over thrum transcript search and returns a short cited answer or NOT FOUND."
---

# Recalling Past Work Across Agent History

Ask a cheap sub-agent instead of searching yourself: it runs several full-text queries, reads the best windows
and returns a short answer with citations, so raw transcript never enters your context. The search is
box-local and needs a Pro licence. Syntax and flags: the `transcript-search` skill.

## When

- Before saying you do not know something that may have come up before.
- A decision, cause, fix, flag or error from earlier work: "what did we decide about X", "has anyone seen this
  error", "last time we", "how did we fix this".
- What an agent, a group of agents or anyone on the box said or did about a topic.

Not for the current code (read it) or anything already in this conversation.

## How

Plugin agents (Claude, Cursor): dispatch the `history-search` agent with the question and a scope: one agent,
`a,b`, a worktree, or all. Pin nothing; the agent carries its own tier.

Runtimes without plugin agents: spawn your cheapest-tier agent, pinned explicitly per
`choosing-subagent-models`, with `resources/search-prompt.md` from this skill's folder as its instructions
plus the question and scope. If you cannot spawn, run that procedure yourself within its budget.

## The answer

`ANSWER`, `SOURCES` (agent, date, `runtime:session:seq`), `CONFIDENCE` (found, partial, not found) and
`QUERIES TRIED`. Open a source with `thrum transcript show <runtime>:<session>:<seq>` to verify a detail you
will act on.

- `NOT FOUND in <scope>`: nothing relevant is recorded. Do not guess.
- `NOT ON THIS BOX: <agent> is on <host>; ask <coordinator>`: transcripts are searched per box. Send the
  question to that coordinator with `thrum send`; the sub-agent never messages.
- `UNAVAILABLE: <error>`: the box is not licensed or the index is not ready. Tell the user and stop.
