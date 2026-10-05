---
name: performance-monitoring
displayName: Performance Monitoring
tagline: Set up application performance monitoring with alerts, dashboards, and SLO tracking.
description: |
  Configures application performance monitoring with real-time dashboards,
  alerting rules, and SLO/SLI tracking. Monitors response times, error rates,
  throughput, and resource utilization. Sets up intelligent alerts that reduce
  noise while catching real issues.
department:
  - Engineering
  - DevOps
  - SRE
use_cases:
  - Monitoring
  - Observability
  - SRE
tools_required:
  - Grafana MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Set up monitoring for our payment service.
  SLO: 99.9% availability, P99 latency < 200ms.
exampleOutput: |
  Monitoring Setup — Payment Service

  DASHBOARDS
  1. Service Overview: requests/sec, error rate, latency percentiles
  2. Resource Usage: CPU, memory, connections, disk I/O
  3. Business Metrics: transactions/min, revenue impact, cart abandonment

  ALERTS
  Critical:  Error rate > 1% for 5 min
  Warning:   P99 latency > 200ms for 10 min
  Info:      Traffic spike > 2x baseline

  SLO TRACKING
  Availability:  99.9% (budget: 43.8 min/month)
  Latency:       P99 < 200ms (current: 142ms)
  Error Budget:  72% remaining this month
---

# Performance Monitoring

Set up application performance monitoring with alerts, dashboards, and SLO tracking.

**Integrations:** Grafana

## When to Use

- The user wants to set up monitoring for services or applications
- SLOs need to be defined and tracked
- The user mentions "monitoring", "alerts", "SLO", or "observability"

## Steps

### Step 1: Define SLOs

Establish service level objectives for availability and latency.

### Step 2: Create Dashboards

Build monitoring dashboards with key metrics.

### Step 3: Configure Alerts

Set up alerting rules with appropriate thresholds and escalation.

## Output

Deliver:
- Monitoring dashboard configuration
- Alert rules with escalation paths
- SLO tracking and error budget reports
