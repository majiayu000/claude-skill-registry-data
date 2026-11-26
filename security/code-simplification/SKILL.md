---
name: code-simplification
description: Use after a feature or fix is verified to simplify the changed code without changing behavior — wraps Claude Code's /simplify with finance and security carve-outs.
type: skill
user-invocable: false
---

# Code Simplification

## Overview

Simplify only verified code, only in the task's files. On Claude Code, run the built-in `/simplify` on the change; elsewhere, apply the same pass by hand. Then re-run build and tests.

## When To Use

- Implement Phase 6, or after a fix is green

## Workflow

**Never simplify away** — presumed load-bearing; if one looks dead, surface it to `security-and-hardening`:
- money arithmetic, decimal types, and rounding mode or order
- idempotency keys, deduplication, retry and concurrency guards
- audit-trail and compliance logging
- authn/authz checks, secret handling and redaction, trust-boundary validation
- migrations, and guards on delete/destructive operations

## Verification

- [ ] Behavior unchanged; build and tests pass; no carve-out removed or collapsed
