---
name: conform
description: "Run the in-scope auditors, print the definition-of-done manifest, and return the engine verdict — READY_TO_SHIP or NOT_READY."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

`/akka:conform` runs the in-scope auditors and reports whether the feature is
ready to ship. For every machine-checkable exit condition it runs the
condition's auditor — building, testing, linting, or probing as the check
requires — and resolves it to a state. It then prints the same manifest
`/akka:status` shows, and returns a verdict.

The verdict is assessed against the **release** tier, so it covers every
applicable condition at every ship tier — not just the tier you happen to be
shipping to next.

Two commands sit close to this one and are not it:

- **`/akka:status`** prints the same manifest but never runs an auditor.
  Status leaves machine-checkable conditions `open`; conform resolves them.
  Once conform has evaluated, the two agree.
- **`/akka:converge`** diffs the codebase against the spec, plan, and tasks and
  queues unbuilt work. Conform evaluates the exit conditions and reports
  readiness. Neither substitutes for the other.

`/akka:ship` reads this same verdict — in Enforced mode it releases only when
the verdict is `READY_TO_SHIP`.

## The verdict

- **`READY_TO_SHIP`** — every applicable condition is `green` and not stale, or
  covered by an effective waiver.
- **`NOT_READY`** — any other combination.

A `NOT_READY` verdict says what is blocking and what to do about it:

- conditions `open` with reason `needs-user-action` are waiting on the user;
- conditions `open` with reason `blocked-outside-project` need a tool or policy
  change beyond this project — never treat one as a failure the user caused;
- stale greens need their auditor re-run.

## Outline

1. **Evaluate.** Call `akka_ec_conform` for the project directory. This runs
   the available auditors and returns the manifest plus the verdict. It is the
   full CLI pipeline — org floor, project strikes, waivers, sign-offs, and mode
   — so it agrees exactly with `akka specify conform`.

   This is not a cheap call. It executes real builds and probes. Do not run it
   speculatively or in a loop; if the user only wants to see where things
   stand, `/akka:status` is the read-only view.

2. **Report the plain outcome.** Call `akka_ec_summary` and present it to the
   user **verbatim**. It is the user-facing summary, and it contains no
   internal ids or machinery words by construction.

3. **Surface the blockers.** For a `NOT_READY` verdict, list what is blocking,
   each with its user-facing reason and the action it implies. Distinguish the
   two `open` reasons — waiting on the user is a different ask from blocked
   outside the project, and collapsing them sends people to fix the wrong
   thing. Name stale greens as needing a re-run, not as failures.

   Prohibition (NEVER) conditions resolve in their own section of the manifest.
   An unaudited prohibition reds — say so plainly rather than reporting it as
   an ordinary open item.

   Do not restate internal condition ids, check keys, or the words "auditor" /
   "coverage gate" / "adequacy review". Offer *"say 'show details' for the full
   checklist"* for the manifest.

## Key rules

- Report the verdict the engine returned. Never soften a `NOT_READY`, and never
  infer `READY_TO_SHIP` from a manifest that looks clean — the verdict accounts
  for staleness and waiver effectiveness, which reading states does not.
- The mode does not change the verdict. Conform judges identically wherever the
  exit-condition set is active; only `/akka:ship` acts on the verdict
  differently. Never restate a `NOT_READY` as though it were a pass because the
  project is À la carte — but do say what it means there, because a verdict
  that reads as a blocker when nothing is blocked is its own kind of wrong.
  Report the verdict, then name the consequence: in À la carte, that ship
  proceeds anyway with a recorded override.
- Where the exit-condition set is dormant there is nothing to conform to.
  Say so plainly — the project has no checks set up yet — and do not present a
  `READY_TO_SHIP` over the Akka baseline as though the project had passed a
  definition of done it never defined.
- Never resolve a condition to get a better verdict. Sign-off, strike, and
  waive are the user's decisions to record, not steps to reach `READY_TO_SHIP`.
- `blocked-outside-project` is not the user's failure. Report it as a missing
  tool or policy change and name what is missing.

## Done When

- [ ] `akka_ec_conform` was called once for the project directory and its
      verdict was reported as returned.
- [ ] The plain `akka_ec_summary` was shown to the user verbatim (never
      internal ids or machinery words).
- [ ] For `NOT_READY`, every blocking condition was surfaced with its
      user-facing reason, with `needs-user-action`, `blocked-outside-project`,
      and stale greens distinguished from each other.
- [ ] Any red prohibition was named as a prohibition rather than folded in with
      the ordinary open items.
- [ ] No condition was signed off, struck, or waived in the course of running
      this command.
