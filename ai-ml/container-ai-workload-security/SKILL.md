---
name: container-ai-workload-security
description: Review Docker and Kubernetes configurations for AI workloads — covering privileged container risks for GPU access, model weight volume security, network policy gaps between inference pods, image provenance for ML base images, and secrets management in pod specs.
last_reviewed: 2026-04-29
---

# Container AI Workload Security

## First Principle

**AI workloads run with configurations that standard container security tooling flags as dangerous — and engineers accept the warnings because "the model needs GPU access." GPU access does not require privileged mode. Most privileged AI containers are over-privileged by habit, not necessity.**

Containerizing AI workloads introduces standard container security concerns (privileged mode, secrets in env vars, missing resource limits) alongside AI-specific concerns (large model weight volumes accessible from multiple pods, ML base images with broad package sets, GPU device access patterns). The intersection creates configurations that are neither well-understood by container security engineers nor by ML engineers.

## Attack Mental Model

1. **Privileged container breakout** — a container running with `--privileged` or `CAP_SYS_ADMIN` that achieves code execution (via prompt injection → tool use) can escape the container and access the host filesystem, other containers, and GPU devices.
2. **Model weight volume access** — model weights mounted as shared volumes are accessible from any pod with access to the volume. A compromised pod can exfiltrate or tamper with model weights.
3. **Secrets in pod specs** — API keys and model registry credentials stored in pod environment variables are accessible to anyone with `kubectl describe pod` access in the namespace.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Container images are built from a pinned, scanned base image. No ML base images with `latest` tags are used in production. |
| **Scope** | GPU access is granted via device plugin (`nvidia.com/gpu: 1` resource limit) — not via `--privileged` or `--device /dev/nvidia0`. Privileged mode is never used for GPU inference. |
| **Isolate** | Model weight volumes are mounted read-only in inference pods. Write access is restricted to the model loading job. Network policies prevent direct pod-to-pod communication between inference and data processing workloads. |
| **Enforce** | Kubernetes secrets are the floor, not the ceiling. Production secrets are managed via a secrets manager (Vault, AWS Secrets Manager) with a sidecar injector — not stored in Kubernetes secret objects. |

## CAW.1 Container Privilege Reduction and GPU Access

**The core vulnerability:** ML practitioners often run containers with `--privileged` because they encountered a GPU access error and adding privilege fixed it. Privileged containers have full access to all host devices and most host capabilities. A prompt injection that achieves code execution inside a privileged inference container has effectively escaped to the host.

### Check

- Do any inference or training containers run with `--privileged: true` or `allowPrivilegeEscalation: true` in their pod security context?
- Is GPU access configured via the NVIDIA device plugin resource request — or via direct device mounts (`/dev/nvidia*`) in the pod spec?
- Is the pod's security context configured with `readOnlyRootFilesystem: true` and `runAsNonRoot: true`?

### Action

- **Use the NVIDIA device plugin for GPU access — not privileged mode.** Configure the NVIDIA GPU Operator and request GPU resources properly:

```yaml
# Correct GPU access — no privilege escalation
resources:
  limits:
    nvidia.com/gpu: 1
securityContext:
  privileged: false
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop: ["ALL"]
```

- **Audit every AI workload pod spec for privileged: true.** Run: `kubectl get pods -A -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged == true) | .metadata'`. Each result requires justification or remediation.
- **Apply a PodSecurity admission policy.** In Kubernetes 1.25+, configure namespace-level Pod Security Standards to `restricted` for inference namespaces. This blocks privileged containers at the admission layer.

### Failure Modes

- An inference pod runs privileged to "fix a CUDA error." The real fix was a missing device plugin configuration. The privileged container remains in production after the error is gone.
- A base image runs as root. An attacker who achieves code execution inside the container has root access to the container filesystem and any mounted volumes.

## CAW.2 Secrets Management and Model Weight Volume Security

**The core vulnerability:** AI workloads require secrets (model registry credentials, API keys, database passwords). These are frequently stored in Kubernetes Secret objects referenced as environment variables in pod specs. Kubernetes secrets encoded in base64 are accessible to anyone with namespace-level read access — which is far broader than intended in most clusters.

### Check

- Are API keys and model registry credentials stored in Kubernetes Secret objects — or in a dedicated secrets manager with dynamic, short-lived credentials?
- Are model weight volumes mounted read-only in inference pods — or do inference pods have write access to the volume?
- Are container images pinned by digest (`image@sha256:...`) rather than by tag (`image:latest`) — preventing tag reassignment attacks?

### Action

- **Replace Kubernetes Secret environment variables with a secrets manager sidecar.** Use Vault Agent or AWS Secrets Manager CSI driver to inject secrets as files, not environment variables. Secrets as files are less accessible to environment variable enumeration:

```yaml
# Vault Agent sidecar pattern
initContainers:
- name: vault-agent
  image: vault:1.15@sha256:...
  args: ["agent", "-config=/vault/config/agent.hcl"]
  volumeMounts:
  - name: secrets
    mountPath: /vault/secrets
containers:
- name: inference
  env: []  # no env var secrets
  volumeMounts:
  - name: secrets
    mountPath: /secrets
    readOnly: true
```

- **Mount model weight volumes read-only in inference pods:**

```yaml
volumeMounts:
- name: model-weights
  mountPath: /models
  readOnly: true
```

- **Pin all image references by SHA-256 digest.** Replace `image: pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime` with `image: pytorch/pytorch@sha256:abc123...`. The digest is immutable; a tag can be reassigned to point to a different image.

### Minimum Deliverable Per Review

- [ ] Privilege audit: zero pods with `privileged: true` in inference/training namespaces, or documented exceptions with compensating controls
- [ ] Security context: `readOnlyRootFilesystem`, `runAsNonRoot`, `allowPrivilegeEscalation: false` on all AI workload pods
- [ ] GPU access: NVIDIA device plugin used, no direct `/dev/nvidia*` device mounts
- [ ] Secrets management: Kubernetes secrets replaced or supplemented with sidecar secrets manager for production credentials
- [ ] Model weight volumes: read-only mount in inference pods
- [ ] Image pinning: all production images referenced by SHA-256 digest

## Quick Win

**Run the privileged container audit right now:** `kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name)"'`. Any pod that prints is a container escape risk if code execution is achieved inside it.

## References

- GPU hardware security → [gpu-infrastructure-security/SKILL.md](../gpu-infrastructure-security/SKILL.md)
- MLOps pipeline security → [mlops-pipeline-security/SKILL.md](../mlops-pipeline-security/SKILL.md)
- Secrets in prompts → [secrets-in-prompts-detection/SKILL.md](../secrets-in-prompts-detection/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
