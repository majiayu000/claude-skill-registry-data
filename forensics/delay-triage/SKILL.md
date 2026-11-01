---
name: delay-triage
description: "Sorts a delay before it becomes a claim: establishes what is actually late against what baseline, whether the delayed activity was ever controlling the completion date, who caused it, and whether the contract makes it compensable, excusable, or neither. Separates the three questions that get merged — is it late, is it critical, and whose is it — because a delay can be real and cost nobody anything. Trigger on \"we are behind\", \"the contractor says we delayed them\", \"is this a critical delay\", \"do we owe them time\", \"delay-triage\", or a delay asserted with a letter likely to follow. Carries no contract terms and no float conventions; entitlement comes from the executed agreement you quote. It is not a delay analysis, which is forensic and has a methodology, and it does not replace the scheduler, the attorney, or the Architect of Record."
license: MIT
metadata:
  title: "Delay Triage"
  summary: "Work out whose delay this is before anyone writes a letter"
  discipline: "construction-admin"
  tags: "Construction Admin, Review"
---

# Delay Triage

A delay is asserted, a letter is drafted, and the position taken in the first
week is the position everyone is stuck with. The three questions that decide it
get merged into one argument, and they have different answers: is something
late, does it matter to the end date, and whose fault is it.

## Scope and limits — read first

**What this does.** Separates the three questions, establishes what can be
answered from the documents at hand, and says what would have to be true for the
delay to be compensable, excusable, or neither. Names what to record this week.

**What this does not do.**

- **It is not a delay analysis.** A forensic analysis has a methodology, a
  baseline, and an expert. This is the triage that decides whether one is
  needed.
- **It carries no contract terms.** What counts as an excusable delay, what
  notice is required, who owns float, and what compensation follows all come
  from the executed agreement, quoted.
- It does not review the schedule. `schedule-review` reads the contractor's
  programme, and this uses what it found.
- It does not decide entitlement or write the response.
  `dispute-advisor` finds the next required step; `/draft-email` and
  `/draft-letter` write.
- It does not replace the scheduler, the attorney, or the Architect of Record.

**What you need before starting.** The accepted baseline, if there is one. The
current schedule or update. What is asserted, by whom, in writing. The contract's
delay and notice provisions, quoted. The record: RFIs, submittals, instructions,
weather.

## Workflow

### Step 1. Establish what baseline this is measured against

Ask, in one message:

> 1. Is there an accepted baseline programme? Accepted by whom, when, and was it
>    ever formally accepted or just received?
> 2. What is the current schedule, and what has changed in its logic since the
>    baseline? Point at `schedule-review`.
> 3. What exactly is asserted: which activity, how many days, and against what?
> 4. Quote the contract on delay: what is excusable, what is compensable, what
>    notice is required and by when, and who owns float.
> 5. Has notice been given, in the form the contract requires, within the time
>    it requires?
> 6. What is the record: RFI log, submittal log, instructions, site records,
>    weather. Point at `rfi-tracker` and `submittal-log-builder`.

**No accepted baseline means no measurable delay**, and it is the most common
finding. Say so plainly and early. Everything after it is provisional.

**The notice question is asked second because it is often decisive.** A valid
entitlement lost for want of notice is common on both sides.

### Step 2. Answer the three questions separately

Never as one:

| Question | Answer | Evidence | Confidence |
|---|---|---|---|
| Is the activity late? | | Against which baseline | |
| Was it on the critical path? | | At the time, not now | |
| Who caused it? | | | |

- **Late** is measurable against a baseline, and only against one.
- **Critical** is the question that most delays fail. An activity with float that
  ran over cost nobody anything, and the contract usually says who owned that
  float. Note also that the critical path moves: what mattered in March may not
  have mattered in June, and the test is whether it was critical **at the
  time**.
- **Caused by** is separate from both. An activity can be late, critical, and
  nobody's fault.

Report each with its own confidence. A delay that is late but not critical
usually ends the conversation, and getting there fast is the point of this.

### Step 3. Sort the cause honestly

| Cause | Who | Evidence in the record |
|---|---|---|

Work through: a late instruction or a late response from the design team (check
the RFI and submittal logs against the contract's response periods, and point at
`schedule-review` which finds durations shorter than the contract allows), a
client decision or change, a differing site condition, weather beyond what the
contract allows for, a third party or utility, the contractor's own resourcing,
sequencing or procurement, and concurrency where two causes ran at once.

**Concurrent delay is where these arguments live**, and it is treated
differently by different contracts and different jurisdictions. Name it when it
is present and hand it to the attorney rather than resolving it.

Be honest where the cause is the design team's. A triage that cannot find its
own side's fault is a triage nobody should rely on, and the record will show it
anyway.

### Step 4. Say what the contract makes of it

Against the quoted provisions, for each cause:

| Cause | Excusable? | Compensable? | Notice given? | Clause |
|---|---|---|---|---|

Three different things, routinely merged:

- **Excusable** means the contractor is not liable for it. Time may be granted.
- **Compensable** means money follows. Fewer causes are compensable than
  excusable.
- **Neither** means the contractor absorbs it.

Never assert an answer the quoted text does not support. Where the contract is
silent or ambiguous, say so and hand it over.

### Step 5. Say what to do this week

Triage exists to produce actions, not a position:

- What to record now, before it is lost: site conditions, resourcing on site,
  what the schedule showed at the time, who said what.
- Whether notice is due from your side, and by when.
- Whether a formal analysis is warranted, and what it would cost.
- What not to write yet. **The first letter sets the position**, and a letter
  conceding or asserting before the three questions are answered is the most
  expensive document in the file.
- Who to bring in: the scheduler, the attorney.

### Step 6. Report

- Whether there is an accepted baseline, first.
- The three questions with separate answers and confidences.
- The cause table, including the design team's own contribution.
- The contract position, with anything the text does not support marked open.
- The actions for this week, and what not to write yet.

Close by saying no analysis was performed and no entitlement was determined.

### Step 7. Save

Ask where. This is read back in a dispute, and its value is that it was written
before anyone took a position.

## Rules

- **Answer late, critical and caused-by as three separate questions.**
- Say plainly when there is no accepted baseline.
- Test criticality at the time, not against the current schedule.
- **Never assert entitlement.** Quote the clause or mark it open.
- Name the design team's own contribution where there is one.
- Name concurrency and hand it over rather than resolving it.
- Say what not to write yet.

## Anti-patterns

- Arguing entitlement before establishing criticality.
- Measuring against the current schedule rather than the baseline.
- Treating excusable and compensable as the same thing.
- Missing that notice was never given.
- A triage that finds no fault on its own side.
- Resolving concurrency.
- Writing the letter first and working out the position afterwards.
- Assuming float belongs to whoever needs it.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
