---
name: dev-calibrate
description: >-
  Playbook for correcting a named skill's star level to match its computed Trust
  Magnitude grade, with an independent post-calibration verification pass and a
  CLI-logged timeline event (never hand-written). Use when: recalibrating a
  skill's level, fixing a stale or drifted star rating, running a batch of
  `gaia dev calibrate` corrections, or confirming a past calibration actually
  landed. Triggers: "calibrate <skill>", "recalibrate the trust magnitude
  backlog", "promote/demote <skill> to N stars", "why is <skill> still N stars",
  "verify a calibration actually landed", "Hall of Heroes ranking is wrong".
playbookVersion: 1
class: B
objective: >-
  Take one named skill whose stored star level has drifted from its computed
  Trust Magnitude grade, and land it at the correct level with pre-flight,
  decision, and independent post-calibration verification all provable — not
  merely asserted by the calibrate command's own stdout.
capability: >-
  Reading a Trust Magnitude leaderboard row against a skill's current stored
  star level, deciding whether the gap is a real promotion or demotion versus a
  case the CLI's pre-flight should legitimately block (missing verified
  links.github, zero evidence), applying the correction through the canonical
  CLI verb, and re-inspecting the same skill afterward to confirm the mutation
  actually took.
preconditions:
  - the target skill_id exists as a named skill under registry/named/<contributor>/<name>.md
  - gaia whoami resolves to verifier, override, or bootstrap, not denied
  - the working tree is on a review/meta/* or dev/* branch, never main
  - the active gaia is this repo's source, not a stale pipx install (compare `python3 -m gaia_cli.main --version` to the version in pyproject.toml)
steps:
  - id: snapshot-target
    run: python3 scripts/inspectTrustMagnitude.py --skill {skill_id}
    proves: current stored level, computed trustMagnitude, and overallTrustGrade are captured for skill_id
  - id: decide
    judgment: PROMOTE | DEMOTE | NO_CHANGE | BLOCKED_MISSING_EVIDENCE
    rules: >-
      Target level is the G7 star mapping of overallTrustGrade (S=5★, A=4★,
      B=3★, C=2★, ungraded=1★), held at the skill's historical rank floor
      (§10.10) if it previously reached 4★+. NO_CHANGE when current level already
      matches the mapping. BLOCKED_MISSING_EVIDENCE when the skill has zero
      evidence rows and zero suiteComponents driving its Trust Magnitude — the
      grade is not a real signal to act on until evidence is sourced.
  - id: calibrate
    run: gaia dev calibrate {skill_id} {target_level} --no-build
    proves: level frontmatter updated and a rank_up or demote timeline event appended automatically by the CLI — never hand-write this event
  - id: verify-landed
    run: python3 scripts/inspectTrustMagnitude.py --skill {skill_id}
    proves: re-inspected stored level equals decide's target_level — confirmed against live state, not trusted from calibrate's own stdout
  - id: relabel-dependent-origins
    judgment: RELABEL_APEX_ORIGINS | NO_DEPENDENT_ORIGINS
    rules: >-
      Find every named skill whose fusion-recipe.origins or suiteComponents
      includes skill_id. Re-run origin-grade resolution and re-inspect any Apex
      Gate predicate state that depends on graded-origin counts. Land any
      resulting calibration change through gaia dev calibrate (never hand-edit
      an origin label or Apex predicate).
  - id: rebuild-docs
    run: gaia dev docs
    proves: Class S artifacts (docs/graph/*, docs/api/v1/*) regenerated to reflect the new level
  - id: verify-docs-clean
    run: python3 scripts/build_docs.py --check
    proves: exit 0 — the committed artifact set has no undeclared drift beyond the documented warn-only categories
stopConditions:
  - decide resolves BLOCKED_MISSING_EVIDENCE — land in the review packet for sourced-evidence follow-up, do not force a level change
  - the calibrate step's pre-flight rejects the target (missing verified links.github blob for a 3★+ promotion) — land in the review packet, the fix is evidence work, not a retry
  - verify-landed shows the stored level still does not equal target_level after calibrate ran clean — escalate to the founder queue, do not re-run blindly
proof:
  - snapshot-target and verify-landed both ran, and verify-landed's stored level equals decide's target_level
  - the skill's frontmatter timeline carries a rank_up or demote event for this change, logged by the CLI, never hand-written
  - build_docs.py --check exits 0 after rebuild-docs
done: >-
  skill_id's stored level matches its computed Trust Magnitude grade under the
  G7 mapping, the change is provable from a re-inspection run after calibrate
  (not from calibrate's own stdout), the timeline carries the CLI-logged event,
  and Class S docs are regenerated and clean.
---

## Overview

This playbook corrects a named skill's stored star level when it has drifted from
its computed Trust Magnitude grade. The objective is not just to run
`gaia dev calibrate` — it is to make the correction *provable*: a pre-flight
snapshot, an explicit promote/demote/no-change/blocked decision against the G7
mapping, the CLI-driven mutation itself (which alone appends the timeline event —
never hand-write it), and an independent re-inspection afterward that confirms the
stored level actually changed, rather than trusting the calibrate command's own
stdout.

## Batch use

For a backlog of N skills, repeat `snapshot-target` through `verify-landed` once
per `skill_id`. `rebuild-docs` and `verify-docs-clean` are expensive registry-wide
rebuilds — run them once at the end of the batch, not after every individual
skill. This is an efficiency note only; it does not change the per-skill spine or
its proof obligations.

## Reference

- `founder/steward/PLAYBOOKS.md` — the playbook contract this file opts into.
- `python3 scripts/inspectTrustMagnitude.py --leaderboard` — finds calibration
  candidates in bulk by ranking all named skills by Trust Magnitude.
