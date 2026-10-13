---
name: acceptance-criteria
description: Write clear, testable acceptance criteria for user stories using Given/When/Then (Gherkin) format. Define Definition of Ready (story is ready to be worked) and Definition of Done (story is truly complete). Bridges the gap between product intent and QA verification. Includes Jira MCP integration.
triggers:
  - "acceptance criteria"
  - "given when then"
  - "definition of done"
  - "definition of ready"
  - "story criteria"
  - "AC"
  - "gherkin"
  - "how do we know it's done"
audience:
  - qa
  - engineer
  - manager
---

# Acceptance Criteria

Write acceptance criteria that both developers and QAs can act on — no interpretation needed.

---

## Why Acceptance Criteria Fail

Bad AC leads to:
- Developer builds the feature correctly per their interpretation; QA rejects it
- QA doesn't know what to test — tests whatever seems right
- "Done" is declared too early, bugs surface in production
- Rework happens in the last day before release

The fix is criteria written as **verifiable, concrete scenarios** — not general descriptions.

---

## The Given / When / Then Format (Gherkin)

```
Given [a precondition — the system state before the action]
When  [an action the user or system takes]
Then  [the observable outcome]
```

One scenario = one testable path. Write multiple scenarios to cover happy path, error cases, and edge cases.

### Example: User login

```gherkin
Scenario: Successful login with valid credentials
  Given the user is on the login page
  And the user has a registered account with email "user@example.com"
  When the user enters their correct email and password
  And clicks "Sign In"
  Then the user is redirected to the dashboard
  And their name appears in the top navigation bar

Scenario: Login fails with incorrect password
  Given the user is on the login page
  When the user enters a valid email and an incorrect password
  And clicks "Sign In"
  Then an error message "Incorrect email or password" is displayed
  And the password field is cleared
  And the user remains on the login page

Scenario: Account locked after 5 failed attempts
  Given the user has failed to log in 4 times
  When the user fails to log in a 5th time
  Then the account is locked for 15 minutes
  And an email is sent to the registered address with unlock instructions
```

---

## AC Writing Checklist

For every acceptance criterion:
- [ ] **Testable**: Can a QA write an automated or manual test directly from this?
- [ ] **Specific**: No ambiguous words ("fast", "correct", "appropriate", "should work")
- [ ] **Bounded**: Describes one behavior — not "all authentication flows"
- [ ] **Observable**: Outcome is visible to a user or detectable in logs/API
- [ ] **Independent**: Each scenario can be run without depending on another scenario passing

### Words to avoid in AC
| Vague word | Replace with |
|---|---|
| "fast" | "responds in < 500ms at p95" |
| "correct" | "returns [specific value/behavior]" |
| "works properly" | "returns HTTP 200 with [schema]" |
| "appropriate error" | "displays 'Email is required' below the email field" |
| "should handle" | "Given X, When Y, Then Z" |
| "user-friendly" | Not testable — remove or define the UX requirement specifically |

---

## How Many Scenarios Per Story?

| Story complexity | Scenarios |
|---|---|
| Simple, single path | 1-2 (happy path + one error) |
| Feature with multiple states | 3-5 |
| Complex feature with many edge cases | 5-8 (consider splitting the story) |
| > 8 scenarios | Story is too big — split it |

---

## Scenario Coverage Template

For each story, make sure you have scenarios for:

```
✅ Happy path       — the normal, expected flow
✅ Error case       — what happens when input is invalid or something fails
✅ Edge case        — boundary values, empty state, maximum size
✅ Permission/role  — does a user without permission see/do the right thing?
✅ State transition — if the feature has states, test the transitions
```

---

## Definition of Ready (DoR)

A story is **ready to be picked up** when:

- [ ] AC written in Given/When/Then format
- [ ] AC reviewed by QA and at least one engineer
- [ ] UI mockup or wireframe linked (if UI work)
- [ ] API contract defined (if API work)
- [ ] Dependencies identified and unblocked
- [ ] Story sized (story points or t-shirt)
- [ ] No open questions that would block implementation

**If any of these are missing, the story is not ready.** It should not enter the sprint.

---

## Definition of Done (DoD)

A story is **done** when:

- [ ] All acceptance criteria pass (verified by QA or automated tests)
- [ ] Code reviewed and merged to main
- [ ] Unit and integration tests written and passing in CI
- [ ] No regressions introduced (CI green on main)
- [ ] Feature flag configured correctly (if applicable)
- [ ] Documentation updated (README, runbook, API docs — if affected)
- [ ] Deployed to staging and smoke tested
- [ ] PM/QA sign-off (for user-facing changes)
- [ ] No P0/P1 bugs open against this story

**Team DoD vs. Story DoD**: The team should maintain a shared DoD that applies to every story, plus story-specific AC.

---

## AC for Non-Functional Requirements

Don't forget NFRs:

```gherkin
Scenario: Search performance under load
  Given 1000 concurrent users are using the system
  When a user searches for a product by keyword
  Then search results are returned in < 800ms at p95

Scenario: Sensitive data is not logged
  Given a user submits a payment form with card number and CVV
  When the server processes the payment
  Then no card number or CVV appears in application logs or error traces
```

---

## AI-Assisted AC Generation

Use with an agent to draft AC from a story description:

```
Given this user story:
[paste story]

Write acceptance criteria in Given/When/Then format covering:
1. The main happy path
2. At least 2 error/failure scenarios
3. Any edge cases you can identify
4. One non-functional scenario if applicable (performance, security, accessibility)

Flag any ambiguities in the story that need clarification before the AC can be finalized.
```

---

## MCP Integration

### Jira MCP — Write AC back to the story

```
# Update a story with acceptance criteria
jira_update_issue: {
  issue: [PROJ-XXX],
  description: [existing description + AC section in Gherkin format],
  customfield_acceptance_criteria: [AC text]
}

# Query stories missing AC before sprint planning
jira_search_issues: project = [KEY] AND issuetype = Story 
  AND sprint in openSprints() 
  AND "Acceptance Criteria" is EMPTY
  ORDER BY priority DESC
```

### Confluence MCP — Pull requirements to write AC from

```
# Fetch the product spec to extract requirements
confluence_get_page: { page_id: [SPEC-PAGE-ID] }
# → Use the content to draft Given/When/Then scenarios

# Search for existing AC templates in your space
confluence_search: "acceptance criteria template space:PRODUCT"
```

---

## References
- Dan North: [Introducing BDD](https://dannorth.net/introducing-bdd/) (origin of Given/When/Then)
- Martin Fowler: [GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)
- Mike Cohn: [User Stories Applied](https://www.mountaingoatsoftware.com/books/user-stories-applied)
- Gojko Adzic: *Specification by Example*
