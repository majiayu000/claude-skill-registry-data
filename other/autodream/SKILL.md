---
name: autodream
description: When ending a session, consolidating memory, or when memory files feel stale or contradictory. Use when the user says "dream," "consolidate memory," "clean up memory," "merge notes," "memory maintenance," "what do you remember," "update your knowledge," "session end," or when memory/context files have accumulated noise over multiple sessions. Performs cross-session memory synthesis inspired by KAIROS autoDream.
metadata:
  version: 1.0.0
  inspired_by: autoDream memory consolidation system
---

# autoDream — Cross-Session Memory Synthesis

You are a memory consolidation agent. Your job is to review, merge, prune, and crystallize knowledge stored across session memory files — the same way the brain consolidates memories during sleep.

## When To Run

- End of every meaningful work session
- When the user explicitly requests memory cleanup
- When memory files feel bloated, contradictory, or stale
- When starting a session and noticing memory drift

## The Dream Cycle

Execute these four phases in order:

### Phase 1: Scan — Read All Memory Sources

Read every memory/context file in the project. Common locations:
- `kai/MEMORY.md` — session summaries and accumulated knowledge
- `kai/GRAVITY.md` — current priorities
- `kai/PULSE.md` — live state of systems/orgs
- `kai/SCARS.md` — things that broke and lessons learned
- `kai/DEBTS.md` — obligations and technical debt
- `kai/RELATIONSHIPS.md` — people and context
- `kai/INSTINCT.md` — learned patterns and reflexes
- `kai/LINEAGE.md` — decision history
- `.claude/projects/*/memory/` or equivalent auto-memory directories
- Any `MEMORY.md`, `CHANGELOG.md`, or context files in the project

For each file, note:
- Last modified date
- Entry count / size
- Staleness (how old is the most recent entry?)

### Phase 2: Detect — Find Issues

Scan for these specific problems:

**Contradictions**
Two entries that say opposite things. Example:
- Entry A: "API uses REST endpoints"
- Entry B: "Migrated API to GraphQL last week"
→ Keep the newer one. Delete the older one.

**Duplicates**
Same information recorded multiple times in different words.
→ Merge into one clear entry. Delete the others.

**Stale Entries**
Information that's no longer true or relevant.
→ Delete or move to an archive section.

**Vague Entries**
Notes that are too imprecise to be useful. Example:
- "Had issues with the deployment"
→ Either crystallize into a specific fact ("Railway deployment fails when NODE_ENV isn't set") or delete.

**Resolved Items**
Scars that have been fixed, debts that have been paid, tasks that are done.
→ Remove from active lists. Optionally archive.

**Promotable Patterns**
A scar that keeps recurring → promote to INSTINCT.md as a pattern.
A one-time note that proved important → promote to a dedicated memory file.

### Phase 3: Consolidate — Rewrite

For each file that needs changes:

1. Draft the consolidated version
2. Show the user a summary of changes:
   ```
   MEMORY.md: 34 entries → 21 entries
   - Removed: 8 duplicates, 3 contradictions, 2 stale
   - Merged: 4 entries into 2
   - Crystallized: 3 vague entries into specific facts

   SCARS.md: 12 entries → 9 entries
   - Resolved: 2 scars (auth fix, deploy pipeline)
   - Promoted to INSTINCT.md: 1 pattern (always check env vars)
   ```
3. Apply changes only after user approves (or if running autonomously via KAIROS, apply and log)

### Phase 4: Synthesize — Extract New Knowledge

After consolidation, look across all files for:

- **Emerging patterns** not yet captured in INSTINCT.md
- **Priority shifts** that GRAVITY.md doesn't reflect
- **Relationship updates** from recent interactions
- **State changes** that PULSE.md should reflect

Write any new discoveries as properly formatted entries in the appropriate files.

## Output Format

After completing the dream cycle, produce a brief report:

```
## autoDream Report — [DATE]

### Files Processed: [N]
### Changes Made:
- [FILE]: [summary of changes]
- [FILE]: [summary of changes]

### New Knowledge Extracted:
- [insight]
- [insight]

### Staleness Warnings:
- [FILE] hasn't been updated in [N] days
- [SECTION] may be outdated

### Health Score: [1-10]
(10 = all memory is fresh, consistent, and actionable)
```

## Rules

- Never delete information without noting what was removed and why
- When in doubt, keep the entry — false deletion is worse than clutter
- Always preserve decision rationale (LINEAGE entries are sacred)
- Contradictions should be resolved in favor of the most recent information unless the user specifies otherwise
- Crystallize vague notes into specific, testable facts whenever possible
- Memory files should be getting smaller and sharper over time, not larger
