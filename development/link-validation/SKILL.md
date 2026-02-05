---
name: link-validation
description: Universal link validation using lychee for Claude Code sessions. Runs at session end to detect broken links and path policy violations.
triggers:
  - link validation
  - broken links
  - lychee
  - check links
  - markdown links
---

# Link Validation Skill

Validates markdown links in your workspace using [lychee](https://github.com/lycheeverse/lychee).

## What It Does

At session end (Stop hook), this skill:

1. **Discovers** all markdown files in your workspace
2. **Runs lychee** to check for broken links
3. **Lints paths** for policy violations (absolute paths, excessive traversal)
4. **Outputs JSON** results for programmatic consumption

## Requirements

- [lychee](https://github.com/lycheeverse/lychee) installed (`brew install lychee`)
- Python 3.11+ and uv

## Output

Results are written to `.link-check-results.md` in your workspace:

```markdown
# Link Check Results

**Correlation ID**: `01JEGQXV8KHTNF3YD8G7ZC9XYK`

## Lychee Link Validation

No broken links found.

## Path Policy Violations

No path violations found.
```

## Path Policy Rules

| Rule                 | Severity | Description                            |
| -------------------- | -------- | -------------------------------------- |
| NO_ABSOLUTE_PATHS    | Error    | Filesystem absolute paths not allowed  |
| NO_PARENT_ESCAPES    | Warning  | Excessive `../` may escape repository  |
| MARKETPLACE_RELATIVE | Warning  | Plugins should use `./` relative paths |

## Configuration

Override the default lychee config by placing `.lycheerc.toml` in your workspace root.

See [config/lychee.toml](../../config/lychee.toml) for the default configuration.

## References

- [ADR: Link Checker Plugin Extraction](../../../../docs/adr/2025-12-11-link-checker-plugin-extraction.md)
- [Design Spec](../../../../docs/design/2025-12-11-link-checker-plugin-extraction/spec.md)
- [lychee Documentation](https://github.com/lycheeverse/lychee)
