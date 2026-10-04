---
name: dream-consolidation
description: Memory consolidation cycle — Orient, Gather, Consolidate, Prune. Run periodically to keep memory files clean, deduplicated, and under size limits.
---

# Dream Consolidation

A 4-phase memory maintenance cycle that mirrors biological memory consolidation.

## When to Trigger
- After major project milestones
- When MEMORY.md exceeds 200 lines
- Every 2 weeks of active use
- When the user says "consolidate memory" or "dream"

## Phase 1: Orient
Read ALL memory files to understand current state:
- Global memory (~/.claude/memory/*)
- Project memory (~/.claude/projects/*/memory/*)
- MEMORY.md index file

Assess: line counts, staleness, duplicates, outdated entries.

## Phase 2: Gather
Identify what to keep, compress, and discard:
- **Keep**: Active project details, current priorities, hard rules
- **Compress**: Session summaries → archive file with key takeaways
- **Discard**: Completed tasks, stale priorities, resolved issues
- **Deduplicate**: Info in MEMORY.md that's already in topic files

## Phase 3: Consolidate
Execute the changes:
- Archive old session summaries to archive file
- Update MEMORY.md with compressed references
- Backfill learning-log.md with missing entries
- Clean up session-handoff.md
- Extract cross-cutting technical lessons into MEMORY.md

## Phase 4: Prune
Verify the results:
- MEMORY.md under 200 lines
- No duplicate information across files
- All topic files still accurate and accessible
- Archive file preserves important details
- Report: before/after line counts, what changed

## Key Principles
- **Deduplication through indirection**: MEMORY.md points to topic files, doesn't repeat them
- **Cross-cutting consolidation**: Scattered lessons get one reusable section
- **Nothing important lost**: Archive preserves details, MEMORY.md keeps pointers
