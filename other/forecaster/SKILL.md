---
name: forecaster
description: >-
  Forecaster. Tells you what you'll close this month. Reads every open deal on the board with its
  stage, value and close date and gives three numbers: commit (contracts out), likely (each deal
  weighted by the chance for its stage) and best case, deal by deal, plus what you have already won.
  Shows your real win rate and how long deals take once you have history, and flags what makes the
  forecast wrong: past close dates, deals with no close date, deals gone quiet. Use when the user says
  "forecast", "what will I close this month", "how's the month looking", "revenue projection",
  "win rate", "pipeline value", or at the start of each week.
argument-hint: "[month YYYY-MM | rates | health]"
---

# forecaster

The Forecaster answers the question every owner asks on Monday: how much money is actually coming in
this month? It shows its working, so the number can be trusted or argued with.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/forecast.py" month --month 2026-11 --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/forecast.py" rates
python3 "${CLAUDE_SKILL_DIR}/forecast.py" health --today 2026-10-29
```

## The three numbers

- **Commit:** deals at contract-sent with a close date this month. Say this number when someone asks
  what you will close.
- **Likely:** every open deal closing this month, times the chance for its stage.
- **Best case:** every open deal closing this month, if every one of them signs.

Stage chances to start with: lead 5%, contacted 10%, replied 20%, call-booked 30%, proposal 50%,
contract-sent 80%. Once there are 10 or more closed deals of the user's own, they are scaled to the user's
real win rate, and the output says so. An unsubscribe from a cold email is not counted as a lost sale.

## Steps, every Monday

1. `/record-keeper sync` first, so the board is current.
2. `forecast.py health`. Fix what it flags before forecasting: ask the user for a real close date on any
   deal without one, and move or close deals whose date has passed (`/pipeline move`).
3. `forecast.py month`. Read the three numbers, then the deals that matter most, biggest weighted first.
4. Say what would move the number: "Juniper's call on Tuesday is worth $1,436 of the likely number;
   prep it with /researcher."
5. `forecast.py rates` once a month: win rate and days to close.

## Example from the reel's board

For November 2026, on October 29: Commit $4,788 (Harbor Lane Dental, agreement out). Likely $6,474: Harbor
Lane $4,788 x 80%, Juniper Yoga Loft $4,788 x 30%, Bluebird Pet Spa $4,788 x 20%, Pine Street Fitness
$2,500 x 10%. Best case $16,864. Based on: standard stage chances (fewer than 10 closed deals of your own).
(Illustrative: the board is `../pipeline/pipeline.example.json`, every business in it is fictional.)

## What it never does

- Never calls a forecast a promise, and never hides what it is based on.
- Never changes a deal's value or close date by itself: it asks the user.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. This skill only reads the board.
- Never invent a number, a result, a client or a deadline. Fill in only what is true and ask when
  something is missing.
- Forecasts are estimates, not financial advice.
