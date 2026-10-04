---
id: angular.upgrade.hops.angular-8-to-9
name: Angular 8 to Angular 9.1 Upgrade
description: >
  Performs the Angular 8.x to Angular 9.1.x major-hop upgrade in a bounded, critical compatibility slice with Ivy, libraries, Material, and validation-gate checks.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular 8 to 9
  - Angular 9.1 upgrade
  - Ivy migration
  - major hop upgrade
compatibility:
  angular:
    sourceMin: "8"
    sourceMax: "8.x"
    target: "9.1"
---

# Angular 8 to Angular 9.1 Upgrade

## Purpose

Use this skill to upgrade an Angular 8.x application to Angular 9.1.x in one bounded major hop.

This hop is a critical compatibility boundary because Angular 9 enables Ivy by default. It upgrades only from Angular 8 to Angular 9.1 and must not continue to Angular 10 or later. The next hop must be handled by a dedicated follow-up skill.

## When to Use

Use this skill when:

- The project is currently on Angular 8.x.
- The target hop is Angular 9.1.x.
- The route planner selected `8 -> 9` as the next step.
- The Angular 7 -> 8 validation gate passed.
- The workspace uses `angular.json`.
- Angular CLI, RxJS, and workspace status are known.
- Angular Material usage is known.
- Lazy route syntax status is known.
- Library compatibility risk is known.

## When Not to Use This Skill

Do not use this skill when:

- The project is AngularJS 1.x.
- The project is Angular 7.x or lower.
- The project is already Angular 9 or later.
- The previous Angular 7 -> 8 validation gate failed.
- The workspace does not use `angular.json`.
- Angular Material version is unknown in a Material project.
- Lazy loaded routes still use string syntax and the risk is not documented.
- Angular library compatibility is unknown.
- The task is only Ivy troubleshooting without version upgrade.
- The requested change is Angular 9 to Angular 10.

For Angular 9 to Angular 10, route to:

```txt
skills/angular/upgrades/hops/angular-9-to-10/SKILL.md
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
- Zone.js version
- Node.js version
- `angular.json`
- `browserslist`
- `.browserslistrc`
- `tsconfig.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `polyfills.ts`
- use of Ivy config: `enableIvy`
- use of Angular libraries
- use of `@angular/material` root imports
- use of lazy route string syntax
- use of `/deep/`
- use of `::ng-deep`
- use of Angular i18n
- use of `$localize`
- use of `entryComponents`
- use of `ANALYZE_FOR_ENTRY_COMPONENTS`
- use of `ModuleWithProviders`
- use of `TestBed.get`
- use of `ngForm` element selector
- use of Angular Universal
- use of `@angular/platform-webworker`
- use of `wtf*` tracing APIs
- use of classes with Angular features but no Angular decorator
- use of incomplete provider definitions
- current build/test/lint/e2e scripts
- screenshot/golden test scripts if present

## Compatibility by Version

| Area | Recommended strategy | Observations |
|---|---|---|
| Angular 8.x source | Upgrade to Angular 9.1.x only | Do not jump to a later major in this skill. |
| Ivy | Enable by default unless a documented blocker exists | View Engine fallback is temporary only. |
| Angular CLI | Upgrade to CLI 9 | Keep workspace validation explicit. |
| TypeScript | Align to Angular 9-compatible TypeScript 3.8 | Verify against project evidence. |
| Angular Material | Upgrade to Material 9 only if used | Do not go beyond Angular 9 in this hop. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Inspect dependency versions and lockfile evidence.
2. Check Node.js, CLI, workspace, and validation-gate status.
3. Update Angular 8 to the latest patch before the Angular 9 upgrade if needed.
4. Scan the codebase for Angular 8-era deprecated or risky APIs.
5. Classify each occurrence by impact and required change.
6. Apply the bounded dependency upgrade to Angular 9.1.
7. Convert only the code required by the hop.
8. Run validation commands that exist in the repository.
9. Set the gate result explicitly.
10. Stop after Angular 9.1. Do not begin the next hop.

## Do

- Keep the hop bounded to Angular 8 -> Angular 9.1.
- Treat Ivy compatibility as the main boundary.
- Review libraries, Material imports, lazy routes, styles, `ModuleWithProviders`, `entryComponents`, `TestBed.get`, `ngForm`, `@angular/localize`, and DI/provider strictness.
- Use the previous validation gate as a hard gate condition.
- Stop after validation and report the next hop.

## Recommended Patterns

Upgrade Angular packages to Angular 9.1-compatible versions using the project-supported package manager and CLI workflow.

Use `ng update` or the repository-supported equivalent for Angular CLI 9 and Angular core 9.

Enable Ivy by default unless a documented blocker exists:

```json
{
  "angularCompilerOptions": {
    "enableIvy": true
  }
}
```

Replace `ModuleWithProviders` with an explicit generic:

```ts
static forRoot(): ModuleWithProviders<CoreModule> {
  return {
    ngModule: CoreModule,
    providers: []
  };
}
```

Use `TestBed.inject` in touched tests:

```ts
const service = TestBed.inject(MyService);
```

Treat the validation gate as part of the hop, not a later concern.

## Anti-Patterns

- Jumping from Angular 8 directly to Angular 21.
- Starting Angular 10 migration in the same change.
- Skipping the latest Angular 8 patch update.
- Updating Angular Material beyond v9.
- Disabling Ivy without a documented blocker.
- Treating View Engine fallback as final state.
- Ignoring Angular library compatibility.
- Leaving string lazy routes for Angular 9.
- Leaving Material root imports unresolved.
- Guessing `ModuleWithProviders` generic types.
- Adding `@angular/localize` when no Angular i18n exists.
- Removing `entryComponents` blindly from libraries consumed by View Engine apps.
- Updating Universal with `--force` without documenting peer dependency risk.
- Regenerating screenshot golden files blindly.
- Removing AngularJS from hybrid apps during this hop.
- Introducing standalone components or signals.
- Claiming success without build/test validation.
- Passing the gate when Ivy, Material, Universal, library, or style status is unknown.

## Do Not

- Do not continue to Angular 10 or later.
- Do not change unrelated application architecture.
- Do not force later Angular patterns into this hop.
- Do not run commands that do not exist in `package.json`.
- Do not claim completion without validation evidence.

## Review Checklist

- [ ] Angular 8.x source version was confirmed.
- [ ] Angular packages were aligned to Angular 9.1.x.
- [ ] Latest Angular 8 patch update was considered or applied first.
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

- Node.js is lower than 10.13
- build fails
- tests fail
- Angular CLI update is incomplete
- Angular Material update is incomplete in a Material project
- Angular Universal update is incomplete in a Universal project
- Ivy compatibility is unknown
- Ivy is disabled without documented blocker
- library compatibility is unknown
- lazy string routes remain
- Material root imports remain without documentation
- `ModuleWithProviders` generics are missing in library APIs
- i18n uses Angular localization but `@angular/localize` is missing
- `tsconfig.app.json` excludes required declaration files
- `TestBed.get` remains in touched tests
- `entryComponents` cleanup status is unknown
- bound style/class regressions are unreviewed
- screenshot changes are unreviewed
- workspace config is unstable

## Risks

- Ivy compatibility can break Angular libraries or hybrid setups.
- Style/class precedence changes can surface subtle UI regressions.
- `ModuleWithProviders` and DI strictness can break libraries or shared modules.
- Entry component cleanup can affect libraries compiled for compatibility.
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

- Angular packages are upgraded to Angular 9.1-compatible versions.
- Angular CLI is upgraded to v9.
- Angular Material/CDK are upgraded to v9 only if used.
- Ivy default status is explicit.
- Angular libraries are reviewed for Angular 9 compatibility.
- Material imports use specific entry points.
- String lazy routes are migrated to dynamic imports.
- `es5BrowserSupport` is removed.
- TypeScript target and browserslist behavior are reviewed.
- `ModuleWithProviders` uses explicit generic types where required.
- `ngForm` element selector is replaced with `ng-form` where applicable.
- `tsconfig.app.json` includes required declaration files.
- `@angular/localize` is added when Angular i18n is used.
- Application `entryComponents` and `ANALYZE_FOR_ENTRY_COMPONENTS` are removed where safe.
- `TestBed.get` is replaced with `TestBed.inject` in touched tests.
- DI/provider strictness issues are migrated or flagged.
- Material and style regressions are reviewed.
- Validation ran or blockers were reported.
- Validation gate result is explicit.
- The next hop remains unexecuted.

