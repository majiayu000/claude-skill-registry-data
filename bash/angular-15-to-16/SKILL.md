---
id: angular.upgrade.hops.angular-15-to-16
name: Angular 15 to Angular 16 Upgrade
description: >
  Upgrade an Angular application from Angular 15.x to Angular 16.x using a controlled major-hop process. Use when the project is ready to move from Angular 15 to Angular 16 and needs explicit handling for ngcc removal, View Engine library compatibility, SSR/TransferState changes, dynamic component creation, router typing, and build output changes.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 15 to 16
  - Angular 16 upgrade
  - ngcc removal
  - View Engine libraries
compatibility:
  angular:
    min: "15"
---

# Angular 15 to Angular 16 Upgrade

## Purpose

Upgrade an Angular application from Angular 15.x to Angular 16.x using a controlled major-hop process.

This hop is a hard compatibility boundary because Angular 16 removes `ngcc`. Projects on Angular 16 and later no longer support View Engine libraries.

## When to Use

- The project uses Angular 15.x.
- The target next hop is Angular 16.x.
- The Angular 14 -> 15 validation gate passed.
- Angular Material status is known.
- View Engine / ngcc library status is known or ready to be audited.
- SSR usage is known.
- TransferState usage is known.
- Dynamic component creation usage is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 14.x or lower.
- The project is already Angular 16 or later.
- The previous Angular 14 -> 15 validation gate failed.
- Critical View Engine libraries exist and no Angular 16-compatible version is available.
- The task is only standalone migration.
- The task is only signals adoption.

## Mandatory Cross-Skill Routing

Before upgrading to Angular 16, run:

`skills/angular/upgrades/libraries/angular-ngcc-view-engine-removal-v16/SKILL.md`

Use it to detect:

- `ngcc` scripts
- View Engine-only libraries
- `__ivy_ngcc__`
- `metadata.json`
- postinstall compatibility scripts

If a critical View Engine-only library is detected, return `FAIL_BLOCK_NEXT_HOP`.

## Required Inputs

- `package.json`
- lock file
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- TypeScript version
- RxJS version
- `zone.js` version
- Node.js version
- `angular.json`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- Angular libraries
- library build scripts
- `postinstall` scripts
- `ngcc` references
- `__ivy_ngcc__` references
- Angular Universal usage
- SSR entry points
- `renderModuleFactory`
- `renderModule`
- `renderApplication`
- `TransferState`
- `ComponentFactoryResolver`
- `ViewContainerRef.createComponent`
- `EnvironmentInjector.runInContext`
- `ReflectiveInjector`
- `Injector.create`
- `entryComponents`
- `ANALYZE_FOR_ENTRY_COMPONENTS`
- `moduleId`
- Router events
- `RendererType2.styles`
- `QueryList.filter`
- `BrowserModule.withServerTransition`
- `APP_ID`
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden tests

## Dependency Upgrade

### Node.js

Angular 16 supports Node.js v16 and v18.

Block the upgrade when Node.js is not supported.

### TypeScript

Angular 16 supports TypeScript 4.9.3 or later.

### Zone.js

Angular 16 supports Zone.js 0.13.x or later.

### Angular Core and CLI

Run:

```bash
ng update @angular/core@16 @angular/cli@16
```

If the local CLI is unreliable, use:

```bash
npx @angular/cli@16 update @angular/core@16 @angular/cli@16
```

### Angular Material

If the project uses Angular Material, update to v16 after Angular core and CLI succeed.

```bash
ng update @angular/material@16
```

or:

```bash
npx @angular/cli@16 update @angular/material@16
```

Do not upgrade Material beyond v16 in this hop.

## Required Code Changes

### ngcc and View Engine removal

Remove `ngcc` scripts only after confirming all Angular libraries are Ivy-compatible.

Gate behavior:

- Critical View Engine-only dependency = `FAIL_BLOCK_NEXT_HOP`
- Unknown Angular library compatibility = `FAIL_BLOCK_NEXT_HOP`
- `ngcc` script still required = `FAIL_BLOCK_NEXT_HOP`

### Router event typing

Review code that handles router events and update assumptions around `RouterEvent` and `NavigationSkipped`.

### RendererType2.styles

Flatten nested style arrays to a flat string array where required.

### BrowserPlatformLocation tests

Review router and location tests that rely on mocked platform location behavior.

### ApplicationConfig import

Import `ApplicationConfig` from `@angular/core`.

### renderModuleFactory removal

Replace `renderModuleFactory` with `renderModule`.

### XhrFactory import

Import `XhrFactory` from `@angular/common`.

### BrowserModule.withServerTransition

Replace with `APP_ID` where multiple apps require unique app IDs.

### EnvironmentInjector.runInContext

Replace with `runInInjectionContext` where applicable.

### Dynamic component creation

Use `ViewContainerRef.createComponent` without factory resolver where possible.

### renderApplication

Update `renderApplication` usage to the Angular 16 signature.

### PlatformConfig

Remove deprecated server platform config usage.

### moduleId

Remove `moduleId` from `@Component` and `@Directive`.

### TransferState

Import `TransferState`, `makeStateKey`, and `StateKey` from `@angular/core`.

### entryComponents and ANALYZE_FOR_ENTRY_COMPONENTS

Remove both from active metadata.

### ngTemplateOutletContext

Review stricter typing for template outlet context objects.

### APF / ES2022

Review custom build tooling for ES2022-compatible distributed output.

### EventManager

Remove `EventManager.addGlobalEventListener` usage.

### BrowserTransferStateModule

Remove `BrowserTransferStateModule`.

### ReflectiveInjector

Replace with `Injector.create`.

### QueryList.filter

Review type-guard narrowing behavior.

## Do

- Run the ngcc and View Engine audit before changing Angular package versions.
- Review SSR, TransferState, and dynamic component creation together when they are used in the project.
- Validate Angular Material/MDC, router, and build tooling after the update.
- Keep library compatibility and build output as explicit gate conditions.

## Do Not

- Do not keep `ngcc` as a workaround.
- Do not continue if critical View Engine-only libraries remain.
- Do not ignore ES2022 build-tool compatibility.
- Do not mix standalone or signals adoption into this hop.

## Review Checklist

- [ ] Node.js, TypeScript, and Zone.js are compatible.
- [ ] `ngcc` is not required.
- [ ] View Engine-only libraries are resolved or blocked.
- [ ] SSR and TransferState paths are updated where used.
- [ ] Dynamic component creation no longer relies on factory resolvers.
- [ ] `entryComponents` and `ANALYZE_FOR_ENTRY_COMPONENTS` are removed.
- [ ] Material/MDC and style regressions are reviewed.
- [ ] Production build passes.

## Validation

Run only existing commands:

- `npm run build`
- `npm run test`
- `npm run lint`
- `npm run e2e`
- `ng build --configuration production`
- `npm run build:ssr`
- `npm run serve:ssr`
- `npm run prerender`

## Validation Gate

Use `FAIL_BLOCK_NEXT_HOP` when:

- Node.js is unsupported
- TypeScript is unsupported
- Zone.js is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- ngcc is still required
- View Engine-only critical libraries remain
- Angular library compatibility is unknown
- SSR still uses removed APIs
- `TransferState` imports are unresolved
- `BrowserTransferStateModule` remains
- `ComponentFactoryResolver` migration is unresolved
- `ReflectiveInjector` remains
- `ANALYZE_FOR_ENTRY_COMPONENTS` remains
- `entryComponents` remains in active metadata
- `ngTemplateOutletContext` typing errors remain
- custom build tooling cannot consume ES2022 output
- `EventManager.addGlobalEventListener` remains
- dynamic component loaders fail
- multiple apps have non-unique `APP_ID`s
- Material/MDC/style regressions are unreviewed

## Expected Output

1. Upgrade summary.
2. ngcc/View Engine audit summary.
3. SSR and DI migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 16 upgrade is complete.
- `ngcc` is not required.
- View Engine compatibility is explicit.
- Validation gate is explicit.
- The next hop is not started automatically.
