---
id: angular.upgrade.hops.angular-11-to-12
name: Angular 11 to Angular 12 Upgrade
description: >
  Performs the Angular 11.x to Angular 12.x major-hop upgrade in a bounded, high-control slice with Node, TypeScript, router, forms, i18n, Universal, service worker, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 11 to 12
  - major hop upgrade
  - validation gate
  - production build
compatibility:
  angular:
    sourceMin: "11"
    sourceMax: "11.x"
    target: "12"
---

# Angular 11 to Angular 12 Upgrade

## Purpose

Use this skill to upgrade an Angular 11.x application to Angular 12.x in one bounded major hop.

This hop is a high-control upgrade boundary. It upgrades only from Angular 11 to Angular 12 and must not continue to Angular 13 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 11.x.
- The target hop is Angular 12.x.
- The route planner selected `11 -> 12` as the next step.
- The Angular 10 -> 11 validation gate passed.
- Angular CLI, Angular core, Angular Material, Router, Forms, i18n, and Node.js status are known.
- The workspace uses `angular.json`.
- The project is ready for TypeScript 4.2 compatibility review.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 10.x or lower.
- The project is already Angular 12 or later.
- The previous Angular 10 -> 11 validation gate failed.
- Node.js version is unknown.
- Angular Material version is unknown in a Material project.
- Angular i18n usage is unknown.
- Angular Forms usage is unknown in a form-heavy application.
- Router status is unknown in a routing-heavy application.
- The task is only Angular Material migration without Angular core upgrade.
- The task is only production build optimization without Angular upgrade.
- The requested change is Angular 12 to Angular 13.

For Angular 12 to Angular 13, route to:

```txt
skills/angular/upgrades/hops/angular-12-to-13/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- Angular Universal packages
- TypeScript version
- RxJS version
- `zone.js` version
- Node.js version
- package manager version
- `angular.json`
- `.browserslistrc`
- `browserslist`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `polyfills.ts`
- `ngsw-config.json`
- Angular i18n usage
- legacy i18n message IDs
- `$localize` usage
- `@angular/localize` usage
- `XhrFactory` imports
- `ContentChildren` queries
- `ViewChildren` queries
- `emitDistinctChangesOnly`
- Angular Forms usage
- `<input type="number">`
- `min` / `max` attributes
- custom classes extending `FormArray`, `FormGroup`, `FormControl`
- custom validators
- async validators
- classes extending `HttpParams`
- `routerLinkActiveOptions`
- router fragments
- custom router code accessing `fragment`
- `APP_INITIALIZER`
- `Injector.get(APP_INITIALIZER)`
- `TestBed.inject(APP_INITIALIZER)`
- `ng.getDirectives`
- build optimization config: `optimization`, `optimization.styles`, `optimization.styles.inlineCritical`
- production build configuration
- Angular Universal SSR/prerender commands
- Angular Service Worker usage
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 11.x source | Upgrade to Angular 12.x only | Do not jump to a later major in this skill. |
| Angular CLI | Upgrade to CLI 12 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 12-compatible TypeScript 4.2 | Verify against project evidence. |
| zone.js | Align to 0.11.4-compatible version | Verify against project evidence. |
| Angular Material | Upgrade to Material 12 only if used | Do not go beyond Angular 12 in this hop. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Update Angular 11 to the latest patch before the Angular 12 upgrade if needed.
4. Scan the codebase for Angular 11-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 12.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 12. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 11 -> Angular 12.
- Review Node, TypeScript, zone.js, IE11 policy, router, forms, i18n, service worker, Universal, and production build behavior.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Cross-Skill Routing

If IE11 appears in browser policy, polyfills, or product requirements, run:

```txt
skills/angular/upgrades/browser-support/angular-ie11-deprecation-removal-governance/SKILL.md
```

Angular 12 deprecates IE11 support. Do not continue to Angular 13 until the IE11 gate is explicit.

## Recommended Patterns

Upgrade Angular packages to Angular 12-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 12 and Angular core 12.

Use `TestBed.inject` in touched tests:

```ts
const service = TestBed.inject(MyService);
```

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 11 directly to Angular 21.
- Starting Angular 13 migration in the same change.
- Updating Angular Material beyond v12.
- Updating TypeScript beyond Angular 12 compatibility.
- Ignoring Node.js 10 removal.
- Treating IE11 deprecation as irrelevant without checking business requirements.
- Disabling `inlineCritical` without documented blocker.
- Adding `emitDistinctChangesOnly: false` everywhere.
- Removing `min` / `max` from number inputs to avoid validation.
- Widening `APP_INITIALIZER`, `HttpParams`, or router types to `any`.
- Hardcoding SSR/base URLs.
- Changing Service Worker caching without review.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components.
- Introducing signals.
- Claiming success without build/test/production validation.
- Passing the gate when Node, Forms, i18n, Router, Universal, Service Worker, Material, or production build status is unknown.

## Do Not

- Do not continue to Angular 13 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 11.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 12.x.
- [ ] Node.js compatibility was checked.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] Angular library compatibility was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Material and style regressions were reviewed.
- [ ] Router, Forms, i18n, and production build behavior were reviewed.
- [ ] Validation commands were run or explicitly unavailable.
- [ ] Validation gate result was explicit.
- [ ] The next hop was not started automatically.

## Validation Minimum

Read `package.json` first. Only run scripts that exist.

Preferred order when available:

- build
- test
- lint
- e2e

For production build validation:

- build --configuration production

For Angular Universal projects, run server-side build commands if present.

For screenshot/golden tests, run them only if scripts exist.

If validation fails, report:

- command
- error summary
- likely cause
- safe next action
- whether the next hop is blocked

## Validation Gate

This hop must close with an explicit gate decision.

Gate result must be one of:

```txt
PASS
PASS_WITH_WARNINGS
FAIL_BLOCK_NEXT_HOP
```

Use `FAIL_BLOCK_NEXT_HOP` when:

- Node.js is version 10 or older
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript 4.2 errors remain unresolved
- zone.js is not aligned to 0.11.4-compatible version
- IE11 hard requirement remains unresolved
- Angular i18n legacy message ID migration is required but unplanned
- i18n extraction or localized builds fail
- critical `ContentChildren` / `ViewChildren` behavior is unknown
- critical forms using number `min` / `max` are unreviewed
- custom `FormArray` / `FormGroup` subclasses fail or are unreviewed
- `HttpParams` subclass signatures are incompatible
- `APP_INITIALIZER` return types are invalid
- router fragment nullability errors remain unresolved
- `optimization.styles.inlineCritical` breaks production output
- Angular Universal build fails
- Service Worker production behavior is unknown in a PWA
- Material/style regressions are unreviewed
- workspace config is unstable

Use `PASS_WITH_WARNINGS` when:

- IE11 support is deprecated but not yet removed
- legacy i18n message IDs exist but migration is planned
- `emitDistinctChangesOnly: false` was used as temporary compatibility bridge
- `inlineCritical` was disabled with documented reason
- non-critical style differences are documented
- Service Worker review is pending but app is not PWA-critical

## Risks

- Node/runtime or TypeScript incompatibility can block the build.
- Router and forms changes can create subtle navigation or validation bugs.
- Material and style changes can surface visual regressions.
- Universal and Service Worker changes can break SSR or caching assumptions.
- Production build changes can expose CSP or critical CSS issues.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Angular CLI and workspace status.
4. Applied dependency and code changes.
5. Validation commands and results.
6. Gate result.
7. Remaining risks.
8. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are upgraded to Angular 12-compatible versions.
- Angular CLI is upgraded to v12.
- Angular Material/CDK are upgraded to v12 only if used.
- TypeScript is aligned to Angular 12-compatible TypeScript 4.2.
- zone.js is aligned to 0.11.4-compatible version.
- Node.js 10 or older is not used.
- IE11 support requirement is reviewed and documented.
- `XhrFactory` is imported from `@angular/common`.
- Angular i18n/localize status is explicit.
- legacy i18n message IDs are migrated or documented with plan.
- `emitDistinctChangesOnly` behavior is reviewed for `ContentChildren` and `ViewChildren`.
- optional production-by-default migration is either executed separately or intentionally postponed.
- number input `min` / `max` validation behavior is reviewed.
- custom `FormArray` / `FormGroup` subclasses are reviewed.
- `HttpParams` subclasses are compatible.
- `routerLinkActiveOptions` typing is handled.
- `APP_INITIALIZER` return types are valid.
- router fragment nullability is handled.
- `ng.getDirectives` behavior is not incorrectly relied on.
- `optimization.styles.inlineCritical` behavior is reviewed.
- Angular Universal builds pass when used.
- Service Worker behavior is reviewed when used.
- Angular Material and style regressions are reviewed.
- production build has been validated.
- validation gate result is explicit.
- the next hop remains unexecuted.
