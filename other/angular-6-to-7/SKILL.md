---
id: angular.upgrade.hops.angular-6-to-7
name: Angular 6 to Angular 7.2 Upgrade
description: >
  Performs the Angular 6.x to Angular 7.2.x major-hop upgrade in a bounded, version-aware slice with CLI, RxJS, forms, Material, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 6 to 7
  - Angular 7.2 upgrade
  - major hop upgrade
  - validation gate
compatibility:
  angular:
    sourceMin: "6"
    sourceMax: "6.x"
    target: "7.2"
---

# Angular 6 to Angular 7.2 Upgrade

## Purpose

Use this skill to upgrade an Angular 6.x application to Angular 7.2.x in one bounded major hop.

This skill upgrades only from Angular 6 to Angular 7.2. It must not continue to Angular 8 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 6.x.
- The target hop is Angular 7.2.x.
- The route planner selected `6 -> 7` as the next step.
- The previous Angular 5 -> 6 validation gate passed or the remaining risks were accepted.
- The workspace, RxJS bridge, and gate status are explicit.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 5.x or lower.
- The project is already Angular 7 or later.
- The previous Angular 5 -> 6 gate blocked continuation and has not been resolved.
- The workspace migration to `angular.json` is incomplete or unstable.
- RxJS 6 status is unknown.
- The task is only RxJS cleanup without Angular upgrade.
- The task is only Angular Material migration without Angular core upgrade.
- The requested change is Angular 7 to Angular 8.

For AngularJS, route to:

```txt
skills/angular/migration/angularjs-to-angular-modernization-orchestrator/SKILL.md
```

For Angular 7 to Angular 8, route to:

```txt
skills/angular/upgrades/hops/angular-7-to-8/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- TypeScript version
- RxJS version
- `rxjs-compat` usage
- Zone.js version
- Node.js version
- workspace config: `angular.json` or `.angular-cli.json`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- Angular Material version
- Angular CDK version
- use of Angular Service Worker
- use of screenshot/golden tests
- use of `HttpModule`
- use of `Http`
- use of `HttpClientModule`
- use of `HttpClient`
- use of `Renderer`
- use of mixed `ngModel` with reactive forms
- use of deprecated RxJS 5 imports/operators
- use of `matRippleSpeedFactor`
- use of `baseSpeedFactor`
- current build/test/lint/e2e scripts

## Compatibility by Version

| Area               | Recommended strategy                                              | Observations                                  |
| ------------------ | ----------------------------------------------------------------- | --------------------------------------------- |
| Angular 6.x source | Upgrade to Angular 7.2.x only                                     | Do not jump to a later major in this skill.   |
| Angular CLI        | Upgrade to CLI 7                                                  | Keep workspace validation explicit.           |
| TypeScript         | Align to Angular 7-compatible TypeScript 3.1                      | Verify against project evidence.              |
| RxJS               | Clean up RxJS 5 legacy imports and remove `rxjs-compat` when safe | Treat `rxjs-compat` as temporary if retained. |
| Angular Material   | Upgrade to Material 7 only if used                                | Do not go beyond Angular 7 in this hop.       |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Scan the codebase for Angular 6-era deprecated or risky APIs.
4. Classify each occurrence by impact and required change.
5. Apply the bounded dependency upgrade to Angular 7.2.
6. Convert only the code required by the hop.
7. Run validation commands that exist in the repository.
8. Set the gate result explicitly.
9. Stop after Angular 7.2. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 6 -> Angular 7.2.
- Check CLI workspace migration, RxJS cleanup, `HttpModule`/`Http` to `HttpClient`, `Renderer`, mixed `ngModel` with reactive forms, Material 7, Service Worker config, and screenshot tests.
- Remove `rxjs-compat` only when no legacy imports or third-party requirements remain and validation passes without it.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 7.2-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 7 and Angular core 7.

Remove mixed template-driven/reactive form usage on the same control:

```html
<input formControlName="email" />
```

Clean up RxJS legacy imports:

```ts
import { Observable } from "rxjs";
import { map } from "rxjs/operators";
```

Keep `rxjs-compat` only as a temporary bridge when needed.

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 6 directly to Angular 21.
- Starting Angular 8 migration in the same change.
- Treating `rxjs-compat` as permanent.
- Leaving RxJS 5 imports without documenting the risk.
- Keeping mixed `ngModel` with reactive form directives.
- Rewriting all HTTP services without tests.
- Updating Angular Material beyond v7.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components or signals.
- Claiming success without validation.
- Passing the gate when workspace, RxJS, or Material status is unknown.

## Do Not

- Do not continue to Angular 8 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 6.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 7.2.x.
- [ ] CLI workspace migration status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] RxJS compatibility was checked.
- [ ] `rxjs-compat` status was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Mixed `ngModel` and reactive forms were reviewed.
- [ ] Material and Service Worker changes were reviewed where applicable.
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
- RxJS migration is incomplete and undocumented
- `rxjs-compat` status is unknown
- mixed `ngModel` and reactive forms remain in critical flows
- Angular Material update causes unresolved UI regressions
- Service Worker config migration is incomplete
- workspace config is unstable

## Risks

- RxJS 6 cleanup can introduce import and operator mismatches.
- `HttpClient` migration can alter response handling if done carelessly.
- Hybrid apps can break if `@angular/upgrade/static` is not handled consistently.
- Material or screenshot tests can surface visual regressions.
- Validation gate state can block the next hop if the workspace is unstable.

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

- Angular packages are upgraded to Angular 7.2-compatible versions.
- Angular CLI is upgraded to v7.
- TypeScript is aligned to Angular 7-compatible TypeScript 3.1.
- RxJS 6 cleanup is explicit.
- `rxjs-compat` status is explicit.
- Validation ran or blockers were reported.
- Validation gate result is explicit.
- The next hop remains unexecuted.
