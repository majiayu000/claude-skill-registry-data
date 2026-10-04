---
name: close-session
description: Standard session close-out - stage, commit, push, update session log and build state.
disable-model-invocation: true
---

# Session Close-Out

Run these steps in order:

1. **Stage all changes** - `git add` every file that was modified or created
2. **Commit** - clear, descriptive commit message
3. **Push the current branch** - `git push origin <current-branch>`
4. **Update CLAUDE.md** - if any new patterns, rules, or decisions were made this session, add them now
5. **Update `docs/session-log.md`** - append departure entry:
   ```
   ## YYYY-MM-DD HH:MM EST
   - Agent: [type]
   - Task: [what you did]
   - Status: completed | partial | blocked
   - Files touched: [list every file you modified]
   - Commits: [commit hashes]
   - Build state on departure: [green | broken]
   - Notes: [anything the next agent needs to know]
   ```
6. **Update `docs/build-state.md`** if you ran a build or type check
7. **Report** - tell the developer what was committed and pushed
