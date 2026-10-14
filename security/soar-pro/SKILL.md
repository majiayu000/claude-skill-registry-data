---
name: soar-pro
description: Build security orchestration and automation — playbooks that enrich, contain, and close the loop on repetitive response work.
category: security
---

## Overview

SOAR (Security Orchestration, Automation, and Response) connects security tools into automated playbooks: an alert fires, the playbook enriches it with threat intel and asset context, and — for well-understood cases — takes containment action automatically. Done right, it multiplies analyst capacity and slashes response times. Done wrong, it auto-remediates the CEO's laptop.

This skill covers the automation discipline: which workflows to automate, playbook design with safety gates, testing, and measuring automation ROI without creating new risks.

Automation earns trust gradually: start with enrichment and notification (read-only actions), progress to low-risk containment with human approval, and only then to fully automatic response for narrow, high-confidence scenarios. Every step up the ladder requires evidence from the step below.

## When to use

- Reducing analyst toil on repetitive triage (phishing inbox, IOC enrichment, user lookups).
- Cutting containment time for well-understood threats (known-malicious hash on one host).
- Standardizing response actions across shifts and analysts.
- Measuring and improving SOC efficiency at scale.

## Core concepts

- **Automation ladder:** enrich/notify → recommend action → act with approval → act automatically with rollback → act automatically. Climb one rung at a time per playbook, with evidence.
- **Playbook anatomy:** trigger, enrichment (intel, asset, identity context), decision logic (confidence thresholds), actions (with safety gates), logging, and rollback. Every playbook documents its blast radius.
- **Human-in-the-loop gates:** any action affecting users, production systems, or external parties needs approval or very narrow pre-authorization. Auto-isolating the wrong host is an outage you caused.
- **Idempotency and safety:** playbooks must handle re-runs safely (already-isolated host, already-blocked IOC) and fail closed — unclear state means stop and escalate, never guess.
- **Confidence thresholds:** automation acts only when confidence is high and impact is bounded. "Probably malicious" gets enrichment and a recommendation, not automatic containment.
- **Integration hygiene:** API credentials for every connected tool, scoped to minimum necessary permissions, rotated regularly, with health checks — a playbook is only as reliable as its weakest integration.
- **Testing discipline:** playbooks tested in lab/staging with simulated triggers before production; chaos-test the failure modes (API down, partial enrichment, timeout).
- **Audit everything:** every automated action logged with trigger, inputs, decision rationale, and outcome — automation without auditability is unaccountable.

- **Playbook versioning and rollback.** Version every playbook change; keep the last-known-good version deployable in one step — a bad playbook update can mass-misbehave.
- **Blast-radius documentation.** Each playbook states exactly what it can touch and the maximum impact of a wrong decision. Reviewers check the blast radius first.

## Practical workflow

1. **Pick the right first playbooks:** high-volume, low-variance workflows — phishing triage enrichment, IOC reputation checks, new-user risk context. Measure baseline analyst time per case first.
2. **Design with gates:** map the decision tree, define confidence thresholds, place human approvals before impactful actions, and document rollback for every action.
3. **Build and test:** implement against staging; simulate triggers including edge cases (missing data, API failures, duplicate triggers); verify idempotency and fail-closed behavior.
4. **Deploy progressively:** shadow mode (log what it would do) → recommend mode → approval mode → automatic for the narrowest high-confidence slice. Advance on evidence, not schedule.
5. **Monitor playbook health:** execution success rate, action outcomes, override rate (analysts undoing automation is a signal), and integration health. Alert on playbook failures like any production system.
6. **Measure ROI honestly:** analyst hours saved, MTTR reduction on automated case types, and error rate vs manual handling — plus the cost of building and maintaining the automation.

### Sustaining the practice

- Review playbook logic quarterly against current threats and tool APIs
- Track override rates; high overrides mean the playbook's judgment is wrong
- Retire playbooks for deprecated tools or resolved threat patterns
- Share playbook patterns across teams; avoid duplicate automation

### Earning autonomy

- Require 30 days of recommend-mode data before enabling approval-mode
- Require 90 days of approval-mode with low override rates before automatic action
- Automatic actions limited to reversible, narrowly-scoped, high-confidence cases
- Every autonomy increase gets a written risk sign-off, not just a ticket

### Metrics that prove it works

- % of eligible cases handled by automation, by playbook
- MTTR for automated case types vs manual baseline
- Automation error/override rate (target: lower than human error rate)
- Analyst hours reclaimed per quarter

## Common pitfalls

- **Automating a broken process.** If the manual workflow is inconsistent, automation scales the inconsistency. Fix the process, then automate it.
- **Skipping the ladder.** Going from idea to fully automatic containment without the evidence rungs is how you auto-quarantine the finance server.
- **No rollback planning.** Every action needs an undo path tested before the action is automated. "We can fix it manually" is not a rollback plan.
- **Alert-to-playbook sprawl.** Dozens of overlapping playbooks with unclear ownership become unmaintainable. Govern the catalog like code.
- **Ignoring integration failures.** A playbook that silently skips enrichment when the intel API is down makes decisions on partial data. Fail closed and alert.
- **Measuring activity instead of outcomes.** "Playbook ran 10,000 times" means nothing if analysts still do the work. Measure hours saved and MTTR delta.
- **Automating external communications.** Auto-sending emails to users or external parties without review risks confusion and liability. Keep humans on outbound comms.
- **Set-and-forget playbooks.** Threats change, APIs change, asset inventories change. Unmaintained playbooks decay into wrong actions executed confidently.
- **Playbooks with hardcoded credentials.** Automation credentials in playbook code or configs are secrets in code. Vault them with rotation like any other secret.
- **No kill switch.** Every automation needs a global pause that works in seconds. When a playbook misbehaves at scale, you will not have time for a change ticket.
