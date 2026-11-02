---
name: form-validation-contract
description: Align client and server form validation with consistent field paths, normalization, accessibility, and submit handling.
---

# Form Validation Contract

## Goal

Prevent invalid data, lost user input, and contradictory validation between UI and API.

## Inputs to inspect

Form schema, server validator, normalization rules, field IDs, submit handler, and tests.

## Workflow

1. Document field types, requiredness, cross-field rules, normalization, lengths/ranges, and authoritative server constraints.
2. Define validation timing for typing, blur, and submit; avoid blocking correction with premature expensive checks.
3. Map server error codes and nested field paths to controls while preserving global/unknown errors in a visible summary.
4. Specify pending state, duplicate-submit protection, cancellation, success navigation, and retained input after recoverable failures.
5. Test empty, malformed, boundary, Unicode, whitespace, conflicting fields, repeated submits, and stale responses.

## Validation checklist

- [ ] Server enforces security- and integrity-critical validation.
- [ ] Normalization matches uniqueness and lookup rules.
- [ ] Field errors are accessible and not communicated by color alone.
- [ ] User values survive recoverable failures.
- [ ] Repeated submissions cannot duplicate side effects.

## Required output

Produce a field-rule matrix, client/server error mapping, accessibility checks, and boundary contract tests.

## Boundaries and failure handling

Do not rely on client validation for security; do not silently rewrite values when normalization changes user intent.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
