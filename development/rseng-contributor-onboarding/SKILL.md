---
name: rseng-contributor-onboarding
description: >-
  Covers turning users into contributors and contributors into regulars:
  curating genuinely good first issues, onboarding paths and checklists
  generated from the repository, first-PR shepherding, mentorship and buddy
  structures, and measuring where the contribution funnel leaks. Use when a
  project wants contributors but gets none, when first-time contributors do
  not return, when the user asks for good-first-issue curation, onboarding
  documentation or mentorship structure, or when a team member or student is
  joining a research software project.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Contributor onboarding

Contributors are made, not found: someone used the software, hit
an edge, and the project either made the path from "I could fix
this" to a merged PR walkable - or it did not. Onboarding is
engineering that path deliberately, for external contributors
and equally for the new student or teammate joining the project
(the same path, walked faster). The funnel framing keeps it
honest: user -> first contact -> first contribution -> second
contribution -> regular; each transition can be measured
(rseng-community-metrics) and fixed.

## Good first issues: curation, not labeling

A good first issue is a real, wanted task that is genuinely
doable without tribal knowledge - and the label is a promise:

- Curate each one: state the problem, point at the relevant
  files, sketch the approach, name the definition of done and
  the test to add (rseng-testing) - fifteen minutes of curation
  per issue, repaid by every newcomer it serves. An agent can
  draft these from the backlog well (rseng-project-tracking).
- Keep the shelf stocked and fresh: a handful available, claimed
  ones released after inactivity, solved ones replaced -
  an empty or stale good-first-issue shelf tells newcomers the
  invitation was decoration (directories like goodfirstissue.dev
  index the label; being indexed with stale issues hurts).
- Non-code first issues count: docs gaps, example datasets,
  FAQ entries (rseng-user-support's pipeline generates them
  naturally) - often the truest first contribution for research
  audiences.

## The walkable path

- The onboarding trail is testable: CONTRIBUTING.md's setup
  steps (rseng-community-governance) run cleanly from a fresh
  clone - verify it the clean-room way (rseng-reproducibility)
  and keep it verified in CI where feasible; a broken dev-setup
  step loses more contributors than any hard bug.
- Generate the project-specific onboarding checklist from the
  repository: where things live (architecture notes -
  rseng-software-design's ADRs), how to run tests, how review
  works, who to ask what - the knowledge-transfer document that
  also cuts the bus factor
  (rseng-maintenance-sustainability). For team members, add
  accounts, data access (rseng-regulatory-compliance where
  sensitive) and the project glossary.
- First-PR shepherding: respond fast (the retention predictor -
  rseng-community-metrics), review kindly with the
  first-contribution bar - correctness yes, style nits no
  (rseng-pair-programming's blocking-vs-preference split), and
  land it; a merged small PR beats a perfect stalled one.
  Credit immediately (rseng-citation-metadata's first-merged-PR
  trigger).
- Mentorship structure, sized honestly: a named point of contact
  for a newcomer's first weeks beats a formal program a
  two-person team cannot staff; buddy pairing for cohorts
  (students, sprint attendees - rseng-trainer for the teaching
  craft). First-timer-friendly conventions
  (firsttimersonly.com collects them) set the tone.

## Measure the funnel, fix the leak

Where do people stall? Issues claimed but never PRed (setup or
scoping problem), PRs opened but abandoned (review latency or
harsh feedback), first PRs merged but no second (no next step
offered - suggest one at merge time). The funnel numbers
(rseng-community-metrics) point at the stage; the fix is usually
in this skill or rseng-user-support. Ask leavers when possible -
one honest exit answer outweighs a dashboard.

## Working with this skill

This skill is source-independent: it encodes contributor
onboarding practice for research software. It is the funnel
between rseng-user-support (users with questions) and
rseng-community-governance (contributors with rights), measured by
rseng-community-metrics.

Learn more (verified):
  - https://opensource.guide - open source guides (finding and
    welcoming contributors)
  - https://goodfirstissue.dev - good first issue directory
  - https://www.firsttimersonly.com - first-timers-only
    conventions
  - https://www.cscce.org - CSCCE community engagement

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-community-governance - rules and CONTRIBUTING newcomers follow
- rseng-community-metrics - measures funnel conversion
- rseng-pair-programming - kind first-PR review bar
- rseng-reproducible-environments - fresh-clone dev setup must work
- rseng-trainer - teaching cohorts and students
- rseng-user-support - active answerers become contributors

<!-- related-skills:end -->
