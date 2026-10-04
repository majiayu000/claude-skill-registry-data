---
name: ownership
description: |-
  Autonomous build-ship-verify loop that ends with code committed, deployed, and confirmed live.
  Triggers on: "$ownership", "execute X with ownership", "build this overnight", or any request
  for an autonomous product loop with no human checkpoints until production is verified.
  NOT for: one-off tasks, quick fixes, or supervised dev work (use devprocess for those).
---

# $ownership — Product Ownership Loop

## When to Use
- You say "$ownership" or "execute X with ownership"
- You're asked to build a new project or feature overnight/autonomously
- If asked to build something without mentioning $ownership, ask: "Do you want me to do this with $ownership?"

## What This Solves
Without $ownership, work gets built in sandboxes and never ships. $ownership ensures every iteration cycle ends with code in the repo, deployed, and verified live on production.

## Setup Phase (run once when $ownership starts)

1. Confirm the project basics:
   - Repo location (local path + GitHub remote)
   - Deploy target (Render service URL, deploy hook, or other)
   - Dev server command (e.g. npm run dev)
   - Test command (e.g. npm test)
   - Spec/plan file location (e.g. SPEC.md, PLAN.md)

2. Ask: "How should I run the loop?"

   Option A - Self-waking loop (agent stays in control)
   - Run iterations continuously in the main session
   - After each iteration, fire a wake event to continue
   - Each turn: check messages -> reflect -> build -> ship -> verify -> log -> wake again
   - Best when: you want the agent personally doing the work with full context
   - Set a stop condition (time limit or "until I say stop")

   Option B - Cron loop (autonomous, isolated sessions)
   - Set up a cron at a chosen interval (e.g. every 30m, 1h, 2h)
   - Each run is an isolated session that reads project files, does one iteration, ships it
   - Best when: overnight/unattended work
   - Set a stop cron to auto-disable after N hours

3. Store project config in <project>/OWNERSHIP.md

## Iteration Cycle

Each iteration is a full product owner cycle, not a status check.

### Step 0: Check Messages
Before anything else - check for new messages from the owner. Did they send feedback? Changed priorities? Said stop? Adjust your plan BEFORE continuing. This is non-negotiable.

### Step 1: Assess Current State
- cd <project> && git status && git log --oneline -5
- Read SPEC.md / PLAN.md - what's the vision?
- Read the PREVIOUS iteration's reflection files

### Step 2: Reflect (7 Lenses)
Create iterations/<YYYY-MM-DD-HHMM>/ and write 7 reflection files:
1. security.md - Auth holes, exposed endpoints, leaked secrets, XSS
2. privacy.md - PII exposure, data retention, unnecessary data collection
3. design.md - Visual consistency, styleguide adherence
4. ux.md - Smooth flows, accessibility, mobile responsiveness
5. product.md - Feature gaps, ICP fit, weak areas
6. marketing.md - Does the website reflect current capabilities?
7. product-marketing.md - Right features promoted? Content gaps?

### Step 3: Prioritize
Pick the MOST IMPACTFUL thing to build/fix this iteration. One focused task.

### Step 4: Build
Use coding agents for substantial work. Follow $devprocess.

### Step 5: Verify Locally
Run tests + manually test in browser.

### Step 6: Deploy to Production (MANDATORY)
Commit, push, trigger deploy. Wait for completion. Every iteration MUST end with code deployed.

### Step 7: Verify Live on Production (MANDATORY)
Open browser, test on production. If broken: fix, push, redeploy.

### Step 8: Log
Append to iteration-log.md with timestamp, what was built, what's next.

## Rules
1. Every iteration MUST end with code pushed and deployed to production
2. Never report "work done" if it's only local
3. Always check messages first (Step 0)
4. Read the spec every iteration
5. Use the app yourself - click through it like a user
6. The 7 reflection files are mandatory
7. Carry forward deferred items from previous iterations
8. Commit often, push always
9. If stuck for more than 15 minutes, move on
10. The iteration log is your memory
