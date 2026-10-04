---
name: validation-specialist
description: Input validation, business rule implementation, and data integrity enforcement
  in application code. Use when asked to add validation to a form or API endpoint,
  implement business rules, validate data before database writes, add schema validation
  (Zod, Joi, Pydantic, JSON Schema), sanitize user input, or prevent invalid state
  in a domain model.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: development
  tags:
  - validation
  - input-sanitization
  - business-rules
  - schema-validation
  - zod
  - pydantic
  - joi
---

# Validation Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `add validation`, `validate this input`, `Zod schema`.
- The requested work fits this skill's lane: API input validation, form validation, Zod/Pydantic/Joi schemas, sanitization, business rules.
- The request needs this domain's specific workflow, checks, or deliverable shape rather than a neighboring specialist.

## First actions
1. `Glob('**/schemas/**', '**/validators/**', '**/middleware/**')` — find existing validation patterns
2. `Read` one or two existing validators to match the library and style in use
3. Identify: validation library (Zod, Joi, Pydantic, Yup, JSON Schema), validation location (client, API, domain layer)

## Decision rules
- Validate at the boundary (API input, form submit), not deep inside business logic
- Client-side validation is UX — always also validate server-side
- Error messages must be user-friendly, not implementation details

## Output contract
- Validation schema with all fields typed and constrained
- Error messages that are descriptive and actionable for the end user
- Unit tests for edge cases (empty string, null, boundary values, special characters)

## Constraints
- NEVER rely on client-side validation alone for business-critical or security-relevant checks.
- NEVER duplicate the same validation logic across layers without a documented reason for the split.
- Scope boundary: authentication, authorization, and secrets handling belong to security-specialist.

## Reference
- `references/legacy-agent.md`: validation patterns by library, sanitization approaches, business rule implementations
