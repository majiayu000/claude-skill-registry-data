---
name: validate-docs-implementation
description: Load when user says "validate docs", "check documentation consistency", "docs vs implementation", or "find documentation mismatches". Systematically compares implementation code against documentation to identify and fix inconsistencies.
---

# Validate Documentation vs Implementation

**Purpose**: Systematically identify and fix mismatches between actual implementation code and documentation.

**Load When**:
- User says: "validate docs", "check documentation", "docs vs implementation"
- User mentions: "documentation mismatch", "docs don't match code"
- After major code changes that may affect docs
- During pre-release validation

**Core Value**: Ensures documentation accurately reflects actual implementation, preventing user confusion and wasted debugging time.

---

## Quick Reference

**What This Skill Does**:
1. ✅ Analyzes implementation code (scripts, core logic)
2. ✅ Identifies what the code actually creates/does
3. ✅ Searches all documentation for references to those entities
4. ✅ Compares documented behavior vs actual behavior
5. ✅ Fixes all mismatches systematically
6. ✅ Provides summary of changes made

**Typical Mismatches Found**:
- File names (e.g., docs say "design.md" but code creates "plan.md")
- Folder structure (e.g., docs missing "02-resources/" directory)
- Counts (e.g., docs say "3 files" but script creates "4 directories + 3 files")
- Naming conventions (e.g., old vs new terminology)
- References to deprecated features

---

## Workflow: 5-Step Validation Process

### Step 1: Analyze Implementation

**Goal**: Understand what the code actually does

**Actions**:
1. Read the implementation file(s) identified by user
2. Document exactly what it creates/generates/does:
   - Files created (names, locations, count)
   - Folders created (names, structure, count)
   - Data structures used
   - Behavior patterns
3. Create a reference list of "ground truth" facts

**Example Output**:
```markdown
## Implementation Analysis: init_project.py

**Creates**:
- 4 directories: 01-planning/, 02-resources/, 03-working/, 04-outputs/
- 3 files in 01-planning/: overview.md, plan.md, steps.md

**Does NOT create**:
- design.md (old name)
- tasks.md (old name)
- requirements.md (never existed)
```

---

### Step 2: Search Documentation

**Goal**: Find all references to the entities/behavior

**Actions**:
1. Use Grep to search for old/mismatched terms across documentation:
   ```bash
   # Search for old file names
   grep -r "design\.md\|tasks\.md\|requirements\.md" 00-system/

   # Search for old folder structure
   grep -r "02-working\|03-outputs" 00-system/
   ```

2. Identify all files that contain references
3. For each file, note line numbers and context

**Output**: List of files needing updates with specific locations

---

### Step 3: Compare & Identify Mismatches

**Goal**: Categorize what needs fixing

**Actions**:
1. For each documentation file found:
   - Read the relevant sections
   - Compare against implementation truth
   - Categorize mismatch type:
     - **File name mismatch**: Wrong file names referenced
     - **Structure mismatch**: Wrong folder structure shown
     - **Count mismatch**: Wrong counts ("3 files" vs "4 directories + 3 files")
     - **Missing info**: Implementation creates X but docs don't mention it

2. Prioritize fixes:
   - Critical: User-facing docs, core system maps
   - Important: Skill workflows, reference materials
   - Nice-to-have: Examples, comments

---

### Step 4: Fix All Mismatches

**Goal**: Update documentation to match implementation

**Actions**:
1. For each file with mismatches:
   - Read the file
   - Use Edit tool to fix each mismatch
   - Preserve context and formatting
   - Update related references (e.g., if fixing folder name, update all mentions)

2. Common fix patterns:
   ```markdown
   # File name fixes
   OLD: "design.md"  → NEW: "plan.md"
   OLD: "tasks.md"   → NEW: "steps.md"

   # Structure fixes
   OLD: "02-working/" → NEW: "03-working/"
   OLD: "03-outputs/" → NEW: "04-outputs/"
   ADD: "02-resources/" (was missing)

   # Count fixes
   OLD: "3 core files"
   NEW: "4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/) + 3 planning files"
   ```

3. Track progress with TodoWrite:
   - Mark each file as completed after fixing
   - Maintains visibility for user

---

### Step 5: Verify & Generate Report

**Goal**: Confirm all fixes are consistent and create permanent validation record

**Actions**:

**5A. Verification**:
1. Re-search for old terms to verify they're gone:
   ```bash
   grep -r "design\.md" 00-system/  # Should return no results
   ```

2. Spot-check fixed files to ensure consistency

**5B. Determine Report Location**:

First time or if location not set:
```markdown
AI: "Where should I save validation reports? Options:
    1. 04-workspace/validation-reports/ (recommended - organized, searchable)
    2. 01-memory/validation-reports/ (persistent record)
    3. Custom location (you specify)

    Or say 'skip' to not save reports."

User: [Chooses option]

AI: "Got it! I'll save reports to [location]. This will be remembered for future validations."
```

If location already configured (from previous validation):
```markdown
AI: "Saving report to configured location: [location]"
```

**5C. Generate & Save Report**:

1. Create validation report using template (see `references/report-template.md`)
2. Generate filename: `validation-{implementation}-YYYY-MM-DD.md`
   - Example: `validation-init-project-2025-11-24.md`
3. Save to configured location
4. Display summary to user with link to full report

**Report includes**:
- Implementation analyzed
- Files updated (with line-by-line changes)
- Mismatch breakdown by type
- Verification results
- Status and next steps

**Example output**:
```markdown
✅ Validation complete!

**Summary**:
- 6 files updated
- 23 total fixes
- 0 grep results for old terms

📄 Full report saved: [04-workspace/validation-reports/validation-init-project-2025-11-24.md](04-workspace/validation-reports/validation-init-project-2025-11-24.md)
```

---

## Common Validation Scenarios

### Scenario 1: Script Creates Different Files Than Documented

**Symptoms**:
- User reports "docs mention design.md but I don't see it"
- Script creates files not mentioned in docs

**Process**:
1. Read script to see what it actually creates
2. Search docs for old file names
3. Replace all references systematically

**Example**: The create-project validation we just did

---

### Scenario 2: Folder Structure Changed

**Symptoms**:
- Documentation shows old folder structure
- New folders not mentioned in docs

**Process**:
1. Check actual project structure (ls)
2. Compare against documented structure
3. Update all structure diagrams and references

---

### Scenario 3: Counts/Descriptions Wrong

**Symptoms**:
- "Creates 3 files" but actually creates more
- Missing important details about what's created

**Process**:
1. Count actual artifacts created
2. Find all count references in docs
3. Update with complete, accurate descriptions

---

## Best Practices

### Be Systematic
- Don't skip steps or assume you've found everything
- Use grep to search exhaustively
- Check related files (if you fix system-map.md, check framework-overview.md too)

### Preserve Context
- Don't just fix the immediate error
- Update related references nearby
- Ensure examples/diagrams stay consistent

### Use Parallel Searches
- When searching for multiple patterns, use multiple Grep calls in parallel
- Saves time and provides complete picture faster

### Track Progress
- Use TodoWrite to show user what's being fixed
- Mark items complete as you go
- Provides transparency and confidence

### Verify Fixes
- Re-search for old terms after fixing
- Spot-check that new terminology is consistent
- Run validation commands if available

---

## Integration Points

- **After code changes**: Run this validation before committing
- **Pre-release**: Validate all docs match current implementation
- **User reports mismatch**: Use this skill to fix comprehensively
- **Documentation updates**: Verify changes didn't introduce new mismatches

---

## Success Criteria

✅ **Zero grep results** for old/deprecated terms
✅ **All structure diagrams** match actual folder structure
✅ **All counts** match actual artifact counts
✅ **All file references** use current names
✅ **User can follow docs** without confusion

---

**Remember**: Documentation debt compounds quickly. Fix mismatches systematically and completely the first time!
