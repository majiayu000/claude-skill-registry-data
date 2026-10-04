---
name: ship
description: Open a pull request with a clean commit history and a body that explains the change. Invoke explicitly when work is reviewed and ready to go out.
argument-hint: [optional PR title or context]
disable-model-invocation: true
---

Ship the current work: $ARGUMENTS

Only you invoke this. Shipping is outward-facing and hard to walk back, so it is never something Claude decides on its own because the code looks done.

## Gate

Stop and report instead of proceeding if any of these is true:

- The diff hasn't been reviewed — run `/preflight:review` first.
- Tests aren't passing, or you haven't run them. Delegate to `test-runner`.
- You're on the default branch. Branch first; never commit straight to `main`.
- There are unrelated changes in the diff. Split them.
- The change made a doc false. Grep the docs for what you touched. Shipping a README that describes behavior you just changed is shipping a bug — the reader trusts it more than the code.

## Commits

One concern per commit. If a commit message needs "and", it's probably two commits.

Write messages that explain *why*. The diff already shows what changed; the reader six months out needs the reason. Reference the issue if there is one.

Match the repository's existing conventions — read `git log` before writing your first message. If the project uses Conventional Commits, use them; if it doesn't, don't impose them.

## PR

1. Push the branch to the remote.
2. Open the PR with `gh pr create`.

The body covers: what changed and why, how to verify it, and anything the reviewer should look at closely. Note what you deliberately left out of scope. If the change is user-visible, say what users will notice.

Keep it honest and specific. Do not claim tests pass that you didn't run, and do not describe verification you didn't perform.

## Stop

Report the PR URL and stop. Do not merge — a human reviews and merges. If CI fails, report the failure; fix it only if asked.
