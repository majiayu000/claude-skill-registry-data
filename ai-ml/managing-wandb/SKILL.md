---
name: managing-wandb
description: |
  Use when working with Wandb — weights & Biases experiment tracking and ML ops
  management. Covers run tracking, sweep management, artifact versioning, report
  analysis, model registry, and team collaboration. Use when managing ML
  experiments, comparing training runs, analyzing hyperparameter sweeps, or
  auditing W&B project resources.
connection_type: wandb
preload: false
---

# Weights & Biases Management Skill

Manage and monitor W&B experiments, sweeps, artifacts, and model registry.

## MANDATORY: Discovery-First Pattern

**Always list projects and recent runs before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

WANDB_ENTITY="${WANDB_ENTITY:-$(wandb whoami 2>/dev/null | head -1)}"

wandb_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $WANDB_API_KEY" \
        "https://api.wandb.ai/api/v1/${endpoint}"
}

wandb_gql() {
    local query="$1"
    curl -s -X POST -H "Authorization: Bearer $WANDB_API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.wandb.ai/graphql" \
        -d "{\"query\": \"$query\"}"
}

echo "=== W&B Entity: $WANDB_ENTITY ==="

echo ""
echo "=== Projects ==="
wandb_gql "{ entity(name: \\\"$WANDB_ENTITY\\\") { projects(first: 20) { edges { node { name, totalRuns, createdAt } } } } }" \
    | jq -r '.data.entity.projects.edges[].node | "\(.name)\t\(.totalRuns) runs\t\(.createdAt[0:10])"' | column -t

echo ""
echo "=== Recent Runs ==="
wandb_gql "{ entity(name: \\\"$WANDB_ENTITY\\\") { projects(first: 5) { edges { node { name, runs(first: 3, order: \\\"-created_at\\\") { edges { node { name, state, createdAt } } } } } } } }" \
    | jq -r '.data.entity.projects.edges[].node | .name as $proj | .runs.edges[].node | "\($proj)\t\(.name)\t\(.state)\t\(.createdAt[0:16])"' | column -t | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

WANDB_ENTITY="${WANDB_ENTITY:-}"
WANDB_BASE="https://api.wandb.ai"

# W&B GraphQL API helper
wandb_gql() {
    local query="$1"
    curl -s -X POST -H "Authorization: Bearer $WANDB_API_KEY" \
        -H "Content-Type: application/json" \
        "${WANDB_BASE}/graphql" \
        -d "{\"query\": \"$query\"}"
}

# W&B CLI wrapper
wb() {
    wandb "$@" 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use GraphQL API with jq for structured queries
- Never dump full run configs -- extract key hyperparameters
- Use run display names, not internal IDs when possible

## Common Operations

### Run Tracking and Comparison

```bash
#!/bin/bash
PROJECT="${1:?Project name required}"

echo "=== Recent Runs in $PROJECT ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { runs(first: 15, order: \\\"-created_at\\\") { edges { node { name, displayName, state, createdAt, summaryMetrics, config } } } } }" \
    | jq -r '.data.project.runs.edges[].node | "\(.displayName // .name)\t\(.state)\t\(.createdAt[0:16])\t\(.summaryMetrics | fromjson? | to_entries[:3] | map("\(.key)=\(.value | tostring[0:8])") | join(","))"' | column -t

echo ""
echo "=== Run States Summary ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { runs(first: 100) { edges { node { state } } } } }" \
    | jq '.data.project.runs.edges | group_by(.node.state) | map({state: .[0].node.state, count: length})'
```

### Sweep Management

```bash
#!/bin/bash
PROJECT="${1:?Project name required}"

echo "=== Active Sweeps ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { sweeps { edges { node { name, displayName, state, runCount, bestLoss, config } } } } }" \
    | jq -r '.data.project.sweeps.edges[].node | "\(.displayName // .name)\t\(.state)\t\(.runCount) runs\tbest_loss=\(.bestLoss // "N/A")"' | column -t

SWEEP_ID="${2:-}"
if [ -n "$SWEEP_ID" ]; then
    echo ""
    echo "=== Sweep Runs: $SWEEP_ID ==="
    wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { sweep(sweepName: \\\"$SWEEP_ID\\\") { runs(first: 10, order: \\\"summaryMetrics.val_loss\\\") { edges { node { name, displayName, state, summaryMetrics } } } } } }" \
        | jq -r '.data.project.sweep.runs.edges[].node | "\(.displayName // .name)\t\(.state)\t\(.summaryMetrics | fromjson? | to_entries[:4] | map("\(.key)=\(.value | tostring[0:8])") | join(","))"' | column -t
fi
```

### Artifact Versioning

```bash
#!/bin/bash
PROJECT="${1:?Project name required}"

echo "=== Artifact Collections ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { artifactCollections(first: 20) { edges { node { name, type, totalArtifacts, createdAt } } } } }" \
    | jq -r '.data.project.artifactCollections.edges[].node | "\(.name)\t\(.type)\t\(.totalArtifacts) versions\t\(.createdAt[0:10])"' | column -t

ARTIFACT="${2:-}"
if [ -n "$ARTIFACT" ]; then
    echo ""
    echo "=== Versions of $ARTIFACT ==="
    wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { artifactCollection(name: \\\"$ARTIFACT\\\") { artifacts(first: 10) { edges { node { versionIndex, state, size, createdAt, aliases { alias } } } } } } }" \
        | jq -r '.data.project.artifactCollection.artifacts.edges[].node | "v\(.versionIndex)\t\(.state)\t\(.size) bytes\t\(.aliases | map(.alias) | join(","))\t\(.createdAt[0:16])"' | column -t
fi
```

### Run Detail and Metrics

```bash
#!/bin/bash
PROJECT="${1:?Project name required}"
RUN_ID="${2:?Run ID required}"

echo "=== Run Details ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { run(name: \\\"$RUN_ID\\\") { name, displayName, state, createdAt, heartbeatAt, config, summaryMetrics, tags } } }" \
    | jq '{
        name: .data.project.run.displayName,
        state: .data.project.run.state,
        created: .data.project.run.createdAt,
        last_heartbeat: .data.project.run.heartbeatAt,
        tags: .data.project.run.tags,
        config: (.data.project.run.config | fromjson? | del(.["_wandb"]) | to_entries[:10] | map({(.key): .value}) | add),
        summary: (.data.project.run.summaryMetrics | fromjson? | del(.["_wandb"]) | to_entries[:10] | map({(.key): .value}) | add)
    }'
```

### Report Analysis

```bash
#!/bin/bash
PROJECT="${1:?Project name required}"

echo "=== Reports ==="
wandb_gql "{ project(name: \\\"$PROJECT\\\", entityName: \\\"$WANDB_ENTITY\\\") { views(first: 10) { edges { node { name, displayName, createdAt, updatedAt, type } } } } }" \
    | jq -r '.data.project.views.edges[].node | "\(.displayName // .name)\t\(.type)\t\(.updatedAt[0:16])"' | column -t
```

## Safety Rules

- **NEVER delete runs or artifacts** without explicit confirmation -- data loss is permanent
- **NEVER stop active sweeps** without verifying no critical runs are in progress
- **Always check artifact aliases** before deleting versions -- "latest" or "production" aliases indicate active usage
- **Be cautious with sweep early termination** -- ensure sufficient runs have completed for valid comparison
- **API rate limits**: W&B enforces rate limits -- batch queries where possible

## Output Format

Present results as a structured report:
```
Managing Wandb Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **API key scope**: API keys are scoped to users -- team resources may require specific entity context
- **Run states**: "crashed" runs may still hold GPU resources -- check the actual compute instance
- **Sweep agents**: Stopping a sweep does not stop running agents -- agents must be terminated separately
- **Artifact aliases**: Moving "production" alias to a new version is immediate -- downstream consumers update automatically
- **Config serialization**: Complex config values (dicts, lists) are JSON-serialized in the API -- parse with `fromjson`
- **Metric step alignment**: Different metrics may be logged at different steps -- use `step` parameter for alignment
- **Offline mode**: Runs in offline mode sync later -- they may not appear immediately in the project
- **Team permissions**: Project visibility settings affect API access -- private projects need explicit team membership
