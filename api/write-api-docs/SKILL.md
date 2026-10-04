---
name: write-api-docs
description: Use when writing or improving API reference documentation, endpoint descriptions, or OpenAPI specifications
source: "Docs for Developers (Bhatti et al., 2021); Stripe API Docs; OpenAPI Initiative Specification 3.1"
tags: [api, documentation, openapi, reference, technical-writing]
verified: true
---

# Write API Docs

Write clear, complete API reference documentation that developers trust and can use without guessing.

## Why This Is Best Practice

**Adopted by:** Stripe, Twilio, GitHub, and Shopify — consistently ranked top developer-experience APIs

**Impact:** Stripe attributes low support volume directly to documentation quality; Twilio reports 30%+ faster onboarding for customers who read docs before integrating

**Why best:** Well-written API docs reduce integration time and support burden simultaneously. Developers treat docs as a contract — ambiguity breaks trust permanently. The OpenAPI Specification enforces machine-readable consistency while Stripe's style demonstrates the narrative layer on top.

## Steps

1. **Define the audience and use cases** — identify whether readers are integrating for the first time or looking up edge cases; write for both with layered depth
2. **Structure each endpoint entry** — include: purpose sentence, HTTP method + path, authentication requirement, all parameters with types/constraints/defaults, request example, response schema, error codes
3. **Write the purpose sentence first** — one plain-language sentence explaining what the endpoint does and when to use it, before any technical detail
4. **Provide runnable examples** — show real request/response pairs with realistic values, not `string` placeholders; include `curl` and at least one SDK snippet
5. **Document every error code** — list status codes the endpoint can return, the condition that triggers each, and the recommended recovery action
6. **Write an OpenAPI spec in parallel** — keep narrative docs and machine-readable spec in sync; spec drives SDK generation and lint tooling
7. **Add changelog entries** — note deprecations, new fields, and breaking changes at the top of each affected page with version and date

## Rules

- Every parameter must state: type, whether required or optional, default value, and valid range or enum values
- Never use `foo`, `bar`, or `string` as example values — use realistic domain data
- Breaking changes must be called out with a deprecation notice and migration path
- Code examples must be copy-paste executable without modification
- Authentication must be documented on every endpoint, not just a getting-started page

## Examples

**Bad:** `POST /charges` — Creates a charge.

**Good:** `POST /charges` — Creates a new charge against a customer's payment method. Use this endpoint to collect a one-time payment; for recurring billing, use the Subscriptions API instead.

## Common Mistakes

- Documenting only the happy path: developers need error states more than success states when debugging at 2 AM
- Letting examples drift from the schema: contradictions destroy trust faster than missing docs
- Burying authentication requirements: state them at the top of every endpoint, not just in an intro section

## When NOT to Use

- Do not apply this skill to internal-only APIs consumed by a single team that owns both producer and consumer, where informal inline code comments and a team wiki page provide sufficient shared context without the overhead of formal reference documentation.
- Do not use this skill for GraphQL APIs where the schema is self-describing and tools like GraphiQL or Apollo Sandbox auto-generate interactive reference; applying this skill's narrative-layer approach to a self-documenting schema creates duplicate, drift-prone content.
- Do not apply this skill before the API contract is stable; writing full reference docs against an actively changing interface produces documentation debt faster than it produces value, and the effort is better spent on a draft OpenAPI spec reviewed by consumers first.
