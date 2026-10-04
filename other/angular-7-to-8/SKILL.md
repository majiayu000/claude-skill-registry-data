---
id: angular.upgrade.hops.angular-7-to-8
name: Angular 7 to Angular 8.2 Upgrade
description: >
  Performs the Angular 7.x to Angular 8.2.x major-hop upgrade in a bounded, version-aware slice with CLI, Material, styles, lazy loading, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 7 to 8
  - Angular 8.2 upgrade
  - major hop upgrade
  - validation gate
compatibility:
  angular:
    sourceMin: "7"
    sourceMax: "7.x"
    target: "8.2"
---

# Angular 7 to Angular 8.2 Upgrade

## Purpose

Use this skill to upgrade an Angular 7.x application to Angular 8.2.x in one bounded major hop.

This skill upgrades only from Angular 7 to Angular 8.2. It must not continue to Angular 9 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 7.x.
- The target hop is Angular 8.2.x.
- The route planner selected `7 -> 8` as the next step.
- The previous Angular 6+ validation gate passed or the remaining risks were accepted.
- The workspace uses `angular.json`.
- Angular CLI, RxJS, and workspace status are known.
- Angular Material usage is known.
- Style strategy is known.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 6.x or lower.
- The project is already Angular 8 or later.
- The previous Angular 6 -> 7 validation gate failed.
- Workspace status is unknown.
- RxJS status is unknown.
- Angular Material version is unknown in a Material project.
- The requested change is Angular 8 to Angular 9.
- The task is only a style cleanup without Angular upgrade.
- The task is only Angular Material migration without Angular core upgrade.

For Angular 8 to Angular 9, route to:

```txt
skills/angular/upgrades/hops/angular-8-to-9/SKILL.md
```

## Inputs Expected

- `package.json`
- lock file: `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`
- Angular package versions
- Angular CLI version
- Angular Material version
- Angular CDK version
- TypeScript version
- RxJS version
- `rxjs-compat` usage
- Zone.js version
- Node.js version
- `angular.json`
- `browserslist`
- `.browserslistrc`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `polyfills.ts`
- use of Angular Service Worker
- use of screenshot/golden tests
- use of SCSS/Sass
- use of `node-sass`
- use of `/deep/`
- use of `::ng-deep`
- use of `@angular/material` barrel imports
- use of lazy route string syntax
- use of `ViewChild`
- use of `ContentChild`
- use of `@angular/platform-webworker`
- use of `wtf*` tracing APIs
- use of custom schematics
- use of legacy `HttpModule`
- use of `Http`
- use of deprecated Material ripple APIs
- current build/test/lint/e2e scripts

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 7.x source | Upgrade to Angular 8.2.x only | Do not jump to a later major in this skill. |
| Angular CLI | Upgrade to CLI 8 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 8-compatible TypeScript 3.4 | Verify against project evidence. |
| RxJS | Keep RxJS 6 cleanup explicit and remove `rxjs-compat` when safe | Treat `rxjs-compat` as temporary if retained. |
| Angular Material | Upgrade to Material 8 only if used | Do not go beyond Angular 8 in this hop. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Scan the codebase for Angular 7-era deprecated or risky APIs.
4. Classify each occurrence by impact and required change.
5. Apply the bounded dependency upgrade to Angular 8.2.
6. Convert only the code required by the hop.
7. Run validation commands that exist in the repository.
8. Set the gate result explicitly.
9. Stop after Angular 8.2. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 7 -> Angular 8.2.
- Check CLI workspace, Material, styles, lazy routes, queries, differential loading, browserslist, `rxjs-compat`, `HttpModule`/`Http`, and service worker status.
- Remove `rxjs-compat` only when no legacy imports or third-party requirements remain and validation passes without it.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 8.2-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 8 and Angular core 8.

Replace `/deep/` with `::ng-deep` as a temporary compatibility step:

```scss
:host ::ng-deep .child {
  color: red;
}
```

Make `ViewChild` and `ContentChild` query timing explicit:

```ts
@ViewChild('foo', { static: false }) foo!: ElementRef;
```

Convert string lazy routes to dynamic imports:

```ts
{
  path: 'admin',
  loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
}
```

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 7 directly to Angular 21.
- Starting Angular 9 migration in the same change.
- Updating Angular Material beyond v8.
- Ignoring style changes caused by Material or Sass compiler changes.
- Replacing `/deep/` with global CSS as a shortcut.
- Accepting all `ViewChild` static values blindly in critical components.
- Leaving string lazy routes for Angular 9 without documenting the blocker.
- Adding `node-sass` preemptively.
- Opting into CLI analytics silently.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components or signals.
- Claiming success without build/test validation.
- Passing the gate when CLI, core, Material, styles, or build target status is unknown.

## Do Not

- Do not continue to Angular 9 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 7.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 8.2.x.
- [ ] CLI workspace status was checked.
- [ ] TypeScript compatibility was checked.
- [ ] RxJS compatibility was checked.
- [ ] `rxjs-compat` status was checked.
- [ ] Deprecated APIs were classified and handled.
- [ ] Styles and query timing were reviewed.
- [ ] Lazy routes were reviewed.
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
- Angular Material update is incomplete in a Material project
- style migration has unresolved breakage
- `/deep/` usage remains without documentation
- `ViewChild` / `ContentChild` query migration is incomplete
- lazy route string syntax remains without documentation
- `rxjs-compat` status is unknown
- legacy `HttpModule` status is unknown
- `es5BrowserSupport` / differential loading status is unknown
- screenshot changes are unreviewed
- workspace config is unstable

## Risks

- CLI and Material upgrades can cascade into build and visual regressions.
- `/deep/` replacement may surface style encapsulation issues.
- Query timing changes can break critical component lifecycle assumptions.
- Lazy route conversion can break route loading if paths are incorrect.

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

- Angular packages are upgraded to Angular 8.2-compatible versions.
- Angular CLI is upgraded to v8.
- Angular Material/CDK are upgraded to v8 only if used.
- TypeScript is aligned to Angular 8-compatible TypeScript 3.4.
- Node.js 10+ compatibility has been confirmed.
- `/deep/` is replaced with `::ng-deep` or documented.
- `ViewChild` and `ContentChild` queries include explicit `static` values.
- String lazy routes are migrated to dynamic imports or documented as blockers.
- Material imports use specific entry points instead of `@angular/material`.
- `rxjs-compat` is removed or explicitly documented.
- Legacy `HttpModule` / `Http` usage is removed or explicitly documented.
- Validation ran or blockers were reported.
- Validation gate result is explicit.
- The next hop remains unexecuted.

