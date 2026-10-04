---
name: capx-agentic-robotics
category: robotics
description: >
  Agentic robotics with CaP-X — LLM-driven robot manipulation via code generation. Use when:
  (1) Setting up CaP-X / CaP-Gym environments for robot manipulation benchmarks,
  (2) Running CaP-Bench evaluations across LLMs/VLMs on robotic tasks,
  (3) Building or extending CaP-Agent0 agentic harnesses (skill libraries, visual differencing, parallel reasoning),
  (4) Training robot coding agents with CaP-RL (GRPO on code generation),
  (5) Developing perception APIs (SAM3, Molmo, depth, point clouds) or control APIs (IK solvers, grasp planners),
  (6) Sim-to-real transfer for Franka Panda, R1Pro humanoid, or other robot platforms,
  (7) Designing auto-synthesized skill libraries for physical manipulation (Voyager-style),
  (8) Integrating agentic robotics with Life Agent OS (Arcan orchestration, Spaces agent networking, Lago persistence),
  (9) Any task involving LLM-based robot control, manipulation benchmarks, robotic code synthesis, or embodied AI agents.
---

# CaP-X Agentic Robotics

LLM agents that write Python code to control real robots — from zero-shot manipulation to RL-trained coding agents with sim-to-real transfer.

Based on [CaP-X](https://capgym.github.io/) (NVIDIA, Berkeley, Stanford, CMU). arXiv: [2603.22435](https://arxiv.org/abs/2603.22435). MIT License.

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/capgym/cap-x.git
cd cap-x

# Requires Python 3.10 (BEHAVIOR) or 3.12 (RL/LIBERO)
uv sync          # uses uv (Astral) for package management
```

### 2. Start Perception Services

CaP-X runs perception models as microservices:

```bash
# SAM3 segmentation (port 8114)
python -m capx.perception.sam3_server

# Molmo 2 pointing (port 8117)
python -m capx.perception.molmo_server

# ContactGraspNet 6-DOF grasps (port 8115)
python -m capx.perception.grasp_server

# OWL-ViT detection (port 8118)
python -m capx.perception.owlvit_server
```

Requires CUDA GPU. For IK solvers:
- **PyRoKi** (port 8116) — CPU-friendly inverse kinematics
- **cuRobo** — GPU-accelerated motion planning (NVIDIA, requires CUDA)

### 3. Run a Benchmark Task

```bash
# Single task evaluation (zero-shot, 100 trials)
python scripts/eval.py \
  --task cube_lift \
  --model openai/gpt-5.2 \
  --tier S1 \
  --num_trials 100

# Full CaP-Bench sweep
python scripts/eval_capbench.py --model anthropic/claude-opus-4.5
```

## Architecture

```
CaP-X
├── CaP-Gym ─── Gymnasium interface wrapping 187 tasks
│   ├── RoboSuite (7 core) ── Franka Panda tabletop/bimanual
│   ├── LIBERO-PRO (130+) ── Franka Panda kitchen/living
│   └── BEHAVIOR (50) ────── R1Pro humanoid, Isaac Sim
│
├── CaP-Bench ── 8 tiers (S1-S4 single, M1-M4 multi-turn)
│   ├── Varies: perception noise, API abstraction, visual grounding
│   └── 12 frontier LLMs/VLMs benchmarked
│
├── CaP-Agent0 ── Training-free agentic harness
│   ├── Visual Differencing Module (VDM)
│   ├── Auto-synthesized skill library (Voyager lineage)
│   └── Parallel ensembled reasoning (multi-model)
│
└── CaP-RL ──── GRPO post-training on code generation
    ├── 7B model: 25% → 80% in 50 iterations
    └── Zero-shot sim-to-real transfer
```

### Control Flow

The agent never outputs raw joint commands. Instead:

```
LLM → generates Python code → composes perception + control APIs → robot executes
```

**API abstraction levels** (Franka example):
- `FrankaControlApi` — Full high-level (perception + IK control)
- `FrankaControlPrivilegedApi` — Oracle state (no perception noise)
- `FrankaControlReducedApi` — Low-level primitives
- `FrankaControlReducedSkillLibraryApi` — Low-level + auto-synthesized skills

## CaP-Bench Tiers

| Tier | Mode | Perception | Abstraction | Visual Grounding |
|------|------|-----------|-------------|-----------------|
| S1 | Single | Noiseless | High | -- |
| S2 | Single | Noisy | High | -- |
| S3 | Single | Noisy | Low | -- |
| S4 | Single | Noisy | Low | -- |
| M1 | Multi | Noisy | High | -- |
| M2 | Multi | Noisy | High | Multimodal feedback |
| M3 | Multi | Noisy | Low | -- |
| M4 | Multi | Noisy | Low | VDM |

Run specific tiers:

```bash
python scripts/eval.py --task cube_stack --model google/gemini-3-pro --tier M4
```

## CaP-Agent0: Training-Free Harness

Three components inspired by Voyager (Wang et al., 2023):

### 1. Visual Differencing Module (VDM)

Convert before/after scene images into structured text describing what changed. Solves cross-modal alignment failures found in M2 tier.

### 2. Auto-Synthesized Skill Library

Reusable functions discovered from successful execution traces. Persist across trials. Compilation pipeline:

```bash
# After running evaluations, compile skill library from successful traces
python scripts/skill_library_compilation/compile.py \
  --eval_outputs results/cube_lift/ \
  --output skills/

# Use compiled library in evaluation
python scripts/eval.py --task cube_stack --tier M4 --skill_library skills/
```

9 task-agnostic skills discovered (geometric utilities, grasp filters, quaternion helpers).

### 3. Parallel Ensembled Reasoning

Multiple models generate candidate solutions:

```bash
python scripts/eval_agent0.py \
  --task cube_stack \
  --models "google/gemini-3-pro,openai/gpt-5.2,anthropic/claude-opus-4.5" \
  --ensemble
```

**Result**: Matches/exceeds human expert code on 4/7 tasks. Competitive with trained VLA policies (OpenVLA, pi_0) despite being training-free.

## CaP-RL: RL on Code Generation

GRPO (Group Relative Policy Optimization) applied to Qwen2.5-Coder-7B:

```bash
# Train on privileged tier S1 for stable convergence
python scripts/train_rl.py \
  --task cube_lift \
  --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
  --group_size 15 \
  --train_iterations 50 \
  --gpu_type h100
```

| Task | Base (7B) | +CaP-RL (50 iter) | Human Expert |
|------|-----------|-------------------|-------------|
| Cube Lift (sim) | 25% | **80%** | 93% |
| Cube Stack (sim) | 4% | **44%** | 73% |
| Spill Wipe (sim) | 30% | **93%** | 100% |
| Cube Lift (real) | 24% | **84%** | 92% |
| Cube Stack (real) | 12% | **76%** | 84% |

Transfer zero-shot to real robots because reasoning is over abstract APIs, not raw pixels.

See `references/caprl-training.md` for full GRPO configuration, GPU requirements, and training recipes.

## Sim-to-Real Transfer

```
Simulation (CaP-Gym) ──[abstract APIs]──> Real Robot
                                          ├── Franka Panda (primary)
                                          ├── AgiBot G1 (bimanual demos)
                                          └── R1Pro (mobile manipulation)
```

Real-world requirements:
- Stereo camera with calibrated metric-scale depth (e.g., ZED)
- `robots_realtime` package for Franka Panda control
- Same perception service stack (SAM3, Molmo, ContactGraspNet)

## Extending CaP-X

### Add a New Task

```python
# Register in capx/envs/your_suite/
class MyTask(CaPGymTask):
    """Gymnasium-compatible task wrapper."""

    def __init__(self):
        self.perception = PerceptionStack(sam3=True, molmo=True, depth=True)
        self.control = FrankaControlApi(ik_solver="pyroki")

    def get_prompt(self) -> str:
        return "Pick up the red cube and place it on the green platform."

    def compute_reward(self, obs, action, next_obs) -> float:
        # Verifiable environment reward for RLVR
        return float(self._check_cube_on_platform(next_obs))
```

### Add a New Robot

Implement the control API interface. See `references/api-spec.md` for the full specification:
- `goto_pose(pos, quat)` — Move end-effector to target pose via IK
- `grasp()` / `open_gripper()` / `close_gripper()` — Gripper control
- `get_ee_pose()` — Current end-effector state

### Add a Perception Module

Register as a microservice with a standard interface:
- Input: RGB image (+ optional depth)
- Output: Structured detection/segmentation result
- Follow the pattern in `capx/perception/` servers

## Integration with Life Agent OS

CaP-X connects to the Broomva Agent OS stack at three points:

### Arcan Orchestration

Orchestrate multi-step robotic workflows as Arcan task graphs:

```rust
// Arcan pipeline for robotic manipulation
let pipeline = arcan::Pipeline::new()
    .step("perceive", capx_perception_step)   // SAM3 + Molmo
    .step("plan", capx_agent_step)            // LLM code generation
    .step("execute", capx_control_step)       // Robot actuation
    .step("verify", capx_vdm_step)            // Visual differencing
    .on_failure("reflect", capx_reflect_step) // Self-correction loop
    .build();
```

### Spaces Agent Networking

Robotic agents publish events to Spaces channels:

```
#robot-logs    <- Execution traces, success/failure, skill library updates
#agent-logs    <- Session summaries (standard bstack integration)
#perception    <- Scene descriptions, object detections, grasp candidates
```

Multiple robot agents share skill libraries via Spaces — a skill discovered by one robot transfers to others.

### Lago Persistence

Store and version:
- **Skill libraries** — SHA-256 hashed Python functions as Lago blobs
- **Evaluation traces** — Execution logs for CaP-RL training data
- **Benchmark results** — CaP-Bench scores across models and tiers
- **Trained checkpoints** — RL-tuned model weights

## Companion Skills

```bash
# ORCA Hand (17-DOF tendon-driven hand — ETH Zurich)
npx skills add broomva/skills --skill orcahand -g -y

# Remote GPU (offload perception/training to NUC or cloud)
npx skills add broomva/skills --skill remote-gpu -g -y
```

## Resources

### references/

- `references/api-spec.md` — Full perception and control API specification
- `references/capbench-results.md` — Benchmark results across 12 models, 8 tiers
- `references/caprl-training.md` — CaP-RL training guide (GRPO config, GPU requirements, recipes)

### scripts/

- `scripts/setup-perception.sh` — Start all perception microservices
- `scripts/run-benchmark.sh` — Full CaP-Bench evaluation sweep

## Key Papers

- CaP-X: [arXiv:2603.22435](https://arxiv.org/abs/2603.22435) — Framework paper
- Voyager: [arXiv:2305.16291](https://arxiv.org/abs/2305.16291) — Skill library + self-reflection origin
- Code as Policies: [arXiv:2209.07753](https://arxiv.org/abs/2209.07753) — LLM code to robot control
- SayCan: [arXiv:2204.01691](https://arxiv.org/abs/2204.01691) — Grounding LLMs in robotic affordances
