---
name: minutes-mcp-recall
description: Route meeting-recall questions to the right Minutes MCP tool.
---

## Skill Path

Before running helper scripts or opening bundled references, set:

```bash
export MINUTES_SKILLS_ROOT="$(git rev-parse --show-toplevel)/.agents/skills/minutes"
export MINUTES_SKILL_ROOT="$MINUTES_SKILLS_ROOT/minutes-mcp-recall"
```

# /minutes-mcp-recall

Route a meeting-memory question to the smallest useful Minutes MCP tool. This
skill is tool-name-oriented for MCP hosts such as OpenClaw, Hermes-agent, and
other MCP clients. Use `minutes-search` instead when the host only has CLI or
shell access.

Read [the complete tool map](references/tool-map.md) only when the decision
table does not cover the request.

## Decision table

| User is asking... | Call |
|---|---|
| "What did we say about X?" or "Find that meeting about Y." | `search_meetings` |
| "What is the full transcript of this specific meeting?" | `get_meeting` after finding its id or date with `list_meetings` or `search_meetings` |
| About what is happening right now, mid-call | `read_live_transcript` with a cursor or time window |
| "What do I still owe?" or "Who owes me?" | `track_commitments` |
| "What is my history with this person?" | `get_person_profile` or `relationship_map` |
| "Have I contradicted myself?" or "Which decisions are stale?" | `consistency_report` |
| Broad research across many meetings | `research_topic` |

## Tool-name prefix by host

- OpenClaw and generic MCP clients use bare tool names such as
  `search_meetings`.
- Hermes-agent prefixes each tool with `mcp_minutes_`, so
  `search_meetings` becomes `mcp_minutes_search_meetings`.

Apply the same prefix rule to every tool in the decision table and tool map.

## Anti-patterns

- Do not call `get_meeting` speculatively to browse. It returns a full
  transcript. Use `search_meetings` or `list_meetings` first to find the right
  id or date and preserve context budget.
- Do not call `read_live_transcript` without a cursor after one is available.
  Replaying the whole transcript wastes tokens and duplicates content already
  in context.
- Do not use capture, dictation, processing, annotation, or speaker-mutation
  tools for a recall question.

