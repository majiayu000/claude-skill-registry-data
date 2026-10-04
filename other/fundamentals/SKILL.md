---
id: typescript.fundamentals
name: TypeScript Fundamentals
description: >
  Coordinates the learning and review path for TypeScript safety, types, DTO boundaries, module hygiene, and pure modeling so agents can choose the right primitive for the codebase and runtime.
stack:
  - TypeScript
category: fundamentals
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - typescript fundamentals
  - typescript learning path
  - ts fundamentals
  - typescript primitives
  - typescript capability path
  - type safety roadmap
compatibility:
  runtime:
    browser: true
    node: true
---

# TypeScript Fundamentals

## Purpose

Use this skill to coordinate the learning and review path for TypeScript safety, types, DTO boundaries, module hygiene, and pure modeling.

This is a mother skill. It does not replace specialized skills for strict typing, DTO mapping, or module patterns. It tells an agent which TypeScript primitive to use, in what order to teach it, and when a runtime-specific or version-specific variant is more appropriate.

The core rule is simple:

```txt
Pick the type shape that matches the contract, the runtime, and the team maturity.
```

## When to Use

Use this skill when:

- a team needs a TypeScript learning path
- type safety is mixed without a policy
- onboarding needs to cover models, DTOs, and module hygiene
- a refactor needs to choose the right TypeScript primitive

## Do

Use a sequencing policy:

```txt
models -> DTOs -> pure transformations -> module boundaries -> strict typing
```

Keep the specialist skills separate:

```txt
strict typing -> unsafe any removal and narrowing
dto mapping -> contract translation at boundaries
modules -> import/export and boundary management
pure functions -> deterministic logic and mutation control
```

Use versioned or runtime-specific variants only when they materially change the guidance.

## Do Not

Avoid turning the mother skill into implementation guidance.

Avoid conflating runtime behavior with type-level policy.

Avoid mixing model design, module structure, and async handling without a policy.

Avoid using this skill to replace the specialized skills.

## Review Checklist

- [ ] The team has a sequencing policy.
- [ ] Runtime and version differences are explicit where relevant.
- [ ] Specialized skills remain separate.
- [ ] The adoption path matches team maturity.
- [ ] The skill is used as routing and coordination, not implementation detail.

## Expected Output

1. Recommend the right primitive sequence.
2. Route to the specialized skills.
3. Consider runtime-specific variants when needed.
4. Keep the scope at architecture and learning-path level.
5. Summarize the TypeScript fundamentals adoption plan.
