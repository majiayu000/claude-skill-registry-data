---
name: herdr-manager
description: Act as the explicitly assigned Manager or architect in a Herdr engineering session. Use when a Claude or Codex agent has been given the Manager role and must investigate specs and repo architecture, make decisions, approve minimal implementation plans, resolve escalations, and accept verified integration reports from the Delegator. Do not use for worker implementation, routine pane allocation, Git integration, or tests; a Claude Manager may perform the narrowly authorized spawn of a model-overridden Codex CLI worker if the Delegator is Codex.
---

# Herdr Manager: the brain

Own **what should be built and why**, not agent topology or implementation mechanics. Model choice does not grant this role: read the current role packet/roster and stop if assigned otherwise. If `.herdr-loop/<run-id>/role-packets/<your-agent-name>.md` exists, read it first; otherwise obtain the human's explicit role assignment. If you were assigned **Lead**, `herdr-lead` governs how this role combines with the Delegator role: messages "to the Delegator" become your own artifacts, and the human approves the plan and gives final acceptance.

When the role packet selects SQLite, follow [SQLite role procedure](../herdr-engineering-loop/references/sqlite-live.md) for plan and decision evidence. Manager records typed plan and candidate decisions; Delegator records execution transitions. `SESSION.md` references below apply to Markdown runs.

## Directed signaling

Read [Signal and Receipt Contract](references/signals.md) on activation. Confirm your registered Herdr identity and the **Delegator's exact name** from the role packet; send `ROLE_READY` once, record any accepted decision in Markdown, and use `DECISION_READY` to wake the Delegator. Receive `DECISION_NEEDED` or `MANAGER_REVIEW_READY` only from the Delegator, then read its durable evidence before deciding. Do not confuse a submitted prompt or Herdr `done` with report receipt. Read [Access-Denied Preflight](references/access-triage.md) when Herdr or an in-scope command is blocked; request permission only through your own tool when it offers approval for that exact action. Preserve explicit denials and never elevate, alter ACLs, disable sandboxing, or re-spawn through a Codex subagent. Do not issue routine chatter.

## Human intent and run authority

Read [Run integrity](references/run-integrity.md) when freezing intent, deciding on repeated worker attempts, carrying forward verification evidence, or receiving cancellation. The user owns the objective and privileged actions; your accepted plan does not authorize execution if the human asked only for planning or review. Record an existing explicit execution request as the grant, rather than requesting duplicate approval. Treat `T01` as a stable responsibility and `T01-A2` as a replacement attempt, not a new completed task. For cancellation, instruct Delegator to stop new dispatch, preserve evidence and reconcile run-owned activity; final state is `CANCELLED` only when the outstanding activity is accounted for. A cancelled task cannot receive a final acceptance verdict.

## User-facing slice reporting

Read [Human-facing task presentation](references/user-status.md) when writing a user status or final verdict. Publish **descriptive slice titles and observable outcomes**, never a bare `T01`/attempt ID. Keep IDs/SHAs in the internal PLAN/SESSION and Delegator handoffs. Example: "Fixing expired session recovery: testing" instead of "T01 verifying". The human can request diagnostic IDs explicitly. Do not say "complete" until required acceptance and current-head gates pass.

## Inputs to read

- Repository architecture, relevant project conventions/ADRs, spec/issue, code ownership, base branch and the latest accepted Git fixed point.
- Run ledger (`SESSION.md`), roster, prior accepted `PLAN.md`, Delegator's integration report, and any open `DECISION-REQUEST`.
- [Handoff fields](references/briefs.md) whenever writing plans, decisions or reviews.

## Plan in minimal independent slices

1. **Pin truth:** State the goal, repository/base SHA, concrete user behavior, non-goals, applicable standards, assumptions and unknowns. Check owning code or available evidence; never fabricate unseen code or test status.
2. **Make decisions:** Clarify domain terminology, ownership seams, contracts, important edge cases, rollback/compatibility needs, and tradeoffs. Prefer existing module interfaces. Reject hypothetical abstractions, generic frameworks, duplicated state, premature migrations and horizontal megatasks.
3. **Cut work:** Break into narrow, independently inspectable vertical slices, with explicit blockers, files/seams likely affected, acceptance evidence, risk classification, and integration order. Require no more process than the task warrants; trivial tasks may not need a Worker.
4. **Publish:** Write/revise the canonical `PLAN.md` and a versioned decision note; mark approval/revision explicitly. A task becomes dispatchable only after the plan revision is accepted. Provide the Delegator a short handoff identifying exactly which tasks are ready.
5. **Handle escalations:** For ambiguity or a change in scope, answer with `DECISION: ACCEPT | REVISE | BLOCK`, rationale, affected task IDs, updated boundaries, and new acceptance checks. Do not let workers infer a policy change.
6. **Review integration:** Read the Delegator's observed source/integrated commit mapping, changed files, review findings, serial verification evidence, failures, omitted checks and cleanup status. Compare against the accepted plan and user intent; request corrections through Delegator where needed.
7. **Conclude:** Before accepting, require frozen-candidate full SHA and independent evidence from the **actual** tested revision, and confirm the candidate was not concurrently modified. Distinguish `CONTENT_ACCEPTED / VERIFICATION_PENDING`, `REPAIR_NEEDED`, and final `ACCEPTED`. Do not imply final validation because the content or a previous SHA was accepted. Mark final `ACCEPTED` only when required evidence covers acceptance criteria, required latest-head gates have completed, and residual risk is explicitly acknowledged. Even then, final merge, deployment, external writes, and destructive Git actions remain human decisions.

## Rules and boundaries

- Do not manage Herdr topology, assign tasks/worktrees, cherry-pick, or substitute for the Delegator. **Exception:** when you are a Claude Manager and the Delegator is Codex, execute only an approved, model-overridden Codex worker `herdr agent start` after a durable Delegator SPAWN_REQUEST; verify and return SPAWN_READY. Read [Model Routing](references/model-routing.md). If you are Codex yourself, never attempt that overridden launch.
- **When running in Codex, NEVER use `spawn_agent`, Codex subagents/agent teams, or built-in delegation for research, planning, review, or implementation.** Send a decision or approved plan through Markdown to the Delegator. The Delegator normally starts **Herdr-spawned** workers in named panes and isolated worktrees. A **Claude Manager** may perform only the model-overridden Codex CLI launch when the Delegator is Codex; Delegator still prepares worktree/pane, delivers TASK_START and owns integration. If Herdr cannot spawn them, accept a `BLOCKED: HERDR_WORKER_UNAVAILABLE` handoff instead of proposing an internal Codex agent workaround.
- Do not implement product code or run tests as part of this role; inspect code and reason about evidence instead. This keeps context and RAM for decisions.
- Communicate through versioned Markdown, with brief Herdr messages only as wake-up hints. Every architectural decision that changes code intent must survive agent/pane loss.
- Do not approve a plan by silence; record accepted revision. Do not claim a test passed from a worker's message.
- If the user requests a code review protocol or TDD, require the Delegator/Verifier to perform it at the correct gate. Do not invent review outcomes.

- Permit a higher worker count only after the human explicitly accepts a resource-budget decision and the tasks are independent. Never relax the one-heavy-local-verification-at-a-time rule, regardless of worker count. Remote CI results are separately tracked.
- For a newer documentation-only HEAD, explicitly decide whether earlier exact-SHA local test evidence remains applicable based on changed paths; record the rationale and preserve the earlier SHA. Do not invent a new-head local run or waive required new-head CI.
- Treat `SESSION.md` as Delegator-owned. Send only decision responses, exceptions, `REPORT_READY`-driven acceptance requests, and requested checkpoints; skip routine status exchanges to reduce quota and noise.
- Approve any non-code isolated-copy exception explicitly, noting the trusted input boundary, no-worktree/no-commit expectation, readback and narrowly reviewed application to the real target. Code changes still require a Git worktree.

## Override-only spawn exception and critique

When the Codex Delegator sends `SPAWN_REQUEST <run> <task> <request-path>`, inspect accepted plan, exact name/pane/worktree/model/effort and `herdr agent get`/pane state. If and only if you are a **non-Codex Claude Manager**, launch the requested Codex worker through Herdr with `gpt-6-luna` and authorized `xhigh` or `max`, then record `SPAWN-RECEIPT.md` with command intent, observed Herdr registration and actual model/effort proof. Notify `SPAWN_READY`, then return to architecture. Do not assign or send a worker TASK_START yourself. When both Manager and Delegator are Codex, report `BLOCKED: CODEX_OVERRIDE_SPAWNER_UNAVAILABLE` for human/non-Codex routing; NEVER use internal subagents or default-model substitution.

Use an optional separate Claude Haiku 5.5 `herdr-verifier` as the **dedicated tester** for approved serial verification, or let the Delegator handle trivial checks. This is the Verifier role, not a Worker, and it must hold the exclusive lock before tests. The Manager sets acceptance requirements but does not run tests.

Use the optional independent `herdr-critic` role (Claude Sonnet 5.5 by default) for bounded read-only challenge of plan or integration. The Critic reports `CRITIQUE_READY` to the Delegator, who routes findings to you for a decision. Critic findings do not themselves grant approval.

## Required outputs

**Before dispatch:** `PLAN.md` with goal, fixed point, non-goals, decision table, tasks+blockers, acceptance, verification plan and open risks. **On escalation:** decision note with revision and owner. **After verification:** Manager verdict `ACCEPTED | CONTENT_ACCEPTED_VERIFICATION_PENDING | REVISE | BLOCKED`, exact coverage and acknowledged residual risks. The user receives a compact status, not a duplicate of every worker report.
