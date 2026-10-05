---
name: disaster-recovery-planning
description: "Disaster recovery has exactly two quantitative inputs, and every architectural"
---

# Disaster Recovery Planning (Verbose)

## Core Patterns

### RTO and RPO: The Two Numbers Everything Hangs On

Disaster recovery has exactly two quantitative inputs, and every architectural
choice downstream is a consequence of them.

**RTO — Recovery Time Objective** is the maximum tolerable time between a disaster
and service being restored. It answers "how long can we be down?" RTO drives how
much standby infrastructure you keep ready: a one-minute RTO is impossible if your
plan starts with provisioning servers.

**RPO — Recovery Point Objective** is the maximum tolerable amount of data loss,
expressed as time. It answers "how much recent work can we afford to lose?" An RPO
of five minutes means your most recent durable copy of the data can be at most five
minutes behind the moment of failure. RPO drives replication and backup frequency:
a five-minute RPO cannot be met by a nightly backup.

Two things teams get wrong. First, these are **business decisions**, set by the
people who own revenue, customer trust, and regulatory exposure — not defaults an
engineer picks. Second, they are **per-system**. An order ledger, a payments
record, and a recommendation cache have wildly different tolerances; a single
blanket "4-hour RTO" either over-spends on the cache or under-protects the ledger.
Tier your systems and assign each tier its own RTO/RPO.

The reason to fix these first is that they are the acceptance criteria for the
entire plan. Without them, "is this DR design good enough?" has no answer.

### Backup vs Replication vs Multi-Region

These three are often used interchangeably and protect against different failures.

**Backup** is a periodic, point-in-time copy stored independently of the source.
Its defining property is that it lets you go *back to a known-good moment*. That is
exactly what you need to recover from logical disasters — data corruption, an
accidental `DELETE` without a `WHERE`, a bad migration, ransomware. Backups are
cheap, but the RPO is the interval since the last one, and restore is slow.

**Replication** continuously copies changes to one or more standbys. It gives a
small RPO and fast failover, and it is how you survive the loss of a node, a zone,
or a region. But replication faithfully copies *everything*, including the bad
write and the corruption — the instant you delete the wrong table, it is deleted on
every replica. Replication is not a backup, and treating it as one is a common and
expensive mistake.

**Multi-region active-active** runs the full stack serving live traffic from two
or more regions simultaneously. Losing a region degrades capacity rather than
causing an outage. It offers the smallest RTO and RPO and the highest cost, and it
forces hard problems — data consistency across regions, conflict resolution,
latency — into the normal operating path rather than the recovery path.

The practical conclusion: you almost always need **both** backups and replication.
Replication handles infrastructure loss; backups handle bad data. Neither
substitutes for the other.

### The Four DR Patterns

DR strategies form a well-known spectrum trading cost against RTO/RPO.

| Pattern | What is running normally | RTO | RPO | Relative cost |
|---|---|---|---|---|
| **Backup & restore** | Nothing in the DR site; data sits in backups | Hours to days | Time since last backup | Lowest |
| **Pilot light** | Core data replicated live; application tier off | Tens of minutes to hours | Small (replication lag) | Low |
| **Warm standby** | A scaled-down but complete stack running | Minutes | Small | Medium |
| **Active-active** | Full stack serving traffic in 2+ regions | Near-zero | Near-zero | Highest |

**Backup & restore** keeps only data, off in storage. On disaster you provision
everything and restore. Cheapest to run, slowest to recover — appropriate for
systems that can tolerate a long outage and some data loss.

**Pilot light** keeps the "always-on" core warm: the database is replicated and
running, but the compute/application tier is dormant (or scaled to nothing). On
failover you start and scale the application against data that is already there.
Cheaper than a full running stack, much faster than restoring from cold.

**Warm standby** runs a complete but under-provisioned copy of the system in the
recovery region, taking replicated data. Failover means redirecting traffic and
scaling up. RTO is minutes because everything is already running; you pay to keep
a whole second environment alive.

**Active-active** eliminates the concept of "failover" for infrastructure loss —
all regions serve concurrently, so a region loss is a capacity event. You pay the
most, in money and in engineering complexity, and you accept the hardest
distributed-data problems as the price of near-zero RTO/RPO.

Choose the *cheapest* pattern that satisfies the RTO/RPO from step one. Buying
active-active for a system that can survive an hour of downtime is waste; running
backup-and-restore for a system with a five-minute RTO is negligence.

### Keeping Backups Out of the Blast Radius

A backup only helps if it survives the event that destroyed production. Three
independent boundaries matter:

- **Region** — a copy in the same region dies with a regional outage.
- **Account / project** — a copy under the same cloud account is exposed to the
  same billing suspension, the same misconfiguration, and the same compromised
  admin.
- **Credentials / trust boundary** — if the same key that runs production can
  delete the backups, a single compromised credential (or a ransomware operator
  who obtains it) can erase both.

Best practice keeps at least one copy in a separate region and a separate trust
boundary, and makes at least one copy **immutable** (write-once / object-lock /
retention-locked) so that neither an attacker nor an operator error can delete it
within its retention window. The 3-2-1 heuristic — three copies, two media/kinds,
one off-site — remains a sound baseline.

### Testing: An Untested Plan Is Not a Plan

A backup job that reports success has proven only that bytes were written. It has
not proven that the data is consistent, that the restore procedure works, that the
runbook still refers to systems that exist, or that the restore fits inside the
RTO. The only way to know is to perform a real restore into a clean, isolated
environment and measure how long it actually takes.

Untested DR plans fail on the day they are needed, and they fail in predictable
ways: the runbook references a decommissioned tool, an IAM permission is missing,
the restore takes three times the RTO, a dependency (DNS, secrets, a certificate)
was never captured, or the "backup" turns out to have been silently failing for
months. Regular game-day exercises — ideally including full regional failover for
higher tiers — convert these from production surprises into scheduled findings.
Automate the restore path so it is exercised often and consistently.

## Common Anti-Patterns

❌ **No documented RTO/RPO, or one blanket target for everything.**
✅ Tier systems by criticality; assign each tier explicit RTO and RPO from the
business.

❌ **"Replication is our backup."** A bad write or deletion propagates instantly.
✅ Keep independent point-in-time backups in addition to replication.

❌ **Backups in the same region, account, and credentials as production.**
✅ Separate region and trust boundary; at least one immutable copy.

❌ **Buying active-active for a system that tolerates an hour of downtime.**
✅ Choose the cheapest DR pattern that meets the stated RTO/RPO.

❌ **Trusting the backup job's success status.**
✅ Restore regularly into a clean environment and measure actual recovery time.

❌ **A runbook written once and never re-run.** It rots as systems are renamed and
retired.
✅ Exercise the plan on a schedule; treat every gap found as a defect to fix.

❌ **Backing up the database but not DNS, secrets, certs, and config.**
✅ Capture everything the restored system needs to actually serve traffic.

## Disaster Recovery Checklist

- [ ] RTO and RPO documented per system tier, signed off by the business
- [ ] DR pattern chosen to match each tier's RTO/RPO (no over/under-buying)
- [ ] Independent point-in-time backups exist alongside any replication
- [ ] At least one backup copy in a separate region and trust boundary
- [ ] At least one immutable / retention-locked copy
- [ ] Backup coverage includes data, config, secrets, DNS, and certificates
- [ ] Restore procedure documented as a runbook, kept current
- [ ] Full restore tested regularly into a clean environment
- [ ] Measured restore time verified to fit within RTO
- [ ] Failover (and failback) exercised for higher tiers
- [ ] Monitoring/alerting on backup and replication failures
- [ ] Post-exercise findings tracked to closure like any other defect
