---
name: qa-hiring-kit
description: "End-to-end structured hiring for QA / SDET / automation / test-lead / quality-manager roles - one chain from job description through interview question bank, competency-anchored scoring rubric, interviewer calibration guide, and post-interview panel debrief, to the 30-60-90 day onboarding plan. Implements the canonical Levashina 2014 et al. structured-interview methodology with ISTQB-aligned competency vocabulary, so the JD a candidate reads, the rubric the panel scores, and the ramp plan the manager runs all describe the same role. Use when opening a QA requisition, authoring any artifact of the hiring loop (JD, questions, rubric, calibration guide, onboarding plan), or running the panel debrief to a defensible hire / no-hire decision."
---

# qa-hiring-kit

## Overview

Hiring for QA roles is calibration-heavy: the same question scored by two
interviewers without a rubric produces high noise. The remedy, per the
structured-interview research
([Levashina et al. 2014, *Personnel Psychology*](https://en.wikipedia.org/wiki/Structured_interview)),
is a **structured interview** - same questions, same order, same scoring
rubric, calibrated interviewers. This kit runs the whole chain as one
workflow, with one competency vocabulary (drawn from the
[ISTQB Foundation Level v4.0 syllabus](https://www.istqb.org/certifications/certified-tester-foundation-level))
threaded through every artifact:

| Stage | Artifact | Deep reference |
|---|---|---|
| 1. Open the role | Job description + recruiter screening note | [references/jd-author.md](references/jd-author.md) |
| 2. Ask | Role + seniority question bank (STAR, Bloom's K1-K4) | [references/interview-questions.md](references/interview-questions.md) |
| 3. Score | 4-level competency-anchored rubric | [references/rubric.md](references/rubric.md) |
| 4. Calibrate | Gold-standard answers + panel session script | [references/calibration.md](references/calibration.md) |
| 5. Decide | Panel debrief to hire / no-hire (workflow below) | this file, "Running the debrief" |
| 6. Ramp | 30-60-90 day onboarding plan | [references/onboarding.md](references/onboarding.md) |

Stages 2-4 are the structured-interview tripod - *what we ask*, *how to
score*, *what each score looks like*. None of the three is sufficient alone;
running structured interviews requires all three.

## When to use

- A QA / SDET / test-lead / quality-manager requisition is approved and
  nothing is written yet - start at stage 1 and work down.
- One artifact of an existing loop needs authoring or recalibrating (a stale
  question bank, a rubric with drifting anchors, a missing calibration
  guide) - jump to that stage's reference.
- An interview round is complete and the panel must converge on a documented
  hire / no-hire recommendation - run the debrief workflow below.
- A hire has accepted and the manager needs the first-90-days plan - stage 6.

Do **not** use this kit to:

- Map the current team's capability or decide train-vs-hire - that is
  `skill-matrix-author` (this plugin); its gap report is the ideal "why this
  role is open" input to stage 1.
- Author generic (non-QA) engineering interview loops - the competency
  model is QA-specific.

## The chain, end to end

1. **JD first** ([references/jd-author.md](references/jd-author.md)).
   Responsibilities derive from ISTQB CTFL §1.4.5's testing-role vs
   test-management-role split; must-haves reuse the rubric's competency
   dimensions so the posting and the scoring describe the same role. Ships
   with a recruiter screening note (signal vs noise per must-have).
2. **Question bank** ([references/interview-questions.md](references/interview-questions.md)).
   6-8 slots per interview, mixed by role (technical / behavioral-STAR /
   scenario / system-design), difficulty tuned by seniority via Bloom's
   K1-K4, with pre-authored follow-up probes. Lock the bank at round start.
3. **Rubric** ([references/rubric.md](references/rubric.md)). 5-8 competency
   dimensions per role; four behavioural anchors per (competency × question)
   cell describing what the candidate **said or did**; summary by
   per-dimension floors, never averages.
4. **Calibration guide** ([references/calibration.md](references/calibration.md)).
   Four worked gold-standard answers per question (one per score level),
   common interviewer pitfalls, and the mandatory 90-minute panel
   calibration session before the first real candidate.
5. **Debrief** - the workflow below, run after the final interview.
6. **Onboarding plan** ([references/onboarding.md](references/onboarding.md)).
   30-60-90 ramp anchored to the same rubric axes; borderline-scored axes
   get targeted phase-2 development.

Lock artifacts at the start of a hiring round; mid-round changes invalidate
prior candidates' scores.

## Running the debrief

After the final interview, the panel converges on a decision in a
facilitated calibration loop. Required inputs: role + seniority, the
filled-in rubric with each interviewer's per-dimension scores, the
calibration guide, and the panel list. Refuse to start if any interviewer's
scores were not submitted independently before the debrief - per
anchoring-bias research
(https://en.wikipedia.org/wiki/Anchoring_effect), the first opinion revealed
in a group setting has disproportionate influence on subsequent scorers;
independent pre-submission is the primary structural mitigation.

1. **Collect independent scores.** Confirm every panelist has scored all
   dimensions before any scores are shared. If a submission is missing,
   halt: emit `INCOMPLETE_PANEL_SUBMISSION` with the missing interviewer's
   name and a deadline.
2. **Compute per-dimension agreement.** Flag any dimension with a spread
   greater than 1 point. Per the employment-interview research showing
   anchored rating scales are the load-bearing mechanism for acceptable
   inter-rater reliability
   (https://en.wikipedia.org/wiki/Employment_interview), a >1 spread means
   the anchor was applied differently - the discussion must focus on the
   anchor text, not general impressions.
3. **Surface evidence, not impressions.** For each flagged dimension, each
   panelist quotes the specific candidate utterance or action that drove
   their score (the rubric's anchor principle: anchors describe what the
   candidate said or did, not what the interviewer felt). Impressions not
   traceable to a quoted behavioural observation are set aside.
4. **Apply the calibration guide to disagreements.** Read the relevant
   gold-standard answers and ask each dissenting panelist: "Which of the
   four worked examples does this candidate's answer most resemble?"
   Concrete comparison is the resolution mechanism - not majority vote or
   seniority deference.
5. **Flag bias language.** Watch for the calibration guide's pitfall
   categories: scoring on tone or confidence; halo-effect generalisation
   ("the candidate is clearly senior"); anchor drift ("I never give 4s").
   When flagged, name the category and re-score against the anchor.
6. **Compute the summary recommendation** by the rubric's per-dimension
   floor rules (any dimension at 1 is a no-hire regardless of totals; two or
   more dimensions at 2 is a no-hire; one dimension at 2 with all others ≥ 3
   is borderline). Never average across dimensions.
7. **Write the decision document**: per-dimension score table with evidence
   anchors, disagreements resolved (scores before discussion, gold-standard
   comparison used, bias flags raised), the HIRE / NO HIRE / BORDERLINE
   summary with a rationale traced to specific scores, and required next
   steps. A BORDERLINE recommendation escalates to the hiring manager with
   the document - never a committee re-vote. A debrief with no rubric
   present reverts to an unstructured discussion (`MISSING_RUBRIC` - halt);
   that validity loss is what structured interviews exist to prevent
   (Levashina et al. 2014,
   https://en.wikipedia.org/wiki/Structured_interview).

## Anti-patterns (chain level)

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Running interviews with questions but no rubric (or vice versa) | Half a structured interview still drifts; the pair is the unit. | Stages 2 + 3 travel together; stage 4 before the first candidate. |
| JD vocabulary differing from the rubric | Candidate applies to one role, gets scored on another; debriefs derail. | Stage 1 reuses the rubric's competency dimensions. |
| Skipping the calibration session | Inter-rater agreement does not appear without practice. | The stage-4 session is mandatory before the first real candidate. |
| Deciding by committee re-vote on a borderline | Reverts to unstructured group dynamics. | Escalate BORDERLINE to the hiring manager with the decision document. |
| Shelving the rubric after the offer | The hire's weak axes are known and then ignored. | Stage 6 converts borderline axes into targeted phase-2 development. |

## Limitations

- **No compensation benchmarking, legal review, or fairness audit.** Salary
  bands, employment-law phrasing, and bias review of questions / anchors /
  criteria are HR and legal's call per jurisdiction.
- **Not a technical screen.** SDET / automation roles still warrant a
  take-home or coding round; the kit produces interview artifacts, not
  coding exercises.
- **Artifacts age.** Re-derive the JD per opening and re-calibrate per
  hiring round; the anchor-drift log in the calibration guide carries
  refinements forward.

## Hand-off targets

- **Why this role is open / train-vs-hire** → `skill-matrix-author` (this
  plugin) - its capability-gap report feeds stage 1.
- **Ongoing development beyond day 90** → the team's career-progression and
  performance process; out of scope here.

## References

- Structured interview research - Levashina et al. 2014
  ([*Personnel Psychology*](https://en.wikipedia.org/wiki/Structured_interview)) -
  the validity uplift from same questions / same order / anchored scoring;
  methodological basis for the whole chain.
- ISTQB Certified Tester Foundation Level v4.0 syllabus - the competency
  vocabulary threaded through JD, questions, rubric, and onboarding:
  https://www.istqb.org/certifications/certified-tester-foundation-level
- STAR behavioral interviewing method:
  https://en.wikipedia.org/wiki/Situation,_task,_action,_result
- Anchoring effect - the bias that independent score pre-submission
  mitigates: https://en.wikipedia.org/wiki/Anchoring_effect
- Employment interview - anchored rating scales and inter-rater
  reliability: https://en.wikipedia.org/wiki/Employment_interview
- PractiTest 2026 State of Testing Report - hiring-artifact authoring as a
  high-adoption, low-risk AI use case for QA managers:
  https://www.practitest.com/state-of-testing/
