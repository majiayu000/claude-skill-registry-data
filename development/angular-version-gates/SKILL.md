---
id: angular.versioning.angular-version-gates
name: Angular Version Gates
description: >
  Detects Angular version constraints before recommending APIs such as Signals, signal inputs, standalone APIs, control flow, @defer, takeUntilDestroyed, resource, or httpResource.
stack:
  - Angular
  - TypeScript
  - RxJS
category: versioning
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular version compatibility
  - version gates
  - unsupported Angular API
  - Angular 12 compatibility
  - Angular 17 migration
  - Angular 20 modernization
compatibility:
  angular:
    min: "2"
    recommendedDetection: "package.json"
---

# Angular Version Gates

## Purpose

Use this skill to prevent the agent from recommending Angular APIs that the target project cannot compile or safely support. The goal is to detect the version first, choose compatible patterns, and provide future migration paths separately.

This skill is a lightweight compatibility helper. For a formal hop gate and version matrix, prefer:

```txt
skills/angular/versioning/angular-version-compatibility-gate/SKILL.md
```

## When to Use

Use this skill when:

- Angular version is unknown.
- A recommendation mentions Signals, `toSignal`, `toObservable`, signal inputs, `@for`, `@defer`, `takeUntilDestroyed`, standalone APIs, `resource`, or `httpResource`.
- A recommendation changes DI style between constructor injection, `inject()`, NgModule providers, application providers, route providers, or component providers.
- The project may support Angular 12-15, Angular 16, Angular 17-18, Angular 19+, or Angular 20+ differently.
- The project may support Angular 22 differently from earlier majors.
- A shared library is consumed by multiple Angular versions.
- The user asks for a modern Angular refactor without stating version constraints.
- The user needs a broad compatibility reminder and a lighter version-style profile before the dedicated gate is invoked.

## Do

Inspect version evidence:

```txt
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
angular.json
nx.json
tsconfig.json
tsconfig.base.json
existing templates and component syntax
```

Apply conservative gates:

```txt
Angular 2-13:
  use NgModules, *ngFor, trackBy, RxJS, async, OnPush, takeUntil
  use constructor injection as the safest DI default
  avoid standalone-only assumptions, Signals, @for, @defer, inject() as a required convention, takeUntilDestroyed

Angular 14-15:
  standalone may exist depending on project adoption
  keep NgModules valid
  avoid Signals, @for, @defer, takeUntilDestroyed as required patterns

Angular 16:
  Signals and RxJS interop are available but require project acceptance
  avoid forcing Signals into shared public contracts
  keep RxJS as the default for async orchestration

Angular 17-18:
  modern control flow and @defer can be considered
  keep fallbacks if the codebase still uses legacy patterns

Angular 19+:
  takeUntilDestroyed is a safe modern lifecycle pattern when dependencies support it
  Signals are suitable for local synchronous state

Angular 20+:
  prefer @for for new list rendering code
  avoid introducing new NgFor-based code unless maintaining legacy sections

Angular 22+:
  resource and httpResource are production-ready
  Signal Forms and Angular Aria are production-ready
  strictTemplates defaults to true and fullTemplateTypeCheck is removed
  webpack builders are deprecated; prefer the supported build path
  keep component, router, and SSR contracts explicit because several legacy APIs were removed
```

Flag experimental APIs explicitly:

```txt
In Angular 22, Signal Forms, Angular Aria, resource(), and httpResource() are production-ready per official Angular sources. WebMCP and future preview APIs remain experimental and need explicit security/risk gates.
```

## Do Not

Avoid unsupported recommendations:

```txt
Use @for in an Angular 12 project.
Use Signals in an Angular 15 project.
Use @defer without Angular 17+ support.
Use WebMCP or preview APIs as a stable default production pattern without a security gate.
```

Avoid assuming the latest Angular version from code style alone.

Avoid using migration syntax in shared libraries consumed by older Angular apps.

## Review Checklist

- [ ] Angular version is detected or uncertainty is stated.
- [ ] Node, TypeScript, and RxJS compatibility are considered when relevant.
- [ ] Recommended APIs are supported by the detected version.
- [ ] Modern alternatives are separated from compatible code.
- [ ] Fallbacks are provided for older Angular versions.
- [ ] Experimental APIs are clearly marked and avoided by default.
- [ ] Shared library compatibility is preserved.
- [ ] The recommendation includes a migration path when modern APIs are not available.

## Expected Output

1. Report detected Angular, TypeScript, RxJS, Node, and tooling versions when available.
2. Select a compatibility profile.
3. List APIs that are safe to use.
4. List APIs to avoid for this project.
5. Provide compatible implementation and optional future migration path.

If a formal upgrade decision is required, hand off to:

```txt
skills/angular/versioning/angular-version-compatibility-gate/SKILL.md
```
