---
id: quality.no-dead-code.unused-exports-cleanup
name: Unused Exports Cleanup
description: >
  Removes unused public exports from JavaScript and TypeScript code while preserving public API contracts, barrel behavior, and cross-package compatibility.
stack:
  - JavaScript
  - TypeScript
category: no-dead-code
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - unused exports
  - export cleanup
  - public api cleanup
  - barrel exports
  - dead exports
compatibility:
  runtime:
    browser: true
    node: true
---

# Unused Exports Cleanup

## Purpose

Use this skill to remove unused public exports without breaking real consumers.

The goal is to reduce API surface while keeping shared contracts stable.

The core rule is simple:

```txt
Remove unused exports only after verifying they are truly unused.
```

## When to Use

Use this skill when:

- exports are no longer referenced
- a public API has grown stale
- barrels are accumulating dead surface
- monorepo libraries need smaller interfaces

## Do

Check:

- direct imports
- barrel re-exports
- package consumers
- generated usage
- test-only references

Confirm the export is not part of an external contract.

## Do Not

Avoid deleting exports that are part of a published API.

Avoid assuming “unused in this repo” means globally unused.

Avoid broad API rewrites while cleaning one export.

## Review Checklist

- [ ] The export is truly unused.
- [ ] Public API compatibility was checked.
- [ ] Barrel behavior is preserved or updated safely.

## Expected Output

1. Verify usage.
2. Confirm API impact.
3. Remove only dead exports.
4. Keep contract stability in mind.
5. Validate imports and builds.
