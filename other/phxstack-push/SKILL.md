---
name: phxstack-push
description: Commit this task's checked changes and push the current branch. Use after phxstack-check passes and the developer approves sending the change.
---

# phxstack-push

1. Confirm `phxstack-check` passed and the developer approved sending this
   change.
2. Inspect the working tree, diff, and staged diff. Separate task changes from
   unrelated work and scan staged content for secrets.
3. Commit with the repository convention, then push the current branch.

Keep `.phxstack/specs/` local. Do not stage, commit, or publish a spec unless
the developer explicitly gives the green light for that named spec.

Report the commit SHA and pushed branch. Do not force-push, amend a pushed
commit, switch branches, merge, deploy, or create a pull request unless asked.
