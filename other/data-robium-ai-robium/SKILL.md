---
name: data
description: Choose and structure training data for robot-learning projects.
---

# Data

Begin with coverage: decide what behavior, embodiment, and conditions the
policy must see before deciding how to collect them.

## Choose the source

- Search existing datasets first. Confirm task, action space, degrees of
  freedom, gripper, cameras, state features, timing, license, and provenance.
- Use an exact embodiment match directly. Treat a near match as pretraining or
  co-training material, not a drop-in dataset.
- When schemas and task labels cannot distinguish two environments, compare a
  deterministic scene observation from the dataset with the pinned target
  environment. Prefer a stable reference camera over a randomized wrist view.
- Generate in simulation when scale, controlled variation, or labels matter
  more than perfect realism.
- If a documented search finds no dataset for the exact scene and control
  contract, generate demonstrations in the pinned application environment and
  retain only episodes that satisfy its success condition.
- Collect on the real robot when contact, appearance, or hardware behavior is
  difficult to reproduce faithfully.
- Mix sources deliberately: simulation can provide coverage; a smaller real
  set can expose the remaining sim-to-real gap.

## Protect the useful signal

- Constrain the task and workspace before adding more episodes. Dense coverage
  of the behavior matters more than a large headline episode count.
- For a successful-expert imitation dataset, keep only demonstrations that meet
  the task's success definition. Retry or discard oracle failures, and stop
  loudly if the success rate collapses. Do not apply this rule to DAgger,
  corrective, recovery, or failure-learning datasets that intentionally retain
  non-expert transitions.
- Define the episode boundary, observations, actions, rates, success label,
  splits, and target storage format before collection starts.
- Record the source revision and collection conditions. Dataset facts and
  licenses must come from the current card or repository, not memory.

## Go deeper only when needed

- For the Robium evidence behind workspace density and demonstration quality,
  read [COLLECTION-QUALITY.md](COLLECTION-QUALITY.md).
- Use Hugging Face guidance only when the decision reaches Hub discovery,
  inspection, transfer, or publication.
- Use LeRobot guidance when the decision reaches LeRobotDataset recording,
  editing, training, evaluation, or platform-specific teleoperation controls.
- Use simulator guidance only after choosing simulation as a source; Isaac Sim
  and Gazebo own their generation mechanics.
- Test fixtures belong to test-assets, not this training-data decision.

## Done

- The chosen sources cover the target embodiment and task, the gaps are named,
  and the first small collection or dataset slice can validate the plan before
  scale or paid compute.
