---
name: fleet-component-patterns
description: How UX maintains and applies consistent component patterns — reuse existing patterns, define new ones properly, ensure pattern compliance across implementations.
---

# Component Patterns — UX's Consistency Framework

When engineers implement the same interaction differently every time, UX degrades. A table in one view uses pagination. The same table in another uses infinite scroll. One error dialog has a retry button. Another just says "Error." Pattern consistency prevents this drift.

## What Counts as a Component Pattern in the Fleet

The fleet doesn't build web UI (primarily). Its "components" are output patterns across all UX levels:

| Pattern Type | Example |
|-------------|---------|
| Table output | CLI `fleet status` agent table format |
| Error message | Error code + what failed + what to do + recovery command |
| Progress indication | "[agent] Working on task X: step 2/5" |
| Status display | Agent status: name, state (colored + symbol), task, last seen |
| Configuration | YAML structure: key naming, nesting, defaults, comments |
| Notification | ntfy message: title format, body structure, priority mapping |
| IRC message | "[agent] event: summary" format across all channels |
| Board memory | "**[tag]** content" format for trail, chat, alerts |

## The Pattern Library Structure

For each established pattern, document:

```
## Pattern: Error Message Format

### When to Use
Any user-facing error across CLI, API, logs

### Structure
{what_failed}: {specific_detail}. {recovery_instruction}. [{error_code}]

### Examples
GOOD: "Cannot connect to MC at localhost:8000. Is it running? Run `make mc-up` to start. [E-MC-001]"
GOOD: "Authentication failed. Token expired at 14:32. Run `fleet auth refresh`. [E-AUTH-001]"
BAD:  "Error occurred"
BAD:  "Connection refused"

### Properties
- Always includes error code for searchability
- Always includes recovery instruction
- Never uses technical jargon without explanation
- Color: red text in TTY, plain text when piped

### Accessibility
- Error code allows screen reader users to search documentation
- Recovery command is copy-pasteable
- No information conveyed only through color
```

## When to Create a New Pattern vs Reuse Existing

### Reuse When:
- The interaction is the same type as an existing pattern
- Only the content differs, not the structure
- The existing pattern handles the use case

### Create New When:
- No existing pattern covers this interaction type
- The existing pattern doesn't handle a critical difference (e.g., async operations need progress, but current pattern only handles sync)
- Multiple implementations have diverged — time to unify

### Create Process:
1. Document the pattern following the structure above
2. Show examples (good and bad)
3. Define accessibility requirements
4. Post to board memory: `[ux, pattern, new]`
5. Reference in your ux_spec contributions: "Follow Pattern: Error Message Format"

## Pattern Compliance During Review

When fleet-ops reviews user-facing work, your pattern library is their reference:
- Does the CLI output follow the table pattern?
- Do error messages follow the error format?
- Do notifications follow the ntfy template?

Flag violations in your ux_spec validation:
```
UX Pattern Check:
✓ Table output: follows fleet status column format
✗ Error messages: missing error code, no recovery instruction
✓ Config: YAML keys use kebab-case with comments
```

## The Fleet's Existing Patterns

The fleet already has established patterns in templates:

| Template | Location | Pattern |
|----------|----------|---------|
| PR body | agents/_template/markdown/pr-body.md | Changelog + diff table + labor stamp |
| Completion comment | agents/_template/markdown/comment-completion.md | Summary + artifacts + next steps |
| Progress comment | agents/_template/markdown/comment-progress.md | Done + next + blockers |
| IRC events | agents/_template/markdown/irc-events.md | [agent] event: summary |
| Board memory alert | agents/_template/markdown/memory-alert.md | **[tag]** severity: details |
| Board memory decision | agents/_template/markdown/memory-decision.md | **[decision]** what + why |

Your ux_spec contributions should reference these templates when applicable — don't reinvent patterns that already exist.
