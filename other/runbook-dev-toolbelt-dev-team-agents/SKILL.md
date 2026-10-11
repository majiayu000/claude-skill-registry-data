---
name: runbook
description: How to write an operational runbook — incident response and maintenance procedures.
---

# Runbook Protocol

A runbook documents how to respond to a specific operational event (incident, scheduled maintenance, deployment). Use the template at `.dev-team-agents/templates/runbook-template.md`.

## When to Create a Runbook

- Production incidents that recur or have multi-step mitigation
- Deployment procedures with more than 3 sequential steps
- On-call escalation paths
- Scheduled maintenance windows

## Runbook Structure (see `.dev-team-agents/templates/runbook-template.md`)

1. **Title and severity** — incident type and impact level
2. **Symptoms** — observable signals that triggered this runbook
3. **Diagnosis steps** — commands to run, logs to check
4. **Mitigation steps** — ordered actions to resolve
5. **Rollback** — how to undo if mitigation fails
6. **Post-mortem checklist** — actions after resolution

## Loading Instructions

Load `.dev-team-agents/templates/runbook-template.md` and fill in each section. Keep steps atomic (one action per step). Include exact commands, not descriptions of commands.
