---
name: task-decomposition
description: Planning discipline for multi-step work — acceptance check first, read the terrain, dependency-ordered steps, de-risk the riskiest step early, re-plan on surprise. Use at the start of any task touching 3+ files or steps, for "implement", "build", "migrate" or "add feature" requests, and mid-task when a discovery invalidates the approach. Not for single-file edits with an obvious fix.
---

# Task Decomposition

Weak runs start editing in the first minute and discover the real shape of the task by breaking things. Strong runs spend the first 10–20% of the task front-loading understanding, commit to a sequence, and change the sequence the moment reality contradicts it.

## 1. Restate the goal as an acceptance check

One or two sentences plus the exact command or observation that proves it: "Done means `npm test -- export` passes and the CSV opens with headers." Run that check once now. Expected result: it fails or does not exist yet. If it already passes, the task is misunderstood; reread the request. If the request is genuinely ambiguous on a decision the user owns, ask ONE batched set of questions now, not a drip mid-task. Ambiguity you can resolve from the code is yours to resolve.

## 2. Read the terrain before planning the route

Before proposing steps:
- Read the project instructions (CLAUDE.md, AGENTS.md) for constraints that override defaults.
- Open every file you expect to edit, plus one caller or consumer of each. Blast radius is defined by callers, not by the file you were pointed at.
- Find the last similar change (`git log`, the newest analog in the tree) and plan to imitate it, not invent.

## 3. Write the step list, dependency-ordered

3–8 concrete steps, each independently verifiable, ordered so the build stays green as long as possible: types and schemas, then implementations, then call sites, then UI. For each step write the files touched and the command that verifies it. "Verify" without a command is not a step.

More than 8 steps means the task is two tasks; split it into phases and finish one before starting the next. Track the list visibly (todo list) for 3+ steps; mark exactly one step in progress at a time, and run its verification before marking it done.

## 4. Identify the risky step and de-risk it first

One step usually carries the real uncertainty: the unfamiliar API, the migration, the concurrency. Probe THAT step first with a spike, a dry run, or a one-file prototype, before investing in the safe steps. Discovering step 5 is impossible after finishing steps 1–4 is the expensive failure.

## 5. Re-plan on surprise, don't push through

When reality contradicts the plan (an API doesn't exist, a test reveals hidden coupling, a file is generated, a second attempt at the same step fails), STOP editing. Rewrite the plan explicitly: what changed, which steps die, which are added. Pushing the original plan through contradicting evidence produces half-finished hybrid states. If the surprise changes the scope the user asked for, surface it with options instead of silently redefining the task.

## 6. Keep a ledger on long tasks

For work spanning many steps or likely to hit context limits: maintain a short scratchpad file with goal, decisions made and why, steps done, steps remaining, current blockers. Update it at each milestone.

## Exit condition

The task is done when the step list is empty AND the acceptance check from step 1 passes, run again after the last edit and pasted into the report. Verified, not assumed.
