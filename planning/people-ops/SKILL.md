---
name: people-ops
description: "Use when hiring, onboarding or offboarding: a defensible hiring decision, a new hire productive early, a departure that leaks neither access nor knowledge. Not employment-law advice."
---

# people-ops

Business layer (`business/README.md`). Same posture as `business/data-protection`: this is the
engineering-adjacent structure around hiring/onboarding/offboarding, not the legal or contractual side
of employment, which is jurisdiction-specific and goes to whoever owns HR/legal.

**This is not employment-law advice.** Notice periods, termination rules, discrimination law, contract
types — all jurisdiction-specific, all go to HR/legal. What this block owns: the structure that makes a
hiring process fair and defensible, a new hire's first months productive, and an offboarding clean
rather than a scramble.

## When
Writing a job posting, running or scoring interviews, choosing between final candidates, planning a new
hire's first weeks, or someone (voluntarily or not) leaving the company.

## Steps

### 1. Hiring: structure before the first interview
1. **Define the role's required competencies before writing the posting**, not while reading CVs — a
   short list of what the job actually requires, derived from the real day-to-day work, not a wishlist
   copied from a similar posting elsewhere.
2. **The same questions, in the same order, for every candidate for a given round.** An unstructured
   "just have a conversation" interview is where irrelevant impressions (does this person remind me of
   someone, do we click) quietly outweigh job-relevant signal — structured interviews are measurably
   better at predicting job performance, not just fairer on paper.
3. **Score against a rubric tied to the competencies from step 1**, not a gut "yes/no" after the call.
   A scorecard filled in by each interviewer independently, before comparing notes, catches a lot that a
   group discussion starting from "so, what did everyone think?" doesn't.
4. **Document why a candidate was passed over or advanced**, tied to the rubric. Not for ceremony — it's
   what lets a hiring decision be explained later, to the candidate or otherwise, as job-related rather
   than a vibe.
5. **Involve more than one interviewer on any decision that ends a candidate's process**, and calibrate
   interviewers on how to score before they run real interviews — an untrained scorer reverts to gut
   feel with extra paperwork around it.

6. **Review the job posting as a document before it goes out.** Check each requirement against step 1:
   a must-have that is really a preference, a years-of-experience figure with no basis, an inflated title, or
   wording that signals who is expected to apply. Symptom: a long list of must-haves and a thin pool. Fix: keep
   the few the job truly needs, state the rest as learnable, and say what the work is and what the process looks
   like.
7. **A scorecard that works is short and anchored.** One line per competency, a described example for each level
   of the scale, a place for the evidence heard (not an impression), and a line for what was not assessed.
   Symptom: every candidate scores four of five on everything. Fix: anchor the levels and ask for the evidence.
8. **Hold the same process for referred and internal candidates**, and keep questions to what the job requires.
   Avoid asking about family, health, age, origin or plans of the candidate; what is lawful to ask differs by
   place and goes to HR or legal, not legal advice.
9. **Check what the process did to the pool.** Count candidates at each stage and look for a step that loses
   people for reasons unrelated to the job (a long test, an unnecessary requirement). Record the counts; do not
   infer a cause from small numbers.
10. **Tell candidates what to expect and when**, then keep to it, including a short reply to those who are
    declined. Silence is the common complaint and costs the employer's reputation.
11. **Write the rubric before reading any application.** A rubric written after seeing the pile gets shaped to
    fit whoever looked good, and cannot be defended later. Three tiers: a short list of must-haves where absence
    truly disqualifies (a legally required licence, availability for the real shift), weighted should-haves that
    produce the ranking, and nice-to-haves that never disqualify. Each criterion must be checkable on a CV
    ("has worked on site with customers"), never a vague trait ("strong communicator", "culture fit") that turns
    into a proxy for polish or schooling. Symptom: "here are the five strongest" with no measure behind it.
12. **Score only what the rubric names, with a quoted line per score.** Name, age, photo, address, school
    prestige, a gap in employment, typos beyond what the job needs and CV layout are not criteria. Score the
    described work against the criteria, and bring identity back after the ranking. If a score has no quoted
    evidence, it is an impression.
13. **Keep a "cannot assess" band apart from a rejection.** A missing fact (the CV never says whether the
    required licence is held) is not a zero: mark the criterion as not assessed, leave its weight out of both the
    points and the total, report the score as a share of the weight actually assessed beside that weight, and send
    a short question to the candidate. Symptom: a candidate declined for a formatting gap.
14. **The ranking is not the decision.** Present the order with the evidence per candidate and where a lower
    overall score is higher on what the team lacks; the person who hires holds context no CV carries. In a batch
    message to that person, name each candidate in each group (invite, hold, decline, question) rather than
    giving counts, so a mis-sorted list is visible before anything is sent, and send nothing to candidates
    without that person's approval. Never state an invented reason in a decline; give a true one or none.

### 2. Onboarding: the first 90 days have a plan
1. **A new hire gets a written plan before day one**, broken into phases: the first 30 days is about
   context (how the company/team actually works, who the key relationships are, the tools), the next 30
   about starting to contribute on real but bounded work, the last 30 about executing more
   independently. The exact split is less important than having *a* plan instead of "figure it out as
   you go."
2. **The manager owns onboarding, not HR handing over a checklist.** A new hire whose manager is
   actively involved in the first weeks — regular 1:1s, explicit check-ins at the 30/60/90 marks — settles
   in measurably faster than one left to self-serve through a wiki.
3. **Set a small number of concrete goals per phase**, not a vague "get up to speed." A goal that's
   checkable ("ship this bounded change," "own this recurring meeting") gives both sides a real signal
   at the 30/60/90 review instead of an impression.
4. **A remote or distributed new hire needs the relationship-building made explicit** — scheduled
   1:1s with people outside their immediate team, not just their manager — because the hallway
   conversations that would otherwise build those connections don't happen on their own.

### 3. Offboarding: clean exit, no leaks
1. **Access revocation is scheduled from the moment a departure is known, not improvised on the last
   day.** For an involuntary departure, access is cut immediately; for a voluntary one, within hours of
   the final working day — and privileged/admin access is revoked at the same time as general access,
   never left for "later, when someone gets to it."
2. **Audit what the departing person actually had access to before revoking it**, including any shared
   credential they held — a shared account nobody rotates after someone leaves is a lingering access
   nobody remembers granting.
3. **Knowledge transfer happens during the notice period, not retroactively reconstructed after they're
   gone.** A short written handover — the processes only they ran, the contacts only they had, the
   decisions only they'd remember the reasoning for — captured in the team's normal documentation
   location, not a one-off email that gets lost.
4. **Assign an owner and a deadline to each offboarding step** (access, hardware return, knowledge
   transfer, final pay/benefits administration) tied to the departure date — an offboarding checklist
   with no owner per line is a checklist nobody is actually accountable for finishing.

### 4. Ongoing performance: continuous, not a once-a-year surprise
1. **A once-a-year review graded mostly on the last few weeks is recency bias by construction.** The
   fix isn't a better rating scale, it's not letting a whole review period go undocumented: regular
   short check-ins (monthly or quarterly) with brief written notes create a real trail to grade against,
   instead of reconstructing a year from memory the week the review is due.
2. **Ground the review in something checkable** — stated goals from the last check-in, concrete
   outcomes, peer/cross-functional input where the work is collaborative — rather than a single
   manager's unaided impression. The goal is the same one `business/data-analytics` §5 states for a
   KPI: a claim that survives being questioned later, not a vibe.
3. **Calibrate across managers before ratings are final** for any process that compares people across
   teams (a bonus pool, a promotion round): a short session comparing how different managers rated
   similar work catches the manager who rates everyone a 4 and the one who never gives a 5, before that
   inconsistency reaches the employee as an unexplained outcome.
4. **State promotion/advancement criteria before the review that decides one**, not as a
   post-hoc justification for a decision already made. An employee who doesn't know what a promotion
   actually requires can't work toward it, and a criterion invented after the fact reads as exactly
   that, whether or not it was.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a scorecard per
candidate tied to a stated competency list, a written 30/60/90 plan for a new hire with a manager
actively engaged in it, a documented trail of check-ins that a periodic review is graded against rather
than the last few weeks alone, and an offboarding checklist with access revoked on schedule, knowledge
captured during the notice period, and an owner per step.

## Guardrails
- Never decide a termination's legality, a notice period, or how a specific jurisdiction's labour law
  applies — that goes to HR/legal, the same way `business/data-protection` routes a lawful-basis
  question.
- Never run an unstructured, ad hoc interview process for a role that has a structured one defined —
  consistency across candidates is what makes the process defensible.
- Never leave access revocation until "whenever IT gets to it" — schedule it to the departure date, not
  to convenience.
- Never treat knowledge transfer as something that happens automatically through documentation that
  already exists — if it wasn't written down before, it needs to be, during the notice period.
- Never read applications before the rubric exists, and never count a missing fact as a zero: write the rubric
  first and use a "cannot assess" band (§1, points 11 to 13).
- Never let a rating that compares people across teams go final without a calibration pass, and never
  invent a promotion criterion after the decision it's meant to justify.
- This block has no dedicated in-house HR expertise behind it yet: a solid set of structural defaults,
  not proven doctrine, to be confronted with a real hiring/onboarding/offboarding/review cycle.

## Origin
Assembled from public sources, written without internal HR expertise, same honesty posture as
`business/data-protection`. Structured-interview and scorecard practice (defined competencies before
writing the posting, same questions in the same order, independent scoring against a rubric before
comparing notes, documented job-related rationale): published hiring-bias-reduction guidance. The
30-60-90-day onboarding structure and the manager-engagement finding: published onboarding-practice
research and guides. Offboarding staging (scheduled access revocation tied to departure type,
privileged access revoked with general access, pre-revocation access audit, notice-period knowledge
transfer into the team's normal documentation, owner-and-deadline per checklist step): published
offboarding/IT-security checklists aimed at HR and security teams jointly. §4 (ongoing performance)
added the same day from published continuous-feedback/recency-bias-mitigation and calibration-session
practice — the once-a-year review's core failure mode (grading mostly on the last few weeks) and the
fix (a documented trail of check-ins, cross-manager calibration before ratings are final, stated
promotion criteria before the decision) are established performance-management guidance, not
internally validated. Stamped 2026-08-11. §1 points 6 to 10 (job-posting review, anchored scorecards,
process consistency, pool check, candidate communication) added 2026-10-20 from general recruiting practice; no
source read, employment and discrimination law not covered. §1 points 11 to 14 (rubric before reading, scoring only
the rubric with quoted evidence, a "cannot assess" band, ranking versus decision and named batch summaries) added
2026-10-21, rewritten in our own words from the hiring-screener notes of a small-business plugin set
(anthropics/knowledge-work-plugins, Apache-2.0, read 2026-10-20); its weights, scale and scoring formula were not
carried and its US-specific lawfulness remarks are not repeated here.
