---
name: add-adr
description: Create a new Architecture Decision Record in the vault Decisions/ folder, update the ADR Index, and cross-link from related notes. Use when a meaningful trade-off is made, an architectural pattern is chosen, or the user says "we decided to X because Y".
---

# add-adr

Capture a non-obvious architectural decision so it survives across sessions.

## When to use

Trigger this skill when one of these happens:

- The user explicitly says "let's go with X over Y because..."
- A pattern is chosen that future-Claude could plausibly question
- A trade-off is made between security/perf/dev-speed
- A library, framework, or service is added/replaced

Do **not** use this for routine implementation choices (variable names, file locations within an existing pattern).

## Steps

1. **Read** `Aqarkom_Knowledge/Decisions/ADR Index.md` to find the next number.
2. **Create** `Aqarkom_Knowledge/Decisions/{NNN} - {Title}.md` with this template:

   ```markdown
   ---
   tags: [decision, adr]
   created: YYYY-MM-DD
   adr: NNN
   status: Proposed | Accepted | Superseded
   ---

   # ADR NNN — {Title}

   ## Context
   What problem are we solving? What constraints are in play?

   ## Decision
   The choice we made, in one paragraph.

   ## Alternatives considered
   - **Option A** — pros/cons
   - **Option B** — pros/cons

   ## Consequences
   - Positive: ...
   - Negative: ...
   - Neutral: ...

   ## Related
   - [[Decisions/ADR Index]]
   - [[other relevant notes]]
   ```

3. **Update the index** at `Aqarkom_Knowledge/Decisions/ADR Index.md` — add a row to the table.
4. **Cross-link** — find any vault notes affected by this decision and add a "See [[Decisions/NNN - Title]]" line at the bottom.
5. **Save a memory** of the form `feedback` or `project` if the decision affects how Claude should behave going forward (e.g., "always do X, never do Y").

## Verification

- [ ] New ADR file exists
- [ ] Index updated
- [ ] At least one related note links back to it
- [ ] Memory saved if behaviorally relevant
