---
name: error-guessing
description: >
  Apply this skill whenever you need to design supplementary test cases using Error Guessing
  — an experience-based test design technique. Use after applying black-box techniques (Domain
  Testing, Decision Table, State Transition, Use Case Testing) to identify additional high-value
  test cases targeting defect-prone areas that systematic techniques may miss. Triggers include:
  "error guessing", "what else should we test", "edge cases", "what could go wrong", "attack the
  system", "fault attack", "experience-based testing", or any request to supplement an existing
  test suite with additional risk-based cases. Also use when the tester has domain knowledge,
  historical defect data, or heuristic intuition about where defects are likely to hide.
---

# Error Guessing Skill

## Overview

**Error Guessing** is an **experience-based test design technique** defined in ISTQB Foundation Level Syllabus where testers use their knowledge, intuition, and experience to anticipate where defects are likely to occur — then design test cases specifically targeting those areas.

Unlike black-box techniques (EP, BVA, Decision Table, State Transition), Error Guessing has **no formal derivation procedure**. Its effectiveness depends on the tester's ability to reason about:

- Common programming mistakes and error-prone constructs.
- Historical defect patterns in the system or similar systems.
- Boundary and special-value behavior beyond formal BVA.
- Interactions between components, configurations, and data states that create unexpected behavior.

**Core purpose:** Supplement systematic techniques by targeting the gaps they leave — the "middle of the valid class" defects, integration edge cases, data combinations, and implementation-specific failure modes that rules-based techniques cannot reliably surface.

**ISTQB classification:** Experience-Based Test Design Technique. Also known in practice as **Fault Attack** — a structured variant where guesses are organized into lists or taxonomies rather than applied ad hoc.

→ For full theoretical background, see [`resources/theory.md`](resources/theory.md).

## Invoke Syntax

```
/error-guessing [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                       | Behavior                                                                                                       |
| ---------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Default (conversation) | `/error-guessing`                            | All analysis and test cases printed inline in the conversation as Markdown                                     |
| File output            | `/error-guessing --file="path/to/output.md"` | All output (Error/Fault List, Test Case Suite) written to the specified file. AI confirms path before writing. |

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/error-guessing --file="path/to/output.md"` then paste the requirements.

## When to Use

- **After** systematic techniques have been applied — Error Guessing supplements, never replaces, black-box techniques.
- When a tester has domain knowledge, system knowledge, or historical defect data about the area under test.
- When reviewing an existing test suite for gaps — "what has the systematic approach missed?".
- When time permits additional high-value test cases beyond the formal coverage baseline.
- When the feature involves: boundary conditions not covered by formal BVA, complex data interactions, third-party integrations, concurrency, configuration-dependent behavior, or known defect-prone constructs.
- When defect data from similar past projects suggests specific failure patterns.
- During exploratory testing sessions to guide investigation.

## When NOT to Use

- **Instead of** systematic techniques — Error Guessing cannot replace EP, BVA, Decision Table, or State Transition Testing as the primary technique; it has no coverage guarantee.
- When the tester has no relevant experience or domain knowledge about the area under test — uninformed guessing adds noise without value.
- As the sole basis for test coverage reporting — Error Guessing produces no formal coverage metric; it cannot be cited as a coverage criterion.
- When requirements are unclear — clarify requirements first; guessing on top of ambiguous specs produces test cases that cannot be evaluated.

## Inputs Required

Before applying this skill, you must have:

1. **Completed systematic test suite** — the existing test cases from black-box techniques; Error Guessing identifies what they missed.
2. **Feature/component description** — FR, BR, user stories, or API spec being tested.
3. **Tester's domain knowledge** — experience with the technology stack, business domain, or similar systems.
4. **Historical defect data** (when available) — past bugs in this system or similar systems; defect taxonomies.
5. **Risk information** (when available) — which areas are highest risk, most complex, or most recently changed.
6. **Error taxonomy reference** — [`resources/error-taxonomy.md`](resources/error-taxonomy.md) — structured catalog of common error categories to guide systematic guessing.

## Core Principles

1. **Supplement, never replace:** Error Guessing adds value only when systematic techniques have already been applied. It fills gaps — it is not a starting point.
2. **Guesses must be justified:** A good error guess is not random — it is based on a specific rationale: known defect pattern, implementation risk, historical data, or heuristic reasoning. Unjustified guesses waste effort.
3. **Structure the guessing:** Apply the **Fault Attack** approach — organize guesses into categories (input faults, boundary faults, computation faults, etc.) using an error taxonomy. Structured guessing finds more defects than unstructured intuition.
4. **Each guess → one test case:** Every error hypothesis must be translated into a specific, executable test case with defined input, expected result, and rationale.
5. **Document the rationale:** Record why each test case was added — what defect is being targeted and why it is suspected. This enables test suite maintenance and defect root cause analysis.
6. **Prioritize by risk:** When time is limited, order error guesses by defect probability × impact. Test the most likely and most damaging failures first.

## Design Process

Follow these steps sequentially. Do not skip any steps.

### Step 1 — Review the Existing Test Suite

Examine the test cases already produced by systematic techniques. Identify:

- Which equivalence classes and boundaries are already covered.
- Which conditions, combinations, and paths have been exercised.
- Which areas of the specification received less attention (complex logic, implicit behavior, integration points).

This prevents duplicating existing coverage and focuses Error Guessing where it adds new value.

### Step 2 — Gather Error Guessing Inputs

Collect all available information that informs error guessing:

**Domain knowledge sources:**

- Personal experience with similar systems, technology stacks, or business domains
- Team knowledge (developers, architects, business analysts) about implementation risks
- Code review findings or known technical debt

**Historical defect data:**

- Past bug reports for this system (look for recurring defect patterns)
- Defect data from similar past projects
- Industry defect taxonomies relevant to the technology (web, API, mobile, embedded)

**Risk information:**

- Recently changed or newly developed components (higher defect density)
- Complex algorithms or business logic
- Third-party integrations and external dependencies
- Concurrency, multi-threading, or race condition risks
- Configuration-dependent behavior

→ Use [`resources/error-taxonomy.md`](resources/error-taxonomy.md) as a structured checklist to ensure all major error categories are considered.

### Step 3 — Generate the Error / Fault List

Produce a structured list of error hypotheses — specific defect scenarios the tester suspects may exist.

For each hypothesis, document:

- **Category:** Which error category it belongs to (input, boundary, computation, state, integration, etc.)
- **Hypothesis:** What specific defect might exist and where
- **Rationale:** Why this defect is suspected (experience, historical data, known risk)
- **Risk:** Probability × impact estimate (High / Medium / Low)

**Structured approach (Fault Attack):** Work through each category in [`resources/error-taxonomy.md`](resources/error-taxonomy.md) systematically. For each category, ask: "Does this apply to the feature under test? What specific failures could occur here?"

→ See [`resources/fault-attack-guide.md`](resources/fault-attack-guide.md) for the structured Fault Attack procedure.

### Step 4 — Prioritize the Error List

Rank error hypotheses by: **Risk = Defect Probability × Defect Impact**

| Priority | Criteria                                                |
| -------- | ------------------------------------------------------- |
| High     | Likely to occur AND high impact if missed in production |
| Medium   | Moderately likely OR moderate impact                    |
| Low      | Unlikely OR low impact                                  |

When time is constrained, design test cases for High priority first, then Medium. Document Low priority items as acknowledged risks even if not tested.

### Step 5 — Design Test Cases from Error Hypotheses

Translate each error hypothesis into one or more executable test cases:

- **One hypothesis → one test case** (or more if multiple specific values need to be tested for the same hypothesis)
- **Input:** Specific values chosen to trigger the suspected defect
- **Expected result:** What the system should do if the code is correct (not what the defect would produce)
- **Rationale:** The error hypothesis this test case is designed to expose
- **Priority:** From the risk ranking in Step 4

→ Use [`resources/output-template.md`](resources/output-template.md) for the recommended format.

### Step 6 — Review Against Quality Checklists

Before finalizing, verify the test suite against the **Test Case Quality Checklist** in [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Anti-Patterns

→ **Full detail:** [`resources/anti-patterns.md`](resources/anti-patterns.md)

**Critical anti-patterns:**

- **Using Error Guessing instead of systematic techniques** — no coverage guarantee; systematic gaps become production defects
- **Unjustified guesses** — test cases added by "gut feel" with no documented rationale; cannot be evaluated, maintained, or defended
- **Duplicating existing systematic coverage** — adding error guessing test cases that test the same classes/boundaries already covered; wastes effort without adding value
- **Random special value testing without taxonomy** — testing `null`, `0`, `""` without reasoning about why these would expose a defect in this specific feature
- **No prioritization** — treating all error guesses as equal; when time runs out, highest-risk guesses may not have been tested
- **Forgetting expected results** — writing "input X" without specifying what correct behavior looks like; test case is not executable

## Best Practices

→ **Full detail:** [`resources/best-practices.md`](resources/best-practices.md)

**Key best practices:**

- Always apply systematic techniques first; apply Error Guessing only to supplement.
- Use a structured error taxonomy (Fault Attack approach) rather than pure intuition — structured guessing finds more defects.
- Mine historical defect data: defects cluster; where bugs were found before, they are likely to be found again.
- Consult domain experts (developers, architects, business analysts) — their implementation knowledge is a high-value input.
- Document every test case rationale — "why do I suspect this?" is as important as "what am I testing?".
- Prioritize by risk: test the most likely and most damaging failure modes first.
- Revisit and update the error list when requirements change or new defects are found.

## Process Quality Checklist

_Use this to verify the Error Guessing process was applied correctly — before reviewing individual test cases._

- [ ] Systematic techniques (EP/BVA, Decision Table, State Transition, etc.) were applied first; Error Guessing is supplementing, not replacing them.
- [ ] The existing test suite was reviewed before generating error hypotheses (no duplicate coverage).
- [ ] Error taxonomy was used as a structured checklist — all major categories considered, not just intuition.
- [ ] Historical defect data was consulted where available.
- [ ] Domain experts were consulted where their knowledge was relevant and accessible.
- [ ] Every error hypothesis has a documented rationale (not "gut feel" without basis).
- [ ] Error hypotheses were prioritized by risk (probability × impact) before test case design.
- [ ] High-priority hypotheses were addressed first.
- [ ] Each hypothesis was translated into at least one specific, executable test case.

→ For the full **Process Quality Checklist** should be verified, see [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Common Rationalizations to Reject

- _"I have years of experience — I don't need a taxonomy, I'll just guess"_ → Unstructured guessing misses entire categories of defects that a taxonomy would surface; experience and structure are complementary, not alternatives
- _"We've already done EP and BVA — that's enough coverage"_ → Systematic techniques have known blind spots (middle-of-class defects, interaction faults, implementation-specific failures); Error Guessing targets exactly these gaps
- _"I don't have time to document the rationale"_ → Without rationale, the test case cannot be evaluated (is it testing the right thing?), maintained (what does it cover?), or defended (why is this test here?); rationale is not optional
- _"We didn't find any defects with error guessing — it wasn't worth it"_ → Absence of findings does not mean the technique failed; it increases confidence that the suspected failure modes are not present; this is valid quality evidence
- _"That edge case is too unlikely — no one would do that"_ → Users, integrations, and automated systems routinely produce inputs that "no one would do"; attackers deliberately craft them; error guessing explicitly targets the unlikely

## Red Flags

Stop and re-evaluate if you observe:

- Error Guessing test cases overlap entirely with the existing systematic test suite — the gap analysis in Step 1 was not performed.
- Every error guess is in the same category (e.g., all boundary-related) — the taxonomy was not used; entire categories of failures are unaddressed.
- No test case has a documented rationale — the "guesses" are arbitrary; the test suite cannot be maintained or evaluated.
- Error Guessing is being used as the primary test design technique for a feature — systematic techniques were skipped.
- Expected results are missing or vague ("system should work", "no error") — test cases are not evaluable.

## Output

The design process produces:

1. **Error / Fault List** — structured list of error hypotheses with category, rationale, and risk priority, organized by error category
2. **Test Case Suite** — supplementary test cases derived from high and medium priority hypotheses, using the template in [`resources/output-template.md`](resources/output-template.md)

## Examples

→ [`examples/user-registration-api.md`](examples/user-registration-api.md) — Error Guessing applied to a REST API user registration endpoint: demonstrates taxonomy-driven fault attack, historical defect mining, prioritization, and full test case suite with rationale
