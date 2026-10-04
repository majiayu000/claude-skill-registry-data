---
id: angular.upgrade.hops.angular-19-to-20
name: Angular 19 to Angular 20 Upgrade
description: >
  Upgrade an Angular application from Angular 19.x to Angular 20.x using a controlled major-hop process. Use when the project is ready to move from Angular 19 to Angular 20 and needs explicit handling for TypeScript 5.8+, moduleResolution bundler, testing behavior, DI deprecations, router redirects, Resource API changes, template operator conflicts, ng-reflect cleanup, and SSR/module-resolution risk.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 19 to 20
  - Angular 20 upgrade
  - moduleResolution bundler
  - Resource API migration
compatibility:
  angular:
    min: "19"
---

# Angular 19 to Angular 20 Upgrade

## Purpose

Upgrade an Angular application from Angular 19.x to Angular 20.x using a controlled major-hop process.

## When to Use

- The project uses Angular 19.x.
- The target next hop is Angular 20.x.
- The Angular 18 -> 19 validation gate passed.
- Angular Material usage is known.
- TypeScript configuration is known.
- Node.js runtime is known.
- Router guard/redirect usage is known.
- Resource/RxResource usage is known.
- Test strategy is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 18.x or lower.
- The project is already Angular 20 or later.
- The previous Angular 18 -> 19 validation gate failed.
- Angular Material v19 migration has unresolved critical blockers.
- The project has unknown TypeScript configuration.
- The project uses unsupported Node.js.
- The task is only zoneless migration.
- The task is only Resource API refactor.
- The task is only testing cleanup.

## Mandatory Cross-Skill Routing

Before upgrading from Angular 19 to Angular 20, run:

`skills/angular/upgrades/changelog/angular-major-changelog-risk-review/SKILL.md`

If the changelog review returns `FAIL_BLOCK_NEXT_HOP`, do not continue to Angular 20.

## Recommended Cross-Skill Routing

- `skills/angular/upgrades/testing/angular-v20-testing-errors-effects-animations/SKILL.md`
- `skills/angular/upgrades/di/angular-v20-injector-injectflags-cleanup/SKILL.md`
- `skills/angular/upgrades/router/angular-v20-guards-redirects-route-validation/SKILL.md`
- `skills/angular/upgrades/resources/angular-v20-resource-rxresource-migration/SKILL.md`
- `skills/angular/upgrades/zoneless/angular-v20-zoneless-api-rename/SKILL.md`
- `skills/angular/upgrades/templates/angular-v20-template-operator-compat/SKILL.md`
- `skills/angular/upgrades/build/angular-v20-module-resolution-bundler/SKILL.md`
- `skills/angular/upgrades/debug/angular-v20-ng-reflect-cleanup/SKILL.md`

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
- base tsconfigs
- `moduleResolution`
- custom builders
- custom test builders
- Angular Material usage
- `afterRender`
- `afterEveryRender`
- `TestBed.flushEffects`
- `TestBed.tick`
- `provideExperimentalCheckNoChangesForDebug`
- `provideCheckNoChangesConfig`
- `provideExperimentalZonelessChangeDetection`
- `provideZonelessChangeDetection`
- `ng-reflect-*`
- `provideNgReflectAttributes`
- `RedirectFn`
- route guards and resolvers
- guard arrays
- string guards
- `RedirectCommand`
- `Route.redirectTo`
- `canMatch`
- commands array types
- `resource`
- `rxResource`
- `ResourceStatus`
- template properties named `in`
- template references named `in`
- template properties named `void`
- template references named `void`
- templates with parenthesized optional chaining
- animation tests
- event listener error tests
- `TestBed.get`
- `InjectFlags`
- `Injector.get`
- `EnvironmentInjector.get`
- `TestBed.inject`
- `AsyncPipe` usage in tests
- `PendingTasks.run`
- `PendingTasks.add`
- `DatePipe`
- week-year formatter `Y`
- `redirectTo` + `canMatch` route configs
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden tests

## Dependency Upgrade

### Node.js

Use the Angular version compatibility matrix as the source of truth.

### TypeScript

Angular 20 requires TypeScript 5.8 or later.

### Angular Core and CLI

Run:

```bash
ng update @angular/core@20 @angular/cli@20
```

If local CLI is unreliable, use:

```bash
npx @angular/cli@20 update @angular/core@20 @angular/cli@20
```

### Angular Material

If the project uses Angular Material, update to v20 after Angular core and CLI succeed.

```bash
ng update @angular/material@20
```

or:

```bash
npx @angular/cli@20 update @angular/material@20
```

## Required Code Changes

### 1. `moduleResolution: "bundler"`

Validate and align tsconfig inheritance to use `moduleResolution: "bundler"`.

### 2. Replace `afterRender` with `afterEveryRender`

Update render callbacks to the new API.

### 3. Replace `TestBed.flushEffects()` with `TestBed.tick()`

Update tests using effect flushing helpers.

### 4. Rename check-no-changes provider

Replace `provideExperimentalCheckNoChangesForDebug` with `provideCheckNoChangesConfig`.

### 5. Remove `ng-reflect-*` dependency

Avoid tests or production logic depending on Angular debug attributes.

### 6. Handle async `RedirectFn` return values

Update direct calls to `RedirectFn` to handle Observable or Promise results.

### 7. Resource API `request` to `params`

Update `resource` usage to the `params` option.

### 8. RxResource `request` / `loader` to `params` / `stream`

Update `rxResource` usage to the new API.

### 9. Replace `ResourceStatus` enum usage

Remove enum-style `ResourceStatus` usage.

### 10. Rename zoneless provider

Replace `provideExperimentalZonelessChangeDetection` with `provideZonelessChangeDetection`.

### 11. Template `in` and `void` conflicts

Rename colliding template properties or references.

### 12. Router commands arrays are readonly

Stop mutating router commands arrays.

### 13. Animation test timing

Review animation-related test timing changes.

### 14. Event listener errors rethrown in tests

Review tests that expect swallowed listener errors.

### 15. Guard arrays no longer accept `any`

Remove `any` from route guard arrays.

### 16. Replace `TestBed.get()` with `TestBed.inject()`

Update all touched tests.

### 17. Remove `InjectFlags`

Replace `InjectFlags` with typed options or explicit handling.

### 18. Use specific `ProviderToken<T>` in `Injector.get`

Avoid untyped or string-token injector usage in critical code.

### 19. AsyncPipe error reporting

Adjust tests and error handling to the new behavior.

### 20. PendingTasks.run return behavior

Stop relying on the return value of `PendingTasks.run`.

### 21. DatePipe week-year formatter

Review suspicious `Y` format usage.

### 22. Template parentheses behavior

Review parenthesized optional chaining and nullish expressions.

### 23. `redirectTo` with `canMatch`

Resolve route configs that combine `redirectTo` and `canMatch`.

## Do

- Run the Angular 19 changelog review before changing package versions.
- Keep module resolution, tests, router, DI, and resource behavior explicit.
- Validate production and SSR builds when they are used.
- Route risky test, build, and router behavior to the dedicated skills.
- Keep Material/MDC validation explicit if Material is used.

## Do Not

- Do not continue if Angular 19 changelog review failed.
- Do not keep `TestBed.get`, `InjectFlags`, or `ng-reflect-*` dependencies.
- Do not rely on `ModuleResolution` inheritance accidentally.
- Do not mix zoneless modernization, control flow, defer, or standalone adoption into the hop.

## Review Checklist

- [ ] Angular 19 changelog review passed.
- [ ] TypeScript 5.8+ is compatible.
- [ ] `moduleResolution` is aligned to `bundler`.
- [ ] Testing helpers are updated.
- [ ] DI deprecations are removed.
- [ ] Router redirects and guards are reviewed.
- [ ] Resource API usage is migrated.
- [ ] Template operator conflicts are resolved.
- [ ] `ng-reflect-*` dependence is removed.
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

- Angular 19 changelog risk review failed
- TypeScript version is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- `moduleResolution: "bundler"` is missing or overridden incorrectly
- `afterRender` remains
- `TestBed.flushEffects()` remains
- deprecated zoneless/check-no-changes providers remain
- production/test code depends on `ng-reflect-*`
- direct `RedirectFn` calls assume sync return
- Resource/RxResource old API remains
- `ResourceStatus` enum usage remains
- template `in` or `void` conflicts remain
- router commands are mutated despite readonly typing
- animation DOM tests are unresolved
- event listener errors are suppressed globally instead of fixed
- route guard arrays use `any`
- string guards remain without migration plan
- `TestBed.get()` remains
- `InjectFlags` remains
- untyped/string-token `Injector.get()` remains in critical code
- AsyncPipe error reporting breaks tests without resolution
- `PendingTasks.run` return value is still relied upon
- suspicious DatePipe `Y` usage remains in critical flows
- parenthesized optional/nullish template expressions can throw
- routes combine `redirectTo` and `canMatch`
- Material/style regressions are unreviewed
- SSR/resource behavior is unvalidated in SSR/resource apps
- workspace config is unstable

## Expected Output

1. Upgrade summary.
2. Changelog baseline summary.
3. Testing, router, DI, and resource migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 19 changelog review has passed.
- Angular dependencies are upgraded to Angular 20-compatible versions.
- Angular CLI is upgraded to v20.
- Angular Material/CDK are upgraded to v20 only if used.
- TypeScript 5.8+ compatibility is confirmed.
- `moduleResolution` is aligned to `bundler`.
- Testing behavior is reviewed.
- DI deprecations are removed.
- Router redirect behavior is reviewed.
- Resource API migration is reviewed.
- `ng-reflect-*` dependency is removed.
- Angular Material and style regressions are reviewed.
- Validation gate result is explicit.
- The next hop is not started automatically.
