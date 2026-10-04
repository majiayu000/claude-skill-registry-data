---
name: spec-driven-development
description: >
  Formal specification authoring with exit criteria and acceptance
  conditions. Use when requirements need to be captured precisely
  before implementation begins. Produces a spec document that drives
  planning and testing.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
triggers:
  - context: "writing requirements"
  - context: "capturing specifications"
  - context: "defining acceptance criteria"
  - command: "/spec"
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
  - brainstorming@^1.0.0
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

Specifications are the contract between "what we want" and "what we build." This skill produces precise, testable spec documents that eliminate ambiguity and drive both implementation and verification. A good spec answers every question an implementer would ask before they need to ask it.

## When to Use

- After brainstorming has produced an approved design
- When requirements need to be formalized before implementation
- When multiple developers (or agents) will implement from the same requirements
- NOT for trivial changes where the brainstorming design IS the spec

## Process

### 1. Define the Scope Boundary

State clearly what IS and IS NOT in scope:

```markdown
## Scope
### In Scope
- User registration via email/password
- Email verification flow
- Password reset via email

### Out of Scope
- Social login (OAuth) — deferred to Phase 2
- Admin user management — separate spec
- Multi-factor authentication — future enhancement
```

### 2. Write Functional Requirements

Each requirement MUST be:
- **Testable** — An automated test can verify it
- **Unambiguous** — Only one valid interpretation
- **Complete** — Covers happy path, error cases, and edge cases

```markdown
## Requirements

### FR-001: User Registration
- The system SHALL accept email and password for registration
- Email MUST be validated as a properly formatted email address
- Password MUST be at least 12 characters with 1 uppercase, 1 number, 1 special
- The system SHALL return 409 Conflict if email is already registered
- The system SHALL send a verification email within 30 seconds of registration
- Registration SHALL NOT grant access until email is verified
```

Use RFC 2119 keywords: MUST, SHALL, SHOULD, MAY, MUST NOT.

### 3. Define Acceptance Criteria

For each requirement, specify the exact test that proves it works:

```markdown
### Acceptance Criteria for FR-001
- [ ] POST /api/register with valid email+password returns 201
- [ ] POST /api/register with invalid email returns 400 with "invalid email" error
- [ ] POST /api/register with weak password returns 400 with password requirements
- [ ] POST /api/register with existing email returns 409
- [ ] Verification email received within 30 seconds (check Mailtrap or similar)
- [ ] Unverified user cannot access protected endpoints (returns 403)
```

### 4. Document Non-Functional Requirements

```markdown
## Non-Functional Requirements
- NFR-001: Registration API response time < 500ms (p99)
- NFR-002: Email sending must not block the registration response
- NFR-003: Passwords stored with bcrypt cost factor ≥ 12
- NFR-004: Rate limiting: max 5 registration attempts per IP per hour
```

### 5. Identify Dependencies and Risks

```markdown
## Dependencies
- Email service (SendGrid, SES, or SMTP)
- Database (PostgreSQL)

## Risks
- Email deliverability may vary by provider — test with multiple domains
- Rate limiting may need tuning based on legitimate usage patterns
```

### 6. Obtain Sign-off

Save the spec to `docs/specs/YYYY-MM-DD-<topic>-spec.md` and get user approval before proceeding to planning.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The design doc IS the spec" | Design describes architecture. Specs describe behavior. They overlap but serve different purposes. You can combine them for simple features, but the acceptance criteria must be explicit. |
| "We can figure out edge cases during implementation" | Edge cases discovered during implementation are the leading cause of scope creep and bugs. Name them now. |
| "RFC 2119 is overkill for this project" | MUST vs. SHOULD vs. MAY eliminates 80% of spec ambiguity in one word. It's not overkill — it's precision. |
| "Acceptance criteria are just tests" | Acceptance criteria are the CONTRACT. Tests are the implementation of that contract. Write the contract first. |

## Red Flags

- Requirements that use vague language: "fast," "user-friendly," "secure"
- Missing error cases — only happy path documented
- No acceptance criteria for any requirement
- Spec changes after implementation has started without re-review

## Verification

- [ ] Scope boundary clearly defined (in/out of scope)
- [ ] Every functional requirement is testable and uses RFC 2119 keywords
- [ ] Acceptance criteria exist for every requirement
- [ ] Error cases and edge cases documented
- [ ] Non-functional requirements specified with measurable targets
- [ ] Dependencies and risks identified
- [ ] Spec saved to `docs/specs/` and user has approved

## See Also

- `codehands:brainstorming` — Design phase that precedes spec writing
- `codehands:planning-and-task-breakdown` — Next step after spec approval
- `codehands:test-driven-development` — Acceptance criteria drive tests
