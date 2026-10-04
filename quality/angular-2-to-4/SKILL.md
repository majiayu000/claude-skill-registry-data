---
id: angular.upgrade.hops.angular-2-to-4
name: Angular 2 to Angular 4 Upgrade
description: >
  Performs the Angular 2.x to Angular 4.x major-hop upgrade in a bounded, version-aware slice with dependency alignment, code adjustments, and validation.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 2 to 4
  - major hop upgrade
  - Angular version hop
  - Angular 4 migration
compatibility:
  angular:
    sourceMin: "2"
    sourceMax: "2.4.x"
    target: "4"
---

# Angular 2 to Angular 4 Upgrade

## Purpose

Use this skill to upgrade an Angular 2.x application to Angular 4.x in one bounded major hop.

This skill upgrades only from Angular 2 to Angular 4. It must not continue to Angular 5 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 2.x.
- The target hop is Angular 4.x.
- The route planner selected `2 -> 4` as the next step.
- The repository has a buildable baseline and dependency files to inspect.
- The upgrade can be done as a controlled major version hop.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is already Angular 4 or later.
- The target is Angular 5 or later.
- The task is a general modernization unrelated to this version hop.
- The project cannot produce a baseline build or install dependencies.

For AngularJS modernization, route to:

```txt
skills/angular/migration/angularjs-to-angular-modernization-orchestrator/SKILL.md
```

For the next hop, route to:

```txt
skills/angular/upgrades/hops/angular-4-to-5/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- TypeScript version
- RxJS version
- Zone.js version
- use of `@angular/upgrade`
- use of Angular animations
- use of Angular Material
- use of forms
- use of router
- use of `Renderer`
- use of `RootRenderer`
- use of `OpaqueToken`
- use of `<template>`
- use of `ngOutletContext`
- use of `preserveQueryParams`
- current build/test/lint scripts

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 2.x source | Upgrade to Angular 4.x only | Do not jump to a later major in this skill. |
| TypeScript | Align to a range compatible with Angular 4 | Verify the exact range in the project before applying. |
| RxJS | Keep the project-compatible version | Do not force a later RxJS major in this hop. |
| ngUpgrade | Move hybrid imports to `@angular/upgrade/static` where applicable | Preserve hybrid behavior. |
| Animations | Move animation symbols to `@angular/animations` where needed | Add `BrowserAnimationsModule` or `NoopAnimationsModule` only when relevant. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Scan the codebase for Angular 2-era deprecated or risky APIs.
3. Classify each occurrence by impact and required change.
4. Apply the smallest compatible dependency upgrade.
5. Make only the code changes required by the hop.
6. Validate the build, tests, and lint if commands exist.
7. Stop after Angular 4. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 2 -> Angular 4.
- Review lifecycle interfaces, animations imports, template tags, tokens, renderer usage, router changes, and ngUpgrade imports.
- Preserve `@angular/http` unless a separate HTTP migration exists.
- Prefer public APIs over deep imports.
- Keep the upgrade slice small and reviewable.
- Stop after validation and report the next hop.

## Recommended Patterns

Replace lifecycle inheritance with `implements`:

```ts
class MyComponent implements OnInit {}
```

Move animations symbols to `@angular/animations`:

```ts
import { trigger, state, style, transition, animate } from '@angular/animations';
```

Replace `<template>` with `<ng-template>` where applicable:

```html
<ng-template></ng-template>
```

Replace `OpaqueToken` with `InjectionToken`:

```ts
export const MY_TOKEN = new InjectionToken<string>('MY_TOKEN');
```

Prefer `Renderer2` or `RendererFactory2` where compatible.

Use `@angular/upgrade/static` for hybrid APIs in this range.

## Anti-Patterns

- Jumping from Angular 2 directly to Angular 21.
- Creating or following a fake Angular 3 hop.
- Updating to a TypeScript version incompatible with Angular 4.
- Removing `@angular/http` as part of this hop without a dedicated HTTP migration.
- Migrating to standalone components or signals during this hop.
- Rewriting routing architecture in the same change.
- Mixing upgrade work with visual redesign or unrelated refactors.

## Do Not

- Do not continue to Angular 5 or later.
- Do not change unrelated application architecture.
- Do not force modern Angular features that belong to later majors.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 2.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 4.x.
- [ ] TypeScript compatibility was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Hybrid imports were updated where applicable.
- [ ] Template and DI migration changes were made only when needed.
- [ ] Validation commands were run or explicitly unavailable.
- [ ] The next hop was not started automatically.

## Validation Minimum

Read `package.json` first. Only run scripts that exist.

Preferred order when available:

- build
- test
- lint

If the repository uses Angular CLI directly and the commands exist, those can be used instead.

## Risks

- Deep imports or private APIs can break the upgrade if not removed.
- Animation and template changes may be needed only in some apps, not all.
- Hybrid apps can break if `@angular/upgrade/static` is not handled consistently.
- TypeScript or RxJS mismatches can block the package upgrade.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Package manager and version evidence.
4. Applied dependency and code changes.
5. Validation commands and results.
6. Remaining risks.
7. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are aligned to Angular 4.x.
- The required compatibility code changes were applied.
- Validation ran or blockers were reported.
- The next hop remains unexecuted.

