---
name: compliance-automation
description: "The annual compliance scramble exists because controls are tested once, by"
---

# Compliance Automation (Verbose)

## Core Patterns

### Continuous Control Monitoring

The annual compliance scramble exists because controls are tested once, by
hand, shortly before the auditor arrives. That model fails on its own terms:
period-based reports and certifications ask whether the control operated
*throughout* the window, and a test performed in week 50 says nothing about
weeks 1 through 49.

Continuous control monitoring inverts it. Each control gets an automated check
running on the cadence at which the control can actually fail, and every run
persists a dated result. Compliance stops being a project and becomes a
property of the system, observed the same way you observe latency.

Define each control as a monitored object:

```yaml
- id: IC-12
  intent: Production data stores are encrypted at rest
  frameworks: [soc2-confidentiality, iso27001-cryptography, pci-protect-stored-data]
  owner: platform-team
  check: checks/storage_encryption.py
  cadence: 30m
  also_on: [infrastructure-change, new-account-onboarded]
  severity: high
  on_failure:
    - open_ticket: platform-team
    - block_release_if: resource_is_new
  evidence_retention: 18mo
```

Choose the cadence from the failure mode, not from convenience:

| Control class | Cadence | Why |
|---|---|---|
| Cloud resource configuration | Continuous / on change | Changes at any moment, often outside the pipeline |
| Pipeline gates (review, tests, approvals) | Per change | The change is the unit of control |
| Access grants and privileges | Daily reconcile, quarterly attest | Joiners and leavers move constantly |
| Vulnerability posture | Daily | Findings age against an SLA |
| Backup restoration | Monthly | Expensive; failure is slow-moving |
| Policy acknowledgement, training | Per cycle | Annual by nature |

Alert on the *trend*, not only the current state. A control that fails for two
hours every deploy is a finding even though it is green when you look.

### Evidence Collection as Code

Treat evidence collectors as production code: versioned, reviewed, tested,
scheduled, and monitored for their own failures. A collector that silently
stopped running three months ago produces a hole you discover during fieldwork.

```python
# collectors/access_review.py
"""Evidence for IC-07: privileged access is approved, least-privilege, reviewed."""

def collect(period: Period) -> Evidence:
    grants = idp.list_role_assignments(scope="production")
    workforce = hris.list_employees(as_of=period.end)
    approvals = tickets.search(type="access-request", closed_within=period)

    records = []
    for g in grants:
        person = workforce.get(g.principal)
        records.append(
            {
                "principal": g.principal,
                "role": g.role,
                "granted_at": g.created_at,
                "employment_status": person.status if person else "NOT_IN_HRIS",
                "approval_ticket": approvals.find_for(g),
                "last_used": idp.last_activity(g.principal),
            }
        )

    return Evidence(
        control="IC-07",
        period=period,
        collected_at=utcnow(),
        sources=["idp:prod", "hris", "tickets"],
        records=records,
        exceptions=[r for r in records
                    if r["employment_status"] != "ACTIVE"
                    or r["approval_ticket"] is None],
    ).sign()
```

Four properties make the output audit-grade:

- **Authoritative source.** Pull from the system's API, not from a
  human-maintained spreadsheet describing that system.
- **Provenance.** Record which systems were queried, when, and by what identity.
- **Immutability.** Write once to storage that denies modification, and hash or
  sign the artifact.
- **Reproducibility.** Re-running for the same period yields consistent results,
  which is what lets an auditor spot-check you.

Surface exceptions explicitly rather than burying them in a row count. The
exception list is the most useful thing the collector produces — it is your gap
list, generated daily.

### Policy as Code

A written policy is an intention. The same rule expressed as code and placed in
a gate is a control, and it produces an enforcement record every time it runs.

Rego, evaluated against a Terraform plan pre-merge:

```rego
package compliance.infra

import rego.v1

# IC-12: storage encrypted at rest
deny contains msg if {
    r := input.planned_values.root_module.resources[_]
    r.type == "aws_s3_bucket"
    not r.values.server_side_encryption_configuration
    msg := sprintf("IC-12: bucket %v has no encryption configured", [r.name])
}

# IC-04: no unrestricted ingress to production
deny contains msg if {
    r := input.planned_values.root_module.resources[_]
    r.type == "aws_security_group_rule"
    r.values.type == "ingress"
    r.values.cidr_blocks[_] == "0.0.0.0/0"
    not r.values.description == "public-load-balancer"
    msg := sprintf("IC-04: rule %v allows unrestricted ingress", [r.name])
}

# IC-19: regulated data stores must carry a data classification tag
deny contains msg if {
    r := input.planned_values.root_module.resources[_]
    r.type in {"aws_rds_cluster", "aws_dynamodb_table"}
    not r.values.tags.data_classification
    msg := sprintf("IC-19: %v missing data_classification tag", [r.name])
}
```

Cloud Custodian for continuously evaluating and remediating deployed state:

```yaml
policies:
  - name: rds-unencrypted-not-permitted
    description: IC-12 — flag and notify on unencrypted database instances
    resource: aws.rds
    filters:
      - type: value
        key: StorageEncrypted
        value: false
    actions:
      - type: tag
        key: compliance-violation
        value: IC-12-unencrypted-at-rest
      - type: notify
        to: [platform-team@example.com]
        transport: {type: sqs, queue: compliance-findings}

  - name: iam-keys-past-rotation-age
    description: IC-08 — surface access keys older than the rotation window
    resource: aws.iam-user
    filters:
      - type: access-key
        key: CreateDate
        value_type: age
        value: 90
        op: greater-than
    actions:
      - type: notify
        to: [security@example.com]
        transport: {type: sqs, queue: compliance-findings}
```

Run the same intent at three points, because each catches what the others miss:

| Point | Catches | Failure mode it prevents |
|---|---|---|
| Pre-merge (plan) | Non-compliant change before it exists | Cheapest fix, no exposure |
| Admission (deploy time) | Bypasses of the pipeline | Direct API deploys |
| Continuous (deployed state) | Manual changes and drift | The console change nobody logged |

Keep enforcement graduated. Introduce a rule in warn mode, publish the current
violation count, give teams a window to fix, then switch to blocking. A rule
that blocks on day one gets an exemption process built around it within a week,
and the exemptions become permanent.

Track exemptions as first-class objects: who approved, why, which control, and
an expiry date. An exemption without an expiry is a silently retired control.

### Drift Detection on Controls

Infrastructure drift is usually framed as a Terraform concern; the compliance
concern is narrower and sharper. You care specifically about changes that alter
whether a control is operating: encryption toggled off, a logging destination
removed, a policy loosened, a public access block disabled, an MFA requirement
relaxed, a retention period shortened.

Detect it by comparing declared state to observed state on a schedule, and by
watching the control-relevant events in the cloud audit trail directly. Every
drift event deserves a cause, and there are only three:

1. **A gap in enforcement** — the pipeline permitted it. Fix the policy rule.
2. **A bypass** — someone had a path around the pipeline. Fix the access model.
3. **An emergency change** — legitimate, but it must be reconciled back into
   code within a defined window, or the next apply silently reverts it and
   nobody learns anything.

Report drift as mean time to detect and mean time to correct per control. Those
two numbers say more about control effectiveness than a pass rate does, and they
are exactly what an auditor is trying to establish by other means.

For the underlying infrastructure practices this depends on, see
`iac-best-practices`.

### Automating Access Reviews

The periodic access review is the control most likely to exist as a signed
document with no operational reality behind it. Automate the whole cycle and it
becomes both cheaper and genuinely effective.

```
1. Reconcile daily
   identity provider grants ⋈ HR employment status ⋈ authorising ticket
   → exceptions: no HRIS record, terminated, no approval, unused 90+ days

2. Deprovision on the HR event, not on the review
   termination or role change → revoke within the same working day, logged

3. Generate the review per reviewer
   each manager or system owner receives only their own list, with
   last-used data and a deadline; no spreadsheet is emailed anywhere

4. Capture the decision
   keep / reduce / revoke, per grant, with reviewer identity and timestamp

5. Execute and verify the revocations
   automatically apply, then re-check that the grant is actually gone

6. Emit the evidence artifact
   reviewer, date, grants reviewed, decisions, revocations completed,
   exceptions outstanding with owners
```

Step 5 is the one teams omit and auditors test. A review that produced decisions
but no verified revocations demonstrates that the control does not work.

The strongest version removes standing privilege altogether: grant elevated
access just in time, time-boxed, tied to a ticket, and expiring automatically.
The review then covers a much smaller set of permanent grants, and the elevation
log is itself continuous evidence of approved, bounded, purposeful access.

### Audit-Log Integrity

Logs function as evidence only if their integrity is defensible. The relevant
question is not "do we have logs" but "could someone with production access have
altered them without detection".

- **Ship promptly off the originating host** so compromising the host does not
  compromise the record.
- **Write to append-only or write-once storage** with an enforced retention
  lock, in an account or project separate from the workloads being logged.
- **Deny deletion to everyone**, including administrators and the shipping
  identity itself. Retention expiry should be the only deletion path.
- **Verify integrity** with hashing or the platform's log validation, and check
  the verification on a schedule rather than assuming it.
- **Monitor the pipeline for gaps.** A silent stop is indistinguishable from a
  quiet period unless you alert on absence.
- **Alert on changes to logging configuration.** Disabling a trail, removing a
  destination, or shortening retention should page, because those are the first
  moves of both an attacker and an inconvenienced engineer.
- **Retain for the required period** and be able to demonstrate the retention
  setting, not merely the presence of old data.

### Coverage Reporting

Report two numbers together, always: what fraction of controls is automatically
monitored, and what fraction of monitored controls is passing. A dashboard
showing 100% passing across the 30% of controls that happen to be automated is
actively misleading — it directs attention away from the unexamined majority.

```
Controls total                          64
  Automated, continuously checked       41  (64%)
  Automated, scheduled only              9  (14%)
  Manual, evidenced                     11  (17%)
  Manual, unevidenced                    3  ( 5%)   <- highest priority

Of the 50 automated:  47 passing, 3 failing (2 with owners, 1 unassigned)
Open exemptions: 6   (2 expiring this month, 1 expired — escalated)
Mean time to correct drift, last 90 days: 4.2h
```

Use `compliance-assessment` to establish the control set, the framework
mapping, and the evidence expectations; automation is how those controls are
then kept honest between assessments.

## Common Anti-Patterns

❌ **Screenshots in a shared folder.** Undated, unattributable, unreproducible,
and always assembled in a panic.
✅ System-generated artifacts with provenance, written immutably on a schedule.

❌ **Collecting evidence only before fieldwork.** Sampling across the period
exposes the gap immediately.
✅ Collect from the moment the control starts operating.

❌ **Policies that live only in documents.** Nothing fails when reality
diverges.
✅ Encode the rule and put it in a gate that produces a record.

❌ **Enforcing only in CI.** Anything changed after deploy, or deployed around
the pipeline, is invisible.
✅ Enforce pre-merge, at admission, and continuously against deployed state.

❌ **Turning a new rule straight to blocking.** Teams build an exemption path
around it and the exemptions never expire.
✅ Warn, publish counts, give a window, then block.

❌ **Exemptions without expiry or owner.** A retired control that still looks
green.
✅ Every exemption has an approver, a rationale, and an expiry date.

❌ **Access reviews that record decisions but not revocations.** The decision was
never executed.
✅ Apply the revocations automatically and verify them afterwards.

❌ **Deprovisioning driven by the quarterly review.** A leaver keeps access for
up to three months.
✅ Drive deprovisioning from the HR event, same day.

❌ **Audit logs deletable by production administrators.** The people the log
observes can edit it.
✅ Separate account, append-only, retention-locked, deletion denied to all.

❌ **No alerting on logging configuration changes.** Disabling the trail is
step one of hiding anything.
✅ Page on trail modification, destination removal, or retention reduction.

❌ **Collectors that fail silently.** The absence of failures reads as success.
✅ Monitor the collectors themselves; alert on missing runs.

❌ **A green dashboard covering only what is automated.** It hides the risk it
was built to surface.
✅ Report coverage and pass rate together.

❌ **Findings with no owner.** They age forever and become background noise.
✅ Route every finding to an owning team with an SLA by severity.

## Compliance Automation Checklist

- [ ] Control set defined with owner, intent, and framework mapping
- [ ] Each control has an automated check where automation is feasible
- [ ] Check cadence chosen from the control's failure mode
- [ ] Manual-only controls explicitly listed and justified
- [ ] Evidence collectors versioned, reviewed, and scheduled like production code
- [ ] Collectors pull from authoritative system APIs
- [ ] Evidence artifacts dated, attributed, immutable, and reproducible
- [ ] Collector failures alert; missing runs are detected
- [ ] Evidence retention meets the required period
- [ ] Policy rules encoded and enforced pre-merge
- [ ] Same rules enforced at admission and continuously against deployed state
- [ ] New rules rolled out warn-first with a published violation count
- [ ] Exemptions tracked with approver, rationale, and expiry
- [ ] Drift detection covers control-relevant configuration
- [ ] Every drift event assigned a cause and a corrective action
- [ ] Mean time to detect and correct drift tracked per control
- [ ] Access reconciliation runs daily against the HR system
- [ ] Deprovisioning triggered by HR events, same day, and logged
- [ ] Access review decisions executed and the revocations verified
- [ ] Privileged access time-bound and just-in-time where feasible
- [ ] Audit logs in a separate account, append-only, retention-locked
- [ ] Deletion denied to administrators and to the shipping identity
- [ ] Log gaps and logging-configuration changes alert
- [ ] Coverage and pass rate reported together
- [ ] Every finding routed to an owning team with a severity-based SLA
