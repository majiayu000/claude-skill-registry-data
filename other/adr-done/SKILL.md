---
name: adr-done
description: Mark an ADR as Implemented (or Superseded) and archive it, following INDEX.md conventions.
argument-hint: "<ADR number> [Superseded by NNN]"
allowed-tools: Read, Glob, Bash(ls *), Bash(mv *), Edit
---

# Mark ADR as Done

Mark ADR $ARGUMENTS as completed and archive it.

## Process

1. **Read INDEX.md** at `docs/ai/adr/INDEX.md` to confirm:
   - Status legend: `Implemented`, `Proposed`, `Superseded` (never "Done")
   - File organization: Implemented/Superseded ADRs go to `docs/ai/adr/archive/`

2. **Find the ADR file**: Look in `docs/ai/adr/` (top-level) for the matching ADR number.

3. **Determine new status**:
   - Default: `Implemented`
   - If the user says "superseded by NNN": `Superseded`

4. **Update the ADR file**:
   - Change `## Status: Proposed` → `## Status: Implemented` (or `Superseded`)

5. **Move to archive**:
   - `mv docs/ai/adr/{file}.md docs/ai/adr/archive/`

6. **Update INDEX.md**:
   - Change the Status column to `Implemented` (or `Superseded`)
   - Update the Notes column if needed to reflect what was built

## Rules

- Status values are ONLY: `Implemented`, `Proposed`, `Superseded` — never "Done", "Complete", etc.
- Implemented and Superseded ADRs MUST be moved to `archive/`
- Proposed ADRs stay in the top-level `docs/ai/adr/` directory
