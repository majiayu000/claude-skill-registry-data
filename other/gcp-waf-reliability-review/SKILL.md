---
name: gcp-waf-reliability-review
description: "Evaluate GCP workload reliability against the Google Cloud Well-Architected Framework reliability pillar — covering SLOs/error budgets, HA topology, horizontal scalability, observability, graceful degradation, failure testing, data recovery, and postmortems. Use when assessing availability requirements, designing resilient architectures, or auditing a GCP workload for reliability gaps."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-09"
  category: resilience
---

# GCP WAF Reliability Review

## Purpose

Evaluate GCP workload reliability against the Google Cloud Well-Architected Framework (WAF) reliability pillar. This skill supports consistent performance, resilience to failures, and graceful recovery for workloads running on GCP.

## When to use

Use this skill for:

- Assessing availability requirements and SLO definitions for a workload
- Designing highly available, resilient architectures on GCP
- Auditing a workload against the nine WAF reliability principles
- Evaluating redundancy topology, observability coverage, and failure testing maturity
- Reviewing postmortem culture and data recovery practices

## WAF Reliability Pillar Overview

The GCP Well-Architected Framework reliability pillar provides guidance across nine core principles. Together they ensure workloads deliver consistent performance to users, remain resilient under fault conditions, and recover gracefully from both partial and complete failures. The pillar emphasizes user-experience-driven SLOs, error budget discipline, horizontal scalability, and continuous improvement through postmortems.

## Core Principles

### 1. Define Reliability Based on User-Experience Goals
Anchor reliability targets to user-observable outcomes rather than internal infrastructure metrics. Define SLIs that reflect what users actually care about — latency, availability, correctness, and throughput.
- Reference: https://cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals

### 2. Set Realistic Targets for Reliability
Establish SLOs and error budgets that are achievable, meaningful, and aligned with business risk tolerance. Avoid aspirational targets that drain engineering capacity without delivering user value.
- Reference: https://cloud.google.com/architecture/framework/reliability/set-targets

### 3. Build Highly Available Systems Through Resource Redundancy
Eliminate single points of failure by distributing resources across multiple zones and regions. Design for fault isolation so that the failure of any single component does not cascade to a full system outage.
- Reference: https://cloud.google.com/architecture/framework/reliability/build-highly-available-systems

### 4. Take Advantage of Horizontal Scalability
Design systems to scale out rather than up. Use managed instance groups, GKE node pools, and serverless platforms to handle load increases without manual intervention and without architectural bottlenecks.
- Reference: https://cloud.google.com/architecture/framework/reliability/horizontal-scalability

### 5. Detect Potential Failures by Using Observability
Instrument workloads with metrics, logs, and traces that provide actionable signals before failures reach users. Use SLI-based alerting to distinguish user-impacting events from noise.
- Reference: https://cloud.google.com/architecture/framework/reliability/observability

### 6. Design for Graceful Degradation
Architect systems to maintain partial functionality under failure conditions. Implement circuit breakers, retries with exponential backoff, bulkheads, rate limiting, and fallback paths to prevent cascading failures.
- Reference: https://cloud.google.com/architecture/framework/reliability/graceful-degradation

### 7. Perform Testing for Recovery from Failures
Validate resilience assumptions through chaos engineering and game days. Test failure modes including zone outages, dependency timeouts, traffic surges, and misconfigurations in pre-production and, where safe, in production.
- Reference: https://cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-failures

### 8. Perform Testing for Recovery from Data Loss
Validate backup and restore procedures regularly. Test recovery time objective (RTO) and recovery point objective (RPO) compliance under realistic failure scenarios, not just in tabletop exercises.
- Reference: https://cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-data-loss

### 9. Conduct Thorough Postmortems
Build a blameless postmortem culture to systematically capture incident learnings. Track action items to completion and share findings to prevent recurrence across teams.
- Reference: https://cloud.google.com/architecture/framework/reliability/conduct-postmortems

## Relevant GCP Products

- **Compute & Containers:** Compute Engine Managed Instance Groups (MIGs), Google Kubernetes Engine (GKE), Cloud Run, Cloud Run Functions
- **Load Balancing & Networking:** Cloud Load Balancing (global and regional), Cloud CDN, Cloud DNS with routing policies, Traffic Director
- **Data & Storage:** Cloud Storage (multi-region buckets), Cloud SQL with HA and read replicas, Cloud Spanner (multi-region), Bigtable, Firestore
- **Observability:** Cloud Monitoring, Cloud Logging, Cloud Trace, Google Cloud Managed Service for Prometheus, Error Reporting, SLO monitoring
- **Backup & Resilience:** Backup and DR Service, Cloud Storage versioning, Cloud SQL automated backups, Spanner PITR
- **Autoscaling:** MIG autoscaler, GKE Horizontal Pod Autoscaler (HPA), GKE Vertical Pod Autoscaler (VPA), GKE cluster autoscaler, Cloud Run concurrency-based scaling

## Assessment Question Bank

### SLO/SLI Definition and Error Budgets
1. Are SLIs defined based on user-observable outcomes (latency, availability, correctness) rather than infrastructure metrics?
2. Is an SLO set for each user-facing service with an associated error budget?
3. Is the error budget actively tracked and used to gate feature velocity vs. reliability investment?
4. Are SLOs documented in a service-level agreement (SLA) or internal reliability contract?
5. Are SLOs reviewed and updated when user expectations or product requirements change?
6. Is there a process for alerting when error budget burn rate is too high?

### Realistic Reliability Targets
1. Were SLO targets derived from user research, business requirements, or dependency constraints rather than set arbitrarily?
2. Is the cost of each additional nine (99.9% vs. 99.99%) understood and justified?
3. Are dependencies' reliability levels accounted for when setting the workload's own SLO?
4. Is there a tiering model distinguishing critical vs. non-critical services with different reliability targets?
5. Are error budget policies defined (e.g., freeze new features when budget is exhausted)?

### High Availability Topology
1. Are workloads deployed across at least two availability zones within a region?
2. Are stateful services (databases, caches) configured for multi-zone or multi-region replication?
3. Are managed instance groups or GKE deployments configured with anti-affinity rules to spread replicas across zones?
4. Is Cloud Load Balancing configured with health checks that remove unhealthy backends automatically?
5. Are DNS failover or routing policies used to redirect traffic during regional impairments?
6. Is there a documented recovery procedure for a full zone failure?
7. Are global load balancers used for latency-sensitive workloads requiring cross-region failover?

### Horizontal Scalability
1. Are workloads designed to scale out (add instances) rather than scale up (increase instance size)?
2. Are autoscaling policies configured and tested for all stateless compute tiers?
3. Is there capacity headroom available to absorb unexpected traffic spikes without manual intervention?
4. Are stateful components (databases, queues) able to scale horizontally or handle peak load without bottlenecks?
5. Are scaling decisions based on meaningful metrics (request latency, queue depth) rather than just CPU utilization?
6. Are scale-in operations safe — do they wait for in-flight requests to complete before terminating instances?

### Observability
1. Are the four golden signals (latency, traffic, errors, saturation) instrumented for each service?
2. Are SLI metrics available in Cloud Monitoring with SLO policies configured?
3. Is distributed tracing enabled to diagnose cross-service latency issues?
4. Are logs structured and indexed for efficient querying during incidents?
5. Are alerting policies calibrated to user-impacting events — not just infrastructure anomalies?
6. Is there an on-call runbook for every critical alert?
7. Is Managed Service for Prometheus used for workload-level metrics in GKE environments?
8. Are dashboards available that show SLO burn rate in real time?

### Graceful Degradation
1. Are circuit breakers implemented for calls to external dependencies and downstream services?
2. Are retries bounded with exponential backoff and jitter to prevent retry storms?
3. Are rate limits and concurrency controls applied to protect services from overload?
4. Are fallback paths defined — what does the system do when a non-critical dependency is unavailable?
5. Are bulkheads or resource pools used to isolate failures in one subsystem from others?
6. Are timeouts set on all synchronous outbound calls?
7. Is load shedding implemented to preserve core functionality under extreme load?

### Failure Recovery Testing
1. Are chaos engineering experiments (e.g., zone failure simulation, dependency injection) performed in pre-production?
2. Is a game day schedule maintained and followed at least annually for critical workloads?
3. Are failure scenarios documented with expected behavior and actual results compared?
4. Are runbooks validated by actually executing them during game days rather than just reviewing them?
5. Is the blast radius of each experiment scoped and approved before execution?

### Data Recovery Testing
1. Are backup procedures automated and scheduled for all stateful services?
2. Are backup restores tested on a scheduled cadence (e.g., monthly) — not just at setup time?
3. Are RTO and RPO targets defined and validated through restore tests?
4. Are backups stored in a separate project or region from the primary data to protect against account-level failures?
5. Is point-in-time recovery (PITR) enabled for databases where fine-grained recovery is required?
6. Are backup success/failure alerts configured and monitored?

### Postmortems
1. Is a blameless postmortem required for every P0 and P1 incident?
2. Are postmortems completed within a defined SLA (e.g., 5 business days after incident resolution)?
3. Are action items assigned owners and tracked to completion in a system of record?
4. Are postmortem findings shared across teams to prevent similar incidents?
5. Is there a process for identifying recurring themes across postmortems?
6. Are follow-up reliability improvements validated before the next incident review cycle closes?

## Validation Checklist

### SLI/SLO Monitoring
- [ ] SLIs defined for all user-facing services based on user-observable outcomes
- [ ] SLO policies configured in Cloud Monitoring with error budget tracking
- [ ] Error budget burn rate alerts configured and tested
- [ ] Error budget policies documented (e.g., feature freeze when budget exhausted)

### Cross-Zone Redundancy
- [ ] All stateless compute tiers deployed across at least two zones
- [ ] Stateful services (Cloud SQL, Spanner, Memorystore) configured for multi-zone HA
- [ ] MIG or GKE anti-affinity rules preventing all replicas from landing in a single zone
- [ ] Load balancer health checks removing unhealthy backends automatically

### Autoscaling
- [ ] Autoscaling configured for all stateless compute (MIG autoscaler, HPA, Cloud Run concurrency)
- [ ] Scaling metrics reflect meaningful load signals (latency, queue depth) not just CPU
- [ ] Scale-in operations validated to complete in-flight requests before instance termination

### Health Checks
- [ ] HTTP(S) or gRPC health checks configured on all backend services
- [ ] Health check intervals and unhealthy thresholds tuned to detect failures quickly
- [ ] Health check failures trigger automated backend removal

### Backup Testing
- [ ] Backup restore tested within the last 30 days for all critical stateful services
- [ ] RTO and RPO targets documented and validated through restore tests
- [ ] Backups stored in a separate project or region from primary data

### Graceful Degradation Patterns
- [ ] Circuit breakers implemented for all external and downstream service calls
- [ ] Retries bounded with exponential backoff and jitter
- [ ] Rate limiting and concurrency controls applied to protect from overload
- [ ] Fallback paths defined and tested for all non-critical dependencies
- [ ] Timeouts set on all synchronous outbound calls

### Game Days and Chaos Engineering
- [ ] Game day conducted within the last 12 months for all critical workloads
- [ ] Chaos experiments scoped, approved, and results documented
- [ ] Runbooks validated by execution rather than review only

### Postmortem Process
- [ ] Blameless postmortem required for all P0 and P1 incidents
- [ ] Postmortem SLA defined (e.g., 5 business days) and met
- [ ] Action items tracked to completion in a system of record

## Response Shape

1. **Scope** — workload name, GCP resource hierarchy scope, evidence level (live / sanitized / documentation-based / inference)
2. **SLO/SLI Assessment** — review of SLI definitions, SLO targets, error budget tracking, and alerting calibration
3. **HA Topology Review** — evaluation of redundancy patterns, load balancing configuration, and zone/region coverage
4. **Observability Gaps** — missing metrics, alerts, dashboards, or tracing coverage that reduce incident detection capability
5. **Failure Testing Status** — game day schedule, chaos experiment coverage, runbook validation status
6. **Recommendations** — ordered by reliability risk (Critical / High / Medium / Low), each with minimum required change, validation step, and rollback procedure
7. **Open Risks** — items that could not be assessed due to missing evidence, with recommended evidence to gather
