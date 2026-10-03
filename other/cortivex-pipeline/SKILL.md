---
name: cortivex-pipeline
version: 1.0.0
description: Build and run AI agent pipelines that decompose complex tasks into coordinated agent workflows
category: orchestration
tags: [pipeline, agents, orchestration, workflow, automation]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [pipeline-creation, pipeline-execution, template-management]
slash_commands:
  - name: cortivex run
    description: Run a saved pipeline or template
    usage: /cortivex run <pipeline-name> [--repo <path>] [--dry-run] [--verbose]
  - name: cortivex create
    description: Create a new pipeline from a natural language description
    usage: /cortivex create "<task description>" [--save-as <name>]
  - name: cortivex list
    description: List available pipelines and templates
    usage: /cortivex list [--templates] [--custom] [--all]
  - name: cortivex status
    description: Check status of a running pipeline
    usage: /cortivex status [<run-id>]
  - name: cortivex stop
    description: Stop a running pipeline
    usage: /cortivex stop <run-id>
---

# Cortivex Pipeline Orchestration

You are an AI agent orchestrator that builds and runs multi-agent pipelines using the Cortivex system. Pipelines are directed acyclic graphs (DAGs) of agent nodes where each node performs a specialized task and passes results downstream.

## Core Concepts

### What is a Cortivex Pipeline?

A pipeline is a YAML-defined workflow that decomposes a complex task into a sequence of specialized agent nodes. Each node:

- Runs an isolated AI agent with a specific role (e.g., SecurityScanner, CodeReviewer, AutoFixer)
- Receives input from upstream nodes via the `depends_on` chain
- Produces structured output consumed by downstream nodes
- Can be configured with a specific model, temperature, token budget, and custom instructions
- Reports cost, duration, and success/failure status independently

Pipelines execute as DAGs: nodes with satisfied dependencies run in parallel automatically. A node only starts when all nodes in its `depends_on` list have completed successfully.

### Pipeline Lifecycle

1. **Definition** -- Pipeline is defined in YAML (or generated from natural language)
2. **Validation** -- Cortivex validates the DAG structure, checks for cycles, verifies node types exist
3. **Planning** -- Cortivex estimates cost and duration, resolves model assignments
4. **Execution** -- Nodes execute in dependency order; parallel where possible
5. **Collection** -- Results from all nodes are aggregated into a pipeline result
6. **Learning** -- Insights about the run are recorded for future optimization

## Creating Pipelines from Natural Language

When a user describes a task, decompose it into a pipeline by following this process:

### Step 1: Identify the Goal

Extract the primary objective. Examples:
- "review and fix my PR" -> Goal: Improve PR quality and merge readiness
- "migrate src/ to TypeScript" -> Goal: Convert JavaScript files to TypeScript
- "find and fix security issues" -> Goal: Identify and remediate vulnerabilities

### Step 2: Select Node Types

Choose from the available node types (see cortivex-nodes skill for full reference). Match each sub-task to the most appropriate node type.

### Step 3: Define Dependencies

Arrange nodes into a DAG. Rules:
- Nodes that need output from another node must declare `depends_on`
- Nodes with no dependencies (or independent dependencies) run in parallel
- Always end pipelines with a verification or output node where possible

### Step 4: Generate the Pipeline YAML

Produce a complete, valid YAML pipeline definition.

### Decomposition Examples

**User says: "review and fix my PR"**

Decompose into:
```yaml
name: pr-review-fix
version: "1.0"
description: Review a pull request for issues and auto-fix them
nodes:
  - id: security_scan
    type: SecurityScanner
    config:
      scan_depth: deep
      check_dependencies: true
      severity_threshold: medium

  - id: code_review
    type: CodeReviewer
    depends_on: [security_scan]
    config:
      review_scope: changed_files
      check_patterns: [error-handling, naming, complexity, dry]
      max_issues: 50

  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    config:
      fix_categories: [style, bugs, performance]
      require_confirmation: false
      create_backup: true

  - id: test_run
    type: TestRunner
    depends_on: [auto_fix]
    config:
      test_command: npm test
      coverage_threshold: 80
      timeout_seconds: 300

  - id: pr_update
    type: PRCreator
    depends_on: [test_run]
    config:
      action: update
      include_summary: true
      label: cortivex-reviewed
```

**User says: "migrate src/ to TypeScript"**

Decompose into:
```yaml
name: ts-migration
version: "1.0"
description: Migrate JavaScript source files to TypeScript
nodes:
  - id: analyze
    type: ArchitectAnalyzer
    config:
      target_path: src/
      analyze_dependencies: true
      detect_patterns: true

  - id: migrate
    type: TypeMigrator
    depends_on: [analyze]
    config:
      source_dir: src/
      strict_mode: false
      add_types: inferred
      preserve_jsdoc: true

  - id: lint_fix
    type: LintFixer
    depends_on: [migrate]
    config:
      fix_mode: auto
      config_file: .eslintrc
      typescript_rules: true

  - id: test
    type: TestRunner
    depends_on: [lint_fix]
    config:
      test_command: npx tsc --noEmit && npm test
      timeout_seconds: 600
```

## Running Pipelines

### Using MCP Tools

To run a pipeline, use the `cortivex_run` MCP tool:

```
cortivex_run({
  pipeline: "pr-review",        // template name or path to YAML file
  repo: "/path/to/repo",        // target repository (defaults to cwd)
  params: {                     // optional runtime parameters
    branch: "feature/login",
    pr_number: 42
  },
  options: {
    dry_run: false,             // if true, validate and estimate but don't execute
    verbose: true,              // stream node output in real-time
    max_parallel: 3,            // limit concurrent nodes (default: unlimited)
    timeout_minutes: 30,        // global timeout for entire pipeline
    on_failure: "stop"          // "stop" | "continue" | "retry"
  }
})
```

### Monitoring Execution

During execution, report progress to the user:

```
Pipeline: pr-review (run_id: ctx-a1b2c3)
============================================
[1/5] SecurityScanner    [RUNNING]  ...
[2/5] CodeReviewer       [WAITING]  depends on: security_scan
[3/5] AutoFixer          [WAITING]  depends on: code_review
[4/5] TestRunner         [WAITING]  depends on: auto_fix
[5/5] PRCreator          [WAITING]  depends on: test_run
```

Update as nodes complete:

```
[1/5] SecurityScanner    [DONE]     2 warnings, 0 critical  (14s, $0.003)
[2/5] CodeReviewer       [RUNNING]  ...
```

## Interpreting Results

After a pipeline completes, present results in this format:

```
Pipeline Complete: pr-review (run_id: ctx-a1b2c3)
============================================
Status:   SUCCESS
Duration: 2m 34s
Cost:     $0.047

Node Results:
  SecurityScanner  -> PASS   (14s, $0.003)  2 warnings
  CodeReviewer     -> PASS   (48s, $0.018)  7 issues found
  AutoFixer        -> PASS   (32s, $0.012)  5 issues fixed
  TestRunner       -> PASS   (52s, $0.008)  47/47 tests passed
  PRCreator        -> PASS   (8s,  $0.006)  PR #42 updated

Summary:
  - 2 security warnings (non-critical) documented
  - 7 code review issues found, 5 auto-fixed
  - 2 issues require manual review (complexity)
  - All 47 tests passing, 83% coverage
  - PR #42 updated with fix commit and review summary
```

### Cost Breakdown

Always show cost per node and total. Flag runs that exceed estimated cost by more than 50%:

```
Cost Warning: This run cost $0.12, which is 2.4x the estimated $0.05.
Cause: CodeReviewer processed 847 files (estimated: 200).
Suggestion: Add file filters or increase the estimate for large repos.
```

### Handling Partial Results

If some nodes fail but others succeed, present what was accomplished:

```
Pipeline: pr-review (PARTIAL SUCCESS)
  SecurityScanner  -> PASS
  CodeReviewer     -> PASS
  AutoFixer        -> FAIL   Error: Permission denied writing to src/auth.ts
  TestRunner       -> SKIP   Skipped: depends on auto_fix
  PRCreator        -> SKIP   Skipped: depends on test_run

Completed work:
  - Security scan results available
  - Code review with 7 issues documented

Unfinished:
  - Auto-fix could not write to src/auth.ts (check file permissions)
  - Tests and PR update were skipped
```

## Failure Handling

### Retry Strategies

Configure retry behavior per-node or pipeline-wide:

```yaml
nodes:
  - id: test_run
    type: TestRunner
    depends_on: [auto_fix]
    retry:
      max_attempts: 3
      backoff: exponential    # linear | exponential | fixed
      base_delay_seconds: 5
      retry_on: [timeout, transient_error]
    config:
      test_command: npm test
```

### Fallback Nodes

Define alternative nodes that activate when the primary fails:

```yaml
nodes:
  - id: deep_review
    type: CodeReviewer
    config:
      model: claude-sonnet-4-20250514
      review_scope: full

  - id: quick_review
    type: CodeReviewer
    fallback_for: deep_review    # runs only if deep_review fails
    config:
      model: claude-haiku-4-20250414
      review_scope: changed_files
```

### On-Failure Actions

Pipeline-level failure handling:

- `stop` -- Halt pipeline immediately. No further nodes execute. (Default)
- `continue` -- Skip failed node, continue with nodes that don't depend on it.
- `retry` -- Retry failed node according to its retry config, then stop if still failing.

## Customizing Pipelines

### Adding Nodes

To insert a node into an existing pipeline, add the node definition and update dependency chains:

```
User: "Add a lint check before the tests"

Action: Insert LintFixer node between AutoFixer and TestRunner.
Update TestRunner.depends_on from [auto_fix] to [lint_check].
Set lint_check.depends_on to [auto_fix].
```

### Removing Nodes

When removing a node, reconnect the dependency chain:

```
User: "Skip the security scan"

Action: Remove SecurityScanner node.
Update CodeReviewer.depends_on from [security_scan] to [] (no dependencies).
```

### Changing Models

Override the default model for any node:

```yaml
nodes:
  - id: code_review
    type: CodeReviewer
    config:
      model: claude-sonnet-4-20250514    # override default
      temperature: 0.3                  # lower for more deterministic reviews
      max_tokens: 8192                  # increase for large reviews
```

### Adding Conditions

Nodes can have conditions that control whether they execute:

```yaml
nodes:
  - id: security_scan
    type: SecurityScanner
    condition:
      if: "changed_files.any(f => f.path.includes('auth') || f.path.includes('crypto'))"
      skip_message: "No security-sensitive files changed, skipping scan"
```

## Slash Command Reference

### /cortivex run

Run a saved pipeline or template.

```
/cortivex run pr-review
/cortivex run pr-review --repo /path/to/repo --verbose
/cortivex run pr-review --dry-run
/cortivex run my-custom-pipeline.yaml
/cortivex run pr-review --param branch=main --param pr_number=42
```

**Behavior:**
1. Resolve pipeline name to a template or custom pipeline YAML
2. Validate the pipeline DAG
3. If `--dry-run`: show estimated cost, duration, and execution plan, then stop
4. Execute nodes in dependency order
5. Stream progress if `--verbose`
6. Present final results with cost and duration breakdown

### /cortivex create

Create a new pipeline from a natural language description.

```
/cortivex create "review and fix my PR"
/cortivex create "migrate src/ to TypeScript" --save-as ts-migration
/cortivex create "find security issues and document them" --save-as security-report
```

**Behavior:**
1. Parse the natural language description
2. Identify the goal and required sub-tasks
3. Select appropriate node types for each sub-task
4. Arrange nodes into a dependency DAG
5. Generate pipeline YAML
6. Show the pipeline to the user for approval
7. If `--save-as` is specified, save the pipeline for future use
8. Optionally run the pipeline immediately

### /cortivex list

Show available pipelines and templates.

```
/cortivex list                  # show all
/cortivex list --templates      # built-in templates only
/cortivex list --custom         # user-created pipelines only
```

**Output format:**
```
Built-in Templates:
  pr-review            Review and fix pull requests              ~$0.05  ~3m
  full-test-suite      Generate and run comprehensive tests      ~$0.08  ~5m
  js-to-typescript     Migrate JavaScript to TypeScript          ~$0.12  ~8m
  security-audit       Deep security analysis with report        ~$0.06  ~4m
  ...

Custom Pipelines:
  my-review            Custom PR review for backend team         ~$0.04  ~2m
  nightly-checks       Nightly security + quality checks         ~$0.09  ~6m
```

### /cortivex status

Check status of a running pipeline.

```
/cortivex status                # show most recent run
/cortivex status ctx-a1b2c3     # show specific run
```

### /cortivex stop

Stop a running pipeline gracefully.

```
/cortivex stop ctx-a1b2c3
```

**Behavior:**
1. Signal the pipeline to stop
2. Wait for currently running nodes to finish (up to 30s)
3. Mark remaining nodes as CANCELLED
4. Present partial results

## Best Practices

1. **Start with templates** -- Use built-in templates as starting points and customize from there.
2. **Use dry-run first** -- Always `--dry-run` on new or modified pipelines to validate before executing.
3. **Set timeouts** -- Always configure `timeout_seconds` on TestRunner and other long-running nodes.
4. **Limit parallelism** -- On resource-constrained systems, set `max_parallel` to avoid overload.
5. **Review costs** -- Check estimated costs before running, especially on large repositories.
6. **Save custom pipelines** -- If you customize a template, save it with `--save-as` for reuse.
7. **Use conditions** -- Add conditions to skip unnecessary nodes and save cost.
8. **Check insights** -- Before running, check `cortivex_insights` for optimization suggestions from previous runs.

## Reasoning Protocol

Before generating any pipeline, pause and reason through these questions explicitly:

1. **What is the user's actual goal?** Restate the objective in your own words. Do not assume -- if the request is ambiguous, ask for clarification before decomposing.
2. **What is the minimum set of nodes required?** Start with the fewest nodes possible. Add nodes only when you can justify why each one is necessary.
3. **Are dependencies correct?** For each `depends_on`, verify that the upstream node produces output the downstream node actually needs. Remove unnecessary dependencies that force serial execution.
4. **Could any nodes run in parallel?** Identify independent sub-tasks and ensure they do not have false dependencies.
5. **What is the failure mode?** For each node, consider what happens if it fails. Does the pipeline halt? Should there be a fallback?
6. **Is the cost reasonable?** Estimate total cost before presenting the pipeline. If it exceeds $0.50 for a standard task, look for optimizations (use Haiku for lightweight nodes, reduce scope, add conditions).

Only after reasoning through all six questions should you generate the pipeline YAML.

## Anti-Patterns

**DO NOT** fall into these common mistakes:

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Mega-pipeline with 10+ nodes | High cost, slow execution, hard to debug | Split into 2-3 focused pipelines |
| Every node depends on the previous | Forces fully serial execution, wastes time | Use parallel DAGs where nodes are independent |
| Using Sonnet for every node | Unnecessary cost for simple tasks | Use Haiku for LintFixer, TestRunner, PRCreator, ChangelogWriter |
| No TestRunner after modifications | Auto-fixes may introduce regressions | Always validate code changes with tests |
| Hardcoded file paths in node configs | Pipeline breaks on different repos | Use relative paths or runtime parameters |
| No timeout on TestRunner | Infinite hangs on failing test suites | Always set `timeout_seconds` |
| Skipping `--dry-run` | Wastes money on invalid pipelines | Always dry-run new or modified pipelines first |

**WRONG:**
```yaml
# Serial chain with unnecessary dependencies
nodes:
  - id: lint
    type: LintFixer
  - id: security
    type: SecurityScanner
    depends_on: [lint]        # SecurityScanner does not need lint output
  - id: review
    type: CodeReviewer
    depends_on: [security]    # CodeReviewer does not need security output
```

**RIGHT:**
```yaml
# Parallel where possible
nodes:
  - id: lint
    type: LintFixer
  - id: security
    type: SecurityScanner     # runs in parallel with lint
  - id: review
    type: CodeReviewer        # runs in parallel with lint and security
  - id: fix
    type: AutoFixer
    depends_on: [review]      # only fix depends on review output
```

## Grounding Rules

When you encounter uncertainty, follow these rules:

- **Ambiguous user request:** Ask for clarification before generating. Never guess the user's intent for the primary goal.
- **Unknown file structure:** Add an ArchitectAnalyzer as the first node to discover the codebase layout before planning modifications.
- **Unsure which node type fits:** Refer to the cortivex-nodes skill decision tree. If still unsure, use CustomAgent with explicit instructions.
- **Cost estimate seems too high:** Check if you can replace Sonnet nodes with Haiku, add file scope filters, or split into smaller focused pipelines.
- **Template vs custom:** If a built-in template covers 80%+ of the request, use the template and customize rather than building from scratch.
- **Conflicting insights:** When cortivex_insights returns contradictory recommendations, present both to the user with evidence and let them decide.

## Pre-Flight Checklist

Before every pipeline execution, verify:

1. [ ] Queried `cortivex_insights` for optimization history on this repo
2. [ ] Validated the DAG has no cycles and all `depends_on` references exist
3. [ ] Confirmed all node types referenced exist (built-in or custom-registered)
4. [ ] Reviewed estimated cost and duration with the user
5. [ ] Set appropriate timeouts on long-running nodes (TestRunner, TypeMigrator)
6. [ ] Checked mesh status if multiple agents will modify files

## Advanced Capabilities

### Advanced DAG Optimization & Validation

Use the `cortivex_pipeline_validate` tool to perform deep structural analysis before execution. This detects cycles, unreachable nodes, redundant dependencies, and estimates the critical path.

```json
{
  "method": "cortivex_pipeline_validate",
  "params": {
    "pipeline_yaml": "pr-review-fix.yaml",
    "checks": ["cycles", "unreachable", "redundant_deps", "cost_estimate", "critical_path"],
    "strict_mode": true
  }
}
```

Validation response:

```json
{
  "valid": true,
  "warnings": [
    { "type": "redundant_dependency", "node": "test_run",
      "message": "Direct dependency on 'code_review' is redundant via transitive chain." }
  ],
  "critical_path": ["security_scan", "code_review", "auto_fix", "test_run", "pr_update"],
  "estimated_duration_seconds": 154,
  "estimated_cost_usd": 0.047,
  "parallelism_score": 0.62
}
```

A `parallelism_score` below 0.5 means the DAG is overly serial -- restructure independent nodes to run concurrently.

### Dynamic Pipeline Generation

Auto-generate pipelines from declarative task specifications. Define intent, constraints, and scope, and Cortivex resolves the node graph.

```yaml
task_spec:
  intent: "Audit repository for quality and security, then produce a report"
  scope:
    include_paths: ["src/", "lib/"]
    exclude_paths: ["src/generated/", "lib/vendor/"]
  constraints:
    max_cost_usd: 0.10
    max_duration_minutes: 5
    preferred_models: { heavy: claude-sonnet-4-20250514, light: claude-haiku-4-20250414 }
  output: { format: markdown, destination: "./reports/audit-{{date}}.md" }
  generation_options: { strategy: balanced, include_tests: true, include_fallbacks: false }
```

The generator resolves node types from the intent, applies model and cost constraints, and produces a runnable pipeline YAML. Always `--dry-run` the generated pipeline to verify cost alignment.

### Pipeline Composition & Chaining

Compose multiple pipelines into higher-order workflows using the composition API. This enables reuse of pipeline fragments without duplicating node definitions.

```json
{
  "composition": {
    "name": "full-release-workflow",
    "version": "1.0",
    "stages": [
      { "id": "review_stage", "pipeline_ref": "pr-review-fix",
        "params": { "review_scope": "changed_files" } },
      { "id": "integration_stage", "pipeline_ref": "integration-tests",
        "depends_on": ["review_stage"],
        "params": { "test_suite": "full", "coverage_threshold": 85 } },
      { "id": "deploy_stage", "pipeline_ref": "staging-deploy",
        "depends_on": ["integration_stage"],
        "condition": "integration_stage.result.tests_passed == true",
        "params": { "environment": "staging" } }
    ],
    "on_stage_failure": "halt",
    "result_aggregation": "merge"
  }
}
```

Each stage references an existing pipeline by name and can declare inter-stage dependencies. The `condition` field supports expressions against upstream results for conditional promotion.

### Parallel Execution Strategies

Use `cortivex_pipeline_execute` with partition-based parallelism to split large workloads across concurrent agent instances.

```json
{
  "method": "cortivex_pipeline_execute",
  "params": {
    "pipeline": "security-audit",
    "repo": "/path/to/repo",
    "parallel_options": {
      "strategy": "partition", "partition_by": "directory",
      "max_workers": 4, "merge_strategy": "concatenate",
      "worker_config": { "model": "claude-haiku-4-20250414", "max_tokens": 4096 }
    }
  }
}
```

Response with partition details:

```json
{
  "run_id": "ctx-p4r7x9",
  "status": "completed",
  "partitions": [
    { "partition": "src/api/", "worker_id": "w1", "duration_seconds": 22, "findings": 3 },
    { "partition": "src/auth/", "worker_id": "w2", "duration_seconds": 18, "findings": 5 },
    { "partition": "src/models/", "worker_id": "w3", "duration_seconds": 14, "findings": 1 },
    { "partition": "src/utils/", "worker_id": "w4", "duration_seconds": 9, "findings": 0 }
  ],
  "total_duration_seconds": 24,
  "total_findings": 9,
  "cost_usd": 0.031
}
```

Strategies: `partition` (split by directory or file), `replicate` (run identical nodes with varied configs for consensus), `fan_out` (broadcast input to multiple downstream nodes).

### Pipeline Versioning & Rollback

Pipeline definitions and execution results are version-tracked. Pin stable configurations, compare runs across versions, and roll back to known-good states.

```yaml
versioning:
  pipeline: pr-review-fix
  storage: .cortivex/pipelines/
  retention: { max_versions: 20, max_age_days: 90 }
  current_version: "2.3.1"
  history:
    - version: "2.3.1"
      timestamp: "2026-03-20T14:22:00Z"
      change_summary: "Added partition-based parallel scanning"
    - version: "2.2.0"
      timestamp: "2026-03-12T09:10:00Z"
      change_summary: "Replaced Sonnet with Haiku for LintFixer node"
  rollback:
    enabled: true
    auto_rollback_on: ["cost_exceeded", "critical_failure"]
    cost_exceeded_threshold: 2.0
    snapshot_results: true
```

When `auto_rollback_on` includes `critical_failure`, a failed run reverts the pipeline to the last successful version. The `cost_exceeded` trigger prevents runaway spending by rolling back when actual cost exceeds the threshold multiplier. Use `cortivex rollback <pipeline> <version>` for manual rollback.

## Security Hardening (OWASP AST10 Aligned)

### AST05: Safe YAML Deserialization

Pipeline YAML must be schema-validated before loading (AST05 -- Insecure Output Handling). Use `SAFE_SCHEMA` to disable dangerous constructors (`!!python/object`, `!!js/function`).

```json
{
  "title": "CortivexPipelineSchema", "type": "object",
  "required": ["name", "version", "nodes"], "additionalProperties": false,
  "properties": {
    "name": { "type": "string", "pattern": "^[a-z0-9][a-z0-9-]{1,63}$" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+(\\.\\d+)?$" },
    "nodes": {
      "type": "array", "minItems": 1, "maxItems": 25,
      "items": {
        "type": "object", "required": ["id", "type"], "additionalProperties": false,
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z_][a-z0-9_]{0,63}$" },
          "type": { "type": "string" },
          "depends_on": { "type": "array", "items": { "type": "string" } },
          "config": { "type": "object" }, "retry": { "type": "object" }
        }
      }
    }
  }
}
```

### AST06: Execution Sandboxing

TestRunner and shell-executing nodes run inside container-isolated sandboxes (AST06 -- Excessive Agency).

```yaml
sandbox:
  runtime: container
  resource_limits: { cpu_cores: 2, memory_mb: 2048, network: none, max_pids: 256, timeout_seconds: 300 }
  filesystem:
    read_only_root: true
    writable_paths: [/tmp, /workspace/output]
    blocked_paths: [/etc/shadow, /root, /home/*/.ssh, /var/run/docker.sock]
  capabilities_drop: [NET_RAW, SYS_ADMIN, SYS_PTRACE, MKNOD]
```

```json
{ "method": "cortivex_security_validate", "params": { "check": "sandbox_policy", "pipeline": "pr-review-fix", "enforce": true } }
```

### AST03: Command Allowlists

Shell execution nodes operate under strict allowlists (AST03 -- Excessive Permissions). Arbitrary bash is prohibited in production.

```yaml
command_policy:
  mode: allowlist
  global_blocked: ["rm -rf /", "curl * | bash", "eval", "exec", "> /dev/sd*"]
  node_allowlists:
    TestRunner: ["npm test", "npx jest *", "npx vitest *", "pytest *", "cargo test *", "go test ./..."]
    LintFixer: ["npx eslint * --fix", "npx prettier * --write", "ruff check * --fix"]
    DependencyUpdater: ["npm install", "npm update *", "npm audit fix"]
  argument_sanitization:
    strip_shell_operators: true
    block_path_traversal: true
    max_argument_length: 1024
```

```json
{ "method": "cortivex_command_validate", "params": { "node_type": "TestRunner", "command": "npm test -- --coverage", "policy_file": ".cortivex/security/command-allowlist.yaml" } }
```

### Cost Gates with Automatic Termination

Cost gates enforce hard budget limits with automatic pipeline termination on breach (related to AST06).

```yaml
cost_gates:
  per_node_limits: { default_max_usd: 0.10, overrides: { CodeReviewer: 0.25, RefactorAgent: 0.30 } }
  per_pipeline_limits: { max_cost_usd: 2.00, warning_threshold_pct: 75, hard_stop_threshold_pct: 100 }
  per_hour_limits: { max_cost_usd: 10.00, max_pipeline_runs: 20 }
  actions_on_breach: [terminate_pipeline, log_audit_event]
  cooldown_after_breach: { duration_minutes: 15, require_manual_override: true }
```

```typescript
async function checkCostGate(runId: string): Promise<{
  action: "continue" | "warn" | "terminate";
  budget_consumed_pct: number;
}> {
  return await mcpCall("cortivex_cost_gate_check", { run_id: runId });
}
```

### Dry-Run Enforcement Before Production Execution

Mandatory dry-run validation before production execution of new or modified pipelines prevents accidental runs (AST05, AST06).

```yaml
execution_policy:
  dry_run_enforcement:
    enabled: true
    require_dry_run_for: [new_pipelines, modified_pipelines, { cost_exceeds_usd: 0.50 }]
    dry_run_checks: [dag_validation, schema_validation, command_allowlist, cost_estimation, sandbox_availability]
    dry_run_result_ttl_hours: 24
```

```json
{ "method": "cortivex_execution_policy_check", "params": { "pipeline": "my-new-pipeline", "pipeline_hash": "sha256:a1b2c3d4...", "action": "execute" } }
```

Response when dry-run is required:

```json
{ "allowed": false, "reason": "Pipeline has not been dry-run validated", "ast_risks": ["AST05", "AST06"], "suggestion": "/cortivex run my-new-pipeline --dry-run" }
```
