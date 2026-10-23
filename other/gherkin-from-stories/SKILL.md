---
name: gherkin-from-stories
description: "Converts requirements in any input shape into Gherkin scenarios - a user story (\"As a … I want … so that …\"), a signed-off acceptance-criteria list (ATDD: @AC-N-tagged scenarios, NotImplementedError step stubs, AC-to-test traceability table), existing manual test steps (declarative rewrite that strips UI mechanics), or a raw spec / PRD section (acceptance-criteria extraction with Gherkin or plain-list output). Maps criteria to Scenario blocks, detects Scenario Outline opportunities, factors shared Background, reuses the curated step library, and flags implicit preconditions instead of fabricating them. Emits Gherkin (plus stubs in ATDD mode): runner detection and full step wiring belong to bdd-scenario-author. Use whenever requirements text of any shape needs to become a .feature file."
---

# gherkin-from-stories

## Overview

The shift-left flow:

```
Spec / User story → Acceptance Criteria → Gherkin Feature → Step definitions → Tests
```

This skill is the authoring umbrella for the left half of that flow: it
turns requirements text into a `.feature` file. Four input shapes route to
the same core transform:

| Input you have | Section to use | Extra output |
|---|---|---|
| A user story with the As-a / I-want / So-that triple | "From a user story" | - |
| A signed-off, numbered acceptance-criteria list | "From an acceptance-criteria list (ATDD)" | `@AC-N` tags, step stubs, traceability table |
| Already-written manual test steps (TestRail / Qase / Xray export, prose script) | "From manual test steps" | side-by-side rewrite table |
| A raw spec / PRD section with no AC structure yet | "Extracting acceptance criteria from a raw spec" | Gherkin or plain numbered AC list |

Whatever the input, the same core discipline applies: one Scenario per
behavior, Scenario Outline when only data varies, shared Background, step
library reuse, and flag-and-ask on implicit preconditions.

## When to use

- A PM hands over a story, spec, or AC list and the team's first test
  artifact is the `.feature` file.
- The team practices ATDD and gates stories on green acceptance tests.
- A team is migrating manual test scripts (or a whole TestRail / Qase
  library) to BDD.
- A migration from non-BDD to BDD wants to convert existing requirements
  into Gherkin in bulk.

Not this skill: reviewing existing Gherkin for style (use
`gherkin-style-reviewer`); wiring step definitions to a runner end to end
(use `bdd-scenario-author`, which invokes this skill first); non-functional
requirements - perf / a11y / security thresholds have a different shape
(thresholds, not Given/When/Then) - use
`non-functional-requirement-extractor` in the qa-shift-left plugin.

## From a user story

### Step 1 - Extract the user-story triple

```markdown
# Story: Apply promo code at checkout

**As a** logged-in customer
**I want** to apply a promotional code at checkout
**So that** I receive the advertised discount on my order
```

The triple maps to the Feature header:

```gherkin
Feature: Apply promo code at checkout

  As a logged-in customer
  I want to apply a promotional code at checkout
  So that I receive the advertised discount on my order
```

If the story doesn't have the triple, **flag and ask** - a story without
explicit value is a signal the team should clarify before testing.

### Step 2 - Map acceptance criteria to Scenarios

The story body usually has an AC list; each AC becomes a Scenario:

```gherkin
  Background:
    Given I am a logged-in customer
    And my cart contains 1 item at $24.99

  Scenario: Apply valid promo
    Given promo code "WELCOME10" is active
    When I enter "WELCOME10" in the promo input
    And I click "Apply"
    Then the subtotal updates to $22.49
    And a confirmation toast appears: "Code applied"

  Scenario: Apply expired promo
    Given promo code "EXPIRED50" is inactive
    When I enter "EXPIRED50" in the promo input
    And I click "Apply"
    Then an error appears: "This code has expired"
```

### Step 3 - Identify Scenario Outline opportunities

Multiple ACs that vary only in input data become a Scenario Outline - use
one whenever the underlying logic is identical and only the data varies:

```gherkin
  Scenario Outline: Promo validation rejects bad input
    When I enter "<code>" in the promo input
    And I click "Apply"
    Then an error appears: "<error>"

    Examples:
      | code         | error                 |
      | EXPIRED50    | This code has expired |
      | NOTREAL      | Code not found        |
      | (empty)      | Please enter a code   |
      | WELCOME10*2  | Already applied       |
```

## From an acceptance-criteria list (ATDD)

When the input is a signed-off, numbered AC list and the team gates
implementation on green acceptance tests (per ISTQB, ATDD is "a
collaboration-based test-first approach that defines acceptance tests in
the stakeholders' domain language"):

1. **One Scenario per AC**, tagged `@AC-X.Y` - the tag is the load-bearing
   traceability that maps failures back to the criterion.
2. **Tests are written before implementation** - the initial run fails on
   every scenario, and the failing tests are the work backlog.
3. **Scaffold step stubs whose bodies raise `NotImplementedError`** (or
   `PendingException`) so nothing passes silently.
4. **Emit the AC-to-test traceability table** - a 1:1 mapping of AC → test
   → status that answers "did we test what the customer asked for?"
5. **Run via the team's incumbent BDD runner** - never force a runner
   switch alongside test-first adoption.

The full worked feature, stub examples, traceability artifact, per-runner
tag-filter commands, and ATDD-specific anti-patterns:
[references/atdd-traceability.md](references/atdd-traceability.md).

## From manual test steps

When the input is an already-written manual step (table row, prose bullet,
TestRail / Qase / Xray exported step), the job is a declarative rewrite,
not a translation: strip UI mechanics ("clicks the button", "types in the
field"), elevate user intent ("signs in", "adds the product"), and align
vocabulary with the existing step library.

1. **Classify each step**: UI mechanic / state assertion / business action
   / setup / observation. Mechanics and assertions get rewritten; business
   actions pass through; setup becomes `Given`; observations drop into
   step-definition detail.
2. **Apply the rewrite rules** R1-R5: remove UI mechanics, collapse
   multi-step UI sequences into one business action, replace UI properties
   with observable outcomes, choose the right keyword, preserve existing
   vocabulary.
3. **Emit a side-by-side table** (manual step → Gherkin step → keyword →
   justification) so a reviewer can confirm semantic equivalence.
4. **Validate**: at most one `When` per scenario; lint; specificity
   preserved (cart count "1" stays "one item", never "non-empty").

The classification table, the full R1-R5 rule catalog with examples, and
migration-specific anti-patterns:
[references/manual-step-rules.md](references/manual-step-rules.md).

## Extracting acceptance criteria from a raw spec

When the input is a PRD section or feature spec with no AC structure yet,
extract the criteria first, then feed them through the sections above.
Emits two interchangeable shapes: **Gherkin** (for Cucumber / Behave /
Reqnroll / pytest-bdd projects) or a **plain numbered list** (`AC-1`,
`AC-2`, … - consumable by the ATDD section and usable as commit-message
references, e.g. `feat: AC-3 - show toast on save`).

1. **Tag each sentence** as Given (steady state / actor context), When
   (action verbs: "clicks", "submits", "navigates"), or Then (asserted
   outcomes), per the Gherkin reference.
2. **Choose Scenario vs Scenario Outline** - Outline + `Examples:` for
   boundary checks, role variants, status-code matrices.
3. **Factor out Background** for truly shared state (auth, seed data,
   navigation) - only one Background per Feature; don't over-extract
   scenario-specific setup.
4. **Validate observability of every Then.** Reject "Then the user feels
   confident" / "Then the system is secure"; replace with concrete targets:
   a visible `data-testid`, a response status, a header present.
5. **Flag implicit Givens** (below) rather than fabricating.

Three worked examples (simple story, PRD with implicit preconditions,
Scenario Outline opportunity):
[references/spec-extraction-examples.md](references/spec-extraction-examples.md).

## Shared discipline (all input shapes)

### Use existing steps from the library

Per `bdd-step-library-curator`, the team has a curated step library. Use
existing steps where possible:

```gherkin
# Use existing step:
Given I am a logged-in customer

# vs (avoid):
Given I have authenticated to the system   # NEW STEP - duplicates "I am a logged-in customer"
```

Before authoring a new step, search the library README.

### Flag implicit Givens

Requirements often imply preconditions. Flag instead of guess:

```markdown
## ⚠ Implicit Given flags (3)

1. Where does the user enter the promo? `/checkout`? `/cart`?
2. What's the cart state? Empty? Multi-item?
3. Authentication required? Guest checkout supported?

The Gherkin Feature can't be authored without these answers.
```

Flag-and-ask is the load-bearing pattern: silently picking one reading
produces a test suite that misses the paths the author never confirmed.

### Validate Gherkin style

- Declarative steps ("I apply a promo") not imperative ("I click the button
  with id #apply-promo-btn").
- Every Then has an observable outcome.
- No technical leakage (DB names, internal API endpoints, CSS selectors).

### Output

```markdown
## Gherkin scenarios for `<source>`

**Source:** `LIN-1234` (story) | AC list | manual script | PRD section
**Implicit-precondition flags:** N
**Scenarios produced:** M
**Step library reuse:** K of M scenarios use existing steps only.

### Generated Feature
### Implicit-precondition flags
### New steps required

| Step                                          | Why new |
|-----------------------------------------------|---------|
| `Given promo code {code} is active`           | New domain (admin promo state) |

### Recommended next step

After the PM clarifies flagged Givens, author the new step definitions per
`bdd-step-library-curator` conventions and pair with the team's runner
(`cucumber-testing` / `behave-testing` / `reqnroll-testing`), or hand the
whole flow to `bdd-scenario-author`.
```

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Fabricating implicit Givens | Tests pass for the wrong reason; the author never confirmed | Flag-and-ask |
| One Scenario per AC even when they should be an Outline | Test code duplication | Detect outline opportunities |
| Not consulting the step library | Step proliferation; library bloats | Search library first |
| Imperative steps ("click button #foo") | Couples to UI; defeats BDD's value | Declarative ("I apply a promo") |
| Skipping the As-a / I-want / So-that header | Loses the value framing | Triple at the Feature top |
| Then with a verb but no observable target ("Then save") | Not testable | Emit `data-testid` / response status / DOM state |
| Copy-pasted Givens across scenarios | Background extraction missed; brittle suite | One Background block for shared state |

## Limitations

- **Input quality drives output quality.** Vague stories and specs produce
  vague Gherkin (or many flags).
- **Step library dependency.** Without one, every step is "new" and the
  proliferation problem manifests.
- **Doesn't run the tests.** This skill emits Gherkin (plus stubs in ATDD
  mode); pair with the runner skills or `bdd-scenario-author` for the
  runnable artifact.
- **ATDD mode requires the team to write ACs first** and doesn't replace
  lower-layer tests - unit / integration coverage is still needed for
  non-AC logic.

## References

- [references/atdd-traceability.md](references/atdd-traceability.md) - the
  full ATDD workflow: tagged scenarios, red-first, stubs, traceability.
- [references/manual-step-rules.md](references/manual-step-rules.md) - the
  manual-step classification + R1-R5 declarative-rewrite rules.
- [references/spec-extraction-examples.md](references/spec-extraction-examples.md) -
  worked spec-extraction examples.
- Cucumber Gherkin reference (keywords, Outline + Examples, Background
  rules): https://cucumber.io/docs/gherkin/reference
- Cucumber Better Gherkin (declarative vs imperative):
  https://cucumber.io/docs/bdd/better-gherkin/
- ISTQB Glossary V4.7.1 - acceptance criteria
  (https://glossary.istqb.org/en_US/term/acceptance-criteria) and ATDD
  (https://glossary.istqb.org/en_US/term/acceptance-test-driven-development).
- `bdd-step-library-curator` - the step library this skill draws from.
- `bdd-scenario-author` - downstream agent that wires the Feature to a
  detected runner.
