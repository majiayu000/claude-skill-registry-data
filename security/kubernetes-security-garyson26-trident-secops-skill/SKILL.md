---
name: kubernetes-security
description: Kubernetes and container security skill for cluster hardening, RBAC review, admission control (OPA Gatekeeper, Kyverno), Pod Security Standards, network policies, secrets management, runtime defense (Falco, Tetragon), image supply chain (cosign, SLSA, in-toto), and CIS benchmark compliance. Use to assess and harden clusters you operate.
---

# Kubernetes Security

## Authorization Boundary

- Require cluster context, namespace scope, and read-only kubeconfig before live queries.
- Avoid disruptive runtime probes on production; prefer staging or ephemeral clusters.

## Hardening Workflow

1. Inventory: API server flags, node OS, CNI, CSI, ingress, service mesh, admission plugins, controllers.
2. Scan: `kube-bench`, `kubescape`, `trivy k8s`, `polaris`, `kubeaudit`, `popeye`.
3. RBAC: enumerate `ClusterRole`/`RoleBinding`; flag wildcard verbs, `system:masters`, `escalate`, `bind`, `impersonate`, secret reads from broad subjects.
4. Workloads: enforce Pod Security `restricted`, drop capabilities, read-only rootfs, non-root UID, seccomp `RuntimeDefault`, no `hostPath`/`hostNetwork`/`hostPID`.
5. Network: default-deny `NetworkPolicy`; explicit egress to known services; mTLS via mesh where applicable.
6. Supply chain: signed images (`cosign verify`), provenance attestations (SLSA), admission policy that blocks unsigned.
7. Runtime: Falco/Tetragon rules for exec-in-container, reverse shells, crypto miners, sensitive mounts.

## Multi-Tenant Patterns

- Namespace-per-tenant with quotas, limit ranges, and `NetworkPolicy` isolation.
- Separate node pools for untrusted workloads; gVisor or Kata for sandboxing.
- Per-tenant audit log filters; secrets via external KMS, never inline.

## Output Contract

- `inventory.yaml`, `findings.csv`, `policies/` (Gatekeeper/Kyverno), `netpol/`, `runtime/falco-rules.yaml`.
- `runbook.md`: incident response for compromised pod, leaked token, miner detection.
- `gap.md`: missing telemetry and proposed fixes.
