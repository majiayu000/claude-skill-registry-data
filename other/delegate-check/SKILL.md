---
name: delegate-check
description: Pre-flight before spawning a sub-agent or any task involving >5 file reads / >3 greps. Forces the "conclusion-only?" test and requires an explicit output contract (goal, allowed tools, return-format). Use before invoking the Agent tool, before exploratory codebase audits, or when about to do many sequential reads to answer a single question.
---

# Delegate-check

Before spawning a sub-agent, answer one question out loud:

> **Will I need this tool output again (raw file contents, full grep results), or just the conclusion?**

- "Just the conclusion" → delegate. The subagent burns its own context window; the main thread stays planning-clean.
- "Raw output" → do it yourself. The subagent's summary will strip exactly what you need to keep.

## Output contract (required for every Agent invocation)

A vague handoff produces a dumping-ground report that re-pollutes the main context, defeating the whole point. State three fields explicitly in the prompt:

1. **Goal** — one sentence. What single question does the agent answer?
2. **Allowed tools** — minimum tool set. Restrict explicitly. Examples:
   - "Read, Grep, Glob only. No Bash, no Edit, no Write."
   - "WebSearch + WebFetch only. No file tools."
3. **Return format** — what the last message must contain, with explicit *do-nots*:
   - "List of file paths, one per line. Do not return raw code or excerpts."
   - "Top 3 candidates, one-line trade-off each, ≤200 words total. No prose narration of process."
   - "Pass/fail verdict + 3 specific findings. No 'observations' section."

## Parallel sub-agents — the two-humans test

Spawn parallel subagents only if you would give the same tasks to two humans without them needing to talk first:
- 3+ independent tasks
- No shared mutable state
- Clear file / area / topic boundaries

If any of those fails, run sequentially. Parallelism without independence causes race conditions, duplicate edits, and stale reads.

## When NOT to delegate

- **Self-reflection** ("what did I just do?", "what should I do next?") — introspect in main context. Spawning for this is a documented failure mode.
- **Decisions you must make** — the subagent will give you a summary, you still decide. If decision is the whole task, you cannot delegate it.
- **Small lookups** (<5 reads, single grep) — direct tool use is cheaper than spawn-overhead.
- **Tasks where you need the raw output** — delegation strips detail.

## Anti-patterns

- ❌ Spawning without specifying return-format → 800-word narration polluting main context.
- ❌ Granting `*` tools when read-only would suffice → subagent burns its own context on irrelevant tool docs.
- ❌ Parallel subagents on tasks that share files / state → race conditions.
- ❌ Forked subagent (same context) for review work → anchoring bias. Use fresh context for review.
- ❌ Subagent for "think harder" — the subagent thinks no harder than the parent. Use it for *exploration*, not *cognition*.

$ARGUMENTS
