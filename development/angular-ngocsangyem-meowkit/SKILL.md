---
name: mk:angular
version: 1.0.0
description: |
  Use when working with Angular code — components, signals, services, forms,
  routing, HTTP, testing, SSR, or tooling. Targets Angular v20+ modern patterns.
  Auto-activates on .ts files in Angular projects (detected via angular.json).
allowed-tools:
  - Read
  - Grep
  - Glob
source: analogjs/angular-skills
license: MIT
original_skills:
  - angular-component
  - angular-signals
  - angular-di
  - angular-directives
  - angular-forms
  - angular-http
  - angular-routing
  - angular-ssr
  - angular-testing
  - angular-tooling
keywords:
  - angular
  - signals
  - components
  - ssr
  - angular-cli
  - framework-specific
  - ts-angular
when_to_use: Use when writing Angular v20+ code (components, signals, services, forms, routing, HTTP, SSR). Auto-activates on .ts files in Angular projects. NOT for generic TypeScript (see mk:typescript) or Vue/React.
user-invocable: true
owner: utility
criticality: medium
status: active
runtime: claude-code
---

# Angular

Angular v20+ patterns — 10 topics consolidated with progressive disclosure.

## v20+ Modern Defaults (apply always)

- **Standalone components** are default — no NgModule needed
- **Signal-based inputs/outputs** — use `input()`, `input.required()`, `output()` (not `@Input`/`@Output`)
- **Signal-based state** — use `signal()`, `computed()`, `linkedSignal()` (not BehaviorSubject)
- **inject() function** — use `inject()` in field initializers (not constructor injection)
- **Native control flow** — use `@if`, `@for` with `track`, `@switch` (not `*ngIf`/`*ngFor`)
- **OnPush change detection** — always set `changeDetection: ChangeDetectionStrategy.OnPush`
- **Functional guards/resolvers** — use functions (not class-based guards)
- **resource() / httpResource()** — prefer over manual HttpClient subscribe for data loading

## When to Read Each Reference

| Task involves                                                  | Read                       |
| -------------------------------------------------------------- | -------------------------- |
| Components, templates, host bindings, content projection       | `references/component.md`  |
| signal(), computed(), linkedSignal(), effect(), reactive state | `references/signals.md`    |
| inject(), providers, injection tokens, services                | `references/di.md`         |
| Custom directives, DOM manipulation, host listeners            | `references/directives.md` |
| Forms, validation, signal forms API                            | `references/forms.md`      |
| HTTP calls, resource(), httpResource(), interceptors           | `references/http.md`       |
| Routes, lazy loading, guards, resolvers, navigation            | `references/routing.md`    |
| SSR, hydration, prerendering, browser-only APIs                | `references/ssr.md`        |
| Unit tests, integration tests, TestBed, Vitest                 | `references/testing.md`    |
| Angular CLI, schematics, build config, project setup           | `references/tooling.md`    |

Read multiple references when task spans topics (e.g., component + signals + forms).

## Gotchas (top 5 — most common Claude mistakes)

1. **Using @Input/@Output decorators**: deprecated in v20+ → use `input()`, `output()` signal functions
2. **Using *ngIf/*ngFor**: deprecated template syntax → use `@if`, `@for` with `track` expression
3. **Constructor injection**: outdated pattern → use `inject()` in field initializers
4. **BehaviorSubject for component state**: over-complex → use `signal()` + `computed()`
5. **Class-based guards/interceptors**: deprecated → use functional `CanActivateFn`, `HttpInterceptorFn`

Full list: `references/gotchas.md`

## Workflow Integration

Auto-activates during Phase 3 (Build) when Angular project detected (angular.json or @angular/core in package.json). Loaded by `developer` agent alongside `mk:typescript`.
