---
name: isaac-lab
description: Train, imitate, evaluate, and deploy robot policies with NVIDIA Isaac Lab.
---

# Isaac Lab

Isaac Lab adds a training loop to a matched Isaac Sim runtime. Prove a shipped
task end to end before creating a robot, environment, or reward.

## Establish the runtime

- Inherit the current hardware and operating-system gate from Isaac Sim.
- Verify the supported Isaac Sim and Isaac Lab pairing; newest plus newest is
  not automatically compatible.
- Prefer NVIDIA's matched Isaac Lab image on a cloud GPU. Use a source install
  when the workstation and version pairing are intentionally maintained.
- List registered tasks from the installed release instead of guessing a task
  ID or script path from an older tutorial.

## Prove the policy loop

- Choose the learning path explicitly: reinforcement learning from rewards, or
  imitation learning from demonstrations and generated variants.
- Run a known task headless with few environments and few iterations.
- Verify environment reset, observation/action shapes, reward terms, logging,
  and checkpoint creation before scaling parallel environments.
- Locate outputs using the training library's experiment name and current
  configuration, not an assumed task-name directory.
- Evaluate a named checkpoint through the matching play script. Export only
  after its observed behavior and metrics are useful.
- Add or change one reward, termination, terrain, or robot dimension at a time;
  a larger batch of edits hides which contract broke.

## Go deeper only when needed

- For NVIDIA's prebuilt image on RunPod, read
  [references/prebuilt-image-runpod.md](references/prebuilt-image-runpod.md)
  after the cloud provider is chosen.
- For the measured Unitree Go2 RSL-RL workflow, rewards, checkpoints, and custom
  task route, read [references/go2-rl-workflow.md](references/go2-rl-workflow.md).
- For teleoperation, Mimic/robomimic imitation learning, export, sim-to-sim, or
  hardware deployment, read
  [IMITATION-AND-DEPLOYMENT.md](IMITATION-AND-DEPLOYMENT.md).
- For runtime, output, task-registry, or interactive-viewer symptoms, start with
  [FAILURES.md](FAILURES.md).
- Use the current [Isaac Lab documentation](https://isaac-sim.github.io/IsaacLab/)
  and [source](https://github.com/isaac-sim/IsaacLab) for task IDs, script paths,
  configuration, and export behavior.
- Isaac Sim owns the underlying scene and sensors. LeRobot owns
  LeRobot-format dataset and real-robot training workflows; data owns the
  simulation-versus-real sourcing decision.

## Done

- A small shipped task trains, writes a discoverable checkpoint, plays back
  through the matching runtime, and provides a measured baseline for any custom
  task or scaled run.
