---
name: authorization-xray
description: "Authorization X-ray for your own codebase (defensive audit): inventories every HTTP endpoint and every recognizable protection layer (middleware chains, authorize decorators, inline role checks, router mounts), builds the permission matrix endpoint x required check, and reports unprotected mutating endpoints and inconsistent protection of similar resources. Static, sends no requests. Read-only. Trigger: /authz"
trigger: /authz
---

## What this is for

"Who can do what?" - in grown systems nobody can answer this. Authorization checks are scattered: middleware here, decorator there, inline `if (user.role...)` somewhere else - and that one unprotected mutation endpoint is found during a pentest (or after). Distilling a complete permission matrix from code means finding every route, mapping every protection layer, spotting gaps and inconsistencies - drudge work plus semantics, i.e. LLM terrain.

**Audience:** Senior
- Security reviews get a complete permission matrix.
- Compliance audits get evidence of authorization coverage.
- New endpoint authors see how existing routes are protected.

### Trigger: `/authz`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Determine project path
Ask for `-ProjectDir`. Confirm. Note: report contains security-relevant findings - keep local.

### Step 3 - Run collector
```powershell
& .\scripts\authz-scan.ps1 -ProjectDir "<path>"
```

### Step 4 - LLM analysis
1. **Resolve protection chain per endpoint**: global mounts (does mount path match endpoint path?) + route guards + decorators + inline checks in handler. Result per endpoint: effective checks with evidence.
2. **Build matrix**: endpoint x (authn: yes/no/unclear) x (authz: which role/check) x evidence.
3. **Findings classes**:
   - **Unprotected + mutating** (severity high; `explicitlyPublic` separate - intentionally public is not a finding, but list for confirmation).
   - **Authn only, no authz on sensitive paths** (`/admin`, `/users/:id` patterns: accessing foreign ID without ownership check - IDOR suspicion, mark as `probable`).
   - **Inconsistency**: similar resource paths with different protection strictness.
   - **Dead roles**: roles referenced in checks never assigned/defined anywhere.
4. **Report**: summary → high findings with evidence → matrix table → inconsistencies → IDOR suspicions → explicitly public (for confirmation) → open questions.

### Step 5 - Produce report
Write `authz-report.md`:

```
# Authorization Report - <project>

## Summary
- <N> endpoints, <P> protected, <U> unprotected + mutating
- <I> IDOR suspicions, <D> dead roles

## High Severity
### 1. Unprotected Mutation Endpoints
Endpoint | File:Line | Without /api Mount | Why Missing
... | ... | ... | ...

## Permission Matrix
Endpoint | Authn | Authz / Role | Evidence
... | ... | ... | ...

## Inconsistencies
...

## IDOR Suspicions
...

## Open Questions
```

## Usage

```powershell
# Interactive
/authz

# Direct path
/authz C:\Projects\my-app

# Help
/authz --help
```
