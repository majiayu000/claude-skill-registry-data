---
id: angular.upgrade.hops.angular-10-to-11
name: Angular 10 to Angular 11 Upgrade
description: >
  Performs the Angular 10.x to Angular 11.x major-hop upgrade in a bounded, compatibility-aware slice with router, forms, TypeScript, Material, Universal, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 10 to 11
  - major hop upgrade
  - router behavior
  - validation gate
compatibility:
  angular:
    sourceMin: "10"
    sourceMax: "10.x"
    target: "11"
---

# Angular 10 to Angular 11 Upgrade

## Purpose

Use this skill to upgrade an Angular 10.x application to Angular 11.x in one bounded major hop.

This hop belongs to the Angular 6+ strict upgrade zone. It upgrades only from Angular 10 to Angular 11 and must not continue to Angular 12 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 10.x.
- The target hop is Angular 11.x.
- The route planner selected `10 -> 11` as the next step.
- The Angular 9 -> 10 validation gate passed.
- Ivy status is explicit.
- Angular Material usage is known.
- Angular Router usage is known.
- Angular Forms usage is known.
- Angular Universal usage is known.
- TypeScript status is known.
- The workspace uses `angular.json`.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 9.x or lower.
- The project is already Angular 11 or later.
- The previous Angular 9 -> 10 validation gate failed.
- Ivy compatibility is unknown.
- Angular Material version is unknown in a Material project.
- Router configuration status is unknown.
- TypeScript migration status is unknown.
- The task is only Angular Material migration without Angular core upgrade.
- The task is only Router cleanup without Angular version upgrade.
- The requested change is Angular 11 to Angular 12.

For Angular 11 to Angular 12, route to:

```txt
skills/angular/upgrades/hops/angular-11-to-12/SKILL.md
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
- TSLint version if still used
- tslib version
- RxJS version
- Zone.js version
- Node.js version
- `angular.json`
- `.browserslistrc`
- `browserslist`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- Router configuration
- `RouterModule.forRoot(...)`
- `initialNavigation`
- `relativeLinkResolution`
- `preserveQueryParams`
- `queryParamsHandling`
- custom `RouteReuseStrategy`
- custom `UrlMatcher`
- `NavigationExtras`
- `routerLink` usages
- Angular Forms usage
- async validators
- `AbstractControl.parent` checks
- validators and async validators constructor usage
- Angular i18n usage
- ICU expressions
- `ViewEncapsulation.Native`
- `@angular/platform-webworker`
- `@angular/platform-webworker-dynamic`
- `CollectionChangeRecord`
- `IterableChangeRecord`
- locale data mutation
- pipes:
  - `slice`
  - `keyvalue`
  - `decimal`
  - `percent`
  - `currency`
  - `date`
  - `async`
  - `uppercase`
  - `lowercase`
- `TestBed.overrideProvider`
- Angular Universal `useAbsoluteUrl`
- Angular Universal `baseUrl`
- webpack version or custom webpack config
- support requirements for IE9, IE10, IE mobile
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 10.x source | Upgrade to Angular 11.x only | Do not jump to a later major in this skill. |
| Angular CLI | Upgrade to CLI 11 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 11-compatible TypeScript 4.0 | Verify against project evidence. |
| Angular Material | Upgrade to Material 11 only if used | Do not go beyond Angular 11 in this hop. |
| Router / Forms | Review stricter router and forms behavior | Do not assume old behavior survives unchanged. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Update Angular 10 to the latest patch before the Angular 11 upgrade if needed.
4. Scan the codebase for Angular 10-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 11.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 11. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 10 -> Angular 11.
- Review router behavior, forms typings, `TestBed.overrideProvider`, Material 11, Universal, platform-webworker removal, `ViewEncapsulation.Native`, `CollectionChangeRecord`, pipes, and style regressions.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 11-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 11 and Angular core 11.

Make router and forms behavior explicit:

```ts
RouterModule.forRoot(routes, {
  relativeLinkResolution: 'corrected',
  initialNavigation: 'enabledBlocking'
})
```

Use `TestBed.inject` in touched tests:

```ts
const service = TestBed.inject(MyService);
```

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 10 directly to Angular 21.
- Starting Angular 12 migration in the same change.
- Updating Angular Material beyond v11.
- Updating TypeScript beyond Angular 11 compatibility.
- Enabling webpack 5 casually during this hop.
- Enabling strict mode globally without a dedicated migration plan.
- Setting `relativeLinkResolution: 'legacy'` everywhere without analysis.
- Ignoring Router behavior in empty-path child routes.
- Replacing `ViewEncapsulation.Native` without style validation.
- Suppressing ICU template errors.
- Widening Forms types to `any`.
- Ignoring `AbstractControl.parent` nullability.
- Keeping platform-webworker dependencies.
- Mutating locale data arrays directly.
- Suppressing all `console.error` in tests.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components or signals.
- Claiming success without build/test validation.
- Passing the gate when Router, Forms, Universal, Material, or style status is unknown.

## Do Not

- Do not continue to Angular 12 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 10.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 11.x.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] Angular library compatibility was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Material and style regressions were reviewed.
- [ ] Router behavior and Forms typings were reviewed.
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

For Angular CLI projects, use direct CLI commands only if they exist in the project.

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

- build fails
- tests fail
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript 4.0 errors remain unresolved
- Router `relativeLinkResolution` behavior is unknown in apps with nested/empty-path routing
- deprecated `initialNavigation` values remain
- `preserveQueryParams` remains
- `ViewEncapsulation.Native` remains
- platform-webworker packages remain
- Universal `baseUrl` is missing when required
- i18n ICU expression errors remain unresolved
- forms nullability or validator typing issues remain unresolved
- async validator `statusChanges` behavior is unreviewed in critical forms
- custom `RouteReuseStrategy` behavior is unknown
- pipe behavior changes are unreviewed in critical screens
- `TestBed.overrideProvider` timing failures remain unresolved
- unsupported IE browser requirements remain unresolved
- Material/style regressions are unreviewed
- workspace config is unstable

## Risks

- Router and forms changes can create subtle navigation or validation bugs.
- Material and style changes can surface visual regressions.
- Universal and browser support policy changes can break SSR or legacy browser assumptions.
- `TestBed.overrideProvider` timing changes can break touched tests.

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

- Angular packages are upgraded to Angular 11-compatible versions.
- Angular CLI is upgraded to v11.
- Angular Material/CDK are upgraded to v11 only if used.
- TypeScript is aligned to Angular 11-compatible TypeScript 4.0.
- Router `relativeLinkResolution` behavior is reviewed.
- Deprecated `initialNavigation` values are removed.
- `ViewEncapsulation.Native` is replaced with `ViewEncapsulation.ShadowDom`.
- Angular i18n ICU expressions compile.
- Angular Forms validator typings are reviewed.
- `AbstractControl.parent` nullability is handled.
- Removed platform-webworker packages are not used.
- `TestBed.overrideProvider` timing issues are fixed.
- Locale data arrays are not mutated directly.
- `CollectionChangeRecord` is replaced with `IterableChangeRecord`.
- Validation ran or blockers were reported.
- Validation gate result is explicit.
- The next hop remains unexecuted.

