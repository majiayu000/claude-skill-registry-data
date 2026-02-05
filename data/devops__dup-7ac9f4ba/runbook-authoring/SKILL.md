---
name: runbook-authoring
description: Author operational runbooks for incident response and troubleshooting
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Runbook Authoring Skill

## When to Use This Skill

Use this skill when:

- **Runbook Authoring tasks** - Working on author operational runbooks for incident response and troubleshooting
- **Planning or design** - Need guidance on Runbook Authoring approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create operational runbooks for incident response and troubleshooting.

## MANDATORY: Documentation-First Approach

Before authoring runbooks:

1. **Invoke `docs-management` skill** for runbook patterns
2. **Verify SRE practices** via MCP servers (perplexity)
3. **Base guidance on operational best practices**

## Runbook Purpose

```text
RUNBOOK GOALS:

┌─────────────────────────────────────────────────────────────────┐
│                    WHY RUNBOOKS?                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  REDUCE MTTR (Mean Time To Recovery)                             │
│  ├── Pre-documented steps save diagnosis time                    │
│  ├── No need to figure it out during incident                    │
│  └── Consistent approach every time                              │
│                                                                  │
│  ENABLE ANYONE TO RESPOND                                        │
│  ├── On-call doesn't need to be expert                           │
│  ├── Knowledge transfer from senior to junior                    │
│  ├── Reduces bus factor                                          │
│  └── New team members can respond effectively                    │
│                                                                  │
│  DOCUMENT TRIBAL KNOWLEDGE                                       │
│  ├── Capture what experts know                                   │
│  ├── Make implicit knowledge explicit                            │
│  └── Preserve knowledge when people leave                        │
│                                                                  │
│  IMPROVE OVER TIME                                               │
│  ├── Each incident improves the runbook                          │
│  ├── Capture new failure modes                                   │
│  └── Evolve with the system                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Runbook Types

```text
RUNBOOK CATEGORIES:

ALERT RUNBOOKS:
┌─────────────────────────────────────────────────────────────────┐
│ One runbook per alert                                            │
│                                                                  │
│ Purpose: What to do when this specific alert fires               │
│ Linked from: Alert annotations                                   │
│ Contains: Triage, diagnosis, remediation for this alert          │
└─────────────────────────────────────────────────────────────────┘

SYMPTOM RUNBOOKS:
┌─────────────────────────────────────────────────────────────────┐
│ One runbook per symptom/problem                                  │
│                                                                  │
│ Purpose: How to diagnose/fix a type of problem                   │
│ Examples: "High Latency", "Out of Memory", "Connection Errors"   │
│ Contains: Decision tree for multiple potential causes            │
└─────────────────────────────────────────────────────────────────┘

PROCEDURE RUNBOOKS:
┌─────────────────────────────────────────────────────────────────┐
│ One runbook per operational procedure                            │
│                                                                  │
│ Purpose: How to perform maintenance tasks                        │
│ Examples: "Database Failover", "Certificate Rotation"            │
│ Contains: Step-by-step procedures                                │
└─────────────────────────────────────────────────────────────────┘

SERVICE RUNBOOKS:
┌─────────────────────────────────────────────────────────────────┐
│ One runbook per service                                          │
│                                                                  │
│ Purpose: Service overview and common operations                  │
│ Contains: Architecture, dependencies, common issues              │
└─────────────────────────────────────────────────────────────────┘
```

## Runbook Structure

```text
RUNBOOK ANATOMY:

┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                           │
│ ├── Title, service, last updated                                 │
│ ├── Alert link (if alert runbook)                                │
│ └── Quick summary                                                │
├─────────────────────────────────────────────────────────────────┤
│ OVERVIEW                                                         │
│ ├── What this runbook covers                                     │
│ ├── When to use it                                               │
│ └── Expected outcome                                             │
├─────────────────────────────────────────────────────────────────┤
│ QUICK ACTIONS (Optimize for speed)                               │
│ ├── 2-3 most common fixes                                        │
│ ├── Copy-paste commands                                          │
│ └── "Try these first" section                                    │
├─────────────────────────────────────────────────────────────────┤
│ DIAGNOSIS                                                        │
│ ├── How to verify the problem                                    │
│ ├── Key metrics/logs to check                                    │
│ ├── Decision tree for root cause                                 │
│ └── Common causes and indicators                                 │
├─────────────────────────────────────────────────────────────────┤
│ REMEDIATION                                                      │
│ ├── Step-by-step fix for each cause                              │
│ ├── Rollback procedures                                          │
│ └── Verification steps                                           │
├─────────────────────────────────────────────────────────────────┤
│ ESCALATION                                                       │
│ ├── When to escalate                                             │
│ ├── Who to contact                                               │
│ └── What information to provide                                  │
├─────────────────────────────────────────────────────────────────┤
│ REFERENCES                                                       │
│ ├── Related dashboards                                           │
│ ├── Architecture docs                                            │
│ └── Related runbooks                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Alert Runbook Template

```markdown
# Runbook: {Alert Name}

**Service:** {Service Name}
**Alert:** {Alert Name}
**Severity:** {P1/P2/P3/P4}
**Owner:** {Team/Person}

---

## Overview

**What this alert means:**
{One sentence explanation of what triggered this alert}

**User impact:**
{How users are affected when this fires}

**Expected resolution time:**
{Typical time to resolve}

---

## Quick Actions

> **Try these first before deep diagnosis**

### 1. Check if it's a known issue

```bash
# Check recent incidents
open https://status.example.com

# Check deployment history
kubectl rollout history deployment/orders-api -n production
```

### 2. Quick restart (if safe)

```bash
# Rolling restart (no downtime)
kubectl rollout restart deployment/orders-api -n production

# Wait for rollout
kubectl rollout status deployment/orders-api -n production
```

### 3. Rollback recent deployment

```bash
# Rollback to previous version
kubectl rollout undo deployment/orders-api -n production
```

---

## Diagnosis

### Step 1: Verify the alert is real

```bash
# Check current metric value
curl -s 'http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])' | jq
```

**Dashboard:** [Grafana - Orders API Overview]({link})

### Step 2: Identify the scope

| Check | Command/Action |
|-------|----------------|
| All pods affected? | `kubectl get pods -n production -l app=orders-api` |
| All endpoints? | Check per-endpoint error rate in Grafana |
| Started when? | Check Grafana annotations for deployments |

### Step 3: Determine root cause

```text
DECISION TREE:

Is it all pods or specific pods?
├── All pods → Likely code/config issue
│   ├── Recent deployment? → Rollback
│   └── No deployment? → Check dependencies
│
└── Specific pods → Likely infrastructure issue
    ├── Same node? → Node issue
    └── Random? → Check pod logs
```

### Common Causes

| Cause | Indicators | Solution |
|-------|------------|----------|
| Bad deployment | Errors started after deploy | Rollback |
| Database issues | Connection errors in logs | Check DB |
| Memory pressure | OOMKilled pods | Scale up or fix leak |
| Dependency down | Timeout errors | Check dependency status |

---

## Remediation

### Cause 1: Bad Deployment

**Indicators:**

- Errors started immediately after deployment
- New error types appearing

**Fix:**

```bash
# 1. Rollback to previous version
kubectl rollout undo deployment/orders-api -n production

# 2. Verify rollback
kubectl rollout status deployment/orders-api -n production

# 3. Check error rate dropping
watch -n5 'curl -s "http://prometheus:9090/..." | jq'
```

**Verification:**

- [ ] Error rate returning to normal
- [ ] No new 5xx errors in logs
- [ ] Alert auto-resolves

### Cause 2: Database Connection Issues

**Indicators:**

- "Connection refused" or "Connection timeout" in logs
- Database metrics showing high connections

**Fix:**

```bash
# 1. Check database status
psql -h db.example.com -U admin -c "SELECT count(*) FROM pg_stat_activity"

# 2. If connection pool exhausted, restart pods
kubectl rollout restart deployment/orders-api -n production

# 3. If database is down, escalate to DBA
```

### Cause 3: Memory Pressure

**Indicators:**

- OOMKilled in pod events
- Memory usage climbing before crash

**Fix:**

```bash
# 1. Check for OOMKilled
kubectl get events -n production --field-selector reason=OOMKilled

# 2. Increase memory limit temporarily
kubectl set resources deployment/orders-api -n production \
  --limits=memory=2Gi

# 3. File ticket for memory leak investigation
```

---

## Escalation

### When to escalate

- [ ] Quick actions didn't resolve
- [ ] Root cause unclear after 15 minutes
- [ ] Data loss or corruption suspected
- [ ] Multiple services affected

### Who to contact

| Situation | Contact | Method |
|-----------|---------|--------|
| Database issues | DBA on-call | PagerDuty: dba-oncall |
| Network issues | Platform team | Slack: #platform-oncall |
| Security concern | Security team | PagerDuty: security |
| Unknown | Engineering Manager | Phone: XXX-XXX-XXXX |

### Information to provide

When escalating, include:

- Alert name and time started
- Actions already taken
- Current hypothesis
- Link to incident channel

---

## References

- **Dashboard:** [Grafana - Orders API]({link})
- **Logs:** [Kibana - Orders API Errors]({link})
- **Architecture:** [Confluence - Orders API Design]({link})
- **Related Runbooks:**
  - [Database Connection Issues]({link})
  - [High Latency Troubleshooting]({link})

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2024-01-15 | Added memory pressure section | @engineer |
| 2024-01-01 | Initial version | @oncall |

```text

```

## Procedure Runbook Template

```markdown
# Procedure: {Procedure Name}

**Purpose:** {What this procedure accomplishes}
**When to use:** {Circumstances requiring this procedure}
**Duration:** {Expected time to complete}
**Risk Level:** {Low/Medium/High}

---

## Prerequisites

- [ ] Access to production Kubernetes cluster
- [ ] Database admin credentials
- [ ] Approval from {approver} if during business hours

## Pre-Flight Checks

```bash
# Verify you have correct access
kubectl auth can-i '*' '*' -n production

# Check current system state
kubectl get pods -n production

# Confirm no ongoing incidents
open https://status.example.com
```

---

## Procedure Steps

### Step 1: {First Step Title}

**Purpose:** {Why this step}

```bash
# Commands to execute
{command}
```

**Expected output:**

```text
{expected output}
```

**Verification:**

- [ ] {Check to confirm step succeeded}

### Step 2: {Second Step Title}

**Purpose:** {Why this step}

```bash
{command}
```

**Expected output:**

```text
{expected output}
```

**Verification:**

- [ ] {Check to confirm step succeeded}

### Step 3: {Third Step Title}

...

---

## Rollback Procedure

If something goes wrong, follow these steps to restore previous state:

### Step 1: {Rollback Step}

```bash
{rollback command}
```

### Step 2: {Verify Rollback}

```bash
{verification command}
```

---

## Post-Procedure Verification

- [ ] Service is healthy (check dashboard)
- [ ] No new errors in logs
- [ ] Dependent services unaffected
- [ ] Monitoring shows expected state

## Cleanup

```bash
# Remove temporary resources
{cleanup commands}
```

---

## Troubleshooting

### Issue: {Common Issue 1}

**Symptom:** {What you see}
**Cause:** {Why it happens}
**Solution:** {How to fix}

### Issue: {Common Issue 2}

...

---

## Template References

- {Related documentation}
- {Architecture diagrams}

```text

```

## Runbook Quality Checklist

```markdown
# Runbook Quality Checklist

## Structure
- [ ] Clear title and service identification
- [ ] Last updated date is recent
- [ ] Owner/team identified
- [ ] Severity/risk level stated

## Quick Actions
- [ ] 2-3 most common fixes at the top
- [ ] Commands are copy-paste ready
- [ ] No unnecessary explanation before actions

## Diagnosis
- [ ] Decision tree for root cause
- [ ] Key metrics/logs to check
- [ ] Links to dashboards
- [ ] Common causes listed

## Remediation
- [ ] Step-by-step for each cause
- [ ] Verification after each fix
- [ ] Rollback procedures included
- [ ] Commands are tested and work

## Escalation
- [ ] Clear escalation criteria
- [ ] Contact information current
- [ ] Information to provide when escalating

## Usability
- [ ] Can be followed at 3am under stress
- [ ] No jargon without explanation
- [ ] Links are not broken
- [ ] Screenshots where helpful
```

## Workflow

When authoring runbooks:

1. **Start from Incidents**: Create runbooks after incidents
2. **Optimize for Speed**: Quick actions first
3. **Include Commands**: Copy-paste ready
4. **Add Decision Trees**: Help diagnose root cause
5. **Define Escalation**: When and who
6. **Test Regularly**: Verify runbooks work
7. **Update After Incidents**: Improve based on learnings

## Further Reading

For detailed guidance:

---

**Last Updated:** 2025-12-26
