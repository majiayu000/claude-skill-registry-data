---
id: frontend.design.component-api-composition
name: Component API and Composition
description: Design reusable component contracts with semantic typed APIs, slots, defaults, events, extension points, and controlled complexity.
stack:
  - Frontend
  - TypeScript
  - Design Systems
category: components
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - component API
  - reusable component
  - component composition
  - boolean prop explosion
---

# Component API and Composition

## Purpose

Create components that are easy to adopt correctly and hard to misuse without exposing implementation details.

## When to Use

- A reusable component has growing booleans, overrides, variants, or copied markup.
- A component family needs stable composition, theming, and event contracts.

## Do

- Define one responsibility, use and non-use cases, typed defaults, variants, slots, domain events, and state ownership.
- Prefer discriminated unions over interacting booleans and public extension points over private DOM selectors.
- Keep accessibility complete in the default path and semantic in API names.

## Do Not

- Do not mirror all HTML/CSS properties, emit vague DOM events, accept arbitrary templates, or create mega-components.

## Review Checklist

- [ ] Basic use needs minimal configuration and invalid combinations are blocked.
- [ ] API remains coherent across state and responsive variants.
- [ ] Consumers need no private DOM targets or repeated ARIA expertise.

## Expected Output

1. Responsibility, typed API, composition, and event contract.
2. Theming and extension policy.
3. Migration examples and validation scope.

## References

- [Design Excellence Guide](../../../../docs/design-excellence-guide.md)
