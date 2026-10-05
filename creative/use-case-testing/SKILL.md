---
name: use-case-testing
description: >
  Apply this skill whenever you need to design test cases using Use Case Testing — a black-box
  test design technique that derives test cases from use case specifications. Use when given
  a use case specification (or equivalent: user story with acceptance criteria, feature with
  defined actor-system interactions), and the goal is to ensure the system correctly handles
  all flows: the main success scenario, alternate flows, and exception flows. Triggers include:
  "design test cases from use case", "test this user story", "test this feature end-to-end",
  "use case testing", "UC", "actor interaction", "flow testing", or any request to test a
  feature where behavior is described as a sequence of actor-system interactions leading to
  a defined goal.
---

# Use Case Testing Skill

## Overview

**Use Case Testing** is a **black-box test design technique** defined in ISTQB Foundation Level Syllabus where test cases are derived from use case specifications. A use case describes an interaction between one or more **actors** (human users or external systems) and the **system under test (SUT)** to achieve a specific **goal**.

The technique systematically derives test cases by identifying all meaningful paths through the use case — the **main flow** (the happy path) and all **alternate flows** (deviations due to optional choices, validation failures, or exception conditions) — then combining them into **scenarios** that represent complete end-to-end journeys from the use case's starting point to an endpoint.

**Core purpose:** Verify that the system correctly delivers business value to actors through every meaningful path — not just the happy path — ensuring all flows are exercised and all preconditions/postconditions are verified.

**Role of Use Case Testing vs. other techniques:** Use Case Testing is responsible for identifying **which flows and paths to test**. It does not design the specific data values used within those paths. Once scenarios are identified, use Domain Testing (EP/BVA) to select specific test data for input fields, and Decision Table Testing for steps with multiple simultaneous conditions. These techniques are complementary: Use Case Testing provides the flow structure; other techniques populate the data.

→ For full theoretical background, see [`resources/theory.md`](resources/theory.md).

## Invoke Syntax

```
/use-case-testing [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                         | Behavior                                                                                                                     |
| ---------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Default (conversation) | `/use-case-testing`                            | All analysis and test cases printed inline in the conversation as Markdown                                                   |
| File output            | `/use-case-testing --file="path/to/output.md"` | All output (Flow Analysis, Scenario Matrix, Test Case Suite) written to the specified file. AI confirms path before writing. |

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/use-case-testing --file="path/to/output.md"` then paste the requirements.

## When to Use

- A **use case specification** (UC spec) exists with defined: actor(s), preconditions, main flow, alternate flows, postconditions.
- A **user story with acceptance criteria** that describes actor-system interactions toward a goal (can be treated as an informal use case spec).
- Testing a **feature end-to-end** where the behavior is defined as a sequence of actor-system interactions.
- When the goal is to verify **complete business flows** — not isolated field validation or individual API endpoints.
- When **integration between system components** needs to be exercised through a realistic actor journey.
- As the primary technique for **acceptance testing** — verifying the system delivers the intended business value.

**Key signal:** If the requirement describes _what an actor does step-by-step and what the system does in response_, Use Case Testing is the right technique.

## When NOT to Use

- No use case specification or equivalent exists — use requirements cannot be mapped to actor-goal-flow structure → clarify requirements first.
- The requirement describes **only input field constraints** with no multi-step interaction → use **Domain Testing** instead.
- The requirement describes **combinations of simultaneous conditions** with no sequence → use **Decision Table Testing** instead.
- The requirement describes **system state transitions over time** → use **State Transition Testing** instead.
- **Do not** use Use Case Testing as a complete test strategy alone — combine with Domain Testing for input data selection within steps, and Error Guessing for additional negative paths.

## Inputs Required

Before applying this skill, you must have:

1. **Use Case Specification** (or equivalent) containing:
   - Use Case ID and Name
   - Actor(s)
   - Preconditions
   - Main Flow (step-by-step)
   - Alternate Flows (each referencing the Main Flow step where deviation occurs)
   - Postconditions
   - Business Rules / Constraints
2. **Business Rules (BR)** referenced within the use case
3. **System context:** what layer is being tested (UI, API, or both); what backend state changes are expected
4. _(Optional but valuable)_ Historical defect data for the feature; risk information for flow prioritization

## Core Principles

1. **Actor-goal orientation:** Every use case has exactly one actor initiating it and one goal being pursued. Test cases must be designed from the actor's perspective — verifying the system delivers (or correctly refuses to deliver) the goal.
2. **Flow completeness:** The main flow and every identified alternate flow must have at least one test scenario covering it. No alternate flow may be silently omitted.
3. **Scenario = complete path:** Every scenario traces a complete path from the use case's starting point to an endpoint. There are no partial paths — a scenario either reaches a success endpoint or a defined failure/rejection endpoint.
4. **Preconditions are mandatory:** Every test case must specify exact preconditions — the system state required before the first actor action. Without preconditions, test cases are non-deterministic.
5. **Postconditions are verified assertions:** Postconditions are not narrative descriptions — they are test assertions that must be explicitly verified, including backend state (database records, audit logs, email delivery) not just UI responses.
6. **Flow structure before data:** Identify all scenarios (paths) first, then apply data selection techniques. Do not let data concerns drive flow identification.
7. **Alternate flows require explicit triggering data:** Each alternate flow must be exercised with specific test data or preconditions that reliably force the system down that path — not hoped to be reached by chance.

## Design Process

Follow these steps sequentially. Do not skip any steps.

### Step 1 — Parse and Validate the Use Case Specification

Read the use case specification thoroughly. For each section, perform validation:

- **Actor(s):** Is every actor identified? Could the same use case be initiated by different actor types with different behavior?
- **Preconditions:** Are they specific and testable? Can each be set up reliably before test execution? If a precondition is vague ("system is operational"), clarify what observable condition confirms it.
- **Main Flow:** Is each step clearly defined as actor action or system response? Are there any implicit steps (actions the spec assumes but does not state)?
- **Alternate Flows:** Does each alternate flow reference the specific Main Flow step where it branches? Does it define an endpoint (does it rejoin Main Flow, or terminate)? Are any alternate flows missing — conditions the system must handle but the spec does not document?
- **Business Rules / Constraints:** Are they complete? Do they define behavior for boundary conditions?
- **Postconditions:** Do they include backend state verification requirements (database changes, audit logs, notifications)?

Document all gaps and ambiguities found. Raise them with the product owner or BA before proceeding to test design.

→ See [`resources/spec-and-flow-guide.md`](resources/spec-and-flow-guide.md) — **Part 1** for validation checklist and common spec gaps.

### Step 2 — Analyze and Enumerate All Flows

Produce a complete **Flow Inventory**:

1. **Main Flow:** Number each step explicitly (Step 1, Step 2, Step 3...). Identify the single success endpoint.
2. **Alternate Flows:** For each alternate flow:
   - Assign an ID (e.g., AF-1, AF-2, AF-3)
   - Identify the Main Flow step it branches from (e.g., "Branches from Step 2")
   - Classify as **Optional Flow** (valid but non-default path) or **Exception Flow** (error, rule violation, system failure)
   - Identify the endpoint: Rejoins Main Flow at step N / Terminates use case / Loops back
3. **Discover hidden alternate flows:** Look for:
   - Every step in the Main Flow where the system performs a conditional action
   - Every Business Rule that implies a rejection case
   - Every postcondition that implies multiple possible states
   - System/network failure scenarios at each step
   - Concurrent access scenarios if applicable

→ See [`resources/spec-and-flow-guide.md`](resources/spec-and-flow-guide.md) — **Part 2** for flow enumeration patterns and hidden flow discovery.

### Step 3 — Build the Scenario Matrix

Construct the **Scenario Matrix** — a systematic enumeration of all meaningful path combinations:

**Fundamental rule:** Every scenario must:

- Begin with the Main Flow
- Incorporate one or more alternate flows at the points where they branch
- Terminate at a defined endpoint (success or defined failure)

**Scenario construction procedure:**

1. S1 always = Main Flow only (the happy path)
2. For each alternate flow AFn, create a scenario = Main Flow + AFn
3. For combinations where alternate flows interact (one alternate flow enabling or blocking another), enumerate the relevant combinations
4. Apply **risk-based selection** to prioritize: not all combinations need to be tested if the risk is low

**Combinatorial explosion mitigation:** When the use case has many alternate flows, apply:

- **Risk-based path selection:** Prioritize flows by probability of defect × business impact. High-risk flows get individual scenarios; low-risk flows may be bundled.
- **Pairwise coverage:** Ensure every pair of alternate flows is covered in at least one scenario — mathematically reduces the scenario count while maintaining high defect detection.

→ See [`resources/scenario-matrix-guide.md`](resources/scenario-matrix-guide.md) for construction procedure and combinatorial reduction strategies.

### Step 4 — Design Test Cases from Scenarios

Translate each scenario into one or more executable test cases:

**Flow → Test Case mapping:**

- One scenario = one or more test cases (multiple test cases when the same path must be exercised with different test data to cover different input partitions)
- Scenarios covering the same path with the same data must not be duplicated

**For each test case, specify:**

- **Preconditions:** Exact system state required. Include: data setup (which records must exist in DB), system state (feature flags, configuration), actor state (logged in as which role).
- **Steps:** Sequential actor actions and expected system responses per step — not just final result.
- **Test data:** Specific input values for each data-entry step. Derived using Domain Testing (EP/BVA) to select the most revealing values for the path being exercised.
- **Expected results per step:** Observable system response after each actor action — not just the final state.
- **Postconditions:** All backend state assertions to verify after the final step: database record changes, audit log entries, email/notification delivery, state of related entities.
- **Alternate flow trigger:** For non-happy-path scenarios, document exactly what input or condition forces the system into the alternate flow.

→ Use [`resources/output-template.md`](resources/output-template.md) for test case format.

### Step 5 — Apply Domain Testing for Test Data Selection

For each test case that involves data entry steps:

- Apply **Equivalence Partitioning** to identify valid and invalid data classes for each input field.
- Apply **BVA** to select specific values at boundaries of ordered classes.
- Select the data value that best exercises the intended path: for valid paths, use a nominal valid value; for alternate flows triggered by invalid data, use the specific invalid class representative or boundary value.

This step **refines test data within scenarios already identified** — it does not add new scenarios. If applying EP/BVA reveals a data class that would exercise a _different_ alternate flow not yet in the scenario matrix, add that flow to the matrix first (Step 3), then design its test case here.

### Step 6 — Verify Postconditions Coverage

Review every test case for postcondition completeness:

For each test case, confirm:

- UI/API response assertion is specified
- Database state assertion is specified (if the use case modifies data)
- Audit/logging assertion is specified (if the use case spec lists audit events as a postcondition)
- Related entity state assertion is specified (if the use case affects more than one entity)
- Notification/email assertion is specified (if applicable)

**Junior tester trap:** Only verifying the UI response and ignoring backend state. Use Case Testing requires verifying all postconditions stated in the spec, not just what is visible in the UI.

### Step 7 — Review Against Quality Checklists

Before finalizing, verify the test suite against the **Test Case Quality Checklist** in [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Design Rules

| Rule                               | Description                                                                                   |
| ---------------------------------- | --------------------------------------------------------------------------------------------- |
| **Main Flow always first**         | S1 must be the Main Flow only; no alternate flows are injected into S1                        |
| **Every alternate flow covered**   | Every identified alternate flow must appear in at least one scenario                          |
| **Scenario = complete path**       | No partial paths — every scenario has a start and an end point                                |
| **Precondition is mandatory**      | Every test case must specify the exact state the system must be in before execution           |
| **Postconditions are assertions**  | Every postcondition in the use case spec must have an explicit test assertion                 |
| **Alternate flow needs a trigger** | Every non-happy-path test case must specify what input or condition forces the alternate flow |
| **Flow structure before data**     | Complete the Scenario Matrix before selecting test data                                       |
| **No silent omission of flows**    | Low-risk flows may be deprioritized but must be documented as acknowledged                    |

## Anti-Patterns

→ **Full detail:** [`resources/anti-patterns.md`](resources/anti-patterns.md)

**Critical anti-patterns:**

- **Testing only the Main Flow (happy path only)** — the most common failure; alternate flows are where most defects live
- **Designing test cases without a Scenario Matrix** — ad hoc scenario selection misses combinations and produces no coverage evidence
- **Missing preconditions** — test cases that do not specify system state before execution are non-deterministic and non-reproducible
- **Verifying only UI response, ignoring postconditions** — backend state changes (DB, audit log, emails) are unchecked; integration defects are invisible
- **Confusing alternate flow trigger with expected result** — the trigger is what forces the path; the expected result is what the system should do in response
- **Treating every alternate flow combination as a required scenario** — combinatorial explosion without risk-based selection; thousands of scenarios for no proportional quality gain

## Best Practices

→ **Full detail:** [`resources/best-practices.md`](resources/best-practices.md)

**Key best practices:**

- Validate the use case spec before designing tests — gaps in the spec become gaps in the test suite.
- Discover hidden alternate flows by asking "what if?" at every Main Flow step.
- Apply risk-based prioritization to the Scenario Matrix — not all alternate flow combinations need testing.
- Always verify all postconditions — use DB queries, log checks, and notification verification in test assertions.
- Use Domain Testing (EP/BVA) to select test data for each scenario's input steps — do not choose data arbitrarily.
- Maintain a Requirements Traceability Matrix (RTM) linking: BR → Use Case → Scenario → Test Case → Defect.

## Process Quality Checklist

_Use this to verify the design methodology was applied correctly._

- [ ] Use case specification was validated before test design (all fields present, no vague preconditions, all alternate flows have defined endpoints).
- [ ] All gaps and ambiguities in the spec were raised and resolved or documented before proceeding.
- [ ] Complete Flow Inventory produced: main flow steps numbered, all alternate flows identified and classified (optional vs. exception).
- [ ] Hidden alternate flows were actively searched for at each main flow step.
- [ ] Scenario Matrix constructed before writing any test case.
- [ ] S1 = Main Flow only (no alternate flows injected).
- [ ] Every alternate flow appears in at least one scenario.
- [ ] Risk-based prioritization applied to scenario selection — low-risk combinations documented as acknowledged if not tested.
- [ ] Alternate flow trigger specified for every non-happy-path test case.
- [ ] Domain Testing (EP/BVA) applied to select test data for each data-entry step.
- [ ] All postconditions from the use case spec have explicit test assertions (not just UI assertions).

→ For the full **Process Quality Checklist** should be verified, see [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Common Rationalizations to Reject

- _"The happy path works — the alternate flows are obvious edge cases"_ → Alternate flows are where most production defects are found; "obvious" is not a testing criterion
- _"We don't have time to test all the scenarios"_ → Apply risk-based selection and document what is being skipped — do not silently omit flows
- _"If the UI shows success, the test passes"_ → Postconditions require backend verification; UI success does not guarantee database consistency, audit trail, or notification delivery
- _"The precondition is 'the system is running'"_ → Preconditions must be specific and verifiable; set up exact data state before each test
- _"I'll figure out the test data when I execute"_ → Test data must be designed before execution; ad hoc data selection produces inconsistent results and misses the data-driven alternate flows

## Red Flags

Stop and re-evaluate if you observe:

- The Scenario Matrix has only one scenario (S1 = Main Flow) — alternate flows were not analyzed.
- A test case has no precondition or has "system is operational" as the precondition — not executable.
- Expected result is only "system shows success message" with no backend assertions — postconditions not verified.
- An alternate flow in the use case spec has zero corresponding scenarios — coverage gap.
- All test cases use the same test data — Domain Testing was not applied; specific paths may not be reliably triggered.

## Output

The design process produces:

1. **Flow Inventory** — numbered main flow steps; all alternate flows with classification, branching point, and endpoint
2. **Scenario Matrix** — all scenarios with path composition and priority
3. **Test Case Suite** — using the template in [`resources/output-template.md`](resources/output-template.md)
4. _(Recommended)_ **Requirements Traceability Matrix (RTM)** — mapping BR → Use Case → Scenario → Test Case

## Examples

→ [`examples/online-purchase.md`](examples/online-purchase.md) — E-commerce online purchase use case: complete UC spec, flow inventory, scenario matrix with risk-based selection, full test case suite with preconditions, data selection rationale, and postcondition assertions
