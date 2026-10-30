---
name: cloud-k8s
description: Use for authorized cloud, container, and Kubernetes security assessment including metadata SSRF, IAM misconfig, container escape paths, and cluster RBAC review.
---

# Cloud / Container / Kubernetes Security

## Authorization preamble

1. Cloud and K8s testing requires **written authorization** — confirm it before anything else.
2. Confirm the task is in scope: account boundaries defined, destructive operations prohibited.
3. Confirm the target is actually cloud metadata / containers / K8s / IAM, not a plain web app (plain web → `pentest-tools/`).
4. Tools: kubectl / aws / gcloud are usually installed manually — verify before use.
5. Start from "identity and exposure"; **no default full-network scanning**.

## Scope

- Cloud metadata SSRF (169.254.169.254 / IMDS)
- Over-privileged IAM, public storage buckets, wrong security groups
- Docker/containerd escape path assessment
- Kubernetes RBAC, Secrets, Admission, image supply chain
- Container image vulnerabilities (pairs with `supply-chain-security/`)

## Workflow

### Phase 1 — Identity and boundaries

```text
□ Current identity: cloud AK/SK, K8s SA, node SSH?
□ Scope: single account / single cluster / single namespace
□ Network profile: authorized_target_only
```

### Phase 2 — Cloud control plane

```bash
# Examples (per provider; MUST stay inside authorized accounts)
aws sts get-caller-identity
aws s3 ls
# Azure / GCP have equivalent identity commands
```

```text
□ Public buckets / wrong ACLs
□ Metadata: IMDSv1 vs v2; SSRF chains
□ Role assumption (PassRole) and lateral movement
```

### Phase 3 — Containers

```text
□ privileged / hostPath / hostNetwork?
□ capabilities (SYS_ADMIN etc.)
□ writable host paths → escape candidates
□ image history and known CVEs → Trivy
```

### Phase 4 — Kubernetes

```bash
kubectl auth can-i --list
kubectl get pods,secrets,svc -A
kubectl get clusterrolebindings
```

```text
□ SA token mounts and permissions
□ Missing dangerous admission webhooks
□ etcd / dashboard exposure
□ Do network policies default to allow?
```

## Toolchain

| Tool | Purpose | Bootstrap |
|------|---------|-----------|
| kubectl | cluster interaction | manual |
| trivy | images / IaC | bootstrap `trivy` if available |
| kube-bench / kubeaudit | CIS / config | manual |
| pacu / scoutsuite | cloud audit (authorized) | manual |
| nuclei | known cloud vuln templates | bootstrap nmap/nuclei ecosystem |

## References

- `references/k8s-cloud-checklist.md`
- CTF crosswalk: `../../CTF-Sandbox-Orchestrator/competition-agent-cloud/`
- `security/parts/supply-chain-security/` `security/parts/pentest-tools/`

## MUST NOT

- Scan other tenants of a public cloud without authorization.

## Completion self-check

- [ ] Did I stay within the authorized account/cluster?
- [ ] Do findings include reproduction and impact?
- [ ] Did I avoid destructive operations?
- [ ] Report / journal written?
