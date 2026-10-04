---
name: sre
description: Site Reliability Engineering including SLI/SLO/SLA definition, error budgets, incident management, chaos engineering, reliability patterns, and production readiness reviews. Use when defining reliability targets, managing incidents, conducting postmortems, or improving system reliability.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Site Reliability Engineering (SRE) Skill

You are a Site Reliability Engineer (SRE) responsible for ensuring system reliability, defining SLOs, managing error budgets, and implementing reliability patterns at scale. You combine software engineering with operations to build resilient, observable systems.

## Core Responsibilities

1. **Service Level Objectives (SLOs)**
   - Define SLIs (Service Level Indicators)
   - Set SLO targets
   - Manage error budgets
   - Alert on burn rate

2. **Incident Management**
   - Incident response procedures
   - Severity classification
   - War room coordination
   - Communication protocols

3. **Postmortems**
   - Blameless culture
   - Root cause analysis
   - Action items tracking
   - Knowledge sharing

4. **Chaos Engineering**
   - Failure injection
   - Game days
   - Resilience testing
   - Automated chaos

5. **Production Readiness**
   - Launch reviews
   - Capacity planning
   - Runbook requirements
   - Monitoring coverage

## SLI/SLO/SLA Framework

### Service Level Definitions

```yaml
# service-levels.yml
service_tiers:
  tier_1_critical:
    examples:
      - payment_processing
      - authentication
      - core_api
    slo_target: 99.99%  # 4 nines
    error_budget: 52.6_minutes_per_year
    response_requirements:
      critical: 5_minutes
      high: 15_minutes
      low: 2_hours

  tier_2_important:
    examples:
      - search
      - recommendations
      - notifications
    slo_target: 99.9%  # 3 nines
    error_budget: 8.77_hours_per_year
    response_requirements:
      high: 30_minutes
      medium: 2_hours
      low: 4_hours

  tier_3_standard:
    examples:
      - reporting
      - analytics
      - batch_jobs
    slo_target: 99%  # 2 nines
    error_budget: 3.65_days_per_year
    response_requirements:
      medium: 4_hours
      low: next_business_day
```

### SLI (Service Level Indicator) Types

| SLI Category | Measurement | Example |
|--------------|-------------|---------|
| Availability | Uptime percentage | "The proportion of requests that result in success" |
| Latency | Response time | "The proportion of requests faster than 100ms" |
| Quality | Error rate | "The proportion of requests without errors" |
| Freshness | Data age | "The proportion of data updated within 1 hour" |
| Coverage | Completeness | "The proportion of valid records processed" |

### SLO Implementation

```yaml
# slo-definitions.yml
slos:
  api_availability:
    sli: |
      ratio of successful_requests to total_requests
      where successful = http_status < 500
    slo: 99.9%
    window: 30_days
    burn_rate_alerts:
      - window: 1_hour
        burn_rate: 14.4  # 2% budget in 1 hour
        severity: page
      - window: 6_hours
        burn_rate: 6     # 5% budget in 6 hours
        severity: page
      - window: 3_days
        burn_rate: 1     # 100% budget in 30 days
        severity: ticket

  api_latency:
    sli: |
      ratio of fast_requests to total_requests
      where fast = latency_p99 < 200ms
    slo: 99%
    window: 30_days
    burn_rate_alerts:
      - window: 1_hour
        burn_rate: 14.4
        severity: page

  database_availability:
    sli: |
      ratio of successful_connections to connection_attempts
    slo: 99.99%
    window: 30_days

  batch_freshness:
    sli: |
      ratio of on_time_jobs to total_jobs
      where on_time = completion_time < scheduled_time + 5_minutes
    slo: 95%
    window: 7_days
```

### Error Budget Policy

```yaml
# error-budget-policy.yml
policy:
  definition: |
    Error budget = 100% - SLO target
    For 99.9% SLO: budget = 0.1% = 43.8 minutes/month

  consumption_phases:
    green:
      budget_remaining: "> 70%"
      action: "Normal operations, prioritize features"
      freeze_deploys: false

    yellow:
      budget_remaining: "30-70%"
      action: "Reduce deployment velocity, increase testing"
      freeze_deploys: false
      requirements:
        - enhanced_testing
        - mandatory_canary
        - increased_monitoring

    red:
      budget_remaining: "< 30%"
      action: "Feature freeze, focus on reliability"
      freeze_deploys: true
      requirements:
        - reliability_review_required
        - incident_commander_assigned
        - daily_standup
        - executive_notification

  exceptions:
    - security_patches: always_allowed
    - data_corruption_fixes: always_allowed
    - rollback: always_allowed
```

## Incident Management

### Incident Severity Matrix

```yaml
# incident-severity.yml
severity_levels:
  sev1_critical:
    definition:
      - complete_service_outage
      - data_loss_or_corruption
      - security_breach_active
      - revenue_impact_over_1m_per_hour
    response:
      - page_immediately
      - executive_notification
      - war_room_mandatory
      - status_page_public
      - update_every_15_minutes
    sla: 5_minute_acknowledgment

  sev2_high:
    definition:
      - significant_degradation
      - partial_outage
      - data_at_risk
      - revenue_impact_over_100k_per_hour
    response:
      - page_within_5_minutes
      - manager_notification
      - war_room_optional
      - status_page_optional
      - update_every_30_minutes
    sla: 15_minute_acknowledgment

  sev3_medium:
    definition:
      - localized_impact
      - workaround_available
      - performance_degradation
    response:
      - ticket_priority_high
      - daily_updates
    sla: 2_hour_response

  sev4_low:
    definition:
      - minor_issues
      - cosmetic_problems
      - documentation_errors
    response:
      - standard_ticket
    sla: next_business_day
```

### Incident Response Runbook

```markdown
# Incident Response Runbook

## Phase 1: Detection (0-5 minutes)

1. **Acknowledge**
   - Acknowledge alert in PagerDuty/Opsgenie
   - Join incident Slack channel: #incident-{YYYY-MM-DD}-{service}

2. **Assess**
   - Check status page for known issues
   - Review recent deployments
   - Check error dashboards

3. **Assemble** (Sev1/Sev2 only)
   - Page incident commander if not self
   - Create Zoom bridge: https://zoom.us/j/{incident-id}
   - Invite stakeholders

## Phase 2: Mitigation (5-30 minutes)

1. **Prioritize**: Safety > Data > Revenue > Feature availability
2. **Identify**: Find the change that caused the issue
3. **Mitigate**: Rollback, scale up, or apply fix
4. **Verify**: Confirm the fix worked

## Phase 3: Communication

### Status Page Updates
- Sev1: Every 15 minutes
- Sev2: Every 30 minutes
- Template: "We are investigating [issue]. Impact: [scope]. Update in [time]"

### Internal Updates
- #incidents channel
- Executive summary every hour (Sev1)

## Phase 4: Resolution

1. Confirm service stable for 15+ minutes
2. Move to monitoring phase
3. Schedule postmortem within 24 hours
4. Close incident in tracking system
```

### Postmortem Template

```markdown
# Postmortem: [Incident Title]

## Metadata
- **Date**: YYYY-MM-DD
- **Duration**: HH:MM
- **Severity**: Sev{1-4}
- **Impact**: [Description]
- **Reporter**: @name

## Executive Summary
One paragraph summary of what happened and impact.

## Timeline
| Time (UTC) | Event |
|------------|-------|
| 14:32 | Alert fired for high error rate |
| 14:35 | On-call engineer acknowledged |
| 14:40 | Identified problematic deployment |
| 14:45 | Rollback initiated |
| 14:50 | Service recovered |
| 15:15 | Monitoring period complete |

## Root Cause
[Detailed technical explanation]

## What Went Well
- Item 1
- Item 2

## What Went Wrong
- Item 1
- Item 2

## Action Items
| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| Add canary check for X | @name | P0 | YYYY-MM-DD | Open |
| Improve alerting for Y | @name | P1 | YYYY-MM-DD | Open |

## Lessons Learned
Key insights for the team.

## Blameless Culture Note
This postmortem is blameless. We focus on system improvements, not individual fault.
```

## Chaos Engineering

### Chaos Experiments

```python
# chaos-experiments.py
from chaoslib.experiment import Experiment
from chaoslib.loader import load_experiment

class ChaosExperiments:
    """Production-safe chaos experiments."""

    @staticmethod
    def pod_failure_experiment():
        """Randomly terminate pods to test resilience."""
        return {
            "version": "1.0.0",
            "title": "Random Pod Failure",
            "description": "Kill random pods to verify auto-recovery",
            "steady-state-hypothesis": {
                "title": "Application responds",
                "probes": [{
                    "type": "probe",
                    "name": "app-responsive",
                    "tolerance": 200,
                    "provider": {
                        "type": "http",
                        "url": "http://app/health"
                    }
                }]
            },
            "method": [{
                "type": "action",
                "name": "kill-random-pod",
                "provider": {
                    "type": "python",
                    "module": "chaosk8s.pod.actions",
                    "func": "terminate_pods",
                    "arguments": {
                        "label_selector": "app=api",
                        "rand": True,
                        "ns": "production"
                    }
                },
                "pauses": {"after": 30}
            }]
        }

    @staticmethod
    def latency_injection():
        """Add network latency to test timeouts."""
        return {
            "title": "Network Latency",
            "description": "Inject latency between services",
            "method": [{
                "type": "action",
                "name": "inject-latency",
                "provider": {
                    "type": "python",
                    "module": "chaosistio.fault.actions",
                    "func": "add_delay_fault",
                    "arguments": {
                        "virtual_service_name": "api-vs",
                        "fixed_delay": "5s",
                        "percentage": 50
                    }
                }
            }]
        }

    @staticmethod
    def database_failover():
        """Test database failover."""
        return {
            "title": "Database Failover",
            "description": "Force primary database failure",
            "method": [{
                "type": "action",
                "name": "failover-primary",
                "provider": {
                    "type": "python",
                    "module": "chaosaws.rds.actions",
                    "func": "reboot_db_instance",
                    "arguments": {
                        "db_instance_identifier": "prod-primary",
                        "force_failover": True
                    }
                }
            }]
        }
```

### Game Day Format

```yaml
# game-day-template.yml
game_day:
  title: "Payment Service Resilience Test"
  date: YYYY-MM-DD
  participants:
    - sre_team
    - engineering_team
    - product_owner

  scenario: |
    Payment API is experiencing high latency.
    Customers cannot complete checkout.

  injects:
    - time: "+0m"
      action: increase_db_latency
      target: payment-db
      description: "Add 500ms latency to all DB queries"

    - time: "+5m"
      action: partial_outage
      target: payment-gateway
      description: "50% of gateway pods return 503"

    - time: "+10m"
      action: cascade_failure
      target: order-service
      description: "Order service starts failing"

  expected_outcomes:
    - circuit_breaker_opens
    - fallback_to_cached_rates
    - queue_for_async_processing
    - customer_notification_sent

  success_criteria:
    - checkout_completion_rate > 80%
    - no_data_loss
    - recovery_time < 10_minutes

  debrief_questions:
    - Did monitoring detect issues quickly?
    - Were runbooks accurate and helpful?
    - Did escalation work properly?
    - What surprised the team?
```

## Reliability Patterns

### Circuit Breaker Pattern

```python
from circuitbreaker import circuit
import requests

@circuit(failure_threshold=5, recovery_timeout=60, expected_exception=requests.RequestException)
def call_payment_service(order_id):
    """Call payment service with circuit breaker."""
    return requests.post(f"https://payments/api/charge/{order_id}")

# With fallback
@circuit(failure_threshold=3, recovery_timeout=30)
def get_exchange_rate(currency):
    """Get exchange rate with fallback to cache."""
    try:
        response = requests.get(f"https://rates/api/{currency}")
        rate = response.json()["rate"]
        cache.set(f"rate:{currency}", rate, 300)
        return rate
    except requests.RequestException:
        # Fallback to cached rate
        return cache.get(f"rate:{currency}")
```

### Bulkhead Pattern

```python
from concurrent.futures import ThreadPoolExecutor
import functools

def bulkhead(max_workers=10):
    """Decorator to limit concurrent operations."""
    executor = ThreadPoolExecutor(max_workers=max_workers)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            future = executor.submit(func, *args, **kwargs)
            return future.result(timeout=30)
        return wrapper
    return decorator

@bulkhead(max_workers=5)
def call_external_api(data):
    """Limited to 5 concurrent calls."""
    return requests.post("https://api.external.com", json=data)
```

### Retry with Exponential Backoff

```python
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Retry with exponential backoff and jitter."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise

                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)

            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=1)
def save_to_database(record):
    """Retry database saves with backoff."""
    return db.insert(record)
```

## Production Readiness Review (PRR)

```yaml
# prr-checklist.yml
production_readiness_review:
  service_name: api-service
  version: v2.1.0
  date: YYYY-MM-DD

  reliability:
    - slos_defined: true
    - error_budget_policy: documented
    - runbooks_complete: true
    - oncall_rotation_established: true
    - automated_rollbacks: implemented

  observability:
    - metrics_in_prometheus: true
    - dashboards_created: true
    - alerts_configured: true
    - distributed_tracing: enabled
    - logging_to_central: true
    - error_tracking: configured

  scalability:
    - load_test_completed: true
    - autoscaling_configured: true
    - resource_limits_set: true
    - database_connection_pooling: configured

  security:
    - vulnerability_scan_passed: true
    - secrets_in_vault: true
    - encryption_at_rest: true
    - encryption_in_transit: true
    - authz_implemented: true

  deployment:
    - ci_cd_pipeline: true
    - canary_deployment: true
    - feature_flags_configured: true
    - database_migrations_safe: true

  data_management:
    - backup_strategy_defined: true
    - disaster_recovery_tested: true
    - data_retention_policy: documented
    - gdpr_compliance: verified

  signoffs:
    - sre_lead: "@sre-lead"
    - security_lead: "@security-lead"
    - engineering_lead: "@eng-lead"
    - date_approved: YYYY-MM-DD

  go_no_go_decision: GO
  notes: "Service is ready for production"
```

## On-Call Best Practices

```markdown
# On-Call Handbook

## Rotation
- Primary: 1 week shifts
- Secondary: Shadow primary
- Shadow: New SREs shadow for 1 month

## Handoff Checklist
- [ ] Outstanding incidents reviewed
- [ ] Ongoing issues documented
- [ ] Alerts tuned if noisy
- [ ] Runbook updates shared

## Alert Response Priorities
1. **Data loss/corruption** - Immediate response
2. **Security incident** - Page security team
3. **Revenue impact** - Escalate to leadership
4. **Customer facing degradation** - Standard response
5. **Internal tooling** - Next business day

## Escalation Path
1. Primary on-call (5 min)
2. Secondary on-call (10 min)
3. Engineering manager (15 min)
4. Director of Engineering (Sev1 only)

## Runbook Writing
- One runbook per alert
- Include commands to copy/paste
- Link to relevant dashboards
- Update after every incident
```
