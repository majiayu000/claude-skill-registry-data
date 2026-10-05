---
name: cx-reviewer-workload
description: Use to staff and schedule QA reviewers for sustainable throughput without grading quality collapsing — fatigue, drift, and false precision from treating reviewers like production agents. Trigger for "how many QA reviewers do we need", reviewer capacity planning, grader fatigue, throughput per reviewer, calibration after long shifts, or scores drifting over the course of a day.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Reviewer workload and grading quality

QA programmes often staff reviewers like production agents: fill eight hours, count
evaluations completed, treat shortfall as a productivity problem. **Grading is
cognitive inspection work**, not ticket handling. Throughput ceilings are real,
fatigue shifts thresholds, and a team that "keeps up" on volume can be silently
destroying measurement quality.

This skill plans **sustainable capacity**, **detects fatigue and drift**, and
**requires calibration as part of workload** — not as an optional extra when someone
has time.

## Step 1: Measure grading time, not assumptions

Before headcount math, observe:

- **Minutes per evaluation** by channel, rubric length, language, and tooling — median
  and upper tail (complex regulated tickets are the tail that breaks plans).
- **Non-grading time** — calibration sessions, dispute adjudication, rubric meetings,
  queue management, breaks.
- **Effective evaluations per reviewer per day** under normal conditions, not hero days.

Plans built on "ten minutes each" without measurement usually miss by half. Run a
one-week time study on a representative mix before scaling.

## Step 2: Set throughput ceilings, not targets

A ceiling is the maximum sustainable count **before quality checks fail**. A target
is what management wants. When target exceeds ceiling, quality loses.

Rules of thumb — verify in your environment, do not treat as constants:

- **Block focused grading in chunks** with breaks; marathon continuous grading
  correlates with drift.
- **Cap evaluations per reviewer per day** from the time study, leaving slack for
  calibration and disputes — not 100% utilisation.
- **Separate high-complexity queues** from bulk grading; mixing them in one shift
  hides fatigue on the hard items.

If volume demands exceed ceiling × headcount, the honest options are: hire, simplify
the rubric, automate with validation, or **reduce claimed coverage** — not speed up
graders indefinitely.

## Step 3: Schedule calibration as production work

Calibration is not training that happens once. It is **ongoing measurement of the
measurement instrument**.

Minimum sustainable programme:

- **Regular calibration sets** — same gold conversations re-scored on a fixed cadence;
  frequency rises when rubric is new, graders are new, or drift is detected.
- **Post-fatigue checks** — short gold re-score after long blocks or end of shift when
  data suggest drift (see Step 4).
- **Dispute sample review** — contested evaluations feed back into grader feedback, not
  only into agent disputes.

Budget **calibration hours per reviewer per week** in the capacity plan. Programmes
that zero this out discover drift only when agents complain.

## Step 4: Detect fatigue and drift over a shift

Fatigue rarely announces itself as "I am tired". It shows up in the data:

| Signal | Possible interpretation |
| --- | --- |
| Pass rate creeps up through the day | Satisficing, shortened reading, threshold drift |
| Pass rate creeps down | Harshness drift, or harder tickets queued later |
| Time-on-evaluation drops while volume holds | Skimming |
| Specific criteria drift before others | Ambiguous criteria; first to go under pressure |
| Disagreement with gold set widens after hour N | Stop point for focused grading |
| AI–human gap widens by reviewer-hour | Reviewer rushing, or model stable while human drifts |

Analyse **verdict and time by reviewer × hour-of-shift × day** (with enough n). One
week of pattern is suggestive; confirm before redesigning shifts.

When drift is present:

- **Shorten grading blocks** and insert calibration breaks.
- **Rotate queue types** so hard items are not always last.
- **Recalibrate** the affected graders; do not assume a rubric fix when the instrument
  moved.
- **Exclude suspect periods from trend analysis** if drift was severe and uncorrected.

## Step 5: Do not mirror production staffing ratios

Production staffing answers "how many contacts arrive". QA staffing answers "how many
inspections can we perform at defined quality".

Common mistakes:

- **Same shrinkage and adherence model as agents** — grading has different failure
  modes; copying AHT logic misleads.
- **Peak staffing on production peaks** — evaluation can lag contact peak by design;
  grading yesterday's draw is often correct.
- **Using junior agents as reviewers without agreement testing** — cheap until disputes
  and rank decisions expose low agreement.
- **100% utilisation plans** — no room for calibration, illness, or rubric updates;
  plans break in the first busy week.

Right-size from **required evaluations per period** (see coverage economics for the
volume question) divided by **sustainable evaluations per reviewer**, plus calibration
and adjudication overhead.

## Step 6: Quality-of-grading checks alongside volume

Every capacity report should pair:

- **Volume** — evaluations completed vs plan.
- **Quality** — agreement with gold set, dispute overturn rate, time-on-task
  distribution, drift signals above.

Hitting volume with failing quality checks is **worse than missing volume** — it
produces numbers that look precise and are not.

Escalate when:

- gold agreement drops below the programme's own documented floor (you set the floor
  from calibration history, not from a textbook);
- overturn rate spikes for one reviewer;
- volume targets were met only by collapsing time-on-evaluation.

## Present results to the user

1. **Observed grading time** — median and upper tail by channel/rubric, with sample
   period stated.
2. **Sustainable evaluations per reviewer per day** — ceiling, not wishful target,
   with calibration and non-grading time included.
3. **Headcount recommendation** for the required evaluation volume, with explicit
   slack.
4. **Shift and block design** — chunk length, break pattern, queue rotation if needed.
5. **Calibration schedule** — cadence, hours budgeted, gold-set size approach.
6. **Drift analysis result** — if data exist: whether fatigue signals appear, by
   reviewer or hour, and proposed mitigations.
7. **Volume vs quality dashboard spec** — what to monitor weekly so throughput targets
   do not silently override grading quality.
