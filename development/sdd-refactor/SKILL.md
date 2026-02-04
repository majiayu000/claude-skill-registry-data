---
name: sdd-refactor
description: Safe refactoring operations using LSP for precise symbol resolution. Supports rename, extract function/method, and move symbol operations with automatic reference updates.
---

# SDD-Refactor: Safe Refactoring Skill

## Overview

`Skill(foundry:sdd-refactor)` provides LSP-powered refactoring with safety checks. It uses `findReferences` to understand impact before making changes, performs batch edits, and verifies correctness.

**Core capabilities:**
- Safe rename operations with complete reference updates
- Extract function/method with reference updating
- Move symbol across files with import fixups
- Unused code cleanup based on zero-reference analysis

**IMPORTANT:** This skill uses Claude Code's built-in LSP tools for precise refactoring. If LSP returns no results for the target language, fall back to Grep-based patterns.

## Skill Family

This skill integrates with the **Spec-Driven Development** workflow:

```
sdd-plan --> sdd-refactor (for planned refactoring tasks) --> sdd-update --> sdd-fidelity-review
```

Can also be used standalone for ad-hoc refactoring outside of specs.

## When to Use This Skill

Use `Skill(foundry:sdd-refactor)` for:
- Renaming classes, functions, methods, or variables across codebase
- Extracting code into new functions/methods
- Moving symbols between files/modules
- Cleaning up unused code (dead code removal)
- Any refactoring that affects multiple files

**Do NOT use for:**
- Simple single-file edits (use Edit tool directly)
- Creating new code from scratch (use sdd-plan + implement)
- Deleting entire files (manual operation)
- Formatting or style changes (use formatter tools)

### Flow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop · `§`=section ref

```
- **Entry** → [Type: Rename|Extract|Move|Cleanup?]
- ValidateTarget → [LSP available?]
  - [yes] → `documentSymbol` → `goToDefinition`
  - [no] → Grep fallback
- ImpactAnalysis (GATE - REQUIRED)
  - `findReferences` → Risk[<10|<50|50-100|>100 refs]
  - (GATE: user approval for scope)
- Execute → [4 operation-specific paths]
- Verify → Structural[LSP] → References[LSP] → Tests[run-tests]
- Document → [spec task?] → journal entry
- **Exit**: Done
```

## LSP Tools

This skill uses Claude Code's built-in LSP tools directly:

| Tool | Purpose |
|------|---------|
| `findReferences` | Find all usages of a symbol |
| `goToDefinition` | Navigate to symbol definition |
| `documentSymbol` | Get file structure/symbol outline |

For spec integration, use foundry-mcp:

| Router | Actions | Purpose |
|--------|---------|---------|
| `task` | `update-status`, `complete` | Track refactoring task progress |
| `journal` | `add` | Document refactoring decisions |

## Core Workflow

### Step 1: Identify Refactoring Target

Gather information about what to refactor:

1. **User provides:**
   - Symbol name (class, function, variable)
   - File path containing the symbol
   - Refactoring type (rename, extract, move, cleanup)
   - New name or destination (if applicable)

2. **Validate target exists with LSP:**
   ```
   definition = goToDefinition(file="src/module.py", symbol="OldClassName", line=10)

   if definition found:
       Proceed to impact analysis
   else:
       Ask user to verify symbol name and location
   ```

3. **Fallback if LSP unavailable:**
   ```
   Use Grep to verify symbol exists:
   Grep(pattern="class OldClassName", path="src/")
   ```

### Step 2: Impact Analysis (REQUIRED)

**NEVER refactor without understanding impact first.**

1. Use `findReferences` to get all usages of the symbol
2. Analyze: total count, unique files, reference types (import, call, annotation)
3. Present impact report to user with risk assessment
4. Get user approval before proceeding

> See [references/impact-analysis.md](./references/impact-analysis.md) for detailed procedures and report format.

### Step 3: Execute Refactoring

Execute the appropriate operation based on refactoring type:

| Operation | Key Steps |
|-----------|-----------|
| **Rename** | Collect references → Sort by dependency → Batch edit → Verify |
| **Extract** | Identify block → Analyze variables → Create function → Replace |
| **Move** | Find references → Move definition → Update imports → Verify |
| **Dead Code** | Check reference count → Remove if zero → Clean imports |

> See [references/operations.md](./references/operations.md) for detailed procedures for each operation type.

### Step 4: Verify Correctness

After any refactoring:

1. **Structural verification (LSP):**
   ```
   documentSymbol(file="src/module.py")
   # Verify expected structure preserved
   ```

2. **Reference verification (LSP):**
   ```
   findReferences(file="src/module.py", symbol="NewName")
   # Verify all references resolve
   ```

3. **Run affected tests:**
   ```
   Skill(foundry:run-tests) "Run tests for affected files"
   ```

### Step 5: Document Changes

If refactoring is part of a spec task:

```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id="{spec-id}" task_id="{task-id}" completion_notes="Renamed OldClassName to NewClassName across 12 files. All tests passing."
```

For significant refactors, add journal entry:

```bash
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id="{spec-id}" title="Refactoring: OldClassName -> NewClassName" content="Renamed class for clarity. 47 references updated across 12 files. No functional changes." entry_type="decision"
```

## LSP Availability Check

Before using LSP-enhanced workflow, verify by calling `documentSymbol` on the target file. If it returns successfully, use LSP workflow. Otherwise, fall back to Grep-based workflow.

> See [references/lsp-check.md](./references/lsp-check.md) for fallback triggers and verification procedure.

## Size Guidelines

| Scope | Approach |
|-------|----------|
| Single file, <10 refs | Direct refactoring |
| Cross-file, <50 refs | Batch with verification |
| 50-100 refs | Split into incremental changes |
| >100 refs | Create spec for tracking, phase the work |

## Example Invocations

**Rename class:**
```
Skill(foundry:sdd-refactor) "Rename AuthService to AuthenticationService in src/auth/service.py"
```

**Extract method:**
```
Skill(foundry:sdd-refactor) "Extract lines 45-67 in src/handlers.py into new method validate_request"
```

**Move function:**
```
Skill(foundry:sdd-refactor) "Move helper_function from src/utils.py to src/helpers/common.py"
```

**Dead code cleanup:**
```
Skill(foundry:sdd-refactor) "Find and remove unused functions in src/legacy/"
```

**Rename with spec context:**
```
Skill(foundry:sdd-refactor) "Complete task-2-3: Rename UserDTO to UserResponse as specified"
```

## Detailed Reference

For comprehensive documentation including:
- Impact analysis → `references/impact-analysis.md`
- Refactoring operations → `references/operations.md`
- LSP availability check → `references/lsp-check.md`
- Troubleshooting → `references/troubleshooting.md`
