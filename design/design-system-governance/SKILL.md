---
id: frontend.design.design-system-governance
name: Design System Governance
description: Evolve reusable UI foundations through explicit tokens, component contracts, accessibility states, and evidence-based adoption decisions.
stack:
  - CSS
  - Design Systems
  - Frontend
category: design
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - design system
  - design tokens
  - component contract
  - theme
  - Material
---

# Design System Governance

## Purpose

Keep reusable frontend foundations coherent while allowing teams to use native CSS, a component library, or a custom system without locking the catalog to one vendor.

## When to Use

Use this skill when:

- a visual value, component behavior, or interaction state is repeated across features;
- a theme, typography, density, color, or token change could affect multiple surfaces;
- a team needs to decide whether to extend, wrap, replace, or standardize a component primitive.

Route Angular Material implementation and migration work to the existing Angular Material theming and upgrade skills. Treat Material as an optional implementation, not the design-system definition.

## Do

- Define tokens by purpose (for example, surface, emphasis, spacing, or state) rather than by a single component's appearance.
- Give each reusable component a contract for content, states, keyboard behavior, responsive behavior, and accessibility semantics.
- Validate contrast, focus, error, disabled, loading, and empty states before broad adoption.
- Prefer incremental adoption with deprecation and migration notes over a visual big-bang rewrite.
- Preserve source-of-truth boundaries: implementation tokens, component docs, and optional design-tool exports must not silently contradict each other.

## Do Not

- Do not make a design-file provider, UI library, or token generator a runtime requirement.
- Do not create a token solely to avoid discussing the semantic purpose of a value.
- Do not declare a component universally reusable without checking variants, content length, and accessibility behavior.
- Do not embed brand-specific or company-specific examples in reusable catalog guidance.

## Review Checklist

- [ ] The token or component has a documented semantic purpose and consumer contract.
- [ ] Interactive and accessibility states are included.
- [ ] The rollout has an owner, migration boundary, and rollback path.
- [ ] Optional tool exports are labelled derived rather than authoritative.
- [ ] Framework-specific work is routed to the applicable implementation skill.

## Expected Output

1. Describe the reusable contract and its intended consumers.
2. Separate platform-neutral decisions from framework implementation work.
3. List adoption, migration, and validation evidence.
4. Record outstanding visual or accessibility risks.
