---
name: architect-frontend-feature-first
description: Explain feature-first frontend architecture. Define capability ownership, layers as needed, source dependencies, and cross-feature collaboration.
metadata:
  language: en
  translation_of: architect-frontend-feature-first-cn
  version: "0.1.0"
---

# Feature-first frontend architecture

Based on Rémy Baudet’s Feature-First Clean Architecture.

A feature owns a business capability and the UI, models, and data access that change with it. Product list and detail screens can both belong to `products`. Changes to the capability stay within one module.

## Shape and responsibilities

```text
<source root>/
  app/
  features/<feature>/
    presentation/
    domain/
    data/
    application/
  shared/
```

- `presentation` owns the UI, interactions, and UI state.
- `domain` defines business models and rules. It owns repository contracts when the business needs external data.
- `data` implements repository contracts and handles external data access and mapping.
- `application` coordinates use cases that span multiple operations or capabilities.
- `app` wires dependencies and manages routes. `shared` provides code independent of specific features.

Create folders as their responsibilities appear. A display-only feature can have just `presentation`. A headless feature can omit it. Entry points and routes follow framework conventions.

## Dependency rules

Arrows show source dependencies. Apply each rule where the relevant layers exist.

```text
presentation → domain
presentation → application → domain
data         → domain
```

Domain rules stay independent of UI frameworks and I/O implementations. The app injects implementations. Features collaborate through the owner's public contracts or use cases and keep dependencies acyclic. Features express navigation intent. The app router chooses the destination.

## Related styles

Feature-first uses business capabilities as the primary boundary. Layer-first groups by technical role, and page-first by route or screen. Clean Architecture governs source dependencies. MVVM organizes presentation. Both can be used within a feature-first layout.
