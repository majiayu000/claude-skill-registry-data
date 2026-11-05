---
name: agent-memory
description: Log agent sessions, consolidate project memory (dream), promote reviewed memory, and load context for new chats. Use when ending a session, improving cross-session recall, or when the user mentions agent memory, dream, log-session, or memory.md.
---

# Agent memory

Local consolidation for **image-scoring-gallery** — scripts and canonical store live in sibling **image-scoring-pipeline** (no duplicate dream engine in gallery).

## When to use

- **Session start:** Read sibling `../image-scoring-pipeline/.agent-memory/memory.md`; prefer repo evidence on conflict.
- **Session end / milestone:** Log durable learnings with `/log-session`.
- **Periodic:** Run `/dream-memory`, review changelog, `/promote-memory` after human approval.

## Memory candidates

Use `text|category|confidence` on CLI or YAML `memory_candidates`:

| Category | Use for |
|----------|---------|
| `stable_fact` | Stack, architecture, env |
| `user_preference` | Style, workflow, review prefs |
| `working_rule` | How to run tests, what not to touch |
| `recurring_issue` | Flakes, traps, env pain |
| `successful_pattern` | Approaches that worked |
| `open_question` | Unverified assumptions |
| `deprecated` | Superseded guidance |

Confidence: `low`, `medium`, `high`.

## Commands (gallery repo root)

```powershell
python ../image-scoring-pipeline/scripts/agent-memory/log_session.py --summary "..." --outcome "..." --candidate "text|working_rule|high"
python ../image-scoring-pipeline/scripts/agent-memory/dream.py
python ../image-scoring-pipeline/scripts/agent-memory/promote_dream.py --dream ../image-scoring-pipeline/.agent-memory/dreams/<timestamp>.md
python ../image-scoring-pipeline/scripts/agent-memory/context.py
```

Transcript import: backend `/import-transcripts` and [AGENT_MEMORY.md](https://github.com/synthet/image-scoring-pipeline/blob/main/docs/technical/AGENT_MEMORY.md).

## Dream review checklist

1. Open backend `dreams/*-changelog.md` — scan **Uncertain / needs review**.
2. Diff proposed `dreams/*.md` vs `memory.md`.
3. Redact anything sensitive; reject promotion if secrets might be present.
4. Promote only when the proposal is accurate and concise.

## Safety

- Scripts block common secret patterns on write.
- Do not log `secrets.json`, `.env`, tokens, or personal library paths.
- Never edit `memory.md` directly during implementation work.

## Reference

- [`.agent-memory/CURSOR_USAGE.md`](../../.agent-memory/CURSOR_USAGE.md)
- Backend [`.agent-memory/CURSOR_USAGE.md`](https://github.com/synthet/image-scoring-pipeline/blob/main/.agent-memory/CURSOR_USAGE.md)
- Backend [docs/technical/AGENT_MEMORY.md](https://github.com/synthet/image-scoring-pipeline/blob/main/docs/technical/AGENT_MEMORY.md)
