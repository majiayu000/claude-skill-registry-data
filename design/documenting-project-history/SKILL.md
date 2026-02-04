---
name: documenting-project-history
description: Documenting and categorizing project prompts and decisions for StickerNest. Use when the user asks to document a session, record what was built, update project history, add to the prompt archive, or when starting a new session and needing context. Covers prompt categorization, decision history, and architectural evolution.
---

# Documenting Project History

This skill maintains a living knowledge base of prompts, decisions, and architectural evolution for StickerNest. It helps future AI sessions understand context and continue work seamlessly.

## When to Use This Skill

1. **End of session**: Document what was accomplished
2. **Major feature complete**: Record the approach taken
3. **Architecture decision**: Capture the why behind choices
4. **Starting new session**: Review history for context
5. **User explicitly asks**: "document this", "add to history", "record what we did"

## How to Document

When documenting, add entries to `prompt-history.md` in this skill folder:

```markdown
## [Category] Brief Title
**Date**: YYYY-MM-DD
**Summary**: 1-2 sentence overview
**Key Decisions**:
- Decision 1 and why
- Decision 2 and why
**Files Changed**: List of main files
**Related**: Links to related entries
```

## Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `ARCHITECTURE` | System design, patterns, structure | Parallel rendering, state management |
| `WIDGETS` | Widget system, creation, pipelines | New widget types, Protocol changes |
| `SPATIAL` | VR/AR, 3D rendering, WebXR | XR entry, coordinate systems |
| `UI/UX` | Components, panels, interactions | Toolbars, modals, gestures |
| `AI` | AI features, prompts, generation | Widget generation, reflection |
| `INFRA` | Build, deploy, testing, CI/CD | Vite config, Playwright tests |
| `FIX` | Bug fixes, debugging sessions | XR issues, rendering bugs |
| `SKILL` | Claude Code skills created | Meta-documentation |

## Documentation Template

When the user asks to document, use this format:

```markdown
---

## [CATEGORY] Title of Work Done
**Date**: [Today's date]
**Session Summary**:
[2-3 sentences describing what was accomplished]

**User's Original Request**:
> [Quote or paraphrase the user's initial prompt]

**Approach Taken**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Key Decisions**:
- **[Decision]**: [Why this choice was made]

**Files Created/Modified**:
- `path/to/file.ts` - [brief description]

**Lessons Learned**:
- [Any insights for future sessions]

**Related Entries**: [Links to related history]

---
```

## Viewing History

To help users understand project evolution:

1. Read `prompt-history.md` for full history
2. Summarize by category if requested
3. Find related past work for current tasks
4. Identify patterns in user requests

## Maintaining the Archive

- Keep entries concise but complete
- Link related entries together
- Update if decisions are reversed
- Archive outdated approaches

## Quick Reference Commands

When user says:
- "document this" → Add entry for current session
- "what did we do last time?" → Read recent history
- "show widget history" → Filter by WIDGETS category
- "update the history" → Append to prompt-history.md
