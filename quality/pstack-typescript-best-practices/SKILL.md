---
name: pstack-typescript-best-practices
description: "Improve TypeScript domain types and input boundaries where casts, optional-field bags, duplicate schemas, or mixed semantic identifiers cause defects. Use for targeted type modeling or TypeScript quality reviews."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/typescript-best-practices
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# TypeScript best practices

Use the repository's existing type, schema, and logging conventions. Apply improvements to the requested work rather than sweeping every TypeScript file.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Model the actual domain

Use discriminated unions for mutually exclusive states. Derive booleans from authoritative state when that removes contradictory combinations. Strengthen a type only where a real operation would otherwise be partial or require an assertion.

Distinguish semantically different identifiers when accidental interchange is a demonstrated risk. Reuse existing brands or constructors. Avoid a blanket brand migration.

## Parse at boundaries

Treat network payloads, persisted JSON, configuration, and other untrusted data as unknown until parsed. Reuse the repository's runtime schemas and derive types from them. Adding a new dependency for one guard is rarely justified.

Parse once into a domain value. Keep transport and persistence representations within their owning boundary. Authorization, tenant isolation, concurrency checks, and changing external state are still runtime responsibilities even after parsing.

## Let the compiler help

Prefer narrowing and exhaustive variants over unsafe assertions. Use satisfies to check object shape without widening literals. Derive appropriate types from authoritative contracts, but do not expose private wire types just to avoid a small domain definition.

Type assertions can be legitimate after a validator proves the required invariant. Record the actual proof rather than banning syntax mechanically. A predicate must verify everything it claims.

A TypeScript number can be negative, infinite, or NaN. A start-plus-duration representation does not prove a valid range without a validated duration. Dates, timezone semantics, and runtime array indexing also need genuine invariants.

## Verify proportionally

Use existing typecheck and behavior checks. Prefer observable public behavior over mocks of internal calls. Retain correct absence, security, and negative-path assertions; expected empty output can be a meaningful contract.

Explain which invalid combination or boundary risk the change now rejects and what remains a runtime responsibility.
