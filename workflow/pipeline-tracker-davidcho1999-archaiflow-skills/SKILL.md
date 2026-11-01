---
name: pipeline-tracker
description: "Keeps one dated record of every pursuit the practice is chasing, from the first mention of a project — a call, a rumor, a client hint — through qualification, the go decision, the proposal, and the outcome, with the effort each pursuit consumed and the reason each loss happened. Leads every read-back with the pursuits consuming effort that have no go decision on record, because chasing without deciding is where business development money quietly goes. Trigger on \"pipeline tracker\", \"what are we chasing\", \"track our pursuits\", \"proposals out right now\", \"did we ever hear back on that RFP\", \"what is our win rate\", \"pipeline-tracker\", or a pile of pursuit emails handed over to make sense of. Carries no win-rate benchmarks, no hit-rate targets, and no probability weightings; the practice's history is the only pattern it reports."
license: MIT
metadata:
  title: "Pipeline Tracker"
  summary: "Track every pursuit from first whisper to won or lost, and what each cost"
  discipline: "practice-contracts"
  tags: "Tracking"
---

# Pipeline Tracker

A practice always knows which proposals are due this week. What it loses track
of is everything else: the lead somebody heard in March, the RFP that was
never answered either way, the pursuit three people are quietly working on
that nobody decided to chase. The log starts at the first mention, because
that is when the spending starts.

## Scope and limits — read first

**What this does.** Records every pursuit from the earliest moment it exists
— a rumor is an entry — through qualification, the go decision, submission,
and the outcome. Keeps the dates, the effort consumed, the go decision with a
name on it, and the reason for every loss. Reads the pipeline back with the
undecided-but-consuming pursuits first, deadlines second, and the history as
recorded fact.

**What this does not do.**

- **It carries no benchmarks and no probabilities.** What a healthy win rate
  is, what a pursuit should cost, and how likely a shortlist is to convert
  are not in here. Your own recorded history is the only pattern it reports.
- **It never forecasts.** No weighted pipeline, no expected revenue, no
  "likely wins". Where the practice wants a projection, it is a named
  person's estimate, recorded as such with a date.
- It does not make the go decision. `go-no-go-review` scores a pursuit; this
  log records that the decision happened, when, and who made it — or that it
  never did, which is the more common finding.
- It does not write anything. `rfp-response-builder`, `draft-proposal`, and
  `sf330-builder` produce the documents; `fee-estimator` prices the work.
- It is not a CRM and does not replace one. If the practice has one, this
  reads what it exports; the log's job is the honesty, not the plumbing.

**What you need before starting.** Whatever exists: the proposals currently
out, the RFPs sitting unanswered, the leads people are carrying around in
their heads. The log absorbs a messy start; the only wrong input is leaving a
pursuit out because it is not official yet.

## Workflow

### Step 1. Establish the pipeline as it stands

Ask, in one message:

> 1. Every pursuit anyone is spending time on, official or not: the client,
>    the project, and how you first heard of it.
> 2. For each: where does it stand? Just heard / deciding whether to chase /
>    decided go / proposal in progress / submitted / interview / waiting /
>    won / lost / went quiet.
> 3. Which have a go or no-go decision actually on record, made by a named
>    person on a date? "We sort of drifted into it" is an answer, and it gets
>    logged as no decision.
> 4. The dates you have: first heard, RFP issued, due, decision expected.
> 5. Is pursuit effort tracked anywhere — hours, or even a rough sense of who
>    is spending time on what?
> 6. Where should the log live? One dated file; same path every run after.

### Step 2. Record each pursuit from its earliest moment

One entry per pursuit, appended, never rewritten:

| Pursuit | Client | First heard | Source | Stage | Go decision | By, date | Due | Effort so far |
|---|---|---|---|---|---|---|---|---|

The rules that make it a method:

- **The entry starts at the first mention**, not at the RFP. The cost of a
  pursuit starts accruing at the coffee where somebody said "you should go
  for this", and a log that starts at the RFP hides the qualifying spend.
- **A stage change is a new dated line, never an edit.** The history of a
  pursuit — how long it sat at each stage — is the data; overwriting it
  keeps the conclusion and deletes the evidence.
- **"No go decision" is a recorded state**, not a blank cell. It is the
  single most important thing this log makes visible.

### Step 3. Record every outcome with its reason

Won, lost, dropped, or went quiet — every pursuit ends, and the ending gets a
line:

| Pursuit | Outcome | Date | Reason | Reason's source | Effort total |
|---|---|---|---|---|---|

The reason's source matters as much as the reason: a client debrief is a
fact, "we think it was fee" is a guess, and the log marks which is which.
For losses, ask the two questions worth recording: was it ever winnable —
was the job wired for someone else before the RFP went out — and what did
the debrief actually say, if anyone asked for one. If nobody asked, log
that; the unasked debrief is a habit the log can surface.

**Went quiet is an outcome that is not final.** Record the elapsed time since
the last movement and the last thing that happened. Never declare a quiet
pursuit dead; report how long it has been quiet and let the practice decide
when to ask or let go.

### Step 4. Read back

At whatever rhythm the practice sets, in this order:

- **Consuming effort, no go decision on record.** First, every time. Each
  one with its effort so far and its elapsed time. These are the pursuits
  where the money is going while nobody has decided it should. Point at
  `go-no-go-review` for each.
- **Deadlines**, nearest first, with what remains to be done against each.
- **Waiting**, by elapsed time since last movement, longest first.
- **The recorded history**: won and lost, with reasons, as counts of what
  actually happened. By source, by client type, by whatever cut the practice
  asks for — presented as history, never as a predictor.
- **Effort against outcomes**: what pursuits are costing, in whatever unit
  the practice tracks, including the ones that ended in nothing.

Report elapsed time everywhere and predict nowhere.

### Step 5. Write the log

One dated file for the whole pipeline, appended to rather than rewritten. Ask
where it lives on the first run and use the same path after. At year end, the
outcome reasons and the effort totals are the input to `lessons-learned` and
to the next year's go-no-go discipline.

## Rules

- **Log from the first mention, never from the RFP.**
- **Append; never rewrite an earlier line.** A stage change is a new dated
  entry.
- "No go decision" is a recorded state and leads every read-back.
- Every outcome records a reason, and every reason records its source:
  debrief, or guess, attributed.
- Never supply a benchmark, a target, or a probability.
- Never forecast. A projection is a named person's estimate with a date.
- A quiet pursuit gets elapsed time, not a verdict.
- Effort spent on lost and dropped pursuits is reported, not buried; it is
  the number that improves the next go decision.

## Anti-patterns

- Starting the log at the RFP and losing the qualifying spend.
- A weighted pipeline. Multiplying a fee by a guessed percentage produces
  revenue that does not exist, with decimals.
- Editing a pursuit's stage instead of appending the change.
- Recording a loss without asking whether anyone requested a debrief.
- Declaring a quiet pursuit dead instead of reporting how long it has been
  quiet.
- Letting "we always chase everything from this client" stand in for a go
  decision. Log it as what it is: no decision.
- Using the win-rate history as a forecast for next year.
- Tracking only the official pursuits because the unofficial ones are not
  real yet. They are the ones spending unbudgeted time.

## Resources

None. This skill is one file. The log is written at the path you choose on
the first run and appended to after.
