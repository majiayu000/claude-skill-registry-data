---
name: oe-security-prompt-injection
description: Maintain and extend prompt-injection defenses. Use when adding new user-input surfaces, changing prompt templates, or when a new injection pattern is observed; run the security regression suite and add a minimal new test case.
---

# oe-security-prompt-injection

## Run the regression suite

- `pytest backend/tests/regression/test_security_prompt_injection.py -v`

## Add a new attack case (when needed)

1. Add the new payload to the parametrized attack list in `backend/tests/regression/test_security_prompt_injection.py`.
2. Assert both:
   - the input is flagged as suspicious, and
   - the matched pattern/category is the expected one (so we catch drift).

## Guardrails

- Do not weaken detection to “make a test pass”; prefer tightening allowlists for safe inputs and adding targeted patterns for new attacks.
