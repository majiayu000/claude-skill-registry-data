---
name: q2010-plan
description: "Produce the off-the-shelf utilisation plan of ECSS-Q-ST-20-10C clause 5.1.1 against its Annex A DRD and grade the draft before it is issued: report an absent DRD section apart from one present with no content, require every listed candidate to carry an attributed evaluation, compare each evaluation completion with the day its result is needed ahead of the procurement commitment, and require each declared interface to name two distinct parties and a defined exchange. Use when the plan is being drafted, reviewed or refused at issue. Trigger: ecss, q-st-20-10c, ots-plan-drd, ots-candidate-evaluation-schedule, ots-plan-responsibilities, ots-interface-two-sided, ots-evaluation-need-date."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, q-st-20-10-ots-item-scope, q2010-plan, ots-plan-drd, ots-candidate-evaluation-schedule, ots-plan-responsibilities, ots-interface-two-sided, ots-evaluation-need-date]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Off-The-Shelf Items -- Utilisation Plan (space-systems/ecss/q2010-plan)

Use when the task is the off-the-shelf plan of ECSS-Q-ST-20-10C clause
5.1.1: the Annex A DRD says what the plan carries, and the question is
whether the draft in front of you can be issued or has to go back for
the candidates, the evaluation schedule, the responsibilities or the
interfaces.

## Domain quick reference

- A missing section and an empty section are different defects. The
  first says the author has not reached that part of the plan; the
  second usually says a template was filled in around a section nobody
  owns. Reporting them together sends both to the same person, and only
  one of them is the author.
- An evaluation has a date it is needed by, not just a date it happens
  on. The result exists to inform a procurement commitment, so the
  useful comparison is completion against the commitment day less the
  agreed decision lead. An evaluation finishing after that day produces
  a report about a decision already taken.
- Every candidate owes an evaluation, and every evaluation owes a name.
  A schedule entry with no responsible role is a date in a plan that
  nobody has agreed to meet, which is why the role is graded against the
  set of parties that can actually carry one.
- An interface has two sides by definition. One named party and a
  defined exchange is a statement of intent; two distinct parties is an
  interface, and repeating the same party twice does not make a second
  side.
- A candidate with no declared interface is a question, not a defect.
  Some items really are drop-in, so it stays advisory and visible rather
  than blocking a plan that is otherwise ready to issue.

## Workflow

1. Normalise the drafted sections against the DRD list, refusing a
   section the DRD does not have and a section drafted twice.
2. Normalise the candidate list with each candidate's procurement
   commitment day.
3. Normalise the evaluation schedule, refusing a duplicate entry and a
   responsible role outside the recognised set, and keeping an
   unattributed evaluation so it can be reported.
4. Normalise the interfaces, collapsing a repeated party and refusing an
   exchange kind the plan cannot mean.
5. Grade the sections, then the schedule against the need days, then the
   interfaces, separating what blocks issue from what is advisory.
6. Return the section completeness, the evaluation coverage over the
   candidates and the decision: issuable, issuable with actions, or not
   issuable.

## Pitfalls

- Grading the plan on section presence alone. A complete set of headings
  with an empty responsibilities section reads as a full plan in any
  table of contents check.
- Comparing an evaluation with the commitment day itself. The decision
  lead is the whole point: the result has to be in hand early enough to
  change the decision.
- Accepting an evaluation whose owner is the project generally. A plan
  is issued so that named parties can be held to dates, and an
  unattributed date is the first one to slip.
- Counting a one-sided interface as declared. The second party is the
  one who has to agree, and the plan is where that is recorded.
- Blocking on a candidate with no interface. Treating an open question
  as a defect pushes authors to invent an interface rather than say
  there is not one yet.

## Behavior contract (gate 3)

The DRD section grading with its missing and empty split, the candidate
and evaluation normalisation, the responsible-role vocabulary, the need
day computed from the commitment day and the decision lead, the
two-sided interface rule and the completeness fractions driving the
issue decision are exercised by the gate 3 contract test:
scripts/test_q2010_plan.py against scripts/q2010_plan_logic.py (stdlib
unittest, offline). Run: python3 scripts/test_q2010_plan.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
