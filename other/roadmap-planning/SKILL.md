---
name: roadmap-planning
description: Use to create or update a project-wide, multi-phase roadmap, including priorities and status. For a single feature or phase, use mak:dev-kickoff.
---

# Project Roadmap Design & Maintenance Guide

This skill owns the **writing and periodic maintenance** of the project's top-level roadmap document.
It focuses on mid/long-term direction across phases — phase boundaries, priorities, status tracking, links to related design docs — not single-feature design.

Write the roadmap and all user-facing output in the user's conversation language (or the project's documented language policy). The bundled template is in English; keep its structure.

## Write boundary

The roadmap directs work, it does not do it: investigation and document writing only. Allowed: read-only investigation (Read / Grep / Glob / git log) and creating/updating the roadmap document (.md) after user approval. Prohibited: creating, modifying, or deleting source code files and running build or execution commands.

---

## When to Use

### Enter this skill

- Establishing a new project's mid/long-term direction for the first time
- Large-scale roadmap restructuring — adding/splitting/merging/removing phases
- Officially updating phase completion / transfer / hold status
- Producing a document that shares overall direction with a team or stakeholders

### Route to a different skill when

- Kicking off a single feature / single phase → `mak:dev-kickoff`
- Direction itself is vague and divergence is needed first → `mak:brainstorming`
- Writing the **detailed design doc** for a specific phase → `mak:design-doc-template`

---

## Pre-Investigation Checklist

Before drafting the roadmap, confirm:

- [ ] Scan `README`, `CLAUDE.md`, `docs/`, and the project's design-doc path — grasp vision and constraints
- [ ] Check for an existing roadmap document — the roadmap path in the project `CLAUDE.md`, then `docs/*roadmap*.md`, then `ROADMAP.md`
- [ ] Recent commit trend (`git log --oneline -20`) — what has been completed
- [ ] Completed features, in-progress branches, unfinished work
- [ ] Project vision and constraints — team size, deadlines, business priorities

---

## Procedure (in order)

### 1. Confirm vision, goals, constraints

Limit questions to 1–2. No open-ended questions that widen scope.

Example questions:

- "Is there a critical deadline or business priority right now?"
- "Any hard constraints this roadmap must include?"
  - If direction is too vague to draw phase boundaries, pause this skill, diverge with `mak:brainstorming`, and return once candidates narrow.

### 2. Draft the current-state summary

Write two blocks:

**Strengths** — structure, patterns, and completed features already in place
**Watch when extending** — areas needing extension/improvement, still-incomplete parts

### 3. Set phase boundaries

Split phases by dependency, risk, and scope; 3–9 phases recommended — too many dilutes direction.
Present 2–3 options in a comparison table with a recommendation. If hard constraints (fixed dependency order, a single viable phase boundary, etc.) leave only one real split, state the constraint and proceed with a single option. Do not fabricate alternative splits.

| Option | Phase split approach | Pros | Cons |
| :--- | :--- | :--- | :--- |
| A | ... | ... | ... |
| B | ... | ... | ... |

**Recommendation**: A. {{reason}}

### 4. Phase ordering logic

For each phase, write one sentence on "why this order".
An order without a reason collapses under change pressure.

### 5. Each phase's "why" and sub-item draft

- Phase title: what it does
- First paragraph of the phase body: why this stage is needed
- Sub-items: `Phase-Index` naming (e.g. `3-7`) for easy reference.

### 6. Decide the status scheme

Choose per team agreement. Icons are 1–2 characters, optimized for visual scanning.

Recommended default (changeable):

| Icon | Meaning |
| :--- | :--- |
| ✅ | Done |
| 🟡 | Partial / in progress |
| ⬜ | Planned |
| 🔵 | On hold (decide after status report) |

Put the legend as a blockquote (`>`) right under the phase summary table.

### 7. Transfer / hold rules

Decide in advance how phase moves are handled:

- **Transfer**: add a "moved to Phase N" note under the sub-item, update the summary table
- **Hold**: mark 🔵, record a one-line reason
- **Done**: add `(✅ done)` to the phase title; keep the body for maintenance reference

### 8. Draft and user approval

Present the draft in chat first, based on `${CLAUDE_PLUGIN_ROOT}/skills/roadmap-planning/assets/roadmap.template.md`.
Fill `{{...}}` placeholders with real content, but record only each phase's purpose, scope, status, next entry skill, and related doc links — no detailed implementation decisions.

Ask for explicit confirmation:

> "I've drafted the roadmap. Please review the phase boundaries and priorities. If it looks good, reply 'save' or 'approve'. I'll write it to the roadmap document after explicit confirmation."

### 9. Save after approval

Save-path priority:

1. Roadmap path specified in the project `CLAUDE.md` → that path
2. An existing roadmap document → that file (`docs/*roadmap*.md`, `ROADMAP.md`, etc.)
3. A `docs/` directory exists → `docs/<index>.roadmap.md` or `docs/roadmap.md` per the project's doc numbering
4. None of the above → `ROADMAP.md` (root)

### 10. Handoff

- Kicking off a single feature within a phase → `mak:dev-kickoff`
- A phase's direction is unclear and needs divergence → `mak:brainstorming` first

---

## Maintenance Rules

### On phase completion

1. Add `(✅ done)` to the phase title
2. Update the summary table status column
3. Keep the body text

### On phase transfer

1. Add `> moved to Phase N` under the sub-item
2. Update the summary table row
3. Add the sub-item to the destination phase

After processing a phase completion or transfer, hand off to `mak:doc-audit` to check whether other documents referencing that phase still hold.

### Recording status changes

State status changes as a change-log unit. Run git commit only when the user explicitly requests it.
Example: `<roadmap-file> > Phase 3 marked done / added sub-item 3-8`

---

## Output Format

See `${CLAUDE_PLUGIN_ROOT}/skills/roadmap-planning/assets/roadmap.template.md`.

Excerpt (phase summary table):

```markdown
| Phase | Content | Status |
| :--- | :--- | :--- |
| **Phase 0** | {{one-line description}} | ✅ **done** |
| **Phase 1** | {{one-line description}} | 🟡 **in progress** |
| **Phase 2** | {{one-line description}} | ⬜ planned |
```
