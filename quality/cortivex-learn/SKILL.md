---
name: cortivex-learn
version: 1.0.0
description: Self-learning system that records and applies insights from pipeline executions
category: learning
tags: [learning, insights, optimization, patterns, self-improvement]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [insight-recording, pattern-detection, pipeline-optimization, confidence-scoring]
---

# Cortivex Learning System

You have access to a learning system that improves pipeline performance over time. After each pipeline run, insights are automatically recorded. Before starting work, you should consult past insights to make better decisions.

## How Learning Works

The Cortivex learning system operates on a feedback loop:

1. **Observe** -- Each pipeline run produces metrics: duration per node, cost per node, success/failure, error types, and output quality signals.
2. **Analyze** -- The system compares these metrics against historical data for the same repository, same pipeline template, and similar task types.
3. **Record** -- Actionable insights are stored with confidence scores, scoped to the repository, pipeline, or node type.
4. **Apply** -- On future runs, insights are surfaced to agents and the orchestrator to optimize execution.

## Checking Insights Before Starting Work

Before every pipeline run, query the learning system for relevant insights:

```
cortivex_insights({
  action: "query",
  repo: "/path/to/repo",
  pipeline: "pr-review",
  node_types: ["SecurityScanner", "CodeReviewer", "AutoFixer"],
  min_confidence: 0.6
})
```

**Response:**

```json
{
  "insights": [
    {
      "id": "ins-7a3b",
      "type": "reorder",
      "confidence": 0.87,
      "description": "Running CodeReviewer before SecurityScanner reduces total duration by 22% in this repo because security scans on already-reviewed code skip false positives",
      "evidence": {
        "sample_size": 14,
        "avg_improvement": "22% faster",
        "last_observed": "2025-01-14T18:30:00Z"
      },
      "recommendation": {
        "action": "reorder",
        "move": "CodeReviewer",
        "before": "SecurityScanner"
      }
    },
    {
      "id": "ins-9c4d",
      "type": "substitute_model",
      "confidence": 0.73,
      "description": "For this repo, using claude-haiku-4-20250414 for SecurityScanner produces equivalent results to claude-sonnet-4-20250514 at 85% lower cost",
      "evidence": {
        "sample_size": 8,
        "quality_delta": "-2% (within noise)",
        "cost_savings": "85%",
        "last_observed": "2025-01-13T09:15:00Z"
      },
      "recommendation": {
        "action": "substitute_model",
        "node": "SecurityScanner",
        "from": "claude-sonnet-4-20250514",
        "to": "claude-haiku-4-20250414"
      }
    },
    {
      "id": "ins-2e5f",
      "type": "add_node",
      "confidence": 0.65,
      "description": "PRs in this repo that include a LintFixer step before TestRunner have a 40% lower failure rate in CI",
      "evidence": {
        "sample_size": 6,
        "failure_rate_with": "12%",
        "failure_rate_without": "52%",
        "last_observed": "2025-01-12T14:00:00Z"
      },
      "recommendation": {
        "action": "add_node",
        "node_type": "LintFixer",
        "insert_before": "TestRunner"
      }
    }
  ]
}
```

### How to Apply Insights

When insights are returned, evaluate them and apply high-confidence ones:

**Confidence >= 0.80:** Apply automatically. Inform the user what was optimized and why.

```
Optimization applied: Reordered CodeReviewer before SecurityScanner
(87% confidence, based on 14 previous runs: 22% faster on average)
```

**Confidence 0.60-0.79:** Suggest to the user and apply if approved, or apply with a note.

```
Suggestion: Use claude-haiku-4-20250414 for SecurityScanner to save ~85% cost
(73% confidence, based on 8 runs with equivalent quality)
Apply this optimization? [Y/n]
```

**Confidence < 0.60:** Present as informational only. Do not apply automatically.

```
Note: Early data (3 runs) suggests adding a LintFixer step could reduce CI failures.
Not enough evidence to recommend yet. Will continue monitoring.
```

## Insight Types

### reorder

Changing the execution order of nodes for better performance.

**When generated:** The system detects that a different node ordering consistently produces faster runs, lower costs, or higher success rates.

**Structure:**
```json
{
  "type": "reorder",
  "recommendation": {
    "action": "reorder",
    "move": "<node_id>",
    "before": "<other_node_id>"
  }
}
```

**How to apply:** Modify the `depends_on` chains in the pipeline to reflect the new order. Ensure the DAG remains valid (no cycles, no broken dependencies).

### substitute_model

Using a different AI model for a node to optimize cost or quality.

**When generated:** The system compares outputs across model variants and finds that a cheaper or faster model produces equivalent results for a specific node type in a specific context.

**Structure:**
```json
{
  "type": "substitute_model",
  "recommendation": {
    "action": "substitute_model",
    "node": "<node_id>",
    "from": "<current_model>",
    "to": "<recommended_model>"
  }
}
```

**How to apply:** Update the node's `config.model` field. Monitor the next few runs to confirm quality is maintained.

### skip_node

Skipping a node that provides no value in a specific context.

**When generated:** The system detects that a node consistently produces no actionable output for a repository or file set. For example, a SecurityScanner that never finds issues in a static documentation repo.

**Structure:**
```json
{
  "type": "skip_node",
  "recommendation": {
    "action": "skip_node",
    "node": "<node_id>",
    "reason": "No issues found in last 12 runs on this repo"
  }
}
```

**How to apply:** Add a `condition` to the node that skips it, or remove it from the pipeline. Always inform the user when skipping a node.

### add_node

Adding a node that would improve pipeline outcomes.

**When generated:** The system identifies a pattern where pipelines that include an extra step have significantly better outcomes. For example, adding a LintFixer before TestRunner reduces test failures.

**Structure:**
```json
{
  "type": "add_node",
  "recommendation": {
    "action": "add_node",
    "node_type": "<NodeType>",
    "insert_before": "<existing_node_id>",
    "config": { /* suggested config */ }
  }
}
```

**How to apply:** Add the recommended node to the pipeline and wire its dependencies appropriately.

### adjust_config

Tuning a node's configuration for better results.

**When generated:** The system identifies that specific configuration values consistently produce better outcomes. For example, increasing `scan_depth` for SecurityScanner in repos with deep dependency trees.

**Structure:**
```json
{
  "type": "adjust_config",
  "recommendation": {
    "action": "adjust_config",
    "node": "<node_id>",
    "changes": {
      "scan_depth": { "from": "shallow", "to": "deep" },
      "timeout_seconds": { "from": 120, "to": 300 }
    }
  }
}
```

### adjust_timeout

Modifying timeout values based on observed execution times.

**When generated:** Nodes consistently finish much faster than their timeout (wasted buffer) or consistently time out (timeout too low).

**Structure:**
```json
{
  "type": "adjust_timeout",
  "recommendation": {
    "action": "adjust_timeout",
    "node": "<node_id>",
    "current_timeout": 120,
    "recommended_timeout": 300,
    "p95_duration": 245
  }
}
```

## Recording Insights After Pipeline Completion

After each pipeline run completes, the system automatically records execution data. You can also manually record insights from your observations:

### Automatic Recording

The orchestrator automatically records:
- Duration per node
- Cost per node
- Success/failure status and error types
- Output quality signals (e.g., number of issues found, test pass rate)
- Resource utilization

### Manual Insight Recording

If you observe a pattern that the automatic system might not catch, record it manually:

```
cortivex_insights({
  action: "record",
  repo: "/path/to/repo",
  insight: {
    type: "reorder",
    description: "Running tests before code review in this repo saves time because the test suite is fast (< 10s) and review can focus on passing code",
    confidence: 0.70,
    evidence: {
      observation: "Manual observation across 3 runs",
      metrics: {
        "duration_with_reorder": "2m 10s",
        "duration_without": "3m 45s"
      }
    },
    recommendation: {
      action: "reorder",
      move: "TestRunner",
      before: "CodeReviewer"
    },
    scope: {
      repo: "/path/to/repo",
      pipeline: "pr-review"
    }
  }
})
```

### Recording Quality Observations

If you notice that a node's output was particularly good or bad, record a quality signal:

```
cortivex_insights({
  action: "record_quality",
  run_id: "ctx-a1b2c3",
  node_id: "code_review",
  quality: "high",
  reason: "Caught a subtle race condition that would have caused production issues",
  tags: ["concurrency", "race-condition", "high-value-find"]
})
```

Or for poor quality:

```
cortivex_insights({
  action: "record_quality",
  run_id: "ctx-a1b2c3",
  node_id: "auto_fix",
  quality: "low",
  reason: "Auto-fix introduced a type error that broke compilation",
  tags: ["type-error", "regression", "needs-review"]
})
```

## Insight Lifecycle

Insights have a lifecycle controlled by confidence scores:

### Confidence Score Calculation

```
confidence = base_signal * consistency * recency * sample_weight

where:
  base_signal   = strength of the observed effect (0.0 - 1.0)
  consistency   = how often the pattern holds (0.0 - 1.0)
  recency       = decay factor for old observations (0.5 - 1.0)
  sample_weight = log(sample_size) / log(max_expected_samples)
```

### Confidence Evolution

- **New insight (1-3 observations):** Confidence typically 0.30-0.50. Treated as hypothesis.
- **Developing (4-8 observations):** Confidence rises to 0.50-0.75 if pattern holds.
- **Established (9+ observations):** Confidence reaches 0.75-0.95 if consistent.
- **Decaying:** If recent observations contradict the pattern, confidence drops.
- **Retired:** If confidence drops below 0.20, the insight is archived.

### Viewing Insight History

```
cortivex_insights({
  action: "history",
  repo: "/path/to/repo",
  limit: 20,
  include_retired: false
})
```

**Response:**

```json
{
  "insights": [
    {
      "id": "ins-7a3b",
      "type": "reorder",
      "confidence": 0.87,
      "created_at": "2025-01-02T10:00:00Z",
      "updated_at": "2025-01-14T18:30:00Z",
      "observation_count": 14,
      "status": "established",
      "trend": "stable"
    },
    {
      "id": "ins-9c4d",
      "type": "substitute_model",
      "confidence": 0.73,
      "created_at": "2025-01-05T14:00:00Z",
      "updated_at": "2025-01-13T09:15:00Z",
      "observation_count": 8,
      "status": "developing",
      "trend": "rising"
    }
  ]
}
```

## Applying Insights in Practice

### Before a Pipeline Run

1. Query insights for the target repo and pipeline type
2. Sort by confidence (highest first)
3. Apply high-confidence insights automatically
4. Present medium-confidence insights as suggestions
5. Note low-confidence insights for awareness

### During a Pipeline Run

If a node produces unusual results (much faster/slower than expected, unexpected failures, exceptional quality), note this for post-run analysis.

### After a Pipeline Run

1. Automatic metrics are recorded by the system
2. Review results for patterns the automatic system might miss
3. Record any manual observations
4. Check if existing insights are confirmed or contradicted by the new data

### Example Workflow

```
User: /cortivex run pr-review

Agent thinking:
1. Query insights for this repo + pr-review pipeline
2. Found: "Reorder CodeReviewer before SecurityScanner" (87% confidence)
3. Found: "Use haiku for SecurityScanner" (73% confidence)
4. Found: "Add LintFixer before TestRunner" (65% confidence)

Agent response:
"Running pr-review pipeline with optimizations:
 - Applied: CodeReviewer runs before SecurityScanner (87% confidence, 22% faster)
 - Suggested: Use claude-haiku-4-20250414 for SecurityScanner to save ~85% cost.
   Apply? [Y/n]
 - Note: Early data suggests adding LintFixer could help. Monitoring."
```

## Insight Scoping

Insights are scoped at multiple levels:

1. **Global** -- Applies to all repos and all pipelines. Example: "TestRunner nodes with timeout < 60s fail 30% of the time."
2. **Pipeline** -- Applies to a specific pipeline template. Example: "pr-review pipelines benefit from LintFixer before TestRunner."
3. **Repository** -- Applies to a specific repo. Example: "In repo X, SecurityScanner finds no issues because there are no dependencies."
4. **Repo + Pipeline** -- Most specific. Example: "In repo X with pr-review, CodeReviewer before SecurityScanner saves 22%."

More specific insights override less specific ones when they conflict.

## Deleting or Overriding Insights

If an insight is no longer valid:

```
cortivex_insights({
  action: "retire",
  insight_id: "ins-7a3b",
  reason: "Repository was restructured; node ordering no longer matters"
})
```

To override an insight with a manual preference:

```
cortivex_insights({
  action: "override",
  insight_id: "ins-9c4d",
  override: {
    action: "ignore",
    reason: "We prefer to use sonnet for security scanning regardless of cost"
  }
})
```

Overrides are permanent until removed. They prevent the insight from being applied but do not delete the underlying data.

## Reasoning Protocol

Before applying any insight, reason through:

1. **Is the sample size sufficient?** Insights with fewer than 5 observations are hypotheses, not facts. Treat them as informational only.
2. **Is the evidence recent?** An insight from 30 runs ago may no longer apply if the codebase has changed significantly. Check `last_observed` timestamps.
3. **Does the insight match the current context?** A model substitution insight for a small repo may not hold for a larger one. Verify the scope matches.
4. **Could this insight cause harm if wrong?** Reordering nodes is low-risk (worst case: slightly slower). Skipping a SecurityScanner is high-risk (could miss vulnerabilities). Weight risk against confidence.
5. **Am I stacking too many optimizations?** Applying multiple insights simultaneously makes it impossible to attribute improvements or regressions. Apply one high-confidence insight at a time and measure.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Auto-applying low-confidence insights | Unreliable optimizations cause regressions | Only auto-apply at confidence >= 0.80 |
| Ignoring all insights | Misses genuine optimizations, wastes cost | Review insights before every run; apply high-confidence ones |
| Overriding insights without recording why | Loses institutional knowledge about what was tried | Always provide a `reason` when overriding |
| Applying insights across different repos | What works for repo A may fail for repo B | Check insight scope; use repo-specific insights |
| Never retiring stale insights | Outdated patterns get applied to changed codebases | Review and retire insights when repos undergo major refactors |
| Treating confidence as binary | 0.73 and 0.95 are not equally trustworthy | Use the tiered approach: auto (>0.80), suggest (0.60-0.80), note (<0.60) |

## Grounding Rules

- **Contradictory insights:** When two insights conflict (e.g., one says reorder, another says keep order), present both to the user with their evidence and let them decide. Do not silently pick one.
- **Insight confidence is dropping:** This means recent observations contradict the pattern. Stop applying the insight and investigate what changed.
- **No insights available for this repo:** This is normal for new repos. Run the pipeline without optimizations and let the system accumulate data.
- **User disagrees with an insight:** Record an override with their reasoning. The system will continue tracking the pattern but will not apply it.
- **Quality signal is ambiguous:** When you cannot determine if a node's output was high or low quality, do not record a quality signal. Noise in quality data degrades all future insights.

## Advanced Capabilities

These capabilities extend the learning system into active training, experimentation, and adaptive optimization.

### Reinforcement Learning Integration

Pipeline outcomes serve as reward signals. Use `cortivex_learn_train` to submit episodes:

```json
{
  "tool": "cortivex_learn_train",
  "request": {
    "action": "submit_episode", "repo": "/path/to/repo", "pipeline": "pr-review",
    "episode": {
      "state": { "repo_size": "large", "file_types": ["typescript", "python"] },
      "actions_taken": [
        { "node": "CodeReviewer", "model": "claude-sonnet-4-20250514", "order": 1 },
        { "node": "SecurityScanner", "model": "claude-haiku-4-20250414", "order": 2 } ],
      "reward": { "duration_score": 0.85, "cost_score": 0.92, "quality_score": 0.78, "composite": 0.84 }
    } }
}
```

```json
{
  "tool": "cortivex_learn_train",
  "response": {
    "status": "accepted", "episode_id": "ep-4f8a2c", "policy_version": "v2.14",
    "updated_q_values": { "CodeReviewer_first": 0.81, "SecurityScanner_first": 0.63 },
    "exploration_rate": 0.15
  }
}
```

The `exploration_rate` decays as the policy accumulates episodes, shifting from exploration to exploitation.

### A/B Testing Pipeline Configurations

Define controlled experiments to compare pipeline configurations:

```yaml
experiment:
  id: exp-model-swap-security
  name: "Haiku vs Sonnet for SecurityScanner"
  pipeline: pr-review
  duration: { max_runs: 50, deadline: "2026-04-15T00:00:00Z" }
  groups:
    control: { weight: 0.5, config: { SecurityScanner: { model: claude-sonnet-4-20250514 } } }
    variant_a: { weight: 0.5, config: { SecurityScanner: { model: claude-haiku-4-20250414 } } }
  metrics: { primary: quality_score, secondary: [duration_seconds, cost_usd] }
  significance: { method: welch_t_test, alpha: 0.05, min_samples_per_group: 20 }
```

When the experiment reaches its threshold, the winner is promoted to an insight.

### Model Performance Tracking

Per-node execution metrics use this JSON schema:

```json
{
  "title": "NodeExecutionMetrics",
  "type": "object",
  "required": ["run_id", "node_id", "timestamp", "metrics"],
  "properties": {
    "run_id": { "type": "string", "pattern": "^ctx-[a-z0-9]+$" },
    "node_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "metrics": {
      "type": "object", "required": ["duration_ms", "cost_usd", "status"],
      "properties": {
        "duration_ms": { "type": "integer" }, "cost_usd": { "type": "number" },
        "status": { "enum": ["success", "failure", "timeout", "skipped"] },
        "tokens_in": { "type": "integer" }, "tokens_out": { "type": "integer" },
        "quality_score": { "type": "number", "maximum": 1.0 }
      } }
  }
}
```

Metrics are aggregated into percentile distributions (p50, p90, p95, p99) for insight generation.

### Adaptive Optimization Strategies

Use `cortivex_learn_optimize` to generate optimized configurations from learning data:

```json
{
  "tool": "cortivex_learn_optimize",
  "request": {
    "action": "generate_plan", "repo": "/path/to/repo", "pipeline": "pr-review",
    "objective": "balanced",
    "constraints": { "max_cost_usd": 0.50, "max_duration_seconds": 300, "min_quality_score": 0.75 }
  }
}
```

```json
{
  "tool": "cortivex_learn_optimize",
  "response": {
    "plan_id": "opt-7b3e9f",
    "strategies": [{
      "rank": 1, "confidence": 0.88,
      "projected": { "duration_s": 145, "cost_usd": 0.12, "quality": 0.82 },
      "changes": [
        { "action": "reorder", "move": "CodeReviewer", "before": "SecurityScanner" },
        { "action": "substitute_model", "node": "SecurityScanner", "to": "claude-haiku-4-20250414" } ]
    }] }
}
```

The `objective` parameter accepts `speed`, `cost`, `quality`, or `balanced`, each weighting criteria differently.

### Confidence Calibration & Scoring

Confidence thresholds are configurable per action type. Higher-risk actions require stricter thresholds:

```json
{
  "title": "ConfidenceThresholdConfig",
  "type": "object",
  "required": ["default_thresholds"],
  "properties": {
    "default_thresholds": {
      "properties": {
        "auto_apply": { "type": "number", "maximum": 1.0 },
        "suggest": { "type": "number", "maximum": 1.0 },
        "note": { "type": "number", "maximum": 1.0 } }
    },
    "action_overrides": {
      "additionalProperties": {
        "properties": { "auto_apply": { "type": "number" }, "suggest": { "type": "number" }, "min_samples": { "type": "integer" } } }
    },
    "calibration": { "properties": { "enabled": { "type": "boolean" }, "recalibrate_interval_runs": { "type": "integer" }, "brier_score_target": { "type": "number" } } }
  }
}
```

```typescript
const confidenceConfig: ConfidenceThresholdConfig = {
  default_thresholds: { auto_apply: 0.80, suggest: 0.60, note: 0.30 },
  action_overrides: {
    skip_node: { auto_apply: 0.92, suggest: 0.75, min_samples: 10 },
    reorder: { auto_apply: 0.75, suggest: 0.55, min_samples: 5 },
    substitute_model: { auto_apply: 0.80, suggest: 0.65, min_samples: 8 },
    add_node: { auto_apply: 0.85, suggest: 0.70, min_samples: 6 }
  },
  calibration: { enabled: true, recalibrate_interval_runs: 50, brier_score_target: 0.15 }
};
```

The calibration subsystem periodically checks whether confidence scores align with actual outcomes using the Brier score, adjusting scoring formula weights when the target is exceeded.

## Security Hardening (OWASP AST10 Aligned)

Security controls for the learning system aligned with the OWASP Automated Security Testing Top 10 risk framework.

### AST03: Security Node Skip Prevention

The `skip_node` insight type must never target security-critical nodes. `SecurityScanner` cannot be auto-skipped regardless of confidence score.

```yaml
security_node_protection:
  # AST03 -- Prevent skip recommendations on security-critical nodes
  protected_node_types: [SecurityScanner, DependencyAuditor, SecretDetector, LicenseChecker]
  enforcement: hard_block
  override_allowed: false
  behavior_on_skip_attempt:
    action: reject_and_log
    log_level: warn
    message: "AST03 violation: skip_node targeting protected node '{node_type}' blocked"
```

```json
{
  "tool": "cortivex_insights",
  "request": { "action": "apply", "insight_id": "ins-skip-sec", "repo": "/path/to/repo" },
  "response": {
    "status": "rejected",
    "reason": "AST03: SecurityScanner is a protected node type and cannot be skipped",
    "insight_type": "skip_node", "target_node": "SecurityScanner", "confidence": 0.94
  }
}
```

### AST03: Model Downgrade Protection

Security-critical nodes are locked to a minimum model tier. The `substitute_model` insight must not downgrade a protected node below its floor.

```yaml
model_tier_policy:
  # AST03 -- Model floor for security-critical nodes
  minimum_model_tiers:
    SecurityScanner: { min_tier: sonnet, allowed: [claude-sonnet-4-20250514, claude-opus-4-20250514], enforcement: hard_block }
    DependencyAuditor: { min_tier: sonnet, allowed: [claude-sonnet-4-20250514, claude-opus-4-20250514], enforcement: hard_block }
  audit: { log_downgrade_attempts: true, alert_on_repeated_attempts: 3 }
```

```json
{
  "title": "ModelDowngradeValidation", "type": "object",
  "required": ["node_type", "requested_model", "allowed", "ast_reference"],
  "properties": {
    "node_type": { "type": "string" }, "requested_model": { "type": "string" },
    "allowed": { "type": "boolean" }, "ast_reference": { "type": "string", "const": "AST03" },
    "minimum_tier": { "type": "string", "enum": ["haiku", "sonnet", "opus"] }
  }
}
```

### Insight Poisoning Detection

Anomalous insight patterns trigger quarantine and review. Monitors for statistical outliers that could indicate data poisoning.

```yaml
insight_poisoning_detection:
  enabled: true
  anomaly_triggers:
    - type: sudden_confidence_spike
      threshold: { min_delta: 0.35, max_observations: 3 }
      action: quarantine_and_review
    - type: contradictory_burst
      threshold: { max_contradictions: 3, window_minutes: 30 }
      action: freeze_insight_recording
    - type: skip_targeting  # AST03
      threshold: { max_attempts: 2, window_hours: 24 }
      action: alert_and_block
    - type: mass_downgrade
      threshold: { min_batch_size: 5, downgrade_percentage: 0.80 }
      action: quarantine_and_review
  quarantine: { duration_hours: 48, requires_manual_review: true, notify: [security-ops] }
```

```json
{
  "tool": "cortivex_insights",
  "request": { "action": "record", "repo": "/path/to/repo", "insight": { "type": "skip_node", "node": "SecurityScanner" } },
  "response": {
    "status": "quarantined", "reason": "Insight poisoning: skip_targeting triggered (AST03)",
    "quarantine_id": "q-8f3a1b", "review_required": true
  }
}
```

### A/B Test Safety Constraints

Security-critical nodes must appear identically configured in both control and all variant groups.

```yaml
ab_test_safety:
  invariant_nodes:
    - { node_type: SecurityScanner, must_be_present: true, config_must_match: true, model_must_match: true }
    - { node_type: DependencyAuditor, must_be_present: true, config_must_match: true }
  validation_rules:
    - { rule: no_security_node_removal, ast_reference: "AST03", enforcement: pre_experiment_gate }
    - { rule: no_security_model_variance, enforcement: pre_experiment_gate }
    - { rule: no_security_config_variance, enforcement: pre_experiment_gate }
  on_violation: { action: reject_experiment, message: "Experiment '{experiment_id}' violates A/B safety: {rule}" }
```

```typescript
interface ABTestSecurityValidation {
  experiment_id: string;
  groups_checked: string[];
  invariant_nodes_verified: Array<{
    node_type: string; present_in_all_groups: boolean;
    config_identical: boolean; model_identical: boolean;
  }>;
  validation_passed: boolean;
  violations: Array<{ rule: string; group: string; node_type: string; ast_reference: string }>;
}
```

### Learning Data Isolation Between Repositories

Insight data is partitioned per repository with encrypted storage. Cross-repo access is only allowed through the `cortivex-cross-repo` promotion pipeline which enforces anonymization and privacy checks.

```yaml
learning_data_isolation:
  storage: { partition_key: repository_id, encryption: aes-256-gcm, key_derivation: per_repository }
  access_control:
    cross_repo_direct_access: denied
    allowed_cross_repo_path: "cortivex-cross-repo.promote"
    audit_all_access: true
  validation:
    - { check: partition_boundary, enforcement: query_interceptor }
    - { check: no_repo_id_in_global, enforcement: promotion_pipeline, ast_reference: "AST03" }
  isolation_breach_response: { action: deny_and_alert, alert_channel: security-ops }
```

```json
{
  "tool": "cortivex_insights",
  "request": { "action": "query", "repo": "/path/to/other-repo", "caller_repo": "/path/to/my-repo" },
  "response": {
    "status": "denied",
    "reason": "Learning data isolation: caller repo does not match target. Use cortivex_crossrepo({ action: 'import' }) instead.",
    "caller_repo": "/path/to/my-repo", "target_repo": "/path/to/other-repo"
  }
}
```
