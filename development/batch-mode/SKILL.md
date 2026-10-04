---
name: batch-mode
description: When the user needs to perform the same operation across multiple files, components, or entities. Use when the user says "do this to all," "batch," "bulk update," "across all files," "every component," "mass refactor," "rename everywhere," "update all," "migrate all," or when a task involves applying a consistent pattern to 3+ targets. Orchestrates parallel processing of repetitive tasks with consistency guarantees.
metadata:
  version: 1.0.0
  inspired_by: batch.ts skill
---

# Batch Mode — Parallel Consistent Processing

You are a batch processing engine. When the same operation needs to happen across multiple targets, you systematize it for speed, consistency, and reliability.

## When To Use

- Same change across 3+ files
- Migrating patterns across a codebase
- Bulk renaming (variables, functions, files, imports)
- Applying a new standard to existing code
- Mass-generating similar content (tests, docs, components)
- Processing multiple items from a list

## The Batch Protocol

### Step 1: Define the Operation

Formalize what needs to happen:

```
BATCH OPERATION:
─────────────────
Template: [the exact change pattern]
Targets: [what gets changed]
Scope: [where to look]
Exceptions: [what to skip]
Validation: [how to verify each change]
```

Example:
```
BATCH OPERATION:
─────────────────
Template: Add error boundary wrapper to React components
Targets: All page-level components in src/pages/
Scope: 14 files matching src/pages/**/*.tsx
Exceptions: Skip _app.tsx and _document.tsx
Validation: Each wrapped component still renders without errors
```

### Step 2: Discover Targets

Systematically find all targets:

```bash
# File-based targets
glob: src/pages/**/*.tsx → 14 files

# Pattern-based targets
grep: "export default function.*Page" → 12 matches

# Intersection
targets = glob ∩ grep - exceptions = 10 files
```

Present the target list to the user:
```
Found 10 targets for batch operation:
1. src/pages/Dashboard.tsx
2. src/pages/Settings.tsx
3. src/pages/Profile.tsx
...

Excluded:
- src/pages/_app.tsx (exception rule)
- src/pages/_document.tsx (exception rule)

Proceed with all 10? Or modify the list?
```

### Step 3: Dry Run

Process ONE target as a reference implementation:

```
DRY RUN — src/pages/Dashboard.tsx:
─────────────────────────────────
Before:
  export default function Dashboard() { ... }

After:
  export default function Dashboard() {
    return <ErrorBoundary><DashboardContent /></ErrorBoundary>
  }

Changes: +3 lines, +1 import
Validation: ✅ compiles, ✅ matches pattern
```

Get user approval: "This is the pattern. Apply to remaining 9 targets?"

### Step 4: Execute Batch

Process all targets, tracking progress:

```
Batch Progress:
[██████████░░░░░░░░░░] 5/10

✅ Dashboard.tsx — applied
✅ Settings.tsx — applied
✅ Profile.tsx — applied
✅ Users.tsx — applied
✅ Analytics.tsx — applied
⏳ Billing.tsx — processing
⬜ Reports.tsx
⬜ Integrations.tsx
⬜ Admin.tsx
⬜ Support.tsx
```

**For independent targets:** Use Agent tool with `isolation: "worktree"` to process in parallel (up to 5 at a time).

**For dependent targets:** Process sequentially, using each result to inform the next.

### Step 5: Handle Exceptions

When a target doesn't fit the pattern:

```
⚠️ EXCEPTION: src/pages/Billing.tsx
Reason: Already has a different error boundary implementation
Options:
  a) Replace existing with new pattern
  b) Skip this file
  c) Merge both patterns

→ Marking as skipped, flagging for manual review
```

Never force a pattern onto code that doesn't fit. Flag it and move on.

### Step 6: Batch Report

After completion:

```
BATCH REPORT
═══════════════════════
Operation: Add error boundary wrapper
Targets: 10 files
Completed: 9 ✅
Skipped: 1 ⚠️ (Billing.tsx — pre-existing pattern)
Failed: 0

Files Modified:
- src/pages/Dashboard.tsx (+3 lines)
- src/pages/Settings.tsx (+3 lines)
...

Manual Review Needed:
- src/pages/Billing.tsx — has existing error boundary, needs human decision

Validation:
- All modified files compile ✅
- Pattern consistency verified ✅
═══════════════════════
```

## Batch Patterns

### Pattern: Find & Replace
```
Operation: Rename `oldFunction` to `newFunction` across codebase
Method: grep → verify each usage → replace → check imports
```

### Pattern: Mass Migration
```
Operation: Migrate from library A to library B
Method: Find all imports of A → map to B equivalents → replace → update usage patterns
```

### Pattern: Bulk Generation
```
Operation: Generate tests for all untested components
Method: Find components → check for test file → generate test from component analysis
```

### Pattern: Consistency Enforcement
```
Operation: All API routes return { data } or { error } shape
Method: Find routes → analyze current return shapes → wrap in standard format
```

### Pattern: Mass Content Update
```
Operation: Update copyright year in all files
Method: grep for old year → replace → verify no false positives
```

## Rules

- **Always dry run first.** Never apply a batch without verifying the pattern on one target.
- **Track progress visibly.** The user should always know how far along the batch is.
- **Handle exceptions gracefully.** One weird file shouldn't stop the whole batch.
- **Verify after each change.** If verification is possible (compile check, test run), do it per target, not just at the end.
- **Report everything.** What changed, what was skipped, what needs manual review.
- **Preserve the ability to undo.** Work on a branch. Commit after the batch with a clear message. User can revert the whole batch if needed.
- **Don't batch what shouldn't be batched.** If each target needs a unique approach, it's not a batch — it's a task list.
- **Maximum batch size: 50 targets.** Beyond that, break into sub-batches for manageability.
