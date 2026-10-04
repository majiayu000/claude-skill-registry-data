---
name: managing-flux
description: |
  Use when working with Flux — flux CD GitOps management for Kubernetes. Covers
  source reconciliation, Kustomization status, HelmRelease management, image
  automation, notification configuration, and drift detection. Use when checking
  GitOps sync status, investigating reconciliation failures, managing Flux
  sources, or auditing Kustomization health.
connection_type: flux
preload: false
---

# Flux CD Management Skill

Manage and monitor Flux CD GitOps reconciliation, sources, and Kustomizations on Kubernetes.

## Core Helper Functions

```bash
#!/bin/bash

# Flux CLI wrapper
flux_cmd() {
    flux "$@" --namespace "${FLUX_NAMESPACE:-flux-system}" 2>/dev/null
}

# kubectl wrapper for Flux CRDs
flux_k8s() {
    kubectl "$@" -n "${FLUX_NAMESPACE:-flux-system}" 2>/dev/null
}

# Get Flux status across all resource types
flux_status() {
    flux_cmd get all 2>/dev/null || {
        echo "=== Sources ==="
        flux_k8s get gitrepositories,helmrepositories,ocirepositories,buckets 2>/dev/null
        echo "=== Kustomizations ==="
        flux_k8s get kustomizations 2>/dev/null
        echo "=== HelmReleases ==="
        flux_k8s get helmreleases -A 2>/dev/null
    }
}
```

## MANDATORY: Discovery-First Pattern

**Always discover all Flux resources before querying specific reconciliation status.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Flux Version & Components ==="
flux_cmd version 2>/dev/null || \
    flux_k8s get deployments -l app.kubernetes.io/part-of=flux -o custom-columns="NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image" 2>/dev/null

echo ""
echo "=== Flux Resources Overview ==="
flux_cmd get all -A 2>/dev/null | head -30 || {
    echo "--- GitRepositories ---"
    flux_k8s get gitrepositories -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[0].status,STATUS:.status.conditions[0].message" 2>/dev/null | head -10
    echo "--- Kustomizations ---"
    flux_k8s get kustomizations -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[0].status,STATUS:.status.conditions[0].message" 2>/dev/null | head -10
    echo "--- HelmReleases ---"
    flux_k8s get helmreleases -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[0].status,STATUS:.status.conditions[0].message" 2>/dev/null | head -10
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `flux get` for human-friendly output, `kubectl -o json | jq` for structured queries
- Truncate long status messages — Flux messages can be verbose

## Common Operations

### GitOps Reconciliation Status

```bash
#!/bin/bash
echo "=== Source Reconciliation ==="
flux_k8s get gitrepositories -A -o json | jq -r '
    .items[] |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[0].status)\trevision=\(.status.artifact.revision[0:12] // "none")\tlastAttempt=\(.status.conditions[0].lastTransitionTime[0:16])"
' | column -t

echo ""
echo "=== Kustomization Reconciliation ==="
kubectl get kustomizations.kustomize.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[] |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[0].status)\treason=\(.status.conditions[0].reason)\tlastApplied=\(.status.lastAppliedRevision[0:12] // "none")"
' | column -t

echo ""
echo "=== Failed Reconciliations ==="
kubectl get kustomizations.kustomize.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[] | select(.status.conditions[0].status == "False") |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[0].message[0:80])"
' | column -t
```

### Source Management

```bash
#!/bin/bash
echo "=== Git Repositories ==="
flux_k8s get gitrepositories -A -o json | jq -r '
    .items[] | "\(.metadata.namespace)/\(.metadata.name)\turl=\(.spec.url)\tbranch=\(.spec.ref.branch // .spec.ref.tag // "default")\tinterval=\(.spec.interval)"
' | column -t

echo ""
echo "=== Helm Repositories ==="
flux_k8s get helmrepositories -A -o json | jq -r '
    .items[] | "\(.metadata.namespace)/\(.metadata.name)\ttype=\(.spec.type // "default")\turl=\(.spec.url)\tinterval=\(.spec.interval)"
' | column -t

echo ""
echo "=== OCI Repositories ==="
flux_k8s get ocirepositories -A -o json 2>/dev/null | jq -r '
    .items[]? | "\(.metadata.namespace)/\(.metadata.name)\turl=\(.spec.url)\tinterval=\(.spec.interval)"
' | column -t

echo ""
echo "=== Source Errors ==="
flux_k8s get gitrepositories,helmrepositories -A -o json | jq -r '
    .items[] | select(.status.conditions[0].status == "False") |
    "\(.kind)/\(.metadata.name)\t\(.status.conditions[0].message[0:80])"
' | column -t
```

### Kustomization Details

```bash
#!/bin/bash
KUSTOMIZATION="${1:?Kustomization name required}"
NS="${2:-flux-system}"

echo "=== Kustomization Config ==="
kubectl get kustomization.kustomize.toolkit.fluxcd.io "$KUSTOMIZATION" -n "$NS" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    namespace: .metadata.namespace,
    source: "\(.spec.sourceRef.kind)/\(.spec.sourceRef.name)",
    path: .spec.path,
    interval: .spec.interval,
    prune: .spec.prune,
    targetNamespace: .spec.targetNamespace,
    healthChecks: [.spec.healthChecks[]? | "\(.kind)/\(.name)"],
    lastAppliedRevision: .status.lastAppliedRevision,
    lastAttemptedRevision: .status.lastAttemptedRevision,
    ready: .status.conditions[0].status,
    message: .status.conditions[0].message
}'

echo ""
echo "=== Inventory (managed resources) ==="
kubectl get kustomization.kustomize.toolkit.fluxcd.io "$KUSTOMIZATION" -n "$NS" -o json 2>/dev/null | jq -r '
    .status.inventory.entries[]? |
    "\(.id)"
' | head -20
```

### HelmRelease Management

```bash
#!/bin/bash
echo "=== Helm Releases ==="
kubectl get helmreleases.helm.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[] |
    "\(.metadata.namespace)/\(.metadata.name)\tchart=\(.spec.chart.spec.chart)@\(.spec.chart.spec.version // "latest")\tinterval=\(.spec.interval)\tready=\(.status.conditions[0].status)"
' | column -t

echo ""
echo "=== Failed HelmReleases ==="
kubectl get helmreleases.helm.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[] | select(.status.conditions[0].status == "False") |
    "\(.metadata.namespace)/\(.metadata.name)\treason=\(.status.conditions[0].reason)\tmessage=\(.status.conditions[0].message[0:80])"
' | column -t

echo ""
echo "=== HelmRelease History ==="
HR_NAME="${1:-}"
HR_NS="${2:-default}"
if [ -n "$HR_NAME" ]; then
    kubectl get helmrelease.helm.toolkit.fluxcd.io "$HR_NAME" -n "$HR_NS" -o json 2>/dev/null | jq '{
        name: .metadata.name,
        chart: .spec.chart.spec.chart,
        version: .spec.chart.spec.version,
        values_from: [.spec.valuesFrom[]? | "\(.kind)/\(.name)"],
        last_release_revision: .status.lastReleaseRevision,
        history: [.status.history[]? | {version: .chartVersion, status, digest: .digest[0:12]}]
    }'
fi
```

### Image Automation

```bash
#!/bin/bash
echo "=== Image Repositories ==="
kubectl get imagerepositories.image.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[]? |
    "\(.metadata.namespace)/\(.metadata.name)\timage=\(.spec.image)\tcanonical=\(.status.canonicalImageName // "unknown")\ttags=\(.status.lastScanResult.tagCount // 0)"
' | column -t

echo ""
echo "=== Image Policies ==="
kubectl get imagepolicies.image.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[]? |
    "\(.metadata.namespace)/\(.metadata.name)\tlatest=\(.status.latestImage // "none")\tpolicy=\(.spec.policy | keys[0])"
' | column -t

echo ""
echo "=== Image Update Automations ==="
kubectl get imageupdateautomations.image.toolkit.fluxcd.io -A -o json 2>/dev/null | jq -r '
    .items[]? |
    "\(.metadata.namespace)/\(.metadata.name)\tlastRun=\(.status.lastAutomationRunTime[0:16] // "never")\tlastCommit=\(.status.lastPushCommit[0:12] // "none")"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess Kustomization or source names — always list first
- NEVER fabricate revision hashes — query source status for actual revisions
- NEVER assume namespace — Flux resources can exist in any namespace
- CRD group names are long (e.g., `kustomizations.kustomize.toolkit.fluxcd.io`) — use correct full names with kubectl

## Safety Rules
- NEVER suspend Flux reconciliation without explicit user confirmation
- NEVER delete sources or Kustomizations without understanding dependencies
- NEVER force reconciliation in production without user approval
- Prune-enabled Kustomizations will DELETE resources removed from Git — flag when `prune: true`

## Output Format

Present results as a structured report:
```
Managing Flux Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **CRD naming**: Flux Kustomization CRD is `kustomizations.kustomize.toolkit.fluxcd.io`, not `kustomizations` (conflicts with kustomize.config.k8s.io)
- **Reconciliation interval**: Short intervals increase Git API calls — check rate limits
- **Suspend vs delete**: Suspending stops reconciliation; deleting removes the resource but NOT managed workloads (unless prune is on)
- **Dependency ordering**: Kustomizations can depend on each other — check `dependsOn` field for ordering issues
- **Health checks**: Kustomizations with `healthChecks` block until resources are healthy — long deployments may timeout
- **Secret decryption**: SOPS/age-encrypted secrets need decryption keys — check Flux secret for decryption key
- **Multi-tenancy**: Flux supports multi-tenancy — `ServiceAccount` impersonation controls permissions per tenant
