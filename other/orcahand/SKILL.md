---
name: orcahand
category: robotics
description: >
  Full-stack skill for the ORCA Hand — 17-DOF tendon-driven robotic hand
  (ETH Zurich). Implements agentic-control-kernel Plant interface with typed
  schemas, safety shields, multi-rate loops. Lifecycle: 3D print + assembly,
  MuJoCo sim (orca_sim), RL training (macOS + remote GPU), teleoperation
  (AVP/Rokoko/MediaPipe via orca_retargeter), sim-to-real, EGRI improvement.
  Use when: building/assembling OrcaHand, orca_sim environments, teleoperating,
  training grasp policies, sim-to-real transfer, control-kernel Plant schemas,
  EGRI loops. Triggers: "orcahand", "orca_core", "orca_sim", "dexterous hand",
  "robotic hand", "tendon-driven", "dynamixel hand", "hand simulation",
  "teleoperate hand", "grasp policy", "sim-to-real hand", "3d print hand".
---

# OrcaHand

Full-stack skill for the [ORCA Hand](https://orcahand.com/) — 17-DOF tendon-driven dexterous robotic hand. Compounds on `agentic-control-kernel` (plant/shield/trace) and `bstack` (governance).

## Plant Interface

Dual-backend: physical (`orca_core`) and simulated (`orca_sim`) share identical typed schemas.

```
observe() → OrcaHandState (schemas/orcahand-state.schema.json)
  measured:
    joint_positions: {thumb_mcp, thumb_abd, thumb_pip, thumb_dip,
                      index_abd, index_mcp, index_pip,
                      middle_abd, middle_mcp, middle_pip,
                      ring_abd, ring_mcp, ring_pip,
                      pinky_abd, pinky_mcp, pinky_pip, wrist}  # degrees
    motor_currents:      17 motors, mA
    motor_temperatures:  17 motors, celsius
    tactile_readings:    per-sensor [fx, fy, fz] in N (touch model only)
  estimated:
    grasp_state:  "open" | "contact" | "secured" | "slipping"
  context:
    backend: "physical" | "simulated"
    control_mode: "position" | "current" | "current_based_position"
    torque_enabled: bool

apply(action) → ActuationResult (schemas/orcahand-action.schema.json)
  directive_type:  setpoint_update | experiment_request | mode_switch
  target_controller: "orca_core" | "orca_sim"
  payload:
    joint_targets: {joint_name: degrees}   # partial dict OK
    num_steps: 25, step_size: 0.001s
    grasp_type: "power" | "precision" | "pinch"

reset(seed?) → neutral position (physical) or env.reset (simulated)

constraints():
  joint_roms: per-joint [min_deg, max_deg] from config.yaml
  max_current: 200mA, max_temperature: 70°C
```

## Safety Shields

Implements kernel SafetyShield contract: `filter()`, `feasible()`, `fallback()`.

| Shield | Invariant | filter() | feasible() |
|--------|-----------|----------|------------|
| Joint ROM | Targets within bounds | Clamp to valid range | >= 1 joint can move |
| Max Current | < 200mA per motor | Disable torque, alert | Current below threshold |
| Temperature | < 70°C per motor | Disable torque, cooldown | All motors < 65°C |
| Velocity | < safe joint velocity | Reduce step_size | Velocity achievable |
| Tactile | Force < sensor max | Release grasp, back off | Force within range |

**Emergency fallback**: `hand.disable_torque()` — hand goes limp. Safe due to popping joints.
**Cascade**: filter() -> feasible() -> if infeasible -> emergency fallback + alert outer loop.

## Multi-Rate Loop Mapping

```
SERVO (ms)     Dynamixel PID firmware. Agent never touches this.
     |
MID (10-100ms) Retargeter @ 30Hz / RL policy @ 60Hz / Replay @ 60Hz
               Safety shields run HERE: ROM clamp + current check per frame
     |
OUTER (sec)    LLM supervisory: grasp strategy, mode switch, task goals
               Outputs ControlDirective -> mid-loop controller
     |
META (min-day) EGRI: problem-spec -> train in sim -> evaluate -> promote to physical
               Runs on remote GPU, validated on local macOS
```

## Quick Starts

- **Build a hand**: Read [references/hardware-build.md](references/hardware-build.md) — BOM, 3D printing, Dynamixel sourcing, assembly, wiring
- **Simulate**: Read [references/simulation-setup.md](references/simulation-setup.md) — `pip install orca_sim`, MuJoCo on macOS, environment catalog
- **Teleoperate**: Read [references/teleoperation.md](references/teleoperation.md) — AVP / Rokoko / MediaPipe -> retargeter -> hand
- **Train RL policies**: Read [references/rl-training.md](references/rl-training.md) — local CPU/MPS or remote GPU, reward design
- **Improve controllers**: Read [references/egri-controller-loop.md](references/egri-controller-loop.md) — EGRI problem-spec, evaluator, promotion

## Scope Router

Load the relevant reference based on user intent. Max 3 references at once.

| Intent | Keywords | Reference |
|--------|----------|-----------|
| Build hand | build, print, assemble, BOM, servo, wire | `hardware-build.md` |
| Calibrate | calibrate, tension, neutral, config.yaml, serial | `calibration-pipeline.md` |
| Simulate | simulate, mujoco, orca_sim, gymnasium, render | `simulation-setup.md` |
| Train | train, RL, PPO, SAC, reward, policy, GPU | `rl-training.md` |
| Teleoperate | teleoperate, retarget, vision pro, rokoko, mediapipe | `teleoperation.md` |
| Sim-to-real | sim-to-real, domain randomization, joint reorder | `sim-to-real.md` |
| EGRI | improve, optimize, EGRI, problem-spec, evaluator | `egri-controller-loop.md` |
| API | OrcaHand class, set_joint_pos, REST API, joint names | `api-reference.md` |
| Install | install, clone, dependencies, which repo, version | `dependency-graph.md` |
| Debug | servo not found, segfault, drift, error, stuck | `troubleshooting.md` |

## Scripts

- `scripts/orcahand_init.py` — Bootstrap workspace: clone repos, install deps, detect serial, generate `.control/plant.yaml`
- `scripts/orcahand_check.py` — Health check for bstack integration (JSON output, exit 0/1)

## Schemas

- `schemas/orcahand-state.schema.json` — extends kernel `state.schema.json`
- `schemas/orcahand-action.schema.json` — extends kernel `action.schema.json`
- `schemas/orcahand-trace.schema.json` — extends kernel `trace.schema.json`

## Templates

- `assets/templates/problem-spec.orcahand.yaml` — EGRI template for grasp optimization
- `assets/templates/config.orcahand.yaml` — starter config for new hand builds
