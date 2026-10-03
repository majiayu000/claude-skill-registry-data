---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly (`TYPECHECK_CMD`), single test files regularly, and the full test suite (`TEST_CMD`) once at the end. Both commands live in `.claude/project.env`; an empty key means that check is off.

Once done, review the diff against the spec or tickets: every acceptance criterion met, nothing built beyond them.

Commit your work to the current branch. If that branch is the trunk (`GIT_TRUNK` in `.claude/project.env`, default `main`), create a branch with `scripts/worktree-create.sh <name>` and commit there instead.
