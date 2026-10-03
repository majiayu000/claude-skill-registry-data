---
name: cortivex-task-decomposition
version: 1.0.0
description: Decompose complex work into atomic tasks with dependency ordering, priority assignment, and cost estimation using TaskDecomposer nodes
category: orchestration
tags: [task-decomposition, scheduling, priority, dependencies, cost-estimation, planning]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [task-decomposition, dependency-ordering, priority-assignment, cost-estimation, task-tracking]
---

# Cortivex Task Decomposition

This skill covers how TaskDecomposer nodes break complex work into atomic tasks with dependency ordering, priority assignment, and cost estimation. TaskDecomposer is the planning layer that sits between a user's high-level request and the execution pipeline.

## Overview

When a user requests something like "refactor the authentication module and add tests," the work contains multiple sub-tasks with implicit dependencies and varying priorities. A TaskDecomposer node analyzes the request, breaks it into atomic work units, determines execution order, estimates cost, and feeds the resulting task queue to the SwarmCoordinator or pipeline DAG.

## When to Use

- The user provides a broad, multi-part request that needs decomposition
- You need to plan work for multiple agents before execution begins
- The work has implicit dependencies (tests must run after code changes)
- You want cost and time estimates before committing to execution
- Tasks have different priorities and some are optional

You do NOT need a TaskDecomposer for:

- Running a pre-defined pipeline template (the DAG is already defined)
- Single-step operations (one agent, one task)
- Pipelines where the node sequence is fixed and known at definition time

## How It Works

### Task Lifecycle

```
User Request
    |
    v
TaskDecomposer (analysis phase)
    |-- Parse request into goals
    |-- Identify sub-tasks for each goal
    |-- Determine dependencies between sub-tasks
    |-- Assign priorities
    |-- Estimate cost and duration
    |-- Produce ordered task queue
    |
    v
Task Queue
    |
    v
SwarmCoordinator / Pipeline DAG (execution phase)
    |-- Assigns tasks to agents based on priority and dependencies
    |-- Tasks flow through: Backlog -> Ready -> In Progress -> Review -> Done
    |
    v
Results
```

### Task States

```
Backlog --> Ready --> In Progress --> Review --> Done
                          |
                        Failed --> Backlog (auto-retry if configured)
```

| State | Meaning |
|-------|---------|
| `backlog` | Task is decomposed but dependencies are not yet satisfied |
| `ready` | All dependencies are satisfied; task can be assigned to an agent |
| `in_progress` | An agent is actively working on the task |
| `review` | Task completed; awaiting validation or downstream verification |
| `done` | Task completed and validated |
| `failed` | Task execution failed; may be retried or escalated |

### Decomposition Rules

The TaskDecomposer follows these rules when breaking down work:

1. **Atomic** -- Each task must be completable by a single agent in a single session. If a task requires coordination between agents, it is too large.
2. **Specific** -- Each task has clear acceptance criteria. "Improve code quality" is too vague; "Fix the 3 ESLint errors in src/utils/parser.ts" is specific.
3. **Bounded** -- Each task should take 2-10 minutes of agent work. Tasks estimated at more than 15 minutes should be split further.
4. **Independent where possible** -- Minimize dependencies between tasks to maximize parallel execution.
5. **Prioritized** -- Every task receives an explicit priority score from 1 (lowest) to 10 (highest).

### Priority Guide

| Priority | Label | Scheduling Behavior | Examples |
|----------|-------|---------------------|----------|
| 9-10 | Critical | Scheduled first; blocks all lower-priority work | Security vulnerabilities, data loss risks, production crashes |
| 7-8 | High | Scheduled early; preempts medium tasks | Core feature implementation, CI failures, blocking bugs |
| 4-6 | Medium | Scheduled in order; runs in parallel with peers | Enhancements, refactoring, new API endpoints |
| 1-3 | Low | Scheduled last; may be dropped if budget is tight | Documentation updates, code cleanup, cosmetic fixes |

## Pipeline Configuration

### TaskDecomposer Node in a Pipeline

```yaml
name: decompose-and-execute
version: "1.0"
description: Decompose a user request and execute the resulting tasks
nodes:
  - id: decompose
    type: TaskDecomposer
    config:
      strategy: dependency-aware
      max_tasks: 50
      min_priority: 1
      estimate_cost: true
      estimate_duration: true
      output_format: task-queue
      auto_detect_dependencies: true
      split_threshold_minutes: 15

  - id: coordinator
    type: SwarmCoordinator
    depends_on: [decompose]
    config:
      pool_size: 3
      task_strategy: priority-queue
      source: decompose.task_queue

  - id: monitor
    type: AgentMonitor
    depends_on: [coordinator]
    config:
      auto_recovery: true
```

### Using TaskDecomposer via MCP Tool

```
cortivex_decompose({
  request: "Refactor the authentication module to use JWT, add input validation, and write tests",
  repo: "/path/to/project",
  options: {
    strategy: "dependency-aware",
    estimate_cost: true,
    dry_run: true
  }
})
```

Output:

```json
{
  "goal": "Refactor authentication to JWT with validation and tests",
  "tasks": [
    {
      "id": "task-1",
      "title": "Analyze current auth module structure",
      "description": "Map all files, functions, and dependencies in src/auth/",
      "type": "ArchitectAnalyzer",
      "priority": 8,
      "depends_on": [],
      "estimated_duration_seconds": 50,
      "estimated_cost": "$0.020",
      "tags": ["auth", "analysis"]
    },
    {
      "id": "task-2",
      "title": "Implement JWT token generation and validation",
      "description": "Replace session-based auth in src/auth/session.ts with JWT using jsonwebtoken library",
      "type": "RefactorAgent",
      "priority": 9,
      "depends_on": ["task-1"],
      "estimated_duration_seconds": 60,
      "estimated_cost": "$0.025",
      "tags": ["auth", "refactor", "jwt"]
    },
    {
      "id": "task-3",
      "title": "Add input validation to login and signup endpoints",
      "description": "Validate email format, password strength, and username uniqueness in src/api/auth.ts",
      "type": "AutoFixer",
      "priority": 8,
      "depends_on": ["task-1"],
      "estimated_duration_seconds": 30,
      "estimated_cost": "$0.012",
      "tags": ["auth", "validation"]
    },
    {
      "id": "task-4",
      "title": "Update existing tests for new JWT auth flow",
      "description": "Modify tests/auth.test.ts to use JWT tokens instead of session cookies",
      "type": "RefactorAgent",
      "priority": 7,
      "depends_on": ["task-2"],
      "estimated_duration_seconds": 45,
      "estimated_cost": "$0.020",
      "tags": ["auth", "testing"]
    },
    {
      "id": "task-5",
      "title": "Generate unit tests for input validation",
      "description": "Write tests for email, password, and username validation functions",
      "type": "TestGenerator",
      "priority": 7,
      "depends_on": ["task-3"],
      "estimated_duration_seconds": 55,
      "estimated_cost": "$0.022",
      "tags": ["validation", "testing"]
    },
    {
      "id": "task-6",
      "title": "Run full test suite and verify coverage",
      "description": "Execute npm test and confirm coverage remains above 80%",
      "type": "TestRunner",
      "priority": 8,
      "depends_on": ["task-4", "task-5"],
      "estimated_duration_seconds": 60,
      "estimated_cost": "$0.003",
      "tags": ["testing", "verification"]
    }
  ],
  "summary": {
    "total_tasks": 6,
    "parallelizable": ["task-2 + task-3", "task-4 + task-5"],
    "estimated_total_cost": "$0.102",
    "estimated_total_duration": "4m 30s (with parallel execution)",
    "critical_path": "task-1 -> task-2 -> task-4 -> task-6"
  }
}
```

### Dependency Graph Visualization

The decomposition above produces this dependency DAG:

```
task-1 (Analyze)
  |         \
  v          v
task-2      task-3
(JWT)       (Validation)
  |              |
  v              v
task-4      task-5
(Update     (Generate
 tests)      tests)
  |          /
  v         v
task-6 (Run tests)
```

Tasks 2 and 3 can run in parallel. Tasks 4 and 5 can run in parallel. This parallelism reduces total execution time.

### Batch Decomposition from a Task File

For projects with predefined work, create a `.cortivex/tasks.yaml` file:

```yaml
tasks:
  - title: "Implement user authentication"
    description: "JWT-based auth with refresh tokens"
    priority: 9
    tags: [auth, security, api]

  - title: "Add rate limiting middleware"
    description: "100 req/min per IP, 1000 req/min per authenticated user"
    priority: 7
    tags: [security, middleware]

  - title: "Write integration tests for API endpoints"
    description: "Test all API endpoints with real database"
    priority: 8
    tags: [testing, ci]
```

Run with automatic decomposition:

```
/cortivex run decompose-and-execute --repo . --verbose
```

The TaskDecomposer reads the task file, further decomposes each item into atomic sub-tasks, and feeds them to the coordinator.

## Monitoring Task Progress

### Via MCP Tool

```
cortivex_tasks({
  action: "status",
  run_id: "ctx-a1b2c3"
})
```

### Via CLI

```
/cortivex status ctx-a1b2c3
```

Output:

```
Task Queue: decompose-and-execute (run_id: ctx-a1b2c3)
============================================
Total: 6 tasks | Done: 2 | Running: 2 | Ready: 1 | Backlog: 1

[DONE]        task-1  Analyze current auth module structure         (50s, $0.019)
[DONE]        task-3  Add input validation to login/signup          (28s, $0.011)
[RUNNING]     task-2  Implement JWT token generation                assigned to: agent-worker-1
[RUNNING]     task-5  Generate unit tests for input validation      assigned to: agent-worker-2
[READY]       task-4  Update existing tests for new JWT auth flow   waiting for: task-2
[BACKLOG]     task-6  Run full test suite and verify coverage       waiting for: task-4, task-5

Progress: 33% complete | Cost so far: $0.030 | Estimated remaining: $0.070
```

## TaskDecomposer Node Reference

```yaml
- id: decompose
  type: TaskDecomposer
  config:
    strategy: dependency-aware          # dependency-aware | flat | sequential
    max_tasks: 50                       # maximum tasks to generate
    min_priority: 1                     # discard tasks below this priority
    estimate_cost: true                 # include cost estimates per task
    estimate_duration: true             # include duration estimates per task
    auto_detect_dependencies: true      # infer dependencies from task descriptions
    split_threshold_minutes: 15         # split tasks estimated above this duration
    output_format: task-queue           # task-queue | yaml | json
    validate_dag: true                  # verify no circular dependencies
    include_rollback: false             # generate rollback tasks for reversible ops
    task_file: .cortivex/tasks.yaml     # optional file to read predefined tasks from
```

## Quick Reference

| Operation | MCP Tool / Command | Description |
|-----------|-------------------|-------------|
| Decompose a request | `cortivex_decompose({ request, repo })` | Break request into atomic tasks |
| Dry-run decomposition | `cortivex_decompose({ request, options: { dry_run: true } })` | Show plan without executing |
| View task queue | `cortivex_tasks({ action: "status", run_id })` | See all tasks and their states |
| Reprioritize a task | `cortivex_tasks({ action: "update", task_id, priority })` | Change task priority mid-run |
| Cancel a task | `cortivex_tasks({ action: "cancel", task_id })` | Remove task from queue |
| Retry failed task | `cortivex_tasks({ action: "retry", task_id })` | Requeue a failed task |
| Add task mid-run | `cortivex_tasks({ action: "add", run_id, task })` | Inject a new task into active queue |
| Load from file | `/cortivex run pipeline --repo . --tasks .cortivex/tasks.yaml` | Load predefined tasks |

## Best Practices

1. **Always dry-run first** -- Use `dry_run: true` to review the decomposition before committing to execution.
2. **Review the critical path** -- The longest chain of dependent tasks determines total execution time. Look for opportunities to parallelize.
3. **Set realistic priorities** -- Not everything is critical. Reserve 9-10 for genuine blockers.
4. **Trust the cost estimates** -- If the estimated cost exceeds your budget, remove low-priority tasks before running.
5. **Use dependency-aware strategy** -- The `dependency-aware` strategy produces better parallel execution plans than `sequential`.
6. **Keep tasks atomic** -- If an agent cannot complete a task in one session, the task is too large. Reduce `split_threshold_minutes`.
7. **Combine with knowledge graph** -- When tasks overlap in scope, pair with a KnowledgeCurator to prevent agents from duplicating analysis.

## Reasoning Protocol

Before decomposing any request, reason through explicitly:

1. **What are the distinct goals?** Separate the user's request into independent objectives. "Refactor auth and add tests" has two goals: refactoring and testing.
2. **For each goal, what are the atomic sub-tasks?** Break each goal into steps that a single agent can complete in one session (2-10 minutes). If a step would take longer, split it further.
3. **What are the true dependencies?** Only add `depends_on` when the downstream task genuinely needs the upstream task's output. Ask: "Would this task produce a different result if the dependency had not run?" If no, remove the dependency.
4. **Are priorities justified?** Every priority score should have a reason. Security fixes are high priority because they prevent exploitation. Documentation is lower priority because it does not affect runtime behavior. State the reasoning.
5. **Is the cost estimate reasonable?** Sum the individual task costs. If total exceeds the user's expectations or the pipeline's `cost_limit`, identify which tasks to defer or remove.
6. **What is the critical path?** Identify the longest chain of dependent tasks. This determines the minimum execution time regardless of agent count. Look for ways to shorten it by parallelizing.

Think through all six questions and show your reasoning before generating the task queue.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Single monolithic task | One agent does all the work; no parallelism, no recovery | Break into 3-10 atomic tasks with clear boundaries |
| Every task depends on the previous | Forces fully serial execution | Only add dependencies where output is genuinely required |
| All tasks at priority 9 | Defeats the purpose of prioritization | Use the full range; reserve 9-10 for genuine blockers |
| Tasks without acceptance criteria | Agent does not know when it is done | Every task needs a clear "done" condition |
| Over-decomposition into 50+ micro-tasks | Coordination overhead exceeds the work itself | Target 5-15 tasks for most requests |
| Decomposing a pre-built template | Templates are already decomposed into nodes | Use TaskDecomposer for custom requests, not for running templates |
| Mixing analysis and modification in one task | Agent tries to find and fix simultaneously, doing both poorly | Separate analysis (find issues) from modification (fix issues) |

**WRONG:**
```json
{
  "tasks": [
    {
      "id": "task-1",
      "title": "Do everything",
      "description": "Refactor auth, add validation, write tests, update docs",
      "priority": 9,
      "depends_on": []
    }
  ]
}
```

**RIGHT:**
```json
{
  "tasks": [
    { "id": "task-1", "title": "Analyze auth module structure", "type": "ArchitectAnalyzer", "priority": 8, "depends_on": [] },
    { "id": "task-2", "title": "Refactor auth to JWT", "type": "RefactorAgent", "priority": 9, "depends_on": ["task-1"] },
    { "id": "task-3", "title": "Add input validation", "type": "AutoFixer", "priority": 8, "depends_on": ["task-1"] },
    { "id": "task-4", "title": "Generate unit tests", "type": "TestGenerator", "priority": 7, "depends_on": ["task-2", "task-3"] },
    { "id": "task-5", "title": "Run test suite", "type": "TestRunner", "priority": 8, "depends_on": ["task-4"] }
  ]
}
```

## Grounding Rules

- **User request is vague:** Ask for clarification before decomposing. "Make it better" is not decomposable. "Improve error handling in the auth module" is.
- **Cannot estimate cost:** Use the node type reference table in cortivex-nodes for per-node cost estimates. Sum them and add 20% buffer for retries.
- **Dependencies are circular:** This means your decomposition has a logical error. Re-examine which tasks truly depend on which. At least one dependency must be removable.
- **Too many tasks generated:** Merge related micro-tasks into larger atomic units. "Rename variable X in file A" and "Rename variable X in file B" can be one task: "Rename variable X across the codebase."
- **User asks to skip a decomposed task:** Remove it from the queue and verify no downstream tasks depend on it. If they do, either remove those too or provide an alternative input source.

## Advanced Capabilities

### Recursive Decomposition Strategies

When a task is too complex for single-pass decomposition, recursive decomposition applies the TaskDecomposer iteratively until all leaves meet the atomicity threshold. The `depth` parameter controls maximum recursion levels and `granularity` sets the target task size.

```json
{
  "tool": "cortivex_decompose",
  "request": {
    "request": "Build a complete user management system with RBAC, audit logging, and SSO integration",
    "repo": "/path/to/project",
    "options": { "strategy": "recursive", "depth": 3, "granularity": "fine", "split_threshold_minutes": 8 }
  }
}
```

```json
{
  "decomposition_depth_reached": 2,
  "tasks": [
    { "id": "task-1", "title": "Analyze user model and permissions", "priority": 8, "children": ["task-1a", "task-1b"] },
    { "id": "task-1a", "title": "Map database schema for user/role tables", "priority": 8, "parent": "task-1", "leaf": true },
    { "id": "task-1b", "title": "Identify permission check call sites", "priority": 7, "parent": "task-1", "leaf": true }
  ],
  "summary": { "total_leaf_tasks": 18, "max_depth_used": 2 }
}
```

### Constraint Propagation & Validation

Constraints define hard boundaries that tasks must satisfy. The TaskDecomposer validates all generated tasks against the constraint set before producing the final queue.

```json
{
  "$schema": "https://cortivex.dev/schemas/task-constraints/v1.json",
  "constraints": {
    "budget": { "max_total_cost_usd": 0.50, "max_per_task_cost_usd": 0.10 },
    "time": { "max_total_duration_seconds": 600, "max_per_task_duration_seconds": 120 },
    "scope": {
      "allowed_paths": ["src/", "tests/"],
      "forbidden_paths": ["node_modules/", "dist/", ".env"],
      "allowed_node_types": ["RefactorAgent", "TestGenerator", "TestRunner", "ArchitectAnalyzer"]
    },
    "quality": { "min_test_coverage_percent": 80, "require_review_step": true },
    "concurrency": { "max_parallel_tasks": 4, "max_agents": 3 }
  }
}
```

When a constraint is violated, the TaskDecomposer splits the offending task or flags it with a `constraint_violation` annotation.

### Adaptive Granularity Control

Granularity policies tune decomposition depth per project, module, or task type. Define them in `.cortivex/granularity.yaml`.

```yaml
granularity_policies:
  default:
    target_duration_minutes: 5
    split_threshold_minutes: 12
    merge_threshold_minutes: 1
    max_depth: 3
  overrides:
    - match: { tags: [security, auth] }
      policy: { target_duration_minutes: 3, split_threshold_minutes: 8, max_depth: 4, require_review: true }
    - match: { tags: [documentation, docs] }
      policy: { target_duration_minutes: 10, split_threshold_minutes: 20, max_depth: 1 }
    - match: { paths: ["src/core/**"] }
      policy: { target_duration_minutes: 4, split_threshold_minutes: 10, max_depth: 3, require_review: true }
```

The `match` field supports tag-based and path-based selectors. When multiple overrides match, the most specific match (by path) takes precedence.

### Dependency Graph Optimization

The `cortivex_dependency_analyze` tool inspects a task queue and identifies redundant edges, critical path bottlenecks, and parallelization gains.

```json
{
  "tool": "cortivex_dependency_analyze",
  "request": { "run_id": "ctx-a1b2c3", "optimizations": ["remove_redundant", "shorten_critical_path", "suggest_merges"] }
}
```

```json
{
  "analysis": {
    "total_edges": 9,
    "redundant_edges": [
      { "from": "task-1", "to": "task-6", "reason": "Transitively implied via task-2 -> task-4" }
    ],
    "critical_path": { "tasks": ["task-1", "task-2", "task-4", "task-6"], "duration_seconds": 215, "bottleneck": "task-2" },
    "parallelization_score": 0.72,
    "suggested_merges": [
      { "tasks": ["task-4", "task-5"], "reason": "Same-module test tasks, no mutual dependency", "savings_seconds": 15 }
    ]
  },
  "optimized_edge_count": 8
}
```

```typescript
interface DependencyAnalysisRequest {
  run_id: string;
  optimizations: Array<"remove_redundant" | "shorten_critical_path" | "suggest_merges" | "detect_cycles">;
  apply?: boolean; // false = dry-run (default), true = apply changes
}
```

### Priority-Weighted Task Scheduling

The priority assignment API enables dynamic priority recalculation based on weighted factors. This allows the scheduler to rebalance the queue when conditions change mid-execution.

```json
{
  "$schema": "https://cortivex.dev/schemas/priority-assignment/v1.json",
  "priority_config": {
    "method": "weighted-score",
    "factors": {
      "urgency":          { "weight": 0.35, "source": "user_label" },
      "dependency_depth": { "weight": 0.25, "source": "graph_position" },
      "estimated_cost":   { "weight": 0.15, "source": "cost_estimator", "invert": true },
      "blocking_count":   { "weight": 0.25, "source": "downstream_task_count" }
    },
    "normalization": "min-max", "output_range": [1, 10],
    "recalculate_on": ["task_complete", "task_failed", "task_added"]
  }
}
```

MCP tool call for on-demand recalculation:

```json
{
  "tool": "cortivex_tasks",
  "request": {
    "action": "recalculate_priorities",
    "run_id": "ctx-a1b2c3",
    "priority_config": {
      "method": "weighted-score",
      "factors": { "urgency": 0.40, "blocking_count": 0.35, "dependency_depth": 0.15, "estimated_cost": { "weight": 0.10, "invert": true } }
    }
  }
}
```

The `invert` flag on `estimated_cost` means cheaper tasks receive higher priority scores, favoring quick wins. Recalculation triggers automatically on events in `recalculate_on`, keeping the schedule adaptive.

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for task decomposition operations, aligned with the OWASP Automated Security Testing (AST) risk taxonomy. Each subsection maps to a specific AST risk ID and provides enforceable configuration, validation schemas, and MCP tool integration examples.

### AST03: Mandatory Forbidden Paths Enforcement

Task decomposition generates file-scoped work items that agents execute autonomously. Per **AST03** (Insufficient Access Control in Automated Testing), certain paths must be unconditionally blocked from all generated tasks to prevent agents from reading, modifying, or exfiltrating sensitive files. The forbidden paths list is immutable at runtime and cannot be overridden by task configuration or user input.

```yaml
# .cortivex/security/forbidden-paths.yaml
forbidden_paths:
  immutable: true                         # cannot be modified at runtime
  override_allowed: false                 # no user or task can bypass
  paths:
    - ".env"
    - ".env.*"
    - "**/.env"
    - "**/.env.*"
    - ".ssh/"
    - "**/.ssh/"
    - "**/credentials"
    - "**/credentials.*"
    - "**/*.pem"
    - "**/*.key"
    - "**/*.p12"
    - "**/secrets.yaml"
    - "**/secrets.json"
    - "**/.aws/credentials"
    - "**/.gcp/service-account.json"
    - "**/id_rsa"
    - "**/id_ed25519"
  enforcement:
    validate_at_decomposition: true       # check before tasks enter queue
    validate_at_execution: true           # check again before agent starts
    block_action: reject_task             # reject | warn | quarantine
    audit_violations: true
  ast_risk_id: AST03
```

```json
{
  "$schema": "https://cortivex.dev/schemas/forbidden-paths-policy/v1.json",
  "title": "ForbiddenPathsPolicy",
  "type": "object",
  "required": ["policy_id", "paths", "enforcement"],
  "properties": {
    "policy_id": { "type": "string", "pattern": "^fpol-[a-z0-9-]+$" },
    "immutable": { "type": "boolean", "const": true },
    "paths": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "enforcement": {
      "type": "object",
      "required": ["validate_at_decomposition", "block_action"],
      "properties": {
        "validate_at_decomposition": { "type": "boolean" },
        "validate_at_execution": { "type": "boolean" },
        "block_action": { "enum": ["reject_task", "warn", "quarantine"] },
        "audit_violations": { "type": "boolean" }
      }
    },
    "ast_risk_id": { "type": "string", "const": "AST03" }
  }
}
```

MCP tool call that triggers forbidden path rejection (AST03 enforcement):

```
cortivex_decompose({
  request: "Read the database credentials from .env and update the config",
  repo: "/path/to/project",
  options: { strategy: "dependency-aware" }
})
```

```json
{
  "status": "rejected",
  "reason": "Task references forbidden path '.env' (AST03). Sensitive files are unconditionally blocked.",
  "ast_risk_id": "AST03",
  "violating_paths": [".env"],
  "policy_id": "fpol-immutable-default",
  "remediation": "Remove references to sensitive files. Use environment variable injection via the runtime config instead."
}
```

### Task Injection Prevention

The task queue accepts new tasks at runtime via `cortivex_tasks({ action: "add" })`. Per **AST03**, runtime task addition must require explicit authorization to prevent malicious or accidental injection of unauthorized work items that could modify protected files, exfiltrate data, or consume budget.

```yaml
# .cortivex/security/task-injection-policy.yaml
task_injection_prevention:
  runtime_task_addition:
    enabled: true
    authorization_required: true
    allowed_roles:
      - pipeline-owner
      - operator
      - admin
    denied_roles:
      - viewer
      - agent                             # agents cannot self-inject tasks
    validation:
      check_forbidden_paths: true         # AST03 path validation on injected tasks
      check_allowed_node_types: true
      check_budget_remaining: true
      max_injected_tasks_per_run: 10
      require_justification: true
    audit:
      log_all_injections: true
      log_denied_injections: true
      alert_on_agent_self_inject: true    # alert if an agent attempts self-injection
  ast_risk_id: AST03
```

```
cortivex_tasks({
  action: "add",
  run_id: "ctx-a1b2c3",
  task: {
    title: "Read SSH keys for deployment",
    description: "Copy .ssh/id_rsa to deployment config",
    type: "CustomAgent",
    priority: 9
  },
  auth: { identity: "agent-worker-1", role: "agent" }
})
```

```json
{
  "status": "denied",
  "reasons": [
    "Role 'agent' is not authorized to inject tasks at runtime (AST03)",
    "Task references forbidden path '.ssh/id_rsa' (AST03)"
  ],
  "ast_risk_id": "AST03",
  "audit_logged": true,
  "alert_triggered": true
}
```

```typescript
interface TaskInjectionValidation {
  task_id: string;
  run_id: string;
  injected_by: string;
  role: string;
  authorized: boolean;
  path_violations: string[];
  node_type_allowed: boolean;
  budget_sufficient: boolean;
  justification_provided: boolean;
  ast_risk_id: "AST03";
}
```

### Priority Manipulation Protection

Security-critical tasks (vulnerability fixes, secret rotation, access revocation) must maintain minimum priority thresholds. Per **AST03**, tasks tagged with security classifications cannot be deprioritized below a configurable floor, preventing attackers or misconfigured automation from burying urgent security work.

```yaml
# .cortivex/security/priority-protection.yaml
priority_manipulation_protection:
  protected_categories:
    - match: { tags: [security, vulnerability] }
      min_priority: 8
      reason: "Security vulnerabilities cannot be deprioritized below 8"
    - match: { tags: [secret-rotation] }
      min_priority: 9
      reason: "Secret rotation is time-sensitive and cannot be deferred"
    - match: { tags: [access-revocation] }
      min_priority: 9
      reason: "Access revocation must execute promptly"
    - match: { tags: [compliance, audit] }
      min_priority: 7
      reason: "Compliance tasks have regulatory deadlines"
  enforcement:
    validate_on_create: true
    validate_on_update: true
    validate_on_recalculate: true
    block_below_floor: true               # reject priority changes below floor
    audit_attempts: true
  ast_risk_id: AST03
```

```
cortivex_tasks({
  action: "update",
  task_id: "task-sec-01",
  priority: 3,
  run_id: "ctx-a1b2c3"
})
```

```json
{
  "status": "denied",
  "task_id": "task-sec-01",
  "current_priority": 9,
  "requested_priority": 3,
  "min_allowed_priority": 8,
  "reason": "Task tagged [security, vulnerability] cannot be deprioritized below 8 (AST03)",
  "ast_risk_id": "AST03",
  "audit_logged": true
}
```

```json
{
  "$schema": "https://cortivex.dev/schemas/priority-protection/v1.json",
  "title": "PriorityProtectionRule",
  "type": "object",
  "required": ["match", "min_priority", "ast_risk_id"],
  "properties": {
    "match": {
      "type": "object",
      "properties": {
        "tags": { "type": "array", "items": { "type": "string" } },
        "node_types": { "type": "array", "items": { "type": "string" } },
        "title_pattern": { "type": "string" }
      }
    },
    "min_priority": { "type": "integer", "minimum": 1, "maximum": 10 },
    "reason": { "type": "string" },
    "ast_risk_id": { "type": "string", "const": "AST03" }
  }
}
```

### Recursive Decomposition Depth Limits

Recursive decomposition can be exploited to trigger unbounded recursion, exhausting CPU, memory, and API budget. Per **AST03**, strict depth limits and resource ceilings must be enforced to prevent denial-of-service through decomposition amplification.

```yaml
# .cortivex/security/decomposition-depth-limits.yaml
recursive_decomposition_limits:
  max_depth: 5
  max_total_tasks: 200
  max_tasks_per_level:
    depth_0: 20
    depth_1: 50
    depth_2: 80
    depth_3: 40
    depth_4: 10
    depth_5: 5
  resource_ceilings:
    max_decomposition_time_seconds: 120
    max_decomposition_cost_usd: 0.50
    max_memory_mb: 256
  on_limit_exceeded:
    action: halt_and_return_partial       # halt_and_return_partial | reject | warn
    include_truncation_report: true
    alert_roles: [operator, admin]
  cycle_detection:
    enabled: true
    action: reject_with_diagnostic
    max_graph_edges: 500
  audit:
    log_depth_reached: true
    log_limit_violations: true
    ast_risk_id: AST03
```

```
cortivex_decompose({
  request: "Recursively refactor every module in the monorepo",
  repo: "/path/to/large-monorepo",
  options: {
    strategy: "recursive",
    depth: 20,
    granularity: "fine"
  }
})
```

```json
{
  "status": "depth_limited",
  "requested_depth": 20,
  "enforced_max_depth": 5,
  "tasks_generated": 147,
  "tasks_at_limit": true,
  "truncation_report": {
    "depth_0_tasks": 12,
    "depth_1_tasks": 45,
    "depth_2_tasks": 58,
    "depth_3_tasks": 27,
    "depth_4_tasks": 5,
    "suppressed_subtrees": 8
  },
  "ast_risk_id": "AST03",
  "recommendation": "Reduce scope or increase split_threshold_minutes to produce fewer tasks"
}
```

### Constraint Validation: Reject Security-Violating Tasks

The constraint propagation engine must reject any generated task that violates security constraints, rather than merely flagging it. Per **AST03**, tasks that reference forbidden paths, exceed budget allocations, or specify disallowed node types must be removed from the queue before execution begins.

```yaml
# .cortivex/security/constraint-validation.yaml
security_constraint_validation:
  validate_at:
    - decomposition_output              # before tasks enter queue
    - runtime_injection                 # when tasks are added mid-run
    - priority_recalculation            # when priorities are recomputed
  rules:
    - rule_id: forbidden-path-check
      check: "task.description NOT MATCHES forbidden_paths"
      on_violation: reject
      ast_risk_id: AST03
    - rule_id: allowed-node-type-check
      check: "task.type IN allowed_node_types"
      on_violation: reject
      ast_risk_id: AST03
    - rule_id: budget-ceiling-check
      check: "SUM(task.estimated_cost) <= budget.max_total_cost_usd"
      on_violation: reject_lowest_priority
      ast_risk_id: AST03
    - rule_id: scope-boundary-check
      check: "task.target_paths SUBSET_OF allowed_paths"
      on_violation: reject
      ast_risk_id: AST03
    - rule_id: no-privilege-escalation
      check: "task.required_role <= current_user.role"
      on_violation: reject
      ast_risk_id: AST03
  enforcement:
    fail_open: false                      # reject on validation error, not allow
    audit_all_validations: true
    report_violations_to: [security-lead]
```

```typescript
interface ConstraintValidationResult {
  run_id: string;
  tasks_validated: number;
  tasks_accepted: number;
  tasks_rejected: number;
  violations: Array<{
    task_id: string;
    rule_id: string;
    violation_detail: string;
    action_taken: "reject" | "reject_lowest_priority" | "quarantine";
    ast_risk_id: "AST03";
  }>;
  validation_passed: boolean;
}
```

```
cortivex_decompose({
  request: "Update secrets.yaml with new API keys and deploy to production",
  repo: "/path/to/project",
  options: { strategy: "dependency-aware", dry_run: true }
})
```

```json
{
  "status": "validation_failed",
  "tasks_generated": 3,
  "tasks_rejected": 2,
  "violations": [
    {
      "task_id": "task-1",
      "rule_id": "forbidden-path-check",
      "violation_detail": "Task references 'secrets.yaml' which is in forbidden_paths",
      "action_taken": "reject",
      "ast_risk_id": "AST03"
    },
    {
      "task_id": "task-2",
      "rule_id": "scope-boundary-check",
      "violation_detail": "Task targets production deployment path outside allowed_paths",
      "action_taken": "reject",
      "ast_risk_id": "AST03"
    }
  ],
  "remediation": "Remove references to forbidden paths and restrict operations to allowed_paths scope"
}
```
