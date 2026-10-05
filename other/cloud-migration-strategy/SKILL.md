---
name: cloud-migration-strategy
description: "There is no such thing as \"the migration.\" An estate is a collection of"
---

# Cloud Migration Strategy (Verbose)

## Core Patterns

### The 6 R's: A Decision Per Workload

There is no such thing as "the migration." An estate is a collection of
applications, and each one gets an independent disposition. The industry-standard
framing is the six R's, and the discipline is to inventory every workload and
assign one — with a reason — rather than applying a single strategy to everything.

**Rehost** — "lift and shift." Move the application essentially unchanged onto
cloud VMs. It is the fastest and lowest-risk option and it captures the operational
wins of leaving the datacenter, but by design it captures none of the cloud's
elasticity, managed-service savings, or resilience. It is a starting position, not
usually an ending one.

**Replatform** — "lift and reshape." Make targeted optimizations during the move
without redesigning the application: swap a self-managed database for the managed
equivalent, put it behind a managed load balancer, containerize it. Modest effort,
meaningful operational savings, core architecture untouched.

**Refactor / re-architect** — redesign the workload to be cloud-native: managed
services, serverless, containers, decomposition. This is the highest-cost and
highest-value path, and it is justified only for workloads where the added agility,
scale, or cost profile pays for the engineering. Refactoring everything is a common
and expensive error.

**Repurchase** — abandon the custom application and move to a SaaS product that
does the job. Often the cheapest total outcome for commodity capabilities (email,
CRM, ticketing) where maintaining a bespoke system adds no differentiation.

**Retire** — turn it off. Real estates always contain applications that nobody
uses, that duplicate another system, or that exist only because no one dared delete
them. Discovering and retiring these reduces the migration scope, the attack
surface, and the running cost at once.

**Retain** — leave it where it is, for now. Some workloads are too risky to touch,
not yet worth the effort, bound by compliance or data-residency rules, or waiting
on a dependency. "Retain" is a legitimate, documented decision — not a failure to
decide.

The "retire" and "retain" outcomes are as valuable as any move: the cheapest
workload to migrate is the one you switch off, and the safest is the one you
correctly decide not to touch yet.

### Lift-and-Shift First, Then Optimize

A recurring temptation is to re-architect applications *as* they move — "we're
touching it anyway, let's do it right." This couples two independently hard
problems: changing the platform underneath the application and changing the
application's design. When something breaks after cutover, you cannot tell which
change caused it, and the rollback has to undo both.

The lower-risk sequence for most estates is: **rehost (or replatform) first to get
out of the datacenter, stabilize in the cloud, then refactor the workloads that
justify it.** This matters because datacenter exits are often on a clock — a lease
ending, a hardware refresh you don't want to buy, a contract deadline — and
rehosting reaches that deadline fastest. Once running in the cloud, iteration is
cheap and reversible in a way it never was on-premises, so optimization work
happens on favorable ground. Migrate to the cloud, then improve *in* the cloud;
don't try to do both in a single irreversible step.

This is a sequencing argument, not a claim that lift-and-shift is the destination.
A pure rehost that is never followed by optimization leaves most of the cloud's
value unrealized and can even cost more than on-prem. The point is to separate the
platform move from the redesign in time.

### Strangler-Fig for Large Systems

Large, business-critical systems cannot be safely moved as one unit, and rewriting
them from scratch while the original keeps changing is the classic doomed project.
The **strangler-fig** pattern (named for the vine that grows around a tree and
gradually replaces it) migrates incrementally:

1. Place a routing layer — a proxy, gateway, or facade — in front of the existing
   system, initially forwarding everything to it.
2. Build one capability in the new environment.
3. Redirect just that route through the router to the new implementation, leaving
   everything else on the old system.
4. Verify, then repeat for the next capability.
5. When no traffic reaches the old system, decommission it.

Each step is small, independently deployable, individually testable, and — because
the router can point back at the old implementation — reversible. This is the
opposite of a big-bang cutover, where the entire system switches at once and a
failure means rolling the whole thing back under pressure. The strangler-fig trades
a single terrifying event for many boring ones, which is exactly the trade you
want for a critical system.

### Data Migration Is the Real Risk

Compute is largely stateless and therefore easy to move: stand up the new
instances, shift traffic, tear down the old. **Data is where migrations actually get
hard**, for two reasons that compound.

First, volume: copying a large dataset takes real wall-clock time, and for very
large datasets, network transfer can be slower than physically shipping data on
transfer appliances — a bandwidth-versus-deadline calculation worth doing
explicitly rather than assuming the network is fine.

Second, and more dangerous: the source keeps changing while you copy. A bulk copy
that takes hours or days is stale the moment it starts. The standard approach is a
bulk transfer of the historical data followed by **change data capture** or
ongoing replication to stream subsequent changes into the target, keeping it in
sync until cutover — at which point the source is frozen and the last changes are
drained. Throughout, you need explicit **consistency and validation**: row counts,
checksums, referential-integrity checks, and reconciliation of the two datasets, so
that you cut over on evidence that the target is correct and complete, not on hope.

Never treat data as a step you'll "handle at the end." It is the constraint the
rest of the plan should be built around.

### De-Risking the Cutover

The cutover — the moment production shifts from old to new — is where migration
outages concentrate, because it is the one irreversible-feeling step. The goal is
to make it neither irreversible nor all-at-once:

- **Run in parallel.** Keep the old system live and capable of serving while the
  new one takes traffic, so falling back is redirecting, not rebuilding.
- **Shift a slice first.** Route a small fraction of traffic (or one low-risk
  customer segment) to the new environment, watch error rates and latency, and
  widen only once it is proven — a canary for infrastructure.
- **Keep a tested rollback.** Have a rehearsed path back to the old system, and do
  not cut over any system you cannot roll back. A rollback plan you have never
  executed is a guess.
- **Validate before real users.** Confirm the new environment is correct — data
  validated, smoke tests passing, dependencies reachable — *before* directing
  production traffic, not by watching it fail with live users.
- **Choose the window.** Cut over during low traffic so that if something is wrong,
  fewer users are affected and there is room to recover.

## Common Anti-Patterns

❌ **Big-bang migration of the whole estate at once, no rollback.**
✅ Per-workload dispositions, incremental sequencing, a rehearsed fallback.

❌ **Re-architecting during the move.** Couples a platform change to a design
change; failures are unattributable.
✅ Rehost/replatform first, stabilize, then refactor what's worth it.

❌ **No inventory — migrating applications nobody uses.**
✅ Inventory everything; retire the dead weight before moving anything.

❌ **Defaulting every app to one R** (all rehost, or all refactor).
✅ Assign each workload an R with a documented reason.

❌ **Treating data migration as a final afterthought.**
✅ Plan bulk-load plus CDC/replication, validation, and cutover around the data.

❌ **Cutover with no parallel run, canary, or rollback.**
✅ Parallel-run, shift a slice first, keep a tested rollback, pick a quiet window.

❌ **Pure lift-and-shift with no follow-up optimization.** Leaves cloud value
unrealized, sometimes costs more than on-prem.
✅ Treat rehost as a stage; schedule the optimization it enables.

❌ **Assuming the network can move the data in time.**
✅ Compare transfer time against deadlines; consider physical transfer appliances.

## Cloud Migration Checklist

- [ ] Full workload inventory with dependencies mapped
- [ ] Each workload assigned one of the 6 R's, with a reason
- [ ] Unused/duplicate workloads identified and retired
- [ ] Platform move (rehost/replatform) separated in time from re-architecture
- [ ] Large systems migrated via strangler-fig, not big-bang rewrite
- [ ] Data migration plan: bulk load + CDC/replication to stay in sync
- [ ] Data validation defined (row counts, checksums, reconciliation)
- [ ] Network-transfer time compared against deadlines (physical transfer if needed)
- [ ] Cutover uses parallel run and/or traffic canary
- [ ] Tested rollback path for every cutover
- [ ] Target validated before real traffic is sent
- [ ] Cutover scheduled in a low-traffic window
- [ ] Post-migration optimization scheduled for rehosted workloads
