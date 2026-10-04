---
name: agentic-control-kernel
category: governance
description: >
  Unifying control-systems metalayer for LLM-as-controller agent development.
  Bootstrap any repository with typed plant/action/trace schemas, safety shield
  conventions, multi-rate loop hierarchy, EGRI-compatible evaluator interfaces,
  and the full consciousness stack (governance + knowledge graph + episodic memory).
  Use when: (1) setting up agentic control primitives in a new or existing project,
  (2) designing LLM-as-controller architectures with safety shields and typed directives,
  (3) wiring EGRI/autoany loops for controller or artifact improvement,
  (4) bootstrapping the consciousness stack (control-metalayer + knowledge-graph + conversation bridge),
  (5) integrating symphony-style orchestration patterns,
  (6) defining plant interfaces, state estimators, or world models for agent-controlled systems,
  (7) user says "control kernel", "agentic control", "safety shield", "plant interface",
  "control metalayer", "agent controller", "multi-rate loop", "LLM control law".
---

# Agentic Control Kernel

A purely knowledge-based metalayer that unifies six subsystems into a single
installable skill for any project:

| Layer | Source / Crates | Role |
|-------|----------------|------|
| Governance | control-metalayer-loop | Setpoints, sensors, gates, policy, profiles |
| Improvement | `autoany_core` + `autoany-aios` + `autoany-lago` | EGRI microkernel, Arcan execution, Lago ledger |
| Orchestration | `symphony-orchestrator` + `symphony-arcan` | Poll/dispatch/worker/reconcile via Arcan HTTP |
| Runtime | Life (`arcan`, `lago`, `autonomic`, `praxis`, `spaces`) | Agent sessions, event journal, homeostasis, networking |
| Protocol | `aios-protocol` | Canonical types — shared vocabulary across all crates |
| Episodic Memory | knowledge-graph-memory | Conversation logs -> Obsidian bridge |
| Consciousness | agent-consciousness | Three-substrate persistent context |
| QA/Actuation | gstack | Headless browser, workflow skills |
| **Control Kernel** | **this skill** | Plant interface, safety shields, typed schemas, multi-rate hierarchy |

## Core Law

> Do not grant an agent more mutation freedom than your evaluator can reliably judge.
> In control terms: do not let the LLM's action space exceed what your runtime monitors,
> safety filters, and evaluators can certify.

## Quick Start

### 1. Bootstrap a project

```bash
python3 scripts/control_kernel_init.py <repo-path> [--profile governed] [--runtime arcan] [--ledger lago]
```

This installs into the target repo:
- `.control/policy.yaml` — control-systems-aware setpoints
- `schemas/` — state, action, trace, evaluator JSON schemas
- `METALAYER.md` — control loop definition with plant/shield/estimator sections
- Harness gates wired to `make smoke`, `make check`, `make control-audit`

### 2. Define the plant interface

Edit `.control/plant.yaml` with typed state and action schemas for your system.
See [references/plant-interface.md](references/plant-interface.md) for the full API spec.

### 3. Wire safety shields

See [references/safety-shields.md](references/safety-shields.md) for CBF-QP patterns,
policy gates, and containment invariants.

### 4. Set up EGRI for controller improvement

Use the problem-spec template in `assets/templates/problem-spec.control.yaml`
to define an autoany loop over your controller artifacts.
See [references/egri-for-controllers.md](references/egri-for-controllers.md).

## Architecture Overview

The LLM emits typed **control directives** `θ_t` — not raw actuations `u_t`.
Deterministic controller modules execute, safety shields filter, and the runtime
logs traces to an append-only ledger.

```
Plant → observe() → Runtime → update estimator → b_t
  → LLM Agent: request decision(b_t) → θ_t (typed directive)
  → Controller: propose(b_t, θ_t) → proposed u_t
  → Safety Shield: filter(u_t, b_t) → safe u_t + certificate
  → Plant: apply(safe u_t) → result
  → Evaluator/Ledger: append trace + score
```

See [references/architecture.md](references/architecture.md) for the full 5-layer diagram.

## Multi-Rate Hierarchy

| Loop | Cadence | LLM here? | What runs |
|------|---------|-----------|-----------|
| Servo | ms | No | PID, state feedback, deterministic |
| Constrained execution | 10-100ms | No (param updates only) | MPC/CBF-QP solvers |
| Supervisory planning | seconds | Yes | Goal setting, mode switching, tool selection |
| Auto-tuning (EGRI) | minutes-days | Yes | Controller synthesis, model learning |

See [references/multi-rate-hierarchy.md](references/multi-rate-hierarchy.md).

## LLM Roles in the Control Stack

| Role | Outputs | When to use |
|------|---------|-------------|
| Supervisory controller | setpoints, mode switches, constraints | Default — long-horizon reasoning |
| Meta-controller | tool/module selection, identification triggers | Modular systems with multiple controllers |
| Controller synthesizer | code, configs, tests | Offline — gated by harness CI |
| EGRI loop compiler | problem-spec, evaluator design, promotion rules | Continuous improvement cycles |

See [references/architecture.md](references/architecture.md) for the full role table.

## Reference Guide

- **[architecture.md](references/architecture.md)** — 5-layer stack, realized crate graph, control-flow diagram, component mapping
- **[integration-map.md](references/integration-map.md)** — Adapter crate boundary map, configuration, direction rule
- **[plant-interface.md](references/plant-interface.md)** — Plant/Estimator/Controller/Shield/Evaluator API specs
- **[safety-shields.md](references/safety-shields.md)** — CBF-QP, policy gates, containment, failure modes
- **[multi-rate-hierarchy.md](references/multi-rate-hierarchy.md)** — Loop rates, LLM placement, heuristics
- **[world-models.md](references/world-models.md)** — Koopman, DeePC, digital twins, learned dynamics
- **[egri-for-controllers.md](references/egri-for-controllers.md)** — Autoany applied to controller optimization
- **[orchestration-patterns.md](references/orchestration-patterns.md)** — Symphony daemon patterns for multi-agent dispatch
- **[consciousness-stack.md](references/consciousness-stack.md)** — Memory/knowledge/episodic integration
- **[failure-modes.md](references/failure-modes.md)** — Mitigations catalog for LLM-in-the-loop control
- **[deep-research-report.md](references/deep-research-report.md)** — Original research report and project plan: formal control theory, literature survey, prototype roadmap

## Schemas

JSON Schemas in `schemas/` enforce typed interfaces:
- `state.schema.json` — Plant/belief state
- `action.schema.json` — Control directives (θ_t)
- `trace.schema.json` — Ledger entries (autoany-compatible)
- `evaluator.schema.json` — Score vectors, promotion decisions
- `egri-event.schema.json` — EGRI trial events for Lago persistence via EventKind::Custom

## Existing Skill Dependencies

This skill synthesizes and references (does not duplicate) these existing skills:
- **control-metalayer-loop** — Use for `.control/` bootstrapping and governance primitives
- **autoany** — EGRI loop execution via `autoany-aios` (Arcan sessions) and `autoany-lago` (Lago ledger)
- **symphony** — Orchestration dispatch via `symphony-arcan` (Arcan HTTP runtime)
- **life** — `arcan` (agent sessions), `lago` (event journal), `autonomic` (homeostasis), `spaces` (networking)
- **aios-protocol** — Canonical types shared across all adapter crates
- **agent-consciousness** — Use for consciousness stack setup
- **knowledge-graph-memory** — Use for conversation bridge to Obsidian
- **gstack** — Use for QA actuation via headless browser
