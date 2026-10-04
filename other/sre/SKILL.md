---
name: sre
description: Site reliability engineering practices
license: MIT
compatibility: opencode
metadata:
  audience: devops-engineer, sre
  category: devops
---

## What I do

- Apply SRE principles to systems reliability
- Define and measure reliability metrics
- Implement monitoring and alerting
- Respond to incidents and outages
- Automate operational processes
- Conduct chaos engineering experiments

## When to use me

- When building reliable distributed systems
- When establishing reliability practices
- When managing production systems
- When responding to incidents
- When automating operations
- When measuring system health

## Key Concepts

### Error Budgets

```yaml
# Define error budget
slo:
  service: payment-api
  sli: availability
  target: 99.9%
  window: 30 days
  
# Error budget calculation
# 30 days * 24 hours * 60 minutes = 43,200 minutes
# 0.1% error budget = 43.2 minutes of allowed downtime

# Error budget alerts
- alert: ErrorBudgetWarning
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{service="payment-api"}[30d])) 
        - sum(rate(http_requests_total{service="payment-api",status=~"5.."}[30d]))
      ) / sum(rate(http_requests_total{service="payment-api"}[30d]))
    ) > 0.05
  for: 1h
```

### Incident Management

```python
# Incident response workflow
class IncidentManager:
    def __init__(self):
        self.escalation_levels = {
            0: ['team-slack'],
            1: ['team-slack', 'on-call'],
            2: ['team-slack', 'on-call', 'manager'],
            3: ['team-slack', 'on-call', 'manager', 'executive']
        }
        
    def create_incident(self, severity: int):
        incident = Incident(
            severity=severity,
            status='investigating',
            timeline=[TimelineEvent('Created', now())]
        )
        
        self.notify(incident, self.escalation_levels[severity])
        return incident
        
    def update_status(self, incident, status: str):
        incident.status = status
        incident.timeline.append(TimelineEvent(status, now()))
        
        if status == 'resolved':
            incident.duration = now() - incident.created_at
            self.schedule_postmortem(incident)
```

### Toil Analysis

```yaml
# Toil classification
toil_categories:
  manual_deployments:
    frequency: 10/week
    duration_minutes: 15
    toil_hours: 2.5/week
    
  data_cleanup:
    frequency: 5/week
    duration_minutes: 30
    toil_hours: 2.5/week
    
  certificate_renewal:
    frequency: 1/month
    duration_minutes: 60
    toil_hours: 1/month
    
# Total toil: ~5 hours/week
# Goal: Reduce to <2 hours/week via automation
```

### Service Health

```python
# Health check implementation
class ServiceHealth:
    def __init__(self):
        self.checks = []
        
    def register_check(self, name: str, check_fn):
        self.checks.append({'name': name, 'check': check_fn})
        
    async def get_health(self):
        results = []
        overall_healthy = True
        
        for check in self.checks:
            try:
                result = await check['check']()
                results.append({
                    'name': check['name'],
                    'healthy': result.healthy,
                    'details': result.details
                })
                if not result.healthy:
                    overall_healthy = False
            except Exception as e:
                results.append({
                    'name': check['name'],
                    'healthy': False,
                    'error': str(e)
                })
                overall_healthy = False
                
        return HealthStatus(healthy=overall_healthy, checks=results)
```

### Reliability Engineering

- **Blameless Postmortems**: Focus on system improvement
- **Proactive Reliability**: Build reliability in, don't add later
- **SLOs over SLAs**: Internal goals stricter than customer promises
- **Error Budgets**: Balance reliability with velocity
- **Reduce MTTR**: Focus on detection and response time
- **Capacity Planning**: Plan for growth

### Runbook Example

```yaml
# runbook: high-cpu-alert
name: High CPU Usage
severity: warning

description: |
  One or more instances have high CPU usage.

steps:
  - name: Identify affected instances
    command: |
      kubectl top nodes
      
  - name: Check for traffic spike
    command: |
      kubectl get pods --sort-by='.spec.containers[0].resources.limits.cpu'
      
  - name: Check for runaway processes
    command: |
      kubectl exec -it <pod> -- top
      
  - name: Scale horizontally if needed
    command: |
      kubectl scale deployment <name> --replicas=5
      
  - name: Check HPA if enabled
    command: |
      kubectl get hpa
```

### Key SRE Practices

1. **Define SLIs**: What matters to users
2. **Set SLOs**: Target reliability levels
3. **Monitor SLIs**: Measure continuously
4. **Alert on SLO Burn**: Proactive warnings
5. **Review Incidents**: Blameless postmortems
6. **Automate**: Reduce toil continuously
