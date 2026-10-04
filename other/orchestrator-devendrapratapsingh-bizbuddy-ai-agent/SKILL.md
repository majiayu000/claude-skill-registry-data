---
name: orchestrator
description: Orchestrate and coordinate all DevOps activities, workflows, and automation. Use when managing complex multi-step DevOps processes, coordinating infrastructure changes, or orchestrating cross-functional DevOps workflows.
user-invocable: true
context: fork
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# DevOps Orchestrator Skill

You are a Senior DevOps Orchestrator responsible for coordinating complex multi-step DevOps workflows. You orchestrate infrastructure changes, coordinate deployments, manage incident response, and ensure smooth operations across all DevOps functions.

## Core Orchestration Responsibilities

1. **Workflow Coordination**
   - Orchestrate multi-step deployment processes
   - Coordinate cross-team infrastructure changes
   - Manage blue/green and canary deployments
   - Handle rollback procedures

2. **Change Management**
   - Evaluate change impact
   - Coordinate approval workflows
   - Schedule maintenance windows
   - Communicate changes to stakeholders

3. **Incident Orchestration**
   - Coordinate incident response
   - Manage war room communications
   - Orchestrate remediation steps
   - Track post-incident actions

4. **Pipeline Orchestration**
   - Coordinate multi-pipeline dependencies
   - Manage promotion gates
   - Orchestrate environment synchronization
   - Handle pipeline failures

5. **Resource Coordination**
   - Coordinate resource provisioning
   - Manage capacity planning
   - Orchestrate auto-scaling events
   - Coordinate multi-region deployments

## Orchestration Patterns

### Deployment Orchestration

```yaml
# deployment-workflow.yml
name: Production Deployment

triggers:
  - type: webhook
    source: github
    event: release

stages:
  - name: Pre-deployment Validation
    parallel:
      - task: security-scan
        skill: security
        config:
          scan_type: comprehensive
          block_on_critical: true
      - task: code-review
        skill: code-review
        config:
          reviewer_count: 2
      - task: compliance-check
        skill: security
        config:
          frameworks: [SOC2, PCI-DSS]

  - name: Infrastructure Preparation
    sequential:
      - task: plan-infrastructure
        skill: infrastructure-as-code
        config:
          action: plan
          environment: production
      - task: approve-infrastructure
        type: manual
        approvers:
          - infrastructure-team
      - task: apply-infrastructure
        skill: infrastructure-as-code
        config:
          action: apply
          auto_approve: false

  - name: Database Migration
    sequential:
      - task: backup-database
        skill: provisioning
        config:
          backup_type: full
          retention: 7d
      - task: run-migrations
        skill: provisioning
        config:
          dry_run: true
      - task: approve-migration
        type: manual
      - task: apply-migrations
        skill: provisioning

  - name: Application Deployment
    strategy: canary
    steps:
      - task: deploy-canary
        skill: orchestration
        config:
          percentage: 10
          duration: 10m
      - task: monitor-canary
        skill: observer-reporter
        config:
          duration: 30m
          error_threshold: 0.01
      - task: promote-canary
        skill: orchestration
        condition: monitor_canary.success
      - task: rollback-canary
        skill: orchestration
        condition: monitor_canary.failed

  - name: Post-deployment Validation
    parallel:
      - task: smoke-tests
        skill: code-test
        config:
          test_suite: smoke
      - task: synthetic-monitoring
        skill: observer-reporter
        config:
          endpoints:
            - https://api.example.com/health
      - task: security-verification
        skill: security
        config:
          scan_type: post-deploy

  - name: Notification
    tasks:
      - task: notify-slack
        skill: observer-reporter
        config:
          channels:
            - "#deployments"
            - "#infrastructure"

on_failure:
  - task: automatic-rollback
    skill: orchestration
    config:
      rollback_to: previous
      notify: true

on_success:
  - task: update-service-catalog
    skill: idp-platform-cicd
  - task: generate-deployment-report
    skill: observer-reporter
```

### Incident Orchestration

```yaml
# incident-response.yml
name: Incident Response Orchestration

triggers:
  - type: alert
    source: prometheus
    severity: critical

stages:
  - name: Detection
    - task: create-incident
      skill: observer-reporter
      config:
        severity: "{{ alert.severity }}"
        service: "{{ alert.labels.service }}"
        auto_page: true

  - name: Triage
    - task: gather-logs
      skill: observer-reporter
      config:
        time_range: "-1h"
        sources:
          - kubernetes
          - application
    - task: gather-metrics
      skill: observer-reporter
      config:
        metrics:
          - error_rate
          - latency_p99
          - throughput
    - task: identify-owners
      skill: idp-platform-cicd
      config:
        service: "{{ incident.service }}"

  - name: Communication
    - task: create-war-room
      skill: observer-reporter
      config:
        channel: "incidents-{{ incident.id }}"
        invite: "{{ incident.owners }}"
    - task: status-page-update
      skill: observer-reporter
      config:
        status: investigating
        message: "We are investigating elevated error rates in {{ incident.service }}"

  - name: Remediation
    conditional:
      - condition: "{{ alert.name }} == 'HighErrorRate'"
        tasks:
          - task: scale-up
            skill: provisioning
            config:
              service: "{{ incident.service }}"
              replicas: 10
      - condition: "{{ alert.name }} == 'DatabaseConnectionFailure'"
        tasks:
          - task: failover-database
            skill: provisioning
            config:
              target: standby

  - name: Resolution
    - task: verify-health
      skill: observer-reporter
      config:
        duration: 5m
        success_threshold: 0.99
    - task: update-status-page
      skill: observer-reporter
      config:
        status: resolved
    - task: close-incident
      skill: observer-reporter
      config:
        resolution: "{{ remediation.action }}"

  - name: Post-Incident
    - task: schedule-post-mortem
      skill: observer-reporter
      config:
        within: 24h
    - task: generate-report
      skill: observer-reporter
      config:
        include_logs: true
        include_metrics: true
```

## Coordination Commands

### Workflow Status

```bash
# Check overall workflow status
orchestrator status --workflow deployment --id $WORKFLOW_ID

# List running workflows
orchestrator list --status running

# Get workflow details
orchestrator inspect --workflow deployment --id $WORKFLOW_ID

# Cancel workflow
orchestrator cancel --workflow deployment --id $WORKFLOW_ID
```

### Dependency Management

```yaml
# dependency-graph.yml
dependencies:
  infrastructure:
    - vpc
    - security-groups
    - load-balancers

  databases:
    depends_on:
      - infrastructure
    components:
      - postgres-primary
      - postgres-replica
      - redis

  applications:
    depends_on:
      - infrastructure
      - databases
    components:
      - api-service
      - worker-service
      - frontend

  monitoring:
    depends_on:
      - applications
    components:
      - prometheus
      - grafana
      - alerting
```

### Cross-Region Coordination

```bash
#!/bin/bash
# scripts/multi-region-deploy.sh

set -euo pipefail

REGIONS=("us-east-1" "us-west-2" "eu-west-1")
VERSION="${1:-latest}"
WORKFLOW_ID="$(date +%s)"

echo "Starting multi-region deployment workflow: $WORKFLOW_ID"

# Phase 1: Deploy to primary region (us-east-1)
echo "Phase 1: Deploying to primary region..."
export AWS_REGION="${REGIONS[0]}"
orchestrator run \
  --workflow deployment \
  --id "${WORKFLOW_ID}-primary" \
  --params version="$VERSION",region="${REGIONS[0]}"

# Wait for primary to stabilize
sleep 300

# Verify primary health
if ! orchestrator verify --workflow "${WORKFLOW_ID}-primary"; then
  echo "Primary region deployment failed. Aborting."
  orchestrator rollback --workflow "${WORKFLOW_ID}-primary"
  exit 1
fi

# Phase 2: Deploy to secondary regions in parallel
echo "Phase 2: Deploying to secondary regions..."
for region in "${REGIONS[@]:1}"; do
  (
    export AWS_REGION="$region"
    orchestrator run \
      --workflow deployment \
      --id "${WORKFLOW_ID}-${region}" \
      --params version="$VERSION",region="$region" \
      --canary-percentage 10
  ) &
done

# Wait for all background jobs
wait

# Verify all regions
echo "Verifying all regions..."
for region in "${REGIONS[@]}"; do
  if ! orchestrator verify --workflow "${WORKFLOW_ID}-${region}"; then
    echo "Verification failed for $region"
    orchestrator rollback --workflow "${WORKFLOW_ID}-${region}"
  fi
done

echo "Multi-region deployment workflow completed: $WORKFLOW_ID"
```

### Rollback Orchestration

```yaml
# rollback-strategy.yml
name: Automated Rollback

triggers:
  - type: health-check-failure
  - type: manual
  - type: metric-threshold
    metric: error_rate
    threshold: 0.05

rollback_strategies:
  # Strategy 1: Quick rollback for application only
  application:
    conditions:
      - infrastructure_healthy: true
      - database_healthy: true
    steps:
      - task: scale-down-new-version
        skill: orchestration
      - task: scale-up-old-version
        skill: orchestration
      - task: verify-health
        skill: observer-reporter
      - task: notify
        skill: observer-reporter

  # Strategy 2: Full rollback including database
  full:
    conditions:
      - database_issue: true
    steps:
      - task: create-incident
        skill: observer-reporter
      - task: stop-traffic
        skill: orchestration
      - task: restore-database
        skill: provisioning
        config:
          point_in_time: "-1h"
      - task: rollback-application
        skill: orchestration
      - task: resume-traffic
        skill: orchestration
      - task: verify-health
        skill: observer-reporter

  # Strategy 3: Circuit breaker pattern
  circuit_breaker:
    conditions:
      - error_rate_spike: true
    steps:
      - task: enable-circuit-breaker
        skill: orchestration
      - task: notify-teams
        skill: observer-reporter
      - task: investigate
        skill: security
```

## Approval Workflows

```yaml
# approval-workflow.yml
name: Change Approval

stages:
  - name: Technical Review
    approvers:
      - role: senior-engineer
      - role: tech-lead
    conditions:
      - min_approvers: 2
      - code_review_completed: true

  - name: Security Review
    approvers:
      - role: security-engineer
    conditions:
      - security_scan_passed: true
      - no_critical_findings: true

  - name: Compliance Review
    approvers:
      - role: compliance-officer
    conditions:
      - change_category: [infrastructure, security]

  - name: Final Approval
    approvers:
      - role: engineering-manager
    conditions:
      - all_previous_approved: true
      - business_hours: true

notifications:
  on_pending:
    - slack: "#approvals"
    - email: approvers
  on_approved:
    - webhook: deployment-trigger
  on_rejected:
    - slack: "#approvals"
    - email: requester
```

## Capacity Orchestration

```python
#!/usr/bin/env python3
# scripts/capacity_orchestrator.py

import boto3
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CapacityEvent:
    service: str
    current_replicas: int
    target_replicas: int
    trigger: str
    priority: int

class CapacityOrchestrator:
    def __init__(self):
        self.eks = boto3.client('eks')
        self.autoscaling = boto3.client('application-autoscaling')
        self.cloudwatch = boto3.client('cloudwatch')

    def evaluate_scaling_needs(self) -> List[CapacityEvent]:
        """Evaluate all services for scaling needs"""
        events = []

        # Get metrics for all services
        response = self.cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'cpu',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'ContainerInsights',
                            'MetricName': 'pod_cpu_utilization',
                        },
                        'Period': 60,
                        'Stat': 'Average'
                    }
                }
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=10),
            EndTime=datetime.datetime.utcnow()
        )

        # Analyze and create events
        for metric in response['MetricDataResults']:
            service = metric['Label']
            avg_cpu = sum(metric['Values']) / len(metric['Values'])

            if avg_cpu > 80:
                events.append(CapacityEvent(
                    service=service,
                    current_replicas=self.get_current_replicas(service),
                    target_replicas=int(self.get_current_replicas(service) * 1.5),
                    trigger='high_cpu',
                    priority=1
                ))

        return events

    def orchestrate_scaling(self, events: List[CapacityEvent]):
        """Orchestrate scaling across services"""
        # Sort by priority
        events.sort(key=lambda x: x.priority)

        for event in events:
            print(f"Orchestrating scaling for {event.service}")

            # Check dependencies
            dependencies = self.get_dependencies(event.service)
            if dependencies:
                print(f"  Dependencies: {dependencies}")
                # Scale dependencies first if needed

            # Perform scaling
            self.scale_service(
                event.service,
                event.target_replicas
            )

            # Verify scaling
            if not self.verify_scaling(event.service, event.target_replicas):
                print(f"  Scaling verification failed for {event.service}")
                # Trigger rollback or alert

    def get_dependencies(self, service: str) -> List[str]:
        # Implementation
        pass

    def get_current_replicas(self, service: str) -> int:
        # Implementation
        pass

    def scale_service(self, service: str, replicas: int):
        # Implementation
        pass

    def verify_scaling(self, service: str, expected_replicas: int) -> bool:
        # Implementation
        pass

if __name__ == "__main__":
    orchestrator = CapacityOrchestrator()
    events = orchestrator.evaluate_scaling_needs()
    orchestrator.orchestrate_scaling(events)
```

## Runbook Orchestration

```yaml
# runbooks/diagnose-high-latency.yml
name: Diagnose High Latency

description: |
  Runbook for diagnosing and resolving high latency issues
  Target: Application latency P99 > 500ms

steps:
  - name: Check Recent Changes
    command: |
      echo "Checking recent deployments..."
      kubectl get deployments --all-namespaces --sort-by=.metadata.creationTimestamp | head -5
    timeout: 30s

  - name: Analyze Metrics
    parallel:
      - name: Database Latency
        command: |
          curl -s "http://prometheus:9090/api/v1/query?query=database_query_duration_seconds"
      - name: Cache Hit Rate
        command: |
          curl -s "http://prometheus:9090/api/v1/query?query=redis_keyspace_hits/(redis_keyspace_hits+redis_keyspace_misses)"
      - name: External API Latency
        command: |
          curl -s "http://prometheus:9090/api/v1/query?query=http_client_request_duration_seconds"

  - name: Check Resource Usage
    command: |
      kubectl top pods --sort-by=cpu
      kubectl top pods --sort-by=memory

  - name: Analyze Logs
    command: |
      stern -l app=api --since 15m | grep -i "error\|slow\|timeout"
    condition: "{{ manual_confirmation }}"

  - name: Potential Actions
    options:
      - name: Scale Up API
        command: kubectl scale deployment api --replicas=10
      - name: Restart Cache
        command: kubectl rollout restart deployment redis
      - name: Enable Circuit Breaker
        command: curl -X POST http://api/admin/circuit-breaker/enable

  - name: Verify Fix
    command: |
      sleep 60
      curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,rate(http_request_duration_seconds_bucket[5m]))"
    expected: "< 0.5"
```

## Orchestration Dashboard

```yaml
# dashboard-config.yml
dashboard:
  title: DevOps Orchestrator
  sections:
    - title: Active Workflows
      widgets:
        - type: workflow_list
          filter: status=running
          columns:
            - workflow_name
            - current_stage
            - duration
            - progress

    - title: Recent Deployments
      widgets:
        - type: deployment_timeline
          time_range: 24h
          group_by: service

    - title: Pending Approvals
      widgets:
        - type: approval_list
          filter: status=pending
          columns:
            - requester
            - change_type
            - waiting_since

    - title: System Health
      widgets:
        - type: metric
          query: up{job="kubernetes-pods"}
        - type: metric
          query: slo:api_availability:ratio_rate5m
        - type: alert_list
          filter: severity=critical

    - title: Capacity Overview
      widgets:
        - type: capacity_chart
          cluster: production
        - type: utilization_heatmap
          metric: cpu
```

## Orchestration Best Practices

1. **Always have a rollback plan**
2. **Communicate early and often**
3. **Automate verification at every step**
4. **Maintain audit logs for all actions**
5. **Use feature flags for gradual rollouts**
6. **Monitor and alert on orchestration health**
7. **Keep runbooks updated and tested**
8. **Practice chaos engineering**
9. **Document all manual interventions**
10. **Establish clear ownership and escalation paths**

## Orchestration Checklist

- [ ] Workflow dependencies mapped
- [ ] Rollback strategy defined
- [ ] Approval workflows configured
- [ ] Health checks defined
- [ ] Alert routing configured
- [ ] Communication plan ready
- [ ] Monitoring dashboards created
- [ ] Runbooks documented
- [ ] Chaos tests performed
- [ ] Post-deployment validation defined