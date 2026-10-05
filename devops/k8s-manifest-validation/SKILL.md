---
name: k8s-manifest-validation
description: This skill should be used when the user mentions "kubernetes manifest", "k8s yaml", "deployment not ready", "pod crashloop", "resource limits", "liveness readiness probe", "securityContext", or "helm values", or is validating manifests before deploy. It provides the silent failure modes of K8s manifests plus a PASS/WARN/FAIL validation checklist.
---

# Kubernetes Manifest Validation

## Purpose
A consistent pre-deploy checklist for the Kubernetes manifest mistakes that pass `kubectl apply` but never become Ready, silent failures. This is K8s-specific domain knowledge about how manifests fail quietly, not generic YAML linting.

## The silent-failure principle
`kubectl apply` validates schema, not intent. A manifest can apply cleanly and then: never pass readiness, get OOMKilled, run as root against policy, or route traffic to a dead Pod. Static pre-flight catches these before they reach the cluster.

## Validation checklist (assign PASS / WARN / FAIL)

| Check | FAIL condition | Why it fails silently |
|-------|----------------|-----------------------|
| Type / quoting | `containerPort: "8080"` (string), `"true"` bool, int env value | schema accepts strings; port never binds / value mis-typed |
| Resource requests & limits | missing on a container | BestEffort QoS → first evicted; can starve the node |
| Readiness probe | missing | traffic routed before the app can serve → 502s |
| Liveness probe | missing (WARN) or too aggressive (FAIL) | wedged Pod never restarts; or healthy Pod killed in a loop |
| Startup probe | missing on slow-starting app | liveness kills it before it finishes booting |
| securityContext | `runAsNonRoot` unset, caps not dropped, writable rootfs | runs as root; policy admission may reject later |
| Image tag | `:latest` or untagged | non-reproducible; rollout pulls a different image silently |
| Replicas / PDB | single replica, no PodDisruptionBudget | node drain / rollout causes full downtime |
| Hardcoded secrets | literal token/password in env or ConfigMap | secret committed to git; ConfigMaps aren't secret |
| Namespace | relies on implicit `default` | deploys to the wrong place; RBAC/quota surprises |

## Type-quoting quick rules
- `containerPort`, `port`, `targetPort` (numeric), `replicas` → **integers**, unquoted.
- Boolean fields (`runAsNonRoot`, `readOnlyRootFilesystem`) → **bare** `true`/`false`, never `"true"`.
- Env `value:` is **always a string**: wrap numbers/bools in quotes: `value: "5432"`.
- YAML gotcha: unquoted `on`, `off`, `yes`, `no`, and `1.20` get coerced, quote version strings.

## Gate verdict
Report per-check PASS/WARN/FAIL, then an overall line: `GATE: PASS` only with zero FAILs, else `GATE: FAIL`.

## Additional Resources
### Reference Files
For per-kind mistakes and how each fails silently, consult:
- **`references/manifest-checklist.md`**: Deployment, Service, Ingress, ConfigMap, Secret, and HPA common mistakes, each with the symptom, the silent failure, and the fix.

For probe and resource semantics in depth, consult:
- **`references/probes-and-resources.md`**: liveness vs readiness vs startup probe semantics and tuning, requests/limits and the Guaranteed/Burstable/BestEffort QoS classes, and the securityContext hardening fields.
