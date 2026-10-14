---
name: loop
description: Emma's daily work loop across every project (target, spike, plan, implement, complete, polish). Use when a session starts with no contract in ~/.now, when work drifts from the contract, when a spike or polish pass has no end, or when Emma asks "what am I doing", "where was I", "am I drifting", or wants to close out a session.
---

# Loop

State lives in files. Triggers live in hooks. Judgment lives here.

Commands in `~/bin`: `now`, `park`, `fin`, `loops`. The SessionStart hook runs `now --hook`.

## Invariants

- No engineering before `~/.now` holds a contract. If it is empty, ask for one line: deliverable, done-when, duration. Default 90m.
- One contract at a time. A second target is a `park` line, not a second contract.
- A tangent gets one `park` line, and the reply continues on the contract. The second tangent in a session stops the work and offers two choices: park it, or `fin swapped` and a new contract.
- Stop time is the OS's call. When the notification fires, or `now --hook` reports it passed, the next reply proposes `fin done|parked|swapped` and nothing else.
- No new rule, hook, or process file until the last contract's done-when moved. Process design is the favourite tangent. Park it.

## Stage exits

| Stage | Exits when |
|---|---|
| Target | `~/.now` has deliverable, done-when, stop |
| Spike | Time-boxed. Ends with one paragraph and one decision. "No decision" is a valid result; log it |
| Plan | A checklist of at most seven verifiable items, in the reply. Not a document |
| Implement | Checklist burns down. Each item ends at a verified boundary: test, screenshot, commit |
| Complete | Done-when is true. `fin done`. Commit at the boundary |
| Polish | Its own contract. Never inside the one that shipped |

## Do not

- Narrate the loop or restate these rules in replies. Tag drift `[DRIFT]` once and move on.
- Turn a plan into a file to maintain. Seven checkboxes in the reply are enough.
