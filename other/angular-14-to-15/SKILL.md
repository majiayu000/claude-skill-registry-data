---
id: angular.upgrade.hops.angular-14-to-15
name: Angular 14 to Angular 15 Upgrade
description: >
  Performs the Angular 14.x to Angular 15.x major-hop upgrade in a bounded, compatibility-aware slice with Material, router, forms, security, styles, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 14 to 15
  - major hop upgrade
  - validation gate
  - Material MDC
compatibility:
  angular:
    sourceMin: "14"
    sourceMax: "14.x"
    target: "15"
---

# Angular 14 to Angular 15 Upgrade

## Purpose

Use this skill to upgrade an Angular 14.x application to Angular 15.x in one bounded major hop.

This hop is a compatibility boundary where Material, router, forms, signals, security, tests, and library packaging changes may surface. It upgrades only from Angular 14 to Angular 15 and must not continue to Angular 16 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 14.x.
- The target hop is Angular 15.x.
- The route planner selected `14 -> 15` as the next step.
- The Angular 13 -> 14 validation gate passed.
- Angular Material usage is known.
- Angular Forms usage is known.
- Router usage is known.
- Test strategy is known.
- The workspace uses `angular.json`.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 13.x or lower.
- The project is already Angular 15 or later.
- The previous Angular 13 -> 14 validation gate failed.
- Angular Material version is unknown in a Material project.
- Angular Forms usage is unknown in a form-heavy application.
- Router behavior is unknown in a routing-heavy application.
- The task is only a Typed Forms migration without Angular version upgrade.
- The task is only Angular Material migration without Angular core upgrade.
- The requested change is Angular 15 to Angular 16.

For Angular 15 to Angular 16, route to:

```txt
skills/angular/upgrades/hops/angular-15-to-16/SKILL.md
```

## Recommended Cross-Skill Routing

If the project has many Angular Reactive Forms, route detailed form migration to:

```txt
skills/angular/upgrades/forms/angular-typed-forms-migration/SKILL.md
```

Use this hop skill to decide the safe strategy:

- migrate forms to typed forms now
- use untyped bridge temporarily
- mix typed migration only for small isolated forms

Default enterprise stance:

Do not migrate all forms to typed forms in the same commit as the Angular 15 upgrade unless the app is small and well tested.

If Material, security, router, DI, or styles show specific risks, route those detections to the matching satellite skill.

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
- `angular.json`
- Angular Forms usage
- Angular Material Stepper/Chips/SelectionList usage
- Material harness usage
- JSONP usage
- router resolvers
- lazy-loaded routes
- custom `LocationStrategy`
- custom `AnimationDriver`
- custom `RouterOutlet`
- iframe bindings
- ControlValueAccessor implementations
- Angular decorator inheritance / DI usage
- `@keyframes` usage in component styles
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 14.x source | Upgrade to Angular 15.x only | Do not jump to a later major in this skill. |
| Angular CLI | Upgrade to CLI 15 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 15-compatible TypeScript | Verify against project evidence. |
| Angular Material | Upgrade to Material 15 only if used | Do not go beyond Angular 15 in this hop. |
| Forms | Choose typed or untyped bridge explicitly | Do not migrate all forms mechanically. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Review the Typed Forms strategy before changing code.
4. Detect and route satellite risks for Material, security, DI, router, styles, and deprecations.
5. Scan the codebase for Angular 14-era deprecated or risky APIs.
6. Classify each occurrence by impact and required change.
7. Apply the bounded dependency upgrade to Angular 15.
8. Convert only the code required by the hop.
9. Run validation commands that exist in the repository.
10. Set the gate result explicitly.
11. Stop after Angular 15. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 14 -> Angular 15.
- Review forms strategy, Material/CDK, router, testing, security, and library packaging behavior.
- Use the forms migration skill for detailed form conversion when the diff is large.
- Use satellite skills for specific detections instead of bloating this hop.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 15-compatible versions using the project-supported package manager and CLI workflow.

Keep typed forms strategy explicit:

- small, isolated forms -> typed forms
- large legacy forms -> untyped bridge
- mixed migration -> only when isolated and documented

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 14 directly to Angular 21.
- Starting Angular 16 migration in the same change.
- Migrating all forms to typed forms in one huge diff.
- Updating Angular Material beyond v15.
- Updating TypeScript beyond Angular 15 compatibility.
- Removing form validation behavior while typing forms.
- Keeping critical forms untested.
- Passing JSONP headers by moving secrets to query params.
- Keeping Protractor-only CDK testing APIs.
- Depending on private Material/CDK APIs.
- Ignoring Material list CSS changes.
- Ignoring router timing test failures.
- Casting all routes with `as any`.
- Ignoring invalid lazy route config errors.
- Rewriting router architecture during this hop.
- Removing AngularJS from hybrid apps during this hop.
- Claiming success without build/test validation.

## Do Not

- Do not continue to Angular 16 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 14.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 15.x.
- [ ] Typed forms strategy was selected.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] Angular library compatibility was checked.
- [ ] Satellite risks were routed where needed.
- [ ] Deprecated APIs were classified and handled.
- [ ] Material and style regressions were reviewed.
- [ ] Router and test behavior were reviewed.
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

- build fails
- tests fail
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript errors remain unresolved
- forms strategy is unknown in a forms-heavy app
- custom FormGroup/FormArray subclasses are incompatible
- JSONP uses headers and replacement strategy is unknown
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

- Typed forms can become a large migration if not separated.
- Material/CDK changes can surface visual or harness regressions.
- Router and testing changes can create subtle behavior shifts.
- JSONP, resolver, and lazy-load changes can break edge cases.
- Production build changes can expose CSS or optimization issues.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Typed forms strategy.
4. Angular CLI and workspace status.
5. Applied dependency and code changes.
6. Validation commands and results.
7. Gate result.
8. Remaining risks.
9. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are upgraded to Angular 15-compatible versions.
- Angular CLI is upgraded to v15.
- Angular Material/CDK are upgraded to v15 only if used.
- TypeScript is aligned to Angular 15-compatible version.
- Forms strategy is explicit.
- Material stepper/chips/selection-list changes are handled or documented.
- JSONP requests do not send headers.
- Router and testing changes are handled.
- Angular Material and style regressions are reviewed.
- Production build has been validated.
- Validation gate result is explicit.
- the next hop is not started automatically.

