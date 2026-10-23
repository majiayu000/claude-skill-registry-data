---
name: dr-drill-runner
description: "The full DR-drill discipline for one service: author the runbook (per-tier RTO + RPO), pre-drill checklist (data sync state, alert silencing, customer comms), drill workflow (announce, fail-over, verify, fail-back) with timestamps, the supervised run protocol (refuse without declared RTO/RPO or against production, RTO/RPO monitoring cadence, abort-on-breach), and an auditor-ready post-drill report. Backup-integrity verification (SHA-256 + signature, restore spot checks, cross-region replication, retention, key recovery) and restore-time / RTO measurement (TTF segments, PITR latency, parallel-restore tuning, trend tracking) are worked in references. Per Google Cloud DR planning guide; covers cold / warm / hot standby tier-specific patterns. Use when a scheduled or post-incident failover drill for one service is being planned, executed, or written up, or when a new tier-1 service ships without a drill defined."
metadata:
  keywords: "disaster-recovery, dr-drill, rto, rpo, failover, runbook"
  version: "1.2.17"
---

# dr-drill-runner

Per the [Google Cloud DR planning guide], DR planning requires
"end-to-end recovery design addressing backup, restoration, and
cleanup procedures." Drills test that the procedure works AND that
the team can run it. Both surface different failures.

## When to use

- Quarterly DR drill (mandatory in compliance-heavy industries:
  banking, healthcare, defense).
- After a region-failover incident: rerun the drill with the
  lessons learned.
- New service onboarding: every new tier-1 service ships with its
  drill defined.

## Step 1 - Define RTO + RPO per service tier

Per the [Google Cloud DR planning guide]:

| Metric | Definition |
|---|---|
| RTO | Maximum acceptable length of time the application can be offline |
| RPO | Maximum acceptable data loss (time window) |

| Tier | Example RTO | Example RPO | Pattern |
|---|---|---|---|
| 1 (revenue-critical) | < 15 min | < 1 min | Hot standby (active-active) |
| 2 (customer-impacting) | < 4 hr | < 1 hr | Warm standby |
| 3 (internal) | < 24 hr | < 24 hr | Cold (rebuild from backup) |

Document per service in a service catalog; drills enforce the
contract.

## Step 2 - DR-pattern tier per service

Per the [Google Cloud DR planning guide]:

- **Cold**: Minimal preparation; recovery requires external
  intervention and extended downtime.
- **Warm**: Basic readiness with resources available; recovery
  stops normal ops temporarily.
- **Hot**: Continuous operation with built-in redundancy; minimal
  interruption.

Drill expectations differ:
- Cold: Test bring-up from backup (restore-time tests -
  [references/restore-time.md](references/restore-time.md)).
- Warm: Test failover automation + warm-up time.
- Hot: Test traffic redirection + sticky-session impact.

## Step 3 - Pre-drill checklist

```markdown
## Pre-Drill Checklist - `<service>` `<date>`

- [ ] Drill window scheduled (low-traffic; aligned with
      customer-comm window)
- [ ] Drill scope decided (region, single service, full app)
- [ ] Replication lag confirmed within RPO at T-30 min
- [ ] Monitoring alerts SILENCED for expected failure indicators
      (alert routing redirected to drill channel)
- [ ] On-call notified (avoid duplicate paging during drill)
- [ ] Customer comms sent if customer-impacting drill
- [ ] Rollback path documented (what triggers abort?)
- [ ] Drill commander assigned (owns go/no-go calls)
- [ ] Postmortem time scheduled (within 48hr of drill end)
```

Skipping the pre-drill = drills become incidents.

## Step 4 - Drill workflow

```markdown
## Drill Workflow

### T-0: Announce
- Post in #drill-channel; confirm all participants ready.
- Drill commander gives "GO" - record T-0 timestamp.

### T+0..N: Fail-over
- Execute the runbook step-by-step (everyone follows the doc; no
  improvisation).
- Capture timestamp of each step.

### Verify
- Run the verification suite (smoke + customer-impact + data integrity).
- Compare actual vs expected RTO; if RTO breached, decide:
  abort + rollback, or continue + capture learning.

### Fail-back
- If hot/warm: redirect traffic back to primary.
- If cold: tear down DR environment + restore primary.
- Verify primary is healthy before claiming drill complete.

### Cleanup
- Re-enable alerts (Step 3).
- Send "all clear" customer comms.
- Reconcile any drill-introduced data divergence.
```

## Step 5 - Post-drill report

```markdown
## Drill Report - `<service>` `<date>`

**Drill objective:** Verify warm standby fails over within RTO 4hr.

**Timeline:**
- T-30 min: Replication lag verified (52s - within RPO 1hr) ✓
- T-0: Announced, on-call silenced
- T+12m: Failover initiated
- T+47m: Standby took traffic
- T+1h22m: Verified service healthy on standby
- T+2h11m: Failback to primary
- T+3h05m: Drill complete

**RTO observed:** 1h22m (target: 4hr) ✓

**Issues found:**
1. CRITICAL: DNS TTL was 24hr in standby DNS records; users
   couldn't reach service for 23min after failover. Fix: lower
   TTL to 60s in standby zone before next drill.
2. MAJOR: Secret-manager copy step was undocumented; commander
   improvised. Fix: add Step 3.4 to runbook.
3. MINOR: One alert wasn't silenced in advance; on-call was paged.

**Action items (with owners + dates):**
- DNS TTL fix → @platform-team - 2026-05-20
- Runbook Step 3.4 → @sre - 2026-05-13
- Alert routing audit → @sre - 2026-05-13

**Next drill:** 2026-08-06 (quarterly cadence).
```

## Step 6 - Cold-tier-specific drill pattern

Cold drills = bring up from backup. Verifies:

- Backup is current within RPO ([references/backup-verification.md](references/backup-verification.md)).
- Restore time is within RTO ([references/restore-time.md](references/restore-time.md)).
- Infrastructure-as-code provisioning works (Terraform / CloudFormation /
  Bicep in DR account).
- Permissions + secrets are in place (per the [Google Cloud DR
  planning guide], "Permission and access validation in DR
  environments" + "Security synchronization").

## Step 7 - Hot-tier-specific drill pattern

Hot drills = redirect traffic between active replicas. Verifies:

- Health check propagation (load balancer detects standby is
  healthy).
- Sticky-session handling (do connections drain or break?).
- Cache warmup not required (or warmup time is within RTO).
- Cross-region replication lag stays within RPO during the drill.

## Step 8 - Cadence

| Tier | Cadence |
|---|---|
| 1 | Monthly (game-day style) |
| 2 | Quarterly |
| 3 | Annually |

Per the [Google Cloud DR planning guide]: "test it regularly,
noting any issues." Without cadence, runbooks rot.

## Run protocol (executing the drill end to end)

Nobody delegates failover execution; a human drill commander runs the five
stages below against this protocol. This is the **rehearsed** DR path - for
injecting unrehearsed failures see the `chaos-drill-protocol` skill in this plugin.

**Refuse to start when:**

- No declared RTO + RPO. Per the [Google Cloud DR planning guide], RTO is
  "the maximum acceptable length of time that your application can be
  offline" and RPO bounds acceptable data loss - without them there is no
  pass/fail criterion.
- The DR environment identifier matches `prod` / `production`.
- Any CRITICAL pre-drill item fails (backup integrity, key recovery, alert
  silencing) - halt and emit the blocking checklist instead of proceeding.

**Stage 1 - pre-drill.** Run the Step 3 checklist. Verify backup SHA-256
integrity, replication lag within RPO at T-30 min, and encryption-key
recoverability in the DR region per
[references/backup-verification.md](references/backup-verification.md).
Verify DR-environment configuration drift is within bounds - per the
[AWS DR testing whitepaper], "Manage configuration drift at the DR Region.
Ensure that your infrastructure, data, and configuration are as needed at
the DR Region."

**Stage 2 - failover.** Record T-0; execute the Step 4 runbook step by step,
capturing a timestamp per step. Per the [AWS DR testing whitepaper], "Our
experience has shown that the only error recovery that works is the path you
test frequently" - a runbook step that requires improvisation is logged as a
MAJOR finding immediately, never silently adapted.

**Stage 3 - RTO/RPO monitor.** While failover is active, sample on a fixed
interval (60 s is a workable default): replication lag at the DR side,
smoke-suite pass rate, and data-row spot checks. Measure time-to-functional
for the Restore + Verification segments per
[references/restore-time.md](references/restore-time.md) and compare against
the per-segment RTO budget. If observed TTF exceeds the RTO - abort the
failover, record the breach metrics, and skip directly to the report. Record
the peak RPO gap (replication lag at fail-over time); flag if it exceeds the
declared RPO.

**Stage 4 - fail-back.** Per Step 4: redirect traffic back (warm/hot) or
tear down + restore primary (cold), re-enable silenced alerts, send the all
clear, verify primary health before recording fail-back complete, reconcile
drill-introduced data divergence.

**Stage 5 - report.** Emit the Step 5 post-drill report, including the
observed TTF, total RTO, and peak RPO gap versus their declared targets.
Schedule the postmortem within 48 hours; every finding gets an owner + due
date before the drill closes.

[AWS DR testing whitepaper]: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/testing-disaster-recovery.html

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skip pre-drill checklist | Drill becomes incident | Step 3 mandatory |
| One person knows the runbook | Bus-factor 1; drill panics when they're out | Rotate drill commander |
| Skip post-drill report | Lessons lost; same issues recur | Step 5 mandatory + 48hr deadline |
| Test failover only; skip failback | Failback is the actual prod path; bugs hide | Step 4 covers both |
| Lower RTO target after a missed drill | Goalpost moving | Hold the line + invest in fixes |

## Limitations

- DR drills don't replace chaos engineering (this plugin's chaos skills) - they test rehearsed paths; chaos tests unrehearsed ones.
- Cloud-managed services may have built-in regional failover that
  bypasses your runbook; document boundaries.
- Some compliance regimes (FFIEC for banks) prescribe specific
  drill frequencies + scopes - verify per regulation.

## References

- [Google Cloud DR planning guide] - RTO / RPO / cold-warm-hot
  tiers / testing requirements
- [AWS DR testing whitepaper] - configuration-drift management,
  "test the path you execute" principle
- [references/backup-verification.md](references/backup-verification.md),
  [references/restore-time.md](references/restore-time.md) - drill
  prerequisites: backup integrity + RTO measurement
- `error-budget-tests` - incident
  metrics fed by drills (MTTR/MTBF schema in its references)

[Google Cloud DR planning guide]: https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide
