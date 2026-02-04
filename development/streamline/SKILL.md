---
name: streamline
description: Identifies files over 300 lines and decomposes them into smaller modules while preserving functionality exactly. Use when user says "streamline", "decompose files", "refactor large files", or wants to break down oversized source files.
disable-model-invocation: true
---

# Streamline Skill

Autonomously identifies oversized source files (>300 lines), creates decomposition plans, and implements refactoring while preserving functionality exactly.

## References Folder

Location: `.claude/skills/streamline/references/`

- **file-inventory.json** - Single source of truth for file state (line counts, exceptions, decomposed history)
- **config.json** - Optional project overrides (only create if customizing defaults)

## Default Configuration

Embedded defaults (override via `references/config.json` if needed):
- `lineThreshold`: 300 (files above this need decomposition)
- `targetLineCount`: 200 (aim for this after decomposition)
- `backupPath`: "deprecated" (where backups go)
- Auto-detect source root (looks for `src/` directory)
- Auto-detect file extensions based on project type

---

## Workflow

### Step 1: Load or Initialize Inventory

**If `references/file-inventory.json` doesn't exist:**
1. Auto-detect source root (find `src/` directory, or use project root)
2. Auto-detect file extensions (scan for .py, .vue, .js, .ts, .tsx)
3. Count lines in all matching files
4. Create initial inventory JSON

**If inventory exists but `lastScanned` is not today:**
1. Re-scan all files in the source root
2. Update line counts for existing files
3. Add any new files discovered
4. Remove files that no longer exist
5. Update `lastScanned` to today's date

### Step 2: Select Candidate

From files in inventory:
1. Filter to files with `lines > 300`
2. Exclude paths in `exceptions` array
3. Exclude paths in `decomposed` array
4. Select the **largest** remaining file

**If no candidates remain:** Report "No files need decomposition" and exit successfully.

### Step 3: Decompose (Interactive Mode)

1. **Analyze the file** - Read and understand its structure
2. **Create decomposition plan:**
   - Break into smaller files, each ≤200 lines
   - Group by logical area of concern
   - Preserve all functionality exactly
3. **Present plan to user** - Explain the logical groupings
4. **Wait for approval** before proceeding
5. **Create backup** in `deprecated/` folder with date prefix (e.g., `2025-12-19-tray.py`)
6. **Decompose:**
   - Create new helper/utility modules
   - Update original file to import from new modules
   - Ensure all imports and references are correct
7. **Update inventory:**
   - Add original path to `decomposed` array
   - Update line counts for all affected files
8. **Suggest tests** for user to verify functionality

### Step 4: Decompose (YOLO Mode)

Same as Step 3 but:
- Skip approval step - proceed immediately
- Auto-select best candidate (largest file)
- Skip test suggestions
- Commit and push changes (see YOLO Mode section)

---

## YOLO Mode

**Trigger:** Invoked with "yolo" argument or from CI/automated workflow.

When in YOLO mode, complete the entire workflow autonomously:

### Autonomous Workflow

1. **Load inventory** - Initialize or update as needed
2. **Select candidate** - Choose largest file over 300 lines
3. **Create decomposition plan** - Design without waiting for approval
4. **Decompose** - Create backup and refactor
5. **Update inventory** - Record the decomposition
6. **Commit and push changes**

### Git Operations (YOLO Mode Only)

After successful decomposition:

```bash
# Ensure on main branch with latest
git checkout main
git pull origin main

# Stage all changes
git add -A

# Commit with descriptive message
git commit -m "refactor: decompose [filename] into smaller modules

- Created [list new modules]
- Original file reduced from X to Y lines
- Backup saved to deprecated/

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to main
git push origin main
```

**CRITICAL:** Do NOT exit without pushing. Unpushed commits will be lost.

### No Changes Scenario

If no files need decomposition:
- Report success without making commits
- Exit cleanly

---

## Decomposition Guidelines

### File Size Targets
- Files >300 lines → decompose
- Target ≤200 lines per new module
- Original file should import from new modules

### Logical Grouping
- Group by area of concern (e.g., UI, data, utilities)
- Keep related functions together
- Maintain clear module boundaries

### Naming Conventions
- New modules: descriptive names reflecting their purpose
- Use existing project patterns
- Avoid generic names like `utils.py` or `helpers.js`

### DRY vs KISS
- Apply DRY (Don't Repeat Yourself) where beneficial
- But prioritize KISS (Keep It Simple) over DRY when:
  - Abstraction adds significant complexity
  - Code becomes less readable
  - Maintenance burden increases

---

## Constraints

**Absolute requirements:**
- **NO functional changes** - Reproduce existing functionality exactly
- **NO design changes** - Preserve visual appearance exactly
- **NO behavioral changes** - Maintain all existing behavior
- **Create dated backup** before decomposing any file
- **Use forward slashes** in all paths (cross-platform)

**Linting:**
- Interactive mode: Delegate to beautifier agent after completion
- YOLO mode: Rely on pre-commit hooks

---

## Exception Management

### Adding Exceptions

To exempt a file from decomposition:

1. Add path to `exceptions` array in `file-inventory.json`:
```json
"exceptions": ["src/syncopaid/tray.py"]
```

2. Document reason below (keep this list updated):

### Current Exceptions

*(None yet - add as needed)*

Example reasons for exemption:
- Virtual scrolling implementation (tight coupling required)
- Threading/async coordination (state must be centralized)
- GUI event handlers (tight coupling to framework)

---

## Auto-Detection Logic

### Source Root Detection
Priority order:
1. `src/` directory if exists
2. `lib/` directory if exists
3. Project root (fallback)

### File Extension Detection
Scan source root for:
- `.py` → Python project
- `.vue`, `.js`, `.ts`, `.tsx` → JavaScript/TypeScript project
- Multiple types → track all found

### Config Override
Create `references/config.json` to override auto-detection:
```json
{
  "sourceRoot": "custom/path",
  "fileExtensions": [".py", ".pyx"]
}
```
