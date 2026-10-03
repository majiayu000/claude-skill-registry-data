---
name: deployment-orchestration
description: >
  Use when orchestrating deployments across multiple services or instances,
  managing deployment pipelines, implementing rollback procedures, or coordinating
  multi-stage rollouts. This skill provides cross-company deployment patterns.
---

# Deployment Orchestration - Shared Skill

## Overview
This skill provides standardized deployment orchestration patterns for managing deployments across multiple services, companies, or cloud instances with zero-downtime and safe rollback capabilities.

## When to Use
- When coordinating multi-service deployments
- When managing deployment pipelines
- When implementing canary/phased rollouts
- When setting up rollback procedures
- When automating deployment workflows

## Core Procedures

### Deployment Pipeline Structure
```yaml
deployment_pipeline:
  stages:
    - name: build
      actions:
        - lint
        - test
        - build
    
    - name: staging
      actions:
        - deploy to staging
        - integration tests
        - smoke tests
    
    - name: production
      actions:
        - backup current version
        - deploy canary (5%)
        - health check
        - gradual rollout (25%, 50%, 100%)
        - monitoring
```

### Zero-Downtime Deployment
```yaml
deployment_strategy:
  type: rolling_update
  
  rolling_update:
    max_surge: 1
    max_unavailable: 0
   健康检查: /health endpoint
    
  blue_green:
    - maintain parallel environments
    - switch traffic after validation
    - instant rollback capability
    
  canary:
    - initial: 5% traffic
    - check: 30 minutes
    - increment: 25%, 50%, 100%
    - automatic rollback on failure
```

### Pre-Deployment Checklist
```yaml
pre_deployment:
  - [ ] All tests passing
  - [ ] Code review approved
  - [ ] Change log updated
  - [ ] Database migrations tested
  - [ ] Rollback plan documented
  - [ ] Stakeholders notified
  - [ ] Maintenance window scheduled
  - [ ] Monitoring alerts configured
```

### Post-Deployment Verification
```yaml
post_deployment:
  health_checks:
    - GET /health → 200
    - GET /api/health → 200
    - Database connectivity
    - Cache connectivity
  
  smoke_tests:
    - User login flow
    - Core business logic
    - Critical integrations
  
  monitoring:
    - Error rate baseline vs post-deploy
    - Latency comparison
    - Resource usage
```

## Rollback Procedures

### Instant Rollback
```yaml
rollback:
  strategy: blue_green
  
  process:
    1. detect_failure:
       - error_rate > threshold
       - health check failed
       - latency spike
  
    2. trigger_rollback:
       - switch traffic to previous version
       - zero-downtime if blue-green
  
    3. verify_rollback:
       - health checks pass
       - error rate normalized
  
    4. notify:
       - stakeholders
       - post-mortem scheduled
```

### Database Rollback
```yaml
database_rollback:
  backup_strategy:
    - pre-deployment backup
    - point-in-time recovery enabled
  
  migration_rollback:
    - down migrations ready
    - data integrity verified
    - rollback tested in staging
```

## Multi-Instance Deployment

### Staged Rollout
```yaml
staged_rollout:
  stages:
    - name: internal
      targets:
        - dev.internal.example.com
      percentage: 0%
      duration: 1 hour
  
    - name: canary
      targets:
        - prod.example.com
      percentage: 5%
      duration: 30 minutes
  
    - name: gradual
      percentage: 25%
      duration: 1 hour
  
    - name: full
      percentage: 100%
      duration: immediate
```

### Cross-Region Deployment
```yaml
cross_region:
  strategy: regional_rollback
  
  regions:
    - us-east-1 (primary)
    - eu-west-1 (GDPR)
    - ap-southeast-1
  
  deployment_order:
    - regions:
        - eu-west-1 (compliance first)
        - us-east-1
        - ap-southeast-1
  
  rollback_order: reverse
```

## Monitoring & Alerts

### Deployment Metrics
```yaml
deployment_metrics:
  - deployment_duration
  - time_to_health_check_pass
  - rollback_frequency
  - success_rate
  
comparison_metrics:
  - error_rate (before/after)
  - latency_p95 (before/after)
  - availability (before/after)
```

### Alerting Rules
```yaml
alerts:
  critical:
    - deployment_failed
    - health_check_failed
  
  warning:
    - error_rate_increased
    - latency_degraded
    - partial_rollout_stalled
```

## Best Practices

1. **Always have rollback plan** before deployment
2. **Deploy during low traffic** windows
3. **Monitor closely** for first 30 minutes
4. **Communicate** with stakeholders
5. **Document** all deployments and outcomes
6. **Automate** where possible
7. **Test** rollback in staging first
