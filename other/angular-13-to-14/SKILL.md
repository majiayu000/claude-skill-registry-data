---
id: angular.upgrade.hops.angular-13-to-14
name: Angular 13 to Angular 14 Upgrade
description: >
  Performs the Angular 13.x to Angular 14.x major-hop upgrade in a bounded, high-control slice with Typed Forms strategy, Material/CDK, Router, tests, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 13 to 14
  - major hop upgrade
  - typed forms
  - validation gate
compatibility:
  angular:
    sourceMin: "13"
    sourceMax: "13.x"
    target: "14"
---

# Angular 13 to Angular 14 Upgrade

## Purpose

Use this skill to upgrade an Angular 13.x application to Angular 14.x in one bounded major hop.

This hop is a high-control migration boundary because Angular 14 introduces typed forms and several Angular Material/CDK, Router, JSONP, animation, testing, and lazy-loading behavior changes. It upgrades only from Angular 13 to Angular 14 and must not continue to Angular 15 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 13.x.
- The target hop is Angular 14.x.
- The route planner selected `13 -> 14` as the next step.
- The Angular 12 -> 13 validation gate passed.
- IE11 is not a hard requirement.
- Ivy is enabled.
- Angular Material usage is known.
- Angular Forms usage is known.
- Router usage is known.
- Test strategy is known.
- The workspace uses `angular.json`.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 12.x or lower.
- The project is already Angular 14 or later.
- The previous Angular 12 -> 13 validation gate failed.
- IE11 is still a hard requirement.
- Ivy is disabled.
- Angular Material version is unknown in a Material project.
- Angular Forms usage is unknown in a form-heavy application.
- Router behavior is unknown in a routing-heavy application.
- The task is only Typed Forms migration without Angular version upgrade.
- The task is only Angular Material migration without Angular core upgrade.
- The requested change is Angular 14 to Angular 15.

For Angular 14 to Angular 15, route to:

```txt
skills/angular/upgrades/hops/angular-14-to-15/SKILL.md
```

## Recommended Cross-Skill Routing

Typed Forms can become a large migration by itself.

If the project has many Angular Reactive Forms, route detailed form migration to:

```txt
skills/angular/upgrades/forms/angular-typed-forms-migration/SKILL.md
```

Default enterprise stance:

Do not migrate all forms to typed forms in the same commit as the Angular 14 upgrade unless the app is small and well tested.

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- TypeScript version
- RxJS version
- `zone.js` version
- Node.js version
- package manager version
- `angular.json`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- Angular Forms usage:
  - `FormControl`
  - `FormGroup`
  - `FormArray`
  - `FormBuilder`
  - `AbstractControl`
  - custom validators
  - async validators
  - custom form abstractions
- existing untyped forms usage
- custom classes extending `FormControl`, `FormGroup`, `FormArray`
- TestBed usage
- `aotSummaries`
- Angular Material Stepper usage
- Angular Material Chips usage
- Material mixin abstractions
- Material list usage
- Material SelectionList usage
- Material Harness usage
- JSONP usage
- router resolvers
- lazy-loaded routes
- `initialNavigation`
- `pathMatch`
- custom `LocationStrategy`
- custom `AnimationDriver`
- `RouterOutletContract`
- `Router.initialUrl`
- query params with plus sign
- Protractor/CDK testing usage
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 13.x source | Upgrade to Angular 14.x only | Do not jump to a later major in this skill. |
| Angular CLI | Upgrade to CLI 14 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 14-compatible TypeScript 4.6 | Verify against project evidence. |
| Angular Material | Upgrade to Material 14 only if used | Do not go beyond Angular 14 in this hop. |
| Forms | Choose typed or untyped bridge explicitly | Do not migrate all forms mechanically. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Review the Typed Forms strategy before changing code.
4. Scan the codebase for Angular 13-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 14.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 14. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 13 -> Angular 14.
- Review forms strategy, Material/CDK, router, JSONP, resolvers, harnesses, lazy loading, and test behavior.
- Use the Typed Forms migration skill for detailed form conversion when the diff is large.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 14-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 14 and Angular core 14.

Keep typed forms strategy explicit:

- small, isolated forms -> typed forms
- large legacy forms -> untyped bridge
- mixed migration -> only when isolated and documented

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 13 directly to Angular 21.
- Starting Angular 15 migration in the same change.
- Migrating all forms to typed forms in one huge diff.
- Updating Angular Material beyond v14.
- Updating TypeScript beyond Angular 14 compatibility.
- Removing form validation behavior while typing forms.
- Passing JSONP headers by moving secrets to query params.
- Keeping Protractor-only CDK testing APIs.
- Depending on private Material/CDK APIs.
- Ignoring Material list CSS changes.
- Ignoring router timing test failures.
- Casting all routes with `as any`.
- Ignoring invalid lazy route config errors.
- Rewriting router architecture during this hop.
- Removing AngularJS from hybrid apps during this hop.
- Claiming success without build/test/production validation.
- Passing the gate when Forms, Material/CDK, Router, JSONP, or tests are unknown.

## Do Not

- Do not continue to Angular 15 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 13.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 14.x.
- [ ] Typed Forms strategy was selected.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] Angular library compatibility was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Material and style regressions were reviewed.
- [ ] Router, JSONP, and test behavior were reviewed.
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

- `ng build --configuration production`

For Angular Material projects, run available visual checks.

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

- Node.js is lower than 14.15.0
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript 4.6 errors remain unresolved
- Typed Forms migration breaks critical forms
- form strategy is unknown in a forms-heavy app
- custom FormGroup/FormArray subclasses are incompatible
- JSONP uses headers and replacement strategy is unknown
- critical resolvers have multi-emission behavior unknown
- removed CDK Protractor APIs remain
- Material Stepper/Chips/List/SelectionList changes are unresolved
- custom Material/CDK subclasses are incompatible
- router `initialNavigation` uses removed values
- route `pathMatch` typing remains broken
- custom lazy loader typing is unresolved
- router redirect timing tests remain broken
- custom `LocationStrategy` lacks `getState`
- custom `AnimationDriver` lacks `getParentElement`
- invalid lazy route configs remain
- custom RouterOutlet integrations are unresolved
- `Router.initialUrl` string assignments remain
- Material/style regressions are unreviewed
- workspace config is unstable

Use `PASS_WITH_WARNINGS` when:

- untyped forms bridge is used with documented follow-up
- large typed forms migration is intentionally postponed
- non-critical resolver behavior requires follow-up
- non-critical Material harness changes are pending
- Protractor migration is planned but not blocking the app
- visual differences are documented and accepted

## Risks

- Typed Forms can become a large migration if not separated.
- Material/CDK changes can surface visual or harness regressions.
- Router and testing changes can create subtle behavior shifts.
- JSONP, resolver, and lazy-load changes can break edge cases.
- Production build changes can expose CSS or optimization issues.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Typed Forms strategy.
4. Angular CLI and workspace status.
5. Applied dependency and code changes.
6. Validation commands and results.
7. Gate result.
8. Remaining risks.
9. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are upgraded to Angular 14-compatible versions.
- Angular CLI is upgraded to v14.
- Angular Material/CDK are upgraded to v14 only if used.
- TypeScript is aligned to Angular 14-compatible TypeScript 4.6.
- Node.js 14.15.0+ compatibility is confirmed.
- Typed Forms strategy is explicit.
- Critical forms are tested.
- `aotSummaries` is removed from TestBed.
- Material stepper/chips/selection-list changes are handled or documented.
- JSONP requests do not send headers.
- Resolver first-emission behavior is reviewed.
- Removed CDK Protractor testing entry point is not used.
- `mixinErrorState` abstractions implement `stateChanges`.
- Router, lazy route, and timing changes are handled.
- Angular Material and style regressions are reviewed.
- Production build has been validated.
- validation gate result is explicit.
- the next hop is not started automatically.

