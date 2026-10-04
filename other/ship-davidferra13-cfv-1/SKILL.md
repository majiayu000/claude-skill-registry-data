---
name: ship
description: Git add, commit, and push everything to GitHub. The full "ship it" chain.
disable-model-invocation: true
---

# Ship It

Run the full ship chain. No confirmation needed, no questions asked.

1. `git add` all modified and created files
2. `git commit` with a clear, descriptive commit message summarizing the work done
3. `git push origin <current-branch>` to GitHub
4. Report what was committed and pushed

Use a HEREDOC for the commit message. Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>` at the end.

If there are no changes to commit, report that and stop.
