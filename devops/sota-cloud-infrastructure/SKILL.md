---
name: sota-cloud-infrastructure
description: >-
  State-of-the-art cloud infrastructure architecture (2026). Applies when designing, building, or auditing cloud environments on AWS, GCP, or Azure — account/project structure and landing zones, IAM and workload identity, VPC/network design, DNS/TLS/CDN, compute selection (serverless vs containers vs Kubernetes vs VMs), object storage and backup architecture, cost engineering (FinOps), and disaster recovery. Trigger keywords: cloud, AWS, GCP, Azure, Kubernetes, EKS, GKE, AKS, VPC, subnet, IAM, role, service account, serverless, Lambda, Cloud Run, Fargate, Terraform architecture, DNS, CDN, load balancer, FinOps, cost, rightsizing, disaster recovery, RTO, RPO, multi-region. Use for BOTH greenfield design and auditing existing infrastructure.
---

# SOTA Cloud Infrastructure

## Purpose

This skill encodes the 2026 state of the art for cloud infrastructure architecture:
organizational structure, identity, networking, compute selection, data placement,
cost, and resilience. Every rule exists to prevent a real failure class — blast-radius
spread, credential theft, public data exposure, egress bill shock, unmeetable RTOs,
or a Kubernetes cluster nobody needed.

Boundaries with sibling skills — reference, do not duplicate:
- **sota-devsecops** owns CI/CD pipelines, IaC scanning, Terraform state security, GitOps.
- **sota-sandboxing** owns container/runtime hardening (seccomp, rootless, distroless).
- **sota-observability** owns monitoring, alerting, SLOs, tracing.
- **sota-databases** owns database engine selection, schema, and query design.
- **sota-secrets-management** owns secret storage and rotation mechanics.

This skill owns: what accounts/networks/identities/compute/storage exist, how they
connect, what they cost, and how they survive failure.

## BUILD mode

Use when designing or extending cloud infrastructure (architecture docs, Terraform
modules, landing zones, network plans, DR plans).

1. Establish context before proposing anything: provider(s), org maturity (single
   account vs landing zone), environment count, data sensitivity, RTO/RPO targets,
   monthly spend ballpark, team size. A 3-person startup and a regulated enterprise
   get different answers from the same rules.
2. Read the matching rules files from the index below BEFORE writing config. Compute
   selection (rules/04) comes before networking details; account structure (rules/01)
   comes before everything.
3. Default to the boring, managed, restrictive option: managed services over
   self-hosted, private over public, multi-AZ over single-AZ, deny-by-default IAM and
   network policy. Every loosening gets a written justification in a comment.
4. Every resource you design must carry: owner tag, environment tag, cost-allocation
   tag, and a deletion/lifecycle story. Untagged infrastructure is unaccountable
   infrastructure.
5. State the cost and the failure mode of what you propose. "Three NAT gateways at
   per-hour + per-GB rates" and "this is single-region; region loss means restore
   from backup" belong in the design, not in the postmortem.
6. Produce infrastructure as code (Terraform/OpenTofu/Pulumi fragments), never
   console-click instructions, except for one-time org bootstrap steps which must be
   documented as such.

## AUDIT mode

Use when reviewing existing cloud environments, Terraform repos, or architecture docs.

Process: inventory what exists (accounts/projects, networks, identities, compute,
storage, DNS); walk the Audit checklist at the end of each relevant rules file;
report findings in the format below. Confirm exploitability/reality before reporting —
read the actual policy JSON or Terraform, don't infer from resource names.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **Critical** | External party can read/modify data or assume identity now | Public S3/GCS bucket with sensitive data; IAM role assumable by `*` or any OIDC subject; security group `0.0.0.0/0` on a database port; root/owner account without MFA; cross-account trust to an unknown account |
| **High** | One credential or insider step from compromise, or guaranteed outage class | Long-lived IAM user keys for humans or CI; wildcard `Action:*` on broad resources; single-AZ stateful workload with no tested backup; no SCPs/org policies on a multi-account org; flat network with no egress control; unencrypted snapshots shared externally |
| **Medium** | Weakens containment, recovery, or cost control | Shared account for prod and non-prod; no permission boundaries on delegated admins; backups in same account/region as source; no cost allocation tags; NAT for traffic that should use private endpoints; cert renewal manual |
| **Low** | Hygiene, drift, headroom | Inconsistent tagging; unused elastic IPs/disks; default VPC still present; missing IPv6 plan; quota headroom unmonitored |

Severity is judged by reachability (anonymous > authenticated external > tenant > insider)
× impact (data/identity compromise > availability > cost). Cost-only findings cap at
High (sustained material burn) and are usually Medium.

### Finding format

```
[SEVERITY] <short title>
Where: <account/project> / <resource or Terraform address> / <file:line if IaC>
Evidence: <the exact policy statement / CIDR / config proving it>
Impact: <who can do what, or what fails and how>
Fix: <specific change — policy JSON / Terraform diff / architecture move>
```

Group repeated instances of the same finding (e.g., 40 buckets without lifecycle
rules) into one finding with a count and a listing.

## Rules index

| File | Read this when... |
|---|---|
| rules/01-org-accounts-governance.md | Setting up or auditing org structure, landing zones, account/project strategy, SCPs/org policies, centralized logging/billing, tagging standards |
| rules/02-iam-design.md | Designing or auditing human access (SSO), workload identity, OIDC federation, permission boundaries, cross-account access, break-glass |
| rules/03-networking.md | Designing or auditing VPCs/VNets, subnets, egress control, private endpoints, hub-spoke, DNS, TLS certs, load balancers, CDN, DDoS, IPv6 |
| rules/04-compute-selection.md | Choosing serverless vs containers vs Kubernetes vs VMs; serverless patterns; Kubernetes architecture (autoscaling, requests/limits, PDBs) |
| rules/05-data-storage.md | Designing or auditing object storage, lifecycle policies, block/file/object choice, backup architecture, encryption and KMS key strategy |
| rules/06-cost-finops.md | Cost visibility, rightsizing, commitment discounts, spot, egress/NAT traps, unit economics, anomaly detection, cost review in PRs |
| rules/07-resilience-dr.md | RTO/RPO tiers, multi-AZ vs multi-region decisions, DR strategies, game days, dependency mapping, quotas, graceful degradation |

Cross-cutting tasks read multiple files: a "review our AWS account" audit touches all
seven; "should we use Kubernetes" is rules/04 + rules/06.

## Top 10 non-negotiables

1. **Blast-radius isolation by account/project, not by tag.** Prod, non-prod, security
   tooling, and logging live in separate accounts/projects under an org with
   guardrails (SCPs / org policy constraints / Azure Policy). A tag is not a security
   boundary; an account is.
2. **No long-lived credentials for humans.** Humans authenticate through SSO/identity
   federation (IAM Identity Center, Google Cloud Identity, Entra ID) with MFA and
   assume short-lived roles. Zero IAM users with passwords or access keys for people.
3. **Workload identity everywhere.** Workloads get roles/service accounts via the
   platform (instance profiles, IRSA/EKS Pod Identity, GKE Workload Identity, Azure
   managed identities) or OIDC federation (CI). A static cloud key in an env var or
   secret store is a finding, not a pattern.
4. **Public access blocked at the org edge.** Account-/org-level public-access blocks
   on object storage, org policy forbidding public IPs and public buckets by default;
   exceptions are explicit, listed, and reviewed.
5. **Three-tier network, deny-by-default.** Public subnets hold only entry points
   (LBs, NAT); apps in private subnets; data in isolated subnets with no internet
   path. Managed services reached via private endpoints, not the public internet.
   No `0.0.0.0/0` ingress except 80/443 on edge load balancers.
6. **Simplest compute that meets requirements.** Serverless/managed containers before
   Kubernetes; Kubernetes only with a written justification (scale, ecosystem need,
   team to run it). Every K8s workload ships with resource requests/limits, a PDB,
   and topology spread.
7. **Encryption with intentional keys.** Everything encrypted at rest (table stakes);
   customer-managed keys (CMK) for sensitive data with key policy ≠ data policy, so a
   single principal can't both read and exfiltrate.
8. **Backups that survive account compromise.** Critical data backed up cross-account
   (and cross-region per DR tier) with immutability/locking. A backup the producing
   account's admin can delete is not a backup against ransomware.
9. **Cost is an architecture review gate.** Allocation tags enforced, per-team
   visibility, anomaly alerts on; infra PRs state expected cost delta. Egress, NAT
   processing, and idle resources are checked in design, not discovered on the bill.
10. **DR is declared and tested.** Every system has an assigned RTO/RPO tier and a
    matching architecture (backup-restore → pilot light → warm standby →
    active-active). Multi-AZ is the default; multi-region is a justified exception.
    Untested DR plans are assumed broken — game days at least annually for tier-1.

## Operating notes

- Principles first, provider examples second. When the user's provider is known, give
  that provider's mechanism; otherwise name all three (AWS / GCP / Azure).
- Verify provider limits, instance types, and prices against current docs before
  committing them to designs — they change faster than any skill text.
- When this skill and a compliance framework conflict (CIS, SOC 2 mapping), state
  both and let the operator choose; do not silently relax.
