---
name: simulation
description: Choose between Gazebo, Isaac Sim, and MuJoCo and define what the simulation must prove.
---

# Simulation

Choose a simulator for the project's hardest requirement, then define the
evidence that would make its results trustworthy.

## Pick by bottleneck

- For a new robot app or first simulation demo, use
  [architect](../architect/SKILL.md) to check compatible reference apps before
  selecting a fresh stack. Keep a selected example's simulator. Continue here
  when no example fits or simulator choice is the actual unresolved question;
  comparisons and existing simulation work do not need onboarding.
- **Gazebo:** prefer for ROS-centric mobile robots, standard sensor simulation,
  and projects without a confirmed compatible NVIDIA GPU.
- **Isaac Sim:** consider when photorealism, synthetic data at scale, or the
  NVIDIA Isaac stack is central. Confirm the current RTX GPU, driver, OS, and
  VRAM requirements before committing to it; use `gazebo` if that environment
  is not real and available.
- **MuJoCo:** prefer for lightweight, contact-rich manipulation that does not
  need ROS integration or photoreal rendering.
- A project may use different simulators for different concerns. Avoid forcing
  one tool to own both navigation validation and training-data generation.

After selection, use `gazebo`, `isaac-sim`, or `mujoco` for tool mechanics.
Use `isaac-lab` for training workflows on top of Isaac Sim.

## Define fidelity before building

- Name what must transfer to hardware: interfaces, sensor behavior, dynamics,
  contacts, timing, or visual appearance.
- Match real sensor rate, noise, frame names, range, field of view, resolution,
  and timestamp source where those affect downstream decisions.
- Record known model gaps instead of treating simulation success as real-world
  evidence.
- If the simulator will back regression tests, control time step and randomness
  and judge behavior with tolerances rather than pixel-perfect coincidence.

Read [sensor fidelity](SENSOR-FIDELITY.md) when adding sensors, preparing
sim-to-real work, or turning a scenario into a repeatable test. Use `data` when
the unresolved question is what training data to generate rather than how to
simulate it.

## Done

- The selected tool fits the available hardware and the project's main
  fidelity requirement.
- The simulation contract names which interfaces and physical properties must
  match reality.
- Every consumer uses a consistent clock and frame convention.
- Repeatability is designed where the simulation will be used as a test.
- Version and hardware requirements were checked in the current upstream
  [Gazebo](https://gazebosim.org/docs/),
  [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/), or
  [MuJoCo](https://mujoco.readthedocs.io/) documentation.
