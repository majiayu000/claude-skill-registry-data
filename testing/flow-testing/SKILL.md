---
name: flow-testing
description: "Use when defining or reviewing test strategy for Salesforce Flow, including Flow Tests, debug runs, path coverage, test data, and explicit validation of fault paths and custom component behavior. Triggers: 'flow test tool', 'how do i test a flow', 'flow fault path testing', 'flow debug interview'. NOT for Apex unit testing or manual QA planning that is unrelated to Flow behavior."
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
inputs:
  - "which flow type is under test and which paths are business-critical"
  - "what test data is required for happy, edge, and failure scenarios"
  - "whether custom LWC components, Apex actions, or external dependencies are involved"
outputs:
  - "flow test strategy covering happy, edge, and fault paths"
  - "review findings for missing test coverage, weak data setup, or manual-only validation"
  - "guidance on combining Flow Tests, debug runs, and component-level tests where needed"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

Use this skill when a Flow works in a demo but nobody can yet prove it is safe to change. Flow testing is not one tool — it is a test STRATEGY that combines declarative Flow Tests where they fit, focused debug runs for diagnosis, deliberate test data, and extra coverage at custom component or Apex boundaries when the Flow itself is not the whole system.

Unlike Apex, Flow does not have a forced test-coverage gate at deploy time. This makes flow testing strictly a discipline problem, not a tooling problem. Teams that rely on "I clicked through it once in sandbox" as their coverage story are one change away from a production incident with no regression safety net. This skill exists to make that discipline concrete.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- What business paths matter most: happy path, edge-case branches, validation failures, or external-action failures?
- Is the flow record-triggered, screen, scheduled, or auto-launched, and what test surface is appropriate for that type?
- Which parts of the behavior live outside the flow itself (Apex actions, custom LWC screen components, external integrations)?
- What test data does the org have? (Test Data Factory Apex class? Sample records in a scratch org?)
- Is the Flow deployed to sandbox or prod? (Flow Tests work differently in each.)

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

**Structure:** An Apex `@IsTest` `TestDataFactory` class creates the needed records. Flow Tests use "Run Flow Debug" with the records fabricated via this factory (or via Connect Test Setup in sandbox).

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

## Well-Architected Pillar Mapping

- **Reliability** — every missing fault-path test is a reliability risk; every missing bulk test is a scalability-failure-as-reliability risk.
- **Operational Excellence** — test assets as regression safety nets; debug runs confused for coverage; lack of test-data discipline. OpsEx dominates this skill.

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

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; build the path matrix first
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **Debug success is not regression coverage** — a one-time manual run does not protect future changes.
2. **Custom LWC screen components widen the test surface** — the Flow test and the component validation contract both matter.
3. **Fault handling needs its own test data** — failures rarely prove themselves unless data is arranged to trigger them intentionally.
4. **A flow can be correct while its boundary dependency is wrong** — orchestration coverage does not replace Apex or component tests.
5. **Flow Tests do NOT enforce coverage at deploy time** — unlike Apex. A flow can be deployed to production with zero tests. This is a discipline problem, not a tool problem.
6. **Flow Tests run with the current user's permissions** — tests may pass in a System Admin's context but fail for the actual users. Test with `runAs()` equivalents or multiple user contexts.
7. **Screen flow tests can't fully automate custom LWC interaction** — manual steps inevitable for some scenarios; Jest fills the LWC gap.
8. **Record-triggered flow tests don't inherently cover bulk** — a 200-record Bulk API insert triggers 200 interviews; Flow Tests run one interview. Use Apex for bulk coverage.
9. **Mocking external callouts in Flow Tests is harder than in Apex** — External Services callouts typically require Apex test setup.
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

## Related Skills

- **flow/fault-handling** — alongside this skill when failure behavior needs redesign as well as test coverage.
- **flow/screen-flows** — when the test strategy depends on interactive runtime UX and custom screen components.
- **flow/flow-bulkification** — when bulk-test coverage is the gap.
- **apex/trigger-framework** — when the flow's boundary is Apex and trigger-framework tests cover that side.
- **lwc/lwc-testing** — companion skill for Jest tests on custom LWC screen components.
