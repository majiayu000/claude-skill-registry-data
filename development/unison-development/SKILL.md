---
name: Unison Development
description: Write, test, and update Unison code using the Unison MCP tool. Use when working with Unison language files (.u extension), UCM operations, or Unison projects. An extension to the XP skill.
---

# Unison Development

- Uses `xp` skill.
- Use the Unison MCP server commands for all operations.

## Core Principles

1. **NEVER run Unison Code Manager (UCM) commands on the command line** — use MCP tools only
2. Code is stored by the UCM, not Git
4. **Always** use fully qualified names in `scratch.u`
5. **Never** create multiple scratch files
6. **ALWAYS** wait for user confirmation after `update` before continuing
7. **ALWAYS** Typecheck code with unison MCP server before adding to scratch file
8. Write code to the scratch.u file in the current directory after it typechecks
9. After successful update, you may delete the scratch file
10. Use the MCP service tool to explore the codebase before writing code

### UPDATE MODE: Handling Typecheck Errors

When an update is performed that results in further changes required, the UCM adds this comment after the user updates:

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
- Fully qualified names in scratch.u

### Modifying Abilities

When modifying `abilities` it is easier to modify the ability first, ask the user to `update` in the UCM which will result in an `update` branch, fix the code in the `update` branch, then ask the user to `update`.

