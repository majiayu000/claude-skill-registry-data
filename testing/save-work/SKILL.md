---
name: save-work
description: Save Steve's code changes to GitHub (git commit + push) in a safe, beginner-friendly way. Use when Steve says save, back up, commit, push, or after finishing a change.
---

# Save work to GitHub

Here "saving" means two things. A **commit** is a labelled save point on this
computer. A **push** copies that save point to GitHub as a backup.

1. Run `git status`. If nothing changed, tell Steve "Nothing new to save" and stop.
2. Safety check: never save `.env`, anything in `data/`, or any file that holds
   an API key or an owner's personal details. If you see one, stop and tell Steve.
3. Run the tests: `uv run pytest`. If they fail, fix the problem first, or ask
   Steve whether to save anyway.
4. Add the changed files by name: `git add <file> <file>`. Never use `git add .`.
5. Commit with a short, clear message, as the `git-commit` skill describes. For
   example: `git commit -m "feat: add Laguna Beach to my cities"`.
6. Push: `git push`. If it fails because GitHub has newer changes, run
   `git pull --no-rebase`, then `git push` again. If there is a conflict, stop
   and explain it to Steve simply. **Never force push.**
7. Tell Steve in one line what you saved. For example: "Saved and backed up:
   added Laguna Beach to your cities."

If the project has no GitHub copy of its own yet (`git remote -v` shows no
`origin`), only commit. Then offer the GitHub step in `docs/SETUP.md`.
