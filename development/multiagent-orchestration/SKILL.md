---
name: multiagent-orchestration
description: Run a genuinely-parallel multiagent implementation with detailed guidance - plan, gate on environment, spawn subagents concurrently, aggregate, and debug/retry
when_to_use: Load before planning ANY work with independently executable units - the request names parallel/multiagent/concurrent execution, asks to orchestrate or fan out agents, or decomposes into lanes that would otherwise run one at a time
languages: [all]
subagents: [all]
tools_needed: [read, glob]
---

## Instructions

Invoke this on demand ("run the multiagent implementation"). **You (the host
assistant) perform the orchestration using your own subagent-spawning primitives.**
prompticorn is a prompt/config generator, not an agent runtime — the parallelism is
realized by you, the capable host, not by prompticorn. This skill composes (does not
duplicate) the existing `multi-agent-coordination`, `workflow-orchestration-patterns`,
and `async-workflow-execution` workflows; read those for the coordinator pattern,
diagrams, and async model.

Two gates are non-negotiable: the **environment-readiness gate** (Step 4) and the
**plan-before-work approval gate** (Step 5). Never spawn implementation lanes before
both pass.

### Step 1: Load conventions

**Purpose:** Every subagent must implement against the same rules.

- Locate and read all governing docs: coding standards, ADRs, naming, directory
  structure, security guidance, and test patterns.
- Confirm explicitly which docs loaded (list them).
- Flag gaps: any convention area with no doc is a risk to call out in the plan.

### Step 2: Discover agents

**Purpose:** Know your roster before designing the pipeline.

- Enumerate the available agent prompts.
- Map each to a pipeline role: code, ATDD, TDD, verify, enforce, security, debug,
  PM/architect.
- Flag any role with no matching agent (a coverage gap for the plan's gap report).

### Step 3: Design the execution model

**Purpose:** Maximize safe parallelism.

- **Explicit dependencies:** each agent/subagent declares what it depends on and
  what its completion unblocks. Two units with no dependency between them run in
  parallel by default — sequencing is the thing that needs justifying.
- **Spawn a subagent per independently executable unit.** Every brief carries four
  things, and a brief missing any of them is not ready to dispatch:
  1. the agent prompt the unit runs as,
  2. the conventions loaded in Step 1,
  3. its specific task scope — and the boundary it must not cross,
  4. the interfaces it shares with other units: what it consumes, what it produces.
- **Recursive spawning:** a unit whose own work decomposes into parallelisable
  subtasks spawns its own subagents rather than working through them serially.
  Parallelism is not reserved for the top level.
- **Aggregator per phase:** define the aggregator that collects a phase's outputs,
  validates consistency *across* them, and gates the next phase. Reuse the
  coordinator pattern from `multi-agent-coordination` /
  `workflow-orchestration-patterns` rather than reinventing it.

### Step 4: Environment-readiness gate (HARD)

**Purpose:** No lane starts against a dead dependency.

The `environment-setup` subagent runs first, alone, and must finish green before
any coding, testing, or verification lane is unblocked — regardless of how much
parallelism exists elsewhere. It must:

- Identify **every** service, server, daemon, or process this phase needs: dev
  server, test runner, database, message broker, mock/stub server, compiler
  watcher, cache.
- Start or verify each one. **Assume nothing is already up** — check, don't hope.
- Confirm ports bind, connections open, and health checks pass.
- Start the watchers and live-reload processes the work ahead depends on.
- Document what it started, how to verify each, and how to stop it cleanly.

**The pipeline owns setup.** Never instruct the human to start a service, run a
command, or provision infrastructure by hand. If a service is needed, start it.

An **unstartable service is a surfaced blocker** — stop and report it. Do not
silently proceed against a degraded environment.

### Step 5: Present the plan for approval (HARD gate)

**Purpose:** The human approves the shape of the run before any work happens.

Deliver the plan as a **markdown document**, containing:
- Conventions loaded (from Step 1).
- Agent roster and role mapping (Step 2).
- Environment manifest (services + health checks, Step 4).
- A **Mermaid execution map**: `env gate → parallel lanes → subagent spawn points →
  aggregation → sequential gates → debug/retry loop`.
- Subagent specs (each unit's inputs, outputs, dependencies, owning agent).
- Convention-enforcement checkpoints (where the enforce/verify roles gate).
- Test strategy: **ATDD before coding, TDD concurrent with coding**.
- Gap report (roles/conventions/services with no coverage).
- Debug / retry / escalate logic.

**Wait for explicit approval before Step 6.**

### Step 6: Concurrent execution on approval

**Purpose:** Realize the parallelism.

- Spawn all currently-unblocked subagents **simultaneously**.
- Unblock a downstream unit the moment its dependencies resolve — do not wait for a
  whole phase if a unit is ready.
- **Never serialize by accident.** Do not wait for one subagent to return before
  launching the next. Each lane runs as an independent stream with its own context,
  and progress from all streams surfaces concurrently rather than being queued to
  the end.
- **Aggregate at each gate**; a gate advances only when its inputs are complete and
  pass enforcement.
- On failure, run the debug/retry loop; escalate a persistently-failing unit as a
  blocker rather than looping indefinitely.

Delegated background/isolated subagents must emit progress heartbeats per the core
"Subagent Progress Heartbeats" convention so their status is observable.

### Re-presenting mid-run

If the agent roster, the loaded conventions, the environment state, or the plan
itself changes materially once execution is under way, **pause every lane and
re-present** the amended plan for approval. An approved plan authorizes the run it
described, not whatever it turned into.
