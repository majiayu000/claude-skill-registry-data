---
name: compliance-tracking
displayName: Compliance Tracking
tagline: Track employee compliance with mandatory training, certifications, and policy acknowledgments.
description: |
  Monitors and tracks employee compliance with mandatory requirements
  including training completions, certification renewals, policy
  acknowledgments, and regulatory deadlines. Sends automated reminders,
  generates compliance reports, and flags overdue items for HR action.
department:
  - HR
  - Legal
  - Compliance
use_cases:
  - Compliance Management
  - Training Tracking
  - Regulatory Compliance
tools_required:
  - BambooHR MCP
  - Slack MCP
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
  Generate a compliance report for Q2.
  Check: security training, SOC 2 acknowledgment, and harassment prevention.
exampleOutput: |
  Compliance Report — Q2 2026

  OVERALL COMPLIANCE: 87%

  SECURITY TRAINING (Annual)
  Completed:    138/150 (92%)
  Overdue:      12 employees — reminders sent
  Deadline:     June 30, 2026

  SOC 2 POLICY ACKNOWLEDGMENT
  Signed:       142/150 (95%)
  Pending:      8 employees — Slack DMs sent
  Deadline:     May 31, 2026

  HARASSMENT PREVENTION (Biennial)
  Completed:    112/150 (75%)
  Overdue:      38 employees — escalated to managers
  Deadline:     July 15, 2026

  ACTION ITEMS
  1. Follow up with 12 security training holdouts (manager CC)
  2. Harassment prevention completion rate below target — schedule makeup sessions
---

# Compliance Tracking

Track employee compliance with mandatory training, certifications, and policy acknowledgments.

**Integrations:** BambooHR, Slack

## When to Use

- HR needs to track compliance across the organization
- Training or certification deadlines are approaching
- The user mentions "compliance tracking", "training completion", or "policy acknowledgment"

## Steps

### Step 1: Define Requirements

List mandatory trainings, certifications, and deadlines.

### Step 2: Check Completion Status

Pull completion data from HR systems and training platforms.

### Step 3: Send Reminders

Notify employees with overdue or upcoming requirements.

### Step 4: Generate Reports

Create compliance reports for HR and leadership.

## Output

Deliver:
- Compliance status by requirement
- Overdue employee list with escalation
- Compliance trend report
