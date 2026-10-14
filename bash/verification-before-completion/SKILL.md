---
name: verification-before-completion
description: Verify Godot work is complete and error-free before claiming done or committing — use before every git commit.
---

# Godot Verification Before Completion

Run this before claiming any work is done. Zero errors required.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

## Checklist

Create TodoWrite for each item below, then work through them in order.

- [ ] `$GDEXEC --save-all` — save all scenes and scripts
- [ ] `$GDEXEC --play res://path/to/affected_scene.tscn` — run the affected scene
- [ ] `sleep 2` — wait for scene to initialize
- [ ] `$GDEXEC --stop` — stop playback
- [ ] `$GDEXEC --log 200` — read the full log

## Pass Criteria

- Zero `ERROR:` lines
- Zero `SCRIPT ERROR:` lines
- Zero `SHADER ERROR:` lines
- Expected `print()` output present (if any)

## If Errors Found

Do NOT commit. Invoke `godot:systematic-debugging`.

## After Passing

```bash
git add <changed files>
git commit -m "<type>: <description>"
```
