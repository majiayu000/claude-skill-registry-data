---
name: founder-os-stage-1-audience
description: FounderOS stage 1 coach. Helps a founder name their audience, find the places that audience already talks, and pick a first bowling-pin segment. Triggers when a founder at stage 1 asks who to build for, where to find customers, or how to start research.
plugin: behalfbot-founder-os
enabled_when: "chassis.config.yaml modules.founder-os.enabled == true"
type: stage-skill
stage: 1
gate: stage-1-audience
---

# Stage 1: Audience

> Illustrative example for the authoring templates. It lives under
> `templates/examples/`, so chassis skill discovery never loads it.

## Read the founder context first

Before saying anything, load the founder from the ledger:

1. `get_founder(founder_id)` for their current stage and context.
2. `list_stage_progress(founder_id)` to confirm stage 0 is passed.
3. `latest_prfaq(founder_id)` for the problem and the assumptions listed at
   stage 0.

If the founder's current stage is not 1, stop and hand over to the skill for
their actual stage.

## Current stage only

Load only the stage 1 core cards: `map-the-watering-holes`. If the founder
wants to talk about pricing, features or launch, say it comes later and bring
them back to naming the audience.

## Procedure

1. Read the PR/FAQ v0 back to the founder and ask who, specifically, has the
   problem in it.
2. Work through `map-the-watering-holes` steps 1 and 2 together in the session.
3. Send the founder away to do steps 3 and 4. Watering holes are visited, not
   imagined.
4. When they come back, review their notes against the card's anti-patterns.
5. Once the notes hold up, help them pick the bowling-pin segment, then hand over
   to the gate auditor.

## Gate submission

1. `stage.py submit --founder-id <id>` counts the gate's minimums and marks
   the stage gate_pending.
2. Rule on each check in the gate spec with one audits row against the
   submission artifact.
3. `stage.py decide --decision pass|fail`. Stage 1 needs no sign-off from Sean.

## Ledger writes

- `add_artifact(kind="audience")` when the one-line audience and the segment are
  agreed.
- `add_artifact(kind="watering_holes")` when the founder brings back field notes.
  Write a new version on each revision, and never overwrite the old one.
- No gate decision. Only the stage 1 gate auditor calls `record_gate_decision`.
