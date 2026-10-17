---
name: aiwf-physics-simulation
description: Use for physics sanity checks, units, coordinate frames, kinematics, dynamics, controls, Gazebo, MuJoCo, robot simulation, and sim-to-real planning.
---

# AIWF Physics Simulation

## Core Rule

Do the physics inventory before trusting a simulation, controller, or robot behavior claim. Track units, frames, mass/inertia, friction/contact assumptions, sensor rates, actuator limits, timestep, and validation data.

## Workflow

1. Identify what is being modeled: rigid body, linkage, drivetrain, arm, payload, vehicle, sensor, controller, environment, or full robot.
2. Record coordinate frames, units, sign conventions, gravity, mass, inertia tensors, friction/contact assumptions, limits, and actuator models.
3. Separate conceptual physics from simulator behavior. A simulator config can be internally consistent and still fail the real system.
4. Choose the right validation level: dimensional analysis, static equilibrium, simple analytic case, simulation-only regression, log replay, bench test, or field comparison.
5. Report uncertainty explicitly when measurements, CAD mass properties, calibration data, or real logs are missing.

## Guardrails

- Never mix meters/inches, degrees/radians, body/world frames, or left/right-handed coordinates without an explicit conversion point.
- Treat contact, friction, compliance, backlash, latency, and sensor noise as assumptions that must be stated, not hidden defaults.
- Do not claim sim-to-real readiness from one simulator run. Require measured comparison, tolerance, and failure cases.
- In controls work, identify sample time, saturation, integrator windup, delay, and failsafe behavior.
- Add `aiwf-robotics-systems` when the task crosses sensors, actuators, ROS 2, logs, or system integration.
- Add `aiwf-field-pilot-readiness` when simulated behavior is used to justify a real-world pilot or customer demo.

## Validation Defaults

Use the cheapest check that can falsify the model:

```powershell
python -m pytest <physics-or-sim-tests>
python <script> --dry-run
```

For simulator work, inspect world/model files and launch configuration before running heavy simulations. Do not start GPU-heavy or long-running simulations unless Shawn asks.

## Primary Source Anchors

- Gazebo Sim: https://gazebosim.org/libs/sim/
- MuJoCo documentation: https://mujoco.readthedocs.io/
- MuJoCo project page: https://mujoco.org/
- NIST robotics measurement work: https://www.nist.gov/el/robotics

Use official simulator documentation for API/runtime behavior and real measurements for real-world claims.
