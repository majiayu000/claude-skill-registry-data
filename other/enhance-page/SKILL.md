---
name: enhance-page
description: Propose 3-5 baby-step enhancements for an existing page following the E1-E20 pattern (frontend + backend + database). Use when the user asks "what can we add to page X", "improve the leads page", or "enhance Y".
---

# enhance-page

Generate a focused enhancement set for a single page. Mirrors the structure of the master Enhancement Plan E1-E20.

## Inputs to gather

- **Target page** (path or English name)
- **User goal** if any ("make it faster" / "more useful for owners" / "missing X")

## Steps

1. **Read the page file** end-to-end. Don't skim — many pages are 500+ LOC.
2. **Read the underlying API route** to understand what's already exposed.
3. **Check the Database Schema vault note** for related tables.
4. **Look at sibling enhancement sessions** (E1, E2, E3) for the kind of enhancements that have worked.
5. **Propose 3-5 enhancements** in the project's signature shape:
   - **Frontend**: visual / interaction improvement
   - **Backend**: new endpoint or calculated field
   - **Database**: new column or table (only if needed)
6. **Format as a checklist** matching the E1-E20 plan format:
   ```markdown
   ### Session E{n} — {Page} Enhancements
   **Page**: `apps/web/src/pages/...`
   **Goal**: {one-line}

   - [ ] **Frontend**: ...
   - [ ] **Frontend**: ...
   - [ ] **Backend**: ...
   - [ ] **Database**: ...
   - **Files**: ...
   ```
7. **Ask the user to confirm** before writing any code. They may want to drop or reorder items.
8. **Once confirmed**, follow `/next-session` flow (create tasks, work through them, run `/complete-session` at the end).

## Quality bar

Good enhancements:
- Are testable (can verify in 30 seconds)
- Move a real metric (speed, completeness, REGA compliance, agent productivity)
- Reuse existing patterns where possible

Bad enhancements:
- "Refactor the file" — too vague, no measurable outcome
- "Add tests" alone — tests aren't an enhancement, they're table stakes
- Anything that takes more than 1 session to ship

## Anti-patterns

- Don't propose enhancements without reading the page first
- Don't suggest something already shipped (check completed E sessions)
- Don't propose more than 5 — baby steps means tight scope
