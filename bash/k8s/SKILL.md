---
name: k8s
description: "MANDATORY parallel execution patterns, cluster overview script, -o json with jq filtering, batch operations, and common pitfalls"
connection_type: k8s
preload: false
---

# Kubernetes CLI Skill

Execute kubectl and helm commands with proper kubeconfig injection.

## Workflow

<critical>
**If no `[cached_from_skill:k8s:discover]` context exists, MUST run the discovery script first:**

```bash
bun run ./_skills/connections/k8s/k8s/scripts/discover.ts
```

The output is auto-cached. Do not re-run unless user explicitly requests refresh.
</critical>

## CLI Tips

### Recommended First Step

Run the cluster discovery script (or the shell script directly):

```bash
bun run ./_skills/connections/k8s/k8s/scripts/discover.ts
# or
./get_k8s_cluster_overview.sh
```

This provides comprehensive cluster analysis (nodes, pods, resources, services, events) in a single parallelized call.
Only run targeted kubectl commands AFTER reviewing the overview output for specific deep-dives.

### Critical Requirements

🚨 MANDATORY: ALL independent kubectl operations MUST run in parallel using background jobs (&) + wait

- FORBIDDEN: Sequential loops `for item in $items; do kubectl get $item; done`
- REQUIRED: Background jobs `for item in $items; do kubectl get $item & done; wait`
- Read-only commands only (get, describe, top, logs) - never modify resources

### Parallel Execution

When to parallelize:

- Multiple namespaces/nodes/pods/resources → ALWAYS parallel
- Operations with data dependencies → Sequential only

Pattern:

```bash
# CORRECT: Parallel (0.5s for 30 pods)
for pod in $pods; do kubectl get pod "$pod" -n "$ns" & done; wait

# WRONG: Sequential (15s for 30 pods)
for pod in $pods; do kubectl get pod "$pod" -n "$ns"; done
```

Best practice - Batch:

```bash
# Fastest: Single kubectl call per namespace
kubectl get pods -n "$ns" -o json | jq '.items[] | {name, phase, ready}'
```

### Output Format

- Complex data: `-o json` with jq (better AI parsing)
  `kubectl get pods -n $ns -o json | jq -r '.items[] | "\(.metadata.name)\t\(.status.phase)"'`
- Simple lists: `-o jsonpath` or `--no-headers` (token efficient)
  `kubectl get pods -n $ns -o jsonpath='{.items[*].metadata.name}'`
- CRITICAL: Always filter JSON with jq - never dump raw output
- Machine-readable only: no decorative formatting, never expose credentials

### Optimization Rules

- Batch operations: Single `kubectl get -o json` instead of multiple calls
  BAD: `kubectl get node $n -o jsonpath='{.status.nodeInfo.machineID}'; kubectl get node $n -o jsonpath='{.status.nodeInfo.kubeletVersion}'`
  GOOD: `kubectl get node $n -o json | jq '{machineID: .status.nodeInfo.machineID, kubeletVersion: .status.nodeInfo.kubeletVersion}'`
- Cache namespaces: Get once and reuse
- Filter at source: Use `--field-selector` and `--selector` before post-processing
- Resource usage: `kubectl top` requires metrics-server; handle gracefully if unavailable

### Common Patterns

- List: `kubectl get <resource> -n <ns> -o json | jq -r '.items[] | ...'`
- Filter by label: `kubectl get pods -n <ns> -l app=myapp`
- Filter by field: `kubectl get pods --field-selector=status.phase=Running`
- Events: `kubectl get events -n <ns> --sort-by='.lastTimestamp'`
- Logs: `kubectl logs <pod> -n <ns> --tail=100` (use cautiously)

### Common Pitfalls

- Multiple calls for same resource → Use single `-o json` + jq
- Not caching namespace list → Cache once
- Sequential namespace processing → Always parallelize
- Raw JSON dumps → Always filter with jq first
- `kubectl describe` verbose → Use `kubectl get -o json | jq` instead

### Helper Script

`./get_k8s_cluster_overview.sh` (in sandbox home) - YOUR GO-TO STARTING POINT
Provides: cluster info, nodes, pods, resources, namespaces, services, events
Usage: `./get_k8s_cluster_overview.sh`
Output: Structured JSON or machine-readable text (all operations parallelized)
TIP: Run this FIRST, then drill down into specific areas based on findings

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

