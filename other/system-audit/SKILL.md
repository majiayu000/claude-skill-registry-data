---
description: Deep infrastructure audit of the entire operating system
argument-hint: ""
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Write
  - Edit
  - Bash(date:*,wc:*,find:*)
---

Comprehensive infrastructure audit. Run monthly or after major system changes.

## Checks

### Check 1: Agent Health
- Read every file in `.claude/agents/*.md`
- Verify each has valid frontmatter (---)
- Verify no TBD/TODO markers
- Check that referenced tools exist
- Check agent-memory directories exist for agents that need them

### Check 2: Command Health
- Read every file in `.claude/commands/*.md`
- Verify each has valid frontmatter
- Check that allowed-tools are reasonable
- Verify no broken cross-references to other commands

### Check 3: Hook Health
- Verify `.claude/settings.json` is valid JSON
- Check every hook script referenced in settings.json exists
- Verify all hook scripts are executable (chmod +x)
- Run a dry test: each hook should exit 0 with empty input

### Check 4: Memory Tier Health
- `memory.md`: Is it under 100 lines? Is "Now" current?
- `knowledge-base.md`: Is it under 200 lines? Do all entries have [Source:]?
- `knowledge-nominations.md`: Are there stale nominations (>30 days)?
- `agent-memory/`: Do directories match existing agents?
- Daily Notes: Are recent notes present?

### Check 5: Log Health
- `audit-trail.md`: Is it under 5000 lines?
- `incident-log.md`: Are there unresolved CRITICAL/HIGH events?
- `failure-log.md`: Are there recurring patterns?
- `verdicts.jsonl`: What's the block rate? Any task-type clustering?

### Check 6: Permission & Config Coherence
- `.claude/settings.json` hooks match actual hook files
- No orphaned hook scripts (exist but not referenced)
- No missing hook scripts (referenced but don't exist)

### Check 7: Cross-File Coherence
- CLAUDE.md references match actual file locations
- Command-index.md matches actual commands
- No circular dependencies between commands

### Check 8: Backup & Storage
- `.claude/backups/`: Is auto-pruning working? (no dirs >7 days old)
- Large files in project root that shouldn't be there?

### Check 9: Via Negativa Sweep
- Are there files/agents/commands that are never used?
- Could any hook be removed without loss?
- Is there duplicated logic between agents?
- Propose removals — simpler is better

## Grading

| Grade | Criteria |
|-------|----------|
| A | All checks pass, no issues |
| B | Minor issues only (cosmetic, non-blocking) |
| C | Some issues need attention (missing provenance, stale nominations) |
| D | Structural issues (broken hooks, invalid JSON, missing agents) |
| F | Critical failures (security issues, data loss risk) |

## Output

Write results to daily note under:
```markdown
## System Audit — MMDDYY

**Grade:** [A-F]
**Checks:** [passed]/9
**Issues:** [bullets with severity]
**Actions:** [corrective tasks, if any]
```

Create corrective tasks on Task Board for any D or F grade issues.
