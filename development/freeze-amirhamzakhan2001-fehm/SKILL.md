---
name: freeze
description: Restrict file edits to a specific directory for the session. (gstack)
category: security
sources:
- repository: gstack
  original_path: freeze/SKILL.md
  sha256: b5beb26f22e55ed1cc9956a76bcd6986c4f6a262882e93fe0adbd831257e834f
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

## When to invoke this skill

Blocks Edit and
Write outside the allowed path. Use when debugging to prevent accidentally
"fixing" unrelated code, or when you want to scope changes to one module.
Use when asked to "freeze", "restrict edits", "only edit this folder",
or "lock down edits".

# /freeze — Restrict Edits to a Directory

Lock file edits to a specific directory. Any Edit or Write operation targeting
a file outside the allowed path will be **blocked** (not just warned).

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"freeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Setup

Ask the user which directory to restrict edits to. Use AskUserQuestion:

- Question: "Which directory should I restrict edits to? Files outside this path will be blocked from editing."
- Text input (not multiple choice) — the user types a path.

Once the user provides a directory path:

1. Resolve it to an absolute path:
```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"
```

2. Ensure trailing slash and save to the freeze state file:
```bash
FREEZE_DIR="${FREEZE_DIR%/}/"
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
STATE_DIR="$GSTACK_STATE_ROOT"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

Tell the user: "Edits are now restricted to `<path>/`. Any Edit or Write
outside this directory will be blocked. To change the boundary, run `/freeze`
again. To remove it, run `/unfreeze` or end the session."

## How it works

The hook reads `file_path` from the Edit/Write tool input JSON (shared
real-JSON extractor with /careful — one copy, sourced by both hooks), then
checks whether the path starts with the freeze directory. If not, it returns a
`hookSpecificOutput` payload with `permissionDecision: "deny"` to block the
operation (nested under `hookSpecificOutput` — Claude Code ignores a top-level
`permissionDecision`).

Polarity is fail-closed: a tool payload the hook cannot parse is DENIED, not
allowed — a boundary that fails open is not a boundary. A payload that parses
but has no `file_path` (a non-file tool) is allowed. Symlinks are resolved
through their FINAL component, so an in-boundary symlink pointing outside the
boundary is checked against its target.

The freeze boundary persists for the session via the state file. The hook
script reads it on every Edit/Write invocation. Boundaries containing spaces
are supported.

## Notes

- The trailing `/` on the freeze directory prevents `/src` from matching `/src-old`
- Freeze applies to Edit and Write tools only — Read, Bash, Glob, Grep are unaffected
- This prevents accidental edits, not a security boundary — Bash commands like `sed` can still modify files outside the boundary
- To deactivate, run `/unfreeze` or end the conversation

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [security/careful](../careful/SKILL.md)
- [security/unfreeze](../unfreeze/SKILL.md)

## Source provenance

- `gstack/freeze/SKILL.md`
