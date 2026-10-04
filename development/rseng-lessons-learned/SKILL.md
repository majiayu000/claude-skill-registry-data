---
name: rseng-lessons-learned
description: >-
  Covers capturing and reusing what a project learns: a lessons-learned record
  fed from debugging sessions, code review findings, failed and successful
  research approaches, incidents and near-misses; blameless postmortems for
  the big ones; retrospectives on a cadence; and routing each lesson into the
  artifact that prevents its repetition (test, doc, checklist, onboarding
  note). Use PROACTIVELY when a nontrivial bug is fixed, a review uncovers a
  recurring pattern, an approach is abandoned, or an incident is resolved -
  and when the user asks to record a lesson, run a retrospective or
  postmortem, wants a LESSONS or NOTES file, or asks why the same mistake
  keeps happening.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Lessons learned and project memory

Every project pays tuition - the bug that took three days, the
approach that silently failed, the review comment made for the
fourth time. The tuition is only wasted if the lesson evaporates.
This skill is the capture mechanism: write the lesson down at the
moment it is learned, in the repository, and then - the step most
teams skip - route it into an artifact that makes repetition
impossible. A lessons file nobody acts on is a diary; a lesson
that became a test is institutional memory.

## Capture at the trigger moments

The lesson is freshest and cheapest at the moment of resolution.
Capture proactively - offer, in one line, to record it - when:

- A nontrivial bug is fixed: what the symptom was, what the cause
  turned out to be, what evidence found it, what would have
  prevented it (rseng-debugging's evidence trail is the draft).
- A code review surfaces a recurring pattern: the third time the
  same class of comment appears, it is a lesson (and a candidate
  lint rule or checklist line - rseng-pair-programming).
- A research approach is abandoned: WHY it lost - data, method,
  numerics, scaling - so the next person (or the same person,
  next year) does not re-walk the dead end. Negative results are
  project knowledge (rseng-software-reuse records reuse decisions
  the same way).
- An incident or near-miss resolves: data almost lost, wrong
  results almost published, credential exposed - these get the
  fuller postmortem below.
- Something WORKED surprisingly well: lessons are not only
  failures; a practice worth repeating is worth recording.

## The record: small, structured, in the repo

- One file, versioned with the code (LESSONS.md or docs/lessons/):
  dated entries, newest first; each entry a few lines - context,
  what happened, the lesson, and the action taken. Searchability
  beats elegance; write plainly.
- Tag entries by theme (numerics, data handling, process,
  dependency...) so patterns become visible when three entries
  share a tag - a themed cluster is a systemic issue asking for a
  systemic fix.
- Personal research notes scale down the same way: a dated
  notebook of decisions and observations per analysis
  (rseng-notebooks' narrative side) - the lab-notebook habit
  applied to computation.
- Keep it honest and blame-free in wording: lessons name causes
  and defenses, never culprits - a record people fear lands in
  performance reviews stops being written
  (rseng-honesty's blame-free framing; rseng-ai-declaration records
  agent-contributed lessons like any other).

## Postmortems and retrospectives

- Blameless postmortem for the big ones (the SRE practice
  transfers whole): timeline of what happened, contributing
  causes (plural - single-cause stories are usually wrong),
  what limited or worsened the impact, and concrete prevention
  actions WITH owners in the tracker
  (rseng-project-tracking). Blameless is the load-bearing word:
  the goal is that the next person in the same position, with
  the same information, does better - not that someone is sorry.
- Retrospectives on a cadence: at milestones or each planning
  cycle, three questions - keep doing, stop doing, start doing -
  fed by the lessons file since last time (structured formats
  and exercises exist when a team wants variety). Fifteen
  minutes is enough; skipping it is how the lessons file goes
  stale.

## Route the lesson into an artifact

The closing discipline - every lesson ends with "and therefore",
picking the artifact that prevents repetition:

- A bug lesson becomes a regression test (rseng-testing) or a
  defensive check (rseng-defensive-coding).
- A review-pattern lesson becomes a lint rule (rseng-code-quality),
  a checklist line, or a PR-template question.
- A process lesson becomes a tracker template or a cadence change
  (rseng-project-tracking).
- A gotcha lesson becomes a documentation warning
  (rseng-documentation) or an onboarding note - the future
  colleague reads the lesson where they will hit the problem,
  not in an archive.
- A dead-end lesson becomes a paragraph in the methods notes or
  the decision log, so the paper and the successors know what
  was tried (rseng-research-integrity values the recorded
  negative).

An agent applying this skill closes the loop in one motion:
record the lesson AND draft the artifact, then offer both.

## Working with this skill

This skill is source-independent: it adapts blameless-postmortem
and retrospective practice to research software work. It is fed
by rseng-debugging, rseng-pair-programming and rseng-project-tracking,
and it feeds rseng-testing, rseng-documentation and rseng-trainer
(lessons are tomorrow's teaching material).

Learn more (verified):
  - https://sre.google/sre-book/postmortem-culture/ - blameless
    postmortem culture (Google SRE book)
  - https://retromat.org - retrospective formats


Recorded lessons are raw material for the project's build story
(rseng-trainer): the mistakes worth learning from belong in the
teaching document, not only the log.

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-code-quality - review-pattern lessons become lint rules
- rseng-debugging - bug fix evidence drafts the lesson
- rseng-documentation - gotcha lessons become doc warnings
- rseng-project-tracking - postmortem actions get tracked owners
- rseng-testing - bug lessons become regression tests
- rseng-trainer - lessons become tomorrow's teaching material

<!-- related-skills:end -->
