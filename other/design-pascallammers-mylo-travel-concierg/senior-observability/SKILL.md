---

# === CORE IDENTITY ===
name: senior-observability
title: Senior Observability Skill Package
description: Comprehensive observability skill for monitoring, logging, distributed tracing, alerting, and SLI/SLO implementation across distributed systems. Includes dashboard generation, alert rule creation, error budget calculation, and metrics analysis. Use when implementing monitoring stacks, designing alerting strategies, setting up distributed tracing, or defining SLO frameworks.
domain: engineering
subdomain: observability-operations

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "4-8 hours per observability implementation"
frequency: "Weekly"
use-cases:
  - Implementing comprehensive monitoring with Prometheus and Grafana
  - Setting up distributed tracing with OpenTelemetry and Jaeger
  - Designing alerting strategies with multi-burn-rate SLO alerting
  - Creating dashboards for service health visibility using RED/USE methods
  - Calculating SLI/SLO targets and error budgets

# === RELATIONSHIPS ===
related-agents: [cs-observability-engineer]
related-skills: [senior-devops, senior-backend, senior-secops]
related-commands: []
orchestrated-by: [cs-observability-engineer]

# === TECHNICAL ===
dependencies:
  scripts:
    - dashboard_generator.py
    - alert_rule_generator.py
    - slo_calculator.py
    - metrics_analyzer.py
  references:
    - monitoring_patterns.md
    - logging_architecture.md
    - distributed_tracing.md
    - alerting_runbooks.md
  assets:
    - dashboard_templates/
    - alert_templates/
    - runbook_template.md
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+, Prometheus, Grafana, OpenTelemetry, Jaeger, ELK Stack, DataDog, CloudWatch, NewRelic]

# === EXAMPLES ===
examples:
  - title: Generate Grafana Dashboard
    input: "python3 scripts/dashboard_generator.py --service payment-api --type api --platform grafana --output json"
    output: "Complete Grafana dashboard JSON with RED method panels, resource metrics, and variable templating"
  - title: Generate SLO-Based Alerts
    input: "python3 scripts/alert_rule_generator.py --service payment-api --slo-target 99.9 --platform prometheus --output yaml"
    output: "Prometheus AlertManager rules with multi-burn-rate alerting and runbook links"
  - title: Calculate Error Budget
    input: "python3 scripts/slo_calculator.py --input metrics.csv --slo-type availability --target 99.9 --window 30d --output json"
    output: "SLO status report with error budget remaining, burn rate, and recommendations"
  - title: Generate NewRelic Dashboard
    input: "python3 scripts/dashboard_generator.py --service payment-api --type api --platform newrelic --output json"
    output: "NewRelic dashboard JSON with NRQL queries for RED method panels and SLO tracking"
  - title: Generate NewRelic Alerts
    input: "python3 scripts/alert_rule_generator.py --service payment-api --slo-target 99.9 --platform newrelic --output json"
    output: "NewRelic alert policy with multi-burn-rate NRQL conditions and notification channels"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-16
updated: 2025-12-16
license: MIT

# === DISCOVERABILITY ===
tags: [observability, monitoring, logging, tracing, alerting, slo, sli, prometheus, grafana, opentelemetry, jaeger, datadog, cloudwatch, newrelic, nrql, engineering, senior]
featured: false
verified: true
---


# Senior Observability

Complete toolkit for senior observability engineering with modern monitoring, logging, tracing, and alerting best practices.

## Overview

This skill provides comprehensive observability capabilities through four core Python automation tools and extensive reference documentation. Whether implementing monitoring stacks, designing alerting strategies, setting up distributed tracing, or defining SLO frameworks, this skill delivers production-ready observability solutions.

Senior observability engineers use this skill for metrics collection (Prometheus, DataDog, CloudWatch, **NewRelic**), visualization (Grafana dashboards, **NewRelic Dashboards**), distributed tracing (OpenTelemetry, Jaeger), centralized logging (ELK Stack, Loki, **NewRelic Logs**), and alerting (AlertManager, PagerDuty, **NewRelic Alerts**). The skill covers the Four Golden Signals, RED/USE methods, SLI/SLO frameworks, and incident response patterns.

**Core Value:** Reduce mean-time-to-detection (MTTD) by 60%+ and mean-time-to-resolution (MTTR) by 40%+ while improving system reliability through comprehensive observability practices and automated tooling.

## Quick Start

### Main Capabilities

This skill provides four core capabilities through automated scripts:

```bash
# Script 1: Dashboard Generator - Create Grafana/DataDog dashboards
python3 scripts/dashboard_generator.py --service my-api --type api --platform grafana --output json

# Script 2: Alert Rule Generator - Create Prometheus/DataDog alert rules
python3 scripts/alert_rule_generator.py --service my-api --slo-target 99.9 --platform prometheus --output yaml

# Script 3: SLO Calculator - Calculate error budgets and burn rates
python3 scripts/slo_calculator.py --input metrics.csv --slo-type availability --target 99.9 --output json

# Script 4: Metrics Analyzer - Analyze patterns, anomalies, and trends
python3 scripts/metrics_analyzer.py --input metrics.csv --analysis-type anomaly --output json
```

## Core Capabilities

- **Dashboard Generation** - Grafana, DataDog, CloudWatch, and **NewRelic** dashboards with RED/USE method panels, resource metrics, and variable templating
- **Alert Rule Creation** - Prometheus AlertManager, DataDog, CloudWatch, **NewRelic**, and PagerDuty alert rules with SLO-based multi-burn-rate alerting
- **SLO Framework** - SLI definition, SLO target calculation, error budget tracking, and burn rate analysis
- **Metrics Analysis** - Baseline calculation, anomaly detection, trend analysis, and cardinality optimization
- **Distributed Tracing** - OpenTelemetry instrumentation patterns, Jaeger/Tempo configuration, and trace analysis
- **Centralized Logging** - Structured logging patterns, ELK Stack/Loki architecture, and log correlation

## Python Tools

### 1. Dashboard Generator

Generate production-ready dashboard configurations for Grafana, DataDog, or CloudWatch.

**Usage:**
```bash
python3 scripts/dashboard_generator.py \
  --service "payment-api" \
  --type api \
  --platform grafana \
  --output json \
  --file dashboards/payment-api.json
```

**Arguments:**
- `--service` / `-s`: Service name (required)
- `--type` / `-t`: Service type - api, database, queue, cache, web (default: api)
- `--platform` / `-p`: Target platform - grafana, datadog, cloudwatch, **newrelic** (default: grafana)
- `--output` / `-o`: Output format - json, yaml, text (default: text)
- `--file` / `-f`: Write output to file
- `--verbose` / `-v`: Enable verbose output

**Features:**
- RED method panels (Request rate, Error rate, Duration percentiles)
- USE method panels (Utilization, Saturation, Errors)
- Resource metrics (CPU, memory, disk, network)
- Variable templating for multi-service dashboards
- Annotations for deployments and incidents
- Threshold configurations for visual alerts

### 2. Alert Rule Generator

Generate alerting rules for Prometheus AlertManager, DataDog, CloudWatch, NewRelic, or PagerDuty.

**Usage:**
```bash
python3 scripts/alert_rule_generator.py \
  --service "payment-api" \
  --slo-target 99.9 \
  --platform prometheus \
  --severity critical,warning \
  --output yaml \
  --file alerts/payment-api.yaml
```

**Arguments:**
- `--service` / `-s`: Service name (required)
- `--slo-target`: SLO availability target percentage (default: 99.9)
- `--platform` / `-p`: Target platform - prometheus, datadog, cloudwatch, **newrelic**, pagerduty (default: prometheus)
- `--severity`: Severity levels to generate - critical, warning, info (default: critical,warning)
- `--output` / `-o`: Output format - yaml, json, text (default: yaml)
- `--file` / `-f`: Write output to file
- `--runbook-url`: Base URL for runbook links
- `--verbose` / `-v`: Enable verbose output

**Features:**
- SLO-based alerting (error budget consumption rates)
- Multi-window, multi-burn-rate alerting patterns
- Alert severity classification with escalation
- Runbook link generation
- Inhibition rules to reduce alert noise

### 3. SLO Calculator

Calculate SLI/SLO targets, error budgets, and burn rates from metrics data.

**Usage:**
```bash
python3 scripts/slo_calculator.py \
  --input metrics.csv \
  --slo-type availability \
  --target 99.9 \
  --window 30d \
  --output json \
  --file slo-report.json
```

**Arguments:**
- `--input` / `-i`: Input metrics file (CSV or JSON) (required)
- `--slo-type`: Type of SLO - availability, latency, throughput (default: availability)
- `--target`: SLO target percentage (default: 99.9)
- `--window`: Time window - 7d, 30d, 90d (default: 30d)
- `--output` / `-o`: Output format - json, text, markdown, csv (default: text)
- `--file` / `-f`: Write output to file
- `--verbose` / `-v`: Enable verbose output

**Features:**
- SLI calculation from raw metrics (success rate, latency percentiles)
- Error budget calculation (total, consumed, remaining)
- Multi-window burn rate analysis (1h, 6h, 24h, 3d)
- SLO recommendations based on historical performance
- Alert threshold suggestions based on error budget

### 4. Metrics Analyzer

Analyze metrics patterns to detect anomalies, trends, and optimization opportunities.

**Usage:**
```bash
python3 scripts/metrics_analyzer.py \
  --input metrics.csv \
  --analysis-type anomaly \
  --metrics http_requests_total,http_request_duration_seconds \
  --threshold 3.0 \
  --output json \
  --file analysis-report.json
```

**Arguments:**
- `--input` / `-i`: Input metrics file (CSV or JSON) (required)
- `--analysis-type`: Analysis type - anomaly, trend, correlation, baseline, cardinality (default: anomaly)
- `--metrics`: Comma-separated metric names to analyze (optional, analyzes all if not specified)
- `--threshold`: Anomaly detection threshold in standard deviations (default: 3.0)
- `--output` / `-o`: Output format - json, text, markdown, csv (default: text)
- `--file` / `-f`: Write output to file
- `--verbose` / `-v`: Enable verbose output

**Features:**
- Statistical baseline calculation (mean, median, percentiles, std dev)
- Anomaly detection using Z-score and IQR methods
- Trend analysis (increasing, decreasing, stable, seasonal)
- Correlation analysis between metrics
- Cardinality analysis for high-cardinality metric optimization
- Actionable recommendations for metric improvements

## Reference Documentation

### 1. Monitoring Patterns (`references/monitoring_patterns.md`)

Comprehensive guide to metrics collection and visualization patterns:
- Four Golden Signals (Latency, Traffic, Errors, Saturation)
- RED Method (Rate, Errors, Duration) for request-driven services
- USE Method (Utilization, Saturation, Errors) for resources
- Platform-specific patterns (Prometheus, DataDog, CloudWatch, **NewRelic**)
- Metric naming conventions and labeling best practices
- Cardinality management and optimization

### 2. NewRelic Patterns (`references/newrelic_patterns.md`)

Complete NewRelic observability guide:
- NRQL query language syntax and best practices
- Four Golden Signals in NRQL (Transaction, SystemSample events)
- RED/USE method queries for NewRelic
- Dashboard widget types and configuration
- Alert condition types (NRQL, baseline, outlier)
- Service Level Management for SLIs/SLOs
- Kubernetes integration with nri-bundle
- PromQL to NRQL translation patterns

### 3. Logging Architecture (`references/logging_architecture.md`)

Complete logging strategy and implementation guide:
- Structured logging formats (JSON, key-value)
- Log levels and their appropriate usage
- ELK Stack architecture and configuration
- Loki/Grafana logging patterns
- Log aggregation strategies (sidecar, DaemonSet)
- Correlation IDs and distributed request tracing
- Log retention policies and cost optimization

### 4. Distributed Tracing (`references/distributed_tracing.md`)

End-to-end distributed tracing implementation:
- OpenTelemetry standards and instrumentation
- Trace context propagation patterns
- Jaeger and Tempo backend configuration
- Sampling strategies (head-based, tail-based, adaptive)
- Critical path analysis and bottleneck identification
- Service dependency mapping
- Performance overhead management

### 5. Alerting and Runbooks (`references/alerting_runbooks.md`)

Alerting strategy and incident response patterns:
- Symptom-based vs cause-based alerting
- SLI/SLO/SLA framework implementation
- Multi-window, multi-burn-rate alerting
- Alert fatigue prevention strategies
- Runbook structure and best practices
- Escalation policies and on-call rotation
- Incident response integration

## Asset Templates

### Dashboard Templates (`assets/dashboard_templates/`)

Pre-built Grafana dashboard JSON templates:
- `api_service_dashboard.json` - RED method dashboard for API services
- `database_dashboard.json` - USE method dashboard for databases
- `kubernetes_dashboard.json` - Cluster and workload metrics
- `slo_overview_dashboard.json` - Error budget and SLO tracking

**NewRelic Dashboard Templates:**
- `newrelic_service_overview.json` - RED method dashboard with NRQL queries
- `newrelic_slo_dashboard.json` - SLO tracking with burn rate visualization

### Alert Templates (`assets/alert_templates/`)

Production-ready alert rule templates:
- `availability_alerts.yaml` - Service availability alerts
- `latency_alerts.yaml` - Latency percentile alerts
- `resource_alerts.yaml` - CPU, memory, disk alerts
- `slo_burn_rate_alerts.yaml` - Multi-window burn rate alerts

**NewRelic Alert Templates:**
- `newrelic_slo_alerts.json` - Multi-burn-rate NRQL alert conditions
- `newrelic_infrastructure_alerts.json` - CPU, memory, disk, container alerts

### Runbook Template (`assets/runbook_template.md`)

Standardized incident response runbook format with sections for alert context, diagnostic steps, remediation actions, and escalation criteria.

## Key Workflows

### Workflow 1: Full Observability Stack Implementation

**Goal:** Deploy comprehensive observability infrastructure for microservices.

**Duration:** 4-6 hours

**Steps:**
1. Analyze service architecture and identify observability requirements
2. Deploy Prometheus with ServiceMonitor configurations
3. Generate Grafana dashboards using `dashboard_generator.py`
4. Configure centralized logging with Loki or ELK
5. Deploy Jaeger for distributed tracing
6. Set up AlertManager with `alert_rule_generator.py`
7. Validate end-to-end observability flow

### Workflow 2: SLI/SLO Framework Definition

**Goal:** Define Service Level Indicators and Objectives with error budget policies.

**Duration:** 2-3 hours

**Steps:**
1. Identify critical user journeys and service boundaries
2. Calculate baseline metrics using `slo_calculator.py`
3. Define SLIs for availability, latency, and throughput
4. Set SLO targets based on service tier and business requirements
5. Configure multi-burn-rate alerting rules
6. Create SLO dashboard for error budget tracking
7. Document error budget policies and escalation procedures

### Workflow 3: Alert Design and Runbook Creation

**Goal:** Design symptom-based alerting with comprehensive runbooks.

**Duration:** 3-4 hours

**Steps:**
1. Audit existing alerts for noise and gaps
2. Generate optimized alert rules using `alert_rule_generator.py`
3. Create runbook templates for each alert type
4. Configure escalation policies and notification channels
5. Test alert firing and notification delivery
6. Document on-call procedures and handoff protocols

### Workflow 4: Dashboard Design for Service Health

**Goal:** Create comprehensive dashboards using RED/USE methodologies.

**Duration:** 2-3 hours

**Steps:**
1. Define dashboard requirements per service type
2. Generate dashboard configurations using `dashboard_generator.py`
3. Add variable templating for multi-service views
4. Configure annotations for deployments and incidents
5. Set up dashboard provisioning for GitOps workflows
6. Document dashboard usage and interpretation

## Best Practices Summary

### Monitoring
- Instrument the Four Golden Signals for every service
- Use RED method for request-driven services, USE method for resources
- Maintain metric cardinality below 10,000 series per service
- Set appropriate scrape intervals (15-30s for most metrics)

### Logging
- Use structured JSON logging for machine parseability
- Include correlation IDs in all log entries
- Log at appropriate levels (ERROR for failures, INFO for state changes)
- Implement log sampling for high-volume debug logs

### Tracing
- Instrument 100% of entry points, sample at collection
- Propagate trace context across all service boundaries
- Use tail-based sampling for error and slow traces
- Keep trace retention to 7-14 days for cost management

### Alerting
- Alert on symptoms (user-facing impact), not causes
- Use multi-window burn rates for SLO-based alerting
- Maintain 1:1 ratio of alerts to runbooks
- Review alert noise monthly and tune thresholds

## Common Commands

```bash
# Generate API service dashboard (Grafana)
python3 scripts/dashboard_generator.py -s my-api -t api -p grafana -o json

# Generate API service dashboard (NewRelic)
python3 scripts/dashboard_generator.py -s my-api -t api -p newrelic -o json

# Generate database dashboard
python3 scripts/dashboard_generator.py -s my-db -t database -p grafana -o json

# Create SLO-based alerts for 99.9% availability (Prometheus)
python3 scripts/alert_rule_generator.py -s my-api --slo-target 99.9 -p prometheus -o yaml

# Create SLO-based alerts for 99.9% availability (NewRelic)
python3 scripts/alert_rule_generator.py -s my-api --slo-target 99.9 -p newrelic -o json

# Calculate error budget from metrics export
python3 scripts/slo_calculator.py -i prometheus_export.csv --target 99.9 --window 30d -o markdown

# Detect anomalies in latency metrics
python3 scripts/metrics_analyzer.py -i metrics.csv --analysis-type anomaly --threshold 3.0 -o json

# Analyze metric cardinality
python3 scripts/metrics_analyzer.py -i metrics.csv --analysis-type cardinality -o text
```

## Troubleshooting

### High Cardinality Metrics
**Problem:** Prometheus memory usage growing, queries timing out
**Solution:** Use `metrics_analyzer.py --analysis-type cardinality` to identify high-cardinality labels, then aggregate or drop unnecessary labels

### Alert Fatigue
**Problem:** Too many alerts, on-call burnout
**Solution:** Implement multi-burn-rate alerting using `alert_rule_generator.py`, add inhibition rules, increase alert thresholds for non-critical services

### Missing Traces
**Problem:** Traces not connecting across services
**Solution:** Verify trace context propagation headers (traceparent, W3C format), check sampling configuration, ensure OpenTelemetry collector is receiving spans

### Dashboard Performance
**Problem:** Grafana dashboards loading slowly
**Solution:** Use recording rules for expensive queries, reduce time range defaults, add query caching, limit panel count per dashboard

## Resources

- [Monitoring Patterns Reference](references/monitoring_patterns.md)
- [NewRelic Patterns Reference](references/newrelic_patterns.md)
- [Logging Architecture Reference](references/logging_architecture.md)
- [Distributed Tracing Reference](references/distributed_tracing.md)
- [Alerting and Runbooks Reference](references/alerting_runbooks.md)
- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [NewRelic NRQL Documentation](https://docs.newrelic.com/docs/nrql/get-started/introduction-nrql-new-relics-query-language/)
