---
name: incident-timeline-creation
description: "**Server Logs:**"
---

# Incident Timeline Creation (Verbose)

## Timeline Reconstruction Process

### Step 1: Gather Data Sources

**Server Logs:**
```
2026-04-10 14:00:05 [ERROR] Connection pool exhausted (available: 0/350)
2026-04-10 14:00:07 [ERROR] Query timeout after 5000ms
2026-04-10 14:00:08 [ERROR] Database unavailable
```

**Metrics:**
- CPU: jumped from 30% to 90% at 14:00:05
- Memory: stable
- Database connections: 0 → 350 at 14:00:05
- Request latency: 50ms → 5000ms at 14:00:05

**Chat History:**
```
14:00:15 @oncall: "Hey, alerts coming in"
14:00:30 @oncall: "Restarting database"
14:05:00 @incident-commander: "Incident declared"
```

**Metrics Dashboard:**
- Alert fire time: 14:00:07
- Error rate spike: 14:00:05
- Recovery time: 14:07:30

### Step 2: Establish Definitive Timeline

Use server logs as source of truth (most accurate):

```
14:00:00 - [OBSERVATION] Deployment completed (from deployment system)
14:00:05 - [ROOT CAUSE] New query deployed with infinite loop
          (From logs: connection pool exhaustion starts)
14:00:07 - [METRIC CHANGE] Database unavailable
          (From metrics: error rate → 100%)
14:00:08 - [DETECTION] Alert fires
          (From monitoring: automated alert triggered)
14:00:15 - [HUMAN RESPONSE] On-call acknowledges
          (From chat: message timestamp)
14:00:30 - [MITIGATION] Kill infinite query / restart database
          (From chat: "Restarting database")
14:05:00 - [INCIDENT DECLARED] Severity: SEV1
          (From Slack: incident created)
14:07:30 - [RECOVERY] Service restored
          (From metrics: error rate drops to <0.1%)
14:10:00 - [RESOLUTION] All-clear sent
          (From Slack: "Service restored")
```

### Step 3: Calculate Critical Metrics

```
Total Incident Duration:
  Start: 14:00:00 (root cause begins)
  End: 14:07:30 (service restored)
  Duration: 7.5 minutes

Customer Impact Duration:
  Start: 14:00:07 (first error)
  End: 14:07:30 (service restored)
  Duration: 7.38 minutes

Detection Lag:
  Root cause: 14:00:05
  Alert fired: 14:00:08
  Lag: 3 seconds (excellent)

Response Lag:
  Alert: 14:00:08
  Human starts: 14:00:15
  Lag: 7 seconds (excellent)

Remediation Time:
  Start: 14:00:15
  Complete: 14:07:30
  Duration: 7.25 minutes
```

### Step 4: Identify Contributing Factors

```
What made this worse?
- No timeout on database queries
  → Connections never released
  → Pool exhausted in seconds
  
- No monitoring on connection pool
  → Didn't detect pool > 80%
  → Hit limit before alert

- No circuit breaker
  → Kept hammering database after pool exhausted
  → Made situation worse
```

### Step 5: Document Final Timeline

```markdown
# Incident #12345: Database Outage April 10, 2026

## Timeline

| Time | Event | Source | Impact |
|------|-------|--------|--------|
| 14:00:00 | Deployment: v1.5.0 | CD System | Root cause deployed |
| 14:00:05 | Connection pool exhausted | Logs | Service degraded |
| 14:00:07 | First 500 errors | Metrics | Users affected |
| 14:00:08 | Alert fires | Monitoring | Detection |
| 14:00:15 | On-call acknowledges | Chat | Response |
| 14:00:30 | Restart database | Chat | Remediation |
| 14:07:30 | Service restored | Metrics | Recovery |
| 14:10:00 | All-clear sent | Slack | Communication |

## Key Metrics

- Customer Impact: 7.38 minutes
- Detection Lag: 3 seconds
- Response Lag: 7 seconds
- Remediation Time: 7.25 minutes
- Total Incident Duration: 7.5 minutes
```

## Accuracy Checklist

- [ ] Sourced timestamps from logs, not memory
- [ ] Cross-referenced with multiple sources
- [ ] Verified with participants
- [ ] Calculated lag times correctly
- [ ] Identified all critical transition points
- [ ] Timeline reflects both system and human actions
- [ ] Root cause time vs detection time clear

## Common Timeline Mistakes

❌ Using participant memory → Inaccurate (+/- 10 minutes)  
✅ Use server logs/metrics → Accurate to seconds

❌ Mixing different time zones → Off by hours  
✅ Convert all to UTC/standard timezone

❌ Starting from alert, not root cause  
✅ Start from actual root cause (may be before alert)

❌ Only including human actions → Miss system behavior  
✅ Include metric changes, errors, and human actions
