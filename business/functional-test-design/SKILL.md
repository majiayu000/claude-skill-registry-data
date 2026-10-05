---
name: functional-test-design
description: >
  Apply this skill whenever you need to design test cases for functional testing of any
  feature, requirement, or system behavior. This is the parent skill that routes to the
  correct black-box or experience-based test design technique based on the nature of the
  requirement. Triggers include: "design test cases", "write test cases", "how do I test
  this", "test this feature", "test this requirement", "test this API", "test this flow",
  "test this business rule", or any request to systematically design a test suite for a
  functional requirement — regardless of the specific technique needed. If you know which
  sub-skill to use, invoke that sub-skill directly instead.
---

# Functional Test Design Skill

## Overview

**Functional Test Design** is the discipline of systematically deriving test cases from functional requirements and business rules — ensuring that what is tested is both **sufficient** (no meaningful defect-prone area left uncovered) and **efficient** (no redundant test cases wasting execution resources).

This skill is the **parent router** for five specialized test design techniques, each targeting a different class of functional requirement. The techniques are grounded in ISTQB Foundation Level and industry practice:

| Technique                     | ISTQB Classification               | Primary Focus                                                                                    |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Domain Testing (EP + BVA)** | Black-Box                          | Input/output value ranges, formats, and classes                                                  |
| **Decision Table Testing**    | Black-Box                          | Multiple interacting conditions producing different outcomes                                     |
| **State Transition Testing**  | Black-Box                          | System behavior that depends on prior history (states)                                           |
| **Use Case Testing**          | Black-Box                          | End-to-end actor-system interaction flows                                                        |
| **Error Guessing**            | Experience-Based                   | Supplementary defect-targeted cases based on knowledge                                           |
| **Pairwise Testing**          | Combinatorial (reduction strategy) | Reducing an explosive number of combinations to a manageable set while maintaining pair coverage |

**Note on Pairwise Testing:** Pairwise Testing is not a standalone primary technique — it is a combinatorial reduction strategy applied when the output of Decision Table Testing or Use Case Testing produces more combinations than are feasible to test. It does not have its own sub-skill; it is applied as an optimization step within those techniques.

**How to use this skill:**

1. Read the requirement and identify its primary characteristic (input constraints? multiple conditions? state-dependent behavior? actor flow?).
2. Use the **Technique Selection Guide** below to identify the right sub-skill(s).
3. Invoke the selected sub-skill directly with the requirement.

In practice, most features require **more than one technique** applied in combination. The combination guidance in this skill ensures techniques complement rather than duplicate each other.

## Invoke Syntax

```
/functional-test-design [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                               | Behavior                                                                                    |
| ---------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Default (conversation) | `/functional-test-design`                            | AI analyzes the requirement, selects the appropriate sub-skill(s), and executes them inline |
| File output            | `/functional-test-design --file="path/to/output.md"` | All output written to the specified file. AI confirms path before writing.                  |

**Direct sub-skill invocation (preferred when technique is known):**

```
/domain-testing [--file="path/to/output.md"]
/decision-table-testing [--file="path/to/output.md"]
/state-transition-testing [--file="path/to/output.md"]
/use-case-testing [--file="path/to/output.md"]
/error-guessing [--file="path/to/output.md"]
```

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- When multiple techniques are needed, each produces its own output section or file.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/functional-test-design --file="path/to/output.md"` then paste the requirements.

## Technique Selection Guide

Use this guide to identify which sub-skill(s) to apply to a given requirement. Read the primary characteristic of the requirement, then select.

### Signal 1: Input/Output Value Constraints → Domain Testing (EP + BVA)

**Requirement signals:**

- Defines valid ranges: "must be between X and Y", "must not exceed Z", "minimum N characters"
- Defines valid formats: "must match pattern", "must be alphanumeric", "must be a valid date"
- Defines valid sets: "must be one of: A, B, C"
- Defines mandatory/optional fields
- Any BR with the words: range, length, format, minimum, maximum, at least, at most

**Apply:** [`domain-testing`](domain-testing/SKILL.md) — EP + BVA for all constrained input/output variables

**Example signals:**

- "Age must be between 18 and 60" → Domain Testing
- "Password must be 8–30 characters, contain uppercase, lowercase, digit, and special character" → Domain Testing
- "Product code must start with 2 uppercase letters followed by 4–10 alphanumeric characters" → Domain Testing

### Signal 2: Multiple Conditions Controlling Different Outcomes → Decision Table Testing

**Requirement signals:**

- Two or more conditions interact to determine what the system does
- Business rules contain "if-then-else" or "and/or" logic
- Different combinations of inputs produce different outputs
- Eligibility, pricing, discount, routing, or access control logic
- The same input can produce different results depending on other flags or states

**Apply:** [`decision-table-testing`](decision-table-testing/SKILL.md) — systematic enumeration of all condition combinations

**Example signals:**

- "New customers get 15% off; loyalty members get 10%; coupons add 20% — but coupons cannot be combined with new customer discounts" → Decision Table Testing
- "Loan eligibility depends on age, employment status, and credit score" → Decision Table Testing
- "Access level is determined by role AND subscription tier AND account status" → Decision Table Testing

### Signal 3: System Behavior Depends on Prior History (States) → State Transition Testing

**Requirement signals:**

- System has named statuses, lifecycle stages, or modes
- The same action produces different results depending on what happened previously
- Requirements use lifecycle language: "can only do X after Y", "once in state Z, W is not allowed"
- Object/entity has a lifecycle: account statuses, order statuses, session states, device modes
- Requirements describe workflows with defined entry/exit conditions

**Apply:** [`state-transition-testing`](state-transition-testing/SKILL.md) — FSM modeling, STD + STT, valid and invalid transition coverage

**Example signals:**

- "An order can be Confirmed only when in Pending status; a Shipped order cannot be Cancelled" → State Transition Testing
- "After 3 failed login attempts, the account is Locked; a Locked account cannot be Logged In without an admin unlock" → State Transition Testing
- "A subscription moves from Trial → Active → Suspended → Cancelled; transitions are event-driven" → State Transition Testing

### Signal 4: Actor-System Interaction Flow Toward a Goal → Use Case Testing

**Requirement signals:**

- Requirement describes a sequence of steps an actor takes to achieve a goal
- Feature has a defined main flow (happy path) and alternate/exception flows
- Use case specification or user story with acceptance criteria is available
- Testing a complete end-to-end feature rather than an isolated field or rule
- Requirement describes integration between multiple system components through a user journey

**Apply:** [`use-case-testing`](use-case-testing/SKILL.md) — flow analysis, scenario matrix, path-based test cases

**Example signals:**

- "User registers, verifies email, logs in, adds items to cart, and completes purchase" → Use Case Testing
- "Loan officer submits application → system validates → underwriter reviews → decision issued" → Use Case Testing
- "Patient books appointment → receives confirmation → attends → receives follow-up" → Use Case Testing

### Signal 5: Supplementary Defect-Targeted Cases → Error Guessing

**Requirement signals:**

- Systematic techniques have been applied and a complete test suite exists
- Tester has domain knowledge, historical defect data, or implementation knowledge about the feature
- Review of the test suite reveals gaps that systematic rules cannot address
- The feature involves: complex integrations, third-party services, concurrency, configuration-dependent behavior, or known defect-prone constructs
- The question is "what else might go wrong?" rather than "what does the spec require?"

**Apply:** [`error-guessing`](error-guessing/SKILL.md) — structured Fault Attack using error taxonomy + historical data

**Important:** Error Guessing is always supplementary. It is applied **after** systematic techniques have been completed, never instead of them.

**Example signals:**

- "After designing domain and use case tests for the payment flow, what else should we test?" → Error Guessing
- "We've had bugs before with null handling and currency rounding — let's target those" → Error Guessing
- "The API has a new third-party integration — what failure modes should we cover beyond the spec?" → Error Guessing

### Signal 6: Too Many Combinations to Test in Full → Pairwise Reduction

**Requirement signals:**

- Decision Table Testing has been applied to a feature with 5+ conditions, and the reduced table still contains more rules than are feasible to execute
- Use Case Testing has produced more alternate flow combinations than can be tested in the available time, after impossibility pruning
- Configuration testing with multiple independent variables (OS × browser × screen size × locale) where full coverage is impractical
- The question is "how do we reduce the test count further without losing meaningful coverage?" — after formal reduction has already been applied

**Apply:** Pairwise Testing as a **reduction strategy on top of the existing technique's output**, not as a replacement for the primary technique.

**How it works:** Rather than testing all N-way combinations (every possible tuple of all variables), pairwise ensures that every **pair** of values from any two variables appears in at least one test case. Empirical research (Kuhn, Kacker, Lei — NIST) shows that most software failures are triggered by interactions between at most 2 variables, making pairwise coverage highly efficient for combinatorial scenarios.

**When NOT to apply Pairwise:**

- When the full reduced Decision Table is already manageable (≤ 16 rules) — formal reduction is sufficient; pairwise adds no value
- When all alternate flow combinations are logically necessary (i.e., no impossibility pruning was possible and risk-based selection has been applied) — apply risk-based deprioritization instead
- As a substitute for building the full Decision Table first — pairwise reduces an existing set; it does not replace formal derivation

**Example signals:**

- "Decision Table has 6 conditions → 64 rules → after reduction still 28 rules — we need to cut further" → Apply Pairwise on the 28 remaining rules
- "Use Case Testing produced 15 valid scenario combinations — we can only run 8" → Apply Pairwise to select the 8 that cover every pair of alternate flows
- "We need to test this feature on 4 OS × 3 browsers × 2 screen sizes × 3 locales = 72 configurations" → Apply Pairwise to reduce to ~12 configurations

## When to Use This Parent Skill

Use `/functional-test-design` (this parent skill) when:

- The requirement is complex and it is unclear which technique to apply first
- The requirement clearly needs multiple techniques and you want AI to orchestrate them in the correct order
- You want a complete test strategy for a feature rather than a single-technique test suite

Use a **sub-skill directly** when:

- You already know which technique applies (most common case after some experience)
- You are testing a specific, well-scoped requirement that clearly maps to one technique
- You want to invoke a specific technique without routing overhead

## When NOT to Use Any Sub-Skill

- **Requirements are unclear or contradictory** → Clarify requirements first; test design on ambiguous specs produces test cases that cannot be evaluated
- **No requirements exist** → Exploratory testing or specification-first conversations are needed before test design
- **Writing automated test code** → These skills design test cases (what to test and what to expect); implementation is separate
- **Performance, security, or compatibility testing** → These require different technique families; functional test design techniques are not sufficient as a primary strategy for these test types (though they may contribute to workload models or attack surfaces)

## Sub-Skills Reference

### [`domain-testing`](domain-testing/SKILL.md)

- **Technique:** Equivalence Partitioning (EP) + Boundary Value Analysis (BVA)
- **ISTQB:** Black-Box Test Design Technique
- **Use when:** Any variable has defined constraints — range, length, format, valid set
- **Output:** Variable Inventory Table → Equivalence Class Table → Test Case Suite
- **Key principle:** One representative per class is sufficient; boundaries are highest risk
- **Invoke:** `/domain-testing`

### [`decision-table-testing`](decision-table-testing/SKILL.md)

- **Technique:** Decision Table Testing
- **ISTQB:** Black-Box Test Design Technique
- **Use when:** 2+ conditions interact to produce different outcomes
- **Output:** Conditions & Actions List → Full Table → Reduced Table → Test Case Suite
- **Key principle:** Build the full table before reducing; one rule = one test case after reduction
- **Invoke:** `/decision-table-testing`

### [`state-transition`](state-transition-testing/SKILL.md)

- **Technique:** State Transition Testing
- **ISTQB:** Black-Box Test Design Technique
- **Use when:** System behavior depends on its current state (prior history matters)
- **Output:** FSM Component List → STD → STT → Coverage Plan → Test Case Suite
- **Key principle:** STD shows valid transitions; STT exposes invalid ones — both are required
- **Invoke:** `/state-transition-testing`

### [`use-case-testing`](use-case-testing/SKILL.md)

- **Technique:** Use Case Testing
- **ISTQB:** Black-Box Test Design Technique
- **Use when:** Testing complete actor-system interaction flows toward a defined goal
- **Output:** Flow Inventory → Scenario Matrix → Test Case Suite → RTM
- **Key principle:** Flow structure first (which paths), then data selection (which values per path)
- **Invoke:** `/use-case-testing`

### [`error-guessing`](error-guessing/SKILL.md)

- **Technique:** Error Guessing (Fault Attack)
- **ISTQB:** Experience-Based Test Design Technique
- **Use when:** Supplementing a complete systematic test suite with defect-targeted cases
- **Output:** Fault List (by category and priority) → Supplementary Test Case Suite
- **Key principle:** Structured guessing via error taxonomy; always supplements, never replaces systematic techniques
- **Invoke:** `/error-guessing`

## Technique Combination Patterns

Most real features require more than one technique. Apply them in this order:

### Pattern 1: Field Validation + Business Logic

**Applies to:** Forms, APIs, or endpoints with both input constraints and conditional processing rules

```
Step 1: /domain-testing          → test data classes and boundaries for each input field
Step 2: /decision-table-testing  → test combinations of conditions that control processing outcomes
Step 3: /error-guessing          → supplement with defect-targeted cases
```

**Example:** A loan application form where each field has constraints (Domain Testing) and eligibility depends on multiple fields in combination (Decision Table Testing).

### Pattern 2: Stateful Feature with Input Validation

**Applies to:** Features with lifecycle states where inputs within each state also have constraints

```
Step 1: /state-transition-testing  → test valid/invalid transitions across states
Step 2: /domain-testing            → test input value constraints within specific states/events
Step 3: /error-guessing            → supplement with defect-targeted cases
```

**Example:** A bank account with states (Active, Suspended, Closed) where the Withdraw event also has guard conditions involving amount ranges (Domain Testing within the guard).

### Pattern 3: End-to-End Flow with Data Variations

**Applies to:** Complete user journeys where each step also involves field-level data entry

```
Step 1: /use-case-testing  → identify all flows (main + alternate) and build scenario matrix
Step 2: /domain-testing    → select specific test data values for each data-entry step in each scenario
Step 3: /error-guessing    → supplement with integration failure modes and edge cases
```

**Example:** An e-commerce checkout flow (Use Case Testing for the paths) where each step has field-level constraints like address format and payment card format (Domain Testing for the data).

### Pattern 4: Complex Business Rules Embedded in a Flow

**Applies to:** Use cases where one or more steps involve multi-condition business logic

```
Step 1: /use-case-testing        → identify all flows and scenarios
Step 2: /decision-table-testing  → for steps with multi-condition logic, enumerate all rule combinations
Step 3: /domain-testing          → for steps with input constraints, derive boundary test data
Step 4: /error-guessing          → supplement
```

**Example:** An insurance claim flow (Use Case Testing) where the "Assess Eligibility" step involves multiple conditions (Decision Table Testing) and the claim amount has numeric constraints (Domain Testing).

### Pattern 5: Supplementary-Only

**Applies to:** An existing test suite that needs gap analysis and additional defect-targeted cases

```
Step 1: Review existing test suite (what is already covered)
Step 2: /error-guessing  → identify and test gaps using structured Fault Attack
```

### Pattern 6: Decision Table with Combinatorial Explosion

**Applies to:** Features with 5+ conditions where Decision Table reduction still produces too many rules to execute feasibly

```
Step 1: /decision-table-testing   → build full table, apply formal reduction (impossible rules + Don't Care)
Step 2: Apply Pairwise reduction  → if reduced table still exceeds feasible test count, apply pairwise coverage to select the minimum set of rules that covers every pair of condition values
Step 3: /domain-testing           → select boundary values for range-based conditions
Step 4: /error-guessing           → supplement with high-risk defect-targeted cases
```

**When to apply Step 2:** Only after formal Decision Table reduction has been completed and the result is still impractical. Pairwise is not applied to the full table — it is applied to the already-reduced set.

**Pairwise reduction procedure for Decision Table:**

1. List all conditions and their values in the reduced table.
2. Generate a pairwise covering array (can be done manually for small sets, or using a tool such as PICT, AllPairs, or JCUnit for larger sets).
3. Each row in the covering array = one test case; verify all remaining rules from the reduced table are covered by at least one row.
4. Document which original rules are covered by each test case for traceability.

**Example:** A product configuration feature with 6 conditions (Plan × Region × User Role × Feature Flag × Language × Tier) → 2⁶ = 64 full combinations → ~15 rules after formal reduction → 8 test cases via pairwise, covering all 15 pairs of condition values.

### Pattern 7: Use Case Testing with Large Alternate Flow Combinations

**Applies to:** Use cases with 6+ alternate flows where the scenario matrix, after impossibility pruning, still contains more combinations than can be tested in the available cycle

```
Step 1: /use-case-testing         → build full scenario matrix; prune impossible combinations; apply risk-based prioritization
Step 2: Apply Pairwise reduction  → if remaining scenarios exceed capacity after risk-based selection, apply pairwise to ensure every pair of alternate flows appears in at least one scenario
Step 3: /domain-testing           → select test data for data-entry steps in each scenario
Step 4: /error-guessing           → supplement with integration failure modes
```

**When to apply Step 2:** Only after risk-based prioritization has been applied and the remaining scenario count is still too large. Pairwise is the last resort before accepting acknowledged gaps.

**Relationship to Use Case Testing's built-in pairwise guidance:** The Use Case Testing sub-skill already mentions pairwise as a combinatorial reduction strategy in its Scenario Matrix guide. This pattern makes the application explicit in the context of the parent skill's orchestration.

**Example:** An online purchase use case with 8 alternate flows → 256 theoretical combinations → 180 logically possible → 40 after impossibility pruning → 15 after risk-based selection → 10 test cases via pairwise ensuring every pair of alternate flows is exercised together at least once.

## Technique Interaction Rules

These rules govern how techniques interact when used together to prevent duplication and ensure each technique adds unique value:

| Rule                                                   | Description                                                                                                                                                                                                              |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Domain Testing owns data values**                    | When combined with Decision Table or Use Case Testing, Domain Testing is responsible for selecting specific input values; other techniques are responsible for selecting which combinations or paths to exercise         |
| **Decision Table owns condition combinations**         | When combined with Domain Testing, Decision Table identifies which combinations to test; Domain Testing selects the specific data values within each condition class                                                     |
| **State Transition owns path sequences**               | When combined with Domain Testing, State Transition identifies which state × event paths to test; Domain Testing selects specific values for guard condition parameters                                                  |
| **Use Case Testing owns flow structure**               | Use Case Testing identifies which paths (scenarios) to test; it delegates data selection to Domain Testing and condition enumeration to Decision Table                                                                   |
| **Error Guessing never duplicates**                    | Error Guessing test cases must target gaps in the systematic coverage — they must not test the same equivalence classes or paths already covered by systematic techniques                                                |
| **Systematic techniques before Error Guessing**        | Error Guessing is always applied last — after all systematic techniques for the feature are complete                                                                                                                     |
| **Pairwise reduces, never replaces**                   | Pairwise Testing is applied after a primary technique (Decision Table or Use Case Testing) has produced its full output and formal reduction has been applied — it further reduces that output, never substitutes for it |
| **Pairwise requires a prior derivation**               | Pairwise cannot be the first step; there must be an existing set of combinations (from Decision Table reduction or Scenario Matrix) to apply it to                                                                       |
| **Pairwise applies last within systematic techniques** | Apply Pairwise after formal reduction (Decision Table) or risk-based selection (Use Case Testing) — before Error Guessing                                                                                                |

## Common Rationalizations to Reject

- _"The feature is simple — I'll just write a few test cases by intuition"_ → Even simple features have equivalence classes and boundaries; intuition misses invalid classes and boundary values consistently
- _"We're doing use case testing so we don't need domain testing"_ → Use case testing identifies paths; domain testing selects data values within those paths — they address different questions
- _"Decision table gives us hundreds of rules — we can't test all of them"_ → Apply formal reduction (impossible rules + Don't Care merges) to produce an efficient, complete set; never reduce by gut-feel selection
- _"Error guessing is faster — we'll skip the systematic techniques"_ → Error guessing has no coverage guarantee; systematic techniques must be the foundation
- _"We've been testing this system for years — we know what to test"_ → Experience informs Error Guessing; it does not replace the systematic derivation that catches the cases experience overlooks
- _"Decision table gives too many rules — I'll just use pairwise from the start"_ → Pairwise requires the full Decision Table to be built and formally reduced first; skipping that step means pairwise is applied to an incomplete or unverified set, producing coverage gaps

## Quick-Reference Decision Tree

```
START: What is the primary characteristic of the requirement?
│
├─ Defines valid/invalid values for inputs or outputs?
│   └─ → /domain-testing
│
├─ Multiple conditions interact to produce different outcomes?
│   └─ → /decision-table-testing
│       (also apply /domain-testing if conditions involve ranges)
│
├─ System behavior depends on what happened before (states/history)?
│   └─ → /state-transition-testing
│       (also apply /domain-testing for guard condition data values)
│
├─ Describes a sequence of steps an actor takes to reach a goal?
│   └─ → /use-case-testing
│       (also apply /domain-testing for data-entry steps)
│       (also apply /decision-table-testing for steps with multi-condition logic)
│
├─ Systematic techniques already applied; looking for additional cases?
│   └─ → /error-guessing
│
├─ Systematic technique applied; output still has too many combinations to test?
│   ├─ Decision Table Testing: full table built + formal reduction applied → still too many rules?
│   │   └─ → Apply Pairwise on the reduced rule set
│   └─ Use Case Testing: impossible pruning + risk-based selection done → still too many scenarios?
│       └─ → Apply Pairwise on remaining scenarios
│
└─ Unclear which applies?
    └─ → Use /functional-test-design and let AI route
```
