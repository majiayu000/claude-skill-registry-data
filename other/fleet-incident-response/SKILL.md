---
name: fleet-incident-response
description: How DevSecOps handles security incidents — triage, containment, assessment, remediation. Not just scanning — responding when something is actually found.
---

# Incident Response — DevSecOps Crisis Skill

Scanning finds problems. Incident response HANDLES them. When your nightly dependency scan finds a critical CVE, or your secret scan detects exposed credentials, this skill defines what happens next.

## Incident Severity Classification

| Severity | Criteria | Response Time | Example |
|----------|----------|--------------|---------|
| CRITICAL | Active exploitation possible, data exposure imminent | Immediate — drop everything | Exposed API keys in committed code, RCE in production dep |
| HIGH | Significant vulnerability, no active exploitation | Same cycle — before next heartbeat | Auth bypass in dependency, SQL injection in code |
| MEDIUM | Vulnerability exists, exploitation requires specific conditions | Next sprint — create task | XSS in admin panel (low traffic), DoS in dev dependency |
| LOW | Theoretical risk, mitigated by other controls | Backlog — track and monitor | Outdated dev dependency, informational finding |

## The Response Protocol

### Step 1: Triage (Minutes)

When a finding is detected (CRON result, manual scan, or alert from another agent):

1. **Classify severity** using the table above
2. **Determine scope** — which projects? which components? which agents' work?
3. **Check for active exploitation** — is this theoretical or are there signs of abuse?

For CRITICAL: skip to Step 2 immediately. For others: document finding, proceed methodically.

### Step 2: Containment (CRITICAL/HIGH only)

**Set security_hold** on affected tasks:
```
fleet_alert(severity="critical", category="security",
    title="CVE-XXXX in {dependency}",
    details="RCE via {mechanism}. Affected: {components}")
```
This automatically: sets security_hold custom field, alerts IRC, ntfy to PO.

**Block affected work:**
- Tasks touching the affected component should NOT be approved
- `fleet_chat("Security hold on tasks touching {component}. Do not approve until cleared.", mention="fleet-ops")`

**Do NOT fix yet** — containment is about stopping the bleeding, not surgery.

### Step 3: Assessment

Produce a `vulnerability_report` artifact:
```
fleet_artifact_create("vulnerability_report", "Incident: {title}")
```

Document:
- **What:** Exact finding, CVE if applicable, affected version
- **Where:** Which files, which dependencies, which configs
- **Impact:** What could an attacker do? What data is at risk?
- **Scope:** All affected tasks, agents, deployments
- **Evidence:** Scan output, code references, reproduction steps

Use `/fleet-vulnerability-assessment` for structured classification.

### Step 4: Remediation

Create fix tasks — do NOT fix inline. Fixes need their own trail.

```
fleet_task_create(
    title="Fix: CVE-XXXX in {dependency}",
    agent_name="software-engineer",  # or devops for infra
    task_type="task",
    priority="urgent",
    description="Security incident remediation. See vulnerability_report artifact."
)
```

For dependency updates: specify the exact version to pin to.
For code fixes: specify the exact pattern to eliminate.

### Step 5: Verification

After the fix is implemented:
1. Re-run the scan that found the issue — does it pass now?
2. Verify the fix doesn't introduce new issues
3. Clear the security_hold: update task custom field
4. Notify fleet-ops: `fleet_chat("Security hold cleared for {component}. Fix verified.", mention="fleet-ops")`

### Step 6: Post-Incident

Post incident report to board memory: `[security, incident, postmortem]`

```
## Security Incident Report
Date: {date}
Severity: {level}
Finding: {description}
Impact: {what was at risk}
Containment: {what was blocked}
Remediation: {what was fixed, by whom}
Verification: {scan results after fix}
Prevention: {what would prevent recurrence}
```

## Escalation Rules

| Condition | Action |
|-----------|--------|
| CRITICAL finding | `fleet_escalate()` + `fleet_notify_human()` — PO must know immediately |
| Security hold blocks sprint completion | `fleet_chat(mention="project-manager")` — PM adjusts sprint |
| Fix requires architecture change | `fleet_chat(mention="architect")` — architect provides design |
| Finding in production-phase code | All gates blocked until fix verified |

## What Incident Response is NOT

- NOT a code review (fleet-ops reviews code quality)
- NOT a vulnerability scan (that's your CRONs and sec_* group calls)
- NOT a policy document (you respond, accountability reports compliance)

This is the RESPONSE when scanning finds something real. Scan → Triage → Contain → Assess → Remediate → Verify → Report.
