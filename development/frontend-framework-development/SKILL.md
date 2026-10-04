---
name: frontend-framework-development
description: "Use when creating a front-end framework or reusable UI library that manages components, state, rendering, or events to define the public component and update contract, build one accessible end-to-end slice, and verify lifecycle and browser behavior before adding abstractions. Trigger for framework runtimes, component systems, renderers, or shared UI primitives."
---

# Front-End Framework and Library Development

## Overview

This skill applies when creating a front-end framework or reusable UI library that manages components, state, rendering, or events. Its intended outcome is to define the public component and update contract, build one accessible end-to-end slice, and verify lifecycle and browser behavior before adding abstractions.

## When to Use

### Preserved source section: When to Use

Use for a framework or library that other code uses to construct interactive interfaces. For ordinary product-page work, prefer the product's existing framework and its conventions.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

5. **Preserve web semantics.** Prefer native elements, labels, keyboard behavior, focus management, and accessible names. Document any interaction the library cannot provide automatically.
7. **Measure before optimizing.** Profile realistic component trees and updates; do not add a scheduler or virtual-DOM complexity without evidence.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target browser/runtime, language, packaging format, and supported versions.
- Component model, rendering mode, state/update semantics, event model, and public API.
- Accessibility, security, performance, and compatibility requirements.

## Instructions

### Preserved source section: Procedure

1. **Define the consumer contract.** Specify how components are declared, how inputs and state update, how errors surface, and which APIs are stable.
2. **Build one vertical slice.** Render a component, update state, handle an event, and observe the resulting DOM using the smallest runtime path.
3. **Make updates predictable.** Define identity/key behavior, render scheduling, cleanup, and effect lifecycle. Prevent stale callbacks and duplicated subscriptions.
4. **Protect DOM boundaries.** Escape text by default, make raw HTML an explicit dangerous escape hatch, and avoid unsafe URL or script insertion. Handle user input as untrusted.
5. **Preserve web semantics.** Prefer native elements, labels, keyboard behavior, focus management, and accessible names. Document any interaction the library cannot provide automatically.
6. **Test public behavior.** Use browser or DOM tests for render/update/unmount, event ordering, accessibility basics, error handling, and supported environments. Avoid tests that lock in private implementation details.
7. **Measure before optimizing.** Profile realistic component trees and updates; do not add a scheduler or virtual-DOM complexity without evidence.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Document the public API, state/render semantics, security defaults, accessibility guarantees, browser support, and tests. Accept the initial library when consumers can build and update a representative component without hidden global state or unbounded listeners.

## Output Format

### Preserved source section: Output and Acceptance

Document the public API, state/render semantics, security defaults, accessibility guarantees, browser support, and tests. Accept the initial library when consumers can build and update a representative component without hidden global state or unbounded listeners.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

1. **Define the consumer contract.** Specify how components are declared, how inputs and state update, how errors surface, and which APIs are stable.
6. **Test public behavior.** Use browser or DOM tests for render/update/unmount, event ordering, accessibility basics, error handling, and supported environments. Avoid tests that lock in private implementation details.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Document the public API, state/render semantics, security defaults, accessibility guarantees, browser support, and tests. Accept the initial library when consumers can build and update a representative component without hidden global state or unbounded listeners.
