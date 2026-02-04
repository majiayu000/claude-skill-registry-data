---
name: project-migrate
description: Use this skill to migrate existing (brownfield) projects with established documentation to the SynthesisFlow structure. Intelligently discovers, categorizes, and migrates documentation while preserving content, adding frontmatter, and maintaining git history.
---

# Project Migrate Skill

## Purpose

Intelligently migrate existing projects (brownfield) to the SynthesisFlow directory structure while preserving all existing documentation. This skill provides safe, guided migration with discovery, analysis, backup, and validation phases to ensure zero data loss.

## When to Use

Use this skill in the following situations:

- Adding SynthesisFlow to an existing project with established documentation
- Migrating docs from ad-hoc structure to SynthesisFlow conventions
- Projects with existing specs, ADRs, design docs, or other markdown files
- Need to preserve documentation while adopting SynthesisFlow methodology
- Want safe migration with backups and rollback capability

## Prerequisites

- Project with existing documentation (docs/, documentation/, wiki/, or markdown files)
- Git repository initialized
- Write permissions to project directory
- `doc-indexer` skill available for frontmatter compliance checking

## Workflow

The skill guides you through 7 phases with phase-by-phase approval.

### Step 1: Run the Migration Script

Execute with one of three modes:

**Interactive (default)** - Review and approve each phase:
```bash
bash scripts/project-migrate.sh
```

**Dry-run** - Preview plan without execution:
```bash
bash scripts/project-migrate.sh --dry-run
```

**Auto-approve** - Skip prompts for automation:
```bash
bash scripts/project-migrate.sh --auto-approve
```

### Step 2: Review Each Phase

**Phase 1 - Discovery**: Scans for all markdown files and categorizes them (spec, ADR, design, proposal, etc.)

**Phase 2 - Analysis**: Maps each file to target location in SynthesisFlow structure with conflict detection

**Phase 3 - Planning**: Shows complete migration plan with source → target mappings for your approval

**Phase 4 - Backup**: Creates timestamped backup directory with rollback script before any changes

**Phase 5 - Migration**: Moves files using `git mv` to preserve history, creates directory structure

**Phase 6 - Link Updates**: Recalculates and updates all relative markdown links to reflect new locations

**Phase 7 - Validation**: Verifies all files migrated correctly, checks link integrity, validates structure

**Phase 8 - Frontmatter (Optional)**: Generates and inserts doc-indexer compliant frontmatter for files missing it

### Step 3: Post-Migration

After successful completion:
- Review validation report for any warnings
- Run `doc-indexer` to verify compliance
- Commit migration changes to git
- Delete backup once satisfied (or keep for reference)

## Error Handling

### Permission Denied

**Symptom**: Cannot create directories or move files

**Solution**:
- Verify write permissions to project directory
- Check parent directory exists
- Run with appropriate permissions if necessary

### Conflicts Detected

**Symptom**: Target location already has files

**Solution**:
- Review conflict resolution options in plan
- Choose to merge, create subdirectory, or skip
- Script defaults to safe option (create subdirectory)

### Broken Links After Migration

**Symptom**: Validation reports broken links

**Solution**:
- Check link update logic worked correctly
- Manually fix any complex link patterns
- Re-run validation after fixes

### Frontmatter Generation Failed

**Symptom**: Cannot extract title or detect file type

**Solution**:
- Manually add frontmatter to problematic files
- Skip frontmatter generation and add later
- Check file has proper markdown structure

### Need to Rollback

**Symptom**: Migration didn't work as expected

**Solution**:
- Navigate to backup directory
- Run the generated rollback script
- Review rollback instructions
- Restore to pre-migration state

## Categorization Rules

The analysis phase categorizes files using pattern matching:

- **Specs** (→ docs/specs/): Contains "spec", "specification", "requirements"
- **Proposals** (→ docs/changes/): Contains "proposal", "rfc", "draft"
- **ADRs** (→ docs/specs/decisions/): Matches `ADR-*` pattern or in `decisions/` directory
- **Design Docs** (→ docs/specs/): Contains "design", "architecture"
- **Plans** (→ docs/): Contains "plan", "roadmap"
- **Retrospectives** (→ RETROSPECTIVE.md): Contains "retrospective"
- **READMEs**: Preserved in original location

## Notes

- **Safe by default**: Backup created before any changes
- **Git-aware**: Preserves file history when possible
- **Interactive**: Review plan before execution
- **Rollback support**: Easy restoration if needed
- **Doc-indexer integration**: Ensures frontmatter compliance
- **Conflict handling**: Never overwrites existing files
- **Link integrity**: Automatically updates relative links
- **Progress reporting**: Visibility into each step

