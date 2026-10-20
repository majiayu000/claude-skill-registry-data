---
name: loki-mode
description: "Master multi-agent swarm orchestration — coordinates personas across the 14-phase lifecycle (10-phase core build loop S01–S10, plus Day-0 S00 and Day-2 S11–S13) with checkpoints, memory, and HITL gates. Use when: loki, swarm, orchestrate, big project, autonomous build, multi-agent, spawn, coordinate swarm."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/brain/loki-mode.skill.md"
  tags: "brain"
  core: "true"
  context_cost: "high"
---
# Loki Mode — Master Orchestration Skill

## Goal

Coordinate a swarm of specialized agent personas through a full SDLC lifecycle, with
durable checkpoints, memory, and human approval gates — enabling large projects that
would otherwise exceed a single agent's context limits.

## Skill, Guide & MCP Selection Mandate
**CRITICAL**: In every phase, gate, and checkpoint of the SDLC, the orchestrator and all sub-personas must **always select (and ask the user to confirm/select) the best guides and skills** for the specific tasks, user query prompt, action, gate passing, or system workflow before executing. Note this in your execution plans. You must also recommend that the user enable any missing **MCP servers** (universal or task-specific) that would optimally assist the current phase.

## Cost & Budget Optimization Mandate
**CRITICAL**: Loki Mode natively orchestrates swarms which can become extremely expensive. All sub-personas must assume a frugal posture, choosing efficient context retrieval over "load everything" approaches. If a specific atomic task requires heavy compute, remote SOTA reasoning, or large API cost spikes, the orchestrator **must present the cost-tradeoff and ask the human user for explicit approval** before delegating that task.

## Dynamic Persona Selection & Delegation
The per-phase persona assignments below are the **safe default**, not a straitjacket. Use `coordination/persona-selector.skill` to adapt:
- **Select the best persona(s)** per task by relevance + scope + past success, and **tier by cost** — route to the cheapest persona + model tier that clears the task's complexity bar (keep persona, drop model tier, for simple work; reserve SOTA for hard/critical tasks). Biggest cost lever in swarm work.
- **Persona→persona delegation is a contract** (task spec, constraints, eval metric = the existing quality gates, output schema, budget) with a negotiation phase that may early-reject ambiguous work. Personas may invoke skills directly as needed.
- **Consensus voting (k-threshold)** is available for high-stakes/ambiguous decisions (security/compliance/architecture) — cost-gated; default to deterministic single-persona execution otherwise.
- **Bounded self-refinement:** personas may improve from *successful* outcomes only (misaligned-replay guard), reversibly and audited; core mandate + security scope stay immutable. (DB-backed `persona_genes` evolution is v2.)
- **Validate every target** against the approved persona registry — never delegate to a hallucinated persona.

---

## Operating-Spine Integration (run the spine, don't bypass it)
Loki orchestrates, but it MUST use the same operating spine as every other agent
(AGENTS.md Step 0 + §13) — do not rely only on the older Pre-Start/Memory/Interruption
sections below:
- **First action:** run `core/preflight.skill` (auto-checks + load index summaries +
  memory headers + cost posture + recommend the optimal set), then `core/update-scan.skill`
  (gated discovery), then `core/clarify.skill`. Only then do the Pre-Start Check.
- **State preservation:** maintain `agents/memory/RESUME_POINTER.md` via `core/state-preserve.skill`
  continuously — refresh it at every checkpoint and before any interruption (see Interruption Handling).
- **Before sign-off:** run `core/final-review.skill` as part of S08 (and after S06) — an
  independent expert pass (correctness/security/observability/spec/cost) before any human gate.

## Pre-Start Check

Before doing anything else (after preflight above):

```
1. Check: does agents/memory/PROJECT_STATE.md exist AND phase is a real lifecycle
   phase S00–S13 (i.e. NOT one of: absent, NOT_STARTED)?
   - YES → This is a RESUMED project → invoke session-resume.skill first
           Load all memory (RESUME_POINTER first), then continue from the current phase
           (S00 Day-0 strategy and S11–S13 Day-2 phases are real phases — resume into them)
   - NO  → This is a NEW project → proceed with INIT below
```

---

## INIT (New Project Only)

```
1. Create directory structure if missing:
   mkdir -p agents/memory/episodic/SESSION_SNAPSHOT
   mkdir -p agents/memory/semantic
   mkdir -p agents/personas

2. Initialize memory files:
   - agents/memory/PROJECT_STATE.md    → set phase: S01, status: IN_PROGRESS
   - agents/memory/AUDIT_LOG.md        → write header + first entry: LOKI_INIT
   - agents/memory/CONTINUITY.md       → write header (empty failures list)

3. Announce to user:
   "Loki Mode initialized. Starting [PROJECT_NAME] from scratch.
    Current phase: S01_REQUIREMENTS
    All checkpoints will be saved to agents/memory/"
```

---

## Orchestration Loop — 14-Phase Lifecycle (S00–S13)

Run each phase in order; gate before advancing. The lifecycle is **14 phases**: a 10-phase
**core** build loop (S01–S10) bracketed by Day-0 strategy (S00) and Day-2 operate/evolve/sunset
(S11–S13). **Full per-phase detail (personas, tasks, outputs, gates, checkpoints) lives in
`agents/guides/processes/loki-sdlc-phases.md`** — load it on demand when orchestrating.

| Phase | Persona(s) | Output | Gate |
|---|---|---|---|
| S00 Strategy & Discovery (Day-0) | prod-research, prod-pm | problem statement, opportunity assessment, North-Star/HEART, RICE | HUMAN GO/NO-GO |
| S01 Requirements | prod-pm | PRD.md (EARS) | HUMAN APPROVAL |
| S02 Architecture | prod-architect, ops-security | PLAN.md, C4, ADRs, THREAT_MODEL | HUMAN APPROVAL |
| S03 Tech Spec | prod-tech-lead | SPEC.md, OpenAPI, schema | approval (lighter/async) |
| S04 Task Decomp | prod-tech-lead, orch-planner | project/TASKS.md (atomic, 15-min) | orch-judge review |
| S05 Implementation | orch-planner + eng-* | code + tests (RARV per task) | VERIFY green |
| S06 Testing & Quality | eng-qa, orch-judge | quality-gate report + final-review | all gates PASS |
| S07 Security Review | ops-security, eng-qa | SECURITY_REVIEW.md, checklist | security sign-off |
| S08 Human Review | prod-tech-lead, orch-judge, prod-ethicist | review summary | DOUBLE VERIFY + HUMAN APPROVAL |
| S09 Staging | ops-devops, eng-qa | staging deploy + smoke tests | smoke green |
| S10 Production | ops-devops, ops-sre | prod deploy (canary) | healthy 15+ min → live |
| S11 Operate & Maintain (Day-2) | ops-sre, ops-monitor, ops-incident, ops-cost | runbooks, SLO report, dependency status | SLOs met + budget healthy |
| S12 Evolve & Improve (Day-2) | prod-product-ops, prod-pm | retrospective, A/B experiments, improvement backlog | actions logged + DORA/SPACE reviewed |
| S13 Decommission & Sunset (Day-2) | prod-pm, ops-sre, biz-legal | decommission plan, data retention/migration, user comms | sunset approved + data archived |

> **Day-0 / Day-2 note:** S00 is the Day-0 strategy & discovery phase (runs before S01);
> S11–S13 are the Day-2 phases (operate, evolve, sunset) that run after the system is live.
> The core build loop remains S01–S10. Full per-phase detail for all of S00–S13 lives in
> `agents/guides/processes/loki-sdlc-phases.md`.

Each phase ends with `sdlc-checkpoint.skill` (snapshot + PROJECT_STATE + AUDIT_LOG). Hard
human-approval gates: S00 (GO/NO-GO), S01, S02, S07, S08. Persona selection is dynamic
(`coordination/persona-selector.skill`) on top of these defaults.

## Interruption Handling

Use `core/state-preserve.skill` — save state CONTINUOUSLY (assume a cutoff can happen
at any moment), not only at a graceful exit:

```
CONTINUOUSLY (after each meaningful step):
  - Refresh agents/memory/RESUME_POINTER.md (current task + the precise NEXT ACTION)
  - Append the outcome to AUDIT_LOG.md
  - Pre-exhaustion flush: when budget/tokens/turns run low, write a full snapshot FIRST

On graceful exit:
  1. Complete current task if < 50% remaining work
  2. sdlc-checkpoint.skill → save mid-phase snapshot
  3. Update PROJECT_STATE.md + RESUME_POINTER.md with exact position + NEXT ACTION
  4. Log: AUDIT_LOG.md → SESSION_END

On unexpected interruption (context limit, crash):
  - Next session: session-resume.skill reads RESUME_POINTER.md first, then detects
    incomplete tasks; any BLOCKED task appears in the resume report
  - Resume from the RESUME_POINTER NEXT ACTION / last DONE task
```

---

## Human-in-the-Loop Protocol

Loki Mode requires human approval at these gates (consistent with `sdlc-checkpoint.skill`):
- **S00**: Strategy & discovery GO/NO-GO (problem statement, opportunity) — hard stop before any build
- **S01**: Requirements approval (PRD.md) — hard stop
- **S02**: Architecture approval (PLAN.md + threat model) — hard stop
- **S07**: Security sign-off (SECURITY_REVIEW.md — accepted risks / no HIGH findings)
- **S08**: Final code review before deployment — hard stop
- (**S03** is a lighter, may-be-async review — not a hard stop.)

Loki Mode escalates to human when:
- Self-heal loop exhausted (5 attempts, still failing)
- Architecture change needed (beyond original PLAN.md)
- Security finding with HIGH severity requiring policy decision
- Conflicting requirements found in PRD/SPEC
- CONSTITUTION.md amendment needed
- Any BLOCKED task after 24 hours

Human responses must be recorded in AUDIT_LOG.md before proceeding.

---

## Memory Management

Throughout the project:

```
After each task DONE:
  → audit-trail.skill: log TASK_DONE

After each self-heal resolution:
  → If root cause was non-obvious:
    Write to agents/memory/CONTINUITY.md:
    "Past failure: [what failed]. Root cause: [why]. Resolution: [what worked]."

After each research finding (from orch-researcher):
  → Write to agents/memory/semantic/PROJECT_KNOWLEDGE_TEMPLATE.md

After each SDLC phase:
  → sdlc-checkpoint.skill: write SESSION_SNAPSHOT
  → Update agents/memory/PROJECT_STATE.md
```

---

## Failure Escalation Protocol

```
Task fails:
  → self-heal.skill (attempts 1-4)
  → self-heal attempt 5 fails
  → orch-coordinator creates escalation:

Escalation report contains:
  1. Task ID and description
  2. Acceptance criteria that failed
  3. 5 attempts with: approach tried, error encountered, why it failed
  4. Research findings (from orch-researcher)
  5. Two recommended options for human decision
  6. Estimated impact of deferral

After escalation:
  → project/TASKS.md: task status → BLOCKED
  → AUDIT_LOG.md: HUMAN_ESCALATION entry
  → ALL autonomous work on this task stops
  → Project continues on unblocked tasks (if DAG allows)
  → Human responds → orch-coordinator applies decision → retry
```

---

## Output Format

At start of each phase:
```
[LOKI] Phase S0X — [PHASE NAME]
Persona(s): [list]
Goal: [one sentence]
Expected outputs: [list]
```

At end of each phase:
```
[LOKI] Checkpoint S0X — SAVED
Gate status: [PASS/PENDING HUMAN APPROVAL/BLOCKED]
Next: [next phase or waiting for human]
```

At interruption:
```
[LOKI] State saved to: agents/memory/episodic/SESSION_SNAPSHOT/
Resume with: "continue loki project" or "session-resume"
Current position: Phase S0X, Task T-NNN
```

---

## Constraints

- Never skip a required HUMAN APPROVAL gate
- Never advance a task to DONE without passing VERIFY phase
- Never modify AUDIT_LOG.md existing entries (append only)
- Never start S05 without S01-S04 checkpoints saved
- Never deploy to production without S07 security review
- Self-heal loop hard limit: 5 attempts per task
- Tasks must remain atomic: if scope grows, decompose further
- orch-judge has veto power over any phase completion

## Security & Guardrails

### Steps
## 1. Skill Security (Loki Mode)
- **Swarm Blast Radius**: Because `loki-mode` orchestrates multiple autonomous personas concurrently, a compromised sub-agent can execute tasks rapidly without individual human oversight. Loki must enforce mathematically rigid boundaries for each persona: a `prod-pm` persona must physically lack the kernel-level permissions to execute code, and an `eng-qa` persona must lack permissions to deploy or merge to the `main` branch.
- **Gate Override Protection**: The 14-phase lifecycle contains mandatory "HUMAN APPROVAL REQUIRED" gates (S00 GO/NO-GO, S01, S02, S07, S08). Loki is strictly prohibited from autonomously advancing `PROJECT_STATE.md` to the next phase without cryptographically verifying a Human-In-The-Loop interaction. The LLM must not be allowed to "hallucinate" human approval based on implicit context.

### 2. System Integration Security
- **Check-Point Integrity**: Loki utilizes `sdlc-checkpoint.skill` to save state. If an attacker manipulates the filesystem to alter `SESSION_SNAPSHOT` or `CONTINUITY.md` between phases, Loki will reboot into a compromised state. The orchestrator must generate hashes of critical checkpoints and verify them upon resumption to prevent rollback or state-tampering attacks.
- **Adversarial Double-Verification Veto**: In Phase S08 (Human Review), the "Double Verification Protocol" relies on `orch-judge` and `prod-ethicist`. The orchestration engine MUST grant these verification personas an unconditional, irrevocable veto capability. If `prod-ethicist` identifies a safety violation, Loki must transition the project directly to a `BLOCKED` state, overriding the `prod-tech-lead`'s progress.

### 3. LLM & Agent Guardrails
- **Self-Heal Escalation Spiral (The Sorcerer's Apprentice)**: The `self-heal.skill` (Phase S05) allows up to 5 attempts to fix failing code. The LLM might desperately try increasingly destructive fixes (like chmod 777 or deleting the test file entirely) to achieve a green build. The orchestrator must rigidly enforce that self-heal agents cannot alter environmental permissions or bypass the automated Security/Lint gates just to satisfy the compiler.
- **Delegation Hallucination**: During the `Delegation (A2A Check)` in S05, the LLM planner might hallucinate a non-existent agent persona (e.g., `eng-god-mode`) to rapidly resolve a complex dependency issue. Loki must validate all agent delegation targets against a hardcoded, static enum of approved system personas. If a target is unrecognized, it must fail safely back to the coordinator.

### 4. Experimental CLI Integration & Swarm Containment
- **Optional Enhancement**: The `gabbe` CLI is strictly optional. Loki Mode can be operated entirely as a conceptual orchestration framework driven exclusively by an LLM reading this markdown file (e.g., inside Cursor, Claude Code, or Copilot).
- **Platform Control Limits**: If utilizing the experimental CLI, Swarm engineering runs using multiple sub-agents can exhaust LLM tokens exponentially. `loki-mode` should strictly be operated inside the boundaries of `gabbe serve-mcp` or `gabbe verify` gateways so all API calls adhere to the budgets laid out in `PLATFORM_CONTROLS.md`.
- **Enforced Determinism**: When using the CLI, Loki commits its entire SDLC transitions to the SQLite internal `project/state.db`. If any sub-agent violates the `PolicyEngine` (such as accessing restricted tools), the RunContext halts Swarm execution and generates a `pending_escalation` requiring human remediation.

### 5. Agent-Only (CLI-Less) Execution Tactics
If the user invokes Loki Mode directly in a chat session *without* the `gabbe` CLI running, the LLM Orchestrator must use one of the following tactics to simulate the Swarm:
- **Tactic A (In-Context Simulation)**: The Orchestrator adopts the required Personas sequentially within its own response (e.g., Outputting `**[Persona: eng-qa]**: I have reviewed the code...`). Use this for fast, low-complexity tasks.
- **Tactic B (True A2A Subagent Delegation)**: For high-complexity tasks, the Orchestrator MUST NOT simulate the persona. Instead, it must generate a `delegation-payload.md` file containing the exact context, the target persona file path, and the sub-task. It then instructs the human "Router" to copy-paste this payload into a fresh, isolated online LLM instance (e.g., Claude, Gemini) and wait for the human to paste the subagent's result back into the main thread.
