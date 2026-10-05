---
name: feature-specification
model: reasoning
description: Convert persona docs into detailed feature specifications with acceptance criteria. Use when translating user needs into implementable specs, writing user stories, defining acceptance criteria, or preparing features for development.
---

# Feature Specification (Meta-Skill)

Bridge persona documentation and development. This skill translates user needs, pain points, and journeys identified in persona docs into structured, implementable feature specifications with clear acceptance criteria.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install feature-specification
```


---

## Purpose

Persona docs define *who* and *why*. Feature specs define *what* and *how well*. This skill closes the gap:

- Extracts actionable features from persona pain points and journeys
- Structures requirements so developers know exactly what to build
- Defines acceptance criteria so QA knows exactly what to verify
- Prevents scope ambiguity before a single line of code is written

---

## When to Use

- After persona docs exist (`docs/PERSONA.md` or `docs/personas/`)
- Before development begins on a new feature or product
- When a feature request lacks clear acceptance criteria
- When stakeholders disagree on what "done" means
- When converting user feedback into development work

---

## Feature Spec Template

Use this structure for every feature specification. Place specs in `docs/specs/` or `docs/features/`.

```markdown
# Feature: [Feature Name]

## Metadata
- **Priority:** [Must / Should / Could / Won't]
- **Target Persona:** [Persona name from persona docs]
- **Status:** Draft | Review | Approved | In Progress | Complete
- **Estimated Effort:** [T-shirt size: XS / S / M / L / XL]

## Problem Statement
[Directly reference the persona pain point this feature addresses.
Quote or link to the relevant section of persona docs.]

## Solution Description
[High-level description of what the feature does and how it solves
the problem. 2-4 sentences. No implementation details.]

## User Stories

- As a [persona], I want [action], so that [benefit].
- As a [persona], I want [action], so that [benefit].

## Acceptance Criteria

### Scenario: [Happy path description]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario: [Alternative path description]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario: [Error case description]
- **Given** [precondition]
- **When** [invalid action]
- **Then** [error handling result]

## Edge Cases
- [ ] [Edge case 1 — description and expected behavior]
- [ ] [Edge case 2 — description and expected behavior]

## Non-Functional Requirements
- **Performance:** [Response time, throughput, load targets]
- **Accessibility:** [WCAG level, keyboard nav, screen reader support]
- **Security:** [Auth requirements, data sensitivity, input validation]
- **Browser/Device:** [Support matrix]

## Dependencies
- [Feature or system this depends on]
- [External API or service required]

## Out of Scope
- [Explicitly list what this feature does NOT include]
- [Prevents scope creep during development]

## Design References
- [Link to mockups, wireframes, or design system components]
- [Screenshots or diagrams if available]
```

---

## Writing Effective User Stories

User stories connect persona needs to developer tasks. Apply the INVEST criteria:

| Criterion | Meaning | Test Question |
|-----------|--------------------------------------|-------------------------------------------|
| Independent | No ordering dependency on others | Can this be built and released alone? |
| Negotiable | Details can be discussed | Is this a conversation starter, not a contract? |
| Valuable | Delivers value to the persona | Would the persona care about this? |
| Estimable | Team can estimate effort | Is the scope clear enough to size? |
| Small | Fits in a single iteration | Can this ship in one sprint? |
| Testable | Clear pass/fail verification | Can QA write a test for this? |

### Good vs Bad User Stories

| Bad | Why It's Bad | Good |
|-----|-------------|------|
| "Users can log in" | No persona, no benefit | "As a returning customer, I want to log in with my email, so that I can access my order history" |
| "Make it fast" | Vague, untestable | "As a mobile user on 3G, I want the product list to load in under 2s, so that I don't abandon the page" |
| "Add admin panel" | Solution-first, no problem | "As a store manager, I want to update product prices without developer help, so that I can respond to market changes daily" |
| "Handle errors" | No specificity | "As a checkout user, I want clear feedback when my payment fails, so that I know whether to retry or use a different card" |
| "Implement caching" | Implementation detail, not a story | "As a repeat visitor, I want previously viewed pages to load instantly, so that browsing feels responsive" |

---

## Acceptance Criteria Patterns

### Pattern 1: Happy Path

```gherkin
Given a logged-in customer with items in their cart
When they click "Checkout"
Then they are taken to the payment page with their cart summary visible
```

### Pattern 2: Boundary Conditions

```gherkin
Given a cart with 100 items (maximum allowed)
When the user tries to add another item
Then they see "Cart limit reached — remove an item to add a new one"
And the item is NOT added to the cart
```

### Pattern 3: Error Cases

```gherkin
Given a user submitting the registration form
When the email field contains "not-an-email"
Then the form shows inline validation: "Enter a valid email address"
And the form is NOT submitted
And focus moves to the email field
```

### Pattern 4: State Transitions

```gherkin
Given an order with status "Processing"
When the warehouse marks it as shipped
Then the order status changes to "Shipped"
And the customer receives a shipping confirmation email within 5 minutes
And the tracking number is visible on the order detail page
```

### Pattern 5: Negative / Security

```gherkin
Given a user who is NOT the account owner
When they attempt to access /account/settings via direct URL
Then they receive a 403 Forbidden response
And the access attempt is logged
```

---

## Priority Framework

Apply MoSCoW prioritization, anchored to persona impact:

| Priority | Label | Definition | Persona Alignment |
|----------|---------|-----------------------------------------------|------------------------------------------|
| P0 | Must | Product is unusable without this | Blocks the persona's primary goal |
| P1 | Should | Significant value, painful to defer | Addresses a top-3 pain point |
| P2 | Could | Nice to have, enhances experience | Improves a secondary journey |
| P3 | Won't | Explicitly deferred (this release) | Low-frequency need or niche scenario |

**Prioritization process:**

1. List all candidate features
2. Map each to a persona pain point or journey step
3. Assign MoSCoW based on persona impact, not technical interest
4. Validate: Do all P0s together form a usable product for the target persona?
5. Cut scope until P0s are achievable in the timeline

---

## Specification Anti-Patterns

| Anti-Pattern | Example | Fix |
|-------------------------------|------------------------------------------|--------------------------------------------------|
| Vague requirement | "System should be user-friendly" | Define measurable criteria: "Task completion in < 3 clicks" |
| Missing edge cases | Only specifying the happy path | Add boundary, error, and concurrent-use scenarios |
| No acceptance criteria | "Implement search" | Add Given/When/Then for each scenario |
| Solution masquerading as need | "Use Redis for caching" | State the need: "Repeat queries return in < 50ms" |
| Missing personas | "Users can export data" | Specify which persona and why they export |
| Unbounded scope | "Support all file formats" | List exact formats: "PDF, CSV, XLSX" |
| Implicit assumptions | Assuming auth exists without stating it | List all dependencies explicitly |

---

## Integration with Workflow

Feature specs connect to the broader development process:

1. **Persona docs** (`docs/PERSONA.md`) — Source of truth for user needs
2. **Feature specs** (`docs/specs/`) — This skill's output; the development contract
3. **Task creation** — Each spec becomes one or more development tasks
4. **Implementation** — Developers reference the spec for scope and criteria
5. **Testing** — QA derives test cases directly from acceptance criteria
6. **Review** — PR reviews check that acceptance criteria are met

When using with the `/new-feature` command or similar workflows:

- Read the relevant persona doc first
- Generate the spec using this template
- Validate acceptance criteria cover happy path, errors, and edge cases
- Confirm priority with stakeholders before development begins

---

## NEVER Do

1. **NEVER write a spec without referencing a persona** — every feature exists for a user
2. **NEVER skip acceptance criteria** — "obvious" requirements cause the most bugs
3. **NEVER use vague qualifiers as requirements** — "fast", "easy", "intuitive" are not testable
4. **NEVER combine multiple features in one spec** — one spec, one feature, one clear scope
5. **NEVER specify implementation details in user stories** — describe the *what*, not the *how*
6. **NEVER mark a spec as Approved without edge cases documented** — happy paths are the easy part
7. **NEVER assume dependencies are obvious** — list every system, API, feature, and data source the spec relies on
