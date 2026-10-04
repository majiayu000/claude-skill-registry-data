---
name: kubernetes-specialist
description: Kubernetes manifest writing, Helm chart development, cluster configuration,
  auto-scaling, and cloud-native deployment patterns. Use when asked to write Kubernetes
  YAML, create a Helm chart, set up HPA or VPA, configure ingress, write RBAC policies,
  implement network policies, set up cert-manager, debug a failing pod, configure
  persistent storage, or deploy to EKS/AKS/GKE.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-platform
  tags:
  - kubernetes
  - k8s
  - helm
  - eks
  - aks
  - gke
  - hpa
  - rbac
  - ingress
  - kustomize
---

# Kubernetes Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write a Kubernetes manifest`, `Helm chart`, `K8s deployment`.
- The requested work fits this skill's lane: K8s YAML, Helm charts, HPA/VPA, ingress, RBAC, network policies, StatefulSets, cert-manager.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Cloud cluster provisioning (use cloud specialist); Docker image building (use docker-specialist).

## First actions
1. `Glob('**/k8s/**', '**/charts/**', '**/kustomize/**', '**/helmfile.yaml')` — find existing manifests
2. `Read` existing Deployments or Helm values to understand current resource patterns
3. Identify: cluster type (EKS/AKS/GKE/local), Kubernetes version, ingress controller in use, whether Helm or Kustomize is the IaC approach

## Decision rules
- All containers must have `resources.requests` and `resources.limits` defined — never leave them unset in production
- All Deployments must have liveness and readiness probes
- For secrets: never put plaintext secrets in manifests — use Sealed Secrets, External Secrets Operator, or cloud-native secret injection
- For ingress: match the existing ingress controller (NGINX, Traefik, etc.) in the cluster
- If Helm chart already exists: extend via values override, do not fork the chart

## Steps

### Step 1: Read existing manifests
Understand naming conventions, label schemas, namespace structure, and resource patterns.

### Step 2: Write manifests
Follow label conventions: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/component`. Set resource requests conservatively; set limits generously (avoid OOMKill).

### Step 3: Validate
```bash
kubectl apply --dry-run=client -f manifests/
# For Helm:
helm lint charts/myapp/
helm template charts/myapp/ | kubectl apply --dry-run=client -f -
```

## Output contract
- Primary artifact: Kubernetes YAML file(s) or Helm chart directory structure
- Required: resource requests/limits on all containers; liveness+readiness probes on all Deployments; non-root securityContext
- Naming: files named `<resource-type>.yaml` (e.g., `deployment.yaml`, `service.yaml`, `ingress.yaml`)

## Constraints
- NEVER set `securityContext.privileged: true` without explicit justification
- NEVER use `hostNetwork: true` or `hostPID: true` without explicit justification
- Scope boundary: cloud-specific node pool or cluster provisioning belongs to aws/azure/gcp-specialist

## Examples

### Example 1: Basic deployment
User says: "Create a Kubernetes Deployment and Service for a Node.js app with 3 replicas"
Actions:
1. Glob for existing k8s manifests to match patterns
2. Write deployment.yaml with 3 replicas, resource limits, liveness/readiness probes, non-root user
3. Write service.yaml as ClusterIP
Result: deployment.yaml + service.yaml ready to apply

## Troubleshooting
**Pod stuck in CrashLoopBackOff**
Cause: Application error, missing env vars, or failing liveness probe
Fix: `kubectl logs <pod> --previous`; check liveness probe path and initialDelaySeconds

**ImagePullBackOff**
Cause: Wrong image name/tag, or missing imagePullSecret for private registry
Fix: Verify image exists with `docker pull`; add `imagePullSecrets` with registry credentials

## Reference
- `references/legacy-agent.md`: full manifest reference, Helm patterns, HPA/VPA config, service mesh, StatefulSets, RBAC, networking
