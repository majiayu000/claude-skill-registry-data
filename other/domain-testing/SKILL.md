---
name: domain-testing
description: >
  Apply this skill whenever you need to design test cases using Domain Testing techniques
  (Equivalence Partitioning and Boundary Value Analysis). Use when given any input/output
  specification, business rule, field constraint, API parameter, or functional requirement
  that involves ranges, sets, formats, or conditions. Triggers include: "design test cases",
  "write test cases", "identify test data", "EP", "BVA", "equivalence class", "boundary value",
  "partition", or any request to test a field/function with defined input constraints.
---

# Domain Testing Skill

## Overview

**Domain Testing** is a black-box test design approach that applies **Equivalence Partitioning (EP)** and **Boundary Value Analysis (BVA)** to structure large or infinite input domains into manageable partitions. Test cases are then selected from within these partitions, with particular emphasis on boundary values where defects are more likely to occur.

- **Equivalence Partitioning (EP):** Divides input/output space into classes where all values are expected to trigger identical behavior. Testing one representative per class is sufficient.
- **Boundary Value Analysis (BVA):** Targets the edges of equivalence classes, where off-by-one errors and mis-specified conditions most frequently occur.

The goal is to achieve effective coverage of the input domain while reducing the number of test cases compared to exhaustive testing.

→ For full theoretical background, see [`resources/theory.md`](resources/theory.md).

## Invoke Syntax

```
/domain-testing [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                       | Behavior                                                                                                                                                                              |
| ---------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Default (conversation) | `/domain-testing`                            | All analysis and test case tables are printed inline in the conversation as Markdown                                                                                                  |
| File output            | `/domain-testing --file="path/to/output.md"` | All output (Variable Inventory Table, Equivalence Class Table, Test Case Suite) is written to the specified file instead of printed inline. AI confirms the file path before writing. |

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/domain-testing --file="path/to/output.md"` then paste the requirements.

## When to Use

- Designing test cases for any input field, parameter, or variable with defined constraints (range, format, length, set of values).
- Designing test cases for output domains (expected results, response codes, calculated values).
- Any requirement containing keywords: "must be between", "must not exceed", "valid values are", "required format", "minimum/maximum".
- Early in the test design phase, before writing test cases — EP and BVA should be the _first_ techniques applied to functional requirements.

## When NOT to Use

- Requirements involving **combinations of multiple conditions** triggering different business rules → use **Decision Table Testing** instead.
- Requirements involving **sequences of states and transitions** → use **State Transition Testing** instead.
- When there are **no defined input/output constraints** (pure exploratory context) → use **Error Guessing** or **Exploratory Testing**.
- Do **not** use Domain Testing alone as a complete test strategy — it has known blind spots (see **Anti-Patterns** section below).

## Inputs Required

Before applying this skill, you must have:

1. **Functional requirements or business rules (BR)** describing what the system accepts/rejects.
2. **Field/variable constraints** — data type, range, length, format, enumeration, mandatory/optional.
3. **Expected system behavior** for valid and invalid inputs (success response, error messages, etc.).
4. _(Optional but valuable)_ **Technical constraints** — database column types, UI field limits, API schema.

## Core Principles

1. **Partition completeness:** Every possible input value must belong to exactly one equivalence class — no gaps, no overlaps.
2. **One representative is sufficient:** Testing multiple values from the same class is redundant — pick the most revealing one.
3. **Boundaries are highest risk:** Always apply BVA to any ordered/sequential partition.
4. **Isolate invalid classes:** Each test case for an invalid class must contain exactly one invalid input — all other inputs must be valid (to prevent Defect Masking).
5. **Combine valid classes:** Multiple valid classes can and should be covered in a single test case to minimize total test count.
6. **Traceability is mandatory:** Every test case must trace back to a specific requirement, BR, or constraint.

## Design Process

Follow these steps sequentially. Do not skip any steps.

### Step 1 — Parse Requirements & Identify Variables

- Read all requirements, BRs, user stories, and field-level constraints.
- Extract every **input variable** (UI fields, API parameters, file inputs, system states, environment values).
- Extract every **output variable** (response codes, UI state changes, DB updates, calculated values, error messages).
- **Note:** data type, valid range/format/set, mandatory vs optional, dependencies between variables.

**Output of this step:** A variable inventory table listing each variable, its type, and its constraints.

### Step 2 — Identify Equivalence Classes for Each Variable

Apply the partitioning guidelines (see [`resources/ep-guidelines.md`](resources/ep-guidelines.md)):

For each variable:

- Identify **valid equivalence class(es)**
- Identify **invalid equivalence class(es)**
- Apply the **Splitting Principle** if there is reason to suspect sub-groups within a class are handled differently by the system

**Output of this step:** Equivalence class table per variable with Valid/Invalid classification and rationale.

### Step 3 — Apply Boundary Value Analysis to Ordered Classes

For every ordered (sequential/range) equivalence class, apply BVA:

- **Standard BVA (2-value):** For lower-risk scenarios, test only `LB` and `LB-1`; `UB` and `UB+1`.
- **Extended BVA (3-value):** Test `LB-1`, `LB`, `LB+1` at the lower boundary; `UB-1`, `UB`, `UB+1` at the upper boundary.
- Add a **nominal value** (representative from the middle of the valid class) to confirm core logic.

For non-ordered classes (discrete sets, boolean conditions), BVA does not apply — EP representative values are sufficient.

→ See [`resources/bva-reference.md`](resources/bva-reference.md) for boundary point definitions and data type guidance.

### Step 4 — Build the Test Case Suite

Apply test case combination rules:

- **Valid test cases:** Combine as many valid classes as possible into a single test case. Continue until all valid classes are covered at least once.
- **Invalid test cases:** One test case per invalid class. All other variables in the same test case must use valid values. This prevents Defect Masking.

**Assign each test case:** ID, description, input values, expected output, and traceability to requirement/class.

→ Use [`resources/output-template.md`](resources/output-template.md) for the recommended test case format.

### Step 5 — Review Against Quality Checklist

Before finalizing, verify the test suite against the **Test Case Quality Checklist** in [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Design Rules

| Rule                                   | Description                                                               |
| -------------------------------------- | ------------------------------------------------------------------------- |
| **No gaps in partition space**         | The union of all classes must cover the entire input domain               |
| **No overlaps between classes**        | A single input value must not belong to two different classes             |
| **One invalid per test case**          | A test case covering an invalid class must have all other inputs as valid |
| **BVA on all ordered partitions**      | Any range or sequential domain requires boundary testing                  |
| **Minimum coverage = 1 rep per class** | Every equivalence class must have at least one test case                  |
| **Expected result must be specified**  | Every test case must have a defined, verifiable expected output           |

## Anti-Patterns

→ **Full detail:** [`resources/anti-patterns.md`](resources/anti-patterns.md)

**Critical anti-patterns:**

- **Combining multiple invalid inputs** in one test case → causes Defect Masking
- **Missing invalid equivalence classes** → only testing happy path
- **Overlapping partitions** → redundant tests, false confidence
- **Testing only exact boundaries, skipping LB-1/UB+1** → misses out-of-range handling
- **Treating all "invalid" as one class** → misses distinct error paths (e.g., wrong type vs out of range are different behaviors)
- **Applying BVA to non-ordered fields** (e.g., enumerations, boolean flags) → meaningless test cases
- **Ignoring output domains** → only testing input partitions, missing output-based defects
- **Assuming spec is complete** → not questioning undocumented technical constraints (DB limits, encoding limits)

## Best Practices

→ **Full detail:** [`resources/best-practices.md`](resources/best-practices.md)

**Key best practices:**

- Always identify both valid AND invalid classes for every variable — do not stop at valid-only.
- When in doubt whether two values belong to the same class, **split** (Splitting Principle) — false splits cost one extra test; missed splits miss defects.
- Use **3-value BVA** (LB-1, LB, LB+1) for high-risk or complex systems; **2-value BVA** for simpler/lower-risk scenarios.
- Supplement boundary tests with **technical boundary testing** (system min/max values beyond business logic) — but treat these as Error Guessing additions, not standard BVA.
- Document the rationale for every equivalence class — enables easy update when requirements change.
- Always validate: _Does the spec explicitly define behavior for invalid inputs?_ If not, clarify before designing test cases.
- For multi-variable inputs, design a **variable inventory table** before jumping to test cases.

## Process Quality Checklist

_Use this to verify you followed the design process correctly — separate from test case quality._

- [ ] All input AND output variables have been identified.
- [ ] Every variable has at least one valid and one invalid equivalence class (unless it's a truly optional field with no constraints).
- [ ] The Splitting Principle was consciously evaluated for each class.
- [ ] BVA was applied to every ordered/sequential partition.
- [ ] Non-ordered partitions (enumerations, booleans) were NOT incorrectly subjected to BVA.
- [ ] All valid classes are covered by at least one test case.
- [ ] All invalid classes are covered by exactly one test case each, with all other inputs valid.
- [ ] Every test case has a specified expected result.
- [ ] Every test case traces to a requirement, BR, or constraint.
- [ ] No two test cases are identical in both input and expected result.
- [ ] Technical constraints (DB limits, field size limits) were considered beyond business rule constraints.

→ For the full **Process Quality Checklist** should be verified, see [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Common Rationalizations to Reject

These are flawed justifications QA practitioners sometimes use — reject them:

- _"The range is obvious, I don't need to document the partitions"_ → Undocumented partitions can't be reviewed or updated
- _"Testing LB is enough, I don't need LB-1"_ → Off-by-one errors live exactly at LB-1
- _"Invalid input is handled by the UI — no need to test it in the backend"_ → Defense in depth; always test each layer independently
- _"I'll combine two invalid inputs to save time"_ → This creates Defect Masking; a "passed" result means nothing
- _"All strings in the valid range behave the same"_ → Unicode, special chars, and extreme lengths often trigger hidden code paths
- _"The spec doesn't mention invalid behavior so I won't test it"_ → The system still needs to handle it; missing spec = clarification needed, not skip

## Red Flags

Stop and re-evaluate the design if you observe:

- A variable has only valid equivalence classes and zero invalid classes.
- A test case covers more than one invalid equivalence class simultaneously.
- BVA was applied to an enumeration or boolean field.
- The total number of test cases equals the number of variables (likely missed most invalid classes and boundaries).
- No test case traces to a specific requirement or constraint.
- Expected result is listed as "no error" or "works fine" without specifics.

## Output

The design process produces:

1. **Variable Inventory Table** — all input/output variables with type and constraints
2. **Equivalence Class Table** — per variable, with valid/invalid classification and rationale
3. **Test Case Suite** — using the template in [`resources/output-template.md`](resources/output-template.md)

## Examples

→ [`examples/product-code.md`](examples/product-code.md) — Multi-condition string validation (format + length + character set rules)  
→ [`examples/login-form.md`](examples/login-form.md) — Multi-variable (username + password), demonstrates Input Value(s) format and isolation strategy across two fields
