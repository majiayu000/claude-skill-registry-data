---
name: loop-engineering
description: Patterns, conventions, and guardrails for the closed-loop systems in AegisNex. Covers the AI intelligence graph, Guardian auto-restart, multi-agent orchestration, incident lifecycle, self-improvement memory, and risk/policy gates.
license: MIT
---

# Loop Engineering for AegisNex

You are an engineer who understands that AegisNex is built on closed feedback loops. Every major subsystem — the AI engine, container guardian, agent orchestration, incident management — operates as a cycle that observes, decides, acts, and learns. When you modify code, add features, or fix bugs, you think about which loop the change lives in, what invariants the loop depends on, and whether your change preserves the loop's termination guarantees.

## The six loops

AegisNex runs six interlocking loops. Know which one you are in before writing code.

### 1. AI Intelligence Loop (LangGraph StateGraph)

**Files:** `src/intelligence/graph.py`, `src/intelligence/nodes.py`, `src/intelligence/state.py`

This is the core autonomous reasoning cycle. A user request enters, and the system plans, executes tools, reflects on results, verifies outcomes, and loops back if the goal is not achieved.

```
START → planner → tool_router → tool_executor → reflection → verifier → rag_generator → goal_evaluator → finish → END
              ↑                                                       │                    │
              └──────────── loop back if goal incomplete ◀────────────┘
```

**Node responsibilities:**

- `planner` (`nodes.py:276`): Retrieves RAG context, uses LLM or keyword matching to select tools, builds `current_plan` and `parallel_batches`. Populates `objective`, `evidence`, `retrieved_context`.
- `tool_router` (`nodes.py:82`): Maps abstract plan steps to concrete registered tools. Never executes. Produces `tool_router_results` with routing decisions and metadata.
- `tool_executor` (`nodes.py:444`): Runs each tool in the plan, respects batch ordering, creates `pending_approvals` for destructive actions. Populates `tool_results`.
- `reflection` / `self_corrector` (`nodes.py:682`): Examines errors, applies corrections (e.g., substituting tools when Docker is unavailable), increments `retries`. Max retries is 3.
- `verifier` (`nodes.py:562`): Computes `confidence` as `successful_tools / total_tools`. Populates `observations`, `evidence`, `reasoning_summary`, `remaining_uncertainty`.
- `rag_generator` (`nodes.py:744`): Calls the LLM provider to generate a natural-language answer from retrieved context and tool results.
- `goal_evaluator` (`nodes.py:776`): Decides if the goal is achieved. Thresholds: confidence >= 0.6 with data = achieved; confidence >= 0.3 with data = achieved; retries exhausted = achieved (best-effort). Otherwise loops back.
- `learning` (`nodes.py:1110`): Runs at finish. Stores error→resolution patterns and success patterns in `ai_learnings` table.
- `risk_assessor` (`nodes.py:925`): Scores planned actions via `RiskEngine`. Sets `approval_required` for medium+ risk.
- `policy_checker` (`nodes.py:955`): Enforces 6 default policies. Can block actions or require approval.

**Key state fields:** `current_plan`, `parallel_batches`, `tool_results`, `confidence`, `retries`, `max_retries`, `goal_achieved`, `executed_steps`, `pending_approvals`, `corrections`, `errors`.

**Termination guarantee:** The graph always terminates because `max_retries` defaults to 3 and `_goal_router` forces `finish` when retries are exhausted. Never remove this bound.

**When modifying this loop:**
- New nodes must accept `AgentState` and return `AgentState`. Use `_make_step()` for execution log entries.
- Use `create_logger_for_state()` for structured logging. Call `logger.finalize(status)` and `add_execution_log_to_state()` before returning.
- Add conditional edges in `graph.py:build_graph()`, not inline. The `planner_router` and `_goal_router` functions control flow.
- If a node can fail, catch exceptions, append to `state["errors"]`, and return state (never raise).
- Tool results must include `{"status": "ok"|"error", ...}`. The verifier and goal evaluator depend on this shape.

### 2. Guardian Auto-Restart Loop

**File:** `src/guardian.py`

The Guardian monitors Docker containers and autonomously restarts failed ones with cooldown protection.

```
detect failure → create incident → check cooldown → check max attempts → restart → record attempt → verify → (loop or resolve)
```

**Key parameters (configured in `config.yaml`):**
- `restart_cooldown_seconds`: 300 (5 minutes between restart attempts)
- `max_restart_attempts`: 3

**Flow:**
1. `Guardian.run()` calls `SystemHealthChecker.run()` to get container statuses.
2. For each unhealthy container (stopped, error, or failed health check):
   - Creates an incident via `IncidentManager.create_incident()`.
   - Calls `_restart_decision()` which checks cooldown and max attempts.
   - If allowed: restarts the container, records the attempt, sends notification.
   - If denied: logs skip reason (`restart_cooldown` or `max_restart_attempts`).
3. When a container becomes healthy again, `_reset_restart_history()` clears its attempt counter.
4. All remediation actions are recorded via `StorageRepository.save_remediation_action()`.

**Termination guarantee:** The loop is bounded by `max_restart_attempts` (default 3) and the cooldown timer. A container that fails 3 times enters a cooldown-only state until manual intervention or recovery.

**When modifying this loop:**
- Never remove the cooldown or max-attempt checks. They prevent restart storms.
- New health checks must implement the `HealthCheck` protocol and return `HealthCheckResult`.
- Incident creation and remediation recording must both happen for audit trail integrity.
- The `_restart_decision()` method is the single decision point — add new guard conditions there.

### 3. Multi-Agent Collaboration Loop

**Files:** `src/agents/orchestrator.py`, `src/agents/registry.py`, `src/agents/domain_agents.py`

The orchestrator decomposes tasks, fans out to domain agents in parallel, resolves conflicts, and aggregates results.

```
task → supervisor decomposes → agents execute in parallel → conflict resolution → aggregation → supervisor reviews → shared state update
```

**Flow:**
1. `AgentOrchestrator.dispatch_task()` sends the task to the `supervisor-agent`.
2. The supervisor produces a `collaboration_plan` with `selected_agents`, `parallel_groups`, and `subtasks`.
3. `_run_agents()` fans out to selected agents using `asyncio.gather()` within parallel groups.
4. `_resolve_conflicts()` compares agent outputs on the same signal — higher confidence wins.
5. `_aggregate()` computes weighted confidence (average minus conflict penalty), merges tool results, collects pending approvals.
6. The supervisor reviews aggregated results via `collaborate()`.
7. Shared state is updated with the full trace.

**Conflict resolution:** When two agents report different values for the same signal, the agent with higher confidence wins. The conflict is logged with both values and the resolution source. Confidence penalty: 0.05 per conflict, capped at 0.25.

**When modifying this loop:**
- New domain agents must extend `BaseAgent` and implement `process()`. Return `AgentResult` with `success`, `summary`, `data` (containing `confidence`, `tool_results`, `pending_approvals`).
- Register agents in `build_default_agents()` in `domain_agents.py`.
- Conflict resolution is confidence-weighted. If you add agents that report signals, ensure they populate `data.primary_signal` with `signal`, `value`, and `source`.
- Parallel groups are defined by the supervisor. Sequential dependencies between agents must be expressed as separate groups.

### 4. Incident Lifecycle Loop

**File:** `src/incidents.py`

Incidents follow a strict state machine with full audit trail.

```
active → acknowledged → in_progress → resolved → closed
```

**States and transitions:**
- `active`: Created by Guardian, health checks, or manual report.
- `acknowledged`: Set via `update_incident(acknowledged_by=..., acknowledged_at=...)`.
- `in_progress`: Remediation underway.
- `resolved`: `resolved_by` and `resolved_timestamp` required.
- `closed`: Final state.

**Deduplication:** `create_incident()` checks for an existing active incident with the same `service_name` and `incident_type`. If found, it updates the existing incident rather than creating a duplicate.

**Notification integration:** Each state change can trigger notification providers (Email, Slack, Discord). The `notification_providers` list and `broadcast_callback` handle dispatch.

**When modifying this loop:**
- Never skip states (e.g., going from `active` directly to `closed`). Each transition must be justified.
- Always populate `resolved_by` and `resolved_timestamp` when resolving.
- New incident types must be added to the `_incident_type` mapping in `dashboard.py`.
- Deduplication depends on `service_name` + `incident_type`. If you add new types, test that duplicates are properly merged.

### 5. Self-Improvement / Memory Loop

**Files:** `src/intelligence/memory/sqlite_memory.py`, `src/intelligence/nodes.py` (learning_node)

The system learns from every execution cycle by storing patterns in the `ai_learnings` table.

```
execute → observe errors/success → extract root cause → store pattern → retrieve for future planning
```

**What gets stored:**
- **Error patterns:** When errors occur, the system stores `root_cause` (from error messages), `resolution` (from corrections applied), with category `tool_failure` and outcome `corrected` or `unresolved`.
- **Success patterns:** When the goal is achieved with high confidence (> 0.7), the system stores the request and plan as a `success_pattern`.

**How it's used:** The RAG engine's retrieval collectors include learnings as a source. Future queries can retrieve past patterns to inform planning decisions.

**When modifying this loop:**
- The `learning_node` runs at the `finish` node, after goal evaluation. Never skip it.
- Stored learnings must have `root_cause`, `resolution`, `service`, `severity`, `category`, `outcome`, `confidence`, and `tags`.
- If you add new error categories, ensure the RAG retrieval can surface them.
- Learnings are append-only. Never mutate or delete existing learning records.

### 6. Risk / Policy Gate Loop

**Files:** `src/intelligence/risk.py`, `src/intelligence/policy.py`

Every action passes through risk assessment and policy checking before execution.

```
plan action → risk_assessor → policy_checker → (auto-approve | require approval) → execute or wait
```

**Risk levels:** `none` (0.0), `low` (0.2), `medium` (0.5), `high` (0.7), `critical` (0.9).

**Risk factors:** Tool risk level, access mode (write operations score >= 0.5), destructive flag (>= 0.8), explicit approval requirement.

**Approval flow:** When `approval_required` is set to `True` in state, the workflow pauses at `goal_evaluator` (via `risk_router` in `graph.py`). The `pending_approvals` list tracks what needs human approval. The `human_approval_check()` function in `nodes.py:1166` gates the flow.

**Policy engine:** 6 default policies check context (environment, restart count, retry count, destructive flag). Policies can allow, deny, or require approval.

**When modifying this loop:**
- New destructive tools must have `destructive=True` and `requires_approval=True` in their tool definition.
- Risk thresholds are configurable via `AEGIS_AI_AUTO_EXECUTE_THRESHOLD` env var (default 0.3).
- Never bypass the risk/policy gate for write operations. The gate exists to prevent autonomous damage.
- If you add new policies, register them in `PolicyEngine._default_policies()`.

## Cross-cutting concerns

### AgentState is the contract

All loops communicate through `AgentState` (defined in `src/intelligence/state.py`). It is a `TypedDict` with 35+ fields. Every node reads from and writes to this shared state. When adding new fields:

1. Add the field to the `AgentState` TypedDict.
2. Add a default value in `initial_state()`.
3. Document what populates it and what consumes it.
4. Never remove a field that other nodes depend on without updating all consumers.

### Execution logging

Every node produces structured execution logs via `ExecutionLogger`:
```python
logger = create_logger_for_state("node_name", state)
logger.add_input({...})
logger.add_decision("category", "action", "reason")
logger.add_tool_call("tool_name", "status", input_params={}, output={})
logger.add_output({...})
log = logger.finalize("success"|"warning"|"error")
add_execution_log_to_state(state, log)
```

This creates an audit trail in `state["executed_steps"]`. Every node must produce a log entry, even when it skips or fails.

### Error handling pattern

Every node follows this error handling pattern:
```python
try:
    # node logic
    pass
except Exception as exc:
    logger.add_error(str(exc))
    log = logger.finalize("error")
    add_execution_log_to_state(state, log)
    state["errors"] = list(state.get("errors", [])) + [f"Node error: {str(exc)}"]
return state
```

Nodes never raise exceptions. They capture errors in `state["errors"]` and return state so downstream nodes can handle partial results.

### Confidence scoring

Confidence flows through the system as a 0.0–1.0 float:
- `verifier_node`: `successful_tools / total_tools`
- `goal_evaluator`: Uses confidence to decide achievement (>= 0.6 or >= 0.3 with data)
- `multi-agent`: Average confidence minus conflict penalty (0.05 per conflict, max 0.25)
- `_requires_manual_investigation()`: True when confidence < `AEGIS_AI_CONFIDENCE_THRESHOLD` (default 0.4)

### Testing loops

When writing tests for loop behavior:
- Test termination: Ensure loops terminate within `max_retries` iterations.
- Test the happy path, the retry path, and the exhausted-retries path.
- Mock LLM providers — never call real APIs in tests.
- Use `reset_graph()` in `graph.py` to clear the cached compiled graph between tests.
- Test that `AgentState` mutations are correct — check that nodes return properly updated state.
- For Guardian tests, mock `SystemHealthChecker` and verify restart decisions against cooldown/attempts.

### Adding a new loop

If you need to add a new closed-loop system to AegisNex:

1. **Define the cycle:** What does it observe, decide, act on, and learn from?
2. **Define termination:** What bounds the loop? (max iterations, timeout, confidence threshold, human gate)
3. **Define state:** What fields does it read/write? Add them to `AgentState` if it plugs into the intelligence engine.
4. **Define the decision point:** Where does the loop branch (continue vs. exit)?
5. **Define the audit trail:** What gets logged at each iteration?
6. **Write the guardrails first:** Implement termination guarantees and safety checks before the happy path.
7. **Test all three paths:** Success, retry/correction, and exhaustion/timeout.
