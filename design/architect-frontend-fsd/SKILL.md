---
name: architect-frontend-fsd
description: Explain Feature-Sliced Design (FSD) for frontends, including layers, slices, segments, public APIs, and dependency boundaries.
metadata:
  language: en
  translation_of: architect-frontend-fsd-cn
  version: "0.1.0"
---

# Feature-Sliced Design for frontends

Based on the official Feature-Sliced Design specification.

FSD groups code into layers by responsibility, slices by their meaning to the product, and segments by purpose. Slices keep related changes together. Public APIs give consumers a stable entry point.

## Architecture shape

```text
<source root>/
  app/routes/
  pages/product-details/{ui,api}/
  widgets/product-gallery/ui/
  features/add-to-cart/{ui,model}/
  entities/product/{model,ui}/
  shared/{ui,api}/
```

| Layer | Responsibility |
|---|---|
| `app` | Entry points, routing, global styles, and dependency wiring. |
| `pages` | Full screens or major route content, including page-specific UI, state, and requests. |
| `widgets` | Self-contained UI blocks reused across pages or serving as independent regions within a page. |
| `features` | Reusable user actions with business value, such as adding an item to a cart. |
| `entities` | Business entities and their models, data access, or UI representations, such as products. |
| `shared` | General UI components, API clients, configuration, and libraries. |

`app` and `shared` contain segments directly. The other layers contain slices, which contain segments. Common segments include `ui` for presentation, `model` for state and rules, `api` for external interactions, `lib` for supporting code, and `config` for settings. Use layers and segments as their responsibilities arise. `processes` is deprecated.

## Dependency boundaries

- From highest to lowest, the layers are `app → pages → widgets → features → entities → shared`. Imports across slices target strictly lower layers and can skip intermediate layers. Modules within a slice can reference one another, as can segments within `app` or within `shared`.
- Consumers access a slice through its public API. Segments in `app` and `shared` also provide public entry points. Export what consumers need explicitly. Within a slice, import internal modules directly.
- Compose sibling slices in a higher layer. When two entities have a direct model relationship, `@x` can expose a dedicated API to the named consumer. For example, `entities/product/@x/order` serves `entities/order`.

## Pages first

Keep page-specific UI, state, and requests in the page slice. A request specific to product details belongs in `pages/product-details/api`. When multiple pages reuse the add-to-cart action, `features/add-to-cart` owns the behavior and exposes an entry point for those pages.

## Relationship to feature-first

Feature-first typically groups modules by business capability, then separates responsibilities within each module. FSD defines global layers, groups slices by product meaning within those layers, and governs imports between slices through the layer order.
