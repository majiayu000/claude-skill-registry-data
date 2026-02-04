---
name: amnesiac
description: Autonomous software development for agents with no persistent memory. Use when building, testing, or maintaining code projects. Ensures all work is independently verifiable without context from previous sessions.
---

# amnesiac

You will forget everything. Design accordingly.

## First Step

Check if `.amnesiac/status` exists.

- **Exists** → read it, continue below
- **Does not exist** → read [adopt.md](adopt.md) to set up this project

## Protocol

1. Read `.amnesiac/status`
2. Load the phase file indicated
3. Do the work
4. Update `.amnesiac/status`
5. Commit

## Status Format

```
phase: [define|design|implement|maintain]
task: [current task number or description]
next: [literal next action]
files: [space-separated list]
verify: [command that returns 0 on success]
```

## Phase Files

Load only the file matching your current phase:

- `phase: define` → read [define.md](define.md) - establish goal with user
- `phase: design` → read [design.md](design.md) - create verifiable plan
- `phase: implement` → read [implement.md](implement.md) - build with tests
- `phase: maintain` → read [maintain.md](maintain.md) - fix and extend

## Reference Files

Load only when stuck:

- [patterns.md](patterns.md) - approaches that work
- [antipatterns.md](antipatterns.md) - approaches that fail

## Rules

1. If you can't verify it without a browser, don't build it
2. If verify fails 3 times, write to `stuck` field and stop
3. If a task touches 5+ files, split it first
4. Commit after every passing verify
