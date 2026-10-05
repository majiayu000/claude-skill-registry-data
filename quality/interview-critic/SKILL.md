---
name: interview-critic
type: critic
description: "Review user interview protocols, scripts, and findings for methodological rigor and bias."
version: 0.1.0
---

# Interview Critic Skill

## When to Use

**Primary triggers:**
- "review this JTBD transcript", "check this interview", "interview quality"
- "is this job statement valid", "review the synthesis", "check the job statement"
- "Four Forces coverage", "did we get all four forces", "were the forces elicited"
- "can we use this for product decisions", "is this ready to use"
- "critique the interview", "assess the interview quality"
- "independent quality score", "check the interviewer's score"

---

## Use When

- A JTBD switching-story transcript is complete and needs verification before product team use
- You want an independent Quality Score to compare against the interviewer's self-assessment
- You need to know whether gaps require a targeted follow-up interview before downstream use
- You suspect the job statement may not be grounded in the transcript evidence
- You want to check for leading questions, affirmations, or premature closure before presenting findings to stakeholders

---

## Do Not Use When

- The interview is still in progress — use `jtbd-interviewer` to conduct the interview first
- You want to review published research or academic JTBD findings — use `research-critic`
- You want to review a formal study protocol — use `study-design-planner`
- You want to draft copy or messaging from the job statement — use `copy-planner` (after this critic approves the synthesis)

---

## What You Get

- **VERDICT**: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT
- **Four Forces Coverage table**: Status (ELICITED/PARTIAL/UNELICITED), confidence, key quote, and caveats per force
- **Job Statement Validity**: Ulwick syntax check, solution-agnosticism, evidence grounding, revised statement if needed
- **Interviewer Technique Assessment**: Affirmations, leading questions, specificity anchoring, contradiction probing, self-score accuracy
- **Independent Quality Score** (1–5) compared to the interviewer's self-reported score
- **Actionable fix recommendations**: Specific follow-up questions for each gap

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Need to conduct the interview first | Use `jtbd-interviewer` |
| Transcript complete — verify before product decisions | This skill |
| Synthesis ACCEPTED — write product messaging | Route to `copy-planner` |
| Synthesis ACCEPTED — quantitative validation | Route to `study-design-planner` |
| Synthesis needs follow-up interview | Use `jtbd-interviewer` with targeted gap-fill questions from this critic's findings |
| Published JTBD research to review | Use `research-critic` |

---

## Background

JTBD interviews produce synthesis artifacts (job statements, Four Forces summaries, struggling moments) that downstream product decisions depend on. A job statement that sounds compelling but isn't grounded in direct participant evidence can misdirect product work for months. This critic provides an independent check before that happens.

**Key concerns this critic addresses:**
- F3 Anxiety and F4 Habit are systematically underprobed — they are the most uncomfortable forces for participants to discuss and the most important for predicting adoption friction
- Interviewers self-report Quality Scores that are often inflated by 1–2 points — an independent score catches this before the synthesis reaches a product team
- Leading questions and affirmations are subtle — they do not always feel wrong in the moment, but they corrupt the data by steering participant responses toward the interviewer's expectations

---

## Companion Skills

- **jtbd-interviewer**: Conducts the interview this critic reviews
- **copy-planner**: Use after ACCEPT/ACCEPT-WITH-RESERVATIONS to brief messaging work from the validated job statement
- **study-design-planner**: Use after ACCEPT to design quantitative validation of job hypotheses
- **research-critic**: For formal JTBD research and published studies

---

## meta-router Registry Note

Listed under the **Critics** table (review intent, not discovery intent).
Trigger signals: `interview review, JTBD transcript, job statement valid, Four Forces coverage, interview quality, critique the interview, independent quality score`
