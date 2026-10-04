---
name: proving-change-safety
description: >-
  Find what a change could break beyond the diff, then prove the one fact
  it is safe because of by running real code. Apply when the user asks
  what a change could break, whether a small diff is safe to merge, or
  to prove a safety fact before shipping. Use subsystem-walkthrough for
  how it works. Use design-rationale for motivation. Use dissect for a
  system-wide entity audit.
user-invocable: true
disable-model-invocation: false
version: "1.2.0"
author: "Ali Farahat"
tags: ["review", "safety", "verification"]
when_to_use: |
  USE WHEN:
  - The user asks what a change could break, or whether a small diff is safe.
  - A small-looking diff is about to merge and they do not trust it.
  DO NOT USE WHEN:
  - They want an onboarding explainer (use subsystem-walkthrough).
  - They want a full entity audit of an existing system (use dissect).
---

# Proving change safety

> **Leading words:** one safety fact, prove by running, unproven stays
> unproven, grep is not enough.

Listing callers is not the job. Grep those in a second. The job is the
breakage grep will not show.

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Read the change: symbols added, changed, deleted, including what the diff does not spell out.
2. Name the one fact it is safe because of.
3. Look where grep stops: library source, pinned version, microtasks, wire format, other languages, flags, code three hops down.
4. Honest risk list: chance, cost, `file:line`. Cleared items listed separately.
5. Prove the one fact by calling the real function (script or test). Leave the prove script in the tree. Cite its path in the reply. If you cannot get to "ran it", write **unproven**. If you ran it and the fact is false, write **do not ship** — that is not unproven.

## How sure

For each safety fact, get as far down this list as is cheap, and say where it stopped.

1. You said so. Worthless alone.
2. You pointed at `file:line` or the library's own source.
3. You walked the failure and it does not reach.
4. You ran it. A script or test that imports the same library the app ships and calls the exact function.
5. You reproduced it in the running app.

Step 4 is the bar. Unproven stays unproven.

## Reply contract

- What it does (including the non-obvious part)
- The one safety fact, the step you reached, and the proof path (or **unproven**)
- **do not ship** if the fact is false; **unproven** only if you did not run it
- Risks that remain
- Cleared
- Cheapest check to catch the real bug before merge
