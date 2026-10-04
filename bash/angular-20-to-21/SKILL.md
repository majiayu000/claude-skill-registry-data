---
id: angular.upgrade.hops.angular-20-to-21
name: Angular 20 to Angular 21 Upgrade
description: >
  Upgrade an Angular application from Angular 20.x to Angular 21.x using a controlled major-hop process. Use when the project is ready to move from Angular 20 to Angular 21 and needs explicit handling for TypeScript 5.9+, Node.js compatibility, zone change detection configuration, SSR security, host binding checks, router and forms changes, dynamic component migration, and removed legacy APIs.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 20 to 21
  - Angular 21 upgrade
  - SSR allowedHosts
  - UpgradeAdapter removal
compatibility:
  angular:
    min: "20"
---

# Angular 20 to Angular 21 Upgrade

## Purpose

Upgrade an Angular application from Angular 20.x to Angular 21.x using a controlled major-hop process.

## When to Use

- The project uses Angular 20.x.
- The target next hop is Angular 21.x.
- The Angular 19 -> 20 validation gate passed.
- Angular Material usage is known.
- SSR usage is known.
- AngularJS hybrid usage is known.
- Host binding usage is known.
- Test strategy is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 19.x or lower.
- The project is already Angular 21 or later.
- The previous Angular 19 -> 20 validation gate failed.
- Angular Material v20 migration has unresolved critical blockers.
- SSR security posture is unknown in an SSR app.
- AngularJS hybrid migration still uses removed APIs without a plan.
- The task is only zoneless migration.

## Mandatory Cross-Skill Routing

Before upgrading from Angular 20 to Angular 21, run:

`skills/angular/upgrades/changelog/angular-major-changelog-risk-review/SKILL.md`

If the changelog review returns `FAIL_BLOCK_NEXT_HOP`, do not continue to Angular 21.

## Recommended Cross-Skill Routing

- `skills/angular/upgrades/zone/angular-v21-zone-change-detection-root-provider/SKILL.md`
- `skills/angular/upgrades/ssr/angular-ssr-allowed-hosts-v21-security/SKILL.md`
- `skills/angular/upgrades/testing/angular-v21-router-zone-platformlocation-tests/SKILL.md`
- `skills/angular/upgrades/templates/angular-v21-host-binding-typecheck/SKILL.md`
- `skills/angular/upgrades/components/angular-v21-custom-elements-signal-inputs/SKILL.md`
- `skills/angular/upgrades/hybrid/angular-v21-upgrade-adapter-removal/SKILL.md`
- `skills/angular/upgrades/forms/angular-v21-formarray-directive-conflict/SKILL.md`
- `skills/angular/upgrades/modules/angular-v21-ngmodulefactory-removal/SKILL.md`

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
- `tsconfig.base.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `emitDeclarationOnly`
- `typeCheckHostBindings`
- `provideZoneChangeDetection`
- `ignoreChangesOutsideZone`
- `moduleId`
- `ApplicationConfig`
- `ngComponentOutletContent`
- `createCustomElement`
- `customElements.define`
- signal inputs
- `UpgradeAdapter`
- `@angular/upgrade`
- `@angular/upgrade/static`
- `FormArray`
- `formArray`
- `NgModuleFactory`
- dynamic module loading
- `Router.lastSuccessfulNavigation`
- router navigation tests
- PlatformLocation tests
- SSR files
- SSR engines
- `allowedHosts`
- `trustProxyHeaders`
- host headers
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden tests

## Dependency Upgrade

### Node.js

Use the Angular compatibility matrix as the source of truth.

### TypeScript

Angular 21 requires TypeScript 5.9 or later.

### Angular Core and CLI

Prefer updating to the latest Angular 21 patch:

```bash
ng update @angular/core@^21 @angular/cli@^21
```

If local CLI is unreliable, use:

```bash
npx @angular/cli@21 update @angular/core@^21 @angular/cli@^21
```

### Angular Material

If the project uses Angular Material, update to v21 after Angular core and CLI succeed.

```bash
ng update @angular/material@^21
```

or:

```bash
npx @angular/cli@21 update @angular/material@^21
```

## Required Code Changes

### 1. Signal inputs with custom elements

Review Angular custom elements using signal inputs and ensure direct property access where required.

### 2. Zone-based apps must provide `provideZoneChangeDetection`

Provide zone change detection at the application root when the app remains Zone-based.

### 3. Remove `ignoreChangesOutsideZone`

Remove `ignoreChangesOutsideZone` from zone configuration.

### 4. Remove custom interpolation markers

Keep only default interpolation markers.

### 5. Remove `moduleId`

Remove `moduleId` from components and directives.

### 6. Strict `ngComponentOutletContent` typing

Use `Node[][] | undefined`.

### 7. Host binding type checking

Fix host binding errors or temporarily bridge them with explicit follow-up.

### 8. `ApplicationConfig` import migration

Import `ApplicationConfig` from `@angular/core`.

### 9. `UpgradeAdapter` removal

Remove `UpgradeAdapter` and use static upgrade APIs.

### 10. Standalone `formArray` directive conflict

Rename custom directives or inputs that conflict with Angular forms names.

### 11. Remove `NgModuleFactory`

Remove dynamic module loading code that still depends on `NgModuleFactory`.

### 12. Remove `emitDeclarationOnly`

Do not use `emitDeclarationOnly` in Angular compilation paths.

### 13. Router `lastSuccessfulNavigation` is now a signal

Update reads to call it as a signal.

### 14. SSR CommonEngine allowed hosts

Configure explicit `allowedHosts` and validate trusted proxy headers.

## Do

- Run the Angular 20 changelog review before changing package versions.
- Keep SSR security, host binding checks, router, forms, and hybrid APIs explicit.
- Validate production and SSR builds when they are used.
- Route risky SSR, router, test, and DI behavior to the dedicated skills.
- Keep Material/MDC validation explicit if Material is used.

## Do Not

- Do not continue if Angular 20 changelog review failed.
- Do not keep `UpgradeAdapter`, `NgModuleFactory`, `moduleId`, or `ignoreChangesOutsideZone`.
- Do not use `allowedHosts: ['*']` without infrastructure validation.
- Do not mix this hop with zoneless modernization, control flow, defer, or standalone adoption.

## Review Checklist

- [ ] Angular 20 changelog review passed.
- [ ] TypeScript 5.9+ is compatible.
- [ ] SSR `allowedHosts` is explicit.
- [ ] `provideZoneChangeDetection` is configured when needed.
- [ ] `ignoreChangesOutsideZone` is removed.
- [ ] Host binding type errors are resolved.
- [ ] `UpgradeAdapter` is removed.
- [ ] `NgModuleFactory` is removed.
- [ ] `Router.lastSuccessfulNavigation` is read correctly.
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

- Angular 20 changelog risk review failed
- Node.js version is unsupported
- TypeScript version is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- `provideZoneChangeDetection` is missing when needed
- `ignoreChangesOutsideZone` remains
- custom interpolation remains
- `moduleId` remains
- `ApplicationConfig` is still imported from `@angular/platform-browser`
- `ngComponentOutletContent` typing is unresolved
- host binding type errors remain
- `UpgradeAdapter` remains
- `NgModuleFactory` remains
- `emitDeclarationOnly` remains in Angular compilation path
- `Router.lastSuccessfulNavigation` is accessed as a property
- custom `formArray` directive/input conflicts remain
- router timing tests are unresolved
- PlatformLocation test failures are unresolved
- SSR production lacks explicit `allowedHosts`
- SSR uses trusted proxy headers without infrastructure validation
- Material/style regressions are unreviewed
- workspace config is unstable

## Expected Output

1. Upgrade summary.
2. Changelog baseline summary.
3. SSR, router, DI, and legacy API migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 20 changelog review has passed.
- Angular dependencies are upgraded to Angular 21-compatible versions.
- Angular CLI is upgraded to v21.
- Angular Material/CDK are upgraded to v21 only if used.
- Node.js compatibility is confirmed.
- TypeScript 5.9+ compatibility is confirmed.
- SSR `allowedHosts` is explicit where used.
- Legacy APIs are removed.
- Router, forms, and host binding changes are reviewed.
- Production build has been validated.
- Validation gate result is explicit.
- The next hop is not started automatically.
