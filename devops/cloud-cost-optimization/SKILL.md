---
name: cloud-cost-optimization
description: "Almost every cloud estate is over-provisioned."
---

# Cloud Cost Optimization (Verbose)

## Core Patterns

### Right-Sizing Is the First and Largest Lever

Almost every cloud estate is over-provisioned. Instances are sized from a guess,
a worst-case peak that never materializes, or a copy-pasted template, and then
never revisited. The result is a fleet running at a fraction of its paid capacity.
Right-sizing — matching provisioned resources to measured usage — is the lever
with the most headroom, and it compounds with every other technique, so it comes
first.

Measure before cutting. Pull real CPU, memory, and IO over a representative
window (a week or more, covering peaks), then move each workload to the smallest
instance family and size that holds its p95 with headroom.

```promql
# CPU actually used vs provisioned, p95 over a week
quantile_over_time(0.95,
  rate(container_cpu_usage_seconds_total{env="prod"}[5m])[7d:5m])
```

For containerized workloads this is the requests-vs-limits problem — set requests
from observed p95, not from fear. See kubernetes-resource-management for the full
method, including why over-tight limits cause invisible throttling.

Right-sizing is not a one-time event. Usage drifts as features ship and traffic
grows, so schedule a recurring review; a workload right-sized last quarter is
often wrong this quarter.

### Commitment Discounts: Commit the Floor, Burst the Peak

On-demand pricing bundles a premium for the right to walk away at any moment. For
the portion of your usage that is predictable, that premium is pure waste.

The pattern is to shape purchases to the load curve:

- **Committed-use discounts / savings plans / reserved instances** for the steady
  baseline — the floor of usage that is always present. All three providers offer
  a version, trading a one- or three-year commitment for a lower rate.
- **On-demand** for the variable top of the curve, where flexibility is worth the
  premium.
- **Spot / preemptible instances** for interruptible, fault-tolerant work — batch
  jobs, CI, stateless workers, rendering. These run at a steep discount and can be
  reclaimed with little notice, so only use them where interruption is survivable
  and the work can resume elsewhere.

Buy commitments against a baseline you have actually measured, and revisit them as
usage shifts — an over-bought reservation for a workload you later shrank is a
sunk cost you keep paying.

### Storage Tiering and Lifecycle

Storage grows monotonically unless something deletes it, and old data is rarely
revisited even as it keeps billing. Two mechanisms address this:

- **Tiering.** Access frequency drops sharply with age for most data. Move it down
  a temperature gradient — for object storage, roughly hot → infrequent-access →
  archive (S3 Standard → Standard-IA → Glacier; equivalents on GCP and Azure).
  Each tier trades retrieval speed and cost for a lower resting price. Automate the
  transitions with lifecycle policies rather than manual migration.
- **Lifecycle expiry.** Data with a natural end of life — logs, temporary
  exports, old versions — should expire automatically. Enable expiration on
  versioned buckets so old object versions do not accumulate forever.

Then clear the debris that bills for nothing: volumes left unattached after their
instance was terminated, snapshots kept long past relevance, and stale machine
images. These are quiet, recurring charges for zero value.

### Killing Idle Resources

Idle resources are the purest waste in the bill — full price, zero value — and
removing them is often the fastest real saving because it touches nothing that is
actually serving traffic.

Common sources:

- **Non-production environments running around the clock.** Dev and staging are
  needed roughly 40 hours a week and billed for 168. Scheduled start/stop on a
  business-hours calendar cuts most of that.
- **Orphaned infrastructure.** Unattached disks, idle load balancers with no
  healthy targets, NAT gateways left after a subnet was decommissioned, and
  databases provisioned for a project that ended.
- **Over-provisioned managed services** kept at a tier the workload outgrew or
  never reached.

Sweep for these on a schedule. Infrastructure drift is part of why they
accumulate — resources created outside the IaC lifecycle are the ones nobody
remembers (see infrastructure-drift-detection, iac-best-practices).

### Egress: the Cost That Surprises Teams

Data egress is the line item that blindsides teams, because it is invisible in
architecture diagrams — the arrows between boxes have a price nobody drew. Three
kinds of transfer are metered, in roughly descending surprise:

- **Internet egress** — data leaving the cloud to users or other networks.
- **Cross-region** — data moving between regions of the same cloud.
- **Cross-availability-zone** — even traffic between zones within one region is
  commonly billed, which catches teams who spread chatty services across zones for
  availability without accounting for the transfer cost.

Design to minimize it:

- **Co-locate chatty components.** Keep services that talk constantly in the same
  zone/region; make cross-zone and cross-region boundaries coarse and infrequent.
- **Keep compute next to its data.** This is data gravity again (see
  cloud-provider-tradeoffs) — the egress consequence of splitting them is
  ongoing.
- **CDN for repeatedly-served content.** Serving the same object from an edge
  cache is far cheaper than repeated origin egress.
- **Private endpoints.** Route service-to-service and cloud-service traffic over
  private networking rather than the public internet where the provider prices it
  more favourably.

A cross-cloud data pipeline is the worst case: it can cost more in egress than in
all the compute it feeds, which is a major reason multi-cloud is expensive (see
multi-cloud-strategy).

### Attribution Makes Optimization Possible

You cannot optimize what you cannot attribute. Without ownership, cost is a single
opaque number that no team feels responsible for, and waste hides in the
aggregate.

Enforce a tagging policy — at minimum team, service, and environment — and treat
untagged resources as a defect. Produce per-owner showback (and, where the culture
supports it, chargeback) so each team sees its own trend and anomalies. A large
"untagged" slice in the cost report is both a governance gap and a reliable place
to find waste. Set budget alerts so a runaway cost is caught in days, not at the
end of the billing month.

## Common Anti-Patterns

❌ **Micro-optimizing line items** — hunting pennies on individual API calls while
the whole fleet runs at 15% utilization.
✅ Right-size the fleet first; that is where the money is.

❌ **Everything on-demand** despite an obvious, measurable steady baseline.
✅ Commit the baseline with savings plans / reservations; burst on-demand; batch
on spot.

❌ **Storage that only grows**, with no tiering or expiry.
✅ Automate lifecycle transitions and expiration; delete orphaned volumes,
snapshots, and images.

❌ **Dev and staging running 24/7** for a 40-hour work week.
✅ Schedule automatic shutdown of non-production outside business hours.

❌ **Ignoring egress** until the bill arrives.
✅ Co-locate chatty services, keep compute next to data, use CDNs and private
endpoints; treat cross-cloud transfer as expensive by default.

❌ **Untagged spend** nobody owns.
✅ Enforce tagging, produce per-owner showback, and set budget alerts.

❌ **Buy-and-forget reservations** that no longer match usage.
✅ Revisit commitments and right-sizing on a recurring schedule as load shifts.

❌ **Optimizing away needed reliability** — deleting redundancy to save money.
✅ Optimize waste, not resilience; protect what your SLOs require
(slo-sli-definition).

## Cloud Cost Optimization Checklist

- [ ] Right-sized instances, databases, and volumes from measured p95 usage
- [ ] Recurring right-sizing review scheduled, not one-time
- [ ] Steady baseline covered by committed-use discounts / savings plans / reservations
- [ ] Spot / preemptible used for interruptible, fault-tolerant work
- [ ] Storage lifecycle and tiering policies automated
- [ ] Orphaned volumes, snapshots, and images swept regularly
- [ ] Non-production environments shut down outside business hours
- [ ] Idle load balancers, NAT gateways, and unused services removed
- [ ] Egress minimized: co-location, data locality, CDN, private endpoints
- [ ] Cross-region and cross-AZ transfer costs accounted for in the design
- [ ] Tagging policy enforced; untagged resources treated as a defect
- [ ] Per-owner showback and budget alerts in place
- [ ] Reliability and SLO-required redundancy protected from cost cutting
