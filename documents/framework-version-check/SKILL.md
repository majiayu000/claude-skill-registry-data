---
name: framework_version_check
description: Validate version synchronization between claude.md and claude-reference.md to ensure framework documentation consistency and detect version drift
schema_version: 1.0
---

# framework_version_check

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** Medium

## Trigger Reference

This skill activates on:
- Keywords: "framework version", "claude.md version", "version mismatch", "version sync", "framework sync"
- Intent patterns: "check.*?framework.*?version", "version.*?(mismatch|sync|drift)"

From: `skill-rules.json` - framework_version_check configuration

## Purpose

Validate version synchronization between `claude.md` and `claude-reference.md` to ensure framework documentation consistency. This is an ANALYSIS-ONLY skill that detects version drift and recommends REPAIR tasks when needed.

## Core Behavior

In any DAIC mode (DISCUSS, ALIGN, IMPLEMENT, CHECK):

1. **Version Sync Validation**
   - Read `claude.md` header for Framework Version and Last Updated
   - Read `claude-reference.md` header for Framework Version and Last Updated
   - Compare versions and dates for consistency
   - Report sync status (matched, mismatched, or missing file)

2. **Drift Detection**
   - Identify which file has newer version
   - Detect date mismatches even if version matches
   - Flag missing `claude-reference.md` file
   - Warn about partial version information

3. **REPAIR Task Recommendation**
   - Suggest creating REPAIR- task for version drift
   - Provide context for the REPAIR task
   - Recommend which file should be authoritative
   - Guide conflict resolution process

4. **Preventive Guidance**
   - Remind to update both files when framework changes
   - Suggest version bump strategy (2.0 → 2.1, etc.)
   - Recommend including version in LCMP decisions.md

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ NEVER auto-fix version mismatches
- ✓ NEVER modify framework files directly
- ✓ Only provide analysis and recommendations
- ✓ Safe to run in any DAIC mode

**Version Checking Rules:**
- Always check BOTH files before reporting
- Handle missing files gracefully
- Never assume which file is authoritative
- Always recommend user decide resolution path
- Log version checks in context when significant

## Examples

### When to Activate

✓ "Check framework version sync"
✓ "Are claude.md and claude-reference.md in sync?"
✓ "I updated claude.md, did I forget something?"
✓ User is starting a new task (auto-check from Section 0.1)
✓ "Validate framework version"

### Typical Output

**Scenario 1: Versions Match**
```markdown
### Framework Version Check: ✓ SYNCED

**claude.md**
- Framework Version: 2.0
- Last Updated: 2025-11-15

**claude-reference.md**
- Framework Version: 2.0
- Last Updated: 2025-11-15

**Status:** Both files are synchronized. Proceeding normally.
```

**Scenario 2: Version Drift Detected**
```markdown
### Framework Version Check: ⚠️ DRIFT DETECTED

**claude.md**
- Framework Version: 2.1
- Last Updated: 2025-11-15

**claude-reference.md**
- Framework Version: 2.0
- Last Updated: 2025-11-10

**Issue:** Framework docs appear out of sync. claude.md is newer (v2.1) while claude-reference.md is still v2.0.

**Recommendation:**
Create a REPAIR-framework-sync task to:
1. Compare both files to understand what changed
2. Determine which version is authoritative
3. Update the other file to match
4. Log the resolution in context/gotchas.md

**Action:**
Would you like me to suggest a REPAIR task manifest?
```

**Scenario 3: Missing claude-reference.md**
```markdown
### Framework Version Check: ⚠️ INCOMPLETE

**claude.md**
- Framework Version: 2.0
- Last Updated: 2025-11-15

**claude-reference.md**
- Status: File not found

**Issue:** claude-reference.md is missing. The framework expects both files to exist.

**Recommendations:**
1. **If intentional:** Document in claude.md why claude-reference.md is not needed
2. **If unintentional:** Create claude-reference.md or locate it
3. **If renamed/moved:** Update claude.md Section 0.1 with new path

**Next Steps:**
- Verify if claude-reference.md should exist
- Create REPAIR task if framework structure changed
```

### When NOT to Activate

✗ User is asking about application version (not framework version)
✗ Question is about git version/commits
✗ Focus is on dependency versions (package.json)
✗ General version control questions

## Version Check Procedure

### 1. Extract Version from claude.md
```bash
# Line 2-3 format:
# Framework Version: 2.0
# Last Updated: 2025-11-15
```

### 2. Extract Version from claude-reference.md
```bash
# Same format in header
```

### 3. Compare
- Version numbers must match exactly (e.g., "2.0" === "2.0")
- Dates should match or be very close
- Both fields must be present

### 4. Report Findings
- **Match:** ✓ Proceed normally
- **Mismatch:** ⚠️ Suggest REPAIR task
- **Missing:** ⚠️ Explain issue, suggest resolution

## REPAIR Task Template

When version drift detected, suggest this task structure:

```markdown
## Task: REPAIR-framework-sync-2025-11-15

### Problem
Framework version mismatch detected:
- claude.md: v2.1 (2025-11-15)
- claude-reference.md: v2.0 (2025-11-10)

### Goals
1. Determine which version is authoritative
2. Identify what changed between versions
3. Update out-of-sync file to match
4. Document resolution

### Approach
1. Read both files completely
2. Diff to find changes
3. Decide: Is v2.1 correct? Or is v2.0 correct?
4. Update the other file
5. Log in context/gotchas.md what caused the drift
6. Suggest preventive measures

### Success Criteria
- Both files show same version and date
- Changes are semantically consistent
- Drift cause documented
- Prevention strategy noted
```

## Integration with Task Startup

Per claude.md Section 0.1, this skill should activate automatically when:
- Starting a new cc-sessions task
- User explicitly requests version check
- Framework files are being modified

## Decision Logging

When significant version drift is detected:

```markdown
### Framework Version Drift: [Date]
- **Detected:** claude.md v2.1, claude-reference.md v2.0
- **Resolution:** Created REPAIR-framework-sync task
- **Root Cause:** claude.md updated during REPAIR-write-gating but claude-reference.md forgotten
- **Prevention:** Add to REPAIR task checklist: "Update both framework files"
```

## Related Skills

- **framework_health_check** - For broader framework validation
- **framework_repair_suggester** - To create REPAIR tasks for drift
- **skill-developer** - If skill system version checking needed
- **cc-sessions-core** - If version checking logic needs enhancement

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
