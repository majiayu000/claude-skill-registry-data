---
name: code-review-iac
description: >
  Security review of infrastructure-as-code — Terraform, CloudFormation, Ansible, Kubernetes/Helm
  manifests. Load when reviewing IaC in a repo/PR, on .tf/.yaml/.yml infra files, or "review our
  Terraform". Signals: *.tf, cloudformation/*.yaml, playbooks, k8s manifests, Helm charts, module registries.
domain: code-review
type: reference
stability: learning
modes: [defense, pentest, bugbounty]
severity: info
cwe: [CWE-16, CWE-732, CWE-798]
tools: [checkov, tfsec, terrascan, kics, ripgrep]
schema_version: 1
---

# Infrastructure-as-code review

## When it applies
Reviewing the code that provisions cloud/infra. IaC misconfigurations become real, exploitable
exposure the moment they apply — a single line can make a bucket public or an SG world-open — so
this pairs directly with the offensive `cloud-*` skills.

## Why it works
IaC is declarative and repeatable: the same insecure default gets deployed everywhere it's
referenced. Scanning the definitions catches the exposure before it exists, and the patterns
(public access, `0.0.0.0/0`, plaintext secrets, missing encryption/logging) are consistent across
providers.

## Sinks & patterns (scan, then reason about blast radius)
- **Public exposure**: S3/GCS/Blob `acl = "public-read"` / public access blocks disabled; security
  groups / firewall rules `0.0.0.0/0` on 22/3389/DB ports; public RDS/ELB; `publiclyAccessible=true`.
- **Over-broad IAM**: `Action:"*"`/`Resource:"*"`, `iam:PassRole` wildcards, `AssumeRole` trust to
  `"*"`, admin-equivalent managed policies attached broadly.
- **Secrets in code**: hardcoded keys/passwords/tokens in `.tf`/vars/playbooks; secrets committed in
  state or plan output; `sensitive = false` on secret outputs.
- **Missing protections**: encryption at rest/in transit off (EBS/S3/RDS/SNS), logging/audit disabled
  (CloudTrail, flow logs, GCP audit), no MFA-delete/versioning, public snapshots/AMIs.
- **Kubernetes/Helm**: `privileged: true`, `hostNetwork/hostPID`, no `securityContext`/`runAsNonRoot`,
  wide RBAC (`cluster-admin`), secrets as env/plaintext, `latest` images, no network policies.
- **Ansible**: `shell`/`command` with unquoted vars, `no_log` missing on secret tasks, world-readable
  file modes, `validate_certs: no`.

## Method
1. Run `checkov`/`tfsec`/`kics` for a broad first pass; they cover hundreds of provider rules.
2. `rg '0.0.0.0/0|public|Action.*\*|password|secret|privileged: true'` and review each hit's context.
3. Trace module inputs/variables — an insecure default in a reused module multiplies everywhere.
4. Check state handling (remote, encrypted, access-controlled) and CI that applies it (`code-review-cicd`).

## Gotchas
- A finding's severity depends on blast radius — a public dev sandbox ≠ a public prod data store.
- Scanners miss cross-resource logic (an SG that's fine until paired with a public subnet) — reason about the whole graph.
- Secrets belong in a manager (Vault/SSM/KMS), never in variables or state — flag any inline secret.

## References
CIS Benchmarks (AWS/Azure/GCP/Kubernetes); Checkov/tfsec/KICS rule sets; provider well-architected security pillars.
