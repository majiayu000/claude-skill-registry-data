---
name: cloud-expert
description: Cloud guardrails for any vendor workload — Google Cloud (GCP, Vertex AI, GKE), AWS (IAM, EKS, Bedrock), Azure (Entra ID, Policy, AKS), Alibaba Cloud (RAM, mainland/international residency). Enforces identity least-privilege, mechanical policy, data boundaries, residency, cost caps, network egress and observability, with official-source validation before any claim. Trigger on any cloud infrastructure design, review, Terraform plan, or LLM/agent deployment; the-architect routes here.
---

# Cloud Expert

> **Identity, tenancy, residency and cost are the design constraints — not the console's defaults.**

One procedure, four vendor references. This skill enforces the discipline that makes a cloud
workload production-safe on whichever provider the team runs. It is not a vendor feature
catalogue: read the vendor reference for specifics, then apply the shared procedure.

| Vendor | Reference | Identity model | Policy engine |
|---|---|---|---|
| Google Cloud | [`references/gcp.md`](./references/gcp.md) | IAM + Workload Identity Federation | Organisation Policy, VPC Service Controls |
| AWS | [`references/aws.md`](./references/aws.md) | IAM roles + OIDC federation | SCPs, Config, Control Tower |
| Azure | [`references/azure.md`](./references/azure.md) | Entra ID + managed identities | Azure Policy, Management Groups |
| Alibaba Cloud | [`references/alibaba.md`](./references/alibaba.md) | RAM roles + STS | Resource Directory, Control Policies; mainland / international split |

## When to use

- Designing any cloud infrastructure, new or modified
- Before deploying agents or LLM workloads to a cloud provider
- Reviewing a Terraform plan or an architecture diagram for a cloud workload
- When a system touches multiple tenants, regulated data, or crosses a regional boundary
- When `the-architect` records a decision that names a specific cloud

## Procedure

Open the vendor reference first; every step below has vendor detail there.

1. **Identity and access** — least privilege for every workload identity and human role: no
   broad administrative roles on service identities; federated identities over long-lived
   keys; conditional, time-bound access where the platform supports it.
2. **Governance made mechanical** — region, resource-type and service constraints enforced by
   the platform's policy engine, not by convention; resource hierarchy mirrors environment and
   data classification; audit logging on identity changes and data-plane operations before any
   data lands.
3. **Data boundaries** — for every store: classification (public / internal / confidential /
   regulated), encryption at rest with customer-managed keys where required, tenant separation
   enforced at the data layer, and an explicit agreement wherever data crosses an account,
   project, subscription or organisation boundary.
4. **Residency** — every resource pinned to the required geography; policy prevents accidental
   multi-region or global creation; model endpoints regional where residency matters.
5. **Cost controls** — budget alerts at 50 / 75 / 90 / 100 %; autoscaling upper bounds set;
   LLM call volumes capped or rate-limited; commitments or spot capacity evaluated.
6. **Network and egress** — private connectivity where public endpoints are avoidable; egress
   estimated for cross-region and internet-bound traffic; default-deny with explicit allows.
7. **Observability** — dashboards, alerting on error rate, latency and cost, and log routing to
   a central retention point, all before go-live.
8. **Run the Adversarial Gate** — name the vendor's common failure modes (listed in each
   reference) and confirm each has a mitigation or a named risk owner.

## Official sources — validate before you assert

Every service, quota, price or model claim cites an official document from the vendor's
documentation or architecture centre (URLs in each reference). Quotas, prices and model names
are dated facts: stale until re-verified against the source on the day you assert them.

## Outputs

- Guardrail checklist (pass / fail per item), per vendor
- Identity matrix: principal | role | scope | justification
- Data classification and boundary map; residency confirmation
- Budget alert and autoscaling-bound confirmation
- Open findings for human review

## Guardrails

- **No administrative roles on workload identities.** Ever.
- **Residency is a constraint, not a preference.** Enforce it with policy, not convention.
- **Budget alerts are not optional.** An unmonitored LLM workload produces a surprise invoice.
- **Audit logs are evidence.** Enable them before go-live, not after an incident.
- **One vendor reference per decision.** Do not let a multi-cloud design inherit the weakest
  provider's defaults; run the procedure per vendor.
