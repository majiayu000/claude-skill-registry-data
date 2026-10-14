---
name: ground-context
description: Context budget management. Solves context exhaustion.
---

# Skill: Context Management

> "Context is RAM. Filesystem is external memory—unlimited, persistent, operable." — Manus

## When

Before context becomes a constraint. The kernel monitors automatically.

## The Thresholds

| Usage | Action | Why |
|-------|--------|-----|
| 60% | Run `/compact` | Prevent drift before it starts |
| 80% | Delegate to sub-agent | Preserve parent for orchestration |
| 90% | Emergency compress | Summarize aggressively |

## The Protocol

1. **At 60%**: Compact. Preserve: objective, ADRs, failures.
2. **At 80%**: Spawn sub-agent for current task. Parent orchestrates.
3. **Always**: Write to files, not context. Files survive. Context doesn't.

## The Key Insight

> **Compaction is continuation, not termination.**

Auto-compaction enables infinite work. Your objective survives if you keep `working.md` current — the system loads it on resume.

Don't wrap up early to "fit" in context. Don't cut corners. Let compaction happen. Work continues on the other side.

## The Anti-Patterns

| Don't             | Do                        | Why                              |
|-------------------|---------------------------|----------------------------------|
| Hoard context     | Write to files            | Files are unlimited              |
| Wait until 90%    | Compact at 60%            | Late compaction loses objectives |
| Orphan sub-agents | Handoff before delegating | Context must transfer            |
| Wrap up early     | Trust the system          | Compaction continues work        |
| Cut corners       | Maintain quality          | Scope doesn't shrink to fit      |

## The Output

State: "Context at [X]%. Action: [compact/delegate/continue]."
