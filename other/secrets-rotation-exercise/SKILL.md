---
name: secrets-rotation-exercise
description: "Use when rehearsing rotation of an application credential or signing token across its dependent services; not for storing or revealing the secret itself."
---

# Secrets Rotation Exercise

## Purpose

Prove that credential rotation can be completed, verified, and recovered without an unsafe outage or lingering old credential.

## Required inputs

Credential owner, affected consumers, secret manager, overlap/revocation policy, health checks, emergency rollback policy, and an approved non-production environment.

## Workflow

1. Inventory consumers and cached copies; establish a baseline health check and identify the safe rotation order.
2. Create the replacement credential using the approved secret-management path, distribute it without placing the value in logs or artifacts, and validate new authentication.
3. Move consumers in controlled stages while measuring failures; test restart and scale-out so stale environment values or replicas are not missed.
4. Revoke the old credential according to the approved overlap policy, then verify old-credential rejection and record residual dependencies.

## Verification checklist

- [ ] The new credential is validated before the old one is revoked.
- [ ] Consumer inventory covers background workers, scheduled jobs, replicas, and local development secrets as applicable.
- [ ] Old credentials stop working after the documented deadline.
- [ ] Rollback does not require publishing the secret into chat, tickets, or shell history.

## Required output

A rotation exercise report with consumer inventory, stage outcomes, revocation evidence, and follow-up owners.

## Boundaries and failure handling

Use an authorized staging credential first. Never print, paste, or commit raw secrets; do not rotate production credentials without explicit approval.

When required evidence, permissions, or environment details are unavailable, stop at the supported analysis, record the missing prerequisite, and do not report an unexecuted validation as passing.

## Trigger examples

- **Positive:** The team needs to prove that a leaked service token can be replaced promptly.
- **Negative:** Scanning the repository for existing secret literals without executing a rotation workflow.
