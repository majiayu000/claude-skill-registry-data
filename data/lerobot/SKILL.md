---
name: lerobot
description: Build and debug LeRobot datasets, training, and policy evaluation. For a first pretrained robot-arm demo, start with architect's reference-app selection.
---

# LeRobot

Follow one contract chain through LeRobot: embodiment, dataset, processor,
checkpoint, runtime observations and actions, then evaluation. Find the first
contract that does not match.

## Establish the contract

- For a new manipulation app or first pretrained-policy demo, read
  [architect](../architect/SKILL.md) before creating an environment or training
  pipeline. It finds the saved apps checkout and selects a compatible baseline.
  If selection already happened, continue here. Existing dataset, training,
  or evaluation work does not need onboarding; an inference-only request does
  not authorize training.
- Inspect the installed LeRobot version and current CLI help before writing
  flags. Dataset formats, policy families, scripts, and extras change quickly.
- Match the robot's state, action space, cameras, rates, and task to the
  dataset. A policy adapts to those features; it cannot repair a mismatched
  embodiment.
- Inspect every checkpoint's configuration and processor files, not only its
  weights. Base and fine-tuned checkpoints from one family can expect different
  camera layouts.
- Keep Hub identity, transfer, publication, and Jobs lifecycle at the Hugging
  Face boundary. Keep source-selection strategy in data.

## Prove the loop cheaply

- Start with a small shipped policy and a known dataset/environment pair.
- Run a short train that writes a checkpoint, then load that exact checkpoint
  through evaluation. Completion and numeric metrics are the smoke-test result;
  policy quality is not.
- Confirm loss, saved processors, input/output shapes, rollout metrics, and
  video or real-robot behavior before increasing steps or hardware cost.
- Treat real-hardware rollout as a new safety boundary even when simulation
  evaluation passed.

## Go deeper only when needed

- For loading, recording, editing, migration, and episode visualization, read
  [references/datasets.md](references/datasets.md).
- For policy choice, camera remapping, training, compute sizing, and remote
  Jobs behavior, read
  [references/policies-and-training.md](references/policies-and-training.md).
- For simulation evaluation, headless rendering, EnvHub, or real-hardware
  rollout, read [references/eval-and-sim.md](references/eval-and-sim.md).
- When a checkpoint, feature contract, evaluation worker, dependency, or remote
  run fails, start with [FAILURES.md](FAILURES.md).
- The concrete PushT examples are useful only when that smoke path matches the
  application: [load dataset](examples/load-dataset-snippet.py) and
  [train ACT](examples/train-act-command.md).
- Use the current [LeRobot documentation](https://huggingface.co/docs/lerobot)
  and [source](https://github.com/huggingface/lerobot) for version-sensitive
  APIs and the shipped policy/environment list.

## Done

- The target dataset loads, the checkpoint carries its processors, evaluation
  exercises matching observations and actions, and measured results justify
  any longer run or hardware deployment.
