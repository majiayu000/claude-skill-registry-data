---
name: lintmesh
description: Run multiple linters (eslint, oxlint, tsgo) in parallel with unified JSON output. Use when linting code, checking for errors before commits, or debugging lint failures. Triggers on "lint", "check code", "run linters", or after editing JS/TS files.
---

# Lintmesh

Unified linter runner. One command, JSON output, all issues sorted by file:line.

## Usage

```bash
# Lint everything (default: eslint + oxlint + tsgo)
lintmesh --quiet

# Lint specific paths
lintmesh --quiet src/

# Select linters
lintmesh --quiet --linters eslint,oxlint
```

Always use `--quiet` to suppress stderr progress.

## Output Schema

```typescript
{
  issues: Array<{
    path: string;           // Relative to cwd
    line: number;           // 1-indexed
    column: number;
    severity: "error" | "warning" | "info";
    ruleId: string;         // "eslint/no-unused-vars", "oxlint/no-debugger", "tsgo/TS2322"
    message: string;
    source: string;         // Which linter
    fix?: {                 // Present if autofixable
      replacements: Array<{ startOffset: number; endOffset: number; text: string }>;
    };
  }>;
  summary: { total: number; errors: number; warnings: number; fixable: number };
  linters: Array<{ name: string; success: boolean; error?: string }>;
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings OK) |
| 1 | Errors found |
| 2 | Tool failure |

## CLI Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--linters <list>` | `eslint,oxlint,tsgo` | Which linters |
| `--fail-on <level>` | `error` | Exit 1 threshold |
| `--timeout <ms>` | `30000` | Per-linter timeout |
| `--quiet` | `false` | No stderr |

## Patterns

```bash
# Error count
lintmesh --quiet | jq '.summary.errors'

# Files with issues
lintmesh --quiet | jq -r '.issues[].path' | sort -u

# Only errors
lintmesh --quiet | jq '[.issues[] | select(.severity == "error")]'

# Check if clean
lintmesh --quiet && echo "No errors"
```

## When to Use

- After editing code: catch issues early
- Before committing: verify no regressions
- Debugging CI: reproduce locally with same format
