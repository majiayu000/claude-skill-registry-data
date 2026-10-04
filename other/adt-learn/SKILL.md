---
name: learn
description: Auto-extract reusable patterns from the current session into skills or memory
triggers:
  - learn
  - extract patterns
  - what did I learn
  - save pattern
  - continuous learning
---

# Learn

Extract reusable patterns from the current session and persist them.

## When to Use

- End of a productive session with new discoveries
- After solving a hard debugging problem
- When a workaround becomes a permanent pattern
- After figuring out a library's quirks

## Steps

1. Review the session for decisions, fixes, and patterns
2. Classify each finding:
   - **Decision** — architecture choice, API design, naming convention
   - **Pattern** — reusable code approach, workflow, or configuration
   - **Gotcha** — bug, quirk, or failure mode to avoid next time
   - **Preference** — style choice, tool selection, commit format
3. For each finding, write a concise entry:
   ```text
   [TYPE] <one-line summary>
   Context: <when this applies>
   Evidence: <what happened that taught us this>
   Confidence: high | medium | low
   ```
4. Persist to the appropriate location:
   - Decisions → `.agents/memory/decisions.md`
   - Patterns → `.agents/memory/patterns.md`
   - Gotchas → `.agents/memory/gotchas.md`
   - Preferences → `.agents/memory/preferences.md`
5. If a pattern is mature enough (high confidence, used 3+ times), promote it to a skill

## Rules

- Extract at session end, not continuously
- One entry per finding — keep them atomic
- Date-stamp every entry
- Remove entries that are no longer true
- Never extract sensitive data (keys, passwords, internal URLs)
- Low-confidence entries are fine — they mature over time
- The codebase is the source of truth, memory is supplementary
