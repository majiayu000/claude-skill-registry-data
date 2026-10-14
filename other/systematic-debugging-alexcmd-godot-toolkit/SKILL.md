---
name: systematic-debugging
description: Debug Godot issues systematically using AgentBridge — use instead of guessing whenever an error, crash, or unexpected behavior occurs.
---

# Godot Systematic Debugging

Never guess. Follow this protocol exactly.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

## Step 1: Get the log

```bash
$GDEXEC --log 200
```

Read every line. Find the **first** error, not just the last. The root cause is usually the first one.

## Step 2: Reproduce with execute

```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
if root == null:
    print("ERROR: no scene open")
    return
print("Root: ", root.name)
# reproduce the minimal condition that triggers the error
GD
$GDEXEC --log 50
```

## Step 3: Isolate

Narrow to the smallest failing unit:
- Comment out code paths
- Test individual methods with `$GDEXEC --execute`
- Check if the error exists without your changes: `git stash` → `$GDEXEC --log`

## Step 4: Form a hypothesis

Write one sentence: "The error occurs because X."

Do not proceed to Step 5 without a hypothesis.

## Step 5: Fix

Make exactly one change. No shotgun changes.

## Step 6: Verify

```bash
$GDEXEC --save-all
$GDEXEC --execute - <<'GD'
# reproduction from Step 2
GD
$GDEXEC --log 100
```

Zero errors = fix confirmed. If errors remain, return to Step 1.

## Rules

- Never make more than one change per iteration
- Never skip an error by commenting it out
- After 3 failed iterations: run `godot:docs` on the relevant API before trying again
