---
name: fee-estimator
description: "Estimates a design fee four ways in parallel, as a percentage of construction cost, by area, as hourly against a cap, and as a lump sum, then splits the result by phase and by consultant and adds a reimbursables budget. Trigger on \"fee estimate\", \"what should I charge\", \"design fee\", \"percent of construction cost\", \"lump sum or hourly\", \"consultant fee split\", or a pasted program with a fee question. Works in any market. Every rate, percentage, phase split, consultant share, and any procurement cap comes from the user's own past projects, their contract, or the rule they name; the skill supplies the four methods and the comparison and never a benchmark figure from memory, since the published fee surveys are paywalled and cannot be quoted."
license: MIT
metadata:
  title: "Fee Estimator"
  summary: "Estimate a design fee four ways and split it by phase"
  discipline: "practice-contracts"
  tags: "Project Management, Pre-Design"
---

# Fee Estimator

Four methods, run side by side on the same project, so the spread between them
is visible. The arithmetic is the same everywhere. Every rate that goes into it
is yours.

## Scope and limits — read first

**What this does.** Takes your program and your rates, runs the four methods,
shows each calculation step by step, compares them, then splits the chosen
figure by phase and by consultant and adds reimbursables. Any method missing an
input comes out `not run` and is named, so a one-method answer never looks like
four.

**What this does not do.**

- **It does not know what anyone charges.** No percentage bands, no rates per
  area, no phase splits, no consultant shares, no multipliers. Every one comes
  from you. That is the design, not a gap.
- **It does not quote a fee survey.** The published compensation surveys are
  paywalled, and a figure recalled from one is both wrong and not yours to
  republish.
- **It does not know any procurement cap.** Where a public procurement rule caps
  a fee, you name the rule and the cap; the skill applies what you gave it and
  cites you.
- It does not price construction, and it does not validate your construction
  cost.
- It does not decide what to charge. It shows four figures and where they
  disagree, which is the useful part.

**What you need before starting.** The program, the construction cost, and your
own rates. Your last three similar projects are the best source; the skill will
ask for them.

## Workflow

### Step 1. Bootstrap if needed

```bash
python scripts/init_workspace.py
```

### Step 2. Establish the basis

Ask, in one message:

> 1. Project type, size, and construction cost, with what the cost is based on.
> 2. Delivery method and the services in scope. Basic services against
>    additional services changes every method below.
> 3. Is this governed by a procurement rule that caps or prescribes the fee? If
>    so, name the rule and its cap, and I will apply it and cite you for it.
> 4. Where do your rates come from? Past projects are best; give me two or three
>    comparable ones with their fee and cost, and I will derive the percentage
>    rather than assume one.
> 5. Which methods do you want run? Any I have no inputs for will be reported as
>    not run.

### Step 3. Collect the inputs, per method

Ask for each, and never substitute a typical value.

| Method | Needs |
|--------|-------|
| Percentage of construction cost | the percentage, and where it came from |
| By area | the rate per unit area, and the area basis |
| Hourly against a cap | staff rates by grade, hours by grade, the multiplier if you bill that way, and the cap |
| Lump sum | the build-up you are proposing, or the figure and its basis |

Then the splits, each of which is also yours:

- Phase split, as percentages that sum to a hundred, with the phases named.
- Consultant shares by discipline, and whether they come out of the total or sit
  alongside it. This distinction moves the number by more than most rate
  choices, so ask it explicitly.
- Reimbursables, as a percentage or a figure, and what it covers.

### Step 4. Run each method, showing the arithmetic

```
Method: percentage of construction cost
  construction cost        <as given>
  percentage               <as given>   [from: <your source>]
  fee                      <arithmetic>
```

Repeat per method. A method with a missing input prints `not run` and names what
it needs. Never carry a figure from one method into another as a substitute.

If a procurement cap was named, apply it last, show the comparison, and say
which figure governs.

### Step 5. Compare and split

Show the four figures together with their spread. A wide spread is information,
not an error, and the memo says which method you chose and why.

Then apply the phase split and the consultant shares to the chosen figure, and
show those arithmetic too.

### Step 6. Write the deliverable

Fill `assets/fee-estimate-template.md`. Head it with the project basis and the
source of every rate. Foot it with the methods not run.

### Step 7. Update the index

```bash
python scripts/append_to_index.py \
  --date <YYYY-MM-DD> \
  --project "<slug>" \
  --type "<project type>" \
  --sector "<sector>" \
  --cc "<construction cost>" \
  --pct "<percentage applied>" \
  --amount "<fee amount>" \
  --source "<slug>-fee.md"
```

Do not edit `docs/fees/index.md` by hand; the table alignment breaks.

### Step 8. Report

The four figures, the spread, the chosen method, the splits, the methods not
run, and:

> Every rate, percentage and cap here came from you, with its source beside it.
> I ran the arithmetic and supplied no figures. Methods marked not run had no
> inputs.

## Rules

- **Never supply a rate, a percentage, a split, or a multiplier.** Not from
  memory, not from a search, not from a figure in this file. There are none in
  this file.
- **Never quote a compensation survey.** They are paywalled, and a remembered
  figure from one is both unreliable and not yours to publish.
- **Derive from the user's own comparables where possible**, and show the
  derivation, so the number belongs to them.
- **Ask whether consultant fees are inside or alongside the total.** Getting
  that backwards changes the answer by more than any rate choice.
- **Show the arithmetic for every method**, and print `not run` rather than
  filling a gap.
- A procurement cap is applied only when the user names the rule and the cap.

## Anti-patterns

- Offering a percentage band because the project type is a familiar one. That
  band is exactly what the paywalled surveys sell, and a recalled version of it
  is a number with no provenance carrying your authority.
- Filling a phase split or a consultant share from convention.
- Applying a statutory or procurement cap the user did not name.
- Running one method and presenting it as the answer, with no note that three
  did not run.
- Rounding a construction cost or a derived fee to a neater figure.
- Bundling a rate table, a phase split, or a procurement cap into this skill
  later. It had all three, plus a script that applied them, and they were
  removed.

## Resources

- `assets/fee-estimate-template.md` — the deliverable structure.
- `assets/fee-index-template.md` — the project index structure.
- `scripts/init_workspace.py` — bootstrap `docs/fees/`.
- `scripts/append_to_index.py` — append a row to the index.

No reference files. The rates come from your projects and your contract.
