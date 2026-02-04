---
name: update-workspace-map
description: Validate workspace-map.md accuracy against actual 04-workspace/ structure (3 levels deep). Load when user says "validate workspace map", "update workspace map", "check workspace map", or from close-session. Ensures deep structure validation with comprehensive documentation.
---

# Validate Workspace Map

Ensure workspace-map.md stays synchronized with actual 04-workspace/ folder structure up to 3 levels deep.

## Purpose

The workspace-map.md file helps AI understand your custom folder organization in 04-workspace/. When it becomes stale (folders added/removed/reorganized but not documented), AI navigation becomes unreliable.

This skill:
- Scans workspace structure **3 levels deep** (root → level 1 → level 2 → level 3)
- Compares actual folders with documented folders at all levels
- Identifies mismatches (missing or extra folders, incorrect nesting)
- Provides detailed structure report with depth indicators
- Guides you through comprehensive updates
- Validates accuracy after changes

**Improvements over v1**:
- ✅ **3-layer deep scanning** (vs 1 layer)
- ✅ **Hierarchical validation** (parent-child relationships)
- ✅ **File detection** (warns about files that should be documented)
- ✅ **Depth indicators** in reports (├──, │  ├──, │  │  ├──)
- ✅ **Comprehensive documentation** prompts for nested structures

**When to use**:
- You reorganized 04-workspace/ folders
- You notice AI can't find your folders
- During onboarding (Project 03, Task 5.6)
- As part of regular maintenance (via close-session)

---

## Workflow

### Step 1: Scan Actual Workspace Structure (3 Levels Deep)

**Scan workspace recursively** (up to 3 levels):
```bash
find 04-workspace -maxdepth 3 -type d | sort
```

**Parse into hierarchical structure**:
```
04-workspace/
├── input/
│   ├── skills/
│   │   ├── examples/
│   │   └── templates/
│   └── docs/
├── clients/
│   ├── acme/
│   │   ├── deliverables/
│   │   └── notes/
│   └── globex/
└── templates/
```

**Also scan for important files** (for documentation warnings):
```bash
find 04-workspace -maxdepth 3 -type f -name "*.md" -o -name "README*" | sort
```

**Store**:
- ACTUAL_STRUCTURE (tree with 3 levels)
- IMPORTANT_FILES (markdown/README files)

**Exclude**:
- Hidden folders (., .., .git, .DS_Store)
- workspace-map.md itself
- System folders

**Time**: 10 seconds

---

### Step 2: Parse workspace-map.md (3 Levels Deep)

**Read**: 04-workspace/workspace-map.md

**Extract documented structure**:
1. **From tree structure** (in "Your Workspace Structure" section):
   - Parse lines with `├──`, `│  ├──`, `│  │  ├──` (depth indicators)
   - Build hierarchical tree from indentation
   - Capture folder descriptions (inline comments with `#`)

2. **From folder descriptions** (in "Folder Descriptions" section):
   - Parse `###` headers (level 1 folders)
   - Parse `####` headers (level 2 folders)
   - Parse `#####` headers (level 3 folders)
   - Extract purpose, contents, and notes

3. **Cross-reference** both sections for completeness

**Store**:
- MAPPED_STRUCTURE (tree with 3 levels)
- MAPPED_DESCRIPTIONS (folder purposes and details)

**Time**: 10 seconds

---

### Step 3: Deep Comparison (Hierarchical)

**Compare at each level**:

**Level 1** (04-workspace/ direct children):
- Missing from map
- Extra in map (stale)
- Matches

**Level 2** (within each level 1 folder):
- For each level 1 folder, compare children
- Track parent-child relationships
- Identify orphaned level 2 folders (parent missing)

**Level 3** (within each level 2 folder):
- For each level 2 folder, compare children
- Validate full path accuracy
- Identify deeply nested mismatches

**Identify**:
- **Missing folders** (at each level)
- **Extra folders** (stale documentation at each level)
- **Hierarchy issues** (documented under wrong parent)
- **Undocumented files** (important .md files with no description)
- **Perfect match** (all levels accurate)

**Time**: 5 seconds

---

### Step 4: Generate Comprehensive Report

Show detailed validation results at all 3 levels with clear depth indicators and actionable feedback.

---

## Total Time Estimates

**Scenarios**:
- **Perfect match** (3 levels): ~20 seconds
- **Minor updates** (1-2 folders): 2-3 minutes  
- **Major reorganization** (5+ folders): 5-7 minutes
- **Deep restructure** (many level 2-3 changes): 8-10 minutes

---

## Integration

### close-session Integration

This skill is automatically triggered during close-session. If mismatches found, prompts user to update.

---

**Remember**: Deep 3-level validation = Comprehensive AI navigation!
