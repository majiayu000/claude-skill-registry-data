---
name: cloud-provider-tradeoffs
description: "Compute, object storage, block storage, a managed relational database, a message"
---

# Cloud Provider Tradeoffs (Verbose)

## Core Patterns

### The Commodity Layer Is a Tie

Compute, object storage, block storage, a managed relational database, a message
queue, a load balancer, a CDN — every major provider has all of these, and they
are close enough in capability that comparing them line by line is wasted effort.
If your architecture only uses the commodity layer, the choice is dominated by
price, region availability, and what your team already knows.

| Need | AWS | GCP | Azure |
|---|---|---|---|
| Object storage | S3 | Cloud Storage | Blob Storage |
| Virtual machines | EC2 | Compute Engine | Virtual Machines |
| Managed Kubernetes | EKS | GKE | AKS |
| Serverless functions | Lambda | Cloud Functions / Cloud Run | Functions |
| Managed relational | RDS / Aurora | Cloud SQL / AlloyDB | Azure SQL / Flexible Server |
| Managed NoSQL | DynamoDB | Firestore / Bigtable | Cosmos DB |
| Data warehouse | Redshift | BigQuery | Synapse / Fabric |
| Object identity / access | IAM | Cloud IAM | Entra ID + RBAC |

Naming and defaults differ, but the shapes match. The moment your comparison
turns into a 200-row feature matrix, you are measuring the wrong layer.

### Differentiation Lives in Managed Services

The real decision is one tier up, where the providers diverge in philosophy:

- **BigQuery vs Redshift.** BigQuery is serverless — you run a query, it bills
  the query, there is no cluster to size. Redshift (in its classic form) is a
  provisioned cluster you scale and tune. A team that wants zero warehouse ops
  leans one way; a team that wants predictable reserved capacity leans the other.
- **Cloud Run vs Lambda vs Container Apps.** All run containers on demand, but
  the concurrency model, request lifecycle, and pricing granularity differ enough
  to change your architecture. See serverless-architecture.
- **GKE vs EKS vs AKS.** GKE is generally considered the most mature managed
  Kubernetes, with the strongest autoscaling and upgrade automation. This matters
  more than the underlying VM prices for a container-heavy shop.

Pick the two or three services that carry the weight of your system and evaluate
those in depth. Everything else is noise.

### Data Gravity and Egress

Data has gravity: it is expensive and slow to move, so compute migrates to sit
next to it. Whichever cloud holds your large datasets tends to acquire all their
consumers over time, because internet egress is billed per gigabyte and
cross-cloud transfer is both metered and latency-heavy.

This is the single most common way a "we'll stay flexible" plan quietly fails —
the data lake lands in one cloud, and two years later everything that reads it
lives there too, egress-free, and moving is now a project. Decide where the data
lives first, and let compute follow. cloud-cost-optimization covers egress in
detail.

### Organizational Gravity

The technically-best cloud is often not the right one. Weigh, honestly:

- **Existing skill.** IAM policy languages, deployment tooling, and failure modes
  differ per cloud. A fluent team is worth more than a marginal feature edge.
- **Enterprise agreements.** Committed spend, Microsoft or Google enterprise
  relationships, and negotiated discounts frequently pre-decide the platform.
- **Hiring market.** AWS has the deepest talent pool; that lowers the cost of
  growing the team.
- **Compliance posture already earned.** If one cloud already carries your
  audited controls (see compliance-automation), replicating them elsewhere is
  real work.

### Regional and Regulatory Footprint

Check that the provider has regions where you need them — for latency, for data
residency, and for disaster-recovery separation. Sovereignty requirements (data
must stay in a specific country or jurisdiction) can eliminate a provider outright
or force a specific region, and this is one of the few genuine drivers of
multi-cloud (see multi-cloud-strategy). Verify the specific managed services you
need are actually available in the target region — service rollout is uneven, and
the newest services reach secondary regions last.

### Pricing Models Differ in Shape, Not Just Number

Do not compare sticker prices; compare models against your workload's shape:

- A **serverless** warehouse bills per query scanned — cheap for sporadic
  analytics, alarming for a dashboard that polls every ten seconds.
- A **provisioned** cluster bills for uptime — cheap under steady load, wasteful
  when idle.
- Committed-use discounts, savings plans, and reserved capacity all reward
  predictability but lock you into a term.

The same architecture can be cheapest on different clouds depending only on
whether its load is spiky or steady. Model your actual usage curve.

### Ecosystem, Maturity, and Support

Two providers can offer the same service on paper with very different lived
experience, and this is hard to see from a comparison chart:

- **Service maturity.** A service that has existed for years has better docs,
  more Stack Overflow answers, more third-party integrations, and fewer sharp
  edges than a freshly-launched equivalent. GKE's autoscaling and Lambda's event
  ecosystem are examples of maturity that a newer competitor's feature list does
  not capture.
- **Regional rollout lag.** New services reach a provider's secondary regions
  months after the primary ones. If you operate outside the flagship regions,
  confirm availability rather than assuming it.
- **Support tier and account engineering.** For a large or regulated workload,
  the quality and cost of enterprise support, and access to solutions architects,
  can matter as much as any feature. Price the support tier you will actually
  need.
- **Third-party and marketplace ecosystem.** Available managed offerings, ISV
  integrations, and Terraform provider coverage differ, and a gap here becomes
  your team's maintenance burden.

Maturity is a feature you cannot see in a feature matrix — weigh it deliberately,
especially for anything load-bearing.

## Common Anti-Patterns

❌ **Deciding on a giant feature-comparison spreadsheet.** It measures the
commodity layer, which is a tie, and nobody reads it after the decision.
✅ Evaluate the two or three managed services your architecture actually leans on.

❌ **Ignoring the team's existing fluency** and picking the "best" cloud in the
abstract.
✅ Weight current skill, tooling, and enterprise agreements explicitly in the
scoring — they are real costs, not excuses.

❌ **Splitting compute and data across clouds** without a requirement forcing it.
✅ Anchor on where the data lives and keep compute next to it; pay egress only
where a real need justifies it.

❌ **Assuming price parity from published rates.**
✅ Model your workload's shape (spiky vs steady) against each provider's pricing
model; the cheapest option flips with the shape.

❌ **Letting one exciting service dictate the entire platform** for unrelated
workloads.
✅ If one service is genuinely unique and decisive, consider best-of-breed
placement rather than moving everything.

❌ **"Cloud-agnostic from day one"** as a default stance.
✅ Commit to a primary cloud, use its managed services, and treat lock-in as a
priced trade-off — revisit only against a concrete trigger.

## Cloud Provider Selection Checklist

- [ ] Identified the two or three managed services the architecture depends on
- [ ] Compared those services concretely, not the commodity layer
- [ ] Weighted existing team skill, tooling, and enterprise agreements
- [ ] Confirmed regions exist for latency, residency, and DR separation
- [ ] Verified required services are available in the target regions
- [ ] Located data gravity and planned compute to sit beside it
- [ ] Modeled workload shape (spiky vs steady) against each pricing model
- [ ] Treated lock-in as a priced cost with a revisit trigger, not a veto
- [ ] Scored the decision with a weighted matrix (technical-decision-making)
- [ ] Recorded the decision and its falsifier as an ADR
