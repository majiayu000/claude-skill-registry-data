---
name: memory-curator
description: Review staged memory, help with promotion or rejection, and suggest durable memory updates.
intents: [memory_query, meta, task]
agents:
  - path: agents/extract-from-turn.md
allowed-tools:
  - spawn_subagent
  - stage_memory
  - list_staged_memory
  - promote_staged_memory
  - reject_staged_memory
  - search_memory
  - read_memory
  - write_memory
---

# Memory Curator

Use this skill when the user wants to inspect, review, promote, reject, or tidy curated memory.

## Default behavior

- Start from staged memory when the user asks what should be remembered.
- Prefer `list_staged_memory` for queue review and `search_memory` for durable-memory lookup.
- Summarize findings before proposing durable changes.
- Use `promote_staged_memory` or `reject_staged_memory` for staged entries instead of direct file edits.
- When suggesting compaction or durable note updates, keep changes factual and short.

## Promotion and rejection posture

- Promotion is durable and should only happen after the built-in confirmation flow succeeds.
- Rejection should keep the reason short and factual.
- If there are multiple plausible staged entries, present the set clearly instead of guessing.

## Compaction help

- When daily notes are noisy, suggest a concise durable note in `notes/` and use `write_memory`.
- Do not rewrite `MEMORY.md` unless it clearly improves the durable catalog.

## Extraction agent

The contributed agent `memory-curator/extract-from-turn` is for explicit "look at what we just covered and suggest things to remember" requests.
