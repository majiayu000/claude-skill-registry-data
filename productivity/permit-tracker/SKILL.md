---
name: permit-tracker
description: "Keeps one dated log of every approval a project has to obtain, from the agencies you name rather than from an assumed list: what each permit is, which agency issues it, what it depends on, who owns it, what has been submitted and when, every comment received and its response, and every expiry. Reads back what is on the critical path and what is waiting on somebody. Trigger on \"permit tracker\", \"track the approvals\", \"what permits do we need\", \"permit log\", \"who owns this approval\", \"when does the permit expire\", \"permit-tracker\", or a list of agencies named with a request to keep track of them. Carries no agency lists, no review durations, no fee schedules and no permit types; every one comes from the jurisdiction, because they differ between adjacent municipalities and change without notice. It does not file anything, does not predict a duration, and does not replace the expediter, the code consultant, or the Architect of Record."
license: MIT
metadata:
  title: "Permit Tracker"
  summary: "Keep one dated record of every permit, review and inspection a project needs"
  discipline: "code-life-safety"
  tags: "Tracking"
---

# Permit Tracker

Permits are lost to two things: an approval nobody knew was required, and a
dependency nobody drew. Both are invisible until the day the schedule needs the
permit that needs the other permit that was never applied for.

## Scope and limits — read first

**What this does.** Keeps one dated log for one project. Records every approval
required, the agency that issues it, what it depends on and what depends on it,
who owns it, and every submission, comment, response and expiry against it.
Reads back the dependency chain and what is blocked.

**What this does not do.**

- **It carries no list of permits and no agency list.** What a project needs
  differs between adjacent municipalities and changes. The list comes from your
  jurisdiction, your expediter, or your own research, and the log records what
  you found and where you found it.
- **It predicts no durations.** A review time from a previous project, a
  published target, or an agency's own estimate can all be recorded as what
  somebody said, with who and when. None of them is a forecast, and the log will
  not turn one into one.
- It records no fees from memory.
- It does not file, submit, or communicate with anyone.
- It does not write the comment responses. `plan-check-response-builder` does
  that, and this records that it happened.
- It does not decide whether an approval is required. It records the question,
  who was asked, what they said and when. An unanswered question stays logged as
  open rather than resolving into "probably not".
- It does not replace the expediter, the code consultant, or the Architect of
  Record.

**What you need before starting.** The jurisdiction and every agency with a say,
including the ones that are not the building department. The project phase. Who
on the team owns approvals. Anything already submitted.

## Workflow

### Step 1. Build the list from the jurisdiction, not from memory

Ask, in one message:

> 1. What jurisdiction, and which agencies have a say? Name each. Building
>    department, fire, health, zoning or planning, public works, utilities,
>    transportation, environmental, historic, a design review body, a landlord
>    or campus authority, an owner's insurer.
> 2. Where did that list come from: an expediter, a pre-application meeting, a
>    published checklist, or an assumption?
> 3. What phase is the project in, and what is the target for each milestone?
> 4. Who owns approvals on the team, and is there an expediter?
> 5. What has already been submitted or obtained?

If the list came from an assumption, log it as such. That distinction is the
single most useful thing in the log for the first six months.

### Step 2. Log each approval with what it depends on

| # | Approval | Agency | Depends on | Blocks | Owner | Status | Date | Source of requirement |
|---|---|---|---|---|---|---|---|---|

Status is one of: `not confirmed required`, `required`, `in preparation`,
`submitted`, `in review`, `comments received`, `resubmitted`, `issued`,
`expired`, `not required — confirmed by`. The last one carries who confirmed it
and when, or it is not that status.

**Dependencies are the point of this log.** A zoning approval that has to
precede a building permit, a utility release that gates an occupancy
certificate, a fire department sign-off that needs an inspection that needs
work that needs the permit: draw these as the `depends on` and `blocks` columns
and the chain becomes visible.

Every approval has exactly one owner. **Two owners means none**, and it gets
flagged rather than logged as covered.

### Step 3. Log every submission, comment and response

Dated entries against an approval:

- **Submission.** What was submitted, when, by whom, under what reference.
- **Comment.** What came back, when, from which reviewer, and the reference.
  Record the comment count and whether responses are due by a date.
- **Response.** When it went back and what changed. Point at the response
  document rather than restating it.
- **Meeting or call.** Who said what, when. An agency position given verbally is
  worth recording and worth flagging as verbal.
- **Issue.** The permit reference, the issue date, and the expiry.

### Step 4. Log every expiry and every condition

Permits expire, and permits carry conditions that have to be discharged before
something else can happen. Both get their own entries:

- Expiry date, what restarts the clock, and what happens if it passes.
- Each condition attached to an issued permit, what discharges it, who owns it,
  and whether it gates occupancy.

A condition attached to an issued permit is not an issued permit. Log the
conditions separately or they are found at occupancy.

### Step 5. Read back the chain

On request, and at every phase change:

- Approvals by status, with `not confirmed required` and `no owner` first.
- The dependency chain for anything on the critical path, drawn as a list of
  what has to happen in order.
- Anything waiting on an agency, with how long it has been waiting, stated as an
  elapsed time and never as a prediction of how much longer.
- Anything waiting on the team.
- Expiries approaching, and undischarged conditions.
- Every requirement still sourced from an assumption rather than from an agency.

### Step 6. Write the log

One dated file per project, appended to rather than rewritten. Ask where it
lives on the first run and use the same path after. Every entry carries a date
and a source.

## Rules

- **Never supply a permit list, an agency list, a duration, or a fee.**
- Every requirement records where it came from, and an assumption is logged as
  an assumption.
- `not required` is only a status when it carries who confirmed it and when.
- Every approval has exactly one owner, or is flagged as having none.
- Elapsed time is a measurement. Remaining time is a prediction, and predictions
  are only ever recorded as what a named person said on a date.
- Conditions on an issued permit are logged separately from the permit.
- Append; never rewrite an earlier entry.

## Anti-patterns

- Starting from a generic permit list rather than from the jurisdiction.
- Predicting a review duration from a previous project.
- Logging an approval as not required because nobody has raised it.
- Recording an issued permit and not its conditions.
- Letting a verbal agency position into the log without being marked verbal.
- Tracking approvals as a flat list with no dependencies, which hides the chain
  that actually controls the schedule.
- Rewriting history when a requirement changes.

## Resources

None. This skill is one file. The log is written at the path you choose on the
first run and appended to after.
