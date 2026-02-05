---
name: Unison Development
description: Write, test, and update Unison code using MCP tools. Use when working with Unison language files (.u extension), UCM operations, or Unison projects. Enforces TDD with strict typechecking via development skill. Used as a part of the XP skill.
---

# Unison Development

- Uses `development` skill for TDD workflow, enhanced with Unison-specific tooling.
- Use the unison MCP server commands for all operations.

## Core Principles

1. **NEVER run UCM commands on the command line** — use MCP tools only
2. Code is stored by the Unison Code Manager, not Git
3. **TDD is mandatory** — be aware UCM may enter "Handling typecheck errors after update"
4. **Always** use fully qualified names in scratch.u
5. **Never** create multiple scratch files
6. **ALWAYS** wait for user confirmation after `update` before continuing
7. **ALWAYS** Typecheck code with unison MCP server before adding to scratch file
8. After successful update, you may delete the scratch file

## Workflow

### 1. Research & Understanding

Use MCP tools to explore before writing:

- `view-definitions` for existing implementations
- `search-definitions-by-name` for related functions
- `docs` for library functions

### 2. Branch

Ask the user to create feature branch before beginning.

### 3. Clear scratch files

Ask the user if they want `scratch.u` deleted.

### 4. Write Tests First

Use `test.verify`, `labeled`, and `ensureEqual`:

```unison
projectName.module.tests.featureTest : '{IO, Exception} [Result]
projectName.module.tests.featureTest = do
  test.verify do
    labeled "Description" do
      use test ensureEqual
      result = performOperation testData
      ensureEqual result expectedValue
```

### 5. Typecheck Incrementally

```
mcp__unison__typecheck-code with {"text": "code here"}
```

Iterate until clean — fix type errors, add imports, verify effects.

### 6. Add to scratch.u with Fully Qualified Names

- **WRONG:** `foo : Text -> ...`
- **CORRECT:** `projectName.module.foo : Text -> ...`

**Why:** Without Fully Qualified Names, Unison creates new function instead of modifying existing functions.

Typecheck output indicators:

- `+` (added) — new definition
- `~` (modified) — updated existing

**Verify you see `~` for modifications!**

### 7. Final Typecheck

```
mcp__unison__typecheck-code with {"filePath": "/path/to/scratch.u"}
```

### 8. UPDATE MODE: Handling Typecheck Errors

If UCM adds this comment after update:

```
-- The definitions below no longer typecheck with the changes above.
-- Please fix the errors and try `update` again.
```

**CRITICAL:**

- **DO NOT** delete functions from scratch.u — they will be removed from codebase
- Repair broken code, typechecking as you go
- Ask user to verify via UCM output
- After successful update, you may remove code from scratch.u

## Success Criteria

- All code typechecks successfully
- Tests written before implementation
- Fully qualified names in scratch.u
- Modified functions show `~` not `+`
- Comprehensive test coverage

### Modifying Abilities

When modifying `abilities` it is easier to modify the ability first, ask the user to `update` in the UCM which will result in an `update` branch, fix the code in the `update` branch, then ask the user to `update`.
