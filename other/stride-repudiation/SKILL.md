---
name: stride-repudiation
description: Generate Repudiation threats for a system, repo, architecture, or data flow. Use when Codex needs to identify where actors can deny actions, where evidence is weak or missing, or where logging, auditability, provenance, and accountability are insufficient.
---

# STRIDE Repudiation

## Overview

Use this skill to generate threat ideas specifically in the Repudiation category of STRIDE. Focus on actions that cannot be reliably attributed, proven, or reconstructed after the fact.

Prefer threats tied to concrete audit gaps, provenance breaks, and weak evidence trails over generic "logging is missing" comments.

## Workflow

### 1. Establish the modeling scope

Choose one concrete slice first:

- one privileged workflow
- one customer-facing transaction
- one admin or support action path
- one automation or background job
- one integration that changes system state

### 2. Identify important actions and evidence sources

Look for:

- creates, updates, deletes, approvals, exports, and configuration changes
- login, logout, reset, impersonation, and delegation actions
- audit logs, event logs, traces, version history, and change records
- request metadata, actor identity, tenant context, timestamps, and correlation IDs
- signatures, receipts, approvals, or immutable append-only records

### 3. Generate Repudiation threats

Generate threats around:

- missing or incomplete audit logs
- actions logged without reliable actor identity
- mutable or deletable logs
- missing tenant, request, or object context in evidence
- support or admin actions with poor accountability
- shared accounts or shared credentials
- asynchronous workflows where original actor attribution is lost
- weak time synchronization or ambiguous event ordering

### 4. Stress accountability assumptions

For each important action, ask:

- Can we prove who performed this action?
- Can we prove what changed and when?
- Can a privileged user alter or erase the evidence?
- Is the acting identity preserved across async jobs or downstream systems?
- Are user-visible actions distinguishable from automated or system actions?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or workflow affected
- repudiation scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Repudiation threats.

Do not drift into Spoofing or Tampering unless the core issue is inability to prove or attribute an action.

## Example Requests

- Generate Repudiation threats for this admin workflow.
- Review this repo and identify gaps in auditability and accountability.
- Use this design to find where state changes cannot be reliably attributed.
