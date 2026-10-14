---
name: finishing-a-development-branch
description: Complete a Godot development branch — use when implementation is done and needs to be integrated into the main branch.
---

# Godot Finishing a Development Branch

## Checklist

Create TodoWrite for each item below, then work through them in order.

- [ ] **Verify** — `godot:verification-before-completion` passes (zero errors)
- [ ] **Review** — `godot:requesting-code-review` complete, all Critical/Important issues addressed
- [ ] **Clean log** — `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --log 200` shows zero errors
- [ ] **All commits clean** — no uncommitted changes: `git status`
- [ ] **Decide: merge or PR**

## Option A: Direct Merge

```bash
git checkout master
git merge feature/<feature> --no-ff -m "feat: <feature>"
git branch -d feature/<feature>
```

Verify after merge:
```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
$GDEXEC --play res://path/to/main_scene.tscn
sleep 2
$GDEXEC --stop
$GDEXEC --log 200
```

## Option B: Pull Request

```bash
git push origin feature/<feature>
gh pr create --title "<feature>" --body "$(cat docs/specs/<spec-file>.md)"
```

## Cleanup

If a worktree was used:
```bash
git worktree remove ../godot-toolkit-<feature>
```
