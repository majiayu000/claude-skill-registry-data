---
name: context-engineering
description: Apply the Write/Select/Compress/Isolate framework to manage the context window. Use when the task is long, the transcript is bloated, the model is drifting, or before /holocron:handoff.
---

# Context engineering

Your context window is a working set. Like any working set, it has limits, and the cost of a bad one compounds.

## The four moves

1. **Write** — commit durable info out of the transcript and into files the model can re-read later. Plans, decisions, learnings, todos. Don't leave them floating in chat.
2. **Select** — load exactly what you need for the current step. Not the whole repo. The specific files that matter for the specific change.
3. **Compress** — summarize old transcript turns into one line each, and offload details to files. After a long debugging arc: one paragraph of "what we tried and what happened" beats 30 turns of blow-by-blow.
4. **Isolate** — delegate sub-problems to subagents so their discovery doesn't pollute the main context. Research-heavy exploration → Explore agent. Review → code-reviewer agent.

## Practical heuristics

- **Hot > cold.** Keep recent decisions, current plan, and the ~3 files you're actively editing in context. Everything else can be retrieved.
- **References, not contents.** "See `docs/adr/0007-queue.md`" beats pasting 400 lines of ADR.
- **One plan, one place.** If the plan is in context AND in a file, they'll drift. Canonicalize in the file; reference from context.
- **Invalidate explicitly.** When a decision changes, say so. "We said X, now we're doing Y because Z." Don't let old assumptions linger.

## Smells that say "you've lost the plot"

- The model repeats analysis you already gave it
- Transcript is >50 turns and you don't remember what turn 10 decided
- You're answering the same question for a second time
- The model confidently contradicts itself

Act on the smell. Use `/holocron:handoff` to write a durable doc and start fresh.

## Related

- `/holocron:handoff` — persist state before compaction
- `/holocron:learn` — persist rules for future sessions
- `/holocron:plan` — write the plan to a file rather than carry it in chat
