---
name: claude-md
description: Keep the CLAUDE.md your agents rely on accurate and lean instead of stale. Use when maintaining (not first creating) a CLAUDE.md — syncing it with architecture, conventions and commands as the project evolves, and pruning bloat so it stays scannable. Complements the built-in /init by owning the ongoing upkeep.
license: MIT
---

# CLAUDE.md Maintenance Workflow

Keep an existing `CLAUDE.md` accurate and lean. This is for ongoing upkeep — use the built-in `/init` for first creation.

## Process

1. Read the current `CLAUDE.md`.
2. Compare against reality: recent commits, changed build commands, new/removed modules, updated conventions, new architecture decisions (check the ADR directory).
3. Update **only the affected sections**. Do not rewrite untouched sections.
4. Prune: remove stale instructions, merge duplicates, and keep each section tight. If a section has grown long, tighten it rather than letting it sprawl.
5. Preserve the user's voice and structure — you are maintaining their file, not replacing it.

## What to check for drift

- Build / test / lint commands that changed
- Module or directory structure changes
- New conventions or rules the team adopted
- Architecture decisions recorded as ADRs that belong in the high-level guidance
- Anything now contradicted by the actual codebase

## Rules

- Never blow away existing content wholesale — edit surgically.
- Keep it scannable; CLAUDE.md is loaded into every session, so brevity matters.
- If something is already obvious from the code or another doc, don't duplicate it here.
