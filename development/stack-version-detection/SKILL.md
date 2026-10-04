---
id: core.stack-version-detection
name: Stack Version Detection
description: >
  Detects Angular, TypeScript, JavaScript, Node, RxJS, package manager, test runner, linting, and framework features from repository evidence before applying version-sensitive guidance.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - detect stack version
  - Angular version
  - TypeScript version
  - Node version
  - RxJS version
  - package manager detection
---

# Stack Version Detection

## Purpose

Use this skill to detect the real project stack before recommending APIs, migrations, test commands, or refactors. The goal is to avoid code that cannot compile in the target project.

## When to Use

Use this skill when:

- Angular, TypeScript, RxJS, or Node versions affect the recommendation.
- The task mentions Signals, standalone APIs, `@for`, `@defer`, `takeUntilDestroyed`, `resource`, or modern Angular features.
- Test, lint, build, or package commands must be chosen.
- The project has multiple package or workspace files.
- A migration or compatibility decision is required.

## When Not to Use

Do not use this skill when:

- The task is version-independent.
- A recent detection already exists in the same turn and the dependency files have not changed.
- The user explicitly provides authoritative versions for the task.

## Inputs Required

Inspect available evidence in this order:

```txt
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
angular.json
nx.json
workspace.json
tsconfig.json
tsconfig.base.json
engines field
.nvmrc
.node-version
Dockerfile
CI workflow files
source imports and template syntax
```

Detect:

```txt
Angular framework and CLI versions
TypeScript version
RxJS version
Node requirement
package manager
workspace tool: Angular CLI, Nx, custom, Vite, other
test runner: Jest, Vitest, Karma/Jasmine, Playwright, Cypress
linting: ESLint, TSLint, none, unknown
feature usage: NgModules, standalone, Signals, control flow, deferrable views
```

Pass the detected versions to:

```txt
skills/angular/versioning/angular-version-compatibility-gate/SKILL.md
skills/_core/compatibility-router/SKILL.md
```

## Version Compatibility

Use detected versions as input for `core.compatibility-router`.

Current official Angular documentation lists active support for Angular 19, 20, and 21, and provides Node, TypeScript, and RxJS compatibility tables. Older Angular versions can still exist in real repositories, but they should be treated as legacy or unsupported by current Angular support policy.

## Decision Rules

Prefer direct dependency evidence:

```txt
dependencies.@angular/core > package lock resolved version > imports or syntax clues > README claims
```

Treat ranges carefully:

```txt
"@angular/core": "^17.3.0" means installed version may be newer within the allowed range.
lockfile gives stronger evidence than package.json range.
```

Detect feature usage separately from version:

```txt
Angular 17 project may still use *ngFor and NgModules.
Angular 16 project may not use Signals.
Angular 15 project may be standalone or NgModule-based.
```

## Execution Workflow

Use this workflow:

```txt
1. Read package metadata.
2. Check lockfile when exact versions matter.
3. Check workspace config.
4. Check TypeScript and Node constraints.
5. Check source syntax for adopted features.
6. Report detected stack and confidence.
```

## Do

Recommended detection pattern:

```txt
Report exact versions when known, ranges when only package.json is available, and unknown when evidence is absent.
```

## Do Not

Avoid guessing:

```txt
The project has Angular syntax, so it must support Signals.
```

Avoid using Angular CLI version as the only evidence for framework version when `@angular/core` is available.

Avoid assuming one lockfile if multiple lockfiles conflict.

## Output Format

Use this format:

```md
## Stack Detected

- Angular:
- Angular CLI:
- TypeScript:
- RxJS:
- Node:
- Package manager:
- Workspace:
- Testing:
- Linting:
- Angular feature style:
- Confidence:
```

## Review Checklist

- [ ] `@angular/core` version is checked when relevant.
- [ ] Lockfile is checked when exact installed version matters.
- [ ] Node and TypeScript constraints are considered.
- [ ] Test and lint commands are inferred from scripts or config.
- [ ] Feature usage is not assumed from version alone.
- [ ] Uncertainty is stated clearly.

## Risks

- Package ranges may not equal installed versions.
- Multiple lockfiles can indicate stale or conflicting package manager usage.
- Source syntax may reflect partial migrations.
- Unsupported Angular versions require conservative recommendations.

## Examples

```txt
Angular 12 detected:
Safe: NgModules, RxJS, *ngFor + trackBy, async pipe, takeUntil.
Avoid: Signals, @for, @defer, takeUntilDestroyed as a required pattern.
```

```txt
Angular 20 detected:
Safe: modern control flow, @for, Signals, takeUntilDestroyed when project style supports it.
Avoid: introducing new NgFor code for new list rendering.
```

## Expected Output

1. Detect stack versions from repository evidence.
2. Distinguish exact versions from ranges.
3. Identify adopted framework features.
4. Report confidence and unknowns.
5. Pass compatibility facts to the next skill.
