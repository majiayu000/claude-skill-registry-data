---
name: verify-governance
description: Verify integrity and completeness of governance framework using workspace-schema.json as single source of truth - checks directories, files, and .gitignore against schema
---

# Verify Governance Framework

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
Using Skill: verify-governance | [brief purpose based on context]
```

**Example:**
```
Using Skill: verify-governance | Checking .wrangler/ structure compliance
```

This creates an audit trail showing which skills were applied during the session.

## Purpose

Governance frameworks can drift over time:
- Directories get renamed or go missing
- Files end up in wrong locations
- .gitignore patterns become incomplete
- Structure diverges from canonical schema

This skill performs systematic verification to detect and fix structural drift using `workspace-schema.json` as the single source of truth.

## What This Skill Checks

**IN SCOPE** (Structure and Existence):
- Directory structure matches `workspace-schema.json`
- Subdirectories exist where schema defines them
- Governance files exist at correct paths
- Files are in correct locations (not legacy paths)
- `.wrangler/.gitignore` exists with all required patterns

**OUT OF SCOPE** (Content Quality):
- File content/template compliance (future enhancement)
- Governance file sections/structure validation
- Cross-document link validation
- Template version mismatches
- Metrics staleness

This simplification focuses on answering: "Is the structure correct?" not "Is the content good?"

## Verification Workflow

### Phase 1: Load Schema

**Load workspace-schema.json as canonical structure:**

```bash
# Find wrangler installation (usually in current project or ~/.local/share/wrangler/)
WRANGLER_ROOT=$(pwd)
SCHEMA_PATH="$WRANGLER_ROOT/.wrangler/config/workspace-schema.json"

# Check if schema exists
if [ ! -f "$SCHEMA_PATH" ]; then
  echo "ERROR: workspace-schema.json not found at $SCHEMA_PATH"
  echo "This project may not have wrangler initialized."
  exit 1
fi

# Read schema (you'll parse this to extract directories, files, gitignore patterns)
cat "$SCHEMA_PATH"
```

**Parse key sections:**
- `directories` - Canonical directory structure
- `governanceFiles` - Required governance files
- `readmeFiles` - Directory README files
- `gitignorePatterns` - Patterns for .wrangler/.gitignore

### Phase 2: Detect Directory Drift

**Check each directory in schema:**

```bash
# For each directory in schema.directories:
# Example: .wrangler/issues, .wrangler/specifications, etc.

echo "=== Checking Directories ==="

# From schema, check all directories
for dir in .wrangler/issues .wrangler/specifications .wrangler/ideas .wrangler/memos \
           .wrangler/plans .wrangler/docs .wrangler/cache .wrangler/config .wrangler/logs; do
  if [ -d "$dir" ]; then
    echo "✓ $dir exists"
  else
    echo "✗ MISSING: $dir"
  fi
done

# Check subdirectories (from schema.directories[].subdirectories)
echo "=== Checking Subdirectories ==="
if [ -d ".wrangler/issues/completed" ]; then
  echo "✓ .wrangler/issues/completed exists"
else
  echo "✗ MISSING: .wrangler/issues/completed"
fi
```

**Detect legacy renamed directories:**

Common v1.0 → v1.2 migrations to detect:
- `.wrangler/issues/complete/` → `.wrangler/issues/completed/` (note: schema uses "completed", user may have "complete")
- `.wrangler/specifications/done/` → `.wrangler/specifications/archived/`
- `.wrangler/templates/` → (removed, templates now in skills/)

```bash
# Detect renamed directories
echo "=== Detecting Legacy Directory Names ==="

if [ -d ".wrangler/issues/complete" ]; then
  echo "⚠️ LEGACY: .wrangler/issues/complete/ should be renamed to .wrangler/issues/completed/"
fi

if [ -d ".wrangler/specifications/done" ]; then
  echo "⚠️ LEGACY: .wrangler/specifications/done/ should be renamed to .wrangler/specifications/archived/"
fi

if [ -d ".wrangler/templates" ]; then
  echo "⚠️ LEGACY: .wrangler/templates/ no longer used (templates in skills/*/templates/)"
fi
```

### Phase 3: Detect File Drift

**Check governance files from schema:**

```bash
echo "=== Checking Governance Files ==="

# From schema.governanceFiles
for file in .wrangler/CONSTITUTION.md .wrangler/ROADMAP.md .wrangler/ROADMAP_NEXT_STEPS.md; do
  if [ -f "$file" ]; then
    echo "✓ $file exists"
  else
    echo "ℹ️  OPTIONAL: $file (not required, but recommended)"
  fi
done

# From schema.readmeFiles
for file in .wrangler/issues/README.md .wrangler/specifications/README.md \
            .wrangler/memos/README.md .wrangler/plans/README.md; do
  if [ -f "$file" ]; then
    echo "✓ $file exists"
  else
    echo "ℹ️  MISSING: $file (consider creating)"
  fi
done
```

**Detect files in wrong locations:**

Common legacy file locations:
- `.wrangler/hooks-config.json` → `.wrangler/config/hooks-config.json`
- `.wrangler/workspace-schema.json` → `.wrangler/config/workspace-schema.json`

```bash
echo "=== Detecting Legacy File Locations ==="

if [ -f ".wrangler/hooks-config.json" ]; then
  echo "⚠️ LEGACY: .wrangler/hooks-config.json should be at .wrangler/config/hooks-config.json"
fi

if [ -f ".wrangler/workspace-schema.json" ]; then
  echo "⚠️ LEGACY: .wrangler/workspace-schema.json should be at .wrangler/config/workspace-schema.json"
fi
```

### Phase 4: Detect .gitignore Drift

**Check .wrangler/.gitignore:**

```bash
echo "=== Checking .wrangler/.gitignore ==="

if [ ! -f ".wrangler/.gitignore" ]; then
  echo "✗ MISSING: .wrangler/.gitignore"
  echo "   Required patterns: cache/, config/, logs/"
else
  echo "✓ .wrangler/.gitignore exists"

  # Check each pattern from schema.gitignorePatterns
  echo "=== Checking gitignore patterns ==="

  for pattern in "cache/" "config/" "logs/"; do
    if grep -q "^${pattern}$" .wrangler/.gitignore; then
      echo "✓ Pattern present: $pattern"
    else
      echo "✗ MISSING PATTERN: $pattern"
    fi
  done
fi
```

### Phase 5: Report Drift

**Compile findings into clear report:**

```markdown
# Governance Structure Verification Report

**Date**: [YYYY-MM-DD HH:MM]
**Schema Version**: [from workspace-schema.json version field]

---

## Summary

- **Status**: [✅ COMPLIANT / ⚠️ DRIFT DETECTED / ❌ CRITICAL ISSUES]
- **Missing Directories**: [N]
- **Missing Files**: [N]
- **Wrong Locations**: [N]
- **Missing Gitignore Patterns**: [N]

---

## Detailed Findings

### Missing Directories ([N])

- `.wrangler/issues/completed/` (required by schema)
- `.wrangler/cache/` (required by schema)

**Fix**: `mkdir -p .wrangler/issues/completed .wrangler/cache`

### Legacy Directory Names ([N])

- `.wrangler/issues/complete/` exists but schema expects `.wrangler/issues/completed/`
  - **Impact**: 12 files in old location
  - **Fix**: `mv .wrangler/issues/complete .wrangler/issues/completed`

- `.wrangler/specifications/done/` exists but schema expects `.wrangler/specifications/archived/`
  - **Impact**: 5 files in old location
  - **Fix**: `mv .wrangler/specifications/done .wrangler/specifications/archived`

### Wrong File Locations ([N])

- `.wrangler/hooks-config.json` should be at `.wrangler/config/hooks-config.json`
  - **Fix**: `mv .wrangler/hooks-config.json .wrangler/config/hooks-config.json`

### Missing Files ([N])

- `.wrangler/.gitignore` (required for proper git tracking)
  - **Fix**: Create with patterns: cache/, config/, logs/

**Note**: Governance files (CONSTITUTION.md, ROADMAP.md) are optional per schema.

### Missing Gitignore Patterns ([N])

- Pattern `sessions/` missing from `.wrangler/.gitignore`
  - **Fix**: Add to .gitignore

---

## Recommended Actions

[List specific commands to fix each issue, grouped by type]
```

### Phase 6: Get Permission

**Present user with 4 options:**

```
## How would you like to proceed?

1. **Fix all automatically** (recommended)
   - I'll apply all fixes shown above
   - Affected files will be moved/renamed
   - Directories will be created
   - .gitignore will be updated

2. **Show me the commands**
   - I'll display bash commands
   - You run them manually
   - Good for reviewing changes first

3. **Let me choose**
   - I'll ask about each fix individually
   - You approve or skip each one
   - Good for selective fixes

4. **Cancel**
   - No changes made
   - Exit verification

Please choose: [1/2/3/4]
```

**Wait for user response before proceeding.**

### Phase 7: Apply Fixes

**Option 1: Fix All Automatically**

```bash
echo "=== Applying All Fixes ==="

# Create missing directories
mkdir -p .wrangler/issues/completed
mkdir -p .wrangler/cache
echo "✓ Created missing directories"

# Rename legacy directories (only if they exist)
if [ -d ".wrangler/issues/complete" ]; then
  mv .wrangler/issues/complete .wrangler/issues/completed
  echo "✓ Renamed .wrangler/issues/complete/ → .wrangler/issues/completed/"
fi

# Move misplaced files
if [ -f ".wrangler/hooks-config.json" ]; then
  mkdir -p .wrangler/config
  mv .wrangler/hooks-config.json .wrangler/config/hooks-config.json
  echo "✓ Moved hooks-config.json to config/"
fi

# Create/update .gitignore
if [ ! -f ".wrangler/.gitignore" ]; then
  cat > .wrangler/.gitignore << 'EOF'
cache/
config/
logs/
EOF
  echo "✓ Created .wrangler/.gitignore"
else
  # Append missing patterns
  for pattern in "cache/" "config/" "logs/"; do
    if ! grep -q "^${pattern}$" .wrangler/.gitignore; then
      echo "$pattern" >> .wrangler/.gitignore
      echo "✓ Added pattern to .gitignore: $pattern"
    fi
  done
fi

echo "=== All Fixes Applied ==="
```

**Option 2: Show Commands**

Display the bash commands without executing:

```bash
echo "=== Commands to Fix Drift ==="
echo ""
echo "# Create missing directories"
echo "mkdir -p .wrangler/issues/completed"
echo "mkdir -p .wrangler/cache"
echo ""
echo "# Rename legacy directories"
echo "mv .wrangler/issues/complete .wrangler/issues/completed"
echo ""
echo "# Move misplaced files"
echo "mkdir -p .wrangler/config"
echo "mv .wrangler/hooks-config.json .wrangler/config/hooks-config.json"
echo ""
echo "# Create .gitignore"
echo "cat > .wrangler/.gitignore << 'EOF'"
echo "cache/"
echo "config/"
echo "logs/"
echo "EOF"
```

**Option 3: Let Me Choose**

Ask about each fix individually:

```
Fix: Create .wrangler/issues/completed/ directory
Apply this fix? [y/n]: _

[wait for user response]

Fix: Rename .wrangler/issues/complete/ → .wrangler/issues/completed/ (12 files)
Apply this fix? [y/n]: _

[and so on...]
```

**Option 4: Cancel**

```
No changes made. Verification report saved for reference.
Run /wrangler:verify-governance again when ready to fix drift.
```

### Phase 8: Re-Verify

**After applying fixes, run verification again:**

```bash
echo "=== Re-Running Verification ==="
echo ""

# Run Phases 2-4 again to confirm all drift resolved

echo "=== Final Status ==="

if [ all checks pass ]; then
  echo "✅ All drift resolved! Governance structure now compliant."
else
  echo "⚠️ Some issues remain:"
  # List remaining issues
fi
```

## Legacy Migration Detection

This skill specifically handles v1.0 → v1.2 migration drift:

| Legacy Location | Current Location | Detection Method |
|-----------------|------------------|------------------|
| `.wrangler/issues/complete/` | `.wrangler/issues/completed/` | Directory exists check |
| `.wrangler/specifications/done/` | `.wrangler/specifications/archived/` | Directory exists check |
| `.wrangler/hooks-config.json` | `.wrangler/config/hooks-config.json` | File exists check |
| `.wrangler/workspace-schema.json` | `.wrangler/config/workspace-schema.json` | File exists check |
| `.wrangler/templates/` | `skills/*/templates/` | Directory exists check (now unused) |

When detected, offer to migrate automatically.

## Edge Cases

### No workspace-schema.json

**Situation**: Schema file doesn't exist

**Response**:
```
ERROR: workspace-schema.json not found at .wrangler/config/workspace-schema.json

This project may not have wrangler v1.2+ initialized.

Options:
1. Run /wrangler:initialize-governance to set up governance
2. Manually create .wrangler/config/workspace-schema.json from template
3. Update wrangler to latest version
```

### Partial .wrangler/ Setup

**Situation**: Some directories exist, others don't

**Response**: Report exactly what's missing, offer to create all at once.

### .gitignore Has Extra Patterns

**Situation**: .gitignore has more patterns than schema requires

**Response**: This is fine. Only report MISSING patterns, never complain about extras.

### Schema Version Mismatch

**Situation**: Schema version field doesn't match wrangler version

**Response**: Report version mismatch as informational only, don't block.

### Empty Directories

**Situation**: Required directory exists but is empty

**Response**: Directory exists = success. Empty is fine (issues/specs may not exist yet).

## Success Criteria

Verification is complete when:

- [ ] workspace-schema.json loaded successfully
- [ ] All directories checked against schema
- [ ] All subdirectories checked against schema
- [ ] All governance files checked against schema
- [ ] All README files checked against schema
- [ ] .gitignore existence and patterns validated
- [ ] Legacy directory/file locations detected
- [ ] Drift report generated with specific fixes
- [ ] User permission obtained (or cancelled)
- [ ] Fixes applied (if approved)
- [ ] Re-verification confirmed success (if fixes applied)

## Output Format

Always provide:

1. **Executive Summary**: Quick status (✅/⚠️/❌) with counts
2. **Detailed Findings**: Broken down by category
3. **Specific Fixes**: Exact commands or actions for each issue
4. **Permission Prompt**: 4 clear options
5. **Confirmation**: Re-verification results after fixes

## Related Skills

- **initialize-governance** - For creating governance files from scratch
- **refresh-metrics** - For updating metrics in README files (content, not structure)

## Design Principles

**Single Source of Truth**:
- Structure defined ONLY in workspace-schema.json
- Skill reads schema, never hardcodes structure
- When wrangler structure changes, only schema updates

**Simplicity**:
- Focus on "does it exist?" and "is it in the right place?"
- No content/quality validation (future enhancement)
- Clear binary checks, no ambiguity

**User Agency**:
- Always ask permission before changes
- Provide multiple options (auto, manual, selective, cancel)
- Show exactly what will happen before it happens

**Idempotency**:
- Can run multiple times safely
- Re-verification confirms fixes worked
- No harm if run on compliant structure

## Remember

This skill validates STRUCTURE ONLY. It doesn't care about:
- Whether CONSTITUTION.md is well-written
- Whether metrics are up to date
- Whether links between docs work
- Whether templates match current versions

Those are future enhancements. Focus: "Is the directory structure and file organization correct per the schema?"
