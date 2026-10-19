---
name: systematic-debugging
description: "Root-cause debugging in four phases: investigate, analyze, hypothesize, implement. Iron Law -- no fixes without root cause. Thin ytstack wrapper around the vendored superpowers systematic-debugging procedure, routing findings into KNOWLEDGE.md / DECISIONS.md. Use when hitting a bug, test failure, or unexpected behavior."
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - AskUserQuestion
---

# ytstack:systematic-debugging

Thin wrapper around the vendored superpowers `systematic-debugging` skill (`vendor/superpowers/skills/systematic-debugging/SKILL.md`). Injects ytstack project context, then inlines the vendored procedure verbatim. Findings are routed into ytstack artifacts. Vendor is single source of truth.

## ytstack context (resolved at render time)

```!
cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$PWD/.ytstack" ]; then _YT_DIR="$PWD/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_M=none; _T=none
if [ -n "$_YT_DIR" ] && [ -f "$_YT_DIR/STATE.md" ]; then
  _M=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
  _T=$(sed -n 's/^active_task: *//p' "$_YT_DIR/STATE.md" | head -1)
fi
echo "HAS_YTSTACK: $([ -n "$_YT_DIR" ] && echo yes || echo no)"
echo "YT_DIR: $_YT_DIR"
echo "CURRENT_MILESTONE: $_M"
echo "ACTIVE_TASK: $_T"
```

## ytstack invocation notes

You are invoked inside a ytstack project (or without -- systematic-debugging is useful outside ytstack too). The Iron Law from the vendored skill holds: no fixes until root cause is identified.

HARD-GATE: none. Debugging may happen before ytstack is initialized.

After the vendored procedure completes:
- If `HAS_YTSTACK=yes` and the root cause reveals a project-level pattern (e.g. "config race between env-vars and config.json reads that will recur elsewhere"), append to `KNOWLEDGE.md` under `## Gotchas` or `## Lessons learned`.
- If the root cause forces an architectural decision (e.g. "we must enforce X pattern across all future modules"), append to `DECISIONS.md` in append-only format.
- If the root cause relates to an active task, reference it in the task-plan body so future sessions see the context.

## Vendored procedure (inlined verbatim)

```!
cat "${CLAUDE_SKILL_DIR}/../../vendor/superpowers/skills/systematic-debugging/SKILL.md"
```
