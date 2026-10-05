---
name: code-consistency
description: >-
  Enforces code consistency rules across all agents. Prevents unnecessary modifications
  to working code, ensures existing patterns are followed, and maintains minimal diffs.
  This skill is loaded automatically by the orchestrator and should be referenced by all
  specialist agents when making code changes.
---

# Code Consistency Rules

## Purpose

Ensure that AI agents produce consistent, predictable changes that respect the existing
codebase. These rules prevent "AI drift" — the tendency for agents to refactor, reformat,
or restructure code beyond what was requested.

## Rules (MANDATORY for all agents)

### Rule 1: Scope Discipline — Only Touch What's Needed

```
BEFORE editing any file, ask:
  "Is this file DIRECTLY required for the current task?"
  
  YES → Edit it
  NO  → Do NOT touch it, even if you see improvements
```

**Examples:**
```
Task: "Add a new /api/products endpoint"

✅ CORRECT:
  - Create ProductController.php
  - Add route in api.php
  - Create Product model (if not exists)

❌ WRONG:
  - Refactor existing UserController "while we're at it"
  - Add return types to unrelated models
  - Update .env.example with unrelated variables
```

### Rule 2: Pattern Conformity — Follow, Don't Innovate

```
BEFORE introducing ANY pattern, check:
  "Does the codebase already have a pattern for this?"
  
  YES → Use the existing pattern
  NO  → Use Laravel's conventional approach
```

**Examples:**
```
Existing codebase uses:
  - Direct Eloquent in controllers (no Repository pattern)
  - $request->validate([]) inline (no Form Request classes)
  - Simple role check in middleware (no Spatie Permissions)

✅ CORRECT: Follow the same patterns
❌ WRONG: Introduce Repository pattern, Form Requests, or Spatie
   UNLESS the user explicitly asks for it
```

### Rule 3: Minimal Diff — Smallest Change Possible

```
WHEN editing a file:
  - Change ONLY the lines needed
  - Do NOT reformat surrounding code
  - Do NOT add/remove blank lines elsewhere
  - Do NOT change import order (Pint will handle this)
  - Do NOT rename variables in existing code
```

### Rule 4: Preserve Documentation

```
WHEN editing a file that has:
  - PHPDoc blocks → Keep them, update if factually wrong
  - Inline comments → Keep them
  - Vietnamese comments → Keep them (this is a Vietnamese team)
  - TODO/FIXME notes → Keep them
```

### Rule 5: Migration Safety

```
WHEN working with database:
  - NEVER modify an existing migration that has been run
  - ALWAYS create a new migration for schema changes
  - NEVER use destructive operations without explicit user approval:
    - dropColumn, dropTable, renameColumn
```

### Rule 6: Config Stability

```
WHEN working with config files:
  - Do NOT modify config/*.php unless directly needed
  - Do NOT change .env.example unless adding a new feature that needs it
  - Do NOT modify bootstrap/app.php unless registering new middleware/routes
  - Do NOT modify composer.json unless adding/removing a package
```

## Self-Check Protocol

Before submitting changes, every agent MUST verify:

```
□ Did I only modify files related to the current task?
□ Did I follow existing code patterns?
□ Did I preserve all existing comments and docblocks?
□ Did I avoid reformatting or restructuring unrelated code?
□ Did I create new migrations instead of modifying existing ones?
□ Would this diff be easy for a human to review? (minimal, focused)
```

## Violation Reporting

If you observe a violation of these rules (including your own), report it:

```markdown
⚠️ **Code Consistency Warning**
- Rule violated: [Rule number and name]
- File: [path]
- Description: [what happened]
- Correction: [what should be done instead]
```
