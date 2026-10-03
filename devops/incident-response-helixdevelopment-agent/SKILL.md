---
name: incident-response
description: Manage and respond to production incidents effectively. Establish on-call rotations, runbooks, and post-mortem processes.
triggers:
- /incident
- /oncall
- /postmortem
---

# Incident Management

This skill covers effective incident response including detection, communication, resolution, and post-incident analysis to minimize downtime and improve reliability.

## When to use this skill

Use this skill when you need to:
- Respond to production incidents
- Set up incident management processes
- Create on-call rotations
- Write runbooks for common issues
- Conduct post-mortems

## Prerequisites

- Incident management tool (PagerDuty, Opsgenie, VictorOps)
- Communication channels (Slack, Teams, Zoom)
- Monitoring and alerting setup
- Documentation system for runbooks
- Post-mortem template

## Guidelines

### Incident Lifecycle

```
Detection → Triage → Mitigation → Resolution → Post-Incident
    ↓          ↓          ↓            ↓            ↓
 Alerting   Assess     Stop the    Fix root    Learn &
  System    impact     bleeding    cause       improve
```

### Detection

**Alert Sources**
- Monitoring alerts (high error rate, latency)
- Customer reports
- Automated health checks
- Synthetic monitoring failures

**Severity Levels**
- **SEV 1**: Critical - Complete outage, data loss
- **SEV 2**: High - Major functionality impaired
- **SEV 3**: Medium - Partial degradation
- **SEV 4**: Low - Minor issues, workarounds exist

### Triage

**Initial Assessment**
1. Acknowledge the alert
2. Assess scope and impact
3. Determine severity
4. Create incident channel/document
5. Notify stakeholders

**Triage Questions**
- What is affected? (services, regions, customers)
- When did it start?
- What changed recently? (deployments, config)
- Is there a workaround?

**Communication**
```
Incident #1234 - Payment Service Degraded

Status: Investigating
Severity: SEV 2
Impact: 50% of payment requests failing
Started: 2024-01-15 14:30 UTC

Updates: #incident-1234 (Slack)
```

### Mitigation

**Priorities**
1. Stop the bleeding (mitigate impact)
2. Restore service (short-term fix)
3. Fix root cause (long-term fix)

**Mitigation Strategies**
- Rollback recent deployments
- Enable feature flags to disable affected features
- Scale up resources
- Failover to standby systems
- Use cached data instead of live queries

**Runbook-Driven Response**
```markdown
# Database Connection Pool Exhausted

## Symptoms
- Error: "Too many connections"
- High response times
- Connection timeouts

## Checks
1. Check active connections: `SELECT count(*) FROM pg_stat_activity;`
2. Check connection pool metrics in dashboard

## Mitigation
1. Restart application to reset connection pool
2. Scale up database connection limit temporarily
3. Enable connection pooling (PgBouncer)

## Verification
- Monitor connection count
- Check error rates
- Confirm response times normalizing
```

### Resolution

**Root Cause Analysis**
- Collect logs and metrics
- Identify trigger (deployment, config change, traffic spike)
- Trace code path that caused issue
- Reproduce in non-production if possible

**Fix Implementation**
- Test fix in staging
- Deploy with monitoring
- Verify resolution
- Update runbooks if new issue type

### Post-Incident Review

**Timeline Construction**
```
14:30 - Deployment #5678 to production
14:35 - Error rate alerts triggered
14:40 - Incident declared, rollback initiated
14:45 - Service restored
15:00 - Root cause identified (missing database index)
```

**Post-Mortem Template**
```markdown
# Post-Mortem: Incident #1234

## Summary
Payment service degraded due to missing database index after schema migration.

## Timeline
[Detailed timeline of events]

## Root Cause
Database query performance degraded after adding new column without index.

## Impact
- 50% payment failure rate
- ~$50K revenue impact
- 200 affected customers

## Lessons Learned
- Schema migrations need performance testing
- Missing index detection in CI/CD

## Action Items
| Task | Owner | Due |
|------|-------|-----|
| Add index monitoring | @alice | 2024-01-22 |
| Update migration checklist | @bob | 2024-01-20 |
```

**Blameless Culture**
- Focus on systems, not individuals
- Assume good intent
- Share learnings widely
- Track action items to completion

### On-Call Best Practices

**Rotation Design**
- Primary and secondary responders
- Follow-the-sun for global teams
- Limit consecutive shifts (max 7 days)
- Compensate for off-hours work

**Handoff Process**
- Document ongoing issues
- Transfer context about alerts
- Review recent changes
- Share relevant runbooks

**Preparation**
- Ensure laptop is setup and charged
- Have VPN access tested
- Keep phone charged with alerts enabled
- Have escalation contacts ready

### Tools and Automation

**Incident Management**
- PagerDuty, Opsgenie, VictorOps for alerting
- Status page (Statuspage.io) for external communication
- Incident.io for modern incident management

**Automation**
- Auto-remediation for known issues
- Automated runbook execution
- Self-healing systems where possible
- ChatOps for common tasks

## Examples

See the `examples/` directory for:
- `runbooks/` - Common issue runbooks
- `postmortem-template.md` - Post-mortem template
- `incident-response-playbook.md` - Response procedures
- `oncall-checklist.md` - On-call preparation checklist

## References

- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)
- [Blameless Postmortems](https://codeascraft.com/2012/05/22/blameless-postmortems/)
