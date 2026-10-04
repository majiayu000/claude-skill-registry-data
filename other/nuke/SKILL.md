---
name: nuke
description: "Use only when the human types /nuke. Throws away the worktree you're in: stop what you started for it, release the lock, remove the tree, delete the local branch, report, hold. Refuses if the branch has commits no remote has. The undo of worktree."
disable-model-invocation: true
---

# Nuke

The human's one word for "throw this workspace away." You never reach for it on your own; the human typing `/nuke` is the approval the `worktree` skill asks for before anything running goes.

You know this tree's stack, because you started it. A dev server, a compose stack, a container runtime of any name, a database, a watcher, none of them, all of them. Stop what you started, the way that stack stops, and don't go looking for anything else.

## In order

1. **Check the branch.** Fetch, then see whether any remote branch holds your last commit:

   ```bash
   git fetch --all --prune
   git branch -r --contains HEAD
   ```

   If nothing prints, stop, list the commits with `git log --oneline @{upstream}..HEAD` (or against the base in the lock), and tell the human to push or drop them. That's the one thing nuke can't undo, so nothing else happens until they do.

2. **Stop what you started for this tree.** Every process, stack, and container this task brought up, stopped the way its stack stops: the dev server killed, `down` with volumes for a compose project of yours, the container runtime's own remove for a plain container. Only what this tree started. The shared checkout's stack, another agent's tree, a database more than one checkout reads: not yours, leave them.

3. **Release the lock.** From the squirrel skills folder, `python3 scripts/worktree_lock.py release --path <worktree-path> --status released`. If there's no lock, say so in the report.

4. **Remove the tree.** From outside it, `git worktree remove --force <worktree-path>`. Uncommitted files go with it; that's the point.

5. **Delete the local branch.** `git branch -D <branch>`. The remote branch and any PR stay, since deleting reviewable work is a different decision.

## The report

Four lines, then nothing:

```
running   what you stopped, or "nothing was running"
worktree  the path, removed
branch    the name, deleted locally; the remote branch and any PR are untouched
lock      released, or "no lock"
```

If a step fails, stop there and say what already went, so the receipt is true even when the run is cut short. No next step, no offer. Hold.

## Never

- Run it because you think the work is done. Only the human runs it.
- Stop, remove, or down anything this tree didn't start.
- Widen it to a remote branch, a PR, or the main checkout.
- Keep going after the report.
