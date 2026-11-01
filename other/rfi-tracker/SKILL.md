---
name: rfi-tracker
description: "Keeps one dated RFI log and reads what the log says that no single RFI does: every RFI with who owns it, when it arrived, when the contract required an answer, when the answer went, and how it was classified, plus the running counts that reveal a pattern — a sheet generating a stream of questions, a contractor sending already-answered ones, a consultant consistently late, a set of clarifications quietly accumulating into a change. Trigger on \"RFI log\", \"RFI tracker\", \"how many RFIs are open\", \"are we late on RFI responses\", \"which drawings are generating RFIs\", \"rfi-tracker\", or an RFI register handed over to keep. Carries no response periods and no classifications of its own; the contract sets the turnaround and each RFI's class comes from whoever answered it. It does not answer RFIs — `/draft-rfi-response` does — and does not replace the Architect of Record."
license: MIT
metadata:
  title: "RFI Tracker"
  summary: "Keep the RFI log, and watch the pattern the individual answers hide"
  discipline: "construction-admin"
  tags: "Tracking"
---

# RFI Tracker

Every RFI gets answered on its own and filed. The log is where the thing worth
knowing lives: that eleven of the last thirty came off one sheet, that the
average response is running past the contract period, or that six
clarifications have quietly become a change nobody priced.

## Scope and limits — read first

**What this does.** Keeps one dated log per project, and reads the aggregate.
Records each RFI with its owner, dates, classification and outcome, then reports
what is open, what is late, and the patterns that only appear in the counts.

**What this does not do.**

- **It carries no response period.** The contract sets it. Without it the log
  records elapsed time and cannot say anything is late.
- It does not classify. The classification comes from whoever answered the RFI,
  and `/draft-rfi-response` produces it. The log records what was decided, not a
  view of its own.
- It does not answer, draft, or send anything.
- It does not decide entitlement. Where a late response is recorded, that is a
  fact in the log and not a concession about delay.
- It does not track submittals or change orders. `submittal-log-builder` and
  `change-order-tracker` do.
- It does not replace the Architect of Record.

**What you need before starting.** The contract's response period, quoted. The
RFIs to date, with dates. Who owns responses on the design team and among the
consultants.

## Workflow

### Step 1. Establish the clock

Ask, in one message:

> 1. Quote the contract's RFI response period, and say what starts it: receipt,
>    logging, or something else. These differ and the difference is days.
> 2. Does the period differ for RFIs routed to a consultant?
> 3. Who owns responses, by discipline?
> 4. What is already logged, and in what form?
> 5. Is there an agreed format the contractor and the design team both use?

Without a quoted period the log still runs, but every lateness column reads
`period not established` rather than a number. Say so once rather than implying
punctuality.

### Step 2. Log each RFI

| # | Subject | Sheet or spec ref | Owner | Received | Due | Answered | Days | Class | Outcome |
|---|---|---|---|---|---|---|---|---|---|

`Class` uses whatever `/draft-rfi-response` assigned: already answered,
clarification, not our question, substitution or means, change.

`Outcome` records what followed: nothing, an ASI, a bulletin, a CCD, a
consultant's answer, or still open.

Multi-part RFIs are logged under the original number with letters. **Never
renumber**, and never log a three-part RFI as one row; the parts can have
different owners and different outcomes.

### Step 3. Log what happens to it after the answer

An RFI is not closed when it is answered. Record:

- Whether the answer produced an instrument, and its reference.
- Whether the contractor accepted the answer or came back.
- Whether the same question returned under a different number.

A question asked twice is a finding about the documents, not about the
contractor.

### Step 4. Read the aggregate

This is what the log is for. Report:

- **By sheet or spec section.** Which documents are generating questions. Three
  or more off one sheet is a signal about that sheet.
- **By class.** How many were already answered in the documents. A rising count
  says something about either the set or the contractor, and the log does not
  guess which.
- **By owner.** Average and worst response time per owner against the contract
  period. Consultants included.
- **Clarifications accumulating.** List clarifications on the same subject or
  the same area. Six clarifications about one condition is often a change that
  nobody priced because each one looked free.
- **Open and late.** Open by age, oldest first. Late by owner.
- **Rate.** RFIs per week, and whether it is rising.

### Step 5. Read back on request

At any point, and at every phase change: open items oldest first, late items by
owner, the sheet-level counts, and the accumulating clarifications.

Report elapsed time as a measurement. Never predict when something will be
answered.

### Step 6. Write the log

One dated file per project, appended to rather than rewritten. Ask where it
lives on the first run and use the same path after.

## Rules

- **Never supply a response period.** Quoted from the contract or not
  established.
- **Never classify an RFI.** Record the class somebody assigned.
- Never renumber, and log multi-part RFIs as separate rows under one number.
- A late response is a recorded fact, never a statement about entitlement.
- Report the accumulating-clarification pattern in every read-back.
- Elapsed time only. No predictions.
- Append; never rewrite an earlier entry.

## Anti-patterns

- Logging an RFI as closed when it was answered but produced no instrument that
  was ever issued.
- Averaging response times across owners so a slow consultant disappears.
- Recording a three-part RFI as one row.
- Treating a repeat question as a contractor problem without noting the document
  it came off.
- Predicting when an open RFI will be answered.
- Letting clarifications accumulate without reading them together.
- Starting the clock at logging when the contract starts it at receipt, or the
  reverse.

## Resources

None. This skill is one file. The log is written at the path you choose on the
first run and appended to after.
