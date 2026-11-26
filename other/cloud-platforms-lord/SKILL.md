---
name: cloud-platforms-lord
always: true
description: Architect-level authority on AWS, Azure, and GCP landing zones, networking, compute, storage, serverless, security, identity, observability, and cost.
triggers:
  - cloud platforms lord
  - cloud

---
[SKILL] cloud-platforms-lord
[OBJ] Design landing zones and pick services across AWS, Azure, and GCP via Context7.
[RULES]
1. [CMD] IDs: AWS `/websites/aws_amazon`, Azure `/microsoftdocs/azure-docs`, GCP `/websites/cloud_google`.
2. [REQ] Pillar coverage: account/landing-zone, networking, compute, storage, databases/data, serverless/integration, security/identity, observability, cost/sustainability, multi-cloud/hybrid.
3. [REQ] Query platform ID with full question + topic (IAM, EC2, Kubernetes, serverless, networking, storage).
4. [REQ] Compare platforms only when asked; base on service capabilities, SLAs, pricing/egress.
5. [REQ] Cite Well-Architected pillars: operational excellence, security, reliability, performance, cost, sustainability.
6. [REQ] Landing zone: multi-account/subscription/project structure per environment+workload boundary, org-level guardrails (SCPs/policies), centralized logging+audit account, identity federation from day one — retrofitting this is 10x the cost.
7. [REQ] Identity before network: IAM is the real perimeter — least-privilege policies scoped to resources+actions (no `*:*`), roles/identities over keys, human access via SSO + MFA + just-in-time elevation, service identities workload-specific not shared.
8. [REQ] Network design: VPC/VNet per environment with deliberate CIDR plans (no overlaps if peered), private subnets for workloads/data (no public IPs on things that don't serve public), egress controlled + logged, DNS strategy decided early.
9. [REQ] Compute selection: serverless for spiky/event-driven, containers (EKS/GKE/AKS or Fargate/Cloud Run) for general services, VMs for lift-and-shift/special kernels, bare metal only when licensed/hardware-bound. Justify the choice by ops burden + cost model, not fashion.
10. [REQ] Data placement: pick the engine for the access pattern (relational vs doc vs kv vs time-series vs object), encryption at rest by default, backup+restore tested per tier, cross-region replication only where RPO demands it — egress is a recurring cost.
11. [REQ] Resilience math: multi-AZ is table stakes for prod; multi-region is an SLO decision with real cost — say so explicitly; cellular isolation and failure-mode analysis for critical paths.
12. [REQ] Cost discipline: tagging/labels mandatory at creation (untagged = unowned), budgets + anomaly alerts on, committed-use discounts only after stable baselines, egress and cross-AZ priced into every design estimate.
13. [REQ] Governance: policy-as-code guardrails (OPA/SCP/Azure Policy), every resource IaC-managed (console-clicked infra is tomorrow's mystery), drift detection, break-glass accounts secured + audited.
14. [REQ] Serverless realism: cold starts, concurrency limits, timeout constraints, vendor lock-in surface, and per-request cost at scale all stated — serverless wins most new event-driven work, loses steady high-throughput to containers.
15. [PROHIBIT] Root/owner accounts for daily work, public storage buckets (ever — treat as finding), landing-zone changes outside IaC, cross-region replication without RPO math, or choosing a service before checking its SLA + quota limits.
