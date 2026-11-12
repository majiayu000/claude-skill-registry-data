---
name: ship
description: Use when the user says "/ship", "ship it", "commit and push", "is it committed", or at the end of a work chunk that touched a repo. Commits, pushes and reports proof in one pass.
---

# /ship: commit, push, prove

1. Target: no argument means the vault (`$ECX_VAULT`); an argument names a project repo.
2. `git status --short`. If clean: "nothing to ship" plus the last commit hash, then stop.
3. Code repos: never commit to main/master. Create or switch to a feature branch first. (Your notes vault may commit to its default branch.)
4. Split into logical commits by topic (2 to 5 is typical). Conventional messages: `feat:`, `fix:`, `notes:`, `content:`.
5. Push the current branch.
6. Report proof in exactly this shape:

```
Shipped: <n> commits pushed to <branch>
<hash> <message>
<hash> <message>
```

If the push fails, show the real error. Never say shipped when it isn't.
