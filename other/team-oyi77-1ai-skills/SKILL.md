---
name: operations-team
description: Use when execute SOPs, triage on-call incidents, manage SLA breaches,
  and drive continuous improvement using lean operations principles. Use when working
  with operations team.
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business-ops
- management
- operations
- team
version: 1.0.0
category: operations
---


# Operations Team

## When to Use

**Trigger phrases:**
- "operations team"
- "Help me with operations team"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Execute SOPs, handle on-call triage, manage SLA breaches.


## When NOT to Use

- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat


## Overview

The Operations Team executes SOPs, triages on-call incidents, manages SLA breaches, and drives continuous improvement using lean principles. This skill provides the structure to run a team as a well-oiled machine — repeatable, measurable, and continuously improving.

**Key areas covered:**
- **SOP Management** — Author, version, distribute, and retire standard operating procedures. Every SOP has a clear purpose, owner, review cadence, and audit trail.
- **SLA Tracking** — Define service-level targets, measure compliance, manage breaches with escalation workflows, and report on trends. SLAs are tied to specific operational workflows with measurable SLOs.
- **Incident Triage** — On-call rotation, severity classification, initial response playbooks, escalation paths, and post-incident reviews.
- **Continuous Improvement** — Use data from SLAs and incidents to drive lean process improvements. Kaizen, retrospectives, and process audits.

## Workflow

The operational cadence follows a standard pattern across daily, weekly, and monthly cycles, with a process-improvement loop running in parallel.

### Daily Cadence
- **Stand-up** — 15-min sync: what was done, what's blocked, what's next. Triage new incidents and assign.
- **Queue Triage** — Review incoming tickets/requests, classify by severity, assign or defer.
- **SLA Monitor Check** — Scan active SLA timers. Flag approaching breaches. Escalate if at risk.
- **End-of-Day Summary** — Brief log of completed work, open items, handoff notes for next shift.

### Weekly Cadence
- **Operational Review** — 30-min meeting: SLA compliance for the week, incident trends, open process improvement items.
- **SOP Audit** — Select 1-2 SOPs for review. Verify they reflect current reality. Update if needed.
- **Escalation Debrief** — Review any escalated incidents from the week. Was escalation appropriate? Were response times met?
- **Capacity Check** — Assess team workload. Rebalance assignments if needed.

### Monthly Cadence
- **KPI Deep Dive** — Full review of all operational metrics: SLA compliance, error rates, throughput, team satisfaction.
- **Process Retrospective** — Root-cause analysis on SLA breaches and recurring issues. Identify improvement opportunities.
- **SOP Rotation** — Publish updated SOPs. Archive retired ones. Communicate changes to stakeholders.
- **Report Distribution** — Monthly operations report to stakeholders: highlights, breaches, improvements, next month's focus.

### Improvement Loop
1. **Assess** — Evaluate current state, identify gaps from KPI and incident data
2. **Design** — Propose process or SOP changes to close gaps
3. **Implement** — Roll out changes with team alignment and training
4. **Measure** — Track post-change KPIs against baseline
5. **Iterate** — Repeat; drive continuous improvement based on measured outcomes

## SOP Template

- **Purpose** — Why this process exists
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions
- **Escalation** — When and how to escalate
- **Review** — Schedule for periodic updates

## Key Metrics

- Process completion time
- Error/rework rate
- Team satisfaction scores
- Cost per operation
- SLA compliance rate

## Common Pitfalls

- **SOP debt** — Writing SOPs once and never reviewing them. SOPs drift as processes change. Set a recurring review cadence (quarterly minimum) and assign an owner to each.
- **Metric without action** — Tracking KPIs without acting on the data. If SLA compliance drops three weeks in a row, a response is required — not just another dashboard refresh.
- **Over-automation** — Automating a process that should not exist. Optimize the workflow first, then automate. Automating waste just produces waste faster.
- **Blaming the operator** — Treating human error as root cause instead of examining process, tooling, and training gaps. Every "human error" is a process failure until proven otherwise.
- **One-size-fits-all SLAs** — Applying the same SLA to every request regardless of priority. Tiered SLAs (critical, standard, low) prevent firefighting from drowning strategic work.
- **Documentation silo** — SOPs locked in a wiki nobody reads. Publish SOPs where they are accessed: embedded in ticketing workflows, at-on-call runbooks, in onboarding checklists.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |


## Process

### Onboard a New SOP
1. **Identify Need** — Recognize a gap or recurring problem that needs a documented process. Gather input from stakeholders and operators who do the work.
2. **Draft the SOP** — Write using the SOP Template (Purpose, Scope, Procedure, Escalation, Review). Keep procedures to single-page if possible. Include decision trees for non-linear flows.
3. **Review and Validate** — Subject-matter expert reads the draft against real workflow. Correct inaccuracies. Test the procedure with someone unfamiliar with the process.
4. **Approve and Publish** — Stakeholder sign-off. Publish in the team's accessible location (wiki, ticketing system, runbook tool). Announce the change.
5. **Train** — Brief training session for affected team members. Update onboarding materials if the SOP changes standard practice.
6. **Monitor and Update** — Set a review date. Track whether the SOP is being followed. Revise as the process evolves.

### Triage an Incident
1. **Detect** — Alert fires. Confirm it is a real incident (not a test or false alarm).
2. **Classify** — Assign severity (SEV1: outage/critical, SEV2: degraded, SEV3: minor). Set SLA timer.
3. **Respond** — Follow the incident playbook for the detected class. If none exists, contain the impact first.
4. **Resolve** — Apply fix, verify service restoration, close the incident.
5. **Review** — Post-incident review (PIR) within 48 hours. Capture what happened, response timeline, what went well, what to improve.

## Verification

Use this checklist to confirm an operational process or SOP is ready for production:

- [ ] SOP is written, reviewed, and approved before execution begins
- [ ] Clear owner assigned for each process and sub-process
- [ ] SLA targets defined and measurable (not aspirational)
- [ ] Escalation path documented: who to contact, when, how
- [ ] Team trained on the SOP before it takes effect
- [ ] Post-incident review completed within 48 hours for any SEV1/SEV2 event
- [ ] Key metrics defined and baselined before measuring improvement
- [ ] Review cadence set (quarterly minimum) with a specific owner and next-review date
- [ ] SOP is accessible where the work happens — not buried in a wiki nobody visits
- [ ] Handoff procedure documented for shift changes or role transitions

## Monetization

Operations expertise translates into consulting revenue across these service lines:

- **SOP Audit & Remediation** — Review a client's existing SOP library for accuracy, completeness, and adoption. Deliver a gap analysis and updated SOPs. Fixed-price per process or packaged per department.
- **SLA Program Design** — Build tiered SLA frameworks for clients who lack formal service-level agreements. Includes metric definition, measurement tooling recommendations, and breach escalation workflows. Retainer or project-based.
- **Incident Response Playbook Development** — Create or audit incident response playbooks for operations teams. Covers severity classification, on-call rotation design, runbook creation, and post-incident review templates. Deliverable-based.
- **Fractional Operations Lead** — Part-time operational oversight for growing teams (10-50 people) that cannot justify a full-time COO. Monthly retainer with weekly cadence meetings, KPI reporting, and process improvement roadmap.
- **Operations Training** — Team training workshops on SOP authoring, incident triage, SLA management, and lean continuous improvement. Per-session or per-team pricing.
- **Tool Stack Assessment** — Evaluate the client's operational tooling (ticketing, monitoring, documentation). Recommend consolidation or upgrades. Fixed-price assessment report.

**Pricing benchmarks:**
- SOP audit (per process): $500–2,000
- SLA program design (full framework): $3,000–8,000
- Fractional operations lead (monthly): $2,000–5,000
- Incident playbook development: $1,500–4,000
- Training workshop (half-day): $1,500–3,000
## Verification Checklist

- [ ] Incident response time < SLA for all severity levels
- [ ] Runbooks cover >90% of incident types
- [ ] Postmortems completed within 48h
- [ ] Action items from postmortems tracked to completion
- [ ] SLA compliance > 99% monthly
- [ ] On-call rotation sustainable (no burnout signals)
