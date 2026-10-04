---
id: angular.upgrade.hops.angular-12-to-13
name: Angular 12 to Angular 13 Upgrade
description: >
  Performs the Angular 12.x to Angular 13.x major-hop upgrade in a bounded, hard-boundary slice with IE11, Ivy, View Engine, libraries, Material, router, Universal, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 12 to 13
  - major hop upgrade
  - IE11 removal
  - View Engine removal
compatibility:
  angular:
    sourceMin: "12"
    sourceMax: "12.x"
    target: "13"
---

# Angular 12 to Angular 13 Upgrade

## Purpose

Use this skill to upgrade an Angular 12.x application to Angular 13.x in one bounded major hop.

This hop is a hard compatibility boundary because Angular 13 removes IE11 support and makes Ivy the only rendering engine. It upgrades only from Angular 12 to Angular 13 and must not continue to Angular 14 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 12.x.
- The target hop is Angular 13.x.
- The route planner selected `12 -> 13` as the next step.
- The Angular 11 -> 12 validation gate passed.
- IE11 status is explicit.
- Ivy status is explicit.
- Angular Material usage is known.
- Angular library compatibility is known.
- Service Worker usage is known.
- Universal usage is known.
- Router usage is known.
- The workspace uses `angular.json`.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 11.x or lower.
- The project is already Angular 13 or later.
- The previous Angular 11 -> 12 validation gate failed.
- IE11 is still a hard requirement.
- IE11 browser support policy is unknown.
- Ivy is disabled without a documented blocker.
- View Engine-only libraries are present and compatibility is unknown.
- Angular Material version is unknown in a Material project.
- The requested change is Angular 13 to Angular 14.

For Angular 13 to Angular 14, route to:

```txt
skills/angular/upgrades/hops/angular-13-to-14/SKILL.md
```

## Mandatory Cross-Skill Routing

Before upgrading to Angular 13, run:

```txt
skills/angular/upgrades/browser-support/angular-ie11-deprecation-removal-governance/SKILL.md
```

If IE11 is a hard requirement, return:

```txt
FAIL_BLOCK_NEXT_HOP
```

Do not continue to Angular 13.

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- Angular Universal packages
- Angular Service Worker usage
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
- `enableIvy`
- Angular libraries
- View Engine libraries
- ngcc usage
- Angular Package Format assumptions
- IE11 entries
- IE-specific polyfills
- IE-specific CSS hacks
- lazy route syntax
- `routerLink` usage
- `routerLink` with nullable values
- `SwUpdate.activated`
- `SwUpdate.available`
- `SwUpdate.versionUpdates`
- `renderModuleFactory`
- `renderModule`
- `AbstractControl.status`
- `statusChanges`
- custom form status typing
- custom URL serializer usage
- tests using `DebugElement.properties['href']`
- tests using `SpyLocation`
- tests asserting `urlChanges`
- usage of `SpyNgModuleFactoryLoader`
- usage of `DeprecatedLoadChildren`
- hybrid AngularJS/Angular routing
- Angular Material styles
- screenshot/golden tests
- current build/test/lint/e2e scripts

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 12.x source | Upgrade to Angular 13.x only | Do not jump to a later major in this skill. |
| IE11 | Must be removed or explicitly blocked | Angular 13 does not support IE11. |
| Ivy | Keep Ivy enabled | Angular 13 is Ivy-only. |
| Angular CLI | Upgrade to CLI 13 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 13-compatible TypeScript 4.4 | Verify against project evidence. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Run the IE11 governance skill and record the decision.
3. Check Node.js, CLI, workspace, and validation-gate status.
4. Scan the codebase for Angular 12-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 13.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 13. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 12 -> Angular 13.
- Treat IE11 removal and Ivy-only status as hard boundary conditions.
- Review libraries, APF assumptions, lazy routes, router nullability, Service Worker, Universal, Material, and router/testing compatibility.
- Use the IE11 governance skill as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 13-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 13 and Angular core 13.

Treat the IE11 governance decision as a blocker, not a suggestion.

## Anti-Patterns

- Jumping from Angular 12 directly to Angular 21.
- Starting Angular 14 migration in the same change.
- Continuing to Angular 13 with IE11 as a hard requirement.
- Updating Angular Material beyond v13.
- Disabling Ivy.
- Treating View Engine fallback as valid in Angular 13.
- Ignoring third-party Angular library compatibility.
- Leaving string lazy routes because â€œng update will probably handle it laterâ€.
- Rewriting router architecture during this hop.
- Changing PWA update behavior without smoke tests.
- Rewriting SSR architecture instead of migrating `renderModuleFactory`.
- Widening Forms status typing to `any`.
- Ignoring test failures caused by `SpyLocation` or `href` changes.
- Ignoring hybrid router cancellation behavior.
- Removing AngularJS from hybrid apps during this hop.
- Claiming success without build/test/production validation.
- Passing the gate when IE11, Ivy, libraries, Service Worker, Universal, or router status is unknown.

## Do Not

- Do not continue to Angular 14 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 12.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 13.x.
- [ ] IE11 governance skill was run.
- [ ] IE11 is not a hard requirement or the hop is blocked.
- [ ] Ivy status was checked.
- [ ] CLI workspace status was checked.
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

For production build validation:

- `ng build --configuration production`

For Angular Universal projects, run server-side commands if present.

For Service Worker / PWA projects, validate production build and update flow.

For Material/style-sensitive projects, run available visual checks.

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

- IE11 is a hard requirement
- build fails
- tests fail
- production build fails
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- TypeScript 4.4 errors remain unresolved
- Ivy is disabled
- View Engine-only critical libraries remain
- Angular library compatibility is unknown
- string-based lazy routes remain
- Service Worker update flow is broken
- Universal SSR build fails
- `renderModuleFactory` remains in active SSR code
- critical form status typing is broken
- URL serializer behavior breaks critical deep links
- router tests fail due to unresolved `href`/`SpyLocation` changes
- hybrid router navigation cancellation behavior is unknown
- removed router testing exports remain
- Material/style regressions are unreviewed
- workspace config is unstable

## Risks

- IE11 removal can break contractual browser support.
- Ivy-only can break libraries or build assumptions.
- Router and testing changes can surface subtle behavior changes.
- Universal and Service Worker changes can break SSR or caching assumptions.
- Material and style changes can surface visual regressions.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Browser policy and IE11 decision.
4. Angular CLI and workspace status.
5. Applied dependency and code changes.
6. Validation commands and results.
7. Gate result.
8. Remaining risks.
9. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are upgraded to Angular 13-compatible versions.
- Angular CLI is upgraded to v13.
- Angular Material/CDK are upgraded to v13 only if used.
- TypeScript is aligned to Angular 13-compatible TypeScript 4.4.
- Node.js 12.20.0+ compatibility is confirmed.
- IE11 governance skill has passed.
- IE11 is not a hard requirement.
- Ivy is enabled.
- View Engine-only blockers are resolved or explicitly blocking.
- Angular library compatibility is reviewed.
- String lazy routes are removed.
- Service Worker deprecated APIs are migrated or documented.
- Universal `renderModuleFactory` usage is migrated or documented.
- Angular Material and style regressions are reviewed.
- production build has been validated.
- validation gate result is explicit.
- the next hop is not started automatically.

