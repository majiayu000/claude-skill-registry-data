---
name: anti-rogue-actions
description: Prevents valid-looking API calls with absurd or destructive outcomes. Enforces business logic guardrails, parameter bounds, permission boundaries, and pre-execution sanity checks.
---

# Anti-Rogue Actions Skill

## Problem

Agents make valid API calls with absurd outcomes. The syntax is correct, the tool exists, the parameters are the right type — but the result is destructive, unauthorized, or nonsensical. This accounts for 30.3% of production agent failures.

Classic examples:
- No quantity limit on an order (the McDonald's bot that ordered 1000+ nuggets)
- Dropping a table instead of querying it
- Deleting all records older than N days when no such column exists
- Pushing to main without confirmation
- Running a recursive delete without a depth limit

## Detection triggers

Activate when:
- Performing a destructive operation (delete, drop, remove, purge, unlink)
- Executing a write operation (insert, update, push, deploy, publish)
- Calling an operation that costs money (provision, scale, purchase, order)
- Any operation without explicit bounds or limits
- Any command that could affect other users or shared resources

## Protocol

### 1. Pre-execution sanity check
Before ANY destructive or mutating operation, ask:
- What is the worst thing this command could do?
- Do I have permission to do this?
- Are there bounds I should enforce? (quantity, depth, scope, limit)

### 2. Bounds are not optional
If a tool accepts a quantity, count, limit, or scope parameter, you MUST set a reasonable bound. Never leave it unbounded.

### 3. Dry-run before execute
For any operation that:
- Deletes data
- Modifies production
- Costs money
- Affects other users

First run with `--dry-run`, verify the output, then ask the user before proceeding with the real operation.

### 4. Scope narrowing
Assume the smallest possible scope:
- Single file, not entire project
- Single record, not entire table
- Current user only, not all users
- Single environment, not all environments

Only expand scope when the user explicitly asks.

### 5. Confirm destructive chains
If a plan has multiple destructive steps, confirm EACH step. An initial "yes" is not a global mandate.

## When NOT to use
- Read-only operations
- Non-destructive queries
- User explicitly says "do it, don't ask" and the action is low-risk
- Operations in clearly isolated/sandboxed environments

## Bundled Script

Copy `sanity-check.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-rogue-actions/scripts/sanity-check.ps1 .ai_scripts/
```

Pre-execution guard that flags destructive commands, missing targets, and broad scopes:

```powershell
.ai_scripts\sanity-check.ps1 -Command "Remove-Item -Recurse src/" -MaxItems 50
.ai_scripts\sanity-check.ps1 -Action "delete" -Target "prod-db" -DryRun
```

## Cross-references

- **anti-library-hallucination** — A wrong package suggestion can lead to destructive actions.

- **anti-phantom-symbols** — Invented APIs can cause runtime failures that cascade.

- **security-best-practices** — Safety bounds and permission checks are security concerns.
- **skill-loader** — Apply the capped selection policy when deciding which validation and security skills should also be active before executing actions.
