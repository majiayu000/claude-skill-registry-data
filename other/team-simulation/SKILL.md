---
name: team-simulation
description: "Orchestrate Project Aegis simulation and AI work: deterministic tick pipeline, sensors, engagement, logistics, policy evaluation, AI/delegation behavior, DOTS/ECS hot paths, replay verification, and military accuracy gates."
argument-hint: "[architecture|tick-pipeline|sensors|engagement|logistics|policy|ai|dots|replay|accuracy|full-story] [scope] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
model: opus
agent: military-simulation-architect
---

# Team Simulation — Deterministic Sim / AI Orchestration

Use this skill for coordinated work on `ProjectAegis.Sim`, deterministic AI and
delegation behavior, DOTS/ECS simulation data, military parameter validation, and
replay reproducibility gates.

## Phase 0: Resolve Mode and Review Level

Modes:

- `architecture` — simulation assembly/API boundaries, system ownership, and ADR impact.
- `tick-pipeline` — fixed update order, command ingestion, policy, engagement, logistics, and logs.
- `sensors` — detection, classification, EW, contact state machines, and sorted pair iteration.
- `engagement` — fire-control, launch authorization, damage, DLZ, and abort reasons.
- `logistics` — magazines, fuel, readiness, supply, and data-driven constraints.
- `policy` — ROE/EMCON/WRA evaluation and delegation-to-sim policy migration.
- `ai` — autonomous controller behavior, decision purity, observed-state inputs, and seeded behavior.
- `dots` — DOTS/ECS, Burst, NativeContainers, BlobAssets, and hot-path layout.
- `replay` — order-log schema, replay hash, golden baselines, and divergence triage.
- `accuracy` — military parameter source review, authenticity/playability trade-offs, and balance.
- `full-story` — readiness → architecture → implementation handoff → tests → replay gate.
- No mode — infer from the request; if ambiguous, ask one focused question.

Review mode:
1. If `--review [full|lean|solo]` is present, use it.
2. Else read `production/review-mode.txt` if present.
3. Else default to `lean`.

## Team Composition

- **military-simulation-architect** — simulation design authority and orchestration lead.
- **engine-programmer** — core sim loop, pure C# systems, performance-critical code.
- **ai-programmer** — autonomous behavior, decision systems, perception/attention integration.
- **determinism-engineer** — seeded RNG, stable ordering, replay hash, wall-clock bans.
- **unity-dots-specialist** — DOTS/ECS, Jobs, Burst, NativeContainers, BlobAssets.
- **sim-data-specialist** — database-to-simulation snapshots and deterministic cache layout.
- **simulation-parameter-analyst** — source-backed military parameters and physical consistency.
- **military-research-specialist** — evidence/citation support for real-world systems.
- **gameplay-mechanics-analyst** — playability, balance, dominant strategy review.
- **performance-analyst** — frame/tick budgets and allocation review.
- **qa-lead / qa-tester** — test strategy, replay evidence, and regression coverage.
- **technical-director** — cross-layer architecture escalation.

## Phase 1: Load Required Context

Read and summarize the minimum required context:

- `docs/architecture/architecture.md` — layers, tick pipeline, ADR index, layer rules.
- Relevant ADRs, especially simulation/delegation boundary, policy, order log, tick order, DOTS.
- Relevant GDD/requirements files for the feature or subsystem.
- `src/ProjectAegis.Sim/**`, `src/ProjectAegis.Delegation/**`, and Unity adapter files in scope.
- Existing tests under `src/ProjectAegis.Sim.Tests/**`, delegation tests, and replay tests.
- Data snapshot contracts if database-backed parameters are involved.

Report the deterministic boundary, owning agents, affected systems, and validation gates.

## Phase 2: Select Workflow Pipeline

### Architecture Pipeline

1. Spawn `military-simulation-architect` for fidelity, ownership, and system boundaries.
2. Spawn `engine-programmer` or `c-sharp-architect` for pure C# API/assembly contracts.
3. Spawn `determinism-engineer` for ordering, RNG, and replay implications.
4. Consult `technical-director` for dependency direction or ADR changes.

### Tick / Replay Pipeline

1. Verify fixed tick order and command ingestion order against ADR-004.
2. Require stable keys for entity, side, contact, order, and event iteration.
3. Run `/determinism-audit` for changed sim/controller paths.
4. Run or plan `/replay-verify` with golden order-log/world-hash evidence.

### Sensors / Engagement / Logistics / Policy Pipeline

1. Spawn `simulation-parameter-analyst` for formulas and source-backed ranges.
2. Spawn `military-research-specialist` when real-world evidence is needed.
3. Spawn `gameplay-mechanics-analyst` for authenticity vs. playability review.
4. Spawn `engine-programmer` or `ai-programmer` for implementation architecture.
5. Gate with deterministic tests and regression evidence.

### AI / Delegation Pipeline

1. Spawn `ai-programmer` for controller behavior and decision-system design.
2. Spawn `determinism-engineer` to enforce pure functions of observed state, traits, and seed.
3. Coordinate with `lead-programmer` for API seams with `ProjectAegis.Delegation`.
4. Require tests for edge cases, seeded behavior, and order-log impact.

### DOTS Pipeline

1. Spawn `unity-dots-specialist` for DOTS/ECS layout and Burst constraints.
2. Spawn `sim-data-specialist` if data snapshots feed ECS runtime structures.
3. Run `/ecs-data-optimization` for blittable layouts and NativeContainer safety.
4. Confirm no UnityEngine dependency leaks into pure sim assemblies.

### Accuracy / Balance Pipeline

1. Spawn `simulation-parameter-analyst` and `military-research-specialist` in parallel.
2. Run `/simulation-accuracy-validation` for parameter authenticity.
3. Run `/gameplay-balance-analysis` or `/balance-check` for playability concerns.
4. Document any real-world deviation and the approved reason.

## Phase 3: Blocking Gates

Stop and ask before proceeding if any of these occur:

- Public sim API, tick order, order-log schema, or replay hash changes.
- New RNG streams or changes to seeded behavior.
- Unordered collection iteration on deterministic paths.
- Wall-clock reads or frame-time reads in simulation/controller logic.
- Per-tick database or UnityEngine dependency from `ProjectAegis.Sim`.
- DOTS/Burst design that is not blittable or allocates in hot paths.
- Military parameter changes without source/provenance or approved abstraction rationale.

## Output

Produce a concise orchestration report:

- Mode and scope.
- Agents/skills invoked or recommended.
- Affected layers and source areas.
- Determinism, replay, DOTS, and accuracy risks.
- Required tests/evidence.
- Next approved action.
