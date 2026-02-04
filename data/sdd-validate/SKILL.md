---
name: sdd-validate
description: Validate SDD JSON specs, auto-fix common issues, generate detailed reports, and analyze dependencies.
---

# Spec Validation Skill

## Overview

The **Skill(sdd-toolkit:sdd-validate)** skill provides comprehensive validation for Spec-Driven Development (SDD) JSON specification files. It checks for structural consistency, auto-fixes common issues, generates detailed reports, and analyzes dependencies.

**Key capabilities:**
- Validate JSON spec structure and hierarchy integrity
- Auto-fix 13 common issue types with preview and backup support
- Generate detailed validation reports in Markdown or JSON
- Calculate comprehensive spec statistics (depth, coverage, complexity)
- Analyze dependencies (cycles, orphans, deadlocks, bottlenecks)
- Differentiated exit codes for warnings vs errors
- Draft 07 JSON Schema validation (installs automatically when `jsonschema` is available; run `pip install claude-skills[validation]` to enable)

## Understanding Exit Codes

Exit codes indicate the **state of your spec**, not command success/failure:

- **Exit 0**: ✅ Spec is valid (no errors)
- **Exit 1**: ⚠️  Spec has warnings (usable but improvable)
- **Exit 2**: 🔧 Spec has errors (needs fixing) - **THIS IS EXPECTED FOR NEW SPECS**
- **Exit 3**: ❌ File not found or access error (actual command failure)

**Important:** Exit code 2 means "I found errors in your spec" not "I failed to validate". The validate command succeeded at detecting issues - your spec just needs work. This is the normal starting point for most specs.

## When to Use This Skill

Use `Skill(sdd-toolkit:sdd-validate)` to:
- Confirm a freshly created spec parses correctly
- Auto-fix common validation issues
- Check for structural errors before running other SDD skills
- Generate validation reports for review or CI/CD
- Analyze spec statistics and dependency issues

## Core Workflow

1. **Validate**: `sdd validate {spec-id}` - Check for issues
2. **Fix**: `sdd fix {spec-id}` - Auto-fix common problems (creates backup)
3. **Re-validate**: Check for newly revealed issues
4. **Repeat**: Continue until error count stops decreasing
5. **Manual fixes**: Use `--verbose` for details when plateau is reached

**Key concept:** Error count decreasing = keep fixing. Plateau (same count for 2+ passes) = switch to manual fixes.

## Key Concepts

### Always Re-validate After Fixing
Fixing issues often reveals new problems that were previously hidden. Always run `sdd validate` after `sdd fix` to see the current state.

### Error Count Progression
Track how error count changes across passes:
- **Decreasing** (88 → 23 → 4) - Continue auto-fixing
- **Plateau** (4 → 4 → 4) - Switch to manual fixes with `--verbose`

### When to Stop Auto-Fixing
Switch to manual intervention when:
- Error count unchanged for 2+ passes
- `sdd fix` reports "skipped issues requiring manual intervention"
- All remaining issues need context or human judgment

### Input Format: Spec Names vs Paths

All sdd-validate commands accept **both** spec names and paths for maximum flexibility:

**Spec name (recommended):**
```bash
sdd validate pomodoro-timer-2025-11-18-001
```
Automatically searches in `specs/pending/`, `specs/active/`, `specs/completed/`, and `specs/archived/`.

**Relative path:**
```bash
sdd validate specs/pending/pomodoro-timer-2025-11-18-001.json
sdd validate ../other-project/specs/active/my-spec.json
```

**Absolute path:**
```bash
sdd validate /full/path/to/my-spec.json
```

**Smart fallback:** If you provide a path that doesn't exist (e.g., `specs/pending/my-spec.json`), the command extracts the spec name (`my-spec`) and searches for it automatically.

## Command Reference

### validate

Validate the JSON spec structure and print a summary.

```bash
sdd validate {spec-id} [--verbose]
```

**Flags:**
- `--verbose` - Show detailed issue information with locations
- `--report` - Generate validation report alongside spec
- `--report-format {markdown,json}` - Choose report format

**Exit codes:**
- `0` - Clean validation
- `1` - Warnings only
- `2` - Errors detected (expected when spec has issues)

**Example:**
```bash
$ sdd validate my-spec
❌ Validation found 12 errors
   8 auto-fixable, 4 require manual intervention

   Errors:
   - 5 incorrect task count rollups
   - 2 missing metadata blocks
   - 1 orphaned node (task-5-3)
   - 2 circular dependencies
   - 2 parent/child mismatches

   Run 'sdd fix my-spec' to auto-fix 8 issues
   Use '--verbose' for detailed issue information
```

### fix

Auto-fix common validation issues with preview and backup support.

```bash
sdd fix {spec-id} [--preview] [--dry-run] [--no-backup]
```

**Flags:**
- `--preview` / `--dry-run` - Show what would be fixed without modifying files
- `--no-backup` - Skip backup creation (use with caution)
- `--diff` - Show before/after changes
- `--diff-format {markdown,json}` - Choose diff format

**Auto-fixable issues:**
- Incorrect task count rollups
- Missing metadata blocks
- Orphaned nodes
- Parent/child hierarchy mismatches
- Malformed timestamps
- Invalid status/type values
- Bidirectional dependency inconsistencies

**Selective fix application:**
```bash
# Apply specific fixes by ID
sdd fix {spec-id} --select counts.recalculate

# Apply all fixes in a category
sdd fix {spec-id} --select metadata

# Apply multiple specific fixes
sdd fix {spec-id} --select counts.recalculate metadata.ensure:task-001
```

**Example:**
```bash
$ sdd fix my-spec --preview
📋 Would apply 8 fixes:
   - Fix 5 task count rollups
   - Add 2 metadata blocks
   - Reconnect 1 orphaned node

⚠️  Would skip 4 issues requiring manual intervention:
   - task-3-2: Circular dependency
   - task-5-2: Dependency references non-existent task

$ sdd fix my-spec
✅ Applied 8 fixes
Created backup: my-spec.json.backup

$ sdd validate my-spec
❌ Validation found 4 errors (manual intervention required)
```

### report

Generate a detailed validation report with stats and dependency analysis.

```bash
sdd report {spec-id} [--output <path>]
```

**Flags:**
- `--output` - Output file path (use `-` for stdout)
- `--bottleneck-threshold N` - Minimum tasks blocked to flag bottleneck (default: 3)

Report includes: validation summary, categorized issues, statistics, and dependency findings.

### stats

Calculate and display comprehensive spec statistics.

```bash
sdd stats {spec-id}
```

**Shows:**
- Node, task, phase, and verification counts
- Status breakdown (pending, in_progress, completed, blocked)
- Hierarchy maximum depth
- Average tasks per phase
- Verification coverage percentage
- Overall progress percentage

### analyze-deps

Analyze dependencies for cycles, orphans, deadlocks, and bottlenecks.

**Note:** This command analyzes spec-wide dependency issues. For checking individual task dependencies, use `sdd prepare-task` from sdd-next which includes dependency details by default in `context.dependencies` (e.g., `sdd prepare-task {spec-id} {task-id}`). The standalone `sdd check-deps` command is rarely needed now.

```bash
sdd analyze-deps {spec-id} [--bottleneck-threshold N]
```

**Analyzes:**
- **Cycles** - Circular dependency chains
- **Orphaned** - Tasks referencing missing dependencies
- **Deadlocks** - Tasks blocked by each other
- **Bottlenecks** - Tasks blocking many others

**Example:**
```bash
$ sdd analyze-deps my-spec
⚠️  Dependency Analysis: 3 issues found

Cycles (2):
  1. task-3-2 → task-3-5 → task-3-2
  2. task-4-1 → task-4-3 → task-4-1

Orphaned dependencies (1):
  task-5-2 references non-existent "task-2-9"

Recommendation: Fix circular dependencies first to unblock work
```

## Common Patterns

### Issue → Fix Mapping

- **Incorrect task counts** → Auto-fixed by recalculating from hierarchy
- **Missing metadata** → Auto-fixed by adding empty metadata blocks
- **Orphaned nodes** → Auto-fixed by reconnecting to parent
- **Circular dependencies** → Requires manual fix (remove one edge)
- **Invalid timestamps** → Auto-fixed to ISO 8601 format
- **Parent/child mismatches** → Auto-fixed by correcting hierarchy references

### Typical Fix Cycles

**Most specs (2-3 passes):**
```bash
Pass 1: 47 errors → fix → 8 errors
Pass 2: 8 errors → fix → 2 errors
Pass 3: 2 errors → fix → 0 errors ✅
```

**Complex specs with circular deps (4-5 passes):**
```bash
Pass 1: 88 errors → fix → 23 errors
Pass 2: 23 errors → fix → 4 errors
Pass 3: 4 errors → fix → 4 errors (plateau)
→ Manual: Remove circular dependencies
Pass 4: Validate → 0 errors ✅
```

## Troubleshooting

### Auto-fix Succeeded But Errors Remain

This is normal. `sdd fix` reports success when it applies fixes successfully, not when all issues are resolved. Fixing one problem often reveals another (e.g., fixing parent-child mismatches may reveal orphaned nodes).

**Solution:** Re-validate to see remaining issues, then run fix again or address manually.

### Error Count Plateau

When error count stays the same for 2+ passes:

1. Run `sdd validate {spec-id} --verbose` to see detailed issue information
2. Identify issues marked "requires manual intervention"
3. Manually fix issues that need context or human judgment
4. Re-validate after manual fixes

**Understanding Spec Requirements:**
- Run `sdd schema` to see the complete spec structure, required fields, and valid values
- The schema shows all field types, enum values (like `status`, `type`, `verification_type`), and optional vs required fields
- Use this when validation errors reference unknown fields or invalid values

**Common manual-only issues:**
- Circular dependencies (remove one dependency edge)
- Orphaned dependencies (fix task ID typos)
- Logical inconsistencies (requires understanding spec intent)
- Custom metadata problems

### How Many Passes Are Normal?

- **2-3 passes**: Typical for most specs
- **5+ passes**: May indicate circular dependencies or structural issues

**Rule:** If error count decreases each pass, keep going. If it plateaus, switch to manual.

## Advanced Usage

### Global Flags

Available on all commands:
- `--quiet` / `-q` - Suppress progress messages
- `--verbose` / `-v` - Show detailed information
