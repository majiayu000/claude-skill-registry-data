---
id: angular.architecture.angular-patterns-senior
name: Angular Senior Architecture Patterns
description: >
  Orchestrates senior Angular architecture review by selecting focused patterns for container/presentational components, facades, state boundaries, service responsibility, and reactive contracts.
stack:
  - Angular
  - TypeScript
  - RxJS
category: architecture
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular architecture review
  - senior Angular patterns
  - scalable Angular structure
  - refactor Angular component
  - split Angular responsibilities
  - facade pattern
compatibility:
  angular:
    min: "2"
    conservativeBaseline: "12+"
    signalsFrom: "16"
    recommendedModern: "17+"
    currentSafe: "19+"
---

# Angular Senior Architecture Patterns

## Purpose

Use this skill to route an Angular architecture task to the smallest applicable architecture skill. The goal is to improve structure, testability, and maintainability without turning every component into a ceremony-heavy architecture exercise.

This is a coordinator skill. It should select focused micro-skills instead of applying every architecture pattern at once.

## When to Use

Use this skill when:

- A component fetches data, maps DTOs, manages state, handles navigation, renders complex UI, and owns permissions at the same time.
- A service has unrelated responsibilities or a generic name such as `CommonService`, `ManagerService`, or `UtilsService`.
- A feature has unclear ownership between UI, API, state, and orchestration.
- Components depend on many low-level services directly.
- Mutable state is exposed through public subjects or writable signals.
- The user asks whether to use RxJS, Signals, facades, or container/presentational split.
- A shared library, microfrontend, or reusable feature needs cleaner public contracts.

## Do

Select the smallest matching architecture skill:

```txt
component orchestration vs UI rendering -> angular.components.container-presentational
Signals vs RxJS decision -> angular.state.signals-vs-rxjs
feature API and service coordination -> angular.architecture.facade-pattern
god service or generic service -> angular.services.single-responsibility-services
public reactive contracts -> angular.rxjs.observable-contracts
version-gated Angular APIs -> angular.versioning.angular-version-gates
providers, injectors, InjectionToken, or NullInjectorError -> angular.dependency-injection
```

Before recommending code, identify:

```txt
Angular version
project style: NgModules, standalone, or mixed
state model: RxJS, Signals, store, facade, or custom service state
file role: app, feature, shared library, data-access, UI, or microfrontend boundary
testing stack: Jest, Jasmine/Karma, Vitest, or unknown
compatibility constraints: legacy support, modern-only, or shared package
```

Prefer incremental refactoring:

```txt
1. Identify responsibilities.
2. Split the highest-risk responsibility first.
3. Define a narrow public contract.
4. Protect mutable internals.
5. Add tests around behavior before deeper restructuring.
```

## Do Not

Avoid applying patterns just because they sound senior:

```txt
Create a facade, store, mapper, state service, UI library, and signal model for a trivial component.
```

Avoid recommending Signals for Angular versions that do not support them.

Avoid replacing RxJS with Signals for asynchronous workflows by default.

Avoid creating a facade that only forwards one method and adds no useful boundary.

Avoid turning containers into business-rule monoliths.

## Review Checklist

- [ ] Angular version is identified before recommending version-specific APIs.
- [ ] The current file responsibilities are listed.
- [ ] The selected pattern solves a real maintainability or testing problem.
- [ ] Presentational components do not fetch data.
- [ ] Services have bounded responsibilities.
- [ ] Mutable subjects or writable signals are not exposed publicly.
- [ ] RxJS remains the default for cancellation, retries, streams, and async orchestration.
- [ ] Signals are limited to compatible versions and appropriate local synchronous state.
- [ ] The proposed split reduces coupling instead of adding ceremony.

## Expected Output

1. Diagnose the current architecture problem.
2. Select the smallest relevant micro-skill.
3. Explain version compatibility and APIs to avoid.
4. Propose an incremental target structure.
5. Include testing guidance and overengineering risks.
