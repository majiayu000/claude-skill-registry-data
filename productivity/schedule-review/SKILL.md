---
name: schedule-review
description: "Reads a contractor's construction schedule from the design team's side rather than as a planner: finds every activity that depends on the architect, the consultants or the owner and checks whether the durations allowed match the contract, traces the critical path to see what actually controls the end date, looks for the logic that makes a delay claim inevitable, and separates what is a genuine concern from what is only unfamiliar. Trigger on \"review the contractor's schedule\", \"CPM schedule review\", \"is this baseline reasonable\", \"submittal durations in the schedule\", \"schedule update review\", \"schedule-review\", or a programme submitted for comment. Carries no durations, no productivity rates and no float conventions; the contract sets the review periods and the schedule specification sets the rules. It is not planning software, does not re-plan the work, does not opine on means and methods, and does not replace the scheduler or the Architect of Record."
license: MIT
metadata:
  title: "Schedule Review"
  summary: "Read a contractor's schedule for what it assumes about you"
  discipline: "construction-admin"
  tags: "Review"
---

# Schedule Review

A construction schedule is reviewed by the design team for the wrong thing. The
question is not whether the contractor can build it in that time. It is what the
schedule assumes about everybody else, because those assumptions become the
basis of a delay claim, and the schedule is the only place they are written
down.

## Scope and limits — read first

**What this does.** Reads the schedule for the design team's exposure: every
activity that depends on the architect, a consultant or the owner, and whether
the duration allowed matches what the contract gives. Traces what actually
controls the end date. Finds the logic patterns that make a claim inevitable.
Then separates real concerns from unfamiliarity.

**What this does not do.**

- **It carries no durations and no rates.** Review periods come from the
  contract. Activity durations are the contractor's. It has no view on how long
  anything should take to build.
- **It does not opine on means and methods.** Sequence, crew size, and how the
  work gets done are the contractor's responsibility, and commenting on them
  transfers it.
- It does not re-plan. It comments; the contractor replans.
- It is not planning software and does not recalculate a network. It reads what
  was submitted and asks about it.
- It does not resolve a delay claim. It reads the schedule that a claim would be
  built on, which is a different and much cheaper exercise.
- It does not replace the scheduler or the Architect of Record.

**What you need before starting.** The schedule, in a readable form, ideally
with the activity list, durations, logic and float. The specification section
governing scheduling. The contract's review and response periods. The submittal
log if there is one. Whether this is a baseline or an update, and against what.

## Workflow

### Step 1. Establish what you are reading and what governs it

Ask, in one message:

> 1. Baseline or update? If an update, against which baseline, and has the
>    baseline been accepted?
> 2. Quote the specification section on scheduling: what the contractor must
>    submit, in what form, and what acceptance means.
> 3. Quote the contract's review periods: submittals, RFIs, and anything else
>    with a stated turnaround.
> 4. What form is the schedule in, and do you have the logic or only the bars?
> 5. Has the contractor claimed any delay yet?
> 6. What is the contract completion date, and what does the schedule show?

A bar chart with no logic cannot be reviewed for most of what follows. Say so
plainly rather than reviewing what is visible and implying the rest was checked.

### Step 2. Find every activity that depends on your side

This is the core of the review. List them:

| Activity | Depends on | Duration allowed | Contract allows | Gap | On critical path? |
|---|---|---|---|---|---|

Cover submittal review, RFI response, shop drawing turnaround, mockup review and
approval, owner decisions and selections, owner-furnished items, permits and
inspections, and any design deliverable still outstanding.

**A review duration shorter than the contract gives is the single most
consequential finding in any schedule review.** It is also easy to miss, because
it sits in an activity duration field nobody reads. Report every one, with the
gap, whether or not it is on the critical path.

### Step 3. Trace what actually controls the end date

Follow the critical path from the completion date backwards and report it as a
chain in plain language. Then ask:

- Does the path run through activities the contractor controls, or through
  yours?
- How many parallel near-critical paths are there? A schedule with several is
  one where any small delay becomes critical.
- Where is the float, and does the specification say who owns it?
- Is the completion date driven by the work, or by a constraint somebody
  imposed on the network?

### Step 4. Look for the patterns that build a claim

Not accusations. Patterns worth a question:

- Activities with no predecessor or no successor, floating free.
- Constraints that fix a date rather than letting logic drive it, especially
  ones on your activities.
- Negative float in a baseline.
- Durations that changed between updates without a stated reason.
- Logic that changed between updates, which moves the critical path without
  anybody deciding to.
- Long activities with no interim milestones, which cannot be measured until
  they are late.
- Out-of-sequence progress in an update.
- A completion date earlier than the contract's, which turns any delay into a
  claim for time the contract never promised.

For each found, ask the question rather than stating the conclusion.

### Step 5. Sort findings into three

| Finding | Kind | Why |
|---|---|---|

- **Comment.** Something to raise in the response.
- **Watch.** Not a comment now; something to track through updates.
- **Unfamiliar, not wrong.** The contractor's approach differs from what you
  expected and that is their prerogative.

The third category matters. A review that comments on everything unfamiliar
trains the contractor to ignore the review.

### Step 6. Report

- Every dependency on your side, with the gap against the contract, shortfalls
  first.
- The critical path in plain language, and who controls it.
- The patterns found, as questions.
- The three counts.
- What could not be reviewed, and why, listed plainly.

Close with the standing limits: no view was taken on means, methods or build
durations; acceptance of a schedule is what the specification says it is and is
not agreement to its assumptions.

### Step 7. Save, if asked

Ask whether to write the review to a file and where.

## Rules

- **Never supply a duration, a rate, or a float convention.**
- **Never comment on means and methods**, including sequence and crew loading.
- Report every review duration shorter than the contract allows, on or off the
  critical path.
- State plainly what could not be reviewed for want of logic or data.
- Raise patterns as questions, never as accusations.
- Say on every run that acceptance is not agreement to the schedule's
  assumptions.

## Anti-patterns

- Reviewing whether the contractor can build it in the time. Not your question,
  and answering it takes on their risk.
- Missing a submittal review duration because the activity was not on the
  critical path.
- Accepting a completion date earlier than the contract's without comment.
- Commenting on a sequence because it is not how you would do it.
- Reviewing a bar chart as though the logic had been checked.
- Treating an update as reviewed when the logic changed and nobody said why.
- Re-planning the work inside the review.
- Ignoring float ownership because the specification is silent. Silence is the
  finding.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
