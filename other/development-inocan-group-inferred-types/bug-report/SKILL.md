---
name: bug-report
description: Log a bug report. Use when user asks to create, log, file, or report a bug.
allowed-tools: Write, Read, Glob
---

# Bug Report Skill

Create bug reports in `DevPlans/Bugs/` following the project's bug tracking conventions.

## File Naming

`{STATUS}-{BugName}.md`

| Status | Meaning |
|--------|---------|
| OPEN | Active bug, not yet fixed |
| FIXED | Bug has been resolved |
| REJECTED | Not a bug, or won't fix |

New bugs should always start with `OPEN-`.

## Required Sections

```markdown
# Bug: {Title}

## Summary
Brief description of the issue.

## Symptoms
- Observable behaviors
- Error messages
- Performance impacts

## Root Cause
Technical explanation of why this happens (if known).

## Affected Code
- List relevant files and line numbers
- `path/to/file.cs:123`

## Potential Solutions
### 1. Solution Name
Description of approach, tradeoffs.

### 2. Alternative
Another option if applicable.

## Priority
Low / Medium / High / Critical

## Related Files
- `path/to/related/file.cs`
```

## Example

For a bug about slow rendering:
- File: `DevPlans/Bugs/OPEN-SlowChunkRendering.md`
- Title: `# Bug: Slow Chunk Rendering`
- Include profiling data if available

## Status Changes

When a bug is fixed or rejected, rename the file:
- `OPEN-MyBug.md` → `FIXED-MyBug.md`
- `OPEN-MyBug.md` → `REJECTED-MyBug.md`
