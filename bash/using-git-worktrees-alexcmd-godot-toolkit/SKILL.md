---
name: using-git-worktrees
description: Use git worktrees to isolate Godot feature branches — use when starting feature work that needs isolation from the main branch.
---

# Godot Using Git Worktrees

## Create a Worktree

```bash
TOOLKIT="$(git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel)"
cd "$TOOLKIT"
git worktree add ../godot-toolkit-<feature> -b feature/<feature>
cd ../godot-toolkit-<feature>
```

## Re-establish AgentBridge

The AgentBridge module symlink is NOT copied to the new worktree. Re-link it:

```bash
# From the new worktree directory
bash install.sh
```

This re-runs the junction/symlink for the AgentBridge module.

## Work in the Worktree

Implement the feature. Commit freely. The main branch is unaffected.

## Merge Back

```bash
TOOLKIT="$(git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel)"
cd "$TOOLKIT"
git merge feature/<feature> --no-ff -m "feat: <feature>"
git worktree remove ../godot-toolkit-<feature>
git branch -d feature/<feature>
```

## Verify After Merge

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
$GDEXEC --play res://path/to/main_scene.tscn
sleep 2
$GDEXEC --stop
$GDEXEC --log 200
```

Zero errors required after merge.
