---
name: flow-testing
description: "Use when defining or reviewing test strategy for Salesforce Flow, including Flow Tests, debug runs, path coverage, test data, and explicit validation of fault paths and custom component behavior. Triggers: 'flow test tool', 'how do i test a flow', 'flow fault path testing', 'flow debug interview'. NOT for Apex unit testing or manual QA planning that is unrelated to Flow behavior — use flow/flow-debugging. Also covers: FlowTest metadata, flowtest-meta.xml, testPoints, Flow.Interview, sf flow run test, flow coverage."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Reliability
  - Operational Excellence
tags:
  - flow-testing
  - flow-tests
  - path-coverage
  - debug-interview
  - test-data
triggers:
  - "how do i test a salesforce flow"
  - "flow test tool and path coverage"
  - "how should i test flow fault paths"
  - "debug flow interview results"
  - "screen flow custom component testing"
  - "write a flowtest for a record triggered flow"
  - "assert a flow fault path fired in a test"
  - "run an autolaunched flow from an apex test class"
  - "flowtest passes but the flow breaks in production"
  - "does salesforce require test coverage to activate a flow"
  - "wire sf flow run test into a ci pipeline"
  - "cannot mock an apex action inside a flow test"
  - "write a flow test for a record-triggered flow before activating it"
inputs:
  - "which flow type is under test and which paths are business-critical"
  - "what test data is required for happy, edge, and failure scenarios"
  - "whether custom LWC components, Apex actions, or external dependencies are involved"
outputs:
  - "flow test strategy covering happy, edge, and fault paths"
  - "review findings for missing test coverage, weak data setup, or manual-only validation"
  - "guidance on combining Flow Tests, debug runs, and component-level tests where needed"
dependencies: []
version: 2.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when a Flow works in a demo but nobody can yet prove it is safe to change. Flow testing is not one tool — it is a test STRATEGY that combines declarative Flow Tests where they fit, focused debug runs for diagnosis, deliberate test data, and extra coverage at custom component or Apex boundaries when the Flow itself is not the whole system.

Unlike Apex, Flow does not have a forced test-coverage gate at deploy time. This makes flow testing strictly a discipline problem, not a tooling problem. Teams that rely on "I clicked through it once in sandbox" as their coverage story are one change away from a production incident with no regression safety net. This skill exists to make that discipline concrete.

**What FlowTest reaches, in the guide's own words.** "Before you activate a record-triggered, autolaunched, or Data Cloud-triggered flow, you can test it to verify its expected results and identify flow run-time failures" (`api_meta.txt` L73961–73962). Screen, scheduled-only and platform-event-triggered flows are absent from that list, and there is no other declarative flow-test surface — see Gotcha 7. Components carry the `.flowtest` suffix, live in the `flowtests` folder, and exist from API version 55.0 (L73976–73980). The `testType` field (`FlowTestType`) is required from API version 66.0 and has one value, `WithAssertion` — "the automated comparison of the actual flow outcome with the user-defined expected outcome that assertions define" (L74042–74051). Run them with `sf flow run test`, the command the `flowtesting` namespace page names (`apexrefguide.txt` L158183–158187); see `devops/github-actions-for-salesforce`. **UNVERIFIED (2026-09-05):** the mapping from API version 66.0 to a named seasonal release, and the claim that FlowTest was record-triggered-only before it, are not stated in any corpus file — the guides give API version gates per field and nothing else.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- What business paths matter most: happy path, edge-case branches, validation failures, or external-action failures?
- Is the flow record-triggered, screen, scheduled, or auto-launched, and what test surface is appropriate for that type?
- Which parts of the behavior live outside the flow itself (Apex actions, custom LWC screen components, external integrations)?
- What test data does the org have? (Test Data Factory Apex class? Sample records in a scratch org?)
- Is the flow Draft or Active, and in which org? FlowTest is positioned as a pre-activation check (`api_meta.txt` L73961), so a flow already Active in production is being tested after the fact, not before.

## Questions to Ask Before Configuring

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| Which flow type is this — record-triggered, autolaunched, Data Cloud-triggered, screen, scheduled, or platform-event? | `FlowTest` covers only the first three (`api_meta.txt` L73961–73962), and `Flow.Interview.start()` only autolaunched and user-provisioning flows (`apexrefguide.txt` L158164–158177). Gotchas 7 and 10. | Decides the deliverable before any work starts: a `.flowtest-meta.xml`, an Apex driver, or a scripted manual pass with Jest at the component boundary. |
| If record-triggered: `Create`, `Update`, `CreateAndUpdate` or `Delete`? | `Update` needs both the before and after record image in the `Start` test point (`api_meta.txt` L74296–74320). Gotcha 8. | Tells you whether the test needs `InputTriggeringRecordUpdated` as well as `InputTriggeringRecordInitial`, and which field must differ between them. |
| What does each branch leave behind in a named variable or a record field? | Assertions fire only at `Start` and `Finish` (`api_meta.txt` L74143–74150). Gotcha 5. | Gives every branch an assertion target. "Nothing" is a finding: the flow needs a variable added before it can be tested at all. |
| Does the flow call invocable Apex, an External Service, or send email? | `isUseMockOuput` is "Reserved for future use" (`api_meta.txt` L74152) — nothing in a flow test is mocked. Gotcha 6. | Tells you which org may safely run the tests, and which behaviour has to move behind an invocable method so `HttpCalloutMock` can cover it. |
| Who runs this in production, and what is `runInMode` set to? | `DefaultMode` means launch context decides user vs system context (`api_meta.txt` L68374–68380); version selection also differs between a flow user and a flow admin (`apexrefguide.txt` L158178–158181). Gotcha 14. | Supplies the `System.runAs` subject and exposes whether the user-context path has ever executed outside an admin session. |
| Does the flow read configuration from a custom object? | Apex test data isolation "applies to all code running in test context" (`apexdev.txt` L40760–40761). Gotcha 11. | Tells you what `@TestSetup` must create — or that the configuration belongs in Custom Metadata, which the isolation rule exempts. |
| What does the release gate require today, and does the repo still ship `flowDefinitions/`? | Active version numbers in flow definitions override the `status` field in the flows (`api_meta.txt` L73925–73930). Gotcha 13, and the unsatisfiable-gate anti-pattern in `references/well-architected.md`. | Confirms the version you tested is the version users get, and catches a gate that cannot be met for screen flows. |

What a proper configuration adds over just doing it: a test suite shaped by these answers proves the branch a change touched, in the version that actually runs, for the user who actually runs it — where a suite written without them proves that one happy path once worked for an admin.

## Core Concepts

Good Flow testing starts with path thinking, not with clicking Debug first. The goal is to prove that the flow behaves correctly when inputs, branching, and failures vary. A happy-path-only test tells you almost nothing about how safe the automation really is in production.

### Flow Tests Need A Path Matrix

For any meaningful flow, start by listing the business outcomes that must be proven. That usually includes the main success path, one or more decision branches, and at least one failure or rejection path. The matrix drives your test data and tells you where declarative Flow Tests, Apex tests, or manual screen validation each belong.

**Example path matrix for a record-triggered flow on Case:**

| Input shape | Expected path | Expected outcome | Test type |
|---|---|---|---|
| Case.Priority = High, Account.Type = Enterprise | Enterprise escalation branch | Case.OwnerId set to enterprise queue | Flow Test |
| Case.Priority = High, Account.Type = SMB | SMB escalation branch | Case.OwnerId unchanged; notification sent | Flow Test |
| Case.Priority = Low | No-op branch | No changes | Flow Test |
| Case with invalid required field | Validation Rule fires | Save rolled back; Flow fault logged | Flow Test + manual UI verify |
| Case with duplicate detected | Duplicate Rule fires | Save blocked with user-facing message | Manual |
| Case saved via Bulk API 200-record batch | Happy path at scale | All 200 processed; no governor error | Apex test (bulkification check) |

### Debug Runs Are Diagnostic, Not Coverage

Debug mode is useful to inspect runtime behavior and investigate failures, but it is NOT the same as having repeatable automated coverage. Use debug runs to understand why something failed, then turn that understanding into a repeatable test asset where possible.

**Debug run is the right tool for:**
- First-time exploration of a flow's behavior
- Investigating a specific failure from Flow Interview Log
- Verifying a quick change didn't break the happy path
- Demoing the flow to a stakeholder

**Debug run is NOT sufficient for:**
- Production deploy readiness
- Regression safety on subsequent changes
- Bulk-safety verification
- Branch-coverage proof

### Custom Boundaries Need Their Own Tests

If the flow calls invocable Apex, depends on a custom LWC screen component, or hands off work to other automation, the Flow Test alone may not be enough. The flow should still be tested at the orchestration level, but the custom component or Apex boundary also needs focused tests at its own layer.

| Dependency | Flow-level test covers... | Additional test needed |
|---|---|---|
| Invocable Apex | That the flow calls it with the right inputs | Apex `@IsTest` class for the invocable method |
| Custom LWC screen component | That the flow renders the component | Jest test for the LWC's `validate()` + user interactions |
| HTTP callout via External Services | That the flow routes around callout result | Mock-based Apex test OR contract test against the external API |
| Platform Event publish | That the flow fires the publish call | Apex test subscribing to the event |
| Subflow | That the parent passes correct inputs | Separate Flow Test on the subflow |

### Fault Paths Must Be Intentional Test Cases

Testing only the success path leaves the most operationally important behavior unproven. Validation-rule errors, missing data, duplicate-rule failures, or external action failures should be part of the test plan when they are realistic outcomes.

A Flow Test's "expected fault" assertion:
- Configure inputs that WILL trigger a known failure (e.g. missing required field).
- Assert that the fault path fires (an assignment, a log creation, a notification).
- Verify the user-safe message doesn't contain raw `$Flow.FaultMessage`.
- Verify the error log captures the diagnostic detail.

## Common Patterns

### Pattern 1: Path Matrix Before Test Authoring

**When to use:** Any flow with more than one meaningful branch or outcome.

**Structure:** Build the matrix (as above) in a doc or spreadsheet. For each row:
1. Define the exact input shape (record field values, user context).
2. Define the expected path through the flow.
3. Define the expected outcome (assertions).
4. Tag the test type (Flow Test, Apex test, manual UI verify).

Authoring tests without the matrix usually produces one happy-path Flow Test and calls it done. The matrix forces coverage thinking first.

### Pattern 2: Pair Flow Tests With Boundary Tests

**When to use:** The flow interacts with Apex, custom screen LWCs, or external systems.

**Structure:**
```text
Flow Test (declarative):
  - Prove orchestration: flow runs, calls the boundary, receives expected return.

Apex @IsTest (for invocable Apex):
  - Prove boundary: given the same input the flow sends, produces the correct output.
  - Cover bulk signatures (List<T>, not single instances).

Jest test (for custom LWC):
  - Prove component: @api validate() returns correct isValid for sample inputs.
  - Prove dispatched events (FlowAttributeChangeEvent) fire with correct payload.
```

Neither layer alone is enough. Combined, they give confidence.

### Pattern 3: Explicit Fault-Path Test Cases

**When to use:** The flow can fail because of business validation, duplicate detection, or integration issues.

**Structure:** For every fault-route in the flow (per `flow/fault-handling` Patterns A/B/C/D), have at least one Flow Test that triggers the fault and asserts the route fires.

```text
Flow Test: "Fault path fires when DML validation blocks Update"
  Input: Case with field value that violates Validation Rule
  Expected assertions:
    - Flow reaches the fault branch
    - Application_Log__c record is created
    - User-safe message contains friendly copy
    - Raw $Flow.FaultMessage does NOT appear in user-visible output
```

### Pattern 4: Test Data Factory For Repeatable Setup

**When to use:** Flows that depend on complex data setups (multi-object relationships, specific role hierarchies, picklist values).

**Structure:** An Apex `@IsTest` `TestDataFactory` class creates the needed records — start from `templates/apex/tests/TestDataFactory.cls`, do not fork it. A `FlowTest` points at that class through `flowTestDataSources`, whose `dataSourceType` has one value, `ApexClass`, from API version 66.0 (`api_meta.txt` L74070–74090). Pair it with `isolatedObjectExternalKeys`, which names the fields that identify unique records in the isolated test data and explicitly excludes lookup fields (L74092–74128).

Alternative: a scratch-org seed script (SFDX tree export/import) that loads a canonical test dataset. Repeatable + CI-friendly.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Repeatable coverage for declarative branching | Flow Tests around a path matrix (Pattern 1) | Turns business paths into durable regression assets |
| Diagnose a failure quickly | Debug Run first, then convert insight to a test | Debug is diagnostic, not long-term coverage |
| Flow depends on invocable Apex or external logic | Pair Flow Tests with boundary tests (Pattern 2) | Flow doesn't own all behavior alone |
| Screen flow uses custom LWC components | Test both interview path AND component contract | Validation/UI behavior crosses the Flow boundary |
| Only happy path covered today | Add edge and fault cases next (Pattern 3) | Reliability risk usually lives outside the main path |
| Test needs complex multi-object setup | Use an Apex TestDataFactory (Pattern 4) | Repeatable, CI-friendly, version-controlled |
| Flow has thousands of expected records at bulk | Apex `@IsTest` with 200-record insert | Flow Tests don't stress-test bulk limits |

## Review Checklist

- [ ] A path matrix exists for success, branch, and failure scenarios.
- [ ] Test data is explicit and not dependent on existing org state.
- [ ] Fault-path behavior is covered where realistic failures exist.
- [ ] Custom screen components or Apex actions have tests at their own boundary.
- [ ] Debug runs are used to learn, not mistaken for repeatable coverage.
- [ ] The chosen test assets align with the flow type and production risk.
- [ ] Bulk behavior tested via Apex `@IsTest` if the flow fires on high-volume objects.
- [ ] Test-data factory or scratch-org seed script exists for the org's common test setups.

## Recommended Workflow

1. **Inventory the gap before designing anything.** Run
   `python3 skills/flow/flow-testing/scripts/check_flow_testing.py --manifest-dir force-app/main/default`.
   It reports Active flows with no `FlowTest` naming them, tests whose `flowApiName`
   resolves to no flow in the tree, tests with a `Start` point and no `Finish` assertions,
   test points with zero assertions, update-triggered tests missing the initial record
   image, and Apex classes touching `Flow.Interview` with no assertion. That output is the
   worklist; the path matrix below fills the gaps it names.
2. **Classify by flow type, then build the path matrix.** Answer the first question in the
   table above. Record-triggered, autolaunched and Data Cloud-triggered flows get
   `FlowTest` components; autolaunched flows may also get an Apex driver; everything else
   gets Jest plus a scripted manual pass. Then list the outcomes each branch must produce
   and the variable or field that proves it.
3. **Author the FlowTest pair from `references/metadata-examples.md`.** §2 is the
   happy-path shape — two test points, assertions on both `Start` and `Finish`, both record
   images for an update trigger, a `HasError` assertion proving the fault route stayed
   quiet. §3 is the negative path at the boundary value. One condition per assertion, each
   with an `errorMessage` naming the suspect element.
4. **Cover what FlowTest structurally cannot reach, in Apex.** §5 of the same file drives
   an autolaunched flow through `Flow.Interview` with input variables, asserts
   `getVariableValue` and then queries the record. Use it for bulk behaviour, user context
   via `System.runAs`, mocked callouts, and any flow type `FlowTest` does not list.
5. **Deploy in the order in `references/metadata-examples.md` and run both suites.** Objects,
   then flows as `Draft`, then `flowtests`, then Apex — `Flow.Interview.<FlowApiName>` will
   not compile before the flow exists. Then `sf flow run test` and
   `sf apex run test --class-names <YourFlowTestClass>`.
6. **Read `elementsNotCovered` from the deploy result, not a percentage.** Walk the list
   per element and classify each as a real gap or a structurally unreachable route, as in
   `references/examples.md` Example 3. Record the accepted ones with their reason.
7. **Re-run the checker and record what remains.** Fill in
   `templates/flow-testing-template.md` with the residual gaps and why each is accepted.

---

## Salesforce-Specific Gotchas

1. **Debug success is not regression coverage** — a one-time manual run does not protect future changes.
2. **Custom LWC screen components widen the test surface** — the Flow test and the component validation contract both matter.
3. **Fault handling needs its own test data** — failures rarely prove themselves unless data is arranged to trigger them intentionally.
4. **A flow can be correct while its boundary dependency is wrong** — orchestration coverage does not replace Apex or component tests.
5. **Flow Tests do NOT enforce coverage at deploy time** — unlike Apex. A flow can be deployed to production with zero tests. This is a discipline problem, not a tool problem.
6. **Admin-context testing hides user-context failures** — `System.runAs` plus a `with sharing` launching class on API version 62.0 or later is what makes an Apex-driven flow honour the running user's sharing (`apexrefguide.txt` L157958–157963). **UNVERIFIED (2026-09-05):** the corpus states nothing about which user context a `FlowTest` component executes in.
7. **There is no FlowTest for a screen flow at all** — the type covers record-triggered, autolaunched and Data Cloud-triggered flows only (`api_meta.txt` L73961–73962). Jest plus a scripted manual pass is the whole story there.
8. **A FlowTest exercises one interview** — the `Start` point takes a single `$Record` image per parameter type (`api_meta.txt` L74296–74320), so nothing about bulk behaviour is proven. Use an Apex test that inserts a realistic batch. **UNVERIFIED (2026-09-05):** the often-quoted "200 interviews per 200-record DML" ratio is not stated in `api_meta.txt` or `apexdev.txt`.
9. **Nothing inside a flow test is mocked** — `isUseMockOuput` is documented as "Reserved for future use" (`api_meta.txt` L74152), so an Apex action, External Services callout or email alert fires for real when the test runs.
10. **Test failures in Flow are harder to debug than Apex** — less tooling, less stack trace detail. Prefer clear test names and narrow scope per test.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Flow deployed to production with zero Flow Tests** → Flag as Critical. Must have at least happy-path + one fault-path test.
- **Happy path covered, no fault tests** → Flag as High. Failure behavior is where production incidents live.
- **Boundary dependency (Apex/LWC/HTTP) not tested at its own layer** → Flag as High. Orchestration coverage doesn't prove boundary correctness.
- **Test data inherited from org state rather than fabricated** → Flag as High. Tests break when the org changes.
- **Debug run cited as "the tests"** → Flag as Critical. Fundamental discipline gap.
- **Flow on high-volume object without bulk test (Apex)** → Flag as High. Bulk failure surfaces only in production.
- **Fault paths exist but have no corresponding Flow Test** → Flag as Medium. Specific, fixable gap.
- **Custom LWC screen component with no Jest tests** → Flag as Medium. Validation contract is unprovable.

## Output Artifacts

| Artifact | Description |
|---|---|
| Test matrix | Mapping of paths, inputs, expected outcomes, test types |
| Coverage review | Findings on missing path, fault, or boundary coverage |
| Test strategy | Recommendation across Flow Tests, debug usage, and boundary tests |
| Test-data plan | TestDataFactory class design or scratch-org seed approach |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | You are writing the artifacts: a record-triggered flow, its happy-path and negative-path `FlowTest` components, an autolaunched flow, the Apex `Flow.Interview` driver, `package.xml`, deploy order and the SOQL verification. |
| `references/gotchas.md` | A test is green and the flow is broken, or a test will not deploy. Fourteen documented platform behaviours with the guide line ranges. |
| `references/llm-anti-patterns.md` | You are reviewing generated test advice — eight failure modes, including Apex-driving a record-triggered flow and quoting a flow coverage percentage. |
| `references/examples.md` | You need a worked path matrix, the split between flow-level and component-level coverage, or the coverage-worklist reading of a deploy result. |
| `references/well-architected.md` | You are choosing between `FlowTest` and Apex as the driver, or need the sourced claim behind a statement in this package. |

## Related Skills

- **flow/fault-handling** — alongside this skill when failure behavior needs redesign as well as test coverage.
- **flow/screen-flows** — when the test strategy depends on interactive runtime UX and custom screen components.
- **flow/flow-bulkification** — when bulk-test coverage is the gap.
- **apex/trigger-framework** — when the flow's boundary is Apex and trigger-framework tests cover that side.
- **lwc/lwc-testing** — companion skill for Jest tests on custom LWC screen components.
- **flow/flow-governance** — owns the release rule ("FlowTest present before Active") and `Flow.settings`; this skill only produces the tests that rule asks for.
- **flow/record-triggered-flow-patterns** — owns `triggerType` / `recordTriggerType` selection and the guide's narrower availability wording; read it before arguing about which trigger type a test should target.
- **flow/flow-interview-debugging** — owns the debug-log side: which Workflow-category events exist and at which level they appear.
- **apex/test-data-factory-patterns** — how to extend `templates/apex/tests/TestDataFactory.cls` for custom objects without forking it.
