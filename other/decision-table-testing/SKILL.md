---
name: decision-table-testing
description: >
  Apply this skill whenever you need to design test cases using Decision Table Testing
  techniques. Use when given requirements involving multiple conditions (inputs/states)
  that combine to produce different outcomes (actions/results) — especially when business
  rules contain "if-then-else", "and/or" logic, overlapping conditions, or multi-variable
  combinations. Triggers include: "design test cases", "write test cases for business rules",
  "test combinations", "decision table", "condition coverage", or any requirement with 2+
  interdependent conditions controlling system behavior (discount rules, access control,
  eligibility logic, pricing engines, validation rules with multiple flags).
---

# Decision Table Testing Skill

## Overview

**Decision Table Testing** is a black-box test design technique for specifying and testing complex business logic where **multiple conditions interact to determine system behavior**. It uses a tabular structure to systematically enumerate all meaningful combinations of conditions and map each to its expected set of actions (outcomes).

**Core purpose:** Guarantee that no meaningful combination of conditions is left untested, while eliminating redundant test cases through structured reduction.

Two complementary goals:

- **Completeness:** Every logical rule (combination of condition values) that the system must handle is identified and covered.
- **Efficiency:** Redundant rules are merged; logically impossible rules are eliminated before test execution

→ For full theoretical background, see [`resources/theory.md`](resources/theory.md).

## Invoke Syntax

```
/decision-table-testing [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                               | Behavior                                                                                                                                                                                                   |
| ---------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Default (conversation) | `/decision-table-testing`                            | All analysis and test case tables are printed inline in the conversation as Markdown                                                                                                                       |
| File output            | `/decision-table-testing --file="path/to/output.md"` | All output (Conditions & Actions List, Full Decision Table, Reduced Decision Table, Test Case Suite) is written to the specified file instead of printed inline. AI confirms the file path before writing. |

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/decision-table-testing --file="path/to/output.md"` then paste the requirements.

## When to Use

- Requirements contain **2 or more conditions** that interact to determine different system behaviors.
- Business rules with **"if-then-else"**, **"and/or"** logic, or multiple overlapping constraints.
- Requirements where **different combinations of inputs produce different outputs** (not just one input → one output).
- Complex eligibility, pricing, discount, access control, or routing logic.
- When requirements analysis reveals **implicit or contradictory conditions** that need to be surfaced.
- Any situation where ad-hoc or intuition-based test case design risks leaving combinations untested.

**Key signal:** If you find yourself writing "If condition A and condition B then..." repeatedly while reading requirements — Decision Table Testing is the right technique.

## When NOT to Use

- Only **one condition** controls behavior → use **Domain Testing (EP/BVA)** instead.
- Requirements describe a **sequence of states and transitions** → use **State Transition Testing** instead.
- Requirements describe a **user workflow or end-to-end flow** → use **Use Case Testing** instead.
- The number of conditions is very large (7+) and no reduction is feasible → consider **Pairwise/Combinatorial Testing** instead.
- Pure UI/UX testing, basic CRUD operations, or API payload structure testing with no conditional logic.
- Do **not** use Decision Table Testing alone as a complete test strategy — it does not cover boundary values within conditions (combine with Domain Testing for that).

## Inputs Required

Before applying this skill, you must have:

1. **Functional requirements or business rules (BR)** describing conditions and expected outcomes.
2. **All conditions (independent variables)** that affect system behavior — both explicit and implied.
3. **All actions (dependent outcomes)** — both explicit and implied, including error/rejection cases.
4. _(Optional but valuable)_ Confirmation from business/product owner on impossible combinations, boundary inclusivity, and any undocumented constraints.

## Core Principles

1. **Every condition must be explicitly represented:** No condition affecting behavior may be omitted from the table — including implied and negative conditions.
2. **Every meaningful rule must be covered:** Before reduction, the full table must account for all possible combinations.
3. **Impossible rules must be classified before acting:** Distinguish Type 1 (impossibility proven by the spec itself — no confirmation needed) from Type 2 (impossibility inferred by the tester — stakeholder confirmation mandatory).
4. **Don't Care conditions require proof:** A condition is only "Don't Care" when the action is provably identical for all its values — not when it seems unlikely to matter.
5. **One rule = one test case (after reduction):** Each column in the reduced table maps to exactly one test case.
6. **Actions must be fully specified per rule:** Every action for every rule must be explicitly marked — omission is not the same as "does not apply".
7. **Traceability is mandatory:** Every rule and resulting test case must trace back to a specific requirement or BR.

## Design Process

Follow these steps sequentially. Do not skip any steps.

### Step 1 — Analyze Requirements and Identify Conditions and Actions

Parse all requirements, BRs, and user stories. Extract:

- **Conditions:** The independent variables that affect system behavior. **Look for:** "if", "when", "given", "provided that", boolean flags, status fields, membership types, numeric thresholds (after EP grouping).
- **Actions:** The dependent outcomes triggered by combinations of conditions. **Look for:** "then", "resulting in", "the system will", "display", "calculate", "reject", "grant access". Include ALL possible outcomes — both positive and negative (error states, rejections, no-action cases).

**Critical tasks at this step:**

- Identify **implied conditions** not explicitly stated (e.g., "VIPs get free shipping" implies a non-VIP condition with different behavior).
- Identify **implied actions** (e.g., "coupon cannot be used with new customer discount" implies the coupon is silently ignored, not rejected).
- Identify **mutual exclusion constraints** between conditions (flags on impossible combinations early).
- Clarify **ambiguities** with stakeholders before proceeding — ambiguous requirements produce wrong tables.

→ See [`resources/conditions-actions-guide.md`](resources/conditions-actions-guide.md) for extraction patterns and examples.

### Step 2 — Build the Full Decision Table

Construct the complete table before any reduction:

1. **Choose table entry type:**
   - **Limited Entry:** Condition values are binary only (T/F, Y/N, 0/1). Simplest form; total rules = 2ⁿ for n binary conditions.
   - **Extended Entry:** Condition values can be multi-valued (e.g., status = `ACTIVE` / `INACTIVE` / `SUSPENDED`). Total rules = product of all value counts per condition.
2. **Calculate total number of rules:** For n binary conditions → 2ⁿ rules. Fill condition rows with all possible combinations systematically (use binary counting pattern for limited entry).
3. **Fill in actions per rule:** For each rule (column), evaluate the requirement and mark every applicable action. **Use consistent notation:** `X` for "action applies"; _blank_ for "action does not apply"; specify exact values for extended entry tables.
4. **Mark impossible rules** (do not remove yet — removal happens in Step 3).

→ See [`resources/table-construction.md`](resources/table-construction.md) for notation standards, entry types, and construction patterns.

### Step 3 — Reduce and Optimize the Decision Table

Apply reduction to eliminate redundancy while preserving 100% logical coverage:

#### 3a. Remove Impossible Rules

- Identify rules containing combinations that cannot occur in the real system (mutually exclusive conditions, physically impossible states).
- **Classify each candidate impossible rule before acting:**
  - **Type 1 (Structurally impossible):** Impossibility is directly proven by a specific BR or spec statement. Document the source BR. Remove without stakeholder confirmation — the spec is the proof.
  - **Type 2 (Assumed impossible):** Impossibility is inferred by the tester, not explicitly stated in the spec. Stakeholder confirmation is mandatory before removal — what appears impossible may occur via API bypass, admin override, data migration, or race conditions.
- Mark removed rules as `IMPOSSIBLE` with documented rationale (do not silently delete).

#### 3b. Merge Rules via Don't Care Conditions

- Two rules can be merged if and only if:
  - They produce **exactly the same set of actions**
  - They differ in the value of **exactly one condition**
- The differing condition becomes a **Don't Care (`—`)** in the merged rule.
- Apply iteratively — a merged rule may be eligible for further merging.

#### 3c. Verify Reduction Completeness

- After reduction, verify that the merged rules still cover all original rules they replaced.
- No valid rule from the full table should be unrepresented in the reduced table.

→ See [`resources/reduction-guide.md`](resources/reduction-guide.md) for detailed reduction procedures, worked examples, and common mistakes.

### Step 4 — Derive Test Cases from the Reduced Table

Translate each remaining column (rule) in the reduced table into one test case:

- **One rule = one test case** (no exceptions)
- **Conditions → Test inputs / preconditions / test data**
- **Actions → Expected results / assertions**
- **For Don't Care conditions:** Choose the most revealing concrete value (typically the one most likely to expose a defect if the condition were to matter unexpectedly)
- **For extended entry tables:** The specific value in the cell is the test data

**Assign each test case:** ID, description, all input values (including Don't Care choices), expected outputs, and traceability to rule number and requirement.

→ Use [`resources/output-template.md`](resources/output-template.md) for the recommended format.

### Step 5 — Review Against Quality Checklists

Before finalizing, verify the test suite against the **Test Case Quality Checklist** in [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Design Rules

| Rule                                     | Description                                                                                                                              |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **All conditions must appear**           | Every condition affecting behavior must be a row in the table — no implied conditions may be omitted                                     |
| **All actions must appear**              | Every possible outcome must be a row — including "no action", "error", "reject" cases                                                    |
| **Full table before reduction**          | Always construct the complete table first; never start with a reduced table                                                              |
| **Impossible ≠ skip**                    | Impossible rules must be documented and confirmed, not silently omitted                                                                  |
| **Type 1: spec proves it**               | If a BR explicitly defines two conditions as mutually exclusive, remove without stakeholder confirmation — cite the BR                   |
| **Type 2: tester infers it**             | If impossibility is the tester's inference (not in the spec), confirm with stakeholder before removal                                    |
| **Don't Care requires proof**            | Only mark Don't Care when actions are provably identical across all values of that condition                                             |
| **One invalid ≠ Decision Table**         | Decision Table tests combinations — not single-variable invalid inputs (use Domain Testing for those)                                    |
| **Combine with EP for range conditions** | When a condition involves a range (e.g., "amount > $100"), first partition using EP, then use the partition class as the condition value |

## Anti-Patterns

→ **Full detail:** [`resources/anti-patterns.md`](resources/anti-patterns.md)

**Critical anti-patterns:**

- **Starting with the reduced table** — skipping the full table means missing combinations before you know they're impossible or mergeable
- **Conflating conditions with test data** — conditions are categories of behavior, not raw input values (e.g., "amount > $100" is a condition class, not a test value)
- **Marking Don't Care without verification** — assuming a condition doesn't matter without proving all action sets are identical
- **Applying the same confirmation rule to all impossible rules** — Type 1 (proven by spec) needs no confirmation; Type 2 (inferred by tester) always does
- **Missing implied conditions or implied actions** — only listing what's explicitly written in the spec
- **Treating mutually exclusive conditions as separate test cases** — should be impossible rules, not additional test cases
- **Using Decision Table for single-condition logic** — overkill and misleading; use EP/BVA instead
- **Leaving actions blank instead of explicitly "no action"** — ambiguous blanks produce ambiguous test results

## Best Practices

→ **Full detail:** [`resources/best-practices.md`](resources/best-practices.md)

**Key best practices:**

- Use EP to convert continuous range conditions into discrete classes before building the table (prevents infinite-column tables).
- Combine with BVA after the table is built — use boundary values as the specific test data for range-based conditions.
- Classify impossible rules before acting: Type 1 (proven by spec) → cite BR and remove; Type 2 (inferred by tester) → confirm with stakeholder first.
- For large tables (5+ conditions), build the table in sections grouped by dominant conditions.
- Document rationale for every Don't Care and every impossible rule.
- Surface specification gaps during table construction — incomplete specs produce incomplete tables; raise gaps before executing.
- In Agile: use Decision Table construction as a "Three Amigos" spec review tool (Product Owner + Dev + QA).

## Process Quality Checklist

_Use this to verify the design process was followed correctly — before reviewing individual test cases._

- [ ] All conditions have been identified — including implied conditions not explicitly stated in the spec.
- [ ] All actions have been identified — including "no discount", "reject", "error" cases and implied outcomes.
- [ ] Ambiguities in requirements were raised and resolved before table construction.
- [ ] The full (unoptimized) table was built before any reduction was applied.
- [ ] Total rule count matches the formula: 2ⁿ for n binary conditions (or product of value counts for extended entry).
- [ ] All actions are explicitly marked per rule — no ambiguous blanks.
- [ ] Impossible rules are classified as Type 1 (proven by spec) or Type 2 (inferred by tester).
- [ ] Type 1 impossible rules have their source BR cited as proof.
- [ ] Type 2 impossible rules have stakeholder confirmation documented (who, when, scope).
- [ ] Don't Care merges are verified: merged rules produce exactly the same action set and differ in exactly one condition.
- [ ] Reduction is complete: no further merges are possible in the reduced table.
- [ ] Every rule in the reduced table traces to one or more rules in the full table.
- [ ] Every test case traces to a specific rule in the reduced table and to a specific requirement or BR.

→ For the full **Process Quality Checklist** should be verified, see [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Common Rationalizations to Reject

- _"That combination is obviously impossible — I don't need to document it"_ → Document and confirm; assumptions about impossibility are a frequent source of missed defects
- _"I need to ask the PO about every impossible rule — even the ones already proven by the spec"_ → Type 1 impossible rules (proven directly by a BR) need no confirmation; asking for it wastes time and signals poor analytical judgment
- _"I'll skip building the full table since I know most of it will be reduced anyway"_ → The full table is the proof of completeness; skipping it means you cannot verify what you've eliminated
- _"The condition doesn't matter for this rule — I'll mark it Don't Care"_ → Only valid if you can prove the action set is identical for all values; prove it, don't assume it
- _"These two test cases look similar, I'll merge them"_ → Merging requires formal Don't Care proof — "looking similar" is not sufficient
- _"The spec doesn't mention what happens when both flags are false — I'll skip that rule"_ → Unspecified behavior is a spec gap, not a reason to skip; raise it, then design the test case based on the resolved answer
- _"This table is too big — I'll just test the important combinations"_ → "Important" is subjective; use formal reduction instead of gut-feel selection

## Red Flags

Stop and re-evaluate if you observe:

- The reduced table has the same number of rules as the full table (reduction likely wasn't applied or impossible rules weren't identified).
- A condition row in the table is always T or always F across all rules (condition may be redundant, or the spec is incomplete).
- A test case has no expected action at all (action row is entirely blank — the rule is either impossible and should be removed, or a required action is missing).
- More than 30% of rules are marked "Impossible" without stakeholder confirmation (likely a misunderstanding of the requirements).
- A Don't Care was applied to a condition that has 3+ possible values but only one was used to verify the merge.
- Two test cases in the final suite have identical input combinations (duplicate rules survived reduction).

## Output

The design process produces:

1. **Conditions and Actions List** — all extracted conditions (with value options) and all actions, traced to requirements
2. **Full Decision Table** — complete unoptimized table before reduction
3. **Reduced Decision Table** — optimized table with impossible rules removed and Don't Care merges applied, with rationale column
4. **Test Case Suite** — using the template in [`resources/output-template.md`](resources/output-template.md)

## Examples

→ [`examples/discount-rules.md`](examples/discount-rules.md) — Multi-condition discount system (limited entry, 3 binary conditions, impossible rules + Don't Care reduction)  
→ [`examples/loan-eligibility.md`](examples/loan-eligibility.md) — Loan eligibility assessment (extended entry, multi-valued conditions, complex action combinations)
