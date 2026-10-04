---
name: torque:status
description: "Show current project state across GSD and Superpowers systems. Reads .planning/, docs/plans/, and git state to give a unified view of where you are and what to do next."
---

# Torque Status

Show the developer a unified view of their project state. No database — read files and git only.

## Procedure

### Step 1: Detect project type

```bash
# Check which system is active
ls -d .planning/ 2>/dev/null && echo "GSD_PROJECT=true" || echo "GSD_PROJECT=false"
ls -d docs/plans/ 2>/dev/null && echo "SP_PROJECT=true" || echo "SP_PROJECT=false"
```

### Step 2: GSD project state (if `.planning/` exists)

Read these files in order (skip any that don't exist):

1. **`.planning/STATE.md`** — current phase, plan statuses, blockers
2. **`.planning/ROADMAP.md`** — milestone and phase overview
3. **`.planning/PROJECT.md`** — project goals and tech stack (first 30 lines)
4. **Active phase directory** — check `.planning/phases/N/` for the current phase:
   - `CONTEXT.md` — what this phase is about
   - `PLAN.md` or `PLAN-*.md` — execution plans and their status
   - `SUMMARY.md` files — completed plan summaries
   - `VERIFICATION.md` — verification results if phase is in verify stage
   - `HANDOFF.md` — if work was paused mid-phase

### Step 3: SP standalone state (if `docs/plans/` exists, no `.planning/`)

1. Read all `docs/plans/*.md` files
2. Check for completion markers (checked boxes `[x]` vs unchecked `[ ]`)
3. Identify current position in the plan

### Step 4: Git context

```bash
git branch --show-current
git log --oneline -5
git status --short
```

### Step 5: Conflict detection

Flag if BOTH `.planning/` AND `docs/plans/` exist — this is a misconfiguration. See `references/conflict-resolution.md`.

### Step 6: Output format

Print a structured summary:

```
## Project Status

**Type**: GSD project | SP standalone | No workflow detected
**Branch**: feature/xyz
**Phase**: 3 of 7 — "Authentication system"
**Phase status**: executing (2/4 plans complete)
**Blockers**: None | [list blockers]
**Last activity**: 2h ago — "add jwt middleware"

### Active Plans
- [x] PLAN-01: Database schema (complete)
- [x] PLAN-02: Auth service (complete)
- [ ] PLAN-03: JWT middleware (in progress)
- [ ] PLAN-04: Route guards (pending)

### Suggested Next Action
→ Continue executing PLAN-03, or run `/gsd:resume-work` if context was lost
```

If no workflow is detected:
```
## Project Status

**Type**: No workflow detected
**Branch**: main

### Getting Started
- New project? → `/gsd:new-project`
- Existing codebase? → `/gsd:map-codebase`
- Quick standalone work? → Just start with `brainstorming`
```

## Rules

- Never modify any files. This is read-only.
- Show real data from files, not guesses.
- Keep output concise — fit in one screen.
- Always include a suggested next action.
