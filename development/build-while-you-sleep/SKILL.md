---
name: build-while-you-sleep
description: Get the most done with several agents at once, builders write code in one shared tree with no test runs, a supervisor tests everything that landed together on a timer and removes the bottleneck each round. Use when you say "/build-while-you-sleep", "keep going", "finish the code", "no test runs", "group and test", "what's the bottleneck", "run agents in parallel", and on every supervisor wake-up.
---

# Run agents in parallel: finish the code, test as a group, remove the bottleneck

When several agents work at once, the slow part is rarely the typing. It's each one stopping to run its own
tests, waiting on the others, and proving the same thing twice. This setup splits the work in two:

- **Builders** finish real code and never wait.
- **One supervisor** tests everything that landed together, on a timer, routes failures back, and removes the
  biggest bottleneck every round.

The default round is 12 minutes. Pick what fits your project: long enough for a combined pass to finish, short
enough that a failure comes back while the builder still remembers the change.

## Before you start (once)

Find these in the project, or ask the user if they don't exist:

- **The shared tree and branch.** Builders all commit to one place, usually `main`. If the project forbids that,
  use one shared integration branch, never one branch per builder.
- **The fast load check.** The cheapest check that a file at least loads: a compile, a type check, a syntax
  check, a lint. Examples: `node --check`, `tsc --noEmit`, `python -m py_compile`, `cargo check`, a game
  engine's headless check-only mode. Plus any project rule checker that runs in seconds.
- **The combined pass.** The one full run the supervisor does: the test suite, one app or game run, one batch of
  screenshots or renders of the views that changed. Note how long it takes.
- **The ledger.** A plain file the supervisor appends to, for example `docs/SUPERVISOR_LEDGER.md`, with a "Now"
  list of pieces waiting to be picked up. Create it if missing.

## Builders: finish, don't prove

- Write the real code in the shared tree. No private branch, no copy, no private bridge, no scratch folder.
- The only check is the fast load check on what you touched. A file that doesn't load never stays in the tree.
- Run nothing else: no probes, no test runs, no headless app runs, no renders. Find causes by reading the code
  and the logs and screenshots that already exist.
- Commit small and often, by path (`git commit -- <your files>`, after checking the index holds only yours).
  Push if the project pushes.
- Report in two lines: what changed, and how to see it (the switch, the screen, the demo hook).
- Never wait on a test. Start the next piece at once. A failure comes back from the supervisor; fix it then.

## Supervisor: the round

Keep the loop alive. In Claude Code: `/loop 12m /build-while-you-sleep`. In other agents: a scheduled task, a
cron job, or a shell loop that re-prompts the supervisor every 12 minutes. Each round:

1. **What landed.** `git log --since="12 minutes ago" --stat` on the shared branch. Nothing new: skip to step 4.
2. **One combined pass** on the shared tree, in the background. One instance of any heavy tool at a time (check
   with `pgrep` first). Fast load check of everything, the test suite or one app run, one batch of screenshots
   or renders of every view the round touched.
3. **Route the results.** Each failure goes to the builder who owns it, with the log line or screenshot and the
   commit. Use your agent's messaging between agents if it has one; otherwise write it into the ledger under
   that builder's name. Don't fix it yourself. Screenshots of visible changes go to the user straight away,
   unasked.
4. **Find the bottleneck.** Answer these and pick the worst:
   - Who is waiting? On a slow machine, a review, the user, a file another builder owns, a download.
   - Who is idle? Give them the next piece from the ledger's "Now" list.
   - What is being done twice? Two agents on one job, or a check repeating one already done.
   - Which step is slower than the code it checks?
   - What keeps failing in the combined pass? A file everyone collides on gets one owner.
5. **Measure it, then remove it.** A bottleneck is a number, not a name. Split the slow thing into its parts
   with timings from the logs you already have, and ask what each part does that it needn't. Fix the step's
   own waste (repeated setup, waiting, work redone) before trimming what goes into it. Then remove the biggest
   part this round: reassign, split a file's ownership, cut or restructure the slow step, or unblock with a
   decision (only product calls the user has handed to you; log each one). Never add a step or a gate.
6. **Log one line** in the ledger: time, what landed, pass or fail, the bottleneck with its numbers, what was
   removed. The same bottleneck in two lines means the last fix didn't work. Break it down further; don't log it
   a third time.

## Never

- Per-change test runs, private bridges, scratch copies, probes before fixing, per-builder renders.
- "Behind a flag", two systems doing one job, keeping the old path around "just in case".
- A builder waiting on anything. A supervisor waiting on builders.
- Treating a slow step as fixed ("the GPU", "the build") without timing its parts.
- Swapping, stashing, resetting or rebasing the shared tree.

## When not to use it

This trades safety per change for speed overall. Don't use it on a tree that deploys on every push, or where
a broken `main` blocks other people. Use a shared integration branch there, and merge it after a green pass.

## Related

`fix-it-for-real` (how code is changed and committed), `dont-break-it`, `ship-it` (taking the
finished work to release).
