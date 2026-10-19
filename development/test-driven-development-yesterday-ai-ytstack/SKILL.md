---
name: test-driven-development
description: "RED-GREEN-REFACTOR: write a failing test, watch it fail, write minimal code, watch it pass, commit. Thin ytstack wrapper around the vendored superpowers test-driven-development procedure, injecting the current task's plan as context. Use during task execution."
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - AskUserQuestion
---

# ytstack:test-driven-development

Thin wrapper around the vendored superpowers `test-driven-development` skill (`vendor/superpowers/skills/test-driven-development/SKILL.md`). Injects the current task's plan (Files + Verification sections) as context, then inlines the vendored procedure verbatim. Vendor is single source of truth.

## ytstack context (resolved at render time)

```!
cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$PWD/.ytstack" ]; then _YT_DIR="$PWD/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_M=none; _S=none; _T=none
if [ -n "$_YT_DIR" ] && [ -f "$_YT_DIR/STATE.md" ]; then
  _M=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
  _S=$(sed -n 's/^active_slice: *//p' "$_YT_DIR/STATE.md" | head -1)
  _T=$(sed -n 's/^active_task: *//p' "$_YT_DIR/STATE.md" | head -1)
fi
_TASK_PLAN="$_YT_DIR/$_M-$_S-$_T-PLAN.md"
echo "HAS_YTSTACK: $([ -n "$_YT_DIR" ] && echo yes || echo no)"
echo "ACTIVE_TASK: $_M-$_S-$_T"
echo "TASK_PLAN: $_TASK_PLAN"
echo "TASK_PLAN_EXISTS: $([ -f "$_TASK_PLAN" ] && echo yes || echo no)"
```

## ytstack invocation notes

You are invoked inside a ytstack project. The work unit is the current task (`_M-_S-_T` above) whose plan file at `TASK_PLAN` contains the `## Files` section (what to touch) and `## Verification` section (how to know it passes). The vendored TDD procedure uses these: the RED test targets the behavior described in the task-plan body; the verification command is the one specified in the plan's Verification section.

HARD-GATE: if `HAS_YTSTACK=no` or `TASK_PLAN_EXISTS=no`, abort with: "Run `ytstack:plan-task` first to produce the task-plan." Do not invoke the vendored procedure; TDD without a target task-plan is guessing.

After the vendored procedure completes (test passes + refactor done):
- Do NOT run `ytstack:summarize-task` automatically; the user triggers that when ready.
- If a behavior decision was made during TDD that was not in the plan, append a note to the task-plan's body or log to `KNOWLEDGE.md` if it generalizes.

## Vendored procedure (inlined verbatim)

```!
cat "${CLAUDE_SKILL_DIR}/../../vendor/superpowers/skills/test-driven-development/SKILL.md"
```
