---
name: acceptance-criteria
description: Write testable acceptance criteria and acceptance tests for requirements using Given/When/Then, checklist, and rule-based formats. Use when defining the conditions that prove a requirement is correctly implemented.
intent: >-
  Create acceptance criteria that define the specific, testable conditions under which a requirement is considered satisfied. Covers three formats (Given/When/Then, checklist, rule-based), SMART criteria for requirements, and the separation between acceptance criteria (conditions) and acceptance tests (procedures). Use this to close the gap between "what does this requirement mean?" and "how do we prove it works?"
type: component
theme: re-artifacts
best_for:
  - "Defining done for user stories and requirements"
  - "Creating testable conditions for functional and non-functional requirements"
  - "Bridging the gap between requirements and test cases"
scenarios:
  - "Developers keep asking what 'done' means for this requirement"
  - "I need to write acceptance criteria that QA can turn into test cases"
estimated_time: "5-10 min per requirement"
trigger: 需要定义功能完成标准
input: PRD 文档
output: 验收标准列表
next: user-story
dependencies: prd-development
---


## Purpose
Create acceptance criteria that define the specific, testable conditions under which a requirement is considered satisfied. Use this to close the gap between "what does this requirement mean?" and "how do we prove it works?"

This is not test case writing -- acceptance criteria define *what* to verify. Test cases define *how* to verify it. Acceptance criteria live in requirements; test cases live in test plans.

## Key Concepts

### Acceptance Criteria vs. Acceptance Tests

| Aspect | Acceptance Criteria | Acceptance Tests |
|--------|-------------------|-----------------|
| What | Conditions for satisfaction | Procedures to verify conditions |
| Who writes | BA / Requirements Engineer | QA / Test Engineer |
| When | During requirements specification | During test planning |
| Format | Given/When/Then, checklists | Step-by-step test procedures with expected results |
| Lives in | SRS, user stories | Test plan, test management tool |

### Three Formats for Acceptance Criteria

**1. Given/When/Then (Gherkin)**
Best for behavior-driven scenarios with clear preconditions and triggers:
```
Given [precondition],
When [action],
Then [expected result].
```

**2. Checklist**
Best for straightforward pass/fail conditions:
```
- [ ] [Condition that must be true]
- [ ] [Another condition that must be true]
```

**3. Rule-Based**
Best for business rules with multiple examples:
```
Rule: [Business rule statement]
Example: [Input] -> [Expected output]
Example: [Different input] -> [Different expected output]
```

### SMART Acceptance Criteria
Every acceptance criterion should be:
- **Specific** -- Describes a single, concrete condition
- **Measurable** -- Has a pass/fail determination
- **Achievable** -- Technically feasible
- **Relevant** -- Traces to a requirement or user need
- **Testable** -- A tester can verify it without interpretation

### Anti-Patterns
- **The Obviously True** -- "The system shall function correctly." Every requirement should function correctly.
- **The Subjective** -- "The interface shall be attractive." Whose taste?
- **The Implementation Detail** -- "The system shall use a 256-bit AES encryption key stored in a hardware security module." That is design, not a requirement.
- **The Infinite Set** -- "The system shall handle all possible inputs." Impossible to test.

## Application

### Step 1: Start with the Requirement

Take your requirement (user story, shall statement, or use case step) and ask:
- "How will we know this requirement is satisfied?"
- "What does the user expect to see when this works?"
- "What does failure look like?"

### Step 2: Choose the Right Format

| Use This Format | When |
|----------------|------|
| Given/When/Then | The behavior depends on preconditions and has clear trigger/response |
| Checklist | Simple pass/fail conditions without complex preconditions |
| Rule-Based | A business rule with multiple scenarios or boundary conditions |

### Step 3: Write the Criteria

**Given/When/Then example:**
```markdown
**Requirement:** CT.ALERT.EXPIRY.1 -- The system shall send an email
alert to the responsible lab technician when a chemical is 30 days
from expiration.

**Acceptance Criteria:**

AC-1: Given a chemical with expiration date exactly 30 days from today,
      and a lab technician is assigned to its storage location,
      When the daily alert job runs,
      Then an email is sent to the assigned technician containing the
      chemical name, CAS number, location, and expiration date.

AC-2: Given a chemical with expiration date exactly 30 days from today,
      and no technician is assigned to its storage location,
      When the daily alert job runs,
      Then an email is sent to the lab manager instead.

AC-3: Given a chemical with status "Disposed,"
      and expiration date is 30 days from today,
      When the daily alert job runs,
      Then no alert is sent for that chemical.
```

**Checklist example:**
```markdown
**Requirement:** CT.CATALOG.SEARCH.1 -- Search for chemicals by name,
CAS number, location, or expiration date range.

**Acceptance Criteria:**
- [ ] Search by partial chemical name returns all matching records
- [ ] Search by exact CAS number returns the specific record
- [ ] Search by storage location returns all chemicals in that location
- [ ] Search by date range returns chemicals expiring within that range
- [ ] Combining multiple criteria narrows results (AND logic)
- [ ] Empty search results display "No chemicals found" message
- [ ] Search results display within 2 seconds for 50,000 records
```

**Rule-based example:**
```markdown
**Requirement:** BR-002 -- Volume discount calculation

**Acceptance Criteria:**

Rule: Discount is calculated on per-SKU order quantity, not total order.
  Example: 50 units of SKU-A -> 0% discount (below 100 threshold)
  Example: 150 units of SKU-A -> 5% discount on all 150 units
  Example: 50 units SKU-A + 100 units SKU-B -> 0% on A, 5% on B
  
Rule: Discount applies to pre-tax unit price.
  Example: SKU-A at $10/unit, 200 units -> $10 * 0.95 * 200 = $1,900
```

### Step 4: Validate Criteria Quality

For each acceptance criterion, verify:
- [ ] A tester can determine pass/fail without asking the BA for clarification
- [ ] The criterion tests one specific condition (not multiple combined)
- [ ] Boundary conditions are covered (what about 29 days? 31 days? exactly 30?)
- [ ] Negative cases are included (what should NOT happen)
- [ ] The criterion traces to the parent requirement

### Step 5: Review with Stakeholders

Walk through acceptance criteria with:
- **Developer** -- "Is this clear enough to implement?"
- **Tester** -- "Can you write test cases from these?" 
- **User** -- "Does this match what you expect the system to do?"

---

## Examples

See `examples/sample.md` for complete acceptance criteria sets.

## Common Pitfalls

### Pitfall 1: No Negative Test Cases
**Symptom:** All acceptance criteria describe what the system *should* do. None describe what it should *not* do.

**Consequence:** Error paths, edge cases, and security concerns are not tested.

**Fix:** For every positive criterion, ask "What should NOT happen?" Add at least one negative criterion per requirement.

---

### Pitfall 2: Criteria Too Vague to Test
**Symptom:** "System responds quickly" or "Data is displayed correctly."

**Consequence:** Tester cannot determine pass/fail. "Quickly" to whom? "Correctly" by what standard?

**Fix:** Quantify: "Response within 2 seconds" and "Displays all 6 fields in the specified order."

---

### Pitfall 3: Criteria Test Implementation, Not Behavior
**Symptom:** "The system uses PostgreSQL to store the record" or "The API returns a 200 status code."

**Consequence:** Criteria are coupled to implementation. If the database changes, the criteria break even though behavior is the same.

**Fix:** Test behavior: "The record is retrievable after save" and "The system confirms successful submission."

## References

### Related Skills
- `user-story-re` -- Acceptance criteria are part of every user story
- `use-case` -- Acceptance criteria can be derived from use case flows
- `business-rule` -- Rule-based criteria often implement business rules
- `requirements-validation-process` -- Acceptance criteria are validated during review

### External Frameworks
- Dan North, "Introducing BDD" (2006) -- Given/When/Then format
- Karl Wiegers & Joy Beatty, *Software Requirements, Third Edition* (2013) -- Chapter 17: Validating the Requirements
- Gojko Adzic, *Specification by Example* (2011) -- Rule-based acceptance criteria

---

**Skill type:** Component
**Dependencies:** None
**Used by:** `user-story-re`, `requirements-validation-process`
