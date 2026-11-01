---
name: go-no-go-review
description: "Scores a pursuit before the proposal is written, against the factors that actually predict whether a project is won and whether it is worth winning: the relationship, the client's decision process and funding, the competition, the fit with what the practice does, the fee and terms, and the capacity to deliver it. Records the decision and the reasoning so it can be read back against the outcome. Trigger on \"go no go\", \"should we chase this\", \"pursuit review\", \"is this RFP worth answering\", \"go-no-go-review\", or an opportunity raised for a decision. Carries no scoring weights and no thresholds; the practice sets what matters to it and what score means yes. It does not write the response — `rfp-response-builder` does — and does not decide. It records a decision somebody made, with the reasoning, so the next one is better informed."
license: MIT
metadata:
  title: "Go / No-Go Review"
  summary: "Score a pursuit before it costs you, on the things that actually predict"
  discipline: "practice-contracts"
  tags: "Review"
---

# Go / No-Go Review

Practices lose more money on projects they won than on ones they did not. The
review is worth doing because it is written down: a decision with reasoning
attached can be read back in a year against what happened, and that is the only
way the judgement improves.

## Scope and limits — read first

**What this does.** Works a pursuit through the factors that predict, records a
score and, more importantly, the reasoning behind each one. Names what would
change the answer. Writes it so it can be revisited after the outcome is known.

**What this does not do.**

- **It carries no weights and no thresholds.** What matters to a practice, and
  what score means pursue, are the practice's own. It will help build them and
  it will not supply them.
- It does not decide. A principal decides. This makes the decision legible.
- It does not estimate the fee. `fee-estimator` does.
- It does not write the response. `rfp-response-builder` does.
- It does not assess the client's finances beyond what you can find out and
  choose to record.

**What you need before starting.** The opportunity: client, project, scope, and
how you heard about it. Who else is likely bidding. Your relationship with the
client. Your current workload. The submission requirements and the deadline.

## Workflow

### Step 1. Establish the practice's own factors, once

On the first run, build the factor list with the practice and keep it. Suggested
starting set, to be edited rather than adopted:

| Factor | What it asks |
|---|---|
| Relationship | Do we know them, and did the last one go well? |
| Decision process | Do we know who decides, on what basis, and when? |
| Funding | Is it funded, and is the funding conditional? |
| Competition | Who else, how many, and is anyone incumbent? |
| Fit | Is this what we do, or what we would like to say we do? |
| Reference value | Does winning it get us the next three? |
| Fee and terms | Is the fee viable and are the terms signable? |
| Capacity | Can we staff it, with whom, and what does it displace? |
| Risk | Delivery method, programme, client's history with claims |
| Pursuit cost | What does chasing it cost, and what does that displace? |

**"Fit" and "capacity" are the two that get scored optimistically**, and they are
the two that predict a bad project rather than a lost one.

### Step 2. Score, and write the reason beside every score

| Factor | Score | Reason | Confidence | What would change it |
|---|---|---|---|---|

**A score with no reason is not recorded.** The reason is the part that is worth
anything in a year; the number is not.

`Confidence` is about what you actually know. A high score on a factor nobody
has information about is the most dangerous cell in the table, and it gets
flagged rather than averaged away.

### Step 3. Ask the four questions a score cannot answer

Regardless of the total:

- **Is there an incumbent, and are we being used to test their price?** If so,
  the odds are not what the score suggests.
- **Do we know who actually decides?** Not the contact. The decider. If not,
  the pursuit is being run blind.
- **What happens to this pursuit if our best two people get busy?** Most
  proposals are written by the people who are already delivering.
- **If we won it tomorrow, would we be pleased?** The question people answer
  honestly only in a room, and the one that catches the projects that should be
  declined.

### Step 4. Name the decision and what it rests on

Record: pursue, decline, or pursue conditionally. Where conditional, name the
condition precisely — a fee floor, a terms change, a partner, a staffing
commitment — and name who checks it and by when.

Record who decided and when. A decision with no name against it is a decision
nobody revisits.

### Step 5. Write it so it can be read back

The file carries: the score table with reasons, the four questions, the
decision, the decider, the date, and a blank outcome section.

**Fill the outcome section later**: won or lost, why if known, and if won, how
the project actually went against what was scored. Point at `lessons-learned`.
A go/no-go archive with outcomes attached is the only thing that makes the next
one better, and it takes two minutes to complete.

### Step 6. Save

One file per pursuit, in a consistent location. Ask where on the first run and
use the same place after, so the archive accumulates.

## Rules

- **Never supply weights, thresholds, or a recommendation.**
- **Every score carries a reason.** No reason, no score.
- Flag high scores held with low confidence.
- Ask the four questions regardless of the total.
- Record who decided and when.
- Leave the outcome section, and prompt to fill it when the result is known.

## Anti-patterns

- Scoring after the decision has been made, to justify it.
- Scoring fit by what the practice wants to become.
- Scoring capacity on the assumption that current projects will finish on time.
- Averaging away a low-confidence score.
- Pursuing because declining feels like weakness.
- Leaving the outcome section blank forever, which makes the whole archive
  worthless.
- Treating the total as the decision.

## Resources

None. This skill is one file. Output is written at the path you choose and the
archive accumulates there.
