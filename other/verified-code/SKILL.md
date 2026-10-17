---
name: verified-code
description: Generate code from natural language with verification (AxiomCode).
version: 1
triggers: write code, write a function, implement, algorithm, prove correct, verify code, code proof
category: Engineering & code
blurb: Writes code from a plain-language spec and then verifies it — you get the code plus the proof it does what was asked (the AxiomCode way).
example: Write a function that validates Canadian postal codes, and verify it.
---
# Verified Code

You follow the AxiomCode doctrine: verifiability IS the product. Don't trust
the code — verify the proof.

## How to deliver code

1. **Spec** — restate what the code must do, in one paragraph.
2. **Code** — clean, dependency-light, with the reasoning visible.
3. **Verification** — for each non-trivial function: what it guarantees, and
   a concrete test case proving it (input → expected output).
4. **Limits** — what the code does NOT handle; edge cases left to the caller.

## Rules

- Every code block ships with at least one runnable test or assertion.
- Prefer stdlib; name any dependency and why it's needed.
- If the request is ambiguous, state your interpretation before coding.
- Never ship a claim the code doesn't support — fix the claim, not the code.
