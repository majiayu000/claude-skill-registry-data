---
id: angular.upgrade.hops.angular-5-to-6
name: Angular 5 to Angular 6.1 Upgrade
description: >
  Performs the Angular 5.x to Angular 6.1.x major-hop upgrade in a bounded, version-aware slice with CLI migration, RxJS planning, and validation.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 5 to 6
  - Angular 6.1 upgrade
  - major hop upgrade
  - angular.json migration
compatibility:
  angular:
    sourceMin: "5"
    sourceMax: "5.x"
    target: "6.1"
---

# Angular 5 to Angular 6.1 Upgrade

## Purpose

Use this skill to upgrade an Angular 5.x application to Angular 6.1.x in one bounded major hop.

This skill upgrades only from Angular 5 to Angular 6.1. It must not continue to Angular 7 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 5.x.
- The target hop is Angular 6.1.x.
- The route planner selected `5 -> 6` as the next step.
- The repository has a buildable baseline and dependency files to inspect.
- The upgrade must remain controlled and reversible.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 4.x or lower.
- The project is already Angular 6 or later.
- The requested change is Angular 6 to Angular 7.
- The project cannot produce a baseline build or install dependencies.
- The task is only RxJS modernization without Angular upgrade.
- The task is only `HttpClient` migration without Angular version upgrade.

For AngularJS, route to:

```txt
skills/angular/migration/angularjs-to-angular-modernization-orchestrator/SKILL.md
```

For the next hop, route to:

```txt
skills/angular/upgrades/hops/angular-6-to-7/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- TypeScript version
- RxJS version
- Zone.js version
- Node.js version
- use of `.angular-cli.json`
- use of `angular.json`
- use of `@angular/upgrade`
- use of Angular Material
- use of Angular animations
- use of `HttpModule`
- use of `Http`
- use of `HttpClientModule`
- use of `HttpClient`
- use of `DOCUMENT`
- use of `ReflectiveInjector`
- use of `Renderer`
- use of `preserveQueryParams`
- use of `ngOutletContext`
- use of `CollectionChangeRecord`
- use of custom RxJS operators
- current build/test/lint/e2e scripts

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 5.x source | Upgrade to Angular 6.1.x only | Do not jump to a later major in this skill. |
| Angular CLI | Migrate to CLI 6 and `angular.json` if applicable | Keep workspace conversion bounded. |
| TypeScript | Align to the repo-compatible Angular 6 range | Verify against project evidence before changing. |
| RxJS | Move toward RxJS 6, optionally bridging with `rxjs-compat` | Do not treat `rxjs-compat` as final state. |
| Http | Migrate to `HttpClient` where feasible | Preserve behavior around headers, params, and non-JSON responses. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Detect Node.js and CLI workspace constraints.
3. Scan the codebase for Angular 5-era deprecated or risky APIs.
4. Classify each occurrence by impact and required change.
5. Apply the bounded dependency upgrade to Angular 6.1.
6. Convert only the code required by the hop.
7. Run validation commands that exist in the repository.
8. Stop after Angular 6.1. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 5 -> Angular 6.1.
- Check CLI workspace migration, RxJS compatibility, `HttpModule`/`Http` to `HttpClient`, `DOCUMENT`, `ReflectiveInjector`, `Renderer`, `preserveQueryParams`, `ngOutletContext`, and `CollectionChangeRecord`.
- Migrate `@angular/upgrade` imports to `@angular/upgrade/static` where applicable.
- Keep `@angular/http` only if the repo still depends on it and a dedicated HTTP migration is not in scope.
- Use `rxjs-compat` only as a temporary bridge when the repo is too large for a full manual RxJS migration.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 6.1-compatible versions using the project-supported package manager and CLI workflow.

Migrate Angular CLI workspace config from `.angular-cli.json` to `angular.json` if the CLI update requires it.

Migrate HTTP access to `HttpClient` where feasible:

```ts
import { HttpClient } from '@angular/common/http';

constructor(private http: HttpClient) {}
```

Use `rxjs-compat` only as a temporary bridge when needed:

```bash
npm install rxjs-compat@^6.0.0
```

Preserve hybrid runtime if AngularJS is still part of the app.

## Anti-Patterns

- Jumping from Angular 5 directly to Angular 21.
- Starting Angular 7 migration in the same change.
- Treating `rxjs-compat` as permanent.
- Migrating the entire application architecture in this hop.
- Removing AngularJS from hybrid apps during this hop.
- Rewriting all HTTP services without tests.
- Rewriting all RxJS streams manually in a massive diff.
- Introducing standalone components or signals.
- Replacing Angular Material blindly.
- Mixing upgrade work with visual redesign.
- Claiming success without validation.

## Do Not

- Do not continue to Angular 7 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 5.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 6.1.x.
- [ ] CLI workspace migration was reviewed.
- [ ] TypeScript compatibility was checked.
- [ ] RxJS compatibility was checked.
- [ ] HTTP migration impact was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Hybrid imports were updated where applicable.
- [ ] Validation commands were run or explicitly unavailable.
- [ ] The next hop was not started automatically.

## Validation Minimum

Read `package.json` first. Only run scripts that exist.

Preferred order when available:

- build
- test
- lint
- e2e

For Angular CLI projects, use direct CLI commands only if they exist in the project.

If validation fails, report:

- command
- error summary
- likely cause
- safe next action

## Risks

- CLI workspace migration can fail if the repo has custom workspace assumptions.
- RxJS 6 migration can introduce import and operator mismatches.
- `HttpClient` migration can alter response handling if done carelessly.
- Hybrid apps can break if `@angular/upgrade/static` is not handled consistently.

## Expected Output

When this skill is used, return:

1. Source Angular version.
2. Target Angular version.
3. Angular CLI version and workspace config status.
4. Applied dependency and code changes.
5. Validation commands and results.
6. Remaining risks.
7. Next hop skill.

## Exit Criteria

This skill is complete only when:

- Angular packages are aligned to Angular 6.1.x.
- The required compatibility code changes were applied.
- Validation ran or blockers were reported.
- The next hop remains unexecuted.

