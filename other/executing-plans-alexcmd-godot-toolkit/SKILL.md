---
name: executing-plans
description: Execute a written Godot implementation plan step by step — use when you have a plan document to implement.
---

# Godot Executing Plans

Execute the plan one checkbox at a time. Do not skip steps. Do not advance until the current step is verified.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

## Before Starting

1. Read the plan file
2. Review critically — raise any concerns with the user before proceeding
3. If concerns: raise them before starting
4. If no concerns: Create TodoWrite and proceed

For each task: mark `in_progress` before starting, `completed` only after checkpoint passes.

## Checkpoint Protocol

After every task:

```bash
$GDEXEC --save-all
$GDEXEC --execute - <<'GD'
# smoke test relevant to this task
GD
$GDEXEC --log 100
```

If `--log` shows `ERROR:` or `SCRIPT ERROR:` lines: **STOP**. Fix before continuing. Do not mark the task complete.

## Before Each Commit

Run `godot:verification-before-completion`:
```bash
$GDEXEC --save-all
$GDEXEC --play res://path/to/affected_scene.tscn
sleep 2
$GDEXEC --stop
$GDEXEC --log 200
```
Zero errors required before committing.

## If Blocked

- Log the issue as a comment on the plan checkpoint
- Invoke `godot:systematic-debugging`
- Do not attempt more than 3 different fixes without pausing to reassess the approach

## Tracking

Mark each checkbox only after:
- [ ] Code written
- [ ] `$GDEXEC --save-all` called
- [ ] `$GDEXEC --log` shows zero errors
- [ ] Committed

## After All Tasks Complete

Invoke `godot:finishing-a-development-branch`.
