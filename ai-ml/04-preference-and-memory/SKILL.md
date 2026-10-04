---
name: "preference-and-memory"
description: "Captures and evolves user preferences with confidence levels. Maintains Voice of the Customer model with exact language, dissatisfaction and aspiration signals. Handles promotion/demotion, global vs project scoping, auto memory system, and Omi wearable data integration."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  effort: "medium"
  model: "haiku"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
priority: 2
pack: "core"
stage: stable
triggers:
  - "remember"
  - "memory"
  - "preference"
paths:
  - "*"
---

# 04 — Preference and Memory

Capture and evolve user preferences with confidence levels, maintaining a Voice of the Customer model scoped globally or per project.

## Auto-memory system

Persistent file-based memory at `/Users/Apple/.claude/projects/<encoded-path>/memory/`. Write directly via Write tool.

## Memory types

- **user** — role, goals, responsibilities, knowledge
- **feedback** — guidance on how to approach work (corrections AND confirmations)
- **project** — ongoing initiatives, bugs, incidents, who/why/when
- **reference** — pointers to external resources

## Capture triggers

- User explicitly says "remember X" / "save Y" → save immediately
- Correction ("no not that", "don't") → feedback memory
- Confirmation of unusual approach ("yes exactly", "perfect") → feedback memory
- New role / preference / responsibility detail → user memory
- Project milestone / decision / deadline → project memory
- External system reference ("check the Linear project X") → reference memory

## Memory file format

```markdown
---
name: {short-kebab-case-slug}
description: {one-line summary — used for relevance ranking}
metadata:
  type: {user | feedback | project | reference}
---

{memory content}
```

For feedback/project: lead with rule/fact, then `**Why:**` line + `**How to apply:**` line.

## Memory routing

- **Universal (across all projects)** → `~/.claude/`
- **Project-specific** → `./.claude/` (path-scoped)
- **Project memory file** → `~/.claude/projects/<encoded-path>/memory/<name>.md` + index in `MEMORY.md`

## MEMORY.md index

One-line pointer per file:

```md
- [Title](file.md) — one-line hook
```

Keep under 200 lines (lines after 200 truncated).

## Confidence levels

- 0.95-1.0 — directly stated by Brian
- 0.85-0.95 — strongly implied by pattern (3+ confirmations)
- 0.70-0.85 — inferred from one signal
- <0.70 — speculative, verify before acting

Below 0.70 → ask `AskUserQuestion` before persisting.

## Voice of the Customer model

- Exact language Brian uses ("pick ONE", "Hey not Hi", "always find 50 more things")
- Dissatisfaction signals (corrections, re-issued prompts)
- Aspiration signals (stated goals, ideal-world descriptions)
- Stylistic preferences (brevity, sharpness, no preamble)

## Brian's preferences (cite from `rules/brian-preferences.md`)

- Pick ONE, never options
- Never ask permission, silence = approval
- "Hey" not "Hi", no preamble
- Code complete, never truncate
- Priority: simplicity > cost > speed > compatibility
- Open-source only
- Side repos auto-push; emdash projects user-push

## Promotion / demotion

- Memory recurring across 3+ projects → promote to rule (`~/.claude/plugins/heymegabyte-claude-skills/rules/`)
- Rule contradicted by repeated correction → demote to memory or remove
- Per `rules/prompt-as-training-signal.md`

## Stale memory

- Memory describing now-incorrect facts (renamed function, removed flag, retired service) → update OR delete
- Per `rules/prompt-as-training-signal.md` § Before recommending from memory

## Omi wearable integration (future)

- Capture Brian's voice notes as candidate memory entries
- Auto-tag by inferred type
- Surface for review before commit
- Path: `~/.claude/_omi-inbox/<timestamp>.md`

## Capture protocol (every prompt)

1. Scan prompt for capture triggers
2. Determine memory type
3. Write file w/ frontmatter
4. Add index entry to `MEMORY.md`
5. Cross-link siblings via `[[name]]`
6. Per `rules/prompt-as-training-signal.md` — extract BEFORE doing requested work
