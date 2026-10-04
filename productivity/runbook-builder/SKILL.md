---
name: runbook-builder
description: Turn a workflow that lives in your head into a runbook anyone can execute. Capture the 5W2H of a repeated process, who, what, when, where, why, how, and how much, name the failure points, and add the checks that prove each step worked, so the task no longer depends on you being available. Trigger on "write a runbook for this", "document this process", "make this an SOP", "turn this into steps", "how do we run X", or any workflow you have now done enough times to hand off.
---

# Runbook Builder

## What this does
Takes a process you run from memory and turns it into a runbook someone else can execute without you. It captures the full 5W2H, who does it, what they do, when it runs, where it happens, why it matters, how each step is performed, and how much it costs in time or money, then it marks where it usually breaks and the check that confirms each step actually worked. The test of a runbook is simple: could a capable person you have never met run this correctly? This builds to that bar.

## What you'll need
You do not need to connect anything to get value today. Walk the skill through the process and it drafts the runbook. Connect the tools below and it grounds the steps in the real tools and stores the finished SOP where the team runs it.

- Works today with: your description of the process, or a rough list of steps. It structures it into a full runbook.
- More powerful connected to a repo or notes tool: the runbook is stored where the team already looks, versioned and linkable.
- Sharper with a task tool: recurring runs become a checklist that can be assigned and tracked.
- Sharper with a knowledge base: the runbook cross-links to the facts and stakeholders it depends on.

## How this runs at your connection level
This skill is never reliant on a connector. It builds from your walkthrough and gets more grounded as you connect the tools the process touches. It never stores the runbook anywhere without approval.

- **Bring your data**: describe the process once. The skill produces the full 5W2H runbook today. No connection required.
- **Connect your tools**: it names the real systems each step uses and saves the runbook where the team runs it, once you approve.
- **Just exploring**: no process to capture yet? Get the runbook template and a worked example, so you can see the shape before you fill it.

Every run ends with the one step most likely to fail in someone else's hands, so you can harden it first.

## Customize this for yourself
This was built for an operator ready to hand a repeated task off. Set these to your setup:

| Set this | What it is | Default / Example |
|---|---|---|
| RB_HOME | where runbooks live | a git repo, /runbooks; a notes tool |
| ROLE | who runs it | a role, not a person's name |
| TRIGGER | what starts the run | a schedule, an event, a request |
| TOOLS | the systems a step touches | your CRM, a sheet, a task tool |
| CHECK_STYLE | how a step is verified | a visible output, a count, a confirmation |
| COST_UNIT | how "how much" is measured | minutes, API calls, dollars |

The 5W2H frame is fixed. What each W points at is yours.

## The method

### 5W2H capture
Every runbook answers seven questions. **Who** runs it (a role, never a single person, so it survives turnover). **What** the outcome is. **When** it triggers. **Where** it happens (which systems). **Why** it matters (so a runner knows when to stop if the reason is gone). **How**, the numbered steps. **How much**, the time or cost per run. Skip one and the runbook has a hole a stranger will fall into.

### Steps a stranger can follow
Each step is an action with an object: "export the signup list from the sheet," not "get the data." No step assumes context only you have. Where a step needs a fact, it links to it rather than assuming the reader knows.

### Failure points, named
For each step that tends to break, say so, and say what breaking looks like. "The sheet read times out on runs over 5k rows" is a failure point. Naming it turns a mystery outage into an expected, handled case.

### Checks that prove it worked
Every step that matters ends with a check: the visible output, the row count, the confirmation message that says it succeeded. A runbook without checks is a wish list. A runner should never have to guess whether a step landed.

### Roles, not names
The runbook names a role, not a person. When the person changes, the runbook still runs. Personal contact details live in the knowledge base and are linked, not hard-coded into the steps.

## Quality gates
- Nothing is saved or published without your explicit approval. The skill drafts the runbook and shows it; you decide where it lands.
- No step without a check. If a step cannot be verified, that is called out as a risk, not left silent.
- Failure points are named, not hidden. A known break that is undocumented is a trap for the next runner.
- Roles, not names. A runbook that depends on one person by name is flagged to be generalized.

## Output (example)
```
RUNBOOK · Nightly signup enrichment + routing · v1 (draft)

WHO      the RevOps on-call role (not a named person)
WHAT     enrich each new signup and route it to an owner
WHEN     nightly, 2am, after the raw signups sync lands
WHERE    the signups sheet -> the enrichment tool -> the CRM
WHY      the AE team works this list first thing; stale = missed speed-to-lead
HOW MUCH ~8 min unattended; ~1,200 API calls/run

HOW (steps)
  1. Confirm the raw sync landed.   CHECK: row count > 0 in "signups-raw"
  2. Run enrichment on new rows.    CHECK: email fill rate reported
  3. Route by company-size band.    CHECK: every row has an owner
  4. Post the run summary.          CHECK: summary message in the channel

FAILURE POINTS
  - Step 2 times out over ~5k rows. If so, batch in chunks of 2k.
  - Step 3 leaves EU signups unrouted (no owner rule yet). Flag, do not drop.

(draft, not saved. approve to store in the runbooks home)
```

## Where the inputs come from
COST_UNIT and CHECK_STYLE are defaults, not laws. Some processes are measured in minutes, some in dollars, some in API calls; some checks are a row count, some a human confirmation. The 5W2H frame is the standard because each question is one a stranger will ask mid-run. Change how you measure. Keep every question answered.

## Example chat

**You:** I do the nightly signup enrichment and routing by hand every night. Turn it into a runbook someone else could run.

**Claude:** Walked through it and built the full 5W2H. One gap needs your input before this is handoff-ready.
```
RUNBOOK · Nightly signup enrichment + routing · v1 (draft)
WHO      the RevOps on-call role (not a named person)
WHEN     nightly, 2am, after the raw signups sync lands

HOW (steps)
  1. Confirm the raw sync landed.   CHECK: row count > 0 in "signups-raw"
  2. Run enrichment on new rows.    CHECK: email fill rate reported

FAILURE POINTS
  - Step 2 times out over ~5k rows. If so, batch in chunks of 2k.
  - Step 3 leaves EU signups unrouted (no owner rule yet). Flag, do not drop.

(draft, not saved. approve to store in the runbooks home)
```
Worth flagging: I wrote WHO as "the RevOps on-call role," not your name, on purpose. A runbook that depends on one person by name breaks the first time that person is out.

**You:** What happens with the EU signups that don't have an owner rule yet?

**Claude:** Right now that's a named failure point, not a hidden one. Step 3 flags them instead of silently dropping them, so whoever runs it knows to route those manually until you set the rule. Sharpener: connect your task tool and this becomes a checklist someone can actually claim and get credit for running, not just a doc they read.

## Go further
The draft proves the process can leave your head. Here is the version that survives without you.

- **Store it where the on-call role already looks.** Push the approved runbook into your team's git repo or notes tool so it's linked, versioned, and findable at 2am.
- **Turn recurring runs into assigned checklists.** Connect a task tool so each nightly run creates a trackable checklist instead of a static doc nobody checks off.
- **Alert on the named failure points automatically.** Wire step 2's row-count check to Slack so a timeout gets flagged the moment it happens, not the next morning.

The next person who runs this doesn't need to call you to find out what step 3 means.

## Make it yours
Fork it. Add a rollback section, an escalation path, a "last run" log. Cut what your process does not need. The point is a runbook that lets you hand the task off and trust it runs without you. Built by an operator. Customize it, break it, make it better.
