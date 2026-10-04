---
name: helm-chart-quality-review
description: Use this skill when a user provides a Helm chart or asks to review Helm chart quality, security, or testability — including Chart.yaml, values.yaml, templates/, tests/, or chart-testing CI configuration.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-17"
  category: delivery
  lifecycle: experimental
---

# Helm Chart Quality Review

## Purpose
This skill reviews Helm chart source for quality, security, and testability defects. It reads chart files statically — Chart.yaml, values.yaml, values.schema.json, templates/, tests/, and CI configuration — without installing the chart or contacting a Kubernetes cluster. The review surfaces defects that allow bad workloads to be deployed silently: insecure container security contexts, missing resource governance, absent health probes, RBAC over-permission, hardcoded or default credentials, and missing helm test coverage.

## Lean operating rules
- Treat `privileged: true`, `capabilities.add: [ALL]` or any combination that grants root-equivalent privileges as CRITICAL — stop and flag before continuing.
- Treat `hostNetwork: true`, `hostPID: true`, or `hostIPC: true` as CRITICAL — these give a container visibility into the node's network stack, process table, or IPC namespace.
- Treat secrets rendered inline in a ConfigMap (not a Secret resource) as CRITICAL — plain-text secrets are visible to any workload that can read ConfigMaps in the namespace.
- Treat a `ClusterRoleBinding` to the `default` service account as CRITICAL — any workload in the namespace inherits cluster-scoped access.
- Treat `capabilities.add: [SYS_ADMIN]` or `[NET_ADMIN]` as CRITICAL — these grant near-root kernel capabilities.
- Treat hardcoded `:latest` image tags without override capability as HIGH — breaks reproducibility and makes rollback unreliable.
- Treat `securityContext.runAsRoot: true` or the absence of `runAsNonRoot` on pod or container spec as HIGH — workloads should not run as UID 0.
- Treat `allowPrivilegeEscalation` not explicitly set to `false` as HIGH — a child process can gain more privileges than the parent.
- Treat cluster-scoped RBAC roles where namespace-scoped would suffice as HIGH — blast radius of a compromise is the entire cluster.
- Treat `serviceAccount.automountServiceAccountToken` not set to `false` when the workload does not call the Kubernetes API as HIGH — the token is mounted unnecessarily and exploitable.
- Treat missing `resources.requests` and `resources.limits` on every container as HIGH — without limits, a misbehaving pod can trigger node over-subscription and OOM kills on neighbours.
- Treat missing `livenessProbe` or `readinessProbe` as HIGH — rolling updates proceed blind; a pod stuck in a failed state can be sent live traffic.
- Treat sensitive default credential values (`admin`, `password`, empty string) in values.yaml as CRITICAL — users forget to override defaults and ship them to production.
- Treat the absence of `values.schema.json` when required values carry no type or pattern constraint as MEDIUM — `helm install` accepts arbitrary input with no validation.
- Treat missing `readOnlyRootFilesystem: true` as MEDIUM — a container with a writable root filesystem can modify its own binaries or drop exploit payloads.
- Treat missing `startupProbe` for slow-starting containers as MEDIUM — liveness checks kill containers that need more startup time, causing crash loops.
- Treat no `PodDisruptionBudget` for stateful or singleton workloads as MEDIUM — node drains can take the workload to zero replicas.
- Treat no `HorizontalPodAutoscaler` where the workload is expected to scale as LOW.
- Treat probe timeouts or failure thresholds at defaults with no tuning rationale as LOW.
- Treat no `NOTES.txt` as LOW — users have no post-install guidance.
- Treat a chart version that is not semver-compliant as LOW.
- Treat `tests/` that contain only pod-existence checks and no service reachability or functional assertion as LOW — existence proves the pod started, not that the service works.
- Treat no `tests/` directory at all as MEDIUM — helm test integration is absent.
- Treat no CI integration for chart-testing (`ct lint-and-install` or equivalent) as MEDIUM — the chart is not regression-tested on install.
- Label every finding with its evidence basis: `chart source provided`, `values only`, `documentation-based`, or `inference`.
- Do not request kubeconfig, cluster credentials, cloud provider credentials, or live values files containing secrets. Ask for sanitized versions with placeholder values.
- Static review only — never install a chart, never contact a Kubernetes cluster, never run `helm upgrade` or `kubectl apply`.

## References
Load these only when needed:
- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review or formatting the final answer.

## Response minimum
Return, at minimum:
- Linting and template correctness findings
- Values hygiene findings (sensitive defaults, schema validation, `:latest` tags)
- Template security findings (securityContext, capabilities, host namespaces, secrets in ConfigMap)
- Resource governance findings (requests/limits, PDB, HPA)
- Health and observability findings (liveness, readiness, startup probes)
- Testability findings (helm test, chart-testing CI)
- RBAC and service account findings
- Severity-labelled finding list (CRITICAL / HIGH / MEDIUM / LOW)
- Safe next actions
