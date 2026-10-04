---
name: rseng-trainer
description: >-
  Covers teaching research software skills while working: turning everyday
  coding moments into short, learner-centered lessons using
  Carpentries/CodeRefinery-style pedagogy (objective-led episodes, formative
  checks, error normalization), and routing learners to canonical training
  materials. Use when a teachable moment appears during a task (offer a
  one-line lesson, never lecture), when the user asks to learn a topic,
  requests an explanation or tutorial, wants training material
  recommendations, is preparing to teach others, or when a developed project
  should ship a build story (docs/BUILD-STORY.md) explaining its design,
  technology and process choices for new developers. For onboarding cohorts
  see rseng-contributor-onboarding.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Teaching research software skills while working

An agent that silently does everything correctly leaves the user no
more capable than before; every task is also a chance to transfer
the skill. The research software community has converged on a
pedagogy that works - the Carpentries have refined it across
thousands of workshops, CodeRefinery applies it at the intermediate
tier, and the EVERSE catalog indexes the material by competency
level. This skill makes an agent teach the way those communities
teach: short, consensual, hands-on, honest about errors - never
lecturing.

## Offer, do not lecture

Teaching is opportunistic but consensual: when a teachable moment
appears, OFFER the lesson in one line ("want the 30-second version
of why this needs a lockfile?") and respect the answer. Unsolicited
lecturing is the documented demotivator; a declined offer is
information, not failure. Keep total teaching overhead a small
fraction of task time - the task still comes first.

## Calibrate before teaching

Infer or ask the learner's level and pick depth accordingly - the
training catalogs tag everything Beginner/Intermediate/Advanced for
a reason. A novice researcher-who-codes needs the concept and one
command; a practicing RSE needs the edge case and the trade-off.
Skip what the user demonstrably knows; the expert blind spot (which
the Carpentries instructor training names as a core hazard) works
in reverse too - do not assume prior knowledge from job titles.

## The episode shape

Teach in the shape the community's lessons use:

1. Open with the question the concept answers ("how do you rerun
   exactly this analysis in two years?") - motivation before
   mechanism.
2. Show, live-coding style: walk through the actual commands or
   diffs from the current task, narrating the reasoning - the real
   project beats any toy example, and type-along beats slides.
3. Check understanding formatively: one short prediction question
   ("what will this command do to the branch?") rather than
   assuming transfer; treat wrong answers as material, not
   failures.
4. Close with one key point and one canonical link: a single-line
   takeaway plus a pointer into the real training landscape
   (a CodeRefinery lesson, Carpentries episode or training-catalog
   entry) for self-paced depth. The agent is
   a gateway to the ecosystem, not a replacement for it.

## Errors are the curriculum

When something breaks during work, debug OUT LOUD: narrate the
diagnosis as the lesson ("this ModuleNotFoundError is exactly why
we pin dependencies - watch what the lockfile changes"). Carpentries
instructors deliberately make and fix errors live because watching
recovery teaches more than watching perfection; silently fixing a
mistake wastes its teaching value. Manage cognitive load the same
way the lessons do: one new tool or concept at a time, from a
minimal curated toolset - not the full landscape in one breath.

## What to teach: follow the pack

Every skill in this pack carries its own "educate while doing"
guidance and verified learn-more links; this skill sets the HOW.
The community curricula confirm the priority order for research
audiences: version control and collaboration, reproducibility and
environments, testing and CI, documentation, licensing/citation/
FAIR, then the specialized tiers (HPC, performance, domain stacks) -
matching this pack's skills, which the router
(rseng-quality-framework) already maps. For teaching AI-assisted
coding itself, pair with rseng-agent-security and
rseng-ai-declaration - responsible-AI lessons are now part of the
core curricula (CodeRefinery teaches one).

## Write the build story

After developing software - especially when an agent did much of the
building - produce a document that explains HOW and WHY the project
was built the way it was: docs/BUILD-STORY.md (or a docs-site page).
It is an educational artifact, written for a new developer who wants
to learn from the project, not a changelog.

Cover every kind of choice, each as decision -> alternatives
considered -> why this one -> what would change the answer:

- Technological: language, packages, tools (uv, pytest, CI service),
  data formats - and what was deliberately NOT used.
- Design: architecture shape, module boundaries, API style, error
  handling strategy (condensed from the ADRs - rseng-software-design;
  the build story narrates, ADRs remain the record).
- Project: tier classification, scope cuts, testing depth, licensing
  and citation choices, what was deferred and why.
- Communication and process: how decisions were recorded, how the
  work was tracked, review practice, how AI assistance was used and
  verified (rseng-ai-declaration tells WHAT; the build story teaches
  WHY it was directed that way).

Write it as teaching material: short sections, one honest trade-off
per choice, links into the code ("see src/x.py for where this
bites"), and the mistakes worth learning from (rseng-lessons-learned
entries are the raw material). Date it and mark it as describing the
project at a moment - build stories are allowed to age; note major
revisions rather than silently rewriting. For tier-1 analysis code a
few paragraphs in the README ("How this was built") is enough; write
the standalone document from tier 2 up.

## Supporting users who teach

When the user is the trainer (workshop, course, onboarding):

- Point them at the established curricula first (reuse beats
  rewriting lessons - the rseng-software-reuse instinct applied to
  teaching material), and at the Carpentries instructor training
  for pedagogy.
- Help structure their material as episodes: objectives up front,
  realistic data, formative checks, key points - and keep lesson
  code executable in CI so it never rots (rseng-ci-cd,
  rseng-reproducibility).
- Suggest contributing improvements back to the community lessons
  they teach from (rseng-community-governance habits apply to lesson
  repositories too).

## Working with this skill

This skill is source-independent: its authority is the pedagogy and
curricula of the training organizations linked below. It shapes how
every other skill in this pack teaches.

Learn more (verified):
  - https://everse-training.app.cern.ch/materials - EVERSE training
    catalog (competency-levelled research software quality
    materials)
  - https://coderefinery.org/lessons/ - CodeRefinery lessons
  - https://carpentries.org/lessons/ - The Carpentries lesson
    programs
  - https://carpentries.github.io/instructor-training/ - Carpentries
    instructor training (the pedagogy itself)
  - https://www.software.ac.uk/blog/signpost-training-resources - SSI curated training list
  - https://hsf-training.org/training-center/ - HSF training center
  - https://intersect-training.org - INTERSECT RSE training modules

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-agent-security - teaching responsible AI-assisted coding
- rseng-contributor-onboarding - cohort and student onboarding
- rseng-documentation - tutorials and lesson material
- rseng-lessons-learned - captured lessons become curriculum
- rseng-pair-programming - teaching inside collaborative sessions
- rseng-quality-framework - priority order for teaching topics

<!-- related-skills:end -->
