---
id: angular.resources.angular-v22-resource-apis
name: Angular v22 Resource APIs
description: >
  Use this skill when Angular 22 async data should be modeled with the production-ready resource APIs.
stack:
  - Angular
  - TypeScript
category: resources
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - resource
  - httpResource
  - async state
  - loading state
compatibility:
  angular:
    min: "22"
---

# Angular v22 Resource APIs

## Purpose

Use this skill when Angular 22 async data should be modeled with the production-ready resource APIs.

## When to Use

Use this skill when:

- The feature needs asynchronous data loading in v22.
- You want resource or httpResource instead of ad hoc fetch orchestration.
- Tests or UI logic depend on the exact loading or value timing.

## When Not to Use

Do not use this skill when:

- The change is purely synchronous signal state.
- The task is only about forms or routing.
- The project does not need async resource modeling.

## Required Inputs

- async source
- sync vs async expectations
- SSR interaction
- test assumptions

## Procedure

1. Model the async source with resource or httpResource.
2. Account for synchronous resolution when the loader emits synchronously.
3. Keep loading, value, and error states explicit.
4. Validate the component and test behavior after the change.

## Do

- Use the production-ready resource APIs on v22.
- Keep the state model declarative.
- Document any sync-vs-async assumption in tests.

## Do Not

- Do not hide async state behind a custom wrapper without a reason.
- Do not assume every resource resolves asynchronously.
- Do not mix resource modeling with unrelated template cleanup.

## Review Checklist

- [ ] The async model is explicit.
- [ ] Sync resolution is handled correctly.
- [ ] Tests still match the runtime behavior.

## Expected Output

1. A resource-API summary.
2. The chosen async model.
3. Timing-related risks.
