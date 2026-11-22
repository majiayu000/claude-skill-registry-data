---
name: commit
description: Commit changes - stage the current changes and write a clear git commit message
---
# Commit

1. Run `git status` and `git diff` to see every change. If nothing changed, say so and stop.
2. Check for files that should not be committed (.env, keys, large binaries, build output).
   If you see any, stop and ask the user before staging.
3. Stage the relevant files by name (avoid `git add -A` if unrelated files are present).
4. Write the message: a subject line under 70 characters in the imperative ("Add …", "Fix …"),
   a blank line, then a short body saying why the change was made.
5. Commit, then run `git log -1 --stat` and report the result.
Never push, amend, or force anything unless the user asks.
