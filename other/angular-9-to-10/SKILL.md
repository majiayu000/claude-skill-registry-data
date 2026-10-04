---
id: angular.upgrade.hops.angular-9-to-10
name: Angular 9 to Angular 10.2 Upgrade
description: >
  Performs the Angular 9.x to Angular 10.2.x major-hop upgrade in a bounded, critical compatibility slice with Ivy, DI, Material, TypeScript, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 9 to 10
  - Angular 10.2 upgrade
  - major hop upgrade
  - validation gate
compatibility:
  angular:
    sourceMin: "9"
    sourceMax: "9.x"
    target: "10.2"
---

# Angular 9 to Angular 10.2 Upgrade

## Purpose

Use this skill to upgrade an Angular 9.x application to Angular 10.2.x in one bounded major hop.

This hop is part of the Angular 6+ strict upgrade zone and follows the Ivy boundary introduced in Angular 9. It upgrades only from Angular 9 to Angular 10.2 and must not continue to Angular 11 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 9.x.
- The target hop is Angular 10.2.x.
- The route planner selected `9 -> 10` as the next step.
- The Angular 8 -> 9 validation gate passed.
- Ivy status is known.
- Angular Material usage is known.
- Angular i18n/localize status is known.
- Angular library compatibility status is known.
- The workspace uses `angular.json`.
- The project is ready for TypeScript 3.9 compatibility review.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 8.x or lower.
- The project is already Angular 10 or later.
- The previous Angular 8 -> 9 validation gate failed.
- Ivy compatibility is unknown.
- Angular library compatibility is unknown.
- Angular Material version is unknown in a Material project.
- Angular i18n usage is unknown.
- The task is only Angular Material migration without Angular core upgrade.
- The task is only TypeScript migration without Angular upgrade.
- The requested change is Angular 10 to Angular 11.

For Angular 10 to Angular 11, route to:

```txt
skills/angular/upgrades/hops/angular-10-to-11/SKILL.md
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
- TSLint version
- tslib version
- RxJS version
- Zone.js version
- Node.js version
- `angular.json`
- `browserslist`
- `.browserslistrc`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `polyfills.ts`
- Ivy config: `enableIvy`
- use of Angular i18n
- use of `@angular/localize`
- use of `entryComponents`
- use of `ANALYZE_FOR_ENTRY_COMPONENTS`
- use of `TestBed.get`
- classes using Angular features without decorators
- incomplete provider definitions
- use of Angular forms
- number input controls
- `minLength` / `maxLength` validators
- route resolvers returning `EMPTY`
- custom `UrlMatcher`
- use of `DatePipe`
- use of `formatDate`
- use of `b` or `B` date format codes
- async pipe bindings
- bindings like `[val]="(observable | async).someProperty"`
- Angular Service Worker usage
- resources with `Vary` headers
- Angular Universal usage
- `useAbsoluteUrl` usage
- custom schematics
- schematic options: `styleext`, `spec`
- direct dependency on Angular package formats: `esm5`, `fesm5`
- tools expecting no `console.error`
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 9.x source | Upgrade to Angular 10.2.x only | Do not jump to a later major in this skill. |
| Ivy | Keep Ivy enabled by default unless a documented blocker exists | View Engine fallback is temporary only. |
| Angular CLI | Upgrade to CLI 10 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 10-compatible TypeScript 3.9 | Verify against project evidence. |
| Angular Material | Upgrade to Material 10 only if used | Do not go beyond Angular 10 in this hop. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Update Angular 9 to the latest patch before the Angular 10 upgrade if needed.
4. Scan the codebase for Angular 9-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 10.2.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 10.2. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 9 -> Angular 10.2.
- Treat Ivy compatibility as already established but still verified.
- Review libraries, Material imports, lazy routes, `entryComponents`, `TestBed.get`, `@angular/localize`, forms behavior, resolvers, Service Worker, Universal, and provider strictness.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 10.2-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 10 and Angular core 10.

Enable Ivy by default unless a documented blocker exists:

```json
{
  "angularCompilerOptions": {
    "enableIvy": true
  }
}
```

Replace `TestBed.get` in touched tests:

```ts
const service = TestBed.inject(MyService);
```

Use explicit generics on `ModuleWithProviders` if touched libraries expose them.

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 9 directly to Angular 21.
- Starting Angular 11 migration in the same change.
- Updating Angular Material beyond v10.
- Updating TypeScript beyond Angular 10 compatibility.
- Migrating TSLint to ESLint inside this hop without a separate plan.
- Disabling Ivy without documented blocker.
- Treating View Engine fallback as final state.
- Adding `@angular/localize` when no Angular i18n exists.
- Removing `entryComponents` blindly from libraries consumed by View Engine apps.
- Decorating every base class blindly.
- Guessing incomplete provider values.
- Rewriting all forms without tests.
- Changing resolver behavior without business validation.
- Hardcoding Universal `baseUrl`.
- Suppressing all `console.error` in tests.
- Forcing `NO_ERRORS_SCHEMA` everywhere.
- Patching custom build pipelines blindly.
- Updating all third-party dependencies blindly.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components or signals.
- Claiming success without build/test validation.
- Passing the gate when Ivy, DI, forms, Universal, Service Worker, Material, or style status is unknown.

## Do Not

- Do not continue to Angular 11 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 9.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 10.2.x.
- [ ] Latest Angular 9 patch update was considered or applied first.
- [ ] Ivy status was checked.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] Angular library compatibility was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Material and style regressions were reviewed.
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

- Node.js is lower than 12
- build fails
- tests fail
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript 3.9 errors remain unresolved
- Ivy compatibility is unknown
- Ivy is disabled without documented blocker
- Angular i18n uses localize but localize is missing
- undecorated Angular feature classes remain unresolved
- incomplete provider definitions remain unresolved
- resolver `EMPTY` behavior is unknown
- Angular Universal `baseUrl` is missing when required
- Service Worker caching risk is unknown
- forms number input behavior is unreviewed in critical flows
- `minLength` / `maxLength` validators are used on non-length values without review
- custom build tooling depends on `esm5` / `fesm5`
- unknown element console errors are unresolved
- async pipe regressions are unreviewed
- Material/style regressions are unreviewed
- workspace config is unstable

## Risks

- Ivy compatibility can break Angular libraries or hybrid setups.
- DI/provider strictness can surface previously hidden errors.
- Resolver, forms, and async pipe changes can create subtle behavior shifts.
- Universal and Service Worker changes can break SSR or caching assumptions.
- Validation gate state can block the next hop if compatibility is uncertain.

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

- Angular packages are upgraded to Angular 10.2-compatible versions.
- Angular CLI is upgraded to v10.
- Angular Material/CDK are upgraded to v10 only if used.
- Node.js 12+ compatibility is confirmed.
- TypeScript is aligned to Angular 10-compatible TypeScript 3.9.
- TSLint v6 is aligned if TSLint is still used.
- tslib v2 is aligned.
- Ivy status is explicit.
- `@angular/localize` is present when Angular i18n is used.
- Application `entryComponents` and `ANALYZE_FOR_ENTRY_COMPONENTS` are removed where safe.
- `TestBed.get` is replaced with `TestBed.inject` in touched tests.
- Classes using Angular features have proper decorators or documented remediation.
- Incomplete provider definitions are fixed or blocked.
- Angular forms number input behavior is reviewed.
- `minLength` and `maxLength` validators on non-length values are reviewed.
- Resolver `EMPTY` behavior is reviewed.
- Angular Service Worker `Vary` header risk is reviewed.
- Async pipe / `WrappedValue` behavior is reviewed.
- DatePipe / `formatDate` day period behavior is reviewed when used.
- Custom `UrlMatcher` nullability is reviewed.
- Angular Universal `useAbsoluteUrl` includes `baseUrl` when required.
- Angular Material and style regressions are reviewed.
- Validation ran or blockers were reported.
- Validation gate result is explicit.
- The next hop remains unexecuted.

