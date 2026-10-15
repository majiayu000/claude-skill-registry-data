---
name: root-cause-tracing
description: Use when fixing a bug. Trace along the call chain to the source — don't stop at the symptom.
---

# Root-Cause Tracing

A bug surfaces at the symptom. The fix belongs at the cause. The two are rarely in the same file.

## Iron Law

**Keep asking "why does this state exist?" until the answer is a decision, not another effect.** Stop one level too early and you'll patch a symptom and ship the bug.

## Red Flags

- Wrapping the failure point in `if (x != null)` without knowing why `x` was null.
- Adding a `try/catch` that swallows the error to "make it pass."
- Coercing types at the boundary to make the function not throw.
- "It happened because of bad input" — yes, but *who produced the bad input, and why?*
- Stopping at the first plausible explanation that lets you write a fix.

If your fix is the same shape as the symptom, you're symptom-patching.

## The "Five Whys" Walk

Classic but works. Each "why" should move you one frame up the call stack, one layer deeper into the system, or one step earlier in time.

Example: API returns 500.

1. **Why 500?** Handler threw `NullReferenceException`.
2. **Why null?** `user.Profile` was null when we accessed `user.Profile.Email`.
3. **Why was Profile null?** `LoadUser()` didn't include the Profile relation.
4. **Why didn't LoadUser include it?** New endpoint reused old `LoadUser`, but old callers don't need Profile.
5. **Why did the new endpoint use the lean loader?** No overload existed; dev copied the old call without checking what it loaded.

Root cause: missing overload + no compile-time signal that Profile is required. Fix: add `LoadUserWithProfile()` (or make Profile lazy with explicit fetch), update the new endpoint. Symptom-fix would have been a null-check in the handler — bug still there for the next endpoint.

## Where to walk

- **Up the call stack** — who called the failing function with this state?
- **Back in time** — when was this object constructed / mutated to look like this?
- **Across boundaries** — did this value come from another service / DB / user? What did *they* think they were sending?
- **Into invariants** — what was supposed to be true here, who's supposed to maintain it, where did that maintenance fail?

## How to know you've hit root cause

You've reached it when the answer is one of:

- A **decision** someone made (correct at the time, wrong now)
- A **missing contract** (no one agreed who maintains this invariant)
- An **assumption** that no longer holds (input was always ASCII; now it isn't)
- A **design gap** (no place for this case to be handled)

If your next "why" answer is *another effect* or *another piece of code doing something*, you're not at root yet.

## Symptom-fix vs. root-cause-fix

| Symptom-fix | Root-cause-fix |
|---|---|
| Patches the crash site | Patches the cause site |
| One bug, one band-aid | Eliminates the *class* of bug |
| Grows the codebase (more guards) | Often shrinks it (removes the bad path) |
| Next similar bug shows up next week | Next similar bug never appears |

Sometimes you legitimately want symptom-protection too — see [[defense-in-depth]]. But that's *in addition to* the root fix, never *instead of*.

## When symptom-fix is acceptable

- Production is bleeding *right now* — patch the symptom, file a ticket for the root cause, fix it tomorrow.
- The root cause is in a system you don't own — guard at your boundary, escalate upstream.
- The "root" is genuinely user input you can't change — validate / sanitize at the boundary, but make sure the validation is the contract, not an afterthought.

In each case, you've consciously decided to stop tracing. That's different from giving up at the first wrap.

## MUST

- MUST trace at least 3 "whys" before declaring a fix.
- MUST distinguish "I found the root" from "I found a place to patch."
- MUST NOT add defensive guards as the entire fix when the cause is fixable.

## Cross-references

- [[systematic-debugging]] — root-cause tracing is the heart of Phase 3.
- [[defense-in-depth]] — guards are valid *additionally*, not *instead of*, root fixes.
- [[verification-before-completion]] — a root-cause fix needs verification at the symptom site AND in adjacent paths.
