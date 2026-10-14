---
name: craft-handoff
description: Create a handoff document. Preserves state across sessions.
---

# Skill: Craft Handoff

> "A handoff is a gift to your future self."

## When

Create a handoff when:
- Ending a session
- Task is complete
- Blocked and switching focus
- Delegating to a sub-agent

## The Standard

1. **Location**: `handoffs/NNN-topic.md` in branch memory.
2. **Sequence**: Increment NNN from last handoff.
3. **Content**: What was done, decisions, next steps, learnings.
4. **Brevity**: One page max. Future you needs signal, not noise.

## The Protocol

1. **Determine trigger**: Why are we creating this handoff?
2. **Summarize done**: What was accomplished this session?
3. **List decisions**: What choices were made and why?
4. **Define next**: What should the next session do first?
5. **Extract learnings**: What patterns or insights emerged?
6. **Save**: Write to `handoffs/NNN-topic.md`.

## The Anti-Patterns

| Don't             | Do                    | Why                           |
|-------------------|-----------------------|-------------------------------|
| Dump full context | Summarize key points  | Brevity is clarity            |
| Skip decisions    | Record with rationale | Decisions are cheap to forget |
| Omit blockers     | State what's stuck    | Prevents wasted cycles        |
| Forget learnings  | Capture insights      | Compound knowledge            |

## Template

See `templates/handoff.md`.

## Loading

Handoffs are loaded automatically on session resume. Your future self will see it.
