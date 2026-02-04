---
name: vault-folder-health
description: Analyze vault organization by folder structure. Triggers on "folder health", "folder analysis", "vault organization", "folder structure".
auto_trigger: true
trigger_keywords:
  - "folder health"
  - "folder analysis"
  - "vault organization"
  - "folder structure"
  - "organize vault"
  - "folder stats"
  - "check folders"
  - "vault folders"
  - "folder report"
  - "folder breakdown"
  - "directory health"
  - "how organized"
  - "folder balance"
  - "note distribution"
  - "folder hierarchy"
  - "vault layout"
allowed-tools: mcp__flywheel__get_folder_structure
---

# Folder Health Skill

Analyze vault organization by folder structure using Flywheel MCP.

## Purpose

This skill helps you:
- Find empty folders (candidates for cleanup)
- Identify overloaded folders (needs splitting)
- Detect shallow folders (maybe consolidate)
- Analyze folder depth and hierarchy
- Understand vault organization patterns

## When to Use

Invoke when you want to:
- **Check vault organization**: "folder health" or "vault organization"
- **Find organizational issues**: "check folders" or "folder analysis"
- **Plan restructuring**: "folder structure" or "organize vault"
- **Quarterly maintenance**: As part of vault gardening routine

## Process

### 1. Call MCP Tool

```
Call: mcp__flywheel__get_folder_structure
Parameters: {}
```

### 2. Analyze Folder Health

Categorize folders by health status:

**Empty Folders (CLEANUP CANDIDATES)**
- `note_count: 0` AND `subfolder_count: 0`
- Action: Consider deleting if truly unused

**Container Folders (NORMAL)**
- `note_count: 0` BUT `subfolder_count > 0`
- Action: This is expected for organization

**Overloaded Folders (NEEDS SPLITTING)**
- `note_count > 50` AND `subfolder_count: 0`
- Action: Consider splitting into subcategories

**Shallow Folders (CONSIDER CONSOLIDATING)**
- `note_count: 1-2` AND `subfolder_count: 0`
- Action: Maybe merge into parent or related folder

**Healthy Folders**
- `note_count: 3-50` AND sensible depth
- Action: No action needed

### 3. Calculate Folder Metrics

**Depth Analysis:**
```
Level 1 (top-level): work/, tech/, personal/
Level 2: work/projects/, tech/tools/
Level 3: work/projects/active/
Max Depth: 5 levels (flag if deeper)
```

**Distribution:**
```
Total folders: 100
Empty: 5 (5%)
Container: 20 (20%)
Overloaded: 3 (3%)
Shallow: 25 (25%)
Healthy: 47 (47%)
```

### 4. Display Report

```
Folder Health Report
═══════════════════════════════════════════════
Total Folders: 100

CLEANUP CANDIDATES (5)
Empty folders with no notes or subfolders:
- old-projects/archive
- temp/scratch
- misc/unsorted
Action: Review and delete if no longer needed

OVERLOADED FOLDERS (3)
Folders with 50+ notes (consider splitting):
- work/tickets (100+ notes) - Consider: by year or by status
- tech/tools (80 notes) - Consider: tech/tools/cloud/, tech/tools/local/
- daily-notes (365 notes) - Normal for time-based folders

SHALLOW FOLDERS (25)
Folders with only 1-2 notes (consider consolidating):
- tech/temp (1 note)
- projects/ideas (2 notes)
Action: Review if these need dedicated folders

FOLDER DEPTH
Max depth: 4 levels (healthy)
Deepest paths:
- work/projects/active/data-platform (4 levels)

SUMMARY
Healthy: 47 folders (47%)
Container: 20 folders (20%) - Normal organization
Needs attention: 33 folders (33%)
═══════════════════════════════════════════════
```

## Health Scoring

Calculate overall folder health score:

```python
base_score = 100
deductions = {
    'empty': empty_count * 2,        # -2% per empty folder
    'overloaded': overloaded_count * 5,  # -5% per overloaded folder
    'shallow': shallow_count * 1,    # -1% per shallow folder
}

folder_health_score = base_score - sum(deductions.values())
```

**Score Interpretation:**
- 90-100%: Excellent organization
- 75-89%: Good organization
- 60-74%: Fair organization (minor improvements needed)
- <60%: Poor organization (restructuring recommended)

## Related Skills

- **health**: Overall vault health (this skill focuses on folders)
- **stale**: Find stale notes (complements folder analysis)
- **clusters**: Find topic clusters (alternative organization view)

## Use Cases

### 1. Quarterly Vault Review
**Command:** "folder health"
**Result:** Full folder health report with recommendations

### 2. Before Restructuring
**Command:** "folder analysis"
**Result:** Understand current organization before making changes

### 3. After Major Import
**Command:** "check folders"
**Result:** See if imported notes created organizational issues

### 4. Vault Cleanup
**Command:** "vault organization"
**Result:** Identify cleanup opportunities (empty/shallow folders)

## Performance

- **MCP call**: ~100-200ms
- **Analysis**: ~50-100ms for 100+ folders
- **Total**: Usually <1 second

---

**Version:** 1.0.0
