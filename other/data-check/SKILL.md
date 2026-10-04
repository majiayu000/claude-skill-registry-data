---
name: data-check
description: >-
  Checks the data quality of a survey CSV before any substantive analysis: fill/completion
  rates, speeders (via completion time), straightlining, thinly filled columns. Gives a
  traffic-light assessment and recommendations. Result as Markdown to reports/. Use as the
  first step on a new file or when data quality is in doubt. Invoke with your request as
  the argument, e.g. /data-check [optional CSV path].
license: MIT
---

# Data-Quality Check

Goal: **Before** any substantive analysis, assess how trustworthy the data is, so that weak
data doesn't lead to strong conclusions. Result as Markdown in `reports/`. A path in the
user's request selects the CSV; otherwise the one in the folder.

## Tool

```
python3 scripts/survey.py quality [--file CSV]
python3 scripts/survey.py profile [--file CSV]
python3 scripts/survey.py freq COL [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
`quality` directly returns:
- **Fill rate per column** (thin columns < 50% flagged),
- **Completion time** (median, range) and **speeders** (< 1/3 of the median duration),
- **Straightlining** in detected rating batteries (identical answer across ≥3 shared scales).

`freq` is needed only to verify a suspected contradiction with the survey context (see
below), not for the quality metrics themselves.

`--json` for structured values.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it — and then do something no other skill
does: **check it against the data.** Everywhere else the context is background; here it is
a claim under test.

A contradiction between what the context states and what the data show is a **finding in
its own right**, often a more serious one than a handful of speeders:

- **Population vs. behavior.** "Only active users were surveyed", but 12% say they never
  use the product → either the recruiting reached further than assumed, or the question is
  being read differently than intended. Both change how every later report must be worded.
- **Fieldwork vs. timestamps.** The stated field period does not match the timestamps in
  the data → possibly the wrong export, a merge of several waves, or stale context.
- **Sample size vs. expectation.** The context names a target group or a quota that the
  data cannot support (a segment that turns out to be n = 7).
- **Column notes vs. reality.** A column named as the lead question is thinly filled, or a
  battery described as belonging together is not present in that form.

Verify contradictions with the engine before reporting them — a suspicion is not a finding.
Describe what the context claims, what the data show, and what follows; do not decide which
side is wrong. A contradiction that materially affects who the results speak for belongs in
the overall verdict, not only in the details: data that are clean but describe a different
population than assumed are not green.

If no context document exists, run the check as before, and note in the report that the
study design could not be verified — this is not a defect of the data, but it is a limit of
this check. Point at `survey-context` once at the end.

## Approach

1. **Run `quality`** (and `profile` if you need column types).
2. **Interpret the findings.** For each dimension, judge whether it's harmless, worth
   watching, or problematic:
   - Thin columns → statements on those questions are only weakly supported.
   - Speeders → if a notable share, bias risk; consider exclusion.
   - Straightlining → sign of inattentive completion in batteries.
3. **Check the context against the data** (see above), if a context document exists.
   Confirm every suspected contradiction with a concrete `freq` / `profile` output.
4. **Assign a traffic light** (green / amber / red) with a short rationale.
5. **Derive recommendations** (e.g. "avoid column X for detail questions", "review/exclude
   Y speeders", "treat results on Z with caution").
6. **Save the report** to `reports/` (`date +%F_data-check`, never overwrite) and give the
   traffic light + path in your reply.

## Report format

```markdown
# Data-quality check

**Data basis:** <file> · n = <…> · columns = <…> · <date>

## Overall verdict: 🟢 / 🟡 / 🔴
1–2 sentences: are the data fit for reliable analysis?

## Findings
| Dimension | Result | Assessment |
|---|---|---|
| Completeness | avg fill, thin columns: … | 🟢/🟡/🔴 |
| Completion time | median … min, speeders … % | … |
| Straightlining | … % in battery / none detected | … |

## Thinly filled columns
List of columns < 50% with the consequence for analysis.

## Context vs. data
Only when a context document exists. Per contradiction: what the context states, what the
data show (with the number), what follows from it. If nothing contradicts, one sentence
saying the stated study design is consistent with the data. Without a context document:
"not assessable — no context document; the study design could not be verified."

## Recommendations
Concrete do's/don'ts for the analysis ahead (including possible case exclusions).

## Method
`survey.py quality`: definitions (speeder < 1/3 median duration; straightlining =
identical answer across a whole rating battery). Name the context document if one was
checked against.
```

## Rules
- Check first, interpret later — this check is deliberately the **first** step.
- Take metrics exactly from the `quality` output, don't estimate.
- Clearly label missing timestamps/batteries as "not assessable", not as "good". The same
  goes for a missing context document — unverified is not the same as verified fine.
- Name data-quality issues without dramatizing; make consequences concrete.
- A contradiction with the survey context is reported, never resolved by picking a side —
  and never quietly dropped because the data look clean otherwise.
- Report language default English.
