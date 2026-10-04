---
id: angular.upgrade.hops.angular-16-to-17
name: Angular 16 to Angular 17 Upgrade
description: >
  Upgrade an Angular application from Angular 16.x to Angular 17.x using a controlled major-hop process. Use when the project is ready to move from Angular 16 to Angular 17 and needs explicit handling for changelog baseline review, Node.js/TypeScript/Zone.js requirements, router configuration, hydration, Signals, destroyed component styles, NgSwitch, Zone.js imports, and dynamic component behavior.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 16 to 17
  - Angular 17 upgrade
  - Angular 16 changelog review
  - Zone.js imports
compatibility:
  angular:
    min: "16"
---

# Angular 16 to Angular 17 Upgrade

## Purpose

Upgrade an Angular application from Angular 16.x to Angular 17.x using a controlled major-hop process.

## When to Use

- The project uses Angular 16.x.
- The target next hop is Angular 17.x.
- The Angular 15 -> 16 validation gate passed.
- The Angular 16 changelog risk review passed.
- View Engine and ngcc risks are already resolved.
- Angular Material usage is known.
- Router usage is known.
- Hydration usage is known.
- Signals usage is known.
- Zone.js usage is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 15.x or lower.
- The project is already Angular 17 or later.
- The previous Angular 15 -> 16 validation gate failed.
- Angular 16 changelog risk review failed.
- ngcc or View Engine dependency risk remains unresolved.
- The task is only control-flow migration.
- The task is only Signals refactoring.
- The task is only standalone migration.

## Mandatory Cross-Skill Routing

Before upgrading from Angular 16 to Angular 17, run:

`skills/angular/upgrades/changelog/angular-major-changelog-risk-review/SKILL.md`

For Angular 16, prefer stabilizing on the latest allowed Angular 16.2.x patch before moving to Angular 17.

If the changelog review returns `FAIL_BLOCK_NEXT_HOP`, do not continue to Angular 17.

## Recommended Cross-Skill Routing

Run these focused skills when detected:

- `skills/angular/upgrades/router/angular-router-v17-public-api-migration/SKILL.md`
- `skills/angular/upgrades/zone/angular-zonejs-imports-v17-migration/SKILL.md`
- `skills/angular/upgrades/hydration/angular-hydration-v17-risk-gate/SKILL.md`
- `skills/angular/upgrades/signals/angular-signals-mutate-to-update-v17/SKILL.md`
- `skills/angular/upgrades/styles/angular-remove-styles-on-destroy-v17/SKILL.md`
- `skills/angular/upgrades/components/angular-dynamic-component-docheck-v17/SKILL.md`

## Required Inputs

- `package.json`
- lock file
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- TypeScript version
- RxJS version
- Zone.js version
- Node.js version
- `angular.json`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- router configuration
- custom `UrlSerializer`
- absolute redirects
- `loadComponent` routes
- child routes of `loadComponent`
- Zone.js imports
- hydration config
- Signals usage
- `NgSwitch` usage
- `REMOVE_STYLES_ON_COMPONENT_DESTROY`
- dynamic component creation
- animation usage
- tests using router navigation
- tests using redirects
- tests using dynamic components
- tests using Zone.js imports
- tests using hydration/SSR
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden test scripts

## Dependency Upgrade

### Node.js

Angular 17 supports Node.js 18.13.0 and newer.

Block the upgrade when Node.js is lower than 18.13.0.

### TypeScript

Angular 17 supports TypeScript 5.2 or later.

### Zone.js

Angular 17 supports Zone.js 0.14.x or later.

### Angular Core and CLI

Run:

```bash
ng update @angular/core@17 @angular/cli@17
```

If local CLI is unreliable, use:

```bash
npx @angular/cli@17 update @angular/core@17 @angular/cli@17
```

### Angular Material

If the project uses Angular Material, update to v17 after Angular core and CLI succeed.

```bash
ng update @angular/material@17
```

or:

```bash
npx @angular/cli@17 update @angular/material@17
```

## Required Code Changes

### 1. Zone.js deep imports

Replace deep imports:

```ts
import 'zone.js/dist/zone';
import 'zone.js/bundles/zone-testing.js';
```

with:

```ts
import 'zone.js';
import 'zone.js/testing';
```

### 2. Router public API configuration

Move router configuration to `provideRouter` or `RouterModule.forRoot`.

Do not mutate router internals directly.

### 3. malformedUriErrorHandler migration

Handle URL parsing errors through `UrlSerializer.parse` instead of relying on `malformedUriErrorHandler`.

### 4. Absolute redirect behavior

Review routes with absolute redirects because Angular 17 no longer prevents additional redirects after them.

### 5. loadComponent child route inheritance

Review `loadComponent` child routes and `paramsInheritanceStrategy` when parent data must flow down.

### 6. Dynamic components and ngDoCheck

Review dynamic component creation if `ngDoCheck` side effects are involved.

### 7. Destroyed component styles removal

Review screens that may have relied on styles leaking after component destruction.

### 8. AnimationDriver.NOOP migration

Replace `AnimationDriver.NOOP` with `NoopAnimationDriver`.

### 9. NgSwitch strict equality

Review `NgSwitch` cases because comparison is now strict.

### 10. Signals mutate to update

Replace `mutate(...)` with immutable `update(...)` patterns where Signals are used.

### 11. Hydration API changes

Use supported hydration APIs only.

### 12. Optional modernizations not included

Do not automatically migrate to built-in control flow, deferrable views, standalone architecture, signals refactors, or zoneless experimentation during this hop.

## Do

- Run the Angular 16 changelog risk review before changing package versions.
- Keep changelog baseline, runtime requirements, and router/hydration risk explicit.
- Validate SSR and hydration when used.
- Validate dynamic components, NgSwitch, and style cleanup where present.
- Keep Material/MDC validation explicit if Material is used.

## Do Not

- Do not continue if Angular 16 changelog review failed.
- Do not keep Zone.js deep imports.
- Do not mutate router internals directly.
- Do not ignore absolute redirect loops.
- Do not mix control flow or Signals modernization into the hop.
- Do not rely on leaked component styles as architecture.

## Review Checklist

- [ ] Angular 16 changelog review passed.
- [ ] Node.js, TypeScript, and Zone.js are compatible.
- [ ] Zone.js deep imports are removed.
- [ ] Router configuration is public-API-based.
- [ ] Absolute redirects are reviewed.
- [ ] `loadComponent` inheritance is reviewed.
- [ ] Hydration behavior is validated where used.
- [ ] `NgSwitch` strict equality cases are reviewed.
- [ ] Signals `mutate` usage is removed or documented.
- [ ] Dynamic component behavior is validated.
- [ ] Destroyed component style cleanup is reviewed.
- [ ] Material/MDC regression risk is reviewed.
- [ ] Production build passes.

## Validation

Run only existing scripts:

- `npm run build`
- `npm run test`
- `npm run lint`
- `npm run e2e`
- `ng build --configuration production`
- `npm run build:ssr`
- `npm run prerender`
- `npm run serve:ssr`

## Validation Gate

Use `FAIL_BLOCK_NEXT_HOP` when:

- Angular 16 changelog risk review failed
- Node.js is lower than 18.13.0
- TypeScript version is unsupported
- Zone.js version is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- Zone.js deep imports remain
- router internals are still mutated directly
- malformed URI handling is unresolved
- absolute redirect loops are possible or untested
- critical `loadComponent` inheritance is broken
- dynamic component `ngDoCheck` side effects are unresolved
- component style removal breaks critical screens
- `AnimationDriver.NOOP` remains
- critical `NgSwitch` loose equality cases remain
- Signals `mutate` remains
- hydration behavior is unknown in SSR/hydrated apps
- Material/style regressions are unreviewed
- workspace config is unstable

## Expected Output

1. Upgrade summary.
2. Changelog baseline summary.
3. Router and hydration migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 16 changelog risk review has passed.
- Angular dependencies are upgraded to Angular 17-compatible versions.
- Angular CLI is upgraded to v17.
- Angular Material/CDK are upgraded to v17 only if used.
- Node.js 18.13.0+ compatibility is confirmed.
- TypeScript 5.2+ compatibility is confirmed.
- Zone.js 0.14.x+ compatibility is confirmed.
- Zone.js deep imports are migrated.
- Router configuration does not rely on removed direct mutation patterns.
- Hydration is validated where used.
- NgSwitch strict equality cases are reviewed.
- Signals mutate usage is removed or documented.
- Angular Material and style regressions are reviewed.
- Production build has been validated.
- Validation gate result is explicit.
- The next hop is not started automatically.
