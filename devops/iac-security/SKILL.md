---
id: iac-security
version: "2.0.0"
title: "Infrastructure-as-Code Security"
description: "Terraform, CloudFormation, and Pulumi hardening: state as a secret store, pinned providers and modules, encryption and network defaults, drift, and the privilege of the pipeline that applies the plan. Use when generating infrastructure code, reviewing IaC changes in a pull request, configuring a state backend, or setting up a new cloud account or workspace."
category: hardening
severity: high
applies_to:
  - "when generating Terraform / Pulumi / CloudFormation"
  - "when configuring a state backend or a CI apply pipeline"
  - "when adding a third-party module or provider"
  - "when reviewing IaC changes in a pull request"
languages: ["hcl", "yaml", "json", "typescript", "python", "go"]
token_budget:
  minimal: 1200
  compact: 1500
  full: 2100
rules_path: "checklists/"
related_skills: ["iam-best-practices", "secret-detection", "container-security", "cicd-security"]
last_updated: "2026-08-12"
sources:
  - "CIS Benchmarks (AWS, Azure, GCP)"
  - "HashiCorp Terraform recommended practices"
  - "NIST SP 800-53 Rev. 5 (CM-6, CM-8, SC-28)"
  - "OWASP IaC Security Top 10"
external_tools:
  - name: checkov
    purpose: "IaC misconfiguration scan (Terraform/CloudFormation/Kubernetes/Helm)"
    command: "checkov -d ."
  - name: trivy
    purpose: "IaC config misconfiguration scan"
    command: "trivy config ."
---

# Infrastructure-as-Code Security

## Rules (for AI agents)

### ALWAYS
- Treat the **state file as a secret store**. Every value that passes through
  Terraform — a generated password, an RDS master credential, a private key, the
  contents of a data source — is written to state in plaintext. `sensitive = true`
  only hides a value from CLI output; it changes nothing about what is stored. So
  read access to the backend is read access to those secrets, and the backend's
  access policy has to be written on that basis.
- Configure a **remote backend** with encryption at rest, state locking, and
  versioning. Prefer the backend's own locking where it exists — recent Terraform
  supports S3-native locking, so a separate DynamoDB lock table is no longer required
  for new stacks. `references/backends-and-state.md` has the per-backend form.
- Pin providers and modules to an exact version or a pessimistic constraint
  (`~> 5.42`), and pin a third-party module sourced from a git URL to a **commit SHA**,
  not a branch or tag. A module is code that runs with your apply credentials, and a
  registry or repository you do not control is a supply-chain input like any other.
- Give the **apply identity** the least privilege that the stack actually needs, and
  keep it separate from the plan identity. A pipeline role with account-wide admin
  turns any CI compromise into a full account compromise — `cicd-security` owns
  hardening the pipeline itself, `iam-best-practices` owns the role's shape.
- Encrypt persistent resources by default with a customer-managed key: object
  storage, block storage, managed databases, queues, log groups. Prefer a module or
  default that applies it, so a new resource is encrypted because of how the code is
  organised rather than because someone remembered.
- Deny inbound by default and open ports deliberately. Administrative and database
  ports reachable from `0.0.0.0/0` are the finding — SSH, RDP, and the managed
  database ports especially — and "it is only dev" does not change the exposure.
  `references/backends-and-state.md` lists the ports worth failing a build over.
- Run `plan` (or `pulumi preview`, a CloudFormation change set) in CI, require human
  approval before applying to production, and run scheduled **drift detection** that
  raises an issue when the cloud diverges from the code. Drift is where a break-glass
  change made at 3am quietly becomes the permanent configuration.
- Scope roles and resource policies with the provider's own condition mechanism —
  source account, source ARN, organization ID, TLS-only access on storage.
  `iam-best-practices` owns policy design; what belongs here is that the condition is
  expressed in the code rather than clicked into the console.

### NEVER
- Hardcode provider credentials in code or `.tfvars` (`access_key`, `secret_key`,
  `client_secret`, `service_account_key`). Use OIDC federation from CI, the platform's
  workload identity, or a secret manager.
- Commit `terraform.tfstate`, `terraform.tfstate.backup`, `.pulumi/`, or a `.tfvars`
  holding real values — see the state rule above for why the file is a credential
  dump even when the code only references variables.
- Use `local-exec` / `null_resource` to fetch a secret at apply time. It lands in
  state, and the provisioner runs on whatever machine ran `apply`, with that machine's
  identity.
- Disable provider TLS verification (`skip_tls_verify`, `insecure = true`).

### KNOWN FALSE POSITIVES
- A bastion deliberately reachable on SSH is not the same finding as a database open
  to the world — but "bastion" is not the exemption, its configuration is: key-only
  authentication, MFA, and a narrow source range. A session-manager or
  identity-aware-proxy path that removes the public port entirely is better than
  hardening one.
- Resources that are meant to be internet-facing: CDN distributions, load-balancer
  listeners on 80/443, API gateways, function URLs.
- Backend bootstrap resources — the bucket and lock mechanism the backend itself
  uses — cannot live in the state they provide. A one-time local backend that is then
  migrated is the normal resolution, not a finding.
- An unencrypted resource that holds nothing but public data, where the tag or
  classification says so explicitly.

## Context (for humans)

IaC mistakes scale by construction: one bad module is applied into every account that
consumes it, and the blast radius is whatever the apply credential can reach. That
credential is the part most reviews skip. A pipeline that can create IAM roles can
create itself a better one, so the privilege of the thing running `apply` bounds
everything else in this skill.

The other recurring surprise is state. Practitioners reach for `sensitive = true` and
believe the value is protected; it is a display flag. Anything Terraform manages, it
has seen, and anything it has seen is in the state file — which is why "who can read
the backend" is a more consequential question than most of the resource-level settings
a scanner will flag.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/backends-and-state.md` — backend and locking options per tool, what is
  stored in state and how to reduce it, and the port list worth failing a build over
- `checklists/terraform_hardening.yaml`
- `checklists/cloudformation_hardening.yaml`
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services).
- [Terraform recommended practices](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices).
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final).
