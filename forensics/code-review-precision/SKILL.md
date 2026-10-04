---
name: code-review-precision
description: Keeps a review to the findings that are real and worth acting on. Use this skill when reviewing a change, in code in any language or in documentation.
---
# Code Review Precision

## Why This Skill Exists

An adversarial review is meant to over-collect, because a defect you never considered is a defect you never report.
Over-collection is only useful if something narrows the result afterwards, and this skill is that step.
Two findings with evidence behind them are worth more than ten a reader has to triage.

## Collect First, Then Filter

Do the full adversarial pass before you judge any candidate.
Filtering while you search suppresses the findings you are least sure about, which are often the ones worth the most.
Only once the pass is complete do you score what you found.

## Scoring Each Finding

Score every candidate from 0 to 100 on how confident you are that it is real, in scope, and has consequences beyond the review.
Drop everything below 80.
Keep the score to yourself; report the finding, not the number.

Drop a candidate when any of the following is true.

- It stops being a defect once you read the surrounding code rather than the diff alone.
- It is a pre-existing problem that the change under review neither introduced nor touched.
  Note it separately as out of scope rather than folding it into the review.
- It is a style preference with no failure scenario behind it.
- You cannot describe the inputs or the state that make it go wrong.

## Reporting the Result

Give every finding that survives a concrete failure scenario, meaning the specific inputs or state that trigger it, so the reader can judge it without repeating your analysis.
When nothing clears the bar, say so plainly and briefly.
Never pad a review to make it look thorough, and never invent a finding because a review with none feels incomplete.
