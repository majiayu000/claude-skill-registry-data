---
name: testing
description: Choose proportional evidence for robotics software before claiming it works.
---

# Testing

Test the claim at the cheapest layer that can falsify it.

## Decide whether a test is needed

- Batch coherent changes, then run the smallest relevant existing check. Do
  not test after every edit or repeat passing checks without a relevant change,
  failure, or unresolved uncertainty. A full suite is not the default.
- Inspection can suffice for low-risk prose or straightforward edits. For
  uncertain API usage, inspect installed source, help, or current official docs
  first; use one isolated probe if uncertainty remains, not a new test suite.
- Write a new automated test when it protects a reproduced bug, a risky durable
  contract, or behavior worth repeatedly checking, or when the user requests it.
  A one-off demo does not automatically need a test harness.
- Stop when evidence supports the requested claim. Do not add platform matrices,
  benchmarks, repeated trials, or qualification work to a simple tryout.

## Match evidence to the claim

- When automation is warranted, test pure logic without ROS or a simulator.
- A node or launch claim needs the expected processes and interfaces to appear,
  not merely a successful build.
- Behavior that depends on physics, sensors, timing, or closed-loop control
  needs a deterministic scenario in simulation or on the target robot.
- A learned-policy pipeline smoke proves that data, training, evaluation, and
  metrics connect. A regression claim needs a known checkpoint and a stated
  performance bar.
- Add costlier layers only when the risk or claim requires them. Claim a demo
  worked only after observing its actual behavior; a launch or manual handoff
  alone must be labeled as behavior not yet verified.

Read [ROS2-AND-SIM.md](ROS2-AND-SIM.md) for ROS launch, simulator, map, and
headless-CI concerns. Read [POLICY-EVAL.md](POLICY-EVAL.md) for learned-policy
smokes and regression gates. Tool-specific syntax remains in official docs and
the owning `ros2`, simulator, or `lerobot` skill.

## Keep interaction and handoff lightweight

- Use browser/computer interaction only when the relevant visual or interaction
  behavior cannot be established more cheaply, a suspected UI bug needs it,
  or the user asks you to look. Prefer existing CLI, API, logs, and focused
  checks for nonvisual claims; do not tour every screen after each change.
- For low-risk visual acceptance or checks requiring the user's environment
  or access, hand off one short manual check: exact command or URL, expected
  result, and what remains unverified. Do not claim that the user has run it.
- Do not defer safety-critical evidence needed before physical motion,
  destructive actions, security-sensitive changes, or paid resource use merely
  to save testing time. Verify the affected boundary or stop before that action;
  testing never substitutes for authorization.

## Make the result trustworthy

- Seed controllable randomness, use simulation time consistently, bound the
  run, and record the fixture and environment that produced the result.
- Assert observable behavior and interfaces, not duplicated configuration
  literals or log wording.
- When checking camera/render correctness or a suspected blank viewer, inspect
  a frame for meaningful content. Non-black mean and non-flat variance are
  cheap blank-frame guards, not proof of the correct scene. HTTP success and a
  “camera ready” status can both pass while the viewer is blank.
- Guard measurement tools against an empty run. Exiting successfully after
  measuring zero devices or episodes is a test-harness failure.
- Keep benchmarks and long evaluations outside the default suite unless their
  cost is justified on every change.
- Use `test-assets` when fixtures, worlds, datasets, recordings, or goldens need
  provenance and maintenance rules.

If a suite is flaky, slow, green without useful evidence, or fails only on a
particular runner, read [FAILURES.md](FAILURES.md).

## Keep remote cost proportional

- Run the same pipeline locally at tiny scale before any paid remote test.
- Before deploying or spending on changed allocation, isolation, cancellation,
  or cleanup behavior, verify the affected lifecycle boundaries in the local
  fake deployment first. Rebuild its image when its inputs change; a stale
  digest does not test the change. Do not rerun this for unrelated edits.
- Keep GPU- or hardware-dependent tests explicit and schedulable; do not make a
  default CI job depend on unavailable hardware.
- A remote success should preserve the exact image, model, data, seed,
  hardware, result, and cost window needed to understand the claim.

## Done

- Report the evidence obtained and any explicitly deferred manual checks.
- A robotics app's smoke exercises the behavior it exists to demonstrate, not
  only process health.
- CI runs the stable, affordable evidence by default and clearly separates
  slow, paid, hardware, and manual checks.
