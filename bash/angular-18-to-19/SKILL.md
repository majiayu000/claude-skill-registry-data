---
id: angular.upgrade.hops.angular-18-to-19
name: Angular 18 to Angular 19 Upgrade
description: >
  Upgrade an Angular application from Angular 18.x to Angular 19.x using a controlled major-hop process. Use when the project is ready to move from Angular 18 to Angular 19 and needs explicit handling for standalone defaults, TypeScript 5.5+, tests, router error handling, dynamic component projection, localize builder changes, signals/effects timing, and NgModule compatibility.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 18 to 19
  - Angular 19 upgrade
  - standalone default
  - effects timing
compatibility:
  angular:
    min: "18"
---

# Angular 18 to Angular 19 Upgrade

## Purpose

Upgrade an Angular application from Angular 18.x to Angular 19.x using a controlled major-hop process.

## When to Use

- The project uses Angular 18.x.
- The target next hop is Angular 19.x.
- The Angular 17 -> 18 validation gate passed.
- Angular Material usage is known.
- NgModule and standalone usage is known.
- Router usage is known.
- Effects/signals usage is known.
- Test strategy is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 17.x or lower.
- The project is already Angular 19 or later.
- The previous Angular 17 -> 18 validation gate failed.
- Angular Material v18 migration has unresolved critical blockers.
- The project has unknown NgModule/standalone status.
- Test behavior is unknown in a test-heavy project.
- Router error handling is unknown in a routing-heavy project.

## Mandatory Cross-Skill Routing

Before upgrading from Angular 18 to Angular 19, run:

`skills/angular/upgrades/changelog/angular-major-changelog-risk-review/SKILL.md`

If the changelog review returns `FAIL_BLOCK_NEXT_HOP`, do not continue to Angular 19.

## Recommended Cross-Skill Routing

- `skills/angular/upgrades/standalone/angular-standalone-default-v19-ngmodule-compat/SKILL.md`
- `skills/angular/upgrades/testing/angular-v19-effects-and-fakeasync-scheduler/SKILL.md`
- `skills/angular/upgrades/router/angular-router-error-handler-v19/SKILL.md`
- `skills/angular/upgrades/components/angular-create-component-projectable-nodes-v19/SKILL.md`
- `skills/angular/upgrades/localize/angular-localize-builder-v19/SKILL.md`

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
- `angularCompilerOptions`
- `strictStandalone`
- NgModule declarations
- components/directives/pipes with `standalone`
- template reference variable usage
- `BrowserModule.withServerTransition`
- `APP_ID`
- `KeyValueDiffers`
- `@angular/localize` builder config
- `ExperimentalPendingTasks`
- `PendingTasks`
- signals/effects usage
- tests using `fakeAsync`
- tests using `tick`
- tests using `flush`
- tests using `whenStable`
- tests using `autoDetectChanges`
- custom elements usage
- `createComponent` usage
- `projectableNodes`
- components with fallback `ng-content`
- router usage
- `Router.errorHandler`
- `withNavigationErrorHandler`
- `Resolve`
- `RedirectCommand`
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden tests

## Dependency Upgrade

### TypeScript

Angular 19 requires TypeScript 5.5 or later.

### Angular Core and CLI

Run:

```bash
ng update @angular/core@19 @angular/cli@19
```

If local CLI is unreliable, use:

```bash
npx @angular/cli@19 update @angular/core@19 @angular/cli@19
```

### Angular Material

If the project uses Angular Material, update to v19 after Angular core and CLI succeed.

```bash
ng update @angular/material@19
```

or:

```bash
npx @angular/cli@19 update @angular/material@19
```

## Required Code Changes

### 1. Standalone by default

Angular 19 makes directives, components, and pipes standalone by default.

Existing NgModule-declared declarations must explicitly use `standalone: false`.

### 2. Remove `this.` from template reference variable access

Review templates that access template refs through `this.`.

### 3. Replace `BrowserModule.withServerTransition`

Use `APP_ID` instead.

### 4. Remove `KeyValueDiffers.factories`

Remove all uses of `KeyValueDiffers.factories`.

### 5. Localize builder `name` to `project`

Update the `@angular/localize` builder config.

### 6. Rename `ExperimentalPendingTasks` to `PendingTasks`

Replace the old token with `PendingTasks`.

### 7. Effects timing changes

Review effects timing and DOM-dependent effect behavior.

### 8. `fakeAsync` pending timers flush by default

Review timer-dependent tests and use `{ flush: false }` only when justified.

### 9. Hybrid scheduler timing

Review `NgZone` and `fakeAsync` timing assumptions.

### 10. `createComponent` and fallback `ng-content`

Pass projectable empty nodes where needed to avoid unintended fallback content.

### 11. Custom elements change detection timing

Review custom element timing-sensitive tests.

### 12. `Router.errorHandler`

Migrate to supported router error handling APIs.

### 13. `ApplicationRef.tick` errors in tests

Update tests that surface errors during `ApplicationRef.tick`.

### 14. `Resolve` includes `RedirectCommand`

Update resolver typing where needed.

## Do

- Run the Angular 18 changelog review before changing package versions.
- Keep standalone, tests, router, and dynamic component behavior explicit.
- Validate production and SSR builds when they are used.
- Route risky test, router, and component behavior to the dedicated skills.
- Keep Material/MDC validation explicit if Material is used.

## Do Not

- Do not continue if Angular 18 changelog review failed.
- Do not migrate all NgModules to standalone during this hop.
- Do not keep `BrowserModule.withServerTransition()`.
- Do not keep `KeyValueDiffers.factories`.
- Do not keep `Router.errorHandler`.
- Do not mix control flow, defer, zoneless, or signals modernization into the hop.

## Review Checklist

- [ ] Angular 18 changelog review passed.
- [ ] TypeScript 5.5+ is compatible.
- [ ] Standalone declarations are explicit where needed.
- [ ] Template reference variables do not use `this.`.
- [ ] `APP_ID` replaces server transition usage.
- [ ] `KeyValueDiffers.factories` is removed.
- [ ] Localize builder uses `project`.
- [ ] `PendingTasks` replaces `ExperimentalPendingTasks`.
- [ ] Effects and fakeAsync timing are reviewed.
- [ ] Dynamic component projection is reviewed.
- [ ] Router error handling is migrated.
- [ ] `Resolve` typing includes `RedirectCommand`.
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

- Angular 18 changelog risk review failed
- TypeScript version is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- NgModule declarations are missing explicit `standalone: false`
- standalone migration breaks declarations or imports
- template reference variables still use `this.`
- `BrowserModule.withServerTransition()` remains
- `KeyValueDiffers.factories` remains
- `@angular/localize` builder still uses `name`
- `ExperimentalPendingTasks` remains
- effect timing tests fail
- fakeAsync timing failures are unresolved
- hybrid scheduler timing tests are unresolved
- dynamic components render unintended fallback content
- custom elements timing tests fail
- `Router.errorHandler` remains
- `ApplicationRef.tick` test errors are unresolved
- `Resolve` typing does not account for `RedirectCommand`
- Material/style regressions are unreviewed
- SSR behavior is unvalidated in SSR apps
- workspace config is unstable

## Expected Output

1. Upgrade summary.
2. Changelog baseline summary.
3. Standalone, testing, router, and component migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 18 changelog review has passed.
- Angular dependencies are upgraded to Angular 19-compatible versions.
- Angular CLI is upgraded to v19.
- Angular Material/CDK are upgraded to v19 only if used.
- TypeScript 5.5+ compatibility is confirmed.
- Standalone defaults are validated.
- Testing and scheduler behavior is reviewed.
- Router error handling is reviewed.
- Dynamic component projection is reviewed.
- Localize builder is updated when used.
- Angular Material and style regressions are reviewed.
- Validation gate result is explicit.
- The next hop is not started automatically.
