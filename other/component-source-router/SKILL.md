---
name: component-source-router
description: Use when deciding whether to implement UI from native HTML/CSS, accessible primitives, shadcn-style source components, or visual component registries such as 21st.dev, Aceternity, React Bits, Motion Primitives, Magic UI, or Animate UI.
metadata:
  short-description: Choose accessible primitives and component sources
---

# Component Source Router

## Principle

A component source solves implementation cost; it does not define the final visual language.

## Route in this order

1. semantic native HTML/CSS when sufficient;
2. accessible unstyled primitives for complex behavior;
3. owned/source components when they save implementation time;
4. animated/visual registries as inspiration or behavior prototypes;
5. custom implementation when the signature interaction requires it.

Read `references/catalog.md` when choosing a source.

## Before adopting an external component

Check:
- behavior fit;
- accessibility and keyboard model;
- framework/runtime fit;
- dependency cost and duplication;
- styling reset effort;
- responsive behavior;
- reduced-motion behavior;
- license/current documentation.

## Integration rule

Strip generic surface styling, map to project tokens, rewrite content, adapt composition, audit states, and remove unused dependencies. If the imported component makes the page look like its registry, the integration is unfinished.
