---
name: guardrails-ai-security
description: Review a Guardrails AI integration for validator bypass via adversarial inputs, schema enforcement gaps that allow malformed LLM output to pass validation, fail-open error handling that silently drops failed guardrails, and RAIL spec injection.
last_reviewed: 2026-04-29
---

# Guardrails AI Security

## First Principle

**A guardrail is only as strong as its validator — and validators are code that runs on untrusted LLM output. A sufficiently adversarial model output can cause a validator to error rather than reject, and most error handlers default to pass-through.**

Guardrails AI applies validators to LLM inputs and outputs to enforce schema, content policies, and structural constraints. The security assumption is that the validator is the last line of defense before output reaches the application. That assumption fails when validators can be bypassed — either by crafting output that the validator accepts but should reject, or by triggering validator exceptions that result in fail-open behavior.

## Attack Mental Model

1. **Validator bypass via adversarial output** — the LLM is manipulated to produce output that is syntactically valid according to the schema but semantically dangerous — passing structure checks while embedding harmful content in string fields.
2. **Exception-based fail-open** — a validator raises an unhandled exception on unexpected output. The guard's `on_fail` action defaults to `noop` or `fix`, passing the output downstream rather than blocking it.
3. **RAIL spec injection** — if RAIL XML specs are constructed from user input, an attacker can inject validator-disabling attributes or add permissive validators that override restrictive ones.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every validator's `on_fail` action is explicitly set to `exception` or `reask` — never left as the default or set to `noop`. Fail-open is not an acceptable guardrail posture. |
| **Scope** | String fields in output schemas are constrained with validators that bound length, character set, and content — not left as free-form strings that validators ignore. |
| **Isolate** | RAIL specs and `Validator` configurations are defined in code or config files — never constructed from user input at runtime. |
| **Enforce** | Guard validation failures are logged and surfaced as errors to the caller — not silently swallowed. |

## GAS.1 Validator Configuration and Fail-Open Prevention

**The core vulnerability:** Guardrails AI validators have an `on_fail` parameter that controls what happens when validation fails. The options include `exception` (raise), `reask` (retry), `fix` (attempt correction), `filter` (remove the field), and `noop` (do nothing). Teams using the `fix` or `noop` modes may believe they have active guardrails while actually passing dangerous output downstream.

### Check

- Is the `on_fail` action for every security-critical validator set to `exception` or `reask` — not `noop`, `fix`, or `filter`?
- Are validator exceptions caught and handled explicitly — rather than being silently swallowed by a broad `except Exception: pass` around the guard call?
- Is there a test for each validator that confirms it raises on invalid input — not just that it passes on valid input?

### Action

- **Set `on_fail="exception"` for every security-critical validator.** This ensures that a validation failure causes an exception that must be explicitly handled — not silently passed:

```python
from guardrails import Guard
from guardrails.hub import DetectPII, ToxicLanguage

guard = Guard().use_many(
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="exception"),
    ToxicLanguage(threshold=0.5, on_fail="exception"),
)
```

- **Wrap guard calls with explicit error handling.** Do not allow validator exceptions to propagate unhandled to the user — but do not silently discard them either:

```python
try:
    result = guard(llm_output)
except ValidationError as e:
    log_validation_failure(e)
    return {"error": "Output failed safety validation", "details": str(e)}
```

- **Write negative tests for each validator.** For every validator in your guard, write a test that passes known-bad input and asserts that a `ValidationError` is raised. If the test passes without raising, the validator is misconfigured.

### Failure Modes

- A `DetectPII` validator is configured with `on_fail="fix"`. When PII is found, Guardrails attempts to redact it automatically — but the redaction regex misses a custom PII format. The output passes with PII intact.
- A validator raises `AttributeError` on unexpected JSON structure. The calling code catches `Exception` broadly and logs a warning but returns the unvalidated output.

## GAS.2 Schema Enforcement and Free-Form Field Containment

**The core vulnerability:** Guardrails AI enforces the structure of LLM output against a defined schema. But structural enforcement does not constrain the content of string fields. An output schema with `{"summary": "string", "recommendations": "string"}` enforces that those keys exist — it does not prevent the LLM from placing a SQL injection payload or a prompt injection attack inside the `summary` field.

### Check

- Are string fields in output schemas constrained by content validators — not just structural validators?
- Is the maximum length of each string field bounded — preventing token-stuffed payloads that would overwhelm downstream parsers?
- Are fields that will be rendered in a UI passed through an output encoding validator before the response is sent to the client?

### Action

- **Apply content validators to every string field that will be consumed by downstream systems.** Do not rely on structural validation alone:

```python
from guardrails import Guard
from guardrails.hub import ValidLength, RegexMatch

guard = Guard().use_many(
    ValidLength(min=1, max=500, on_fail="exception"),   # bounds length
    RegexMatch(regex=r"^[^<>{};]*$", on_fail="exception"),  # blocks common injection chars
)
```

- **Treat every string output field as potentially attacker-controlled.** Apply the same output encoding you would apply to user-supplied input when rendering schema fields in HTML, SQL queries, or shell commands.
- **Use `Pydantic` output schemas with field-level validators.** Pydantic's `@validator` decorators run before Guardrails returns the result, providing a second validation layer:

```python
from pydantic import BaseModel, validator

class SafeOutput(BaseModel):
    summary: str
    
    @validator("summary")
    def no_injection_chars(cls, v):
        if any(c in v for c in ["<", ">", "{", "}", ";"]):
            raise ValueError("Injection characters detected in summary")
        return v
```

### Minimum Deliverable Per Review

- [ ] Validator inventory: every validator, its `on_fail` setting, and justification for any non-exception setting
- [ ] Negative test coverage: at least one known-bad input test per validator asserting `ValidationError`
- [ ] String field content validators: length bounds and character set constraints on all string output fields
- [ ] Exception handling audit: no broad `except Exception` silently discarding validator failures
- [ ] RAIL spec construction: confirmed that no RAIL specs are built from user input at runtime

## Quick Win

**Search your codebase for `on_fail="noop"` and `on_fail="fix"` in any guard configuration.** Each one is a guardrail that passes output rather than blocking on failure. Change security-critical validators to `on_fail="exception"` and add a negative test.

## References

- NeMo Guardrails for rail-based dialog control → [nemo-guardrails-security/SKILL.md](../nemo-guardrails-security/SKILL.md)
- LLM output validation at the prompt layer → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Data leakage through output fields → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
