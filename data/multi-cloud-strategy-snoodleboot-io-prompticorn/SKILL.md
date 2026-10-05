---
name: multi-cloud-strategy
description: "\"Multi-cloud\" is a loose word that hides four distinct architectures with"
---

# Multi-Cloud Strategy (Verbose)

## Core Patterns

### Name the Pattern You Actually Need

"Multi-cloud" is a loose word that hides four distinct architectures with
different costs. Most requests for multi-cloud are really requests for one of the
cheaper cousins.

| Pattern | What it means | Typical genuine driver | Cost |
|---|---|---|---|
| Multi-region | One provider, several regions | Latency, availability, disaster recovery | Low — native to the platform |
| Hybrid | Cloud plus on-prem / colocation | Legacy systems, data residency, sunk capex | Medium |
| Best-of-breed | Different workloads on different clouds | One provider's service is genuinely superior | Medium |
| Multi-cloud (true) | The same workload runs on two+ providers | Regulatory mandate, whole-provider resilience, M&A | High |

The important realization: **most availability and latency goals are met by
multi-region on a single cloud**, which is a supported, well-trodden path with no
cross-provider tax. If someone asks for multi-cloud "for resilience", check
whether multi-region already satisfies the actual SLO (see slo-sli-definition)
before taking on a second provider.

### Justify It With a Requirement, Not a Principle

Avoiding vendor lock-in is not, by itself, a justification. Lock-in is a cost you
can quantify; true multi-cloud is a cost that is almost always larger. Multi-cloud
earns its keep only against a concrete requirement:

- **Regulatory / sovereignty** — data or workloads must live in jurisdictions or
  under conditions a single provider cannot satisfy.
- **Contractual** — a large customer's agreement mandates provider diversity or a
  specific provider you do not otherwise use.
- **Whole-provider resilience the business truly requires** — surviving the
  outage of an entire cloud, not just a region. This is rare; most businesses
  accept single-provider-with-multi-region risk once they price the alternative.
- **Mergers and acquisitions** — you inherited another cloud and must operate
  both, at least for a transition.
- **A genuinely unique service** — one provider has a capability with no adequate
  substitute, decisive for one workload (this usually leads to best-of-breed, not
  full multi-cloud).

If none of these apply, the honest recommendation is a single primary cloud with
managed-service lock-in accepted as a priced trade (see
cloud-provider-tradeoffs).

### Count the Costs Before Committing

Multi-cloud spreads cost across places that do not show up on a pricing
calculator:

- **Duplicated expertise.** Two IAM models, two networking stacks, two sets of
  failure modes — the team must be fluent in both, or you hire twice.
- **Lowest-common-denominator architecture.** True portability means using only
  what both clouds offer, which excludes the differentiated managed services that
  justified cloud in the first place.
- **Egress and latency.** Any workload that spans clouds pays per-gigabyte egress
  and eats cross-provider network latency on every hop
  (see cloud-cost-optimization).
- **Doubled operational surface.** Two monitoring setups, two deployment
  pipelines, two on-call runbooks, two security postures to audit.
- **Slower delivery.** Every feature must be designed against the constraints of
  both platforms.

These are what you weigh against the lock-in being avoided. Frequently the lock-in
is the cheaper risk.

### Choose a Coupling Level

Multi-cloud is not one architecture. Pick the least coupling that meets the
requirement:

**Best-of-breed placement.** Each workload runs on the cloud where it is
strongest; no workload is required to be portable. Analytics on BigQuery, the
main app on AWS, an ML service where the tooling is best. Cheapest and most
common form of "multiple clouds", and it keeps full managed-service leverage per
workload. The cost is cross-cloud data movement, so place data-heavy workloads
next to their data.

**Portable core.** Package workloads as containers on Kubernetes and use open
data formats (Parquet, standard SQL, open table formats) so a workload *can* be
relocated with effort, without abstracting every dependency away. A pragmatic
middle ground — you retain most managed services for the periphery while keeping
the core movable. Kubernetes gives compute portability; it does **not** make your
managed databases or queues portable, so those still need a plan.

**Full abstraction.** A provider-agnostic layer (often Terraform plus a
homegrown or third-party abstraction) sits over everything, so any workload runs
anywhere. This delivers maximal portability and is almost always a mistake for
general workloads: you rebuild, worse, the managed services you are paying the
cloud to run, and you pay the abstraction's maintenance forever. Reserve it for
the narrow slice with a hard portability requirement.

### Centralize the Cross-Cutting Concerns

If you commit to genuine multi-cloud, the concerns that span providers must be
unified or the operational cost compounds:

- **Identity** — federate to a single identity provider; do not maintain
  disconnected IAM populations per cloud.
- **Secrets** — one secrets system spanning providers, not a per-cloud silo
  (see secret-management).
- **Observability** — one pane of glass aggregating metrics, logs, and traces
  across clouds, so an incident does not require logging into two consoles.
- **Provisioning** — a single IaC toolchain (see iac-best-practices) with
  per-provider modules, not click-ops in two portals.
- **Networking** — a deliberate interconnect (private peering / dedicated
  interconnect) rather than routing sensitive traffic over the public internet.

### Exercise the Failover You Claim to Have

A multi-cloud resilience story that has never failed over is a story, not a
capability. If the justification is surviving a provider outage, that failover
must be tested on a schedule — data must actually be replicated and current, DNS
and traffic steering must actually cut over, and the standby must actually carry
load. Untested failover reliably fails when first used in anger.

## Common Anti-Patterns

❌ **"Multi-cloud to avoid lock-in"** with no concrete requirement.
✅ Commit to a primary cloud and accept priced lock-in unless a named
requirement (regulatory, contractual, M&A) forces otherwise.

❌ **Reaching for multi-cloud when multi-region would do.**
✅ Meet availability and latency goals with multi-region on one cloud first;
verify against the actual SLO.

❌ **Full abstraction over everything** to stay portable.
✅ Use best-of-breed placement or a portable core; reserve abstraction for the
narrow slice that truly needs it.

❌ **Lowest-common-denominator design** that bans every differentiated service.
✅ Let each workload use its cloud's best managed services; keep only the core
movable if portability is required.

❌ **Chatty cross-cloud calls on the hot path**, quietly billing egress and
adding latency.
✅ Keep data and its consumers co-located; make cross-cloud boundaries coarse and
rare.

❌ **Two clouds, two IAM models, two secrets stores, two dashboards.**
✅ Federate identity, unify secrets and observability, provision from one IaC
toolchain.

❌ **A failover plan that has never been run.**
✅ Test cross-cloud failover on a schedule — replication, cutover, and load.

## Multi-Cloud Strategy Checklist

- [ ] Confirmed the need is true multi-cloud, not multi-region / hybrid / best-of-breed
- [ ] A concrete requirement (regulatory, contractual, resilience, M&A) is named
- [ ] Multi-region on one cloud ruled out against the actual SLO
- [ ] Costs counted: duplicated skill, LCD architecture, egress, doubled ops
- [ ] Coupling level chosen deliberately (best-of-breed / portable core / abstraction)
- [ ] Data-heavy workloads placed next to their data to limit egress
- [ ] Identity federated to a single provider
- [ ] Secrets unified across clouds (secret-management)
- [ ] Single observability pane spanning all providers
- [ ] One IaC toolchain provisions every cloud (iac-best-practices)
- [ ] Cross-cloud networking deliberate, not public-internet by default
- [ ] Failover tested on a schedule if resilience is the justification
