---
name: Incident Response
description: Emergency response workflow for production issues
---

# Incident Response Skill

## Overview

Emergency workflow for handling production incidents with **DevOps Engineer** and **Observability Expert**.

**Duration:** Variable (15 minutes - 2 hours)
**Personas Required:** DevOps, Observability

## Incident Workflow

### Phase 1: Detect (@observability-expert)

**Actions:**
1. Receive alert from monitoring
2. Check Grafana dashboards
3. Query Prometheus for metrics
4. Assess impact and severity

### Phase 2: Investigate (@devops-engineer + @observability-expert)

**Actions:**
1. Review recent deployments
2. Check application logs
3. Analyze distributed traces
4. Identify root cause

### Phase 3: Mitigate (@devops-engineer)

**Actions:**
1. Rollback deployment if needed
2. Scale resources if capacity issue
3. Apply hotfix if minor bug
4. Notify stakeholders

### Phase 4: Resolve (@devops-engineer)

**Actions:**
1. Verify metrics return to normal
2. Close alerts
3. Monitor for 30 minutes
4. Document actions

### Phase 5: Postmortem (@observability-expert)

**Actions:**
1. Write incident report in Logseq
2. Identify preventive measures
3. Update runbooks
4. Share learnings with team

## Success Criteria

- ✅ Incident detected <5 minutes
- ✅ Response initiated <10 minutes
- ✅ Service restored <1 hour
- ✅ Postmortem complete <24 hours
- ✅ Preventive measures implemented
