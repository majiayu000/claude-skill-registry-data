---
name: work-on-milestone
description: |
  Use this skill when asked to work on a milestone.
  You are not required to complete the milestone when this skill is invoked.
---

# Working Through a Milestone

## Before Starting

1. Review the last commit: `git show HEAD`
2. Run tests to see current state: `mise test`
3. Read relevant test files in `testcases/` to understand expected behavior
4. **CRITICAL: Assess host interface sufficiency**
   - Review `src/tclc.h` (TclHostOps) to understand available primitives
   - Determine if the feature can be implemented using existing ops
   - **If TclHostOps needs to be extended: STOP IMMEDIATELY and inform the user**
   - Do not proceed until you have received explicit approval and direction

## Implementation Loop

For each failing test:

1. **Identify what's missing** - parse test output to understand the gap
2. **C interpreter changes** (in `src/`):
   - Create new `builtin_*.c` file if adding a command
   - Add declarations to `internal.h`
   - Register command in `interp.c` builtins table
   - Implement using `TclHostOps` primitives only
3. **Go host changes** (in `interp/`):
   - Implement callbacks in `callbacks.go`
   - Add state to `Interp` struct in `tclc.go` if needed
   - Follow shimmering rules in `interp/CLAUDE.md`
4. **Run tests**: `mise test`
5. **Iterate** until tests pass

## Key Patterns

- **List operations mutate**: Use `ops->list.from()` to copy before iterating
- **String lengths**: Count carefully, don't include null terminator
- **Shimmering**: Use `Get*()` methods in Go for type conversion, never access Object fields directly
- **Error messages**: Match TCL's exact format (check test expectations)

## After All Tests Pass

1. Run tests multiple times to verify stability
2. Commit with detailed message explaining:
   - What was implemented
   - Key implementation details
   - Important learnings for future work
3. Use the format from CLAUDE.md (heredoc, co-author line)

## File Checklist for New Commands

- [ ] `src/builtin_<cmd>.c` - implementation
- [ ] `src/internal.h` - declaration
- [ ] `src/interp.c` - registration
- [ ] `interp/callbacks.go` - host callbacks (if new ops needed)
- [ ] `interp/tclc.go` - state/structs (if needed)
