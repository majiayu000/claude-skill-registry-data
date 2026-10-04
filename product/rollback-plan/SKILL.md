---
name: rollback-plan
description: Create rollback and fallback plans for deployments, releases, migrations, feature flags, and production changes. Use when Codex is asked to define rollback triggers, recovery steps, data restore needs, communication, or post-rollback validation.
license: MIT
---

# Rollback Plan

## Core Workflow

1. Identify change type, affected users, state changes, data migrations, and
   dependencies.
2. Define rollback triggers, decision owner, time window, and monitoring
   signals.
3. Document rollback steps, fallback alternatives, feature-flag switches,
   restore procedures, and verification checks.
4. Separate reversible code/config changes from irreversible data changes.
5. Include customer/support communication and incident handoff when relevant.
6. Add post-rollback validation and follow-up actions.

## Safety Rules

- Do not claim rollback is possible when data or external side effects are
  irreversible.
- Do not run rollback commands or restore data without explicit approval.
- Escalate rollbacks involving migrations, payments, auth, customer data, or
  regulatory impact.

## Deliverable Shape

For rollback plans, provide:

- Change scope
- Rollback triggers and owner
- Reversible and irreversible parts
- Rollback steps
- Fallback path
- Validation checks
- Communication plan
- Follow-up actions

## References

- Read `references/rollback-plan-checklist.md` when preparing rollback or
  fallback plans.
