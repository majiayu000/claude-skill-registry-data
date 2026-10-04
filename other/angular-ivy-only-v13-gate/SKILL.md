---
id: angular.ivy.angular-ivy-only-v13-gate
name: Angular Ivy Only v13 Gate
description: >
  Gate Angular upgrades on Ivy-only readiness. Use when the project is moving to Angular 13+ and View Engine or ngcc compatibility must be explicitly resolved before the upgrade can proceed.
stack:
  - Angular
  - TypeScript
category: ivy
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Ivy only
  - View Engine
  - ngcc
compatibility:
  angular:
    min: "13"
---

# Angular Ivy Only v13 Gate

## Purpose

Gate Angular upgrades on Ivy-only readiness.

## When to Use

- The project is moving to Angular 13+.
- View Engine or ngcc compatibility must be reviewed.

## When Not to Use

- The project is already Ivy-only.

## Required Inputs

- libraries
- ngcc status
- View Engine artifacts

## Procedure

1. Review Ivy readiness.
2. Identify blockers.
3. Decide gate status.

## Do

- Keep the gate explicit.

## Do Not

- Do not pass the gate with unresolved blockers.

## Review Checklist

- [ ] Ivy readiness is known.
- [ ] Blockers are explicit.

## Expected Output

1. Ivy gate decision.

## Exit Criteria

- Ivy gate is explicit.
