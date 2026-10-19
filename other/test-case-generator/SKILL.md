---
name: test-case-generator
description: Use when QA or developers need manual test cases or test scenarios from a requirement, user story, PRD, ticket, acceptance criteria, UI screen or feature description, including negative, boundary and edge cases, in a table or test-management format.
---

# Test Case Generator

## Overview

Turn a requirement into test cases that a tester can run without asking questions, and that would catch the bugs most likely to ship. Cover the happy path once and spend most cases on boundaries, errors and states.

## Method

1. **Extract testable rules** from the input: inputs and their valid ranges, business rules, roles and permissions, states and transitions, integrations, messages shown to users. List ambiguities as questions instead of guessing.
2. **Apply design techniques** to each rule:

| Technique | Use for |
|---|---|
| Equivalence partitioning | One case per class of valid and invalid input |
| Boundary values | min-1, min, min+1, max-1, max, max+1, empty, very long |
| Decision table | Rules that combine conditions (role × plan × status) |
| State transition | Workflows: allowed and forbidden moves between states |
| Error guessing | Duplicates, special characters, emoji, leading/trailing spaces, time zones, double submit, back button, slow network, session expiry |

3. **Add non-functional checks** relevant to the feature: permissions, accessibility basics, responsive layouts, performance with large data, localization.
4. **Write the cases** in the format below. One expected result per case, observable and specific.
5. **Prioritize:** P1 for the core flow and anything touching money, data loss or security; P2 for common variations; P3 for rare edge cases.

## Output format

| ID | Title | Priority | Type | Preconditions | Steps | Test data | Expected result |
|---|---|---|---|---|---|---|---|
| TC-01 | Apply valid coupon at checkout | P1 | Positive | Logged-in user, cart total ₹1,000 | 1. Open cart 2. Enter coupon 3. Click Apply | `SAVE10` | Total shows ₹900; message "Coupon applied" |

Type is one of: Positive, Negative, Boundary, Permission, State, UI, Non-functional.

Then **Coverage summary** (rules → case IDs) and **Open questions** for the product owner.

If the user's team uses a specific tool (TestRail, Zephyr, Xray, Excel), match its columns; for BDD teams write scenarios in Gherkin (`Given / When / Then`).

## Common mistakes

- Ten positive cases and no negative ones.
- Expected results like "works correctly" or "page loads".
- Steps that depend on knowledge only the writer has.
- Combining several checks in one case, so a failure does not show what broke.
- Guessing business rules instead of listing them as open questions.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
