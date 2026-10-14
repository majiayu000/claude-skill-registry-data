---
name: plan-mode-verify
description: Verify a planned outcome with direct evidence. Use when the user asks whether work is done, requests a verification pass, or needs proof that implementation meets acceptance criteria.
license: MIT
---

# Verify

Test the claim the user cares about. A green command is evidence only for the behavior that command actually exercises.

1. Restate the goal and enumerate its acceptance criteria. Include constraints that could be violated by an otherwise working result. If criteria were never written, derive them from the request and label the interpretation.
2. For each criterion, choose a check that could expose failure. Inspect the artifact and use a running integration or user interaction when the claim is about runtime behavior. Use static checks for structural claims; avoid redundant broad tests.
3. Run the checks and keep receipts: command or interaction, environment, observed result, and relevant file or log location. Distinguish direct observation from an agent report or inference.
4. Mark each criterion **passed**, **failed**, **blocked**, or **unverified**. A blocked check lacks a needed dependency; an unverified check was not run. Neither counts as passed.
5. Return a concise verdict with the evidence and remaining gaps. For a failure, give a reproducible symptom and the next useful action; invoke **plan-mode-reroute** if the accepted route can no longer reach the goal.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
