---
name: liveops-incident-response
description: Use when a live production service outage needs incident-controlled service or database mitigation, an incident commander, containment, timeline, player communications, recovery, and postmortem.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [service, client, database, network]
metadata:
  studio:
    type: workflow
    lifecycle_stage: operate
    risk_level: high
    packs: [production-design-liveops]
    side_effects: network
    artifact: liveops-incident-record.json
    required_evidence: [incident-timeline, impact-assessment, command-authority, recovery-validation]
    owner: HoaTV Studio
    reviewer: Incident Commander
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, studio-handoff, evidence-first-debugging]
      copied_text: none
---
# Liveops Incident Response

## Overview
Create a calm, evidence-based incident record and decision structure while preserving explicit human authority over production changes.

## When to use
Use for outages, severe latency, failed deployments, exploit waves, economy abuse, data integrity risk, authentication failures, or player-impacting service degradation.

## When NOT to use
Do not use for routine bug triage, speculative incidents without observable impact, or autonomous production commands.

## Required inputs and context discovery
Collect incident start time, affected services and regions, player impact, dashboards, alerts, deployment history, build and configuration identity, security or privacy indicators, incident commander, communication owner, authorized runbooks, rollback state, and protected credentials.

## Safety and risk level
High-risk production context. Read-only diagnosis may proceed, but service control, traffic changes, rollback, database writes, bans, credential rotation, and public communication require explicit authority for the exact action. Otherwise mark them `BLOCKED`.

## Workflow
1. Establish incident command, severity, scope, communication channel, and decision log.
   Completion criterion: one incident commander and current impact statement are explicit.
2. Preserve a timestamped timeline of alerts, observations, hypotheses, and actions.
   Completion criterion: facts are separated from assumptions and every action names its actor.
3. Stabilize by proposing the smallest reversible mitigations from approved runbooks.
   Completion criterion: unapproved production actions remain `BLOCKED` with risk and owner.
4. Validate recovery against player-facing and system health indicators.
   Completion criterion: recovery is not declared from one metric or absence of alerts alone.
5. Hand off monitoring, follow-up defects, security review, and post-incident analysis.
   Completion criterion: owners, deadlines, evidence paths, and residual risks are recorded.

## Evidence and output contract
Produce `liveops-incident-record.json` with severity, scope, command roles, timeline, evidence, hypotheses, authorized actions, blocked actions, recovery validation, communications, and follow-ups.

## Handoff contract
Record current status, affected players, mitigations, rollback state, monitoring window, residual risks, security/privacy escalation, next commander, and pending approvals.

## Pitfalls and anti-rationalization
- Urgency does not expand command authority.
- Silence in alerts does not prove player recovery.
- Do not paste secrets, tokens, or sensitive player data into incident artifacts.
- Preserve timestamps and actors; do not rewrite the timeline after the fact.

## Verification checklist
- [ ] Incident commander and severity are explicit.
- [ ] Facts, hypotheses, and actions are separated.
- [ ] Every production action has exact authority.
- [ ] Recovery uses multiple relevant indicators.
- [ ] Residual risks and follow-up owners are recorded.

## References and scripts
Read [references/commands.md](references/commands.md) for read-only identity, timeline, deploy-correlation, multi-indicator impact, and abuse-signal commands, plus the table of actions that stay `BLOCKED` without explicit authority. Use project-specific approved incident and rollback runbooks. This kit contains no production service-control runner; unavailable access remains `BLOCKED`.
