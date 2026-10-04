---
name: risk-assessment-and-escalation
description: >
  Evaluate the risk profile of a change and automatically escalate
  reviews when high-risk areas are touched. Triggered by the task
  decomposition engine when risk signals are detected. Ensures auth,
  payments, data handling, and infrastructure changes get appropriate
  scrutiny.
version: 1.0.0
permissions:
  - fs.read
triggers:
  - context: "change touches authentication or authorization"
  - context: "change touches payment processing"
  - context: "change touches personal data handling"
  - context: "change modifies infrastructure or deployment"
  - context: "task-decomposition-engine flags elevated risk"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - security-and-hardening@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Not all changes are equal. A typo fix in a README and a change to the authentication flow carry vastly different risk profiles. This skill provides automatic risk detection based on what files and domains a change touches, and escalates the review process accordingly.

## When to Use

- When `codehands:task-decomposition-engine` assesses risk as Medium or higher
- When a change touches files in high-risk domains (auth, payments, data, infra)
- Before merging any PR that touches high-risk areas
- NOT for isolated, low-risk changes (the engine will skip this)

## Process

### 1. Risk Signal Detection

Scan the change scope for these automatic triggers:

| Signal | Files/Patterns | Risk Level |
|---|---|---|
| **Authentication** | `*auth*`, `*login*`, `*session*`, `*token*`, `*password*`, `*oauth*` | 🔴 High |
| **Authorization** | `*permission*`, `*role*`, `*access*`, `*policy*`, `*guard*` | 🔴 High |
| **Payments** | `*payment*`, `*billing*`, `*stripe*`, `*charge*`, `*subscription*` | 🔴 Critical |
| **Data/Privacy** | `*user*` (models), `*pii*`, `*gdpr*`, `*migration*` (DB) | 🟠 High |
| **Infrastructure** | `*deploy*`, `*docker*`, `*terraform*`, `*k8s*`, `*.env*`, CI configs | 🟠 High |
| **Dependencies** | `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt` | 🟡 Medium |
| **API surface** | Public endpoints, API routes, GraphQL schema | 🟡 Medium |
| **Configuration** | App config, feature flags, environment variables | 🟡 Medium |

### 2. Escalation Matrix

Based on detected risk level, escalate the review:

| Risk Level | Standard Review | Additional Review | Human Gate |
|---|---|---|---|
| **Low** | `code-review-and-quality` | — | Optional |
| **Medium** | `code-review-and-quality` | `security-and-hardening` check | Optional |
| **High** | `code-review-and-quality` | `agents/security-auditor.md` full audit | Recommended |
| **Critical** | `code-review-and-quality` | `agents/security-auditor.md` + `agents/architect.md` | **Mandatory** |

### 3. Risk Report

Produce a brief risk report appended to the plan or PR:

```markdown
## Risk Assessment
- Risk Level: [Low | Medium | High | Critical]
- Signals Detected:
  - 🔴 Authentication: modifies src/services/auth.ts
  - 🟡 API Surface: adds new endpoint POST /api/users
- Escalated Reviews:
  - [x] Security audit required (High risk)
  - [ ] Architecture review required (Critical risk)
- Human Gate: [Required | Recommended | Optional]
```

### 4. Mitigation Requirements

For High/Critical risk changes, add mandatory verification:

- **Auth changes:** Verify session handling, token validation, and RBAC tests pass
- **Payment changes:** Verify idempotency, error handling, and amount validation
- **Data changes:** Verify migration rollback works, data integrity preserved
- **Infra changes:** Verify rollback plan exists, staging tested first

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's a small change to the auth file" | Small auth changes cause big breaches. A one-line change to a token validator can invalidate all authentication. Always escalate. |
| "Security audit slows us down" | Security incidents slow you down infinitely more. A 10-minute security review is cheap insurance. |
| "This doesn't need human review" | Critical-risk changes always need human eyes. Agents can miss context that humans catch. |

## Red Flags

- High-risk files modified without elevated review
- Payment-related changes without idempotency verification
- Auth changes without session/token validation tests
- DB migrations without tested rollback
- No risk assessment on cross-cutting changes

## Verification

- [ ] Risk signals scanned across all modified files
- [ ] Risk level determined (Low/Medium/High/Critical)
- [ ] Appropriate review escalation applied
- [ ] Risk report generated and attached to plan/PR
- [ ] Human gate enforced for Critical risk
- [ ] Mitigation requirements met for High/Critical

## See Also

- `codehands:task-decomposition-engine` — Invokes this when risk is elevated
- `codehands:security-and-hardening` — Security review content
- `codehands:code-review-and-quality` — Standard review pipeline
- `agents/security-auditor.md` — Security audit persona
- `agents/architect.md` — Architecture review persona
