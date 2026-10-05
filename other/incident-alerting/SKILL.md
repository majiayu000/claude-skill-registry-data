---
name: incident-alerting
displayName: Incident Alerting
tagline: Configure intelligent incident alerting with escalation policies and on-call routing.
description: |
  Sets up incident alerting workflows with smart routing, escalation
  policies, and noise reduction. Configures alert grouping to prevent
  alert fatigue, routes incidents to the right on-call engineer, and
  provides runbooks for common scenarios. Integrates with monitoring
  and communication tools.
department:
  - Engineering
  - DevOps
  - SRE
use_cases:
  - Incident Management
  - On-call Management
  - Alert Configuration
tools_required:
  - Slack MCP
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
  Set up incident alerting for our platform.
  On-call rotation: 4 engineers, weekly rotation.
  Escalation: page after 5 min, escalate to manager after 15 min.
exampleOutput: |
  Incident Alerting — Platform

  ON-CALL ROTATION
  Week 1: @alice  |  Week 2: @bob  |  Week 3: @carol  |  Week 4: @dave

  ESCALATION POLICY
  0 min:   Slack #incidents + page on-call engineer
  5 min:   Re-page if no acknowledgment
  15 min:  Escalate to engineering manager
  30 min:  Escalate to VP of Engineering

  ALERT GROUPING
  - Group by service name (5 min window)
  - Suppress duplicate alerts for same root cause
  - Auto-resolve when metrics recover for 10 min

  RUNBOOKS LINKED
  - High error rate: check recent deployments, rollback if needed
  - Latency spike: check database connections, scale if needed
  - Memory pressure: restart pods, investigate leak
---

# Incident Alerting

Configure intelligent incident alerting with escalation policies and on-call routing.

**Integrations:** Slack, Grafana

## When to Use

- The user wants to set up incident alerting and on-call rotations
- Alert fatigue needs to be reduced with smart grouping
- The user mentions "incident alerting", "on-call", or "escalation policy"

## Steps

### Step 1: Define On-call Rotation

Configure team rotation schedule and coverage rules.

### Step 2: Set Escalation Policy

Define escalation tiers with timeouts and notification channels.

### Step 3: Configure Alert Grouping

Set up alert deduplication and noise reduction rules.

### Step 4: Link Runbooks

Attach response procedures to common alert types.

## Output

Deliver:
- On-call rotation schedule
- Escalation policy configuration
- Alert grouping rules
- Runbook templates for common incidents
