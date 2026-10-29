---
name: control-session-orchestrator
description: Control-plane workflow for coordinating multi-agent, multi-session project work from a single Codex, GitHub Copilot, or agent-app control session. Use this skill whenever the user asks to orchestrate agents, create or steer worker sessions, run a workflow-like effort, fan out audits/research/migrations, coordinate parallel implementation streams, monitor other project sessions, or compare this control-session pattern to Claude Code dynamic workflows. This skill is especially relevant when the current session can spawn persistent project sessions and those sessions can spawn their own subagents, creating a two-level orchestration hierarchy.
---

# Control Session Orchestrator

Use the current session as the control plane for project work that is too broad, risky, or
stateful for one conversation. The control session owns intent, decomposition, routing, status,
verification, and consolidation. Worker sessions own scoped execution. Worker subagents are local
implementation/research/audit helpers inside each worker session.

## Mental model

```
User
  -> Control session (strategy, dispatch, tracking, integration)
       -> Worker project session A (persistent branch/workstream)
            -> Subagents for research, implementation, review, tests
       -> Worker project session B (persistent branch/workstream)
            -> Subagents for local fan-out
       -> Verifier/reviewer session (optional independent gate)
```

This is similar to dynamic workflows, but the orchestration is human-readable and session-native
instead of a runtime script. Use it when persistence, branches, PRs, human steering, or cross-session
continuity matter more than fully automated fan-out.

A code runtime gets reliability for free (validated results, barriers, budgets, dedup, resume). A
prompt-driven control plane only gets it if you make state machine-checkable. Two contracts do that
without a runtime: a required **worker result block** and a durable **control-state manifest** (see
[Machine-checkable contracts](#machine-checkable-contracts)). Everything else in this skill keys off
those two artifacts — without them, "is this worker done and passing?" is a guess, not a field read.

## Supported control apps

This skill is app-agnostic. First discover which orchestration tools are available in the current
session, then adapt the same control workflow to that surface.

| Capability | Codex app | GitHub Copilot app | Fallback |
|---|---|---|---|
| Find worker sessions | List/search project threads | List/search app sessions | Ask user for target session links/IDs |
| Create persistent workstreams | Create or reuse Codex threads/worktrees when available | Create or reuse Copilot app sessions/workspaces when available | Use local subagents only |
| Steer an existing workstream | Send a follow-up prompt to the thread | Send a follow-up prompt to the session | Ask user to paste the prompt into the worker |
| Local fan-out | Spawn subagents from this session or ask workers to spawn their own | Use Copilot's available agent/session tools | Keep work local |
| Tracking | Thread titles, pins, branches, PRs, canvas nodes, compact status tables | Session names, branches, PRs, issues, canvas nodes, compact status tables | Markdown status table |

Do not assume the GitHub Copilot or Codex tool names. Use the tools exposed in the current
environment, and say which control surface is active before dispatching workers.

## When to use

Use this skill for:

- Codebase-wide audits, migrations, or parity checks
- Parallel investigation across modules, services, features, or PRs
- Work that benefits from independent implementer and verifier sessions
- Large features where design, implementation, testing, and review should be split
- Project-control prompts like "coordinate agents", "spin up sessions", "run a workflow",
  "make workers handle this", "monitor the other sessions", or "act as control"
- Situations where worker sessions may themselves use subagents for local research, coding, or review

Do not use it for a simple one-file fix, a quick answer, or a task where a single local subagent is
enough. Orchestration has overhead; spend it only when coordination reduces risk or increases
throughput.

## Machine-checkable contracts

These are the session-native analog of a runtime's typed results and durable run state. They stay
human-readable, but they are **required**, not advisory — the control session parses them instead of
re-reading prose.

### Worker result block

Every worker MUST end its report with a fenced ` ```json ` block tagged `control-result`. The control
session reads this block (never the surrounding prose) to update state, dedup, and decide routing.

```json control-result
{
  "worker_id": "auth-api",
  "wave_id": "w1",
  "unit_key": "service/auth",
  "scope": "src/auth/** — refresh-token rotation",
  "status": "complete",
  "files_changed": ["src/auth/rotate.ts"],
  "verification": { "command": "pnpm test auth", "result": "pass", "evidence": "42 passed" },
  "subagents_used": "2 — one research, one test author",
  "risks": ["rotation interacts with logout; covered by test"],
  "next_step": "ready for review session",
  "report_ref": "thread/PR/path to the full report"
}
```

The block must be **strict JSON** (no comments/trailing commas) so it parses. `status` is one of
`complete | blocked | needs-decision | failed`; `verification.result` is one of `pass | fail | not-run`.

### Control-state manifest

One durable artifact that **is** the source of truth for the mission — a pinned control thread, a
tracking-issue body, a canvas node, or a committed `control/state.json`. Re-read and update it every
turn; keep the conversation for decisions, not state. One row per **unit** (unit-keyed, so the same
unit is never dispatched twice — this is the dedup ledger).

```json
{
  "mission": "MCP tool parity audit",
  "non_goals": ["no behavior changes"],
  "success_criteria": ["every tool present in server, HTTP, SDK, docs or flagged"],
  "budget": { "max_concurrent_workers": 5, "max_total_workers": 25, "spawned": 0, "in_flight": 0 },
  "convergence": { "rule": "single-pass", "k_empty": 2, "empty_streak": 0, "target": null, "current": 0 },
  "worker_contract": { "schema_name": "control-result/v1", "required_output_schema": null },
  "batch_guard": {
    "service_key": null,
    "pilot_unit_key": null,
    "pilot_status": "not-required",
    "pause_after_same_signature": 2,
    "paused": false,
    "failure_signatures": {}
  },
  "workers": [
    {
      "unit_key": "surface/http",
      "worker_id": "http-audit",
      "session_ref": "thread-or-session id/link",
      "scope": "HTTP API surface",
      "branch_or_pr": "—",
      "status": "pending",
      "wave_id": "w1",
      "last_update": "ISO-8601",
      "evidence_ref": "report_ref from the result block",
      "verification": "not-run",
      "blocker": null
    }
  ],
  "decisions": [],
  "open_followups": []
}
```

Rules:

- **Worker status** (what a worker self-reports in its result block): `complete | blocked |
  needs-decision | failed`.
- **Manifest unit status** (the superset the control session maintains): `pending | dispatched |
  needs-decision | blocked | stalled | complete | failed | dropped`. Worker-reported values are a
  subset of these, so setting a unit's status from a worker block (Step 5) is always valid.
- **Terminal** states — a unit is closed — are `complete | failed | dropped`. Everything else is
  non-terminal and must be resolved, or explicitly converted to `dropped` with a reason, before the
  mission closes (Step 8).
- `budget.in_flight` is the number of rows currently `dispatched`. Increment `spawned` and `in_flight`
  on dispatch; decrement `in_flight` when a unit leaves `dispatched`; recompute it from the rows on
  rehydrate.
- `convergence.rule` is one of `single-pass | loop-until-dry | loop-until-budget |
  accumulate-to-target`. `k_empty`/`empty_streak` are used only by `loop-until-dry`; `target`/`current`
  only by `accumulate-to-target` (`target` = the count or coverage goal, `current` = progress so far).
- `worker_contract.required_output_schema` stores the caller's exact structured-output schema when
  one exists. The default contract is `control-result/v1`; never paraphrase or silently replace an
  external schema.
- `batch_guard` records the pilot and normalized failure signatures for a homogeneous
  external-service batch. `service_key` identifies the shared dependency, not an individual item.
- dropped/failed units MUST carry a reason in `open_followups`.

This manifest is what a fresh control session rehydrates from (Step 0).

## Control workflow

### 0. Rehydrate (resume an in-flight mission)

On session start, look for an existing control-state manifest for this mission. If one exists:

- Load it; treat it as the source of truth.
- Re-attach to workers by `session_ref` and reconcile each worker's *real* status (read the thread/PR)
  before any new dispatch.
- Recompute `budget.in_flight` from the rows still marked `dispatched`.
- Do NOT re-dispatch a unit whose status is `dispatched` or `complete` — route a follow-up instead.

If no manifest exists, this is a new mission — create one during Step 1.

### 1. Frame the mission

Before spawning anything, capture (and write into the manifest):

- Objective and non-goals
- Repositories, branches, PRs, or issues in scope
- File or subsystem boundaries for each workstream
- Success criteria and verification gates
- Merge/integration expectations
- Any "do not touch" constraints
- The exact worker output schema, when the caller or execution surface requires one
- Any shared external service used by a multi-item batch

Also set explicit limits up front (manifest `budget` and `convergence`):

- `max_concurrent_workers` (default ~4–6) — never more in flight at once
- `max_total_workers` — a lifetime backstop for the whole mission (e.g. 25)
- optional token / cost / time ceiling
- the convergence rule: `single-pass` for bounded missions; `loop-until-dry`, `loop-until-budget`,
  or `accumulate-to-target` for open-ended audits/migrations/parity sweeps

If any boundary is ambiguous and could cause conflicting edits, ask before dispatch.

### 2. Detect the control surface

Before dispatch, identify the available app tools:

- Codex app: thread/session tools such as list, create/read, send-message, rename, pin/archive, plus
  optional local subagent tools.
- GitHub Copilot app: session or workspace tools exposed by the app connector, plus any available
  GitHub issue/PR/branch controls.
- Generic agent app: any combination of session, task, subagent, branch, issue, PR, or automation
  tools.

If no persistent-session tools are available, downgrade to a local multi-agent plan and explain the
limitation. Do not invent a backend.

### 3. Choose the topology

Pick the smallest useful topology:

- **One worker**: isolated implementation or bug fix that should live in its own project session
- **Parallel workers**: independent modules, packages, endpoints, tests, or docs
- **Research then implementation**: exploratory sessions report findings before coding starts
- **Implementer + verifier**: one session changes code, another reviews or verifies independently
- **Control-only**: no workers yet; just inspect state, list sessions, or plan the dispatch

Prefer separate sessions when workers may edit overlapping history, need different branches, or need
long-running context. Prefer local subagents inside one session when the task is exploratory and does
not need persistent branch state.

### 4. Dispatch workers with complete prompts

Respect the budget: **never dispatch while `in_flight >= max_concurrent_workers`** — queue the unit
(`status: pending`) and log it. On reaching `max_total_workers` or a token/cost ceiling, STOP
dispatching and surface a *Decision needed* rather than spawning more. Dispatch is an **atomic
manifest update**: set the unit's row to `status: dispatched` (with `session_ref`, `worker_id`,
`wave_id`, `last_update`) and increment `spawned` and `in_flight` together; if the dispatch fails to
start, leave the row `pending` and advance neither counter. Decrement `in_flight` when a unit leaves
`dispatched` (it reaches a terminal state, or returns to `needs-decision`/`blocked`/`stalled`) so
queued units can start. This keeps `in_flight` equal to the count of `dispatched` rows that Step 0
recomputes.

Each worker prompt should be self-contained. Include:

- The mission and exact scope (and its `unit_key`)
- Files, subsystems, issue/PR links, and branch expectations
- What the worker may and may not change
- Verification commands or acceptance criteria
- Whether it may create commits, PRs, or only report back
- The required output contract

Worker prompt template:

```text
You are worker <name> for <project>.

Mission: <specific outcome>
unit_key / wave_id: <key> / <wave>
Scope: <files/subsystems/issue/PR>
Do not touch: <boundaries>
Approach: <expected plan or constraints>
Verification: <commands/checks/evidence>
Required output schema: <exact JSON schema, or "control-result/v1">
Submission format: <default control-result block, or exact external-schema instruction>

You MAY use your own subagents for local research, implementation, and review, but you remain
accountable for this scope and the final report. Do NOT create or steer further persistent project
sessions — if the work needs another full workstream, say so in next_step.

Follow the submission format exactly and validate the payload against the required output schema
before submission. The control session reads only that payload.
```

For `control-result/v1`, set the submission format to a fenced `json control-result` block populated
with every field, including `subagents_used`. When a caller requires a different schema, store and
include that schema verbatim, including every required root key and type, and tell the worker to
return exactly that schema without a `control-result` wrapper. If the execution surface exposes
structured-output validation, configure it with the same schema; do not invent an argument for
surfaces that do not. Define and test a lossless adapter from the external schema into the control
manifest before dispatch. Without one, return `needs-decision` rather than approximating either
contract.

When using Codex app controls, prefer to rename and pin important worker/control threads so the
session graph stays legible. When using GitHub Copilot app controls, use the corresponding session or
workspace labels if exposed.

#### Pilot shared-service batches

Before dispatching a large homogeneous batch through one external service:

1. Set `batch_guard.service_key` and choose one representative `pilot_unit_key`.
2. Dispatch only the pilot; keep the remaining units `pending`.
3. Release the batch only after the pilot returns a schema-valid result and passes its acceptance
   checks.

Different item IDs do not make failures independent. If the same normalized failure signature
occurs on two distinct units, set `batch_guard.paused: true`, stop queued launches sharing that
service, and report the blocker. Resume only after the diagnosis or input materially changes, or
after an explicit decision accepts the risk.

### 5. Track state centrally

The control-state manifest is the single source of truth — update it every turn, not the
conversation. From each accepted worker result (after applying the tested adapter when required),
set the unit's `status`, `evidence_ref`, `verification`, and — when `status` is `blocked` or
`needs-decision` — `blocker` (otherwise `null`). For `control-result/v1`, these map from
`report_ref`, `verification.result`, and the blocking reason. The control session records the
remaining fields itself: stamp `last_update` from its own clock, and set `branch_or_pr` from the
worker's session/PR metadata when known. Keep the control session's context focused on summaries and
decisions, not full transcripts; the full report lives at `evidence_ref`.

Track at least, per unit: `unit_key`, `worker_id`, `session_ref`, scope, status, branch/PR, last
update, blocker, and verification state — matching the row schema above. Canvas nodes or a SQL/todo
table are good backends for the manifest when the app exposes them.

### 6. Route follow-ups (result-gate)

When a worker reports, first run the **result-gate**:

- Parse the payload required by `worker_contract`: the fenced `control-result` block for the default
  contract, or the exact external payload otherwise. If a required field is missing or malformed,
  do NOT accept it — send exactly one standardized re-prompt asking only for the corrected payload.
  Cap at 2 retries, then escalate to the user.
- For an external schema, validate every required root key, type, and enum before applying the tested
  adapter. A valid default control-result that violates the caller's exact schema is still invalid.
- After validation and any adapter, reject a completion whose status conflicts with its evidence.
  `status: complete` normally requires `verification.result: pass`.
- A completed source-backed read-only research unit may instead use `verification.result: not-run`
  only when its manifest scope and success criteria explicitly say runtime verification is out of
  scope, `files_changed` is empty, and its evidence cites the inspected sources and satisfies those
  criteria without making untested runtime claims. Record `not-run` truthfully in the manifest.
  Unavailable tooling, omitted checks, or any implementation/configuration change is not this
  exception and must be rejected as unverified work.
- Accept completed work only when the block validates AND meets the success criteria.

Then route:

- Send targeted follow-ups for missing verification, scope drift, or blockers.
- Avoid duplicating a worker's investigation unless its result is incomplete or suspect (check the
  unit ledger first).
- If two or more workers conflict, pause integration and resolve ownership before more edits happen.
- Normalize repeated external-service failures by removing volatile item IDs, request IDs, and
  timestamps. Record the signature and affected unit keys in `batch_guard.failure_signatures`; at
  the configured threshold, pause queued units sharing the service. A transient retry may use
  bounded backoff, but never fan out simultaneous retries against a service already showing the
  same failure.

### 7. Iterate waves to convergence

For multi-wave missions, after routing a wave's follow-ups, apply the declared `convergence.rule`
before consolidating:

- **single-pass** — one wave; skip to consolidate.
- **loop-until-dry** — keep opening units until `k_empty` consecutive waves produce zero *new*
  (deduped) units; maintain `empty_streak` in the manifest.
- **loop-until-budget** — stop when a budget cap is hit.
- **accumulate-to-target** — stop when the target count/coverage is reached.

"New" and "dry" are measured against the manifest's set of `unit_key`s, not memory. Never stop
silently — write why iteration ended (`open_followups` / `decisions`).

### 8. Verify and consolidate

Before declaring the mission done:

- Run or delegate the agreed verification gate.
- Review diffs or ask an independent reviewer session for high-signal findings.
- Ensure worker outputs are integrated in the right branch/session.

**Wave-join / completeness gate:** the mission is complete only when **every** manifest worker row is
in a **terminal** state — `complete`, `failed`, or `dropped`. Non-terminal rows (`pending`,
`dispatched`, `needs-decision`, `blocked`, `stalled`) must first be resolved; a unit that cannot be —
e.g. a worker that never reported by its checkpoint, marked `stalled` — must be explicitly converted
to `dropped` with a reason. Only then may the mission be declared *"complete with N dropped: <ids +
reasons>"*. Never close with a non-terminal row, and never drop silently. Enumerate every dispatched
unit in the final summary.

**Pull cadence (no push signal):** a session-native control plane has no "worker done" event to wake
it. After dispatching a wave, define the next checkpoint trigger — a follow-up turn, a status-table
poll, or a user ping — and never leave a wave un-joined.

For PR-bound work, keep the control session responsible for final PR readiness and review routing.

## Safety rules

- Do not spawn workers for trivial tasks.
- Do not let multiple workers edit the same files unless explicitly coordinated.
- Do not assume a named app connector exists; discover it and fall back honestly.
- Do not silently create branches, commits, pushes, or PRs; follow the user's consent and repo rules.
- Do not ask workers to share secrets or sensitive data across sessions.
- Worker subagents are leaf helpers — they MUST NOT create or steer further persistent sessions. The
  hierarchy is exactly two levels (control -> worker -> subagents); a worker that needs another full
  workstream reports that need to control.
- Enforce the concurrency and total-fan-out caps; never exceed them silently. Dropped, skipped, or
  failed units MUST be recorded with a reason (no silent truncation).
- Pilot large homogeneous external-service batches and pause repeated shared failure signatures.
- If using an in-place checkout, be extra careful: other user-owned changes may already exist.
- If the plan changes materially, update the user and the workers before continuing.

## Recommended reporting format

Use a compact control-plane update (rows derived from the manifest):

```markdown
**Status:** <on track | blocked | needs decision | complete>
**Budget:** in-flight <X/Y> · spawned <A/B> · wave <N> (empty-streak <E>)

| Workstream | Session | Scope | State | Evidence |
|---|---|---|---|---|
| <name> | <id/name> | <scope> | <state> | <test/report/PR> |

**Decision needed:** <only if blocked>
```

Keep user-facing updates concise. The control session should make coordination legible, not flood the
user with every worker's transcript.
