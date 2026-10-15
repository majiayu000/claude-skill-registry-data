---
name: governance-script-generator
description: "Generate production-ready PowerShell and PAC CLI scripts for Power Platform governance. Use for auditing apps/flows/environments, orphaned resources, capacity and license monitoring, DLP enforcement, environment lifecycle, CoE Starter Kit patterns, governance reports."
---

# Power Platform Governance Script Generator

Translate a natural-language governance requirement into a robust, documented PowerShell, PAC CLI or hybrid script that follows Microsoft best practices and fails safely. The scripts manage critical business applications: reliability, safety and clear documentation come before brevity.

## Choose the tool

| Use case | Tool | Why |
|---|---|---|
| Solution management, environment create/delete, data export/import | PAC CLI | Native operations, simpler syntax |
| PCF development, connector management | PAC CLI | Native support |
| Bulk resource auditing, custom reporting | PowerShell | Better filtering and objects |
| Complex logic, cross-environment orchestration | PowerShell | Flexible control flow |
| API rate limit handling | PowerShell | Advanced retry logic |

Hybrid: PowerShell orchestrates (`Get-AdminPowerAppEnvironment` loop), PAC CLI performs single operations (`pac solution export --environment ...`).

## Workflow

1. **Understand**: governance objective, resources (apps, flows, environments), action (audit, disable, delete, reassign, notify), one-time or scheduled, safety needs (dry-run, approval, rollback).
2. **Choose tools**: PAC CLI, PowerShell or hybrid. Identify modules, authentication and error strategy.
3. **Generate** from `references/script-template.md` (header, validated parameters, prerequisites check, authentication, main logic with error handling, reporting, cleanup). Reuse `references/common-patterns.md` (auditing, bulk with progress, confirmation, email notification, PAC CLI loop).
4. **Add safety features** (below).
5. **Document usage**: prerequisites, parameters, examples, scheduling, troubleshooting.

Read the references before generating complex scripts:
- `references/pac-cli-reference.md`: PAC CLI commands, parameters, examples.
- `references/powershell-reference.md`: Power Platform cmdlets and usage patterns.
- `references/governance-patterns.md`: governance scenarios and implementations.
- `references/examples-and-advanced.md`: worked requests (audit, cleanup, monitoring), multi-cloud endpoints, parallel processing, interim reporting.

## Safety guidelines

Destructive operations:
- Implement `-WhatIf` / `$DryRun`.
- Require explicit confirmation for production.
- Back up before deletion and log every deletion in full.
- Roll out in phases (test then prod).

Bulk operations:
- Start with a small test batch, set batch size limits, add delays, monitor rate limiting, allow pause/resume.

Automated scripts:
- Use service principal authentication and store credentials in Azure Key Vault.
- Add health checks, failure alerting and audit logs.

## Checklist before delivering

- Authentication handled (interactive or service principal), prerequisites documented.
- try/catch with retry logic, logging to console and file, progress for long runs.
- Parameters typed and validated, edge cases handled (empty results, nulls).
- Output exported to files, rate limiting handled, rollback strategy for destructive operations.
- Syntax valid for PowerShell 5.1+, cmdlets taken from the correct modules, comments on non-obvious code.

## Response format

Brief approach, the complete script, then Prerequisites, Parameters, Usage Examples (2-3 commands), Scheduling (Azure Automation, Task Scheduler), Notes (including common errors and debug mode).

## Non-negotiables

- Always read reference documentation before complex scripts. Never assume cmdlet parameters: verify them.
- Always include error handling, logging and a dry-run for destructive operations.
- Never hardcode credentials or sensitive data.
- Never skip authentication validation or prerequisite checking.
- Always consider rate limiting for bulk operations.

## Success criteria

A script runs unmodified on a properly configured system, handles errors with clear messages, shows progress, produces actionable reports, is documented, can be scheduled, and carries safety features for production use.
