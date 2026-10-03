---
name: cortivex-mesh-coordination
version: 1.0.0
description: Enhanced mesh coordination with MeshResolver nodes for conflict detection, resolution strategies, and multi-agent file ownership
category: coordination
tags: [mesh, coordination, conflict-resolution, file-ownership, agents, resolver]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [conflict-detection, conflict-resolution, file-locking, ownership-tracking, merge-resolution, deadlock-detection]
---

# Cortivex Mesh Coordination (Enhanced)

This skill extends the base cortivex-mesh protocol with MeshResolver node capabilities, automated conflict detection, and resolution strategies adapted from SWARM's coordination patterns. While cortivex-mesh defines the file ownership protocol that every agent must follow, this skill adds the orchestration layer that detects, prevents, and resolves conflicts across the agent pool.

## Overview

In multi-agent pipelines, file conflicts are inevitable. Two agents may need the same file, an agent may hold a claim too long, or a complex refactor may touch files that another agent is reviewing. The MeshResolver node sits alongside the SwarmCoordinator and actively manages these situations:

- **Detects** potential conflicts before they occur by analyzing task scopes
- **Prevents** conflicts by pre-allocating file ownership based on task assignments
- **Resolves** conflicts using configurable strategies when they do occur
- **Detects deadlocks** when two agents are each waiting for files held by the other

## When to Use

- Pipelines with 3+ agents that may modify overlapping files
- Refactoring or migration pipelines that touch many files across the codebase
- When agents have long-running tasks and file claims may expire before completion
- Pipelines where conflict-related failures have occurred in previous runs
- Any orchestrated pipeline where you want proactive conflict management rather than reactive error handling

You do NOT need a MeshResolver for:

- Pipelines where agents work on strictly separate file sets
- Read-only analysis pipelines (no file modifications)
- Single-agent pipelines

## How It Works

### Conflict Detection

The MeshResolver continuously monitors the mesh state and detects conflicts in three categories:

**1. Direct Conflicts** -- Two agents attempt to claim the same file simultaneously.

```
Agent A claims src/auth/login.ts for "auto-fixing"
Agent B claims src/auth/login.ts for "refactoring"
--> MeshResolver detects: direct conflict on src/auth/login.ts
```

**2. Scope Overlaps** -- Two agents' task scopes cover the same directory or module, creating a high probability of future conflicts.

```
Agent A assigned to "refactor src/auth/ module"
Agent B assigned to "add input validation to src/auth/ endpoints"
--> MeshResolver detects: scope overlap on src/auth/
```

**3. Deadlocks** -- Two or more agents are each waiting for files held by the other, creating a circular wait.

```
Agent A holds src/auth/login.ts, waiting for src/auth/session.ts
Agent B holds src/auth/session.ts, waiting for src/auth/login.ts
--> MeshResolver detects: deadlock between Agent A and Agent B
```

### Resolution Strategies

The MeshResolver supports five resolution strategies, configured per-pipeline or per-conflict:

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `priority` | Higher-priority task wins; lower-priority agent releases its claim | Tasks with clear priority differences |
| `first-claim` | The agent that claimed first keeps the file; the other waits | Fair ordering; equal-priority tasks |
| `preempt` | The coordinator forcibly releases one agent's claim | Time-critical situations |
| `partition` | The MeshResolver splits the file scope so each agent works on a subset | Large refactors touching many files |
| `serialize` | One agent completes fully before the other begins on the contested files | When parallel work on the same files is unsafe |

### Deadlock Resolution

When a deadlock is detected, the MeshResolver:

1. Identifies the cycle of waiting agents
2. Selects the agent with the lowest-priority task as the "victim"
3. Forcibly releases the victim's claim
4. Requeues the victim's task with status `ready`
5. Broadcasts a `deadlock_resolved` event to all agents
6. Logs the deadlock for post-run analysis

### Pre-Allocation

Before agents begin work, the MeshResolver can analyze all task assignments and pre-allocate file ownership to prevent conflicts entirely:

```
cortivex_mesh_resolver({
  action: "pre_allocate",
  tasks: [
    { task_id: "task-1", agent_id: "agent-1", files: ["src/auth/login.ts", "src/auth/session.ts"] },
    { task_id: "task-2", agent_id: "agent-2", files: ["src/api/routes.ts", "src/api/middleware.ts"] },
    { task_id: "task-3", agent_id: "agent-3", files: ["src/auth/session.ts", "src/models/user.ts"] }
  ]
})
```

Response:

```json
{
  "status": "conflicts_detected",
  "conflicts": [
    {
      "file": "src/auth/session.ts",
      "agents": ["agent-1", "agent-3"],
      "tasks": ["task-1", "task-3"]
    }
  ],
  "resolution": {
    "strategy": "serialize",
    "order": ["task-1", "task-3"],
    "reason": "task-1 has higher priority (8) than task-3 (6)"
  },
  "allocation": {
    "agent-1": ["src/auth/login.ts", "src/auth/session.ts"],
    "agent-2": ["src/api/routes.ts", "src/api/middleware.ts"],
    "agent-3": ["src/models/user.ts"]
  },
  "deferred": {
    "agent-3": {
      "files": ["src/auth/session.ts"],
      "available_after": "task-1 completes"
    }
  }
}
```

## Pipeline Configuration

### Adding a MeshResolver to an Orchestrated Pipeline

```yaml
name: conflict-aware-refactor
version: "1.0"
description: Multi-agent refactor with proactive conflict resolution
nodes:
  - id: coordinator
    type: SwarmCoordinator
    config:
      pool_size: 4
      runtime: auto
      task_strategy: priority-queue

  - id: resolver
    type: MeshResolver
    depends_on: [coordinator]
    config:
      strategy: priority
      deadlock_detection: true
      deadlock_check_interval_seconds: 10
      pre_allocate: true
      stale_claim_timeout_seconds: 300
      max_wait_seconds: 60
      on_conflict: resolve
      on_deadlock: release_lowest
      log_conflicts: true

  - id: monitor
    type: AgentMonitor
    depends_on: [coordinator]
    config:
      auto_recovery: true

  - id: analyze
    type: ArchitectAnalyzer
    depends_on: [resolver]
    config:
      target_path: src/
      managed_by: coordinator

  - id: refactor_auth
    type: RefactorAgent
    depends_on: [analyze]
    config:
      target_path: src/auth/
      managed_by: coordinator
      mesh_aware: true

  - id: refactor_api
    type: RefactorAgent
    depends_on: [analyze]
    config:
      target_path: src/api/
      managed_by: coordinator
      mesh_aware: true

  - id: refactor_models
    type: RefactorAgent
    depends_on: [analyze]
    config:
      target_path: src/models/
      managed_by: coordinator
      mesh_aware: true

  - id: test_run
    type: TestRunner
    depends_on: [refactor_auth, refactor_api, refactor_models]
    config:
      test_command: npm test
      coverage_threshold: 80
```

### MeshResolver with Partition Strategy

For large-scale migrations where many agents need to touch many files:

```yaml
name: large-migration
version: "1.0"
description: TypeScript migration with file partitioning
nodes:
  - id: coordinator
    type: SwarmCoordinator
    config:
      pool_size: 5
      runtime: auto

  - id: resolver
    type: MeshResolver
    depends_on: [coordinator]
    config:
      strategy: partition
      partition_method: directory
      pre_allocate: true
      deadlock_detection: true

  - id: analyze
    type: ArchitectAnalyzer
    depends_on: [resolver]
    config:
      target_path: src/
      managed_by: coordinator

  - id: migrate
    type: TypeMigrator
    depends_on: [analyze]
    config:
      source_dir: src/
      managed_by: coordinator
      mesh_aware: true
      batch_size: 10

  - id: test
    type: TestRunner
    depends_on: [migrate]
    config:
      test_command: npx tsc --noEmit && npm test
```

With `partition` strategy, the MeshResolver divides `src/` into non-overlapping directory partitions and assigns each to a different agent instance, preventing any possibility of file conflicts.

## Conflict Event Flow

When a conflict occurs during execution, the following sequence plays out:

```
1. Agent B calls cortivex_mesh({ action: "claim", files: ["src/auth/login.ts"] })
2. Mesh returns { status: "denied", owner: "agent-A" }
3. Agent B calls cortivex_mesh({ action: "report_conflict", ... })
4. MeshResolver receives the conflict report
5. MeshResolver checks the configured strategy:
   - If "priority": compare task priorities of Agent A and Agent B
   - If "first-claim": Agent A keeps the file; Agent B waits
   - If "preempt": coordinator decides which agent to interrupt
6. MeshResolver executes the resolution:
   - Forcibly releases claims if needed
   - Requeues affected tasks if needed
   - Notifies agents of the resolution
7. Agent B retries the claim (or receives alternative assignment)
```

## MeshResolver Node Reference

```yaml
- id: resolver
  type: MeshResolver
  config:
    strategy: priority                    # priority | first-claim | preempt | partition | serialize
    deadlock_detection: true              # enable circular-wait detection
    deadlock_check_interval_seconds: 10   # how often to check for deadlocks
    pre_allocate: true                    # analyze tasks and pre-assign files before execution
    partition_method: directory           # directory | file-list | module (used with partition strategy)
    stale_claim_timeout_seconds: 300      # force-release claims older than this
    max_wait_seconds: 60                  # max time an agent waits before escalating
    on_conflict: resolve                  # resolve | report | halt
    on_deadlock: release_lowest           # release_lowest | release_newest | halt
    log_conflicts: true                   # record all conflicts for post-run analysis
    conflict_report_on_complete: true     # include conflict summary in pipeline results
```

## Monitoring Conflicts

### During Execution

```
cortivex_mesh_resolver({
  action: "status",
  run_id: "ctx-a1b2c3"
})
```

Response:

```json
{
  "active_conflicts": 1,
  "resolved_conflicts": 3,
  "deadlocks_detected": 0,
  "stale_claims_released": 1,
  "current_conflicts": [
    {
      "file": "src/auth/session.ts",
      "agents": ["agent-worker-2", "agent-worker-4"],
      "strategy_applied": "priority",
      "status": "resolving",
      "waiting_agent": "agent-worker-4"
    }
  ],
  "allocation_map": {
    "agent-worker-1": ["src/api/routes.ts", "src/api/middleware.ts"],
    "agent-worker-2": ["src/auth/login.ts", "src/auth/session.ts"],
    "agent-worker-3": ["src/models/user.ts", "src/models/session.ts"],
    "agent-worker-4": ["src/utils/validator.ts"]
  }
}
```

### Post-Run Conflict Report

After the pipeline completes, the MeshResolver produces a conflict summary:

```
Mesh Coordination Report
========================
Total conflicts:       4
Resolved automatically: 4
Deadlocks:             0
Stale claims released: 1

Conflict History:
  1. src/auth/session.ts  agent-2 vs agent-4  -> resolved by priority (agent-2 won)
  2. src/models/user.ts   agent-3 vs agent-1  -> resolved by first-claim (agent-3 won)
  3. src/utils/helpers.ts  agent-1 vs agent-2  -> resolved by priority (agent-1 won)
  4. src/auth/login.ts    stale claim by agent-2 (expired) -> auto-released

Recommendations:
  - src/auth/ had 2 conflicts; consider partitioning this directory in future runs
  - agent-4 was blocked 3 times; assign it to a separate module scope
```

## Quick Reference

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Pre-allocate files | `cortivex_mesh_resolver({ action: "pre_allocate", tasks })` | Assign file ownership before execution |
| Check resolver status | `cortivex_mesh_resolver({ action: "status", run_id })` | View active conflicts and allocations |
| Force resolve conflict | `cortivex_mesh_resolver({ action: "force_resolve", file, winner })` | Manually resolve a stuck conflict |
| Release stale claims | `cortivex_mesh_resolver({ action: "release_stale" })` | Free expired claims across all agents |
| Detect deadlocks | `cortivex_mesh_resolver({ action: "check_deadlocks" })` | Run deadlock detection on demand |
| View conflict history | `cortivex_mesh_resolver({ action: "history", run_id })` | Full log of conflicts and resolutions |
| Change strategy | `cortivex_mesh_resolver({ action: "set_strategy", strategy })` | Switch resolution strategy mid-run |
| View allocation map | `cortivex_mesh_resolver({ action: "allocation_map" })` | See which agent owns which files |

## Best Practices

1. **Use pre-allocation** for pipelines where task scopes are known in advance. Preventing conflicts is cheaper than resolving them.
2. **Choose the right strategy** -- Use `priority` when tasks have clear importance rankings. Use `partition` for large-scale migrations. Use `serialize` when file-level atomicity is required.
3. **Enable deadlock detection** in any pipeline with 3+ agents that may need overlapping files.
4. **Set stale claim timeouts** to prevent abandoned claims from blocking other agents indefinitely.
5. **Review the conflict report** after each run. Recurring conflicts on the same files suggest the pipeline should partition those directories.
6. **Combine with AgentMonitor** -- Dead agents leave orphaned claims. The AgentMonitor detects agent death, and the MeshResolver releases the dead agent's claims.
7. **Keep claims short** -- Agents should claim files, do their work, and release immediately. Long-held claims increase conflict probability.
8. **Use mesh_aware: true** on modification nodes so they automatically follow the check-claim-release protocol from the base cortivex-mesh skill.

## Reasoning Protocol

Before configuring a MeshResolver, reason through:

1. **Will agents actually have overlapping file scopes?** If each agent works on a completely separate directory, you do not need a MeshResolver. Save the overhead.
2. **Which resolution strategy fits the workload?** Use `priority` when tasks have clear importance rankings. Use `partition` for migrations. Use `first-claim` when tasks are equal priority. Use `serialize` only when file-level atomicity is critical.
3. **Should I pre-allocate or resolve on-the-fly?** Pre-allocation prevents conflicts entirely but requires knowing all task scopes in advance. On-the-fly resolution handles dynamic workloads where scopes emerge during execution.
4. **What is the acceptable wait time?** Configure `max_wait_seconds` based on your pipeline's time budget. Short pipelines need aggressive resolution; long-running pipelines can afford to wait.
5. **How many agents are involved?** 2-3 agents rarely need a MeshResolver. 4+ agents with overlapping scopes benefit significantly from proactive coordination.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| MeshResolver on a read-only pipeline | Unnecessary overhead; analysis agents do not need file claims | Only use MeshResolver when agents modify files |
| `strategy: preempt` as default | Forcibly interrupting agents causes wasted work | Use `priority` or `first-claim` by default; reserve `preempt` for time-critical emergencies |
| Disabling deadlock detection | Deadlocked agents hang indefinitely, blocking the pipeline | Always enable for pipelines with 3+ modifying agents |
| No `stale_claim_timeout_seconds` | Dead agents' claims never expire, blocking files permanently | Always set a stale claim timeout |
| `partition` strategy on tiny codebases | Partitioning 10 files across 5 agents creates 2-file partitions with no benefit | Partition only when file count significantly exceeds agent count |
| Ignoring the conflict report | Recurring patterns go unaddressed | Review the post-run conflict report and adjust pipeline scopes to reduce future conflicts |

## Grounding Rules

- **Unsure which strategy to use:** Default to `priority`. It handles most scenarios well and degrades gracefully when priorities are equal (falls back to first-claim behavior).
- **Too many conflicts in a single directory:** This signals that the directory should be treated as a single unit of work. Assign it to one agent instead of splitting across multiple agents.
- **Deadlock detected but cannot identify the cycle:** Use `cortivex_mesh_resolver({ action: "check_deadlocks" })` to get the full cycle. The agent with the lowest-priority task should be the release victim.
- **Agent needs a file held by a higher-priority agent:** Wait. Do not escalate unless the wait exceeds `max_wait_seconds`. Higher-priority work should complete first.

## Advanced Capabilities

### Multi-Strategy Conflict Resolution

The MeshResolver can evaluate conflicts against multiple strategies simultaneously and select the optimal resolution. Use `cortivex_conflict_resolve` to request a multi-strategy evaluation.

```json
{
  "tool": "cortivex_conflict_resolve",
  "request": {
    "action": "evaluate",
    "conflict_id": "cfl-8x92ka",
    "file": "src/auth/session.ts",
    "agents": ["agent-worker-2", "agent-worker-5"],
    "strategies": ["priority", "partition", "serialize"]
  }
}
```

The resolver scores each strategy and returns a ranked recommendation:

```json
{
  "tool": "cortivex_conflict_resolve",
  "response": {
    "conflict_id": "cfl-8x92ka",
    "recommended_strategy": "serialize",
    "rankings": [
      { "strategy": "serialize", "score": 0.92, "reason": "Sequential adds minimal overhead" },
      { "strategy": "priority", "score": 0.85, "reason": "Clear priority gap" },
      { "strategy": "partition", "score": 0.41, "reason": "Single file; cannot partition" }
    ],
    "applied": "serialize",
    "execution_order": ["agent-worker-5", "agent-worker-2"]
  }
}
```

### Distributed Transaction Coordination

For pipelines where multiple file modifications must succeed or fail as a unit, define transaction boundaries in your pipeline YAML.

```yaml
resolver:
  type: MeshResolver
  config:
    transactions:
      enabled: true
      groups:
        - name: auth-refactor
          files: [src/auth/login.ts, src/auth/session.ts, src/auth/middleware.ts]
          atomicity: all-or-nothing
          rollback_on_failure: true
        - name: api-update
          files: [src/api/routes.ts, src/api/handlers.ts]
          atomicity: best-effort
      isolation_level: read-committed
      max_concurrent_transactions: 3
```

With `all-or-nothing` atomicity, the MeshResolver locks all files in the group before any agent begins. If any agent fails, all changes are rolled back.

### Deadlock Detection & Auto-Recovery

The MeshResolver uses a wait-for graph to detect circular dependencies. Configure detection policy to control frequency, victim selection, and recovery.

```json
{
  "deadlock_policy": {
    "detection": {
      "enabled": true,
      "algorithm": "wait-for-graph",
      "check_interval_ms": 5000
    },
    "victim_selection": {
      "strategy": "lowest-priority",
      "fallback": "youngest-task",
      "preserve_agents_with_commits": true
    },
    "recovery": {
      "auto_recover": true,
      "max_recovery_attempts": 3,
      "backoff_base_ms": 1000,
      "on_max_attempts_exceeded": "halt_pipeline"
    }
  }
}
```

When `preserve_agents_with_commits` is enabled, the victim selector avoids releasing agents that have already committed partial work. The exponential backoff prevents rapid re-deadlocking after recovery.

### Coordination Protocol Selection

Use `cortivex_coordination_configure` to switch coordination protocols at runtime. Supported protocols: `pessimistic-locking`, `optimistic-concurrency`, and `hybrid`.

```json
{
  "tool": "cortivex_coordination_configure",
  "request": {
    "action": "set_protocol",
    "run_id": "ctx-d4e5f6",
    "protocol": "optimistic-concurrency",
    "params": { "conflict_check": "on-commit", "retry_on_conflict": true, "max_retries": 5 }
  }
}
```

```json
{
  "tool": "cortivex_coordination_configure",
  "response": {
    "run_id": "ctx-d4e5f6",
    "protocol": "optimistic-concurrency",
    "previous_protocol": "pessimistic-locking",
    "status": "applied",
    "warnings": ["3 agents hold pessimistic locks; converted to version stamps on next cycle"]
  }
}
```

### Failover & Graceful Degradation Patterns

When the MeshResolver encounters failures or agents become unresponsive, failover strategies keep the pipeline running. Define failover behavior with the following schema.

```json
{
  "failover": {
    "resolver_unavailable": {
      "strategy": "fallback-to-local",
      "local_strategy": "first-claim",
      "max_local_duration_seconds": 300
    },
    "agent_unresponsive": {
      "detection_timeout_seconds": 30,
      "action": "release-and-reassign",
      "preserve_partial_work": true
    },
    "degradation_levels": [
      { "level": 1, "trigger": "single_agent_failure", "response": "reassign_tasks" },
      { "level": 2, "trigger": "resolver_partial_failure", "response": "switch_to_local_resolution" },
      { "level": 3, "trigger": "multiple_agent_failures", "response": "pause_and_consolidate" }
    ]
  }
}
```

When `fallback-to-local` activates, each agent uses local conflict resolution until the MeshResolver recovers. At degradation level 3, the coordinator pauses all agents, consolidates remaining work into fewer agents, and resumes with a simplified allocation map.

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for Cortivex mesh coordination operations, aligned with the OWASP Agentic Security Top 10 risk framework. Each subsection references the specific AST risk ID it mitigates.

### AST06: Force-Release Protection

The `preempt` resolution strategy forcibly releases an agent's file claims, which can cause data loss if abused. Force-release operations require elevated approval to prevent unauthorized or accidental claim eviction (AST06).

```yaml
# AST06 -- Require elevated approval for preemptive claim release
resolver:
  type: MeshResolver
  config:
    strategy: priority
    force_release_policy:
      require_approval: true                  # AST06: no auto-preempt without authorization
      approval_source: coordinator            # only the SwarmCoordinator can approve
      require_reason: true                    # must provide justification string
      max_force_releases_per_run: 5           # AST06: cap to prevent abuse
      cooldown_after_force_release_ms: 5000   # prevent rapid repeated preemptions
      audit:
        log_all_force_releases: true
        include_approver_identity: true
        alert_on_threshold_exceeded: true
```

```json
{
  "$schema": "https://cortivex.io/schemas/force-release-request.json",
  "type": "object",
  "properties": {
    "action": { "const": "force_release" },
    "file": { "type": "string" },
    "current_owner": { "type": "string" },
    "requested_by": { "type": "string" },
    "approved_by": { "type": "string" },
    "reason": { "type": "string", "minLength": 10 },
    "approval_token": { "type": "string" },
    "ast_risk_id": { "const": "AST06" }
  },
  "required": ["action", "file", "current_owner", "requested_by", "approved_by", "reason", "ast_risk_id"]
}
```

MCP tool invocation with approval:

```
cortivex_mesh_resolver({
  action: "force_resolve",
  file: "src/auth/session.ts",
  winner: "agent-worker-5",
  approval_token: "apr-9f2e-coordinator",
  reason: "agent-worker-2 unresponsive for 120s; blocking critical path"
})
```

### Transaction Rollback Integrity

When rolling back file modifications in `all-or-nothing` transaction groups, the system must verify file state before and after the rollback to prevent partial rollbacks or state corruption (AST06).

```yaml
# AST06 -- Verify file integrity during transaction rollback
resolver:
  config:
    transactions:
      enabled: true
      rollback_integrity:
        verify_pre_state: true                # AST06: hash file content before rollback
        verify_post_state: true               # AST06: confirm rollback restored original
        hash_algorithm: sha256
        on_integrity_mismatch: halt_and_alert # do not proceed if hashes diverge
        preserve_rollback_evidence: true      # keep copies of pre/post state
        evidence_retention_hours: 72
      groups:
        - name: auth-refactor
          files: [src/auth/login.ts, src/auth/session.ts]
          atomicity: all-or-nothing
          rollback_on_failure: true
```

```json
{
  "tool": "cortivex_mesh_resolver",
  "request": {
    "action": "verify_rollback",
    "transaction_id": "txn-3f8a",
    "checks": ["pre_state_hash_match", "post_state_hash_match", "no_partial_writes"]
  }
}
```

Response:

```json
{
  "transaction_id": "txn-3f8a",
  "status": "rollback_verified",
  "files": [
    {
      "path": "src/auth/login.ts",
      "pre_hash": "sha256:a1b2c3d4...",
      "post_hash": "sha256:a1b2c3d4...",
      "match": true
    },
    {
      "path": "src/auth/session.ts",
      "pre_hash": "sha256:e5f6a7b8...",
      "post_hash": "sha256:e5f6a7b8...",
      "match": true
    }
  ],
  "integrity": "verified",
  "ast_risk_id": "AST06"
}
```

### Deadlock Detection Timeout Limits

Unbounded deadlock detection intervals create resource starvation attack vectors where a malicious or buggy agent can hold claims indefinitely. Strict timeout limits prevent agents from monopolizing resources (AST06).

```yaml
# AST06 -- Bound deadlock detection to prevent resource starvation
resolver:
  config:
    deadlock_detection: true
    deadlock_security:
      max_claim_hold_seconds: 600            # AST06: absolute max any agent can hold a file
      max_wait_seconds: 120                  # AST06: max time waiting for a contested file
      max_detection_cycles: 50               # prevent infinite detection loops
      starvation_detection:
        enabled: true                        # detect agents repeatedly denied access
        threshold_consecutive_denials: 5
        on_starvation: escalate_to_coordinator
      timeout_actions:
        on_claim_timeout: force_release_and_requeue
        on_wait_timeout: reassign_task
        on_detection_loop: halt_and_alert
```

```typescript
import { MeshSecurity } from "@cortivex/mesh";

// AST06: Configure starvation prevention at runtime
const meshSecurity = new MeshSecurity({
  maxClaimHoldSeconds: 600,
  maxWaitSeconds: 120,
  starvationDetection: {
    enabled: true,
    consecutiveDenialThreshold: 5,
    onStarvation: (event) => {
      meshSecurity.escalate({
        agent: event.agentId,
        file: event.contestedFile,
        denials: event.consecutiveDenials,
        astRiskId: "AST06",
      });
    },
  },
});
```

### Protocol Switching Authorization

Switching coordination protocols at runtime (e.g., from `pessimistic-locking` to `optimistic-concurrency`) changes the security posture of the entire pipeline. Protocol switches must require explicit approval and must be logged for audit purposes (AST06).

```json
{
  "$schema": "https://cortivex.io/schemas/protocol-switch-policy.json",
  "type": "object",
  "properties": {
    "protocol_switching": {
      "type": "object",
      "properties": {
        "require_approval": { "type": "boolean", "default": true },
        "allowed_transitions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "from": { "enum": ["pessimistic-locking", "optimistic-concurrency", "hybrid"] },
              "to": { "enum": ["pessimistic-locking", "optimistic-concurrency", "hybrid"] },
              "approval_level": { "enum": ["coordinator", "admin", "quorum"] }
            },
            "required": ["from", "to", "approval_level"]
          }
        },
        "deny_by_default": { "type": "boolean", "default": true },
        "ast_risk_id": { "const": "AST06" }
      }
    }
  }
}
```

```yaml
# AST06 -- Restrict protocol transitions to authorized parties
resolver:
  config:
    protocol_switching:
      require_approval: true                  # AST06: no silent protocol changes
      deny_by_default: true                   # unlisted transitions are blocked
      allowed_transitions:
        - from: pessimistic-locking
          to: optimistic-concurrency
          approval_level: admin               # AST06: elevated approval required
        - from: optimistic-concurrency
          to: pessimistic-locking
          approval_level: coordinator         # downgrade is less risky
        - from: pessimistic-locking
          to: hybrid
          approval_level: coordinator
      audit:
        log_all_switch_requests: true
        log_denied_switches: true
        alert_on_unapproved_attempt: true
```

MCP tool for authorized protocol switch:

```
cortivex_coordination_configure({
  action: "set_protocol",
  run_id: "ctx-d4e5f6",
  protocol: "optimistic-concurrency",
  approval_token: "apr-admin-7c3e",
  reason: "Switching to optimistic for read-heavy phase of migration"
})
```

### Conflict Resolution Audit Trail

Every conflict resolution decision must produce an immutable audit record. The audit trail captures who was involved, what strategy was applied, the outcome, and a timestamp, enabling post-incident forensic analysis (AST06).

```json
{
  "$schema": "https://cortivex.io/schemas/conflict-audit-record.json",
  "type": "object",
  "properties": {
    "record_id": { "type": "string", "pattern": "^aud-[a-f0-9]{8}$" },
    "conflict_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "agents_involved": { "type": "array", "items": { "type": "string" } },
    "contested_file": { "type": "string" },
    "strategy_applied": { "enum": ["priority", "first-claim", "preempt", "partition", "serialize"] },
    "winner": { "type": "string" },
    "loser_action": { "enum": ["requeued", "reassigned", "waited", "halted"] },
    "approval_token": { "type": ["string", "null"] },
    "force_release": { "type": "boolean" },
    "integrity_verified": { "type": "boolean" },
    "ast_risk_id": { "const": "AST06" }
  },
  "required": ["record_id", "conflict_id", "timestamp", "agents_involved", "contested_file", "strategy_applied", "ast_risk_id"]
}
```

```yaml
# AST06 -- Immutable audit trail for all conflict resolutions
resolver:
  config:
    audit_trail:
      enabled: true                           # AST06: mandatory in production
      storage: .cortivex/mesh/audit/
      format: jsonl                           # append-only JSON lines
      include_fields:
        - conflict_id
        - timestamp
        - agents_involved
        - contested_file
        - strategy_applied
        - winner
        - approval_token
        - force_release
        - integrity_verified
      retention_days: 90
      immutable: true                         # AST06: no modification or deletion
      sign_records: true                      # ed25519 signature on each record
      signature_key_path: /etc/cortivex/keys/audit.key
```

Query the audit trail through the MCP tool:

```
cortivex_mesh_resolver({
  action: "audit_query",
  run_id: "ctx-d4e5f6",
  filters: {
    "force_release": true,
    "time_range": { "from": "2025-01-15T00:00:00Z", "to": "2025-01-16T00:00:00Z" }
  }
})
```
