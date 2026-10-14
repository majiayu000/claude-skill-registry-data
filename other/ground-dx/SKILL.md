---
name: ground-dx
description: The 7 DX dimensions. An evaluation framework for package quality.
---

# Skill: The 7 DX Dimensions

> "DX is the product. Everything else serves it."

## The Standard

- **First-Touch**: Steps from `composer require` to working code. Target: 1-3 steps. If your install instructions have more than 3 numbered steps, simplify.
- **Cognitive Load**: How much the developer must learn. The best packages add zero new mental models -- you learn your domain through the package's lens.
- **Error Messages**: Tell what's wrong AND what's valid. Named constructors with interpolated context. One exception class per failure mode.
- **IDE Experience**: Code that autocompletes beautifully. `@template`, `@mixin`, `@method`, union types. The IDE is a feature surface.
- **Migration Path**: Before/after code examples for every breaking change. Additive migrations. Broad version constraints. Honest about pain.
- **Defaults**: Zero-config for 80% of developers. Three-tier override: config-level, model-level, call-level. Customize only what you need.
- **Progressive Disclosure**: Four additive layers. Trait or function (80%), config or preset (15%), provider or plugin (4%), contract implementation (1%).

## The Check

Ask yourself:
- Can a developer go from `composer require` to working code in under 2 minutes?
- Does the IDE autocomplete every public method?
- Will the next major upgrade take hours, not days?
- Does every dimension score "good" or better?

## Real-World Examples

See [examples.md](examples.md).
