---
name: code-hygiene
description: Apply code hygiene standards for clean, maintainable code. Use when writing, refactoring, or reviewing code.
---

# Code Hygiene Standards

## Core Principles

- **Comments explain WHY, not WHAT** - Code shows what through clear naming
- **Self-documenting code** - Descriptive names > comments
- **Git captures history** - Never add "moved from X" or "extracted from Y" comments

## Comment Rules

**Never write:**
- Archaeological: "Extracted from X to reduce complexity"
- Motion tracking: "Moved from Y on DATE"
- Obvious: "Increment counter" above `counter += 1`
- Vague TODOs: "TODO: fix this" (add ticket number + context)
- Commented-out code (Git remembers)

**Do write:**
- Design rationale: "Binary search because dataset >10k items"
- Security markers: "SECURITY: Validate path to prevent traversal"
- Performance constraints: "Must complete <50ms for 60Hz tick"
- External quirks: "GitHub API returns max 100 items per page"
- Actionable TODOs: "TODO(#423): Replace with spatial hash for >1000 entities"

## File Size Limits

- **>500 lines**: Stop. Refactor before adding code.
- **>300 lines + new code**: Ask about extraction first.

## Responsibility Check

Before adding code: Does this add a different responsibility? If yes, suggest where it should live instead.

## Naming

- Descriptive: `validate_path_within_boundary` not `check_path`
- No vague names: `data`, `info`, `temp`, `mgr`, `handler`
- Booleans: `is_valid`, `has_permission`, `can_edit`
- Constants: `TIMEOUT_MS` (include units)

## Refactoring Hygiene

- Delete "extracted from" comments after moving code
- Delete code completely (don't comment out)
- Remove unused imports
- Update all call sites atomically

**Remember**: Every line should serve a purpose. Delete ruthlessly. Name precisely.
