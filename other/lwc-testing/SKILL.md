---
name: lwc-testing
description: "Use when setting up or reviewing Lightning Web Component unit tests with Jest, including `@salesforce/sfdx-lwc-jest`, wire adapter mocks, imperative Apex mocks, async rerender handling, and accessibility smoke checks. Triggers: 'how do I test @wire in LWC', 'Jest test is flaky', 'mock Apex in LWC test', 'flushPromises pattern'. NOT for Apex unit tests, browser end-to-end automation, or performance testing."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Reliability
  - Operational Excellence
  - User Experience
tags:
  - lwc-testing
  - jest
  - sfdx-lwc-jest
  - wire-mocks
  - accessibility-testing
triggers:
  - "how do i test @wire in lwc"
  - "jest test is flaky after clicking the button"
  - "how should i mock apex in an lwc test"
  - "lwc unit test needs flushPromises"
  - "need accessibility checks in lwc jest"
inputs:
  - "component responsibilities, data sources, and important user interactions"
  - "whether the component uses wire adapters, imperative Apex, navigation, or LMS"
  - "current Jest setup, package.json scripts, and test coverage gaps"
outputs:
  - "jest testing strategy for the component"
  - "review findings for missing mocks, weak assertions, and flaky async handling"
  - "test skeletons for render, interaction, wire, and error scenarios"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when the component works in the browser but the test suite does not prove it reliably. LWC testing is mostly about isolating behavior, mocking the right Salesforce boundaries, and waiting for rerenders intentionally instead of guessing at timing.

---

## Before Starting

Gather this context before working on anything in this domain:

- What behavior matters most: initial render, user interaction, wired data, imperative save, error state, or navigation?
- Which platform boundaries need mocks: Apex, UI API wire adapters, navigation, LMS, or labels?
- Is the current test pain a setup problem, a mocking problem, or an assertion problem?

---

## Core Concepts

Jest unit tests run in Node and use mocks instead of live Salesforce services. That means a good test verifies behavior at the component boundary, not whether the real platform is present. Most flaky tests fail because they mix production mental models with a mocked unit-test runtime.

### Test Behavior, Not Private Implementation

The test should render the component, drive the public interaction, and assert visible behavior or emitted events. A test that knows too much about private fields or incidental DOM structure becomes brittle during harmless refactors.

### Async Rerendering Must Be Awaited Intentionally

LWC rerendering is asynchronous. After setting properties, emitting wire values, or resolving promises, the test must wait for microtasks before asserting the DOM. Many "random" failures are simply assertions that run before the component has had a chance to rerender.

### Wire And Imperative Apex Use Different Mocking Patterns

A wired Apex method or wire adapter should use the appropriate wire test utilities and emitted values. Imperative Apex calls should be mocked as module functions that resolve or reject promises. Mixing those patterns creates confusing tests that do not reflect the component's actual contract.

### Base Components And Platform Services Are Test Doubles

`lightning-*` base components are stubs in Jest. Navigation, toasts, labels, and many platform modules are mocked. That is expected. The test should focus on your component behavior, not on reproducing the entire browser-plus-Salesforce runtime.

---

## Common Patterns

### Render, Interact, Assert

**When to use:** The component behavior is driven by user actions or reactive property updates.

**How it works:** Create the element, append it to `document.body`, simulate the user action, wait for rerender, then assert the visible state or dispatched event.

**Why not the alternative:** Snapshot-only tests or direct private-field assertions tend to miss the actual behavior users care about.

### Wire Adapter Emission Testing

**When to use:** A component reads data through `@wire`.

**How it works:** Register the test wire adapter, create the component, emit data or error payloads, and assert both the happy path and the error state after the rerender boundary.

**Why not the alternative:** Mocking the rendered HTML without exercising the wire contract gives false confidence.

### Imperative Apex Promise Testing

**When to use:** A component saves or refreshes data through an imperative Apex call.

**How it works:** Mock the imported Apex module with `jest.mock`, resolve and reject the promise intentionally, and assert loading, success, and failure behavior.

**Why not the alternative:** Treating an imperative method like a wire adapter hides the actual async behavior and error path.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Component only needs a render or interaction check | `createElement` plus DOM assertions | Fastest path to behavior coverage |
| Component uses a wire adapter or wired Apex | Register and emit from a test wire adapter | Mirrors the reactive contract of the component |
| Component calls Apex imperatively | `jest.mock` the module and resolve or reject promises | Matches the import's imperative usage |
| Component navigates or fires platform events | Mock the platform module and assert invocation | Unit tests should verify intent, not real container behavior |
| Team is relying on snapshots as primary coverage | Replace with behavioral assertions | Snapshots rarely prove business behavior well |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] The project includes `@salesforce/sfdx-lwc-jest` and a runnable unit-test script.
- [ ] Each important component has tests for success and failure paths, not only happy render.
- [ ] Wire adapters and imperative Apex calls use the correct mocking pattern.
- [ ] Tests wait for rerender or promise completion before asserting DOM state.
- [ ] `afterEach` cleanup removes mounted elements from `document.body`.
- [ ] Assertions target behavior that users or consumers rely on.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **LWC rerenders after the current microtask** - assertions immediately after a click or `emit()` often run too early.
2. **Imperative Apex and wired Apex are not mocked the same way** - using a wire utility for an imperative import produces misleading tests.
3. **Base components are stubs in Jest** - the test should not assume exact runtime markup from the live platform.
4. **Platform modules such as navigation or toast are mocked boundaries** - assert that your component asked for the action, not that the container performed it.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Test plan | Coverage strategy for render, interaction, wire, Apex, and error paths |
| Jest review findings | Missing mocks, flaky async patterns, weak assertions, or setup gaps |
| Test scaffold | Reusable test skeleton with cleanup, mocks, and rerender handling |

---

## Related Skills

- `lwc/wire-service-patterns` - use when the real bug is the data contract rather than the test harness.
- `lwc/lifecycle-hooks` - use when timing or cleanup bugs exist in production as well as tests.
- `lwc/component-communication` - use when the component contract itself is hard to test because the communication design is wrong.
