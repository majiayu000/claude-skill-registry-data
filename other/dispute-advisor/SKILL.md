---
name: dispute-advisor
description: "Locates a live construction dispute on the escalation ladder of the contract in force, names the next required step, the notice deadline that governs it, and the point at which counsel should be engaged. Trigger on \"dispute advice\", \"claim escalation\", \"is this a claim\", \"notice of claim\", \"time extension request\", \"mediation or arbitration\", \"termination notice\", or a pasted change order rejection, delay narrative, or RFI thread that has turned contested. Works with any standard form or bespoke contract. The user supplies the contract and its clauses; the skill reads what it is given and never recalls a notice period, a ladder step, or a procedure from memory. Procedural only: it produces an escalation memo and a notice letter draft, and it is not legal advice."
license: MIT
metadata:
  title: "Dispute Advisor"
  summary: "Find the next required step and notice deadline in a dispute"
  discipline: "practice-contracts"
  tags: "Construction Admin, Project Management"
---

# Dispute Advisor

Where are you on the ladder, what step comes next, and what deadline is running.
Those three questions have the same shape in every contract. The steps and the
periods are written in yours, so they come from yours.

## Scope and limits — read first

**What this does.** Reads the contract text you supply, places the dispute on
its escalation sequence, names the next required step and the clause that
requires it, computes the deadline from the date you give and the period the
clause states, and drafts the memo and the notice letter. Anything it could not
find in your text is reported as a gap, counted, and never filled in.

**What this does not do.**

- **It does not know your contract.** It has no clause text, no notice periods,
  no ladder, and no form-specific procedure. Every one comes from the document
  you give it. That is the design, not a gap.
- **It is not legal advice**, and it does not say whether a claim will succeed.
  It says what the contract requires next and when.
- It does not decide entitlement, quantum, or causation.
- It does not cite case law, statutes, or regulations. Where the answer turns on
  law rather than on the contract, it says so and stops.
- It does not send anything. The notice letter is a draft for you and counsel.

**What you need before starting.** The contract, or at least its dispute and
notice articles, the dates, and the correspondence so far.

## Workflow

### Step 1. Bootstrap if needed

```bash
python scripts/init_disputes_workspace.py
```

Confirm before creating `docs/` in a project that does not have one.

### Step 2. Anchor the contract

Ask, in one message:

> 1. Which contract governs, in what form and what year, and has it been
>    modified? Amendments to the dispute articles are common and change
>    everything downstream.
> 2. Paste the dispute and notice articles, or name a file I should read. I work
>    only from the text you give me.
> 3. Who do you act for, and against whom?
> 4. The dates: when the event occurred, when it was discovered, and when each
>    piece of correspondence went out.
> 5. Is counsel already engaged?

If no clause text arrives, stop after Step 3 with the ladder blank. A ladder
drawn from memory would produce a deadline, and a wrong deadline is the most
damaging output available here.

### Step 3. Build the ladder from the text

Read what was supplied and write out the sequence it actually sets: what must
happen, in what order, who decides at each stage, and what moves it to the next.
Quote the clause for each step.

Mark each step `found`, with its clause, or `not in supplied text`. Never fill a
missing step from what contracts of that family usually do, and never present
the sequence as a published or standard numbering.

### Step 4. Place the dispute and compute the deadline

Say which step it sits at and why. Then for the next step:

```
Clause, as supplied      <quoted>
Period it states         <as written>
Runs from                <the event the clause names>
Date of that event       <as you gave it>
Deadline                 <arithmetic, shown>
Days remaining           <arithmetic, shown>
```

Use the kind of day the clause uses, and say which. If the clause is silent on
what the period runs from, that is a gap, not something to infer.

If a deadline has already passed, say so plainly. Never paper over a missed
notice, and never extend one on the user's behalf.

### Step 5. Counsel threshold

Read `references/counsel_engagement_triggers.md` and say which triggers this
dispute meets. That file is a checklist of situations, not legal advice and not
a threshold from any particular contract.

Where the answer turns on law rather than the contract, say so and stop there.

### Step 6. Write the memo and the notice

Fill `assets/dispute_memo_template.md`: the contract and its form at the head,
the ladder with a clause beside every step, the deadline arithmetic, the gap
list, and the counsel triggers met.

If a notice is due, draft it from `assets/notice_letter_template.md`, quoting the
clause that requires it. Say on the draft that nothing has been sent and that
counsel should see it first.

### Step 7. Report

Current step, next step, deadline and days remaining, gap list, and:

> Every step and every period here was read out of the contract text you
> supplied. I supplied none of them, and I have not given legal advice. Gaps are
> steps I could not find in what you gave me, not steps that do not exist.

## Rules

- **Never supply a notice period, a ladder step, or a procedure.** Not from
  memory, not from a search, not from what a form usually says. There are none
  in this file.
- **Show the deadline arithmetic**, including which kind of day the clause
  counts.
- **A missing clause is a gap**, never an inference from the contract family.
- **Never cite case law, a statute, or a regulation.** Name the question and
  hand it to counsel.
- **Never extend or soften a missed deadline.** Name it plainly in the memo.
- **Never send anything.** Drafts say so on their face.
- Where the contract is modified, work from the modification and say you are.

## Anti-patterns

- Stating a notice period because it is the familiar one for that form. Those
  are exactly the periods amended in the front-end documents and never noticed.
- Filling in a ladder step the supplied text does not contain.
- Counting calendar days where the clause says working days, or the reverse.
- Advising whether a claim will succeed.
- Presenting the ladder numbering as an industry standard. It is a reading of
  the text you supplied.
- Producing a memo with no gap list, so a partial read looks complete.
- Bundling a contract quick reference or a notice timing matrix into this skill
  later. It had both, transcribed from one family of forms, and they were
  removed.

## Resources

- `references/counsel_engagement_triggers.md` — situations that warrant counsel.
  A checklist, not advice and not a contract threshold.
- `assets/dispute_memo_template.md` — the memo structure.
- `assets/notice_letter_template.md` — the notice draft, marked for counsel.
- `scripts/init_disputes_workspace.py` — bootstrap `docs/disputes/`.

No contract references. The clauses come from your contract.
