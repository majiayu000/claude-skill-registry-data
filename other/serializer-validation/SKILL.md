---
name: serializer-validation
description: 'Harden backend input and output validation with DRF serializers. Use when adding fields, enforcing domain rules, sanitizing user input, and standardizing error payloads.'
argument-hint: 'Describe serializer(s), fields involved, domain constraints, and security risk level.'
user-invocable: true
---

# Serializer Validation Hardening

## Purpose
Prevent invalid or unsafe data from entering backend logic while keeping error responses predictable for frontend clients.

## Use When
- Adding/updating serializer fields
- Enforcing domain constraints (age, profile completeness, preference ranges)
- Sanitizing potentially unsafe text
- Standardizing validation and error payloads

## Mandatory Workflow

### 1. Field Inventory and Threat Mapping
- List each changed field, type, constraints, and trust level
- Identify abuse vectors: invalid type, oversized payload, XSS payloads, unsupported enum values

### 2. Define Explicit Validation Rules
- Type and length constraints
- Enum/choice whitelist checks
- Semantic business validation in validate_<field> and validate()
- Cross-field consistency checks (example: age_min <= age_max)

### 3. Sanitize and Normalize
- Normalize incoming values where required (trim, casing, controlled defaults)
- Strip unsafe HTML where user-generated rich text is not allowed
- Keep normalization deterministic and documented

### 4. Error Shape Consistency
- Return structured errors matching project standard
- Keep messages i18n-ready and non-sensitive
- Avoid leaking internals in validation messages

### 5. Integration Safety
- Ensure serializers are used in views for all writes
- Ensure model save paths cannot bypass critical validation
- Verify partial updates do not break required invariants

### 6. Tests and Regression
- Add/adjust unit tests for valid and invalid payloads
- Include edge cases and boundary values
- Verify no existing accepted payload is unintentionally broken unless intended

### 7. Output Contract
1. Serializer rules added/changed
2. Invalid payload classes covered
3. Sanitization decisions
4. Error format confirmation
5. Tests and residual validation risk

## Quality Gates
- No unbounded free-text field without explicit max_length/sanitization decision
- No business-critical field without semantic validation
- No silent coercion that changes user intent unexpectedly
