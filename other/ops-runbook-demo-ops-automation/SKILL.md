---
name: ops-runbook-demo-ops-automation
description: Use when running ops automation workflows for ops-runbook-demo.
---

# ops-runbook-demo-ops-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Operations automation workflows for recurring checks, monitors, and runbooks.

## Workflow
- Identify the service, environment, and operational objective
- Check current state before making changes
- Run the least invasive command that proves or fixes the issue
- Record verification output and any remaining risk

## Commands
- install: `npm install`
- test: `npm test`
- doctor: `npm run doctor`
- check: `npm run check`

## Principles
- Make every operational action observable and auditable
- Prefer idempotent commands with clear rollback paths
- Escalate destructive or credential-sensitive actions before execution
