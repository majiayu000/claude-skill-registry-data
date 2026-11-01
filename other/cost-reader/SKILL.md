---
name: cost-reader
description: "Reads any document with money in it — an estimate, a budget, a cost plan, a supplier quote, a contractor's proposal, a client's own number — and does the part an architect can do without being an estimator: establish what it covers, what it excludes, what it assumed, and what date it is on. Those four decide almost every argument about a price, and none of them require checking the arithmetic. Trigger on \"read this estimate\", \"what does this quote actually include\", \"the budget came back\", \"is this number comparable\", \"cost-reader\", or any priced document handed over. Carries no rates, no benchmarks and no cost data; `/lookup-cost` quotes a benchmark with its source and `senior-cost-estimator` gives judgement. It checks no arithmetic, prices nothing, and does not replace the estimator, the contractor, or the Architect of Record."
license: MIT
metadata:
  title: "Cost Reader"
  summary: "Read any cost document for what it excludes and what it assumed"
  discipline: "construction-admin"
  tags: "Review, Analysis"
---

# Cost Reader

An architect cannot check an estimate and does not need to. Almost every
argument about a price is settled by four things that need no cost expertise at
all: what is in it, what is not, what it assumed, and when it was made.

The exclusions list is the most informative page in any priced document and it
is the one nobody reads.

## Scope and limits — read first

**What this does.** Reads any priced document for its coverage, its exclusions,
its assumptions and its date, and reports what would have to be true for it to
be comparable to another number.

**What this does not do.**

- **It carries no rates, benchmarks or cost data.** `/lookup-cost` quotes a
  benchmark with its source.
- **It checks no arithmetic and prices nothing.** Whether the quantities are
  right or the rates are reasonable is the estimator's, and
  `senior-cost-estimator` gives that judgement.
- It does not reconcile a budget against a design. `budget-reconciliation` does.
- It does not review a bid for award. `bid-review` does, and `/explain-bid`
  separates real cost from risk-shifting language.
- It does not replace the estimator, the contractor, or the Architect of Record.

**What you need before starting.** The document, complete, including its
exclusions, its qualifications and any covering note. What it is being compared
to, if anything. What the project actually is.

## Workflow

### Step 1. Establish what kind of number this is

Ask, or read off the document:

> 1. What is it: an estimate, a budget, a cost plan, a quote, a bid, a client's
>    own figure?
> 2. Who produced it, and are they selling something?
> 3. What date, and what date does it price to? Those differ.
> 4. What is it being compared against?
> 5. What stage of design was it priced from, and do you have that design?

A quote from somebody who wants the work, an estimate from a consultant paid to
be right, and a client's number from their board are three different documents
and they are routinely set side by side.

### Step 2. Read the exclusions before the total

Deliberately, and first. The exclusions list is where a document says what it
really is.

| Excluded | Who carries it then | Is it in the other number? |
|---|---|---|

Then look for the exclusions that are not on the list, because they are stated
as assumptions or buried in a qualification: access, working hours, sequence,
weather, escalation beyond a date, contaminated ground, existing conditions,
temporary works, attendance on other trades, testing, commissioning, and making
good.

**Anything excluded by one number and included by another makes the two
incomparable**, and that is usually the whole answer.

### Step 3. Find the assumptions

Priced documents assume things and say so in prose that nobody reads:

- What programme it assumes, and what happens if it changes.
- What design stage it was priced from, and whether the design has moved since.
- What access, hours and sequence.
- What is provided by others.
- What quantities came from: measured, taken off a drawing, or assumed.
- Whether escalation is included, to what date, and at what rate.
- What contingency is in it, and for what: design development, construction
  risk, or the estimator's own uncertainty. **Those three are different and are
  usually one line.**

### Step 4. Establish what date it lives on

Two dates matter and they are rarely the same:

- When it was produced.
- What date it prices to: today, tender, midpoint of construction, completion.

A number priced to today set against one priced to tender is an escalation
argument, not a design argument, and half of budget conversations are this.

### Step 5. Say what it would take to compare

Where a comparison is wanted:

| | Number A | Number B | Same basis? |
|---|---|---|---|
| Scope | | | |
| Exclusions | | | |
| Design stage | | | |
| Date priced to | | | |
| Contingency | | | |
| Escalation | | | |

Report the rows that do not match before reporting any difference in the
totals. **A difference in a total between two numbers on different bases is not
information.**

### Step 6. Report

- What kind of number it is and who produced it.
- The exclusions, and which of them somebody else now carries.
- The assumptions, and which have already changed.
- Both dates.
- What is in the contingency, or that it is not broken down.
- If comparing: the rows that do not match, before the totals.
- What to ask the person who produced it, as a short list.

Close by saying no arithmetic was checked and nothing was priced.

### Step 7. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Read the exclusions before the total.** Every run.
- **Never check the arithmetic and never supply a rate.**
- Establish both dates: produced, and priced to.
- Ask what the contingency is for, and say when it is one undifferentiated line.
- When comparing, report the basis mismatches before the totals.
- Ask what design stage it was priced from, and whether the design has moved.

## Anti-patterns

- Reading the total first.
- Comparing two numbers without checking they cover the same scope.
- Treating an exclusion list as boilerplate.
- Missing that one number includes escalation and the other does not.
- Reading a quote from an interested party as an estimate.
- Checking the maths.
- Accepting a single contingency line as an answer.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
