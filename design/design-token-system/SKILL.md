---
id: frontend.design.design-token-system
name: Design Token System
description: Define semantic, scalable design tokens and component token boundaries instead of hardcoded visual values.
stack:
  - Frontend
  - CSS
  - Design Systems
category: design-system
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - design tokens
  - CSS variables
  - theme architecture
  - component tokens
---

# Design Token System

## Purpose

Create token contracts that encode semantic purpose, theming, ownership, and controlled component variation.

## When to Use

- Repeated hardcoded values cause visual drift or themes, brands, density, or contrast modes are needed.
- A component library needs stable styling extension points.

## Do

- Separate primitives from semantic roles and define component tokens only for intentional local variation.
- Cover surface, text, border, action, status, focus, disabled, type, spacing, radius, elevation, and motion roles.
- Define naming, fallback, versioning, deprecation, contrast, and state-coverage policy.

## Do Not

- Do not create a token for every isolated value or expose palette names as component APIs.
- Do not mix primitive and semantic levels in consumer contracts or bypass accessibility states with overrides.

## Review Checklist

- [ ] Critical component states contain no unexplained hardcoded values.
- [ ] Token names describe purpose and themes do not require template changes.
- [ ] Component extension points are explicit and safe.

## Expected Output

1. Taxonomy, naming convention, and theme mapping.
2. Component-token, migration, and deprecation policy.
3. State and contrast validation evidence.

## References

- [Design Excellence Guide](../../../../docs/design-excellence-guide.md)
