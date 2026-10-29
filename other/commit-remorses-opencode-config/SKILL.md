---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: commit
description: >
  Commit all uncommitted changes split into focused, detailed commits grouped by
  goal (including submodules). Covers .gitignore cleanup, splitting by file or
  hunk, finding the session that edited each file with `kimaki session editors`,
  and the `Session: ses_xxx` trailer. Load when the user asks to commit, "commit
  all", or commit in groups.
---

see git diff. if there are submodules also see their diff too.

if there are files that should not be tracked (like opensrc output, node_modules, tsbuildinfo files) add them to .gitignore first

understand the diff by also reading relevant files if the diff are from files you did not touch

analyze the diff and their goal. think of a nice split of groups of commits to split the diffs

each commit should be focused on a single set of changes only

group unrelated things in different commits. be very detailed in the commit messages

group by files if possible. hunks only if necessary

example principles to choose commit splits:

- are these files part of the same feature set? would these change break the codebase if not put together?
- were these files modified by a different agent? if so we should understand the changes and split in a different commit. understanding the second agent goals

if possible split the changes in smaller commits. if a commit diff includes 1000 of lines changes that's definitely too big.

each commit must use the original session that edited those files. do not put this session id on files another session changed.

find that session with:

```bash
kimaki session editors path/to/file.ts
```

the command prints session id, discord title, and time ago, newest first. use the title to understand what that session was doing. put that session id as the last line of the commit message:

```
Session: ses_xxx
```

if this session edited the files, use the current session id. if files come from different sessions, split into one commit per session.

NEVER ask for confirmation before committing. The user asking to commit IS the confirmation. Just do the commits directly without asking "should I proceed?" or showing a plan and waiting. Execute immediately.
