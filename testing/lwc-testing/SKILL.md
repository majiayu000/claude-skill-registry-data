---
name: lwc-testing
description: "Jest unit tests for LWC — @salesforce/sfdx-lwc-jest, wire adapter mocks, DOM assertions. Triggers: LWC Jest, sfdx-lwc-jest, component test. NOT for Apex tests — use apex/test-class-standards. NOT for browser E2E — use devops/automated-regression-testing."
category: lwc
salesforce-version: "Spring '25+"
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
  - "lwc testing isn't working"
  - "we're having issues with lwc testing"
  - "set up jest for a salesforce dx project"
  - "mock an imperative apex call in a jest test"
  - "emit mock data into a getRecord wire adapter in jest"
  - "assert a custom event fired from a lightning web component"
  - "stop lwc jest tests leaking state between test cases"
  - "test the error path of an lwc without an org"
  - "jest cannot find module @salesforce/apex"
  - "add __tests__ to forceignore"
  - "replace registerLdsTestWireAdapter with the modern api"
  - "gate the ci pipeline on lwc jest coverage"
  - "write jest tests for a lightning web component"
inputs:
  - "component responsibilities, data sources, and important user interactions"
  - "whether the component uses wire adapters, imperative Apex, navigation, or LMS"
  - "current Jest setup, package.json scripts, and test coverage gaps"
outputs:
  - "jest testing strategy for the component"
  - "review findings for missing mocks, weak assertions, and flaky async handling"
  - "test skeletons for render, interaction, wire, and error scenarios"
  - "a runnable component bundle plus its full Jest suite, jest.config.js delta, and CI commands"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when the component works in the browser but the test suite does not prove it reliably. LWC testing is mostly about isolating behavior, mocking the right Salesforce boundaries, and waiting for rerenders intentionally instead of guessing at timing.

---

## Before Starting

Gather this context before working on anything in this domain:

- What behavior matters most: initial render, user interaction, wired data, imperative save, error state, or navigation?
- Which platform boundaries need mocks: Apex, UI API wire adapters, navigation, LMS, or labels?
- Is the current test pain a setup problem, a mocking problem, or an assertion problem?

---

## Questions to Ask Before Configuring

Ask these before writing the first `it()`. Each one traces to a failure in
`references/gotchas.md` that a green suite will not tell you about.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Which of this component's inputs are known before mount, and which arrive after it?" | Properties set before `appendChild` render synchronously; anything set after schedules an async rerender | The exact list for `Object.assign(element, …)` versus the assignments that need an awaited microtask |
| "Every `@salesforce/*` module this component imports — name them." | `apex`, `label`, `schema`, `user/Id` are compiler-generated with no file on disk; each needs `{ virtual: true }` or a `moduleNameMapper` entry, and a label resolves to its *path* if left alone | The mock block, and the config delta, before the first `Cannot find module` |
| "Is each Apex call wired or imperative?" | A wire is driven by `emit()` on the imported adapter; an imperative import is a promise you resolve or reject | Which of the two mocking shapes each import gets — mixing them produces tests that pass against a contract the component does not have |
| "What does the failure path render, and who dispatches nothing when it fires?" | Suites that only emit success leave the `catch` block and the `error` branch at zero coverage while the report still looks healthy | A named negative test per boundary, plus a `not.toHaveBeenCalled()` on the event that must not fire |
| "For every custom event: does it bubble, and does it cross the shadow boundary?" | `bubbles` and `composed` both default to `false`, so a listener anywhere but the host element never fires | Where the listener attaches, and the `detail` shape to assert — not just that the handler was called |
| "Shadow DOM or light DOM?" | Light DOM returns `null` from `this.template`, does not retarget events, and needs different queries | Whether the suite queries through `shadowRoot` at all, and what `event.target` will be |
| "What makes this suite go red — show me the mutation." | A test that appends, never awaits, and asserts `not.toBeNull()` on a conditional region passes on both branches | One deliberate break that proves the assertion reaches the DOM, before the suite is trusted as a gate |

What a proper Jest harness adds over just writing tests: the suite fails for the reasons the component can actually fail, every mocked boundary is declared once instead of drifting per file, and a green run in CI means the error paths ran — not merely that nothing threw.

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

**How it works:** Import the *same* adapter the component imports, create the component, append it, then emit data or an error payload and assert both the happy path and the error state after an awaited microtask. Registering the adapter under test was the Spring '21-and-earlier shape and is no longer recommended (`lwc_guide unit-testing-using-wire-utility L12533, L12548, L12562`).

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
| Component uses a `lightning/ui*Api` adapter | Import the same adapter and call `.emit()` on it after `appendChild` | The sfdx-lwc-jest stub already carries `emit()`; no registration and no `jest.mock` needed |
| Component wires an Apex method | Mock the generated module so its default export is an Apex test wire adapter | The wired Apex contract is a stream, not a promise — see `references/code-examples.md` |
| Component calls Apex imperatively | `jest.mock` the module and resolve or reject promises | Matches the import's imperative usage |
| Component navigates or fires platform events | Mock the platform module and assert invocation | Unit tests should verify intent, not real container behavior |
| Team is relying on snapshots as primary coverage | Replace with behavioral assertions | Snapshots rarely prove business behavior well |

---


## Recommended Workflow

1. **Inventory the boundaries.** List every import the component makes that is not `lwc`: each `@salesforce/*` module, each `lightning/*` service module, each base component. That list is the mock plan; nothing else needs mocking.
2. **Answer the Questions table above.** The wired-versus-imperative question and the propagation question decide the shape of half the suite.
3. **Wire the harness once.** `sf force lightning lwc test setup` at the project root — it installs `@salesforce/sfdx-lwc-jest`, adds the `package.json` scripts, and writes the `__tests__` glob into `.forceignore`. Then take `templates/lwc/jest.config.js` as the base and add only the `moduleNameMapper` delta from `references/code-examples.md`.
4. **Build the suite from `references/code-examples.md`.** Copy the `contactQuickEditor` bundle and its test file; they cover wire emit, wire error, Apex resolve, Apex reject, custom-event payload, label mock, cleanup, and the missing-input negative path. Extend `templates/lwc/component-skeleton/__tests__/componentSkeleton.test.js` rather than starting from a blank file.
5. **Place one `await Promise.resolve()` per async boundary.** Emit after `appendChild`, never before; a click that awaits Apex and then rerenders needs two awaits, not one — see `references/gotchas.md`.
6. **Run the checker.** `python3 skills/lwc/lwc-testing/scripts/check_lwc_testing.py --manifest-dir force-app/main/default/lwc` — zero ERRORs before review, `--strict` in CI so the WARNs (untested bundles, un-flushed emissions, legacy `register*TestWireAdapter`, missing `.forceignore` entry) also block.
7. **Prove the suite can fail.** Break one assertion's expected value on purpose and confirm it goes red, then run `npm run test:unit:coverage` and check the failure branches — not just the totals — against the thresholds in `jest.config.js`. Verification steps are in `references/code-examples.md`.

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

1. **LWC rerenders asynchronously** - assertions immediately after a click or `emit()` run before the DOM updates; one awaited microtask per async boundary, two for a click that awaits Apex.
2. **Imperative Apex and wired Apex are not mocked the same way** - using a wire utility for an imperative import produces misleading tests.
3. **Base components are stubs in Jest** - the test should not assume exact runtime markup from the live platform.
4. **Platform modules such as navigation or toast are mocked boundaries** - assert that your component asked for the action, not that the container performed it.
5. **A custom event with default propagation is invisible off the host** - `bubbles` and `composed` both default to `false`, so the listener belongs on the element `createElement` returned.
6. **A `@salesforce/label` import resolves to its path, not its text** - mock it, or the assertion compares against `c.MyLabel` forever.
7. **A property set before `appendChild` renders synchronously** - only assignments made after the append need an awaited microtask.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Test plan | Coverage strategy for render, interaction, wire, Apex, and error paths |
| Jest review findings | Missing mocks, flaky async patterns, weak assertions, or setup gaps |
| Test scaffold | Reusable test skeleton with cleanup, mocks, and rerender handling |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are writing the suite: full bundle, `.js-meta.xml`, the eight-test Jest file, the `jest.config.js` delta, `.forceignore`, CLI/CI commands, and the verification table |
| `references/gotchas.md` | A test is flaky, falsely green, or fails on something the browser does correctly |
| `references/llm-anti-patterns.md` | Reviewing generated Jest code, or self-checking your own |
| `references/examples.md` | You want the short single-scenario patterns rather than the whole bundle |
| `references/well-architected.md` | Mapping the review to pillars, or checking which official source backs a claim |
| `templates/lwc-testing-template.md` | You need the bare skeleton to paste into a new `__tests__` file |
| `scripts/check_lwc_testing.py` | Auditing an existing `lwc/` tree: `--manifest-dir <dir>`, add `--strict` in CI |

## Related Skills

- **lwc/wire-service-patterns**: what `@wire` provisions and when; come here only for how to drive it from a test.
- **lwc/lwc-imperative-apex**: the production-side call shape this skill mocks.
- **lwc/lifecycle-hooks**: owns hook-order and cleanup assertions; that skill's tests are the reference for `connectedCallback`/`disconnectedCallback` coverage.
- **lwc/component-communication**: the event contract itself — if it is hard to assert, the contract is probably wrong.
- **lwc/lwc-custom-event-patterns**: `bubbles` / `composed` design decisions behind the propagation gotcha here.
- **lwc/lwc-jest-testing-with-accessibility**: the a11y-deep-dive sibling — ARIA, focus, keyboard, and axe integration in the same suite.
- **lwc/static-resources-in-lwc**: owns the `loadScript` / `loadStyle` resource-loader mocking caveat.
- **lwc/lwc-light-dom**: what changes for queries and event targets when the component drops shadow DOM.
- **lwc/lwc-data-table**: `lightning-datatable` specifics that its stub does not reproduce.
- **lwc/lwc-forms-and-validation**: form-state assertions on `lightning-record-edit-form` and friends.
- **devops/automated-regression-testing**: the browser/E2E layer Jest deliberately does not cover.
- **apex/test-class-standards**: server-side coverage; Jest coverage and Apex coverage are unrelated gates.
