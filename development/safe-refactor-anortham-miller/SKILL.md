---
name: safe-refactor
description: Perform safe code refactoring with reference checking and validation. Uses Miller's rename_symbol for workspace-wide renames and fast_refs for impact analysis. Activates when user wants to refactor, rename, or safely modify code.
allowed-tools: mcp__miller__rename_symbol, mcp__miller__fast_refs, mcp__miller__get_symbols, Edit, Read, Bash
---

# Safe Refactor Skill

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
🛡️ **Safe Refactor Mode Active**
Using Miller's reference checking and rename_symbol for validated changes...
```

This provides a visual indicator to the user that the skill is running.

## Purpose
Perform **safe, validated code refactoring** using Miller's intelligence to prevent breaking changes. This skill combines **reference checking**, **workspace-wide renames**, and **impact analysis** to modify code confidently.

## When to Activate
Use when the user:
- **Wants to rename**: "rename this function", "change variable name"
- **Needs to refactor**: "extract this code", "refactor this class"
- **Modifies code safely**: "update this API", "change this interface"
- **Reorganizes code**: "move this to another file", "split this class"

## Miller's Refactoring Tools

### Workspace-Wide Renaming

**rename_symbol** - AST-aware symbol renaming
```
Renames symbols across entire workspace
- Checks all references first (dry_run=True by default)
- Word-boundary safe (won't rename substrings)
- Name collision detection
- Preview before commit
```

**Use when:** Renaming classes, functions, methods, variables, types

### Safety Checks

**fast_refs** - Find all references (REQUIRED before changes!)
```
Critical for impact analysis
- See all usage points
- Verify scope of change
- Identify breaking changes
```

**get_symbols** - Structure validation
```
Verify file structure before/after edits
Ensure no symbols lost
```

## Orchestration Strategy

### Pattern 1: Safe Symbol Rename
**Goal:** Rename across entire workspace

```
1. fast_refs({ symbol_name: "oldName" }) -> Check all references
2. Review impact (how many files affected?)
3. Ask user confirmation if >10 files
4. rename_symbol({ old_name: "oldName", new_name: "newName" }) -> Preview
5. rename_symbol({ old_name: "oldName", new_name: "newName", dry_run: false }) -> Apply
6. Verify completion
```

### Pattern 2: Targeted Code Edit
**Goal:** Modify specific code section

```
1. get_symbols to understand structure
2. Read target section
3. Make edit with Edit tool
4. Verify edit succeeded
5. Run tests if available
```

### Pattern 3: Refactor with Validation
**Goal:** Large refactoring with safety

```
1. get_symbols(mode="structure") -> Baseline
2. fast_refs on symbols being changed
3. Perform edits (rename_symbol + Edit)
4. get_symbols again -> Verify structure
5. Run tests -> Confirm no breakage
```

## Safety Checklist

Before any refactoring:

### Pre-Refactor Checks
- [ ] Check references with `fast_refs`
- [ ] Understand current structure with `get_symbols`
- [ ] Identify impact scope (how many files?)
- [ ] Consider backward compatibility needs

### During Refactor
- [ ] Use rename_symbol for symbol renames (not find-replace!)
- [ ] Preview with dry_run=True first
- [ ] Verify each step before proceeding

### Post-Refactor Validation
- [ ] Verify edits applied correctly
- [ ] Check symbol structure unchanged (unless intended)
- [ ] Confirm all references updated
- [ ] Run tests if available
- [ ] Review git diff for unexpected changes

## Tool Selection Guide

### Use rename_symbol when:
- Renaming classes, functions, methods, variables
- Need workspace-wide consistency
- Multi-file impact expected

### Use Edit tool when:
- Modifying method bodies
- Updating specific code sections
- Single file, targeted changes

## Key Behaviors

### DO
- Always check references before renaming
- Use rename_symbol for symbol renames (word-boundary safe)
- Verify edits succeeded
- Run tests after significant changes
- Provide clear descriptions of changes
- Ask for confirmation on large-scope changes

### DON'T
- Rename without checking references first
- Use find-replace for symbol renames
- Skip post-refactor verification
- Ignore test failures after refactoring
- Make changes without understanding impact
- Proceed with risky renames without user consent

## Success Criteria

This skill succeeds when:
- Code refactored without breaking changes
- All references updated consistently
- Tests still pass (if applicable)
- Changes are semantically correct
- User confident in the safety of edits
