---
id: typescript.strict-types
name: TypeScript Strict Types
description: >
  Coordinates the learning and review path for TypeScript strict typing, narrowing, DTO boundaries, and safe type contracts so agents can choose the right safety primitive for the codebase.
stack:
  - TypeScript
category: strict-types
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - typescript strict types
  - strict typing
  - type safety
  - typescript safety path
  - unsafe any removal
  - type narrowing
  - dto boundaries
compatibility:
  runtime:
    browser: true
    node: true
---

# TypeScript Strict Types

## Purpose

Use this skill to coordinate the learning and review path for TypeScript strict typing, narrowing, DTO boundaries, and safe type contracts.

This is a mother skill. It does not replace specialized skills for removing `any`, DTO mapping, or module structure. It tells an agent which strictness primitive to use, when to teach it, and when a strict-mode variant is more appropriate.

The core rule is simple:

```txt
Pick the narrowest safe type for the contract and keep unsafe boundaries explicit.
```

## When to Use

Use this skill when:

- a team needs a strict typing path
- unsafe `any` usage is mixed without a policy
- onboarding needs to cover narrowing and DTOs
- a refactor needs to choose the right type-safety primitive

## Do

Use a sequencing policy:

```txt
unknown -> narrowing -> DTOs -> generics -> strict contracts
```

Keep the specialist skills separate:

```txt
avoid-any -> remove unsafe any usage
dto-mappers -> map contracts at boundaries
fundamentals -> learning and adoption path
```

Use strict-mode variants when the repo already enforces or can adopt strict typing.

## Do Not

Avoid turning the mother skill into implementation guidance.

Avoid conflating strict typing with runtime behavior.

Avoid mixing type safety, module structure, and async handling without a policy.

Avoid using this skill to replace the specialized skills.

## Review Checklist

- [ ] The team has a strictness sequencing policy.
- [ ] Unsafe boundaries are explicit.
- [ ] Specialized skills remain separate.
- [ ] The adoption path matches team maturity.
- [ ] The skill is used as routing and coordination, not implementation detail.

## Expected Output

1. Recommend the right strictness sequence.
2. Route to the specialized skills.
3. Consider strict-mode variants when needed.
4. Keep the scope at architecture and learning-path level.
5. Summarize the TypeScript strict-types adoption plan.
