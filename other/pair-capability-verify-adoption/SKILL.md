---
name: pair-capability-verify-adoption
description: "Checks code and configuration against project adoption files for a given scope. Detection-only: returns conformity/non-conformity list per area without resolving issues. Caller decides resolution. Invocable independently or composed by /pair-process-review and /pair-process-implement."
version: 0.4.1
author: Foomakers
---

# /pair-capability-verify-adoption — Adoption Compliance Checker

Check code, configuration, or a PR against the project's adoption files. Detection-only — returns a conformity/non-conformity list per area. Does NOT resolve issues; resolution is the caller's responsibility.

## Arguments

| Argument | Required | Description                                                                                                                      |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `$scope` | Yes      | Area to check: `tech-stack`, `architecture`, `security`, `coding-standards`, `infrastructure`, `all`. Determines which adoption files are read. |

## Scope-to-Adoption Mapping

| Scope              | Adoption File(s)                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `tech-stack`       | [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md)                                             |
| `architecture`     | [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) + [adoption/tech/adr/](../../../.pair/adoption/tech/adr) |
| `security`         | Security-related sections in adoption files + [security guidelines](../../../.pair/knowledge/guidelines/quality-assurance/security/security-guidelines.md) |
| `coding-standards` | Code design adoption + [code-design guidelines](../../../.pair/knowledge/guidelines/code-design/README.md)           |
| `infrastructure`   | [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md)                                     |
| `all`              | All of the above                                                                                                     |

## Algorithm

For each area in scope, follow the **check → skip → act → verify** pattern.

### Step 1: Resolve Scope

1. **Check**: Is `$scope` provided?
2. **Act**: If `$scope = all`, expand to all 5 areas: `tech-stack`, `architecture`, `security`, `coding-standards`, `infrastructure`.
3. **Act**: If single scope, use only that area.
4. **Verify**: Area list determined.

### Step 2: Check Tech Stack Compliance

_Skip if `tech-stack` not in resolved scope._

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist and contain project-specific content?
2. **Skip**: If adoption file missing or template-only → report `tech-stack: NOT CONFIGURED` and move to next area.
3. **Act**: Read the adoption file. Extract adopted technologies with versions. Scan the codebase or PR for:
   - Dependencies not listed in tech-stack.md (unlisted imports, package.json entries)
   - Version mismatches (code uses a different version than adopted)
   - Deprecated or removed technologies still in use
4. **Verify**: Report per finding:
   - **CONFORMANT**: All dependencies match adoption.
   - **NON-CONFORMANT**: List each violation with file, dependency, and reason.

### Step 3: Check Architecture Compliance

_Skip if `architecture` not in resolved scope._

1. **Check**: Does [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) exist with project-specific content?
2. **Skip**: If missing → report `architecture: NOT CONFIGURED` and move to next area.
3. **Act**: Read architecture adoption and existing ADRs in [adoption/tech/adr/](../../../.pair/adoption/tech/adr). Check code for:
   - Pattern violations (e.g., direct DB access bypassing service layer)
   - Layer boundary crossings not permitted by the architecture
   - Architectural changes without a corresponding ADR
   - ADR decisions not reflected in implementation
4. **Verify**: Report CONFORMANT or NON-CONFORMANT with findings.

### Step 4: Check Security Compliance

_Skip if `security` not in resolved scope._

1. **Check**: Do security-related adoption files or [security guidelines](../../../.pair/knowledge/guidelines/quality-assurance/security/security-guidelines.md) exist?
2. **Skip**: If no security guidelines found → report `security: NOT CONFIGURED` and move to next area.
3. **Act**: Check code for:
   - Hardcoded secrets or credentials
   - Input validation gaps at system boundaries
   - Injection vulnerabilities (SQL, command, XSS)
   - Improper data handling or logging of sensitive data
   - Missing authentication/authorization checks
4. **Verify**: Report CONFORMANT or NON-CONFORMANT with findings.

### Step 5: Check Coding Standards Compliance

_Skip if `coding-standards` not in resolved scope._

1. **Check**: Do [code-design guidelines](../../../.pair/knowledge/guidelines/code-design/README.md) or coding standards adoption files exist?
2. **Skip**: If missing → report `coding-standards: NOT CONFIGURED` and move to next area.
3. **Act**: Check code for:
   - Naming convention violations
   - File/module organization deviations from adopted patterns
   - Missing or improper error handling patterns
   - Test structure violations (1:1 mapping, behavior-based tests)
4. **Verify**: Report CONFORMANT or NON-CONFORMANT with findings.

### Step 6: Check Infrastructure Compliance

_Skip if `infrastructure` not in resolved scope._

1. **Check**: Does [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) exist with project-specific content?
2. **Skip**: If missing → report `infrastructure: NOT CONFIGURED` and move to next area.
3. **Act**: Read infrastructure adoption. Check for:
   - CI/CD configuration deviations from adopted pipeline
   - Deployment patterns not matching adopted infrastructure
   - Environment configuration inconsistencies
4. **Verify**: Report CONFORMANT or NON-CONFORMANT with findings.

## Output Format

```text
ADOPTION COMPLIANCE REPORT:
├── Scope:           [$scope — expanded areas]
├── Tech Stack:      [CONFORMANT | NON-CONFORMANT — N findings | NOT CONFIGURED]
├── Architecture:    [CONFORMANT | NON-CONFORMANT — N findings | NOT CONFIGURED]
├── Security:        [CONFORMANT | NON-CONFORMANT — N findings | NOT CONFIGURED]
├── Coding Standards:[CONFORMANT | NON-CONFORMANT — N findings | NOT CONFIGURED]
└── Infrastructure:  [CONFORMANT | NON-CONFORMANT — N findings | NOT CONFIGURED]

FINDINGS (if any):
1. [area] — [description] ([file:line])
   Resolution: [/assess-stack | /pair-capability-record-decision | developer action]
2. ...

RESULT: [ALL CONFORMANT | N non-conformities across N areas]
```

## Resolution Routing

This skill does NOT resolve non-conformities. It routes them to the appropriate resolver:

| Area             | Resolver                | Rationale                                |
| ---------------- | ----------------------- | ---------------------------------------- |
| Tech Stack       | `/pair-capability-assess-stack`         | Stack changes go through tech assessment |
| Architecture     | `/pair-capability-record-decision`      | Architectural gaps need an ADR           |
| Security         | Developer action        | Security fixes are context-specific      |
| Coding Standards | Developer action        | Code style fixes are manual              |
| Infrastructure   | Developer action        | Infra changes need manual review         |

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: `/pair-process-review` invokes `/pair-capability-verify-adoption` with `$scope=all` during the adoption compliance phase.
- **Output**: Returns the compliance report. /pair-process-review incorporates findings into review output.
  - NON-CONFORMANT areas contribute to CHANGES-REQUESTED verdict.
  - NOT CONFIGURED areas are noted but do not block.

When composed by `/pair-process-implement`:

- **Input**: `/pair-process-implement` may invoke `/pair-capability-verify-adoption` with a targeted `$scope` (e.g., `tech-stack`) before commit.
- **Output**: Returns the compliance report. /pair-process-implement resolves non-conformities via /pair-capability-assess-stack or /pair-capability-record-decision.
  - Unresolved non-conformities do not HALT — /pair-process-implement warns and continues.

When invoked **independently**:

- Full interactive flow. Developer receives the compliance report and decides resolution.
- This skill only reads and reports — it does not modify files.

## Graceful Degradation

- If an adoption file for a given area does not exist, report that area as `NOT CONFIGURED` — do not fail.
- If `$scope=all` and no adoption files exist at all, report: "No adoption files found — run `/pair-process-bootstrap` to establish project standards."
- If guidelines referenced by an area are not found, check only adoption-file-derived constraints for that area.
- If the codebase is empty or no code changes to check, report all areas as `CONFORMANT` (nothing to violate).

## Notes

- This skill is **read-only** — it inspects code and adoption files but never modifies anything.
- **Detection-only contract**: the skill identifies non-conformities but never resolves them. Resolution is always delegated to the caller or the appropriate skill.
- **Idempotent**: re-invocation on conformant code immediately confirms compliance. Re-invocation on non-conformant code returns the same findings until the code is fixed.
- **Scope is mandatory** to prevent accidental full scans when only a targeted check is needed. Use `all` explicitly for comprehensive checks.
- Contextual checking: when invoked on a PR, only changes in the PR are checked, not the entire codebase. When invoked independently, the scope of code analysis is determined by the area.
