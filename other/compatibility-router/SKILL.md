---
id: core.compatibility-router
name: Compatibility Router
description: >
  Prevents incompatible recommendations by routing Angular, TypeScript, JavaScript, RxJS, Node, and tooling advice through detected project versions and supported feature gates.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - compatibility router
  - version compatibility
  - Angular compatibility
  - unsupported API
  - fallback pattern
  - version gate
---

# Compatibility Router

## Purpose

Use this skill to prevent the agent from recommending APIs or patterns that are not compatible with the detected project version. The goal is to provide compatible implementation first and future migration guidance second.

## When to Use

Use this skill when:

- A recommendation depends on Angular, TypeScript, RxJS, Node, browser, test runner, or build tooling version.
- A task mentions Signals, `toSignal`, `toObservable`, `@for`, `@defer`, standalone APIs, `takeUntilDestroyed`, Signal Forms, Angular Aria, `resource`, `httpResource`, `injectAsync`, `@Service`, or WebMCP.
- The project may be legacy, transitional, modern, or current.
- A shared library may be consumed by multiple Angular versions.
- The user asks for a migration path or modern Angular implementation.

Always route Angular version decisions through:

```txt
skills/angular/versioning/angular-version-compatibility-gate/SKILL.md
```

## When Not to Use

Do not use this skill when:

- The change is plain Markdown or version-independent.
- The selected skill already provides a compatible implementation for the detected version.
- No version-sensitive API is involved.

## Inputs Required

Use outputs from `core.stack-version-detection`:

```txt
Angular version
TypeScript version
RxJS version
Node version
package manager
project feature style
shared library constraints
target runtime or browser constraints
```

If version evidence is missing, choose conservative recommendations and mark modern options as future alternatives.

## Version Compatibility

Use these Angular gates:

```txt
Angular 12-13:
  use NgModules, structural directives, *ngFor + trackBy, RxJS, async pipe, OnPush, takeUntil + destroy$
  use constructor injection as the safest DI default
  avoid Signals, @for, @defer, signal inputs, inject() as a required convention, takeUntilDestroyed as a required pattern

Angular 14:
  standalone APIs may appear but should not be assumed as the project default
  inject() may be used only in valid injection contexts and when project convention allows it
  avoid Signals, @for, @defer

Angular 15:
  standalone APIs are safer than Angular 14 but NgModules remain valid
  providedIn, NgModule providers, application providers, and constructor injection remain valid DI choices
  avoid Signals, @for, @defer unless backported tooling proves support

Angular 16:
  Signals and RxJS interop can be considered with caution
  inject() is valid in supported injection contexts
  prefer RxJS for async orchestration
  avoid forcing Signals into public library contracts

Angular 17-18:
  control flow and deferrable views can be considered
  prefer @for for new list code when project style supports it
  use fallbacks for legacy sections

Angular 19:
  prefer modern lifecycle helpers when dependencies support them
  Signals are appropriate for local synchronous state

Angular 20:
  prefer @for for new list rendering code
  avoid introducing new NgFor code for new features

Angular 21:
  follow current Angular compatibility tables for Node, TypeScript, and RxJS
  use current DI patterns such as providedIn, application providers, route providers, and inject() when project style supports them
  prefer current Angular patterns when the project is already current

Angular 22:
  Signal Forms, Angular Aria, resource(), and httpResource() are production-ready according to official Angular v22 sources
  OnPush is the default for new applications and the prior default is named ChangeDetectionStrategy.Eager
  WebMCP remains experimental and must go through a security gate
  route upgrade work through skills/angular/upgrades/21-to-22/ before applying modernization satellites
```

## Required Angular Version Gate

Before recommending an Angular hop or version-sensitive Angular API, require:

```txt
skills/angular/versioning/angular-version-compatibility-gate/SKILL.md
```

Use it to determine:

- whether the current project can move to the target Angular version,
- whether the next hop is blocked by Node, TypeScript, RxJS or Angular CLI ranges,
- whether routing to a satellite skill is required before planning the hop.

Treat WebMCP and future preview APIs as experimental unless official Angular sources say otherwise. In Angular 22, `resource()` and `httpResource()` are production-ready, but still require SSR/cache/security review when used for data fetching.

## Subagent Review Trigger

When `agents/ngautopilot/subagents/` is available and compatibility risk remains after routing, use the Compatibility Gatekeeper as a focused reviewer. Do not load unrelated subagents or replace the required Angular version gate with a subagent opinion.

## Decision Rules

Apply this policy:

```txt
compatible implementation > modern syntax > future migration path
project style > framework trend
shared library compatibility > app-only modernization
stable API > experimental API
small safe change > broad migration
```

If the detected version is unsupported by current framework support policy, still provide practical legacy-compatible guidance and label it as legacy.

## Execution Workflow

Use this workflow:

```txt
1. Read detected versions.
2. Classify profile: legacy, transitional, modern, or current.
3. List safe APIs.
4. List APIs to avoid.
5. Choose compatible implementation.
6. Add optional future migration path.
7. Flag experimental or unstable APIs.
```

## Do

Recommended compatibility pattern:

```txt
For Angular 12, solve with *ngFor + trackBy.
For Angular 17+, offer @for with track.
For Angular 20+, prefer @for for new code.
```

## Do Not

Avoid unsupported code:

```txt
Use signal inputs in Angular 12.
Use @defer in Angular 15.
Require takeUntilDestroyed in Angular 13.
Require inject() style in an Angular 12 codebase.
Use resource as a default production data-fetching baseline.
```

Avoid hiding compatibility uncertainty.

## Output Format

Use this format:

```md
## Compatibility Profile

- Angular:
- TypeScript:
- RxJS:
- Node:
- Profile:

## Safe APIs

- ...

## APIs To Avoid

- ...

## Compatible Recommendation

- ...

## Future Migration Path

- ...
```

## Review Checklist

- [ ] Detected versions are listed.
- [ ] Safe and unsafe APIs are separated.
- [ ] The recommendation compiles for the target version.
- [ ] Modern alternatives are marked as future path when unsupported.
- [ ] Experimental APIs are avoided by default.
- [ ] Shared library consumers are considered.

## Risks

- Version ranges can hide actual installed versions.
- Shared libraries may need a lower compatibility baseline than the app.
- Experimental APIs may change.
- Modernizing syntax without tests can create subtle behavior changes.

## Examples

```txt
Angular 15 task asks for Signals:
Recommendation: do not use Signals. Use RxJS or component state. Add Signals as a future Angular 16+ migration path.
```

```txt
Angular 21 task asks for list rendering:
Recommendation: use @for with track for new code. Do not introduce NgFor for new list code.
```

## Expected Output

1. Classify compatibility profile.
2. Identify safe and unsafe APIs.
3. Provide compatible code or guidance.
4. Provide future migration notes separately.
5. Avoid unsupported or experimental defaults.
