---
name: power-quick
description: Use when a change is small and already understood - at most three files, such as a typo, a config value, a rename, or a one-line bugfix - and a plan file would cost more than the change
---

# Deliver a Bounded Change

Read [collaboration](../../references/collaboration.md) and
[safety](../../references/safety.md) before acting.

## The scope gate

This skill is for changes that are small **and** understood. Both, not either.

Escalate to `pwdev-power:power-brainstorm` the moment any of these is true:

- more than three files would change
- you cannot name the failure mode of the change
- it adds a new interface, dependency, or migration
- it touches auth, payments, permissions, or data deletion
- you are about to write "while I'm here"

Escalating is not failure. Discovering mid-change that this was never quick, and continuing
anyway, is.

## Steps

1. **Read before proposing.** Read the actual files. A quick change proposed from memory of a
   codebase is a guess. `.planning/power/context/project.md`, if it exists, gives you the
   conventions without exploring — which is the whole point on a change this small.
2. **Present a mini-plan**: what changes, in which files, and how you will verify it. Three or
   four lines.
3. **Gate.** Wait for a yes.
4. **Implement.** If this is a bugfix, `pwdev-power:power-tdd` still applies — a bug means a
   test was missing, and "it is only one line" is the most common way that test never gets
   written.
5. **Verify.** Run the real command, read the real output. `pwdev-power:power-verify` states
   the standard: evidence before the claim.
6. **Commit** with a message that says why, not what. The diff already says what.

## Record

Write `.planning/power/quick/<date>-<slug>/contract.md` with the mini-plan you agreed to, and
`report.md` with what you did and the verification output. Two short files.

They exist because "quick" changes are the ones nobody can explain three months later, and
because a pattern of quick changes to the same area is evidence that the area needs a real
plan.
