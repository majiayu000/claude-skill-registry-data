---
name: ship
description: "Run the auditors for every exit condition in scope for the requested ship target (review or release), and on pass run the ship steps the organization declared for that target."
---

## User Input

You **MUST** consider the user input before proceeding.

## Purpose

`/akka:ship` runs the auditors for every applicable exit condition in scope for
the requested ship target, and on pass runs the ship steps the organization
declared for that target. The target argument is REQUIRED. Two targets are
accepted:

- **`review`** — runs the auditors for every applicable exit condition tagged
  `author` or `review`. On pass, runs the organization's review ship steps
  (typically push the branch and open a pull request).
- **`release`** — runs the auditors for every applicable exit condition at any
  tier (`author`, `review`, and `release`). On pass, runs the organization's
  release ship steps (typically deploy to production).

Author-time is a precondition, not a ship target. There is no `/akka:ship
author`.

The author-time conditions are evaluated first, on their own, before any
higher-tier auditor is given a chance. In À la carte mode the gate is advisory
like every other condition: the run continues, every in-scope tier is
evaluated, and the user gets the complete picture to override against.

In Enforced mode a ship that fails them stops right there — the review-time and
release-time checks never run, so a ship that cannot succeed does not first
spend minutes on scanning, dynamic analysis, or live-service probes. The user
sees only the author-time verdict, which is the only one that has been computed.

An active waiver satisfies the precondition exactly as it satisfies any other
condition — a waiver is a person's time-bound, recorded acceptance, not a
bypass.

## Outline

1. **Parse the target from `the user's request`.** Read the first argument. It MUST be
   `review` or `release`. If missing, invalid, or anything else, stop and tell
   the user: *"`/akka:ship` requires an explicit target: `review` or `release`.
   For example: `/akka:ship review`."* Do not call the CLI.

2. **Invoke the CLI.** Run `akka specify ship <target>` in the project directory
   (via the shell). Capture the output. The CLI:
   - Runs the author-time auditors first; in Enforced mode stops there if any
     of them blocks.
   - Otherwise runs the auditors for every remaining applicable exit condition
     in scope for the target.
   - Reports the verdict (`READY_TO_SHIP` or `NOT_READY`).
   - In À la carte mode, records an explicit override and proceeds even when
     the verdict is `NOT_READY`.
   - In Enforced mode, refuses to run any ship steps unless the verdict is
     `READY_TO_SHIP`.
   - Writes a conformance receipt recording which target was shipped, what was
     verified, and any conditions that remained `open` with their reasons.

3. **Report plainly.** Present the CLI output. Do not restate internal condition
   ids, check keys, or the words "auditor" / "coverage gate" / "adequacy review".
   If the ship succeeded, say so and name the target that was shipped. If the
   ship refused, say what would unblock it — the reason field on each blocking
   condition is the user-facing action.

   When the refusal came from the author-time precondition, say so explicitly
   and say that the later checks were not run. Do not describe the remaining
   conditions as passing, failing, or outstanding — nothing is known about them
   yet. "Your own checks have to pass before the rest even run" is the honest
   framing.

## Key rules

- The target is required. Never invoke the CLI without one.
- Never invent a target. If the user typed only `/akka:ship`, ask which target
  they intended rather than guessing.
- Ship steps are org-specific. This command runs the auditors and, on pass,
  hands off to whatever steps the organization declared in its policy.
- The author-time precondition is checked before anything else, in both modes.
  In À la carte mode it is reported and the run continues; in Enforced mode it
  is where the run stops on failure.
- How a condition is judged never depends on the mode. What differs is
  ship-gating (advisory in À la carte, blocking in Enforced) and, as a
  consequence, how much gets evaluated before a blocked ship gives up.
- Where the exit-condition set is dormant, a ship has no definition of done to
  clear and proceeds. Say that the project has no checks set up rather than
  announcing that it passed them.

## Done When

- [ ] The target was parsed from `the user's request` and validated as `review` or
      `release`; missing or invalid targets were reported to the user without
      calling the CLI.
- [ ] `akka specify ship <target>` was invoked with the validated target.
- [ ] The plain outcome was shown to the user, and any blocking conditions
      were surfaced with their user-facing reasons (no internal ids, no
      machinery words).
- [ ] If the refusal came from the author-time precondition, the report said so
      and did not characterize the checks that never ran.
