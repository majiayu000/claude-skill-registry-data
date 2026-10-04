---
name: autopilot-chaos
description: Takes the whole task and runs it end to end without stopping to ask, leaving the user to review at the finish line; invoke via /autopilot-chaos when you want a fully autonomous run and will inspect the result once it's done.
---

# Autopilot Chaos

Hands off the wheel. This mode takes the entire task and drives it from start to finish without pulling over to ask for directions. You review the whole thing at the destination — not at every intersection.

## When to use
- You want a fully autonomous run with no mid-task check-ins.
- You're fine reviewing everything at the end rather than approving each step.

## Behavior
1. Plan the full task up front, then execute the whole plan without stopping for confirmation on routine decisions.
2. Make reasonable default choices at every fork and keep moving.
3. Maintain a decision log of every meaningful choice so the end-of-run review is fast and complete.
4. Self-correct: when a step fails, diagnose and retry autonomously rather than halting to ask.
5. Only break autopilot for genuinely destructive or irreversible actions (data deletion, spending, prod writes) — pause for those.
6. Verify your own work along the way (run tests/builds) instead of assuming success.
7. Deliver a finish-line summary the user can scan and approve or correct in one pass.

## Output
A fully completed task plus a clear decision log and a finish-line summary, structured for a single end-of-run review.
