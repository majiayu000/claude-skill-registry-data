---
name: undo
description: Safely undo changes or go back to an earlier version of the code. Use when Steve says undo, go back, revert, "it was working before", or "I broke it".
---

# Undo safely

First ask Steve what he wants to undo. Then run `git status` and
`git log --oneline -10` to see where things stand, and explain it in plain words.

Pick the safe option:

- **Changes to one file that are not saved yet** (not committed):
  `git restore <file>`. This throws away those edits, so ask Steve first.
- **The last save** (commit) was bad: run `git revert HEAD`, then `git push`.
  This adds a new save that undoes the old one. Nothing is lost.
- **An older save**: find it with `git log --oneline`, then run `git revert <id>`.
- **Settings only**: change `settings.toml` back by hand.

Never use `git reset --hard`, `git checkout -- .`, `git clean` or a force push.
They delete work for good.

Undo never touches `data/` (the homes, statuses and notes), because git does not
save it. To undo a home's status, run `uv run python -m sellers mark <id> <status>`.

After the undo, run `uv run pytest` and show Steve that things work again.
