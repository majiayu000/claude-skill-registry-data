---
name: doc-validator
description: Use this skill to validate that Markdown files are in standard locations. Scans for .md files outside of predefined allowed directories and outputs warnings to prevent documentation sprawl. Triggers include "validate docs", "check markdown locations", or as part of quality checks.
category: project
---

# Doc Validator

## Purpose

Scan the repository for Markdown files (`.md`) located outside of predefined, allowed directories. This skill helps prevent documentation sprawl and enforces a consistent repository structure by warning about `.md` files in non-standard locations.

## When to Use

Use this skill in the following situations:

- During code reviews to ensure documentation is properly organized
- As part of CI/CD quality checks
- Before merging changes that add new documentation
- When auditing the repository for documentation compliance
- Called automatically by other skills (issue-executor, change-integrator)

## Prerequisites

- Standard bash utilities (`find`, `bash`)
- Project follows SynthesisFlow directory conventions

## Workflow

### Step 1: Run the Validator

Execute the validator script to scan for misplaced Markdown files:

```bash
bash skills/doc-validator/scripts/doc-validator.sh
```

### Step 2: Review Warnings

The script outputs warnings for any `.md` files found in non-standard locations:

```
WARNING: Markdown file in non-standard location: ./src/notes.md
WARNING: Markdown file in non-standard location: ./scripts/temp-docs.md
```

### Step 3: Take Action

For each warning:

1. **Determine if the file should exist**: Is it temporary or abandoned?
2. **Move to proper location**: Relocate to `docs/` or appropriate skill directory
3. **Add to allowed patterns**: If it's a legitimate exception (update the script)
4. **Remove the file**: If it's no longer needed

## Allowed Patterns

The validator considers these locations as standard and will not warn about them:

- **Root-level documentation**: `README.md`, `LICENSE`, `AGENTS.md`, `RETROSPECTIVE.md`
- **Main docs directory**: `docs/**/*.md` (all subdirectories)
- **Skill documentation**:
  - `skills/*/SKILL.md`
  - `skills/*/references/*.md`
  - `skills/*/examples/*.md`
  - `.claude/skills/*/SKILL.md`
  - `.claude/skills/*/references/*.md`
  - `.claude/skills/*/examples/*.md`

## Error Handling

### False Positives

**Symptom**: The validator warns about a file that should be allowed

**Solution**:
- Check if the file matches an allowed pattern
- If it's a legitimate location not covered by current patterns, update `doc-validator.sh`
- Add the new pattern to the `ALLOWED_PATTERNS` array

### Script Not Finding Files

**Symptom**: The script runs but finds no files or fewer files than expected

**Solution**:
- Verify you're running from the repository root
- Check file permissions
- Ensure `.md` files exist in the repository

### Permission Denied

**Symptom**: Script cannot access certain directories

**Solution**:
- Check directory permissions
- Ensure the script is executable: `chmod +x skills/doc-validator/scripts/doc-validator.sh`

## Notes

- **Non-destructive**: The script only reports issues, it does not move or delete files
- **Excludes**: Automatically skips `.git/` and `.synthesisflow-backup-*` directories
- **Integration**: Designed to be called by other skills as part of quality checks
- **Extensible**: Easy to add new allowed patterns by updating the script
- **CI-friendly**: Returns parsable output suitable for automated checks
