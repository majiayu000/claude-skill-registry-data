---
name: tasks-bug-diagnosis
description: >-
  DEPRECATED: This skill has been merged into `debugging` with `--autonomous` flag.
  Use `/debugging --autonomous` instead for structured headless debugging.
  Redirect: debugging --autonomous
version: 2.0.0
deprecated: true
redirect: debugging --autonomous
---

# tasks-bug-diagnosis (Deprecated)

> **⚠️ This skill has been merged into `debugging`.**
>
> Use `/debugging --autonomous` for the same functionality.

## Migration Guide

| Old Command | New Command |
|-------------|-------------|
| `/tasks-bug-diagnosis` | `/debugging --autonomous` |
| `/tasks-bug-diagnosis [bug-name]` | `/debugging --autonomous [bug-name]` |

## Why Merged?

The `tasks-bug-diagnosis` skill was a standalone autonomous debugging workflow. It has been consolidated into the main `debugging` skill as an `--autonomous` mode to:

1. **Reduce confusion** - One skill for all debugging needs
2. **Enable mode switching** - Start interactive, switch to autonomous as needed
3. **Share techniques** - Both modes use the same underlying debugging techniques
4. **Simpler discovery** - Users find `debugging`, see both modes

## What Moved Where

| Original Content | New Location |
|------------------|--------------|
| 5-phase workflow | `debugging` → Mode Selection section |
| Anti-hallucination protocols | `debugging/references/autonomous-workflow.md` |
| Evidence gathering templates | `debugging/references/autonomous-workflow.md` |
| Confidence level tracking | `debugging/references/autonomous-workflow.md` |
| Approval gate protocol | `debugging/references/autonomous-workflow.md` |

## Related

- **Replacement:** `debugging --autonomous` - Full autonomous debugging workflow
- **Interactive:** `debugging` - Standard interactive debugging

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-20 | Deprecated, merged into debugging --autonomous |
| 1.0.0 | 2025-09-01 | Initial release |

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
