---
name: managing-helm
description: |
  Use when working with Helm — helm chart management for Kubernetes deployments.
  Covers chart installation, upgrade, rollback, release history, repository
  management, template rendering, dependency resolution, and values inspection.
  Use when managing Helm releases, debugging chart issues, or reviewing
  deployment configurations.
connection_type: helm
preload: false
---

# Helm Management Skill

Manage Helm charts, releases, repositories, and template rendering for Kubernetes.

## Core Helper Functions

```bash
#!/bin/bash

# Helm command wrapper with namespace support
helm_cmd() {
    helm "$@" 2>/dev/null
}

# Get release values as JSON
helm_values() {
    local release="$1"
    local ns="${2:-default}"
    helm get values "$release" -n "$ns" -o json 2>/dev/null
}

# List releases across all namespaces
helm_all() {
    helm list -A -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.namespace)\t\(.chart)\t\(.status)\t\(.app_version)"' | column -t
}
```

## MANDATORY: Discovery-First Pattern

**Always list releases and repos before operating on specific charts.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Helm Version ==="
helm version --short 2>/dev/null

echo ""
echo "=== Configured Repositories ==="
helm repo list -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.url)"' | column -t

echo ""
echo "=== All Releases (all namespaces) ==="
helm list -A -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.namespace)\t\(.chart)\t\(.status)\t\(.updated[0:19])"' | column -t | head -30

echo ""
echo "=== Failed/Pending Releases ==="
helm list -A --failed --pending -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.namespace)\t\(.status)\t\(.chart)"' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq filtering for structured data
- Never dump full chart values -- extract relevant sections

## Common Operations

### Release Health Dashboard

```bash
#!/bin/bash
echo "=== Release Status Summary ==="
helm list -A -o json 2>/dev/null | jq '{
    total: length,
    deployed: [.[] | select(.status == "deployed")] | length,
    failed: [.[] | select(.status == "failed")] | length,
    pending: [.[] | select(.status == "pending-install" or .status == "pending-upgrade")] | length,
    superseded: [.[] | select(.status == "superseded")] | length
}'

echo ""
echo "=== Outdated Charts ==="
for release in $(helm list -A -o json | jq -r '.[].name'); do
    NS=$(helm list -A -o json | jq -r --arg r "$release" '.[] | select(.name == $r) | .namespace')
    CHART=$(helm list -A -o json | jq -r --arg r "$release" '.[] | select(.name == $r) | .chart')
    echo "$release ($NS): $CHART"
done | head -20
```

### Release Inspection

```bash
#!/bin/bash
RELEASE="${1:?Release name required}"
NS="${2:-default}"

echo "=== Release Info: $RELEASE ==="
helm status "$RELEASE" -n "$NS" -o json 2>/dev/null | jq '{
    name: .name,
    namespace: .namespace,
    status: .info.status,
    revision: .version,
    chart: .chart.metadata.name,
    chart_version: .chart.metadata.version,
    app_version: .chart.metadata.appVersion,
    deployed_at: .info.last_deployed,
    description: .info.description
}'

echo ""
echo "=== Release History (last 5) ==="
helm history "$RELEASE" -n "$NS" -o json 2>/dev/null | jq -r '
    .[-5:][] | "\(.revision)\t\(.status)\t\(.chart)\t\(.updated[0:19])\t\(.description[0:50])"
' | column -t

echo ""
echo "=== User-Supplied Values ==="
helm get values "$RELEASE" -n "$NS" -o json 2>/dev/null | jq '.' | head -30
```

### Template Rendering & Validation

```bash
#!/bin/bash
CHART="${1:?Chart path or name required}"
VALUES_FILE="${2:-}"

echo "=== Chart Info ==="
helm show chart "$CHART" 2>/dev/null | head -15

echo ""
echo "=== Template Dry-Run ==="
if [ -n "$VALUES_FILE" ]; then
    helm template test-release "$CHART" -f "$VALUES_FILE" 2>/dev/null | head -60
else
    helm template test-release "$CHART" 2>/dev/null | head -60
fi

echo ""
echo "=== Lint Results ==="
helm lint "$CHART" ${VALUES_FILE:+-f "$VALUES_FILE"} 2>&1 | tail -10
```

### Repository Management

```bash
#!/bin/bash
echo "=== Configured Repos ==="
helm repo list -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.url)"' | column -t

echo ""
echo "=== Updating Repos ==="
helm repo update 2>&1 | tail -10

echo ""
echo "=== Search for Chart ==="
SEARCH="${1:-nginx}"
helm search repo "$SEARCH" -o json 2>/dev/null | jq -r '.[] | "\(.name)\t\(.version)\t\(.app_version)\t\(.description[0:50])"' | column -t | head -15
```

### Dependency Analysis

```bash
#!/bin/bash
CHART_PATH="${1:?Chart path required}"

echo "=== Chart Dependencies ==="
helm dependency list "$CHART_PATH" 2>/dev/null | head -20

echo ""
echo "=== Dependency Update ==="
helm dependency update "$CHART_PATH" 2>&1 | tail -10

echo ""
echo "=== Default Values (top-level keys) ==="
helm show values "$CHART_PATH" 2>/dev/null | grep -E "^[a-zA-Z]" | head -25
```

## Safety Rules
- **Dry-run first**: Always use `helm upgrade --dry-run` or `helm template` before applying
- **Never force-delete**: Avoid `helm uninstall` without explicit user confirmation
- **History preservation**: Keep release history for rollback (`--history-max` default is 10)
- **Values review**: Always review computed values with `helm get values` before upgrades

## Output Format

Present results as a structured report:
```
Managing Helm Report
════════════════════
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
- **Helm 2 vs 3**: Helm 3 has no Tiller -- ensure correct version context
- **Namespace mismatch**: Release is namespace-scoped -- always specify `-n` correctly
- **Values merge**: `--set` overrides file values -- order matters, last wins
- **CRD management**: Helm does not update CRDs on upgrade -- handle manually
- **Secret storage**: Default storage is Kubernetes secrets -- sensitive data may be exposed via `helm get values`
