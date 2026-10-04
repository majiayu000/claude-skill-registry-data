---
id: angular.upgrade.hops.angular-4-to-5
name: Angular 4 to Angular 5.2 Upgrade
description: >
  Performs the Angular 4.x to Angular 5.2.x major-hop upgrade in a bounded, version-aware slice with dependency alignment, compatibility checks, and validation.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 4 to 5
  - Angular 5.2 upgrade
  - major hop upgrade
  - Angular version hop
compatibility:
  angular:
    sourceMin: "4"
    sourceMax: "4.x"
    target: "5.2"
---

# Angular 4 to Angular 5.2 Upgrade

## Purpose

Use this skill to upgrade an Angular 4.x application to Angular 5.2.x in one bounded major hop.

This skill upgrades only from Angular 4 to Angular 5.2. It must not continue to Angular 6 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 4.x.
- The target hop is Angular 5.2.x.
- The route planner selected `4 -> 5` as the next step.
- The repository has a buildable baseline and dependency files to inspect.
- The upgrade must remain controlled and reversible.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 2.x.
- The project is already Angular 5 or later.
- The requested change is Angular 5 to Angular 6.
- The project cannot produce a baseline build or install dependencies.
- The task is general modernization unrelated to this version hop.

For AngularJS modernization, route to:

```txt
skills/angular/migration/angularjs-to-angular-modernization-orchestrator/SKILL.md
```

For the next hop, route to:

```txt
skills/angular/upgrades/hops/angular-5-to-6/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- TypeScript version
- RxJS version
- Zone.js version
- use of `@angular/upgrade`
- use of Angular Material
- use of animations
- use of i18n
- use of date, currency, decimal, or percent pipes
- use of Angular compiler options
- use of `gendir`
- use of forms
- use of router
- use of `Renderer`
- use of `OpaqueToken`
- use of `<template>`
- use of `ngOutletContext`
- use of `preserveQueryParams`
- current build/test/lint scripts

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 4.x source | Upgrade to Angular 5.2.x only | Do not jump to a later major in this skill. |
| TypeScript | Align to `2.4.2` unless project evidence proves a stricter compatible range is required | Verify against the repo before changing. |
| RxJS | Align to `^5.5.2` | Do not force RxJS 6 syntax in this hop. |
| ngUpgrade | Move hybrid imports to `@angular/upgrade/static` where applicable | Preserve hybrid behavior. |
| i18n/locale | Register locale data when the app uses locale-sensitive pipes outside `en-US` | Do not add locale data blindly. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Scan the codebase for Angular 4-era deprecated or risky APIs.
3. Classify each occurrence by impact and required change.
4. Apply the bounded dependency upgrade to Angular 5.2.
5. Make only the code changes required by the hop.
6. Run validation commands that exist in the repository.
7. Stop after Angular 5.2. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 4 -> Angular 5.2.
- Review locale data, pipe formatting, `gendir`, RxJS compatibility, templates, DI tokens, renderers, router query params, and ngUpgrade imports.
- Preserve `@angular/http` unless a separate HTTP migration exists.
- Prefer public APIs over deep imports.
- Keep the upgrade slice small and reviewable.
- Stop after validation and report the next hop.

## Recommended Patterns

Update Angular packages to Angular 5.2:

```bash
npm install @angular/animations@^5.2.0 @angular/common@^5.2.0 @angular/compiler@^5.2.0 @angular/compiler-cli@^5.2.0 @angular/core@^5.2.0 @angular/forms@^5.2.0 @angular/http@^5.2.0 @angular/platform-browser@^5.2.0 @angular/platform-browser-dynamic@^5.2.0 @angular/platform-server@^5.2.0 @angular/router@^5.2.0 typescript@2.4.2 rxjs@^5.5.2
```

Register locale data only when needed:

```ts
import { registerLocaleData } from '@angular/common';
import localeEs from '@angular/common/locale/es';

registerLocaleData(localeEs);
```

Move `ngUpgrade` imports to the static package:

```ts
import { downgradeComponent, downgradeInjectable, UpgradeComponent, UpgradeModule } from '@angular/upgrade/static';
```

Replace `preserveQueryParams` with `queryParamsHandling: 'preserve'`.

Replace `[ngOutletContext]` with `[ngTemplateOutletContext]`.

## Anti-Patterns

- Jumping from Angular 4 directly to Angular 21.
- Starting Angular 6 migration in the same change.
- Upgrading to RxJS 6 in this hop.
- Upgrading to a modern TypeScript version incompatible with Angular 5.2.
- Removing `@angular/http` without a dedicated HTTP migration.
- Introducing standalone components or signals.
- Rewriting the router architecture.
- Rewriting all forms.
- Replacing Angular Material blindly.
- Mixing upgrade work with visual redesign.
- Claiming success without validation.

## Do Not

- Do not continue to Angular 6 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 4.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 5.2.x.
- [ ] TypeScript compatibility was checked.
- [ ] RxJS compatibility was checked.
- [ ] Locale-sensitive formatting was reviewed.
- [ ] Deprecated APIs were classified and handled.
- [ ] Hybrid imports were updated where applicable.
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
- Locale-sensitive pipe output can change without explicit locale registration.
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

- Angular packages are aligned to Angular 5.2.x.
- The required compatibility code changes were applied.
- Validation ran or blockers were reported.
- The next hop remains unexecuted.

