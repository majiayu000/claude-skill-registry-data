---
name: kit-kubernetes
description: Write, change, or review Kubernetes manifests, Helm charts, and Kustomize overlays with health probes, resource requests and limits, security contexts, disruption budgets, and pinned images, verified by rendering and offline or dry-run validation. Use when the user asks to add, change, fix, or review Kubernetes Deployments, Services, Ingresses, Jobs, ConfigMaps, Helm templates, or Kustomize overlays. Do not use for Terraform (use kit-terraform), for Dockerfiles (use kit-dockerfile), or to change a live cluster; this skill never runs kubectl apply, delete, or helm install.
---

# Kubernetes

Use rendering and offline validation only; never run a `kubectl` or `helm` command that changes a cluster (for example `apply`, `create`, `delete`, `edit`, `patch`, `replace`, `scale`, `set`, `label`, `rollout`, `cordon`, `drain`, `exec`, `helm install`, `upgrade`, `rollback`, or `uninstall`). Leave deploying to the user.

## 1. Learn the layout

Find how manifests are organized (plain YAML, Helm charts with values per environment, Kustomize bases and overlays), labels and naming conventions, namespaces, and existing policies (Pod Security admission level, network policies). Follow them.

## 2. Write or review

- **Images:** a specific tag or digest, never `latest`; `imagePullPolicy` consistent with that.
- **Health:** `readinessProbe` for traffic, `livenessProbe` only for real deadlock detection and with generous thresholds, `startupProbe` for slow starts.
- **Resources:** CPU and memory requests on every container, and a memory limit; avoid CPU limits that throttle unless the project uses them.
- **Security context:** `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem` where the app allows it, `capabilities: drop: ["ALL"]`, `automountServiceAccountToken: false` unless the pod calls the API, `seccompProfile: RuntimeDefault`, and no `hostPath`, `hostNetwork`, or privileged containers without a stated reason.
- **Availability:** more than one replica for services that need it, a `PodDisruptionBudget` (not `minAvailable: 1` on a single replica, which blocks node drains), topology spread or anti-affinity, and graceful shutdown (`terminationGracePeriodSeconds`, a `preStop` hook if needed).
- **Config and secrets:** configuration in ConfigMaps, credentials in Secrets or the project's secret manager integration, never in plain env values in Git. Service accounts with only needed RBAC permissions.
- Selectors must match pod labels; Service ports must match container ports.

## 3. Verify

Render with `helm template` or `kustomize build`, validate offline with `kubeconform` and the project's policy tools (`kube-linter`, `conftest`) when available. Use `--dry-run=server` only if the user confirms a non-production cluster context.

## 4. Report

Summarize the objects changed, security and availability choices, validation results, and how the user should roll it out.

## Examples

- Use: "Add a Deployment and Service for the worker." "Review this Helm chart." "Why does the pod keep restarting?" (from manifests)
- Skip: "Write the Dockerfile." (kit-dockerfile) "Delete the pods in production."
