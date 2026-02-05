---
name: automation/skill-smoke-bench
description: Run lightweight import/exec smoke tests for skills and report pass/fail. Use in CI/CD or after creating new skills.
---

# Skill Smoke Bench

Capabilities
- import_check: ensure skills load without ImportError.
- stub_exec: call minimal functions to ensure runtime viability.
- report_results: emit pass/fail summary and store for history.

Dependencies
- ops-chief-of-staff (optional scheduling)
- tangible-memory (optional storage)

Inputs
- list of skill modules/paths to check.

Outputs
- results summary with errors, optional persisted log.
