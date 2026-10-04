---
id: angular.performance.performance-audit
name: Angular Performance Audit
description: >
  Audits Angular components, features, or applications for performance risks before recommending targeted optimizations.
stack:
  - Angular
  - TypeScript
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular performance audit
  - performance checklist
  - slow component
  - slow dashboard
  - performance review
compatibility:
  angular:
    min: "2"
    recommended: "12+"
    modern: "17+"
---

# Angular Performance Audit

## Purpose

Use this skill to inspect Angular code for performance risks before making changes. The goal is to produce a prioritized diagnosis, not a pile of speculative refactors.

## Compatibility

Use patterns compatible with the detected Angular version:

- Angular 2-16: audit `*ngFor`, `trackBy`, NgModules, pure pipes, `async`, and manual subscription cleanup.
- Angular 16+: include signals and computed values when used by the project.
- Angular 17+: include `@for`, `@defer`, and modern control flow.
- Angular 20+: flag new `NgFor` usage as a modernization risk for new code.

## When to Use

Use this skill when:

- A component, page, table, dashboard, grid, or form feels slow.
- A pull request needs a performance checklist.
- The user asks for performance risks without requesting immediate refactoring.
- The application has high initial load cost, render lag, or duplicated requests.
- There are no clear measurements yet, but the code can be inspected.

## Do

Audit the relevant surfaces:

```txt
1. Version and feature profile.
2. Change detection strategy.
3. List rendering and identity tracking.
4. Template expressions and method calls.
5. Pipes and repeated transformations.
6. RxJS subscriptions, stream reuse, and cancellation.
7. Route, component, and visual lazy loading.
8. Bundle, network, and rendering evidence when available.
```

Route findings to the smallest existing skill instead of inventing a new pattern for every smell:

```txt
template method calls or expensive getters -> angular.performance.avoid-template-functions
heavy template expressions -> angular.performance.template-logic-optimization
list identity or DOM churn -> angular.performance.trackby-for-lists or angular.performance.list-rendering-optimization
initial bundle or route cost -> angular.performance.lazy-loading-strategy
rendering checks or mutation issues -> angular.performance.change-detection-optimization or angular.performance.onpush-change-detection
subscriptions, leaks, or duplicated requests -> angular.performance.rxjs-performance or angular.rxjs.avoid-nested-subscriptions
```

Classify findings by priority:

```txt
High: likely user-visible slowdown, leak, duplicated network call, or large unnecessary initial load.
Medium: repeated work, fragile rendering identity, avoidable recalculation.
Low: style-level improvement or future modernization with limited current impact.
```

## Do Not

Avoid treating every performance smell as a defect:

```txt
Small static list without trackBy -> low priority, not an emergency.
Single trivial template method -> inspect before refactoring.
OnPush missing everywhere -> not enough evidence by itself.
```

Avoid proposing syntax that the Angular version cannot support.

## Review Checklist

- [ ] Angular version and project style are identified.
- [ ] Lists are checked for `trackBy` or `@for track`.
- [ ] Heavy template logic is identified.
- [ ] Large default-change-detection components are reviewed.
- [ ] Manual subscriptions and nested subscriptions are reviewed.
- [ ] Lazy-loading opportunities are separated from rendering issues.
- [ ] Pipes are checked for purity and repeated heavy work.
- [ ] Evidence from Angular DevTools, Lighthouse, browser Performance, network, or bundle output is used when available.
- [ ] The selected follow-up skill is the smallest existing skill that matches the evidence.

## Expected Output

1. Provide a concise diagnosis.
2. List findings in priority order.
3. Recommend concrete next actions.
4. Include a minimal refactor example only when useful.
5. Explain regression risks and version compatibility constraints.
