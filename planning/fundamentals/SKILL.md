---
id: javascript.fundamentals
name: JavaScript Fundamentals
description: >
  Coordinates the learning and review path for JavaScript async error handling, modules, and pure functions so agents can choose the right primitive for the runtime and project maturity.
stack:
  - JavaScript
  - TypeScript
category: javascript
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - javascript fundamentals
  - javascript learning path
  - javascript primitives
  - js fundamentals
  - javascript roadmap
  - javascript capability path
compatibility:
  runtime:
    browser: true
    node: true
---

# JavaScript Fundamentals

## Purpose

Use this skill to coordinate the learning and review path for JavaScript async error handling, modules, and pure functions.

This is a mother skill. It does not replace the specialized skills. It tells an agent which primitive to use, what order to teach it in, and when a versioned or runtime-specific variant is more appropriate.

The core rule is simple:

```txt
Pick the primitive that matches the problem, the runtime, and the team maturity.
```

## When to Use

Use this skill when:

- a team needs a JavaScript learning path
- fundamentals are mixed without a policy
- onboarding needs to cover async behavior, modules, and pure logic
- a refactor needs to choose the right JavaScript primitive

## Do

Use a sequencing policy:

```txt
modules -> pure functions -> async error handling
```

Or, for operational refactors:

```txt
identify module boundaries -> isolate pure logic -> harden async failure paths
```

Keep the specialist skills separate:

```txt
async-error-handling -> Promise and failure contracts
modules -> import/export and boundary management
pure-functions -> deterministic logic and mutation control
```

Use runtime variants only when the runtime materially changes the guidance.

## Do Not

Avoid turning the mother skill into implementation guidance.

Avoid teaching browser-only or Node-only concerns as universal if the runtime differs.

Avoid mixing pure logic, module structure, and async handling without a policy.

Avoid using this skill to replace the specialized skills.

## Review Checklist

- [ ] The team has a sequencing policy.
- [ ] Runtime differences are explicit.
- [ ] Specialized skills remain separate.
- [ ] The adoption path matches team maturity.
- [ ] The skill is used as routing and coordination, not implementation detail.

## Expected Output

1. Recommend the right primitive sequence.
2. Route to the specialized skills.
3. Consider runtime-specific variants when needed.
4. Keep the scope at architecture and learning-path level.
5. Summarize the JavaScript fundamentals adoption plan.
