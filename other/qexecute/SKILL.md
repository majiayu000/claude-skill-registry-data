---
name: Qexecute
description: "Use when a routed pipeline or an active task artifact (TASK_REQUEST UUID) needs execution or the -verify quality loop — router-owned internal PSE unit. Use Qgoal to enter."
user_invocable: false
recommendedModel: haiku
tier: core
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

> **`.qe` reads → DB:** `.qe/` content is stored in the SQLite store (`qe_files`), so a path may have **no file on disk**. Read `.qe/` content with `node scripts/qe-cat.mjs <path>` (or `--ls`/`--exists`) and structured state with `node scripts/qe-query.mjs …` — do not assume the raw file exists. See `QE_CONVENTIONS.md`.

# Qexecute — Unified Execution Engine

> Internal PSE unit. Users start work with `{adapter.commandPrefix}Qgoal {목표}`; `user_invocable` is catalog/documentation metadata only. Runtime enforcement is the G010 PreToolUse gate, while active UUID artifacts preserve in-chain continuity.

## Role
The single entry point for executing spec documents. Qexecute consolidates the three former
execution engines — sequential run, parallel-wave atomic, and the code quality loop — into one
skill. It reads the actual `TASK_REQUEST` — not the user's phrasing — to decide **how** to execute.

> **MANDATORY:** All user confirmations MUST use the interaction adapter. Claude MUST use
> `AskUserQuestion`. Codex interactive may use concise plain-text choices. Codex
> non-interactive selects the documented recommended default only when the action is
> reversible and reports it; destructive ambiguity must stop.

## Flag Grammar

| Invocation | Mode | Behavior |
|------------|------|----------|
| `Qexecute {UUID}` | **default** | Read the spec → classify → **sequential** or **parallel wave** |
| `Qexecute -verify {UUID}` | **verify** | test → review → fix → retest quality loop on already-changed code |
| `Qexecute -utopia …` | **modifier** | Fully autonomous: no-confirmation / auto-approve, combines with default or `-verify`. Sub-flags `-ralph`, `off`, `status`. See “-utopia — Fully Autonomous Execution”. |

- Flags use a **single dash**. `-utopia` is a modifier (combinable); `-verify` and default
  are mutually exclusive execution axes.

## Client Adapter Compatibility
- **Claude**: approvals/next-task prompts use `AskUserQuestion`; delegation uses the Agent tool.
- **Codex native**: prefer native subagents via installed agent TOML (`model` /
  `model_reasoning_effort` derived from `recommendedModel`).
- **Codex client adapter**: role-separated inline execution only when native subagent dispatch
  is unavailable; mark the fallback explicitly.
- **Command rendering**: user-visible handoffs use `adapter.commandPrefix` (`/Q…` Claude, `$Q…` Codex).

---

# Default Mode — Execute a Spec

## Step 1: Document Discovery

**Plan Knowledge Pull:** Qplan performs knowledge retrieval before it creates this internal
execution task. If the task needs more context, use `node scripts/qe-plan-context.mjs "<task intent>"`
and verify selected source documents; do not invoke a user-facing wiki workflow.

1. **State utility**: call `parseClaudeTaskTable(cwd)` from `hooks/scripts/lib/state.mjs`
   (prefers `.qe/TASK_LOG.md`, falls back to the legacy Claude task table).
2. Glob `.qe/tasks/{pending,in-progress,on-hold}/*.md` for TASK_REQUEST files.
3. Backward compat: check project root if `.qe/tasks/` is missing.
4. UUID argument → select directly. No argument + multiple tasks → ask which to run.
5. Multiple space-separated UUIDs → see **Multiple UUID Execution**.

## Step 2: Summary and Approval

Read TASK_REQUEST + VERIFY_CHECKLIST and show a summary.

**Chained skip:** if TASK_REQUEST contains `<!-- chained-from: Qgenerate-spec -->`, skip the
approval prompt (already approved in Qgenerate-spec) and remove the comment after reading.

Otherwise get approval via the interaction adapter. On approve:
- Move files to `in-progress/`.
- **Status**: call `updateClaudeStatus(cwd, uuid, "🔶")`.

## Step 2.5: Classification — Sequential vs Wave

Parse the TASK_REQUEST checklist and decide the execution shape:

```
WAVE  when ALL hold:
  1. checklist items ≥ 5
  2. topological sort by `depends`/`depends_on` tags yields a max wave width ≥ 2
     (i.e. ≥ 2 items can run at once)
  3. file ownership is non-overlapping — no two items write the same `→ output:` path
SEQUENTIAL  otherwise
```
- No tags → let `Etask-executor` infer dependencies from file paths (existing behavior).
- `--worktree` (opt-in) requests isolated per-item execution when two+ items must touch the
  same file in one wave; default is in-place.

### Code Risk Gate (`type: code` — hard block)
Before any implementation worker starts, enforce:
- TASK_REQUEST has a `## Risk Register` with all six fields filled: worst-case failure,
  data loss/corruption risk, security/permission risk, concurrency/race risk, rollback
  strategy, and unverified assumptions.
- The paired VERIFY_CHECKLIST has checks for worst-case failure, data/security/concurrency
  risk evaluation, unverified-assumption/residual-risk reporting, and high-risk
  mitigation/defer rationale.
- Empty fields, placeholder text, or missing paired checks → route back to
  `{adapter.commandPrefix}Qgenerate-spec` or amend the spec. Do not start execution.

## Step 3: Execute

### Plan-owned micro-Goal handoff

Qplan may invoke execution without a TASK_REQUEST only when its immutable Goal
acceptance contract contains the ledger-validated `assurance.lane=bounded-micro`
declaration defined by `core/GOAL_ACCEPTANCE_CONTRACT.md`. Task size alone is not
an admission signal.
That contract replaces only the formal Spec artifact and Spec/Supervise fan-out;
it does not waive TDD applicability, locked command execution, regression evidence,
distinct-session machine verification, or Goal-alignment review. Scope growth,
new high-impact risk, or verification failure returns control to Qplan, which
blocks the immutable micro Goal and creates a linked formal successor Plan/Goal;
it never rewrites the original assurance. Direct Qexecute entry never
self-declares this exception.

### TDD Applicability Gate (R004 — scale-aware)

For `type: code`, call `judgeTddPolicy()` from `qexecute-tdd-policy.mjs`.
When `apply=true`, enforce RED → GREEN → REFACTOR: prove the new test fails
for the intended reason, implement the minimum passing behavior, then refactor
without losing GREEN. Docs/analysis, config-only work, or absent test
infrastructure records `formatExclusionHandoff()` and skips TDD. Full signal,
contradiction, and completion rules: [./reference/execution-protocol.md](./reference/execution-protocol.md).

### Execution routing

Delegate bounded work to `Etask-executor` under `core/AGENT_DELEGATION_CONTRACT.md`.
Sequential work preserves checklist order. Wave work requires five or more items,
topological width of at least two, and non-overlapping output ownership; use
worktree isolation or fall back to sequential. The Lead synthesizes envelopes
and runs final verification once.

### Lifecycle Cleanup

The Lead calls `wait_agent` and `close_agent` for every handle and records
`completed`, `failed`, `timed-out`, or `stale`. The final report states
`open handles: 0` or lists each stale warning.

### SIVS Single-AI Role Contract

The active client owns Implement, Verify, and Supervise. Native same-client
subagents are preferred; unavailable delegation uses `mode=degraded-inline`,
never a cross-client bridge. Verify is the evidence gate and Supervise is the
merge-readiness gate. Detailed execution, wave, and lifecycle rules:
[./reference/execution-protocol.md](./reference/execution-protocol.md).

## Step 4: Final Verification

Verify every checklist item with concrete evidence and run the cross-phase
regression gate for code. TDD-applicable items require their test file plus a
fresh post-refactor GREEN run. Auth, crypto, payment, credential, or secret
changes require `Esecurity-officer`.

For code, invoke `Esupervision-orchestrator`; WARN is remediated and rechecked,
FAIL creates a request using
[`core/REMEDIATION_REQUEST_FORMAT.md`](../../core/REMEDIATION_REQUEST_FORMAT.md).
The adversarial owner remains
`Qcritical-review --stage supervise`. Before completion run `-verify`, including
the final **Risk Proof Gate** via `Qcritical-review --risk {UUID}`. Missing or
unknown HIGH/CRITICAL risk evidence is a hard block.

The verify loop is owned by `Eqa-orchestrator`; see
[./reference/execution-protocol.md](./reference/execution-protocol.md).

## Step 5: Completion

Mark both documents `[x]`, write and verify their completed destinations before
removing in-progress sources, update TASK_LOG to ✅, and reset the UUID loop
counters. Preserve unrelated artifacts. Report changed files, verification,
Facts, Residual Risks, Assumptions, and the next pending task. Detailed state
and safe-move rules: [./reference/autonomy-and-state.md](./reference/autonomy-and-state.md).

# Verify Mode (`-verify`)

Run test → review → fix → retest through `Eqa-orchestrator`, at most three
iterations. Required gates are regression, smoke, Nyquist coverage, comment
coverage, adversarial Verify, and Risk Proof. The test and review first passes
receive the same source evidence but not each others verdict.

**Loop limit: 3 iterations** (confirm continuation via the interaction adapter each round).

# `-utopia` modifier

`-utopia` auto-approves only reversible recommended defaults; destructive
ambiguity still stops. `-ralph` repeats incomplete work without weakening any
gate. `off` disables continuation and `status` is read-only. Multiple UUIDs may
run as a bounded wave only when write ownership is disjoint.

State, safety, autonomous-mode, and handoff details:
[./reference/autonomy-and-state.md](./reference/autonomy-and-state.md).

## Role Constraints

- Execute only the selected TASK_REQUEST and paired VERIFY_CHECKLIST.
- Preserve unrelated user changes and obey build admission.
- Route commits through Qcommit and version/release work through Qrelease.
- Never report completion before checklist, evidence, safe move, and TASK_LOG are complete.
