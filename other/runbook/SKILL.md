---
name: runbook
description: Write an operational runbook that turns a recurring or incident response task into safe prerequisites, diagnostics, actions, verification, rollback or recovery, escalation, and evidence capture.
---
# Runbook

Use when operators need a reliable procedure for maintaining, diagnosing, restoring, or changing a technical system.

## Procedure
1. Define the situation or trigger, target system, audience, required access, safety constraints, and authoritative environment in scope.
2. State prerequisites and prechecks before any mutating command, especially for production, data, networking, security, or destructive operations.
3. Provide diagnostic steps that establish current state and distinguish common failure classes before remediation.
4. Give exact commands, dashboards, paths, queries, or controls with placeholders and explanation of expected evidence.
5. Define decision branches and stop conditions so operators know when a symptom requires a different procedure or specialist.
6. Include validation from the service or user perspective, not merely command success.
7. Document rollback or forward-recovery, data or access risks, and escalation paths with the evidence the receiving owner needs.
8. Test the runbook in a representative environment or exercise and update steps that rely on hidden local knowledge.

## Decision rules
- A runbook should help an operator decide, not merely paste commands.
- Mutating steps need clear prerequisites and verification.
- Never embed real credentials or machine-specific secrets.
- Fleet placement can change; refer to stable services, profile identities, or runtime discovery rather than hard-coded nodes unless the runbook is intentionally host-specific.

## Quality gate
The runbook is ready when a qualified operator can establish state, execute the correct branch safely, verify the real outcome, recover or escalate with evidence, and complete the procedure without undocumented access, environment, or machine assumptions.