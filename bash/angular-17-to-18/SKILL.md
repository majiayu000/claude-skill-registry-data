---
id: angular.upgrade.hops.angular-17-to-18
name: Angular 17 to Angular 18 Upgrade
description: >
  Upgrade an Angular application from Angular 17.x to Angular 18.x using a controlled major-hop process. Use when the project is ready to move from Angular 17 to Angular 18 and needs explicit handling for Node.js/TypeScript requirements, tests, SSR/platform-server, TransferState, HTTP transfer cache, router redirects, forms, OnPush, and change detection behavior.
stack:
  - Angular
  - TypeScript
category: upgrade
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 17 to 18
  - Angular 18 upgrade
  - test stability
  - SSR platform-server
compatibility:
  angular:
    min: "17"
---

# Angular 17 to Angular 18 Upgrade

## Purpose

Upgrade an Angular application from Angular 17.x to Angular 18.x using a controlled major-hop process.

## When to Use

- The project uses Angular 17.x.
- The target next hop is Angular 18.x.
- The Angular 16 -> 17 validation gate passed.
- Angular Material usage is known.
- SSR/platform-server usage is known.
- TransferState usage is known.
- Router guards/resolvers usage is known.
- Forms usage is known.
- Test strategy is known.

## When Not to Use

- The project is AngularJS 1.x.
- The project is Angular 16.x or lower.
- The project is already Angular 18 or later.
- The previous Angular 16 -> 17 validation gate failed.
- Node.js version is unsupported.
- Angular Material v17 migration has unresolved critical blockers.
- SSR behavior is unknown in an SSR app.
- Router redirect behavior is unknown in a routing-heavy app.
- The task is only testing cleanup without Angular upgrade.
- The task is only SSR migration without Angular upgrade.

## Mandatory Cross-Skill Routing

Before upgrading from Angular 17 to Angular 18, run:

`skills/angular/upgrades/changelog/angular-major-changelog-risk-review/SKILL.md`

If the changelog review returns `FAIL_BLOCK_NEXT_HOP`, do not continue to Angular 18.

## Recommended Cross-Skill Routing

- `skills/angular/upgrades/testing/angular-v18-test-stability-change-detection/SKILL.md`
- `skills/angular/upgrades/ssr/angular-platform-server-v18-migration/SKILL.md`
- `skills/angular/upgrades/router/angular-router-redirect-command-v18/SKILL.md`
- `skills/angular/upgrades/http/angular-http-transfer-cache-v18/SKILL.md`
- `skills/angular/upgrades/forms/angular-ngmodel-template-write-cleanup-v18/SKILL.md`
- `skills/angular/upgrades/change-detection/angular-onpush-host-bindings-v18/SKILL.md`

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
- test setup files
- `polyfills.ts`
- SSR files
- TransferState usage
- HTTP transfer cache usage
- Angular Forms usage
- `[(ngModel)]` templates
- router guards
- router resolvers
- `RedirectCommand`
- `UrlTree`
- `Route.redirectTo`
- `platformDynamicServer`
- `platformServer`
- `@angular/compiler`
- `PlatformConfig`
- `useAbsoluteUrl`
- `baseUrl`
- `ServerTransferStateModule`
- `RESOURCE_CACHE_PROVIDER`
- `isPlatformWorkerUi`
- `isPlatformWorkerApp`
- `AnimationDriver`
- `matchesElement`
- `Testability`
- `increasePendingRequestCount`
- `decreasePendingRequestCount`
- `getPendingRequestCount`
- environment providers
- routed components
- `OnPush` components
- host bindings
- dynamic views
- `ComponentFixture.whenStable`
- `ApplicationRef.isStable`
- `ComponentFixture.autoDetectChanges`
- current build/test/lint/e2e scripts
- production build scripts
- SSR/prerender scripts
- screenshot/golden tests

## Dependency Upgrade

### Node.js

Angular 18 supports Node.js 18.19.0 and newer.

Block the upgrade when Node.js is lower than 18.19.0.

### TypeScript

Angular 18 requires TypeScript 5.4 or newer.

### Angular Core and CLI

Run:

```bash
ng update @angular/core@18 @angular/cli@18
```

If local CLI is unreliable, use:

```bash
npx @angular/cli@18 update @angular/core@18 @angular/cli@18
```

### Angular Material

If the project uses Angular Material, update to v18 after Angular core and CLI succeed.

```bash
ng update @angular/material@18
```

or:

```bash
npx @angular/cli@18 update @angular/material@18
```

## Required Code Changes

### 1. Replace `async` from Angular testing with `waitForAsync`

Use `waitForAsync` instead of `async` from `@angular/core/testing`.

### 2. Remove `AnimationDriver.matchesElement`

Remove uses of `matchesElement` from `AnimationDriver`.

### 3. TransferState imports

Import `StateKey` and `TransferState` from `@angular/core`.

### 4. HTTP transfer cache with authorization headers

Only enable `includeRequestsWithAuthHeaders` with a security review.

### 5. Remove WebWorker platform APIs

Remove `isPlatformWorkerUi` and `isPlatformWorkerApp`.

### 6. Test change detection behavior

Review tests that rely on exact change detection order or stabilization timing.

### 7. Remove template write expressions with `[(ngModel)]`

Move writes out of the template and into handlers.

### 8. Remove Testability pending request APIs

Remove `increasePendingRequestCount`, `decreasePendingRequestCount`, and `getPendingRequestCount`.

### 9. Environment providers for routed components

Move providers needed by routed components to route-level or bootstrap-level providers.

### 10. Guard/resolver redirect behavior with `replaceUrl`

Use `RedirectCommand` when redirect history behavior must be explicit.

### 11. Remove `RESOURCE_CACHE_PROVIDER`

Remove dependencies on `RESOURCE_CACHE_PROVIDER`.

### 12. platform-server URL behavior

Review canonical URLs, redirects, and tests that compare exact SSR URLs.

### 13. Absolute URL handling

Replace `useAbsoluteUrl` and `baseUrl` with request/environment-aware absolute URL handling.

### 14. Replace `platformDynamicServer` with `platformServer`

Use `platformServer` and import `@angular/compiler` when JIT/server behavior requires it.

### 15. Remove `ServerTransferStateModule`

Remove `ServerTransferStateModule` usage.

### 16. `Route.redirectTo` can be a function

Update route readers that assume string-only redirects.

### 17. Guards and resolvers can return `RedirectCommand`

Update custom typing where needed.

### 18. OnPush host binding updates

Review `OnPush` components with host bindings and explicit dirty marking.

### 19. Newly created or reattached views refresh behavior

Review dynamic views, overlays, and portal-like behavior.

### 20. `whenStable` and `ApplicationRef.isStable`

Review test timing and stabilization assumptions.

### 21. `ComponentFixture.autoDetectChanges`

Review tests that rely on auto-detection order.

## Do

- Run the Angular 16 changelog review before changing package versions.
- Keep tests, SSR, router, forms, and transfer cache behavior explicit.
- Validate production and SSR builds when they are used.
- Route risky test, SSR, and router behavior to the dedicated skills.
- Keep Material/MDC validation explicit if Material is used.

## Do Not

- Do not continue if Angular 16 changelog review failed.
- Do not keep deprecated testing, transfer state, or webworker APIs.
- Do not enable authenticated transfer cache without security review.
- Do not mix this hop with control flow, defer, standalone, or zoneless modernization.
- Do not rely on leaked styles or unstable test timing.

## Review Checklist

- [ ] Angular 16 changelog review passed.
- [ ] Node.js, TypeScript, and Zone.js are compatible.
- [ ] Testing helper usage is updated.
- [ ] SSR and transfer cache behavior are reviewed.
- [ ] Router redirect history behavior is reviewed.
- [ ] ngModel template writes are removed.
- [ ] Testability APIs are removed.
- [ ] OnPush host binding behavior is reviewed.
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
- Node.js is lower than 18.19.0
- TypeScript version is unsupported
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- `async` from Angular testing remains
- `AnimationDriver.matchesElement` remains
- TransferState imports remain from `@angular/platform-browser`
- authenticated transfer cache is enabled without security review
- WebWorker platform APIs remain
- template write expressions with `[(ngModel)]` remain
- removed Testability APIs remain
- routed components depend on misplaced environment providers
- critical guard redirect history behavior is unknown
- `RESOURCE_CACHE_PROVIDER` remains
- SSR URL behavior is unvalidated
- `platformDynamicServer` remains in active SSR code
- `ServerTransferStateModule` remains
- custom route readers assume `redirectTo` is only string
- custom guard/resolver typing does not allow `RedirectCommand`
- critical OnPush host bindings are stale
- test stability issues remain unresolved
- Material/style regressions are unreviewed
- workspace config is unstable

## Expected Output

1. Upgrade summary.
2. Changelog baseline summary.
3. SSR, router, and testing migration summary.
4. Validation result.
5. Gate decision.

## Exit Criteria

- Angular 16 changelog review has passed.
- Angular dependencies are upgraded to Angular 18-compatible versions.
- Angular CLI is upgraded to v18.
- Angular Material/CDK are upgraded to v18 only if used.
- Node.js 18.19.0+ compatibility is confirmed.
- TypeScript 5.4+ compatibility is confirmed.
- Testing behavior is reviewed.
- SSR/platform-server behavior is reviewed.
- TransferState and transfer cache behavior are reviewed.
- Router redirect behavior is reviewed.
- `ngModel` template writes are removed.
- Testability APIs are removed.
- OnPush host binding behavior is reviewed.
- Angular Material and style regressions are reviewed.
- Validation gate result is explicit.
- The next hop is not started automatically.
