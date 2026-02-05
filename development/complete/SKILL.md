---
name: complete
description: |
  Finalize a completed ticket: write 5-final.md, update 4-progress.md, commit.

  WHEN TO USE:
  - All required tests pass (via /pmc:ticket-status)
  - Ready to mark ticket as COMPLETE or BLOCKED
  - User says "complete ticket", "finalize", "wrap up ticket"

  PRODUCES:
  - 5-final.md with Status: COMPLETE or BLOCKED
  - Updated 4-progress.md frontmatter
  - Git commit: "T0000N: complete"
---

# Complete Ticket

Finalize a completed ticket with proper documentation and commit.

## Prerequisites

**ALWAYS run /pmc:kb first** to understand ticket formats.

**Before completing:**
- Run `/pmc:ticket-status T0000N` - must return `needs-final` or better
- All required tests should pass (unless marking BLOCKED)

---

## When to Use

| Status from ticket-status | Action |
|---------------------------|--------|
| `needs-final` | Ready to complete |
| `complete` | Already done |
| `blocked` | Review blocker, may complete as BLOCKED |
| Other | Not ready - fix issues first |

---

## Step 1: Verify Ready State

```
/pmc:ticket-status T0000N
```

Expected: `needs-final` (all tests pass, no 5-final.md yet)

If not ready, address issues first:
- `tests-failing` → fix implementation
- `needs-impl` → run more TDD cycles
- `red-phase` → complete RED verification

---

## Step 2: Write 5-final.md

**Format:** See [kb/references/ticket-formats.md](../kb/references/ticket-formats.md) (5-final.md section)

### For COMPLETE Status

```markdown
# T0000N: {Title}

Status: COMPLETE

## Summary

[One paragraph - what was accomplished]

## Changes

- `path/file.py`: [what changed]
- `path/new.py`: [created, purpose]

## Tests

All required tests passing: X/X

## Limitations (optional)

- [Known limitation]

## Revealed Intent

User preferences and clarifications discovered during this ticket:
- [Preference/clarification discovered during iterative work]

## Declared Use-Cases

Specific scenarios user mentioned this solves:
- [Use-case or scenario user described]

## Open Questions

Unresolved items for future reference:
- [Question that wasn't answered]

## Learned

### What worked
- [Approach/tool/technique that was effective]

### What to improve
- [What could be done better next time]

### KB updates made
- [List any docs created/updated during reflection]
```

### For BLOCKED Status

```markdown
# T0000N: {Title}

Status: BLOCKED

## Reason

[Why blocked: dependency unavailable, needs human decision, cancelled, etc.]

## Summary

[What was accomplished before blocking]

## Changes Made

- [Any changes that were made before blocking]

## To Unblock

- [What needs to happen to proceed]
```

---

## Step 3: Update 4-progress.md Frontmatter

Update the pipe-delimited frontmatter:

**Before (IN_PROGRESS):**
```markdown
---
T0000N|IN_PROGRESS|Brief Title|3/4 TDD cycles complete
---
```

**After (COMPLETE - move to 5-final.md):**
The frontmatter in 4-progress.md stays as final in-progress state.
5-final.md existence indicates completion.

---

## Step 4: Verify with KB Integrity

```
/pmc:lint-kb
```

Ensure:
- [ ] 5-final.md exists with proper status
- [ ] Ticket still in index.md (until archived)
- [ ] No format violations

---

## Step 5: Commit

```bash
git add .pmc/docs/tickets/T0000N/
git add .pmc/docs/tests/tickets/T0000N/
git commit -m "T0000N: complete"
```

---

## Checklist

### Before Completing
- [ ] `/pmc:ticket-status` returns `needs-final`
- [ ] All required tests pass
- [ ] 4-progress.md is up to date

### 5-final.md Content
- [ ] Status: COMPLETE or BLOCKED
- [ ] Summary describes what was done
- [ ] Changes lists modified files
- [ ] Tests section shows pass count
- [ ] Revealed Intent captures user clarifications
- [ ] Learned section filled out

### After Completing
- [ ] 5-final.md created
- [ ] `/pmc:lint-kb` passes
- [ ] Committed with "T0000N: complete"

---

## Next Steps

After completing a ticket:

1. **Run `/pmc:reflect`** - Capture learnings to KB
2. **Check phase status** - Is this the last ticket in phase?
3. **Archive if ready** - Move to `tickets/archive/`

---

## Example Run

```
$ /pmc:complete T00021

## Completing T00021: Add User Dashboard

### Status Check
Running /pmc:ticket-status T00021...
Status: needs-final
Tests: 4/4 required passed
Ready to complete: YES

### Writing 5-final.md

Created .pmc/docs/tickets/T00021/5-final.md:
- Status: COMPLETE
- Summary: Added user dashboard with charts, metrics, and settings
- Changes: 4 files modified, 2 created
- Tests: 4/4 passed

### KB Lint Check
Running /pmc:lint-kb...
All checks passed.

### Commit
git add .pmc/docs/tickets/T00021/
git commit -m "T00021: complete"

## Complete

Ticket T00021 marked COMPLETE.

Next steps:
- Run /pmc:reflect to capture learnings
- Archive ticket when ready
```
