---
name: write-spec
description: Use when the user says "write a spec", "/write-spec", "add a feature file", "write a Gherkin spec", "specs for this feature", or asks to capture a feature's behaviour as a Gherkin .feature file (Cucumber/SpecFlow/Behave/pytest-bdd style). Discovers the repo's existing specs folder and conventions, discusses the feature interactively to extract scenarios (golden path, edges, errors), then writes the .feature file matching local style. Pulls context from a related ADR if one exists. Standalone counterpart to /plan-change, which writes ADR + spec together.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Bash(fd:*), Read, Edit, Write, Grep, Glob
---

# write-spec - write a Gherkin .feature file

A Gherkin `.feature` file describes a feature's behaviour in a structured,
human-readable format executable by a BDD test runner (Cucumber, SpecFlow,
Behave, pytest-bdd, godog, etc.). It captures:

- **What** the feature does, from the user's perspective.
- **Who** uses it and **why**.
- **Concrete scenarios** with `Given` / `When` / `Then` steps.
- **Edge cases and error paths**, not just the happy path.

A good spec doubles as documentation and test plan. A bad spec reads like
documentation and tests nothing - usually because scenarios are vague
("user does the thing" rather than "user enters '12345' and clicks 'Submit'").

This skill discovers the repo's conventions, discusses the feature with
the user to draw out scenarios, then writes the `.feature` file in
proper Gherkin.

## Phase 0 - Find existing specs

Hunt for the specs folder. Don't assume a path; the repo will tell you.

```bash
# Common spec folder locations.
for d in specs features test/features tests/features spec/features; do
  if [ -d "$d" ]; then echo "$d"; fi
done

# Fallback: search for .feature files directly.
fd --type f --extension feature . | head -20
```

If you find existing `.feature` files, **read 2-3 of them** to extract
the convention:

- Where do they live? (Use the same directory.)
- What's the naming pattern? (`order-cancellation.feature`,
  `OrderCancellation.feature`, `cancel_order.feature`?)
- Do they have a `Feature:` narrative ("As a … I want … So that …")?
  Some teams include it; others jump straight to scenarios.
- Are `Background` sections used to avoid repeating common `Given`
  steps?
- Is `Scenario Outline` used for parameterized scenarios?
- Are scenarios tagged? (`@smoke`, `@wip`, `@regression`, `@p0`?)
- What's the typical step language style? (`Given the user has X` vs
  `Given a user with X`; past tense vs. present tense; using `When I…`
  for first-person actor or `When the customer…` for third-person.)
- Are there reusable steps in step-definition files? Match the same
  natural-language phrasing so the new scenarios reuse them.

If **no existing `.feature` files**, default to **`specs/`** at the repo
root (the convention the user mentioned), kebab-case file names, with
the full `As a … I want … So that …` narrative. State this default to
the user so they can redirect.

## Phase 1 - Find related context

Before discussing the feature, look for what's already known about it:

```bash
# Related ADR - search by feature keyword.
fd --type f --extension md . docs/adr docs/architecture/decisions 2>/dev/null \
  | xargs rg -l -i '<feature-keyword>' 2>/dev/null

# Related PR / branch description.
gh pr view --json body --jq .body 2>/dev/null
```

If a related ADR exists, read it. ADRs answer "why are we doing this";
the spec answers "what exactly does it do". Don't repeat the ADR - link
to it in a comment at the top of the `.feature` file:

```gherkin
# See docs/adr/0042-order-cancellation.md
```

## Phase 2 - Discuss the feature

A spec written without conversation usually misses the cases that
matter. Pull the substance out before writing.

Cover, in roughly this order:

1. **Feature + actor + goal in one sentence.** "Customers can cancel
   orders placed within the last 24 hours." Multiple actors usually
   means multiple scenarios with different `Given`s.
2. **Golden path - step by step.** What the user does, what the system
   does, what's the visible result. Be concrete: "clicks Cancel" beats
   "interacts with the UI." Include the success state on both sides
   (DB updated / event emitted; toast / redirect / email).
3. **Edge cases** - boundary, auth, authz, concurrency, missing,
   already-acted-on.
4. **Error paths.** Network, validation, downstream service failure.
   What does the user see? What does the system do?
5. **Input variations** - candidates for `Scenario Outline`.
6. **What's NOT in scope.** Often more useful than what is - prevents
   the team assuming coverage that isn't there.

Don't ask everything in one turn. Pick the 2-3 gaps and iterate.

**Concreteness wins.** A scenario like:

```gherkin
Scenario: User does something
  Given the system is set up
  When the user does the thing
  Then it works
```

…is worse than no spec at all - it gives false confidence. Push for
concrete values, observable outcomes, and specific user actions.

## Phase 3 - Draft the spec

Structure each `.feature` file like this:

```gherkin
# Optional: link to ADR / related docs
# See docs/adr/0042-order-cancellation.md

Feature: <short feature title>
  As a <role>
  I want <capability>
  So that <benefit>

  Background:
    # Steps that apply to EVERY scenario in this file.
    # Use sparingly - if it's only common to 2 of 5 scenarios, repeat.
    Given <common precondition>

  @<tag>
  Scenario: <one specific, descriptive title>
    Given <concrete starting state>
    When <one specific action>
    Then <one observable outcome>
    And <next observable outcome>

  Scenario Outline: <parameterized scenarios>
    Given an order placed <age> ago
    When the customer requests cancellation
    Then the response is <result>

    Examples:
      | age      | result    |
      | 1 hour   | success   |
      | 23 hours | success   |
      | 25 hours | rejected  |
```

Drafting guidelines:

- **One Feature per file**, named after the file.
- **Scenarios are independent.** Each starts from its own `Given`; don't
  chain Scenario B onto Scenario A's state.
- **Declarative steps, one `When` per scenario.** `Given the user is
  logged in` beats `Given I navigate to /login, enter "...", click
  Submit`. Multiple `When`s usually means two scenarios glued together.
- **`Then` describes outcomes, not actions.** No HTTP routes, DB tables,
  or CSS selectors - those belong in step definitions.
- **`Scenario Outline` only for genuine parameterization.** Variations
  across one variable - outline. Across multiple unrelated variables -
  separate scenarios.
- **Include negative scenarios.** "User cannot cancel after 24 hours" is
  as important as the positive case, and often forgotten.

Tag conventions (`@smoke`, `@wip`, `@regression`, `@p0`, etc.) live in
`references/gherkin-reference.md`. Match what the repo already uses.

## Phase 4 - Review with the user

Show the draft. Ask:

- "Does the golden path scenario capture how a customer actually uses
  this?"
- "Are the edge cases the ones you'd want to catch in a regression?"
- "Is anything in the spec that *isn't* in the implementation - i.e., are
  we specifying behaviour that doesn't exist yet?"
- "Is anything in the implementation that *isn't* in the spec?"

The last two questions are critical: a spec out of sync with code is
worse than no spec because it lies. If the conversation reveals drift,
flag it but don't fix code in this skill - that's `/review-feature`.

## Phase 5 - Write the file

When the user signs off:

```bash
mkdir -p <specs-dir>
```

Use the `Write` tool. File name: match existing convention.

Commit it separately from code changes - specs deserve their own commit:

```bash
git add <specs-dir>/<file>.feature
git commit -m "spec: <feature title>"
```

(Match the local commit-message style: `git log --oneline -20`.)

## Phase 6 - Verify it parses

If the repo has a BDD runner configured, run a syntax check:

```bash
npx cucumber-js --dry-run <specs-dir>/<file>.feature
# Other runners (behave, pytest-bdd, godog, cucumber-rb) take the same --dry-run flag.
```

A failing dry run usually means a syntax mistake in the `.feature`
file. Fix and re-verify.

If no runner is configured, that's fine - the file is still valid
Gherkin. Mention to the user that a runner can be wired up to make
these executable.

## Operating rules

- **Don't spec a feature that doesn't exist and isn't being built.**
  That's a wishlist. Mark `@wip` if actively in development; otherwise
  put it in `proposals/` if the team uses that pattern.
- **Don't over-specify implementation.** Steps with HTTP verbs, routes,
  or selectors are cURL commands in disguise - lift to a declarative
  step.
- **Don't pad with redundant scenarios.** Same behaviour, different
  inputs - one `Scenario Outline`. Same trivial thing thrice - one
  scenario.
- **Don't skip negative cases.** "What goes wrong" is half the spec.
- **Match local style.** First-person vs third-person voice consistency
  matters; mirror existing specs.

## Composing with other skills

- **`/plan-change`** - writes ADR + spec together. The usual workhorse for new features, refactors, and design-shaped bug fixes.
- **`/backfill-feature`** - writes a characterization spec for existing code that has none.
- **`/write-adr`** - architecture side, standalone.
- **`/review-spec`** - check for overlap / conflict with existing specs.
- **`/review-feature`** - verifies implementation matches the spec.
