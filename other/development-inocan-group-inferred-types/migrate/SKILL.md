---
name: migrate
description: Migrate a docent v0.9 project to v1.0 skills-based architecture
group: docent
keywords: [migration, upgrade, v0.9, v1.0, migrate docent, upgrade docent]
version: 1.0.0
author: docent
---

# Migrate Docent v0.9 → v1.0

This skill guides you through migrating an existing docent v0.9 project to the new v1.0 skills-based architecture.

## Purpose

Convert legacy runbooks and templates to the new skills format, update configuration, and maintain backward compatibility.

## Prerequisites

- Existing `.docent/` directory (v0.9 format)
- Write permissions to project directory
- Git repository (recommended for version control)

## Migration Overview

**What changes:**

- `runbooks/*.md` → `skills/{group}/{name}/SKILL.md`
- `templates/*.md` → Skills can still use bundled templates
- `config.yaml` → Add `version` and `skills` fields
- Legacy directories backed up, not deleted

**What stays the same:**

- `.docent/` root directory location
- Search paths configuration
- Journal and session directories
- Template usage (bundled templates still work)

## Procedure

### Step 1: Detect Current Version

**Action:** Check if migration is needed

```bash
# Check for version field in config
if grep -q "^version:" .docent/config.yaml 2>/dev/null; then
  echo "Already on v1.0 or later"
  exit 0
fi

# Check for legacy structure
if [ -d ".docent/runbooks" ] || [ -d ".docent/templates" ]; then
  echo "v0.9 detected - migration needed"
fi
```

**Decision Point:**

- If version exists in config → Already migrated, exit
- If runbooks/ or templates/ exist → Proceed with migration
- If neither → New project, use bootstrap instead

---

### Step 2: Backup Existing Content

**Action:** Create timestamped backup before making changes

```bash
# Create backup directory with timestamp
BACKUP_DIR=".docent/.backup-$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup runbooks if they exist
if [ -d ".docent/runbooks" ]; then
  cp -r .docent/runbooks "$BACKUP_DIR/"
  echo "Backed up runbooks to $BACKUP_DIR/runbooks/"
fi

# Backup templates if they exist
if [ -d ".docent/templates" ]; then
  cp -r .docent/templates "$BACKUP_DIR/"
  echo "Backed up templates to $BACKUP_DIR/templates/"
fi

# Backup config
if [ -f ".docent/config.yaml" ]; then
  cp .docent/config.yaml "$BACKUP_DIR/config.yaml.bak"
  echo "Backed up config to $BACKUP_DIR/config.yaml.bak"
fi
```

**Validation:**

- Backup directory created
- All existing content preserved
- User can revert if needed

---

### Step 3: Analyze Existing Content

**Action:** Inventory what needs to be migrated

```bash
# Count runbooks
RUNBOOK_COUNT=$(find .docent/runbooks -name "*.md" 2>/dev/null | wc -l)

# Count templates
TEMPLATE_COUNT=$(find .docent/templates -name "*.md" 2>/dev/null | wc -l)

echo "Found:"
echo "  - $RUNBOOK_COUNT custom runbooks"
echo "  - $TEMPLATE_COUNT custom templates"
```

**Report to user:**

- Number of runbooks to convert
- Number of templates (note: templates don't need conversion, bundled still work)
- Estimated time (1-2 minutes per runbook)

---

### Step 4: Convert Runbooks to Skills

**Action:** Transform each runbook into a skill

**For each runbook in `.docent/runbooks/*.md`:**

1. **Parse frontmatter** to get name and metadata
2. **Determine group** based on name or content:
   - `git-*` → `git/`
   - `github-*` → `github/`
   - `health-*`, `bootstrap`, `doctor` → `project/`
   - Everything else → `docent/`
3. **Create skill directory:** `.docent/skills/{group}/{name}/`
4. **Convert frontmatter:**
   - `type: runbook` → `group: {detected_group}`
   - `tags: [...]` → `keywords: [...]`
   - Add `version: 1.0.0` if not present
5. **Write SKILL.md** with updated frontmatter

**Example conversion:**

**Before** (`.docent/runbooks/git-commit.md`):

```yaml
---
name: git-commit
description: Create professional git commits
type: runbook
tags: [git, commit]
---
```

**After** (`.docent/skills/git/git-commit/SKILL.md`):

```yaml
---
name: git-commit
description: Create professional git commits
group: git
keywords: [git, commit, commits]
version: 1.0.0
---
```

**Implementation:**

For each runbook file:

1. Read frontmatter and content
2. Detect appropriate group
3. Update frontmatter fields
4. Create skill directory structure
5. Write SKILL.md file
6. Log conversion

---

### Step 5: Update Configuration

**Action:** Add v1.0 fields to config.yaml

**Read existing config**, then add/update:

```yaml
# Add version field at top
version: "1.0.0"

# Keep existing root and search_paths unchanged

# Add skills section based on what was migrated
skills:
  - docent/*      # Always include
  - project/*     # Always include
  - git/*         # If git runbooks found
  - github/*      # If github runbooks found
```

**Smart skill detection:**

- Scan converted skills to determine which groups were created
- Only enable skill groups that have content
- Add comments explaining glob patterns

**Implementation:**

1. Parse existing config.yaml
2. Add `version: "1.0.0"` at top
3. Analyze migrated skills to determine groups
4. Add `skills:` section with appropriate patterns
5. Write updated config
6. Validate YAML syntax

---

### Step 6: Verify Migration

**Action:** Confirm all content was migrated successfully

**Checklist:**

- [ ] `.docent/config.yaml` has `version: "1.0.0"`
- [ ] `.docent/config.yaml` has `skills:` array
- [ ] All runbooks converted to `.docent/skills/{group}/{name}/SKILL.md`
- [ ] Backup created in `.docent/.backup-*/`
- [ ] No data loss (backup contains originals)

**Test skill loading:**

```bash
# Test that skills load correctly
# Agent should be able to discover migrated skills
```

**Validation commands:**

```bash
# Count skills created
find .docent/skills -name "SKILL.md" | wc -l

# Verify config is valid YAML
cat .docent/config.yaml
```

---

### Step 7: Report Results

**Action:** Show migration summary to user

**Success Message:**

```
✅ Migration to v1.0 complete!

Migrated:
  - {N} runbooks → skills
  - Config updated with version and skills

Created:
  .docent/skills/
    ├── git/          {N} skills
    ├── github/       {N} skills
    ├── project/      {N} skills
    └── docent/       {N} skills

Backup:
  - Original files preserved in .docent/.backup-{timestamp}/
  - Safe to delete after verifying migration

Next steps:
  1. Test skill discovery: "how do I commit changes?"
  2. Verify migrated skills work correctly
  3. Delete .docent/runbooks/ when confident (optional)
  4. Delete .docent/templates/ when confident (optional - bundled still work)
  5. Commit migration: git add .docent/ && git commit -m "chore: migrate to docent v1.0"

Note: Legacy runbooks and templates are NOT deleted automatically.
You can keep them for reference or delete manually after testing.
```

---

## Error Handling

### No .docent/ Directory

**If:** Project doesn't have `.docent/` directory

**Fix:** Use bootstrap instead:

```
Agent should run: docent act bootstrap
```

### Already Migrated

**If:** Config already has `version: "1.0.0"`

**Fix:** Report already migrated, show current config

### Invalid Frontmatter

**If:** Runbook has malformed frontmatter

**Fix:**

1. Skip that runbook
2. Log warning with filename
3. Continue with others
4. Report skipped files in summary

### Backup Fails

**If:** Cannot create backup directory

**Fix:**

1. Check permissions
2. Try alternate backup location
3. If fails, abort migration (don't proceed without backup)

---

## Migration Options

### Minimal Migration (Recommended)

Only update config, keep using bundled skills:

```yaml
skills:
  - docent/*
  - git/*
  - github/*
  - project/*
```

Migrated custom runbooks go to `.docent/skills/` and override bundled.

### Selective Migration

Migrate only specific runbooks:

1. Copy desired runbooks to skills format
2. Enable only their groups in config
3. Keep others in legacy format

### Full Cleanup

After verifying migration:

```bash
# Delete legacy directories
rm -rf .docent/runbooks
rm -rf .docent/templates

# Delete backup (only after thorough testing!)
rm -rf .docent/.backup-*
```

---

## Notes

- **Idempotent:** Safe to re-run (checks version first)
- **Non-destructive:** Original files backed up, not deleted
- **Backward compatible:** Bundled templates still work
- **Incremental:** Can migrate one runbook at a time
- **Reversible:** Restore from `.docent/.backup-*/` if needed

---

## Advanced: Group Detection Logic

**Automatic group assignment based on filename:**

```
git-*        → git/
github-*     → github/
bootstrap    → project/
health-*     → project/
doctor       → project/
commit       → git/
issue        → github/
pr-*         → github/
pull-*       → github/
default      → docent/
```

**Can override with frontmatter:**

```yaml
---
name: custom-workflow
group: git  # Explicitly set group
---
```

---

## Validation

After migration:

1. ✅ Skills discoverable via `/docent:ask "upgrade docent"`
2. ✅ Migrated skills load and display correctly
3. ✅ Config valid YAML with version and skills
4. ✅ No data loss (originals in backup)
5. ✅ Agent can follow migrated skill instructions
