---
id: angular.performance.lazy-loading-strategy
name: Angular Lazy Loading Strategy
description: >
  Reduces Angular initial load cost by selecting compatible lazy loading patterns for routes, standalone components, feature modules, and deferrable views.
stack:
  - Angular
  - TypeScript
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - lazy loading
  - initial bundle
  - loadChildren
  - loadComponent
  - "@defer"
  - route splitting
compatibility:
  angular:
    min: "2"
    standaloneStableFrom: "15"
    deferFrom: "17"
---

# Angular Lazy Loading Strategy

## Purpose

Use this skill to reduce initial load cost by loading Angular features, routes, components, and non-critical UI only when needed.
If the issue is shared-module bloat or eager imports rather than routing, pair this with the relevant architecture or bundle-control skill instead of forcing route changes.

## Compatibility

Use the compatible variant:

- Angular 2+: use route-level lazy loading with `loadChildren`.
- Angular 14-15+: use standalone components and `loadComponent` only when the project supports standalone APIs.
- Angular 17+: use `@defer` for non-critical visual content when dependencies can actually be deferred.
- All versions: measure bundle impact before and after the change.

## When to Use

Use this skill when:

- The initial bundle is large.
- A feature is not needed at application startup.
- Routes, dashboards, reports, admin sections, or heavy widgets load eagerly.
- Third-party libraries are imported globally but used in limited areas.
- The user asks to improve initial load time or Core Web Vitals.
- The app uses NgModules, standalone APIs, or both, and the smallest compatible lazy boundary must be selected.

## Do

Use route-level lazy loading for feature routes:

```ts
{
  path: 'admin',
  loadChildren: () =>
    import('./admin/admin.routes').then((module) => module.ADMIN_ROUTES),
}
```

Use standalone component lazy loading when supported:

```ts
{
  path: 'detail',
  loadComponent: () =>
    import('./detail/detail.component').then((module) => module.DetailComponent),
}
```

Use `@defer` for non-critical visual content in Angular 17+:

```html
@defer (on viewport) {
<app-heavy-widget />
} @placeholder {
<app-heavy-widget-skeleton />
}
```

Separate critical initial content from demand-loaded, deferred, and preloaded content.
Prefer route boundaries first, then component-level lazy loading, then visual deferral only when it actually reduces startup cost.

## Do Not

Avoid eager feature imports:

```ts
import { AdminModule } from "./admin/admin.module";
```

Avoid placing large feature dependencies in a global shared module.
Avoid using lazy loading as a substitute for poor feature boundaries or duplicated imports that should be fixed at the module or route layer.

Avoid using `@defer` for content that must be visible immediately on initial render unless layout stability and user experience are handled.

Avoid assuming a component inside `@defer` is actually split if it is also referenced outside the defer block.

## Review Checklist

- [ ] Initial route and bundle cost are identified.
- [ ] Critical startup content is separated from non-critical content.
- [ ] `loadChildren` is used for feature boundaries when appropriate.
- [ ] `loadComponent` is used only when standalone support fits the project.
- [ ] `@defer` is used only when Angular version and dependency constraints support it.
- [ ] Heavy third-party dependencies are not imported globally by accident.
- [ ] Preloading strategy is considered for post-startup user experience.
- [ ] Bundle output is measured after the change.

## Expected Output

1. Identify what is loaded at startup and why.
2. Select route, component, visual defer, or preloading strategy.
3. Provide code compatible with the detected Angular version.
4. Preserve routing and user experience.
5. Explain bundle, SSR, hydration, and layout-shift risks when relevant.
