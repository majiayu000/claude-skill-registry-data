---
name: aiwf-robotics-systems
description: Use for robotics architecture, Rnv1-style prototype planning, ROS 2, sensors, actuators, perception, control, logging, robot integration, and robotics code or design reviews.
---

# AIWF Robotics Systems

## Core Rule

Treat robotics work as a system integration problem before treating it as a code task. Identify the robot job, operating environment, sensors, actuators, compute, power, communication paths, control loops, safety boundaries, logging, and test plan before recommending architecture or edits.

## Workflow

1. Classify the robot: mobile base, manipulator, vehicle, inspection rig, service robot, simulation-only prototype, or AIWF/Rnv1 planning artifact.
2. Inventory hardware and software boundaries: sensors, motors, motor drivers, embedded controllers, host compute, ROS 2 nodes, network links, power budget, and mechanical constraints.
3. Separate loops by timing and risk: safety interlock, low-level control, perception, planning, local AI reasoning, UI/operator controls, logging, and cloud or service integrations.
4. Choose the smallest route: architecture plan, sensor/actuator interface review, ROS graph check, field-test checklist, data/logging plan, or code patch.
5. Validate with observable checks: node/topic/service inventory, simulated run, bench test, log replay, hardware-in-loop, or documented field-test gate.

## Guardrails

- Do not assume ROS 2 is present. If it is present, inspect the distro, workspace layout, launch files, packages, nodes, topics, services, actions, parameters, and message types before changing behavior.
- Keep hard real-time or motor-control work off unreliable high-level loops unless the project already proves the timing path.
- Preserve manual stop, remote disable, operator handoff, watchdog, and rollback paths.
- Require logging for perception inputs, control outputs, state transitions, errors, and operator interventions before claiming field readiness.
- Add `aiwf-physics-simulation` for kinematics, dynamics, contact, units, simulation, or sim-to-real issues.
- Add `aiwf-embedded-edge-ai` for microcontrollers, RTOS, Jetson, power, thermal, or edge deployment details.
- Add `aiwf-field-pilot-readiness` before outdoor trials, partner pilots, customer demos, or site-specific robotics work.

## Validation Defaults

Prefer project-native checks. Useful robotics checks include:

```powershell
ros2 doctor
ros2 node list
ros2 topic list
ros2 service list
ros2 launch <package> <launch-file>
```

Use these only when ROS 2 is installed and the workspace is meant to run. Otherwise validate with static review, simulation config checks, or written test gates.

## Primary Source Anchors

- Ai Embedded Systems Rnv1 robotics page: https://aiembeddedsystems.com/rnv1-robotics/
- ROS 2 documentation: https://docs.ros.org/
- ROS 2 release schedule and supported distributions: https://docs.ros.org/en/rolling/The-ROS2-Project/Release-Schedule.html
- ROS 2 design articles: https://design.ros2.org/
- NIST robotics measurement and test-method work: https://www.nist.gov/el/robotics

Verify the actual robot stack and ROS distribution before using version-specific commands.
