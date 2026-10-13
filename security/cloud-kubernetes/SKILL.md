---
name: cloud-kubernetes
description: >
  Attack exposed Kubernetes: API server, kubelet, etcd, dashboards, and RBAC. Load on k8s
  signals — ports 6443/10250/2379/8443, /api/v1, kube-dns, a pod foothold, or "kubernetes/k8s".
  Signals: kubectl, service-account tokens, exposed dashboard, container in a cluster.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-284]
mitre: [T1610, T1613]
tools: [kubectl, kube-hunter, peirates]
schema_version: 1
---

# Kubernetes attacks

## When it applies
A Kubernetes control-plane or node component is reachable (externally or from a pod foothold),
or you landed in a container inside a cluster and want to escalate to cluster admin / other tenants.

## Why it works
k8s exposes powerful HTTP APIs that are frequently unauthenticated or over-permissioned:
anonymous API access, kubelet read/exec on 10250, unauth etcd (all secrets), and mounted
service-account tokens with broad RBAC. One over-scoped token = cluster takeover.

## Method
1. **From outside**: `kube-hunter`; probe API server 6443 (`/api/v1` anonymous), kubelet 10250
   (`/pods`, `/run` exec), etcd 2379 (keys→secrets), and exposed dashboards (8443/anonymous).
2. **From a pod**: read the mounted token `/var/run/secrets/kubernetes.io/serviceaccount/`;
   `kubectl auth can-i --list` to see what it grants.
3. **Escalate via RBAC**: over-permissioned SA → create/exec pods, read secrets across namespaces,
   or `create pods` with a hostPath/privileged spec to mount the node (→ node/cluster takeover).
4. **Container→node breakout**: privileged pod, hostPID/hostNetwork, or a hostPath mount to the
   host filesystem (→ `cloud-container-escape`).
5. **Loot**: `kubectl get secrets -A`, cloud IAM via node metadata (→ `cloud-imds-ssrf`).

## Gotchas
- `kubectl auth can-i --list` first — it tells you exactly what the token can do; don't guess.
- Anonymous API/kubelet is common in labs and misconfigured clusters — always test unauth.
- On bug bounty, prove access read-only where possible; creating privileged pods is high-impact — mind RoE.

## Verify success
Cluster-level access proven: reading secrets across namespaces, exec into others' pods, or node
filesystem/cloud-creds access from an over-scoped token.

## References
kube-hunter/peirates; NCC "Kubernetes security"; MITRE ATT&CK Containers.
