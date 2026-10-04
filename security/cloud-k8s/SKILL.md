---
name: cloud-k8s
description: "Use for authorized cloud, container, and Kubernetes security assessment including metadata SSRF, IAM misconfig, container escape paths, and cluster RBAC review."
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: reverse-skill
  upstream: https://github.com/zhaoxuya520/reverse-skill
---

> Bundled with Unleash skills pack. Upstream: https://github.com/zhaoxuya520/reverse-skill

# Cloud / Container / Kubernetes Security

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-pentest.md` — **cloud/K8s testing requires written authorization**
2. `NOW`: case-init + scope; clarify account boundaries, no destructive operations allowed
3. `NOW`: confirm this is cloud metadata/container/K8s/IAM, not ordinary web scanning (for that, `pentest-tools/`)
4. `NEXT`: tool-index; kubectl/aws/gcloud etc. are mostly manual installs
5. `ACT`: start from "identity and exposure surface"; no default whole-network scanning

## Applicable Scenarios

- Cloud metadata SSRF (169.254.169.254 / IMDS)
- IAM excessive permissions, public storage buckets, wrong security groups
- Docker/containerd escape path assessment
- Kubernetes RBAC, Secrets, Admission, supply-chain images
- Container image vulnerabilities (can bring in `supply-chain-security/`)

## Workflow

### Phase 1 — Identity and Boundaries

```text
□ Current identity: cloud AK/SK, K8s SA, node SSH?
□ Scope: single account / single cluster / single namespace
□ Network profile: authorized_target_only
```

### Phase 2 — Cloud Control Plane

```bash
# Examples (substitute per vendor; MUST stay within the authorized account)
aws sts get-caller-identity
aws s3 ls
# Azure / GCP equivalent identity commands
```

```text
□ Public buckets / wrong ACLs
□ Metadata: IMDSv1 vs v2; SSRF chains
□ Roles that can be assumed (PassRole) and lateral movement
```

### Phase 3 — Containers

```text
□ Privileged / hostPath / hostNetwork?
□ Capabilities (SYS_ADMIN etc.)
□ Writable host paths → escape candidates
□ Image history and known CVEs → Trivy
```

### Phase 4 — Kubernetes

```bash
kubectl auth can-i --list
kubectl get pods,secrets,svc -A
kubectl get clusterrolebindings
```

```text
□ SA token mounts and permissions
□ Missing dangerous-admission webhooks
□ etcd / dashboard exposure
□ Whether network policies default to allow
```

## Toolchain

| Tool | Purpose | Bootstrap |
|------|------|------|
| kubectl | Cluster interaction | Manual |
| trivy | Image/IaC | bootstrap `trivy` if available |
| kube-bench / kubeaudit | CIS/config | Manual |
| pacu / scoutsuite | Cloud auditing (authorized) | Manual |
| nuclei | Known cloud vulnerability templates | bootstrap nmap/nuclei ecosystem |

## References

- `references/k8s-cloud-checklist.md`
- CTF counterpart: `../../CTF-Sandbox-Orchestrator/competition-agent-cloud/`
- `../supply-chain-security/` `../pentest-tools/`

## Routing Context

**Upstream**: MASTER R23  
**Downstream**: node shell obtained → `attack-chain` / `windows-ad`; image vulnerabilities → supply-chain  
**MUST NOT**: scan other tenants of a public cloud without authorization

## Task Completion Self-Check

- [ ] Confined to the authorized account/cluster?
- [ ] Findings include reproduction and impact?
- [ ] Destructive operations avoided?
- [ ] Report / journal?
