---
name: browser-crypto-protocol-reconstruction
description: Reconstruct browser-side credential transforms and encrypted management requests from JavaScript, captures, and firmware evidence. Use for embedded web UIs with minified crypto, challenge-response login, lookup tables, or application-layer encryption.
---

# Browser Crypto Protocol Reconstruction

Use this skill when a web interface transforms credentials or wraps
management requests in browser-side cryptography. The goal is an auditable
plaintext-to-wire data flow, not password guessing or exploit development.

## Workflow

1. Preserve and hash original HTML/JS/CSS. Create separate derived copies for formatting.
2. Map UI validation and event handlers to helper functions, endpoints, methods, headers, and request ordering.
3. Separate plaintext validation, character/table transforms, hashes, challenge responses, RSA/AES/envelope encryption, and transport encoding.
4. Extract lookup tables and index formulas statically. If selection is randomized, enumerate the proven index range offline rather than sampling.
5. Build small offline reference vectors and round-trip tests. Compare randomized encryption semantically unless deterministic equality is proven.
6. Validate one intentionally invalid transaction before any repeated candidate work; apply explicit pacing and stop on lockout signals.

## Required distinctions

- Mark claims `PROVEN FROM CODE`, `OBSERVED IN CAPTURE`, `VALIDATED OFFLINE`, `DERIVED`, or `UNKNOWN`.
- Keep lossy transform equivalence classes separate from downstream encryption/session values.
- Do not infer backend storage or authorization from frontend code alone.
- Never log plaintext credentials or reusable tokens by default.
- Keep device-specific keys, addresses, credentials, and exploit packets in case evidence, not this generic skill.

## Deliverables

Produce a data-flow diagram, transform/table artifacts, request/response
schema, test vectors, collision/inverse analysis where applicable, and an
unresolved-questions list. Use `references/analysis-checklist.md` as a
worksheet.
