---
name: capacity
description: Analyze service capacity, load patterns, and scaling requirements
---

# Capacity Planning Analysis

**Current Time:** !`date`
**K8s Context:** !`kubectl config current-context`

Analyze service capacity, load patterns, and scaling requirements. Generates forecasts and recommendations for resource planning. Documents to Obsidian.

## Input

- Target: service, cluster, or infrastructure component
- Context: current traffic patterns, growth expectations
- Optional: specific scaling concerns or upcoming events

## Investigation Strategy

Launch parallel investigation tracks:

### Track 1: Codebase Exploration (explore agent)

- Find autoscaling configuration
- Identify resource requests/limits
- Locate performance-critical code paths
- Map service dependencies

### Track 2: Infrastructure Analysis (inferred agent: k8s/gcp-dev/sre)

- Review current resource utilization
- Analyze scaling policies
- Check quota and limits
- Assess headroom and buffer

### Track 3: External Research (librarian agent)

- Find capacity planning best practices
- Research scaling patterns for similar workloads
- Identify industry benchmarks

## Output

Write to Obsidian via `obsidian_append_content` at:
`$OBSIDIAN_PATH/Capacity/YYYY-MM-DD-service-analysis.md`

> **Note**: `$OBSIDIAN_PATH` must be a vault-relative path (e.g., `Projects/myapp`), set per-project via direnv. The `obsidian_append_content` tool expects paths relative to the vault root.

### Document Structure

Use this template for the Obsidian document:

@~/.config/opencode/templates/capacity-analysis.md

## Behavior

1. Parse target to identify service and infrastructure scope
2. Infer appropriate infrastructure agent (k8s, gcp-dev, sre)
3. Launch explore, librarian, and inferred agent in parallel
4. Analyze current utilization and scaling configuration
5. Identify load patterns and growth trends
6. Generate capacity forecast with resource requirements
7. Identify bottlenecks and risks
8. Write analysis to Obsidian via `obsidian_append_content` with auto-generated filename: `YYYY-MM-DD-service-analysis.md`

$ARGUMENTS
