---
name: define-behavior
description: >
  Writes behavior-driven features and scenarios in Gherkin (`.feature` files) that read as
  specification by example: domain-level, one behavior per scenario, observable outcomes. Use this
  skill whenever the user wants to author or refine Gherkin, BDD scenarios, acceptance criteria,
  Given/When/Then steps, feature files, or Cucumber, SpecFlow, or Behave specs. Use it even when the
  user describes the behavior in plain prose and never says "Gherkin". Use it also to turn a ticket,
  a user story, or acceptance criteria into scenarios, and to clean up scenarios that leak UI, API,
  or database mechanics. Do not use it to write the automation code behind the steps, which is a
  separate concern.
argument-hint: "[feature description, ticket, or path to a .feature file]"
allowed-tools: [Read, Glob, Grep, Edit, Write, AskUserQuestion]
---

# Define Behavior

BDD runs on three practices. **Discovery** asks what the system *can* do, through a conversation about concrete examples. **Formulation** states what the system *must* do, by capturing those examples as Gherkin. **Automation** shows what the system *actually* does, by wiring the scenarios to code. This skill lives in formulation and leans on discovery. Liz Keogh puts the order this way: "having conversations is more important than capturing conversations is more important than automating conversations."

Gherkin describes what a system does for a user, in the terminology of the problem domain. It does not describe how the system is built or tested. A team that writes Gherkin together builds a shared language for the system, and that language runs all the way down into the code. A good feature file is an executable specification that anyone on the team can read and agree on, and it survives as living documentation. Each scenario is a concrete and believable example of one behavior.

## Discover before you formulate

Good scenarios come out of a conversation, not out of a lone author. Real BDD discovery is a workshop where three perspectives meet. The Product Owner sets the scope, which is what is in and what is out. The Tester brings the edge cases and the ways the behavior breaks. The Developer brings the details that each rule implies.

You will often work alone from a work item, so play all three roles on purpose. Map what the user gave you the way Example Mapping does. The input is a work item, a user story, prose, existing `.feature` files, or related code.

- **Rules**: the business rules and acceptance criteria that the behavior must satisfy. Each rule anchors one or more scenarios. Where the tool supports it, a rule can group its scenarios under a Gherkin `Rule:` keyword.
- **Examples**: one concrete and believable case for each rule. Each example becomes a scenario. Cover the unhappy paths as well as the happy one, because a missing edge case is the most common gap.
- **Questions**: anything load-bearing that is unclear or assumed. A wrong assumption produces a scenario that looks confident and specifies nothing useful. Raise each question and **ask rather than guess**.

Also settle three more things. Settle the actor, which is the role that uses the capability. Settle any precondition that several scenarios share, because that precondition is a `Background` candidate. Settle whether the user wants tight single-behavior scenarios, which is the default, or a journey that spans several steps, which you write only on request.

Too many questions cost less than invented requirements. A short clarifying exchange is cheaper than a feature file that specifies the wrong thing.

## How to write each part

**File and feature.** Write one `Feature` per file. Name the file in kebab-case, aligned with the feature title, with the `.feature` extension. Indent the body by 2 spaces. Put a short user story under the title, so the value is explicit:

```gherkin
Feature: Discount codes at checkout
  As a shopper
  I want to apply a discount code to my order
  So that I pay the reduced price I was promised
```

**Scenarios, one behavior each.** Each scenario targets a single behavior, and it must run independently of the others. Give it a one-line title that names the behavior, which is what is true, not "test X". Keep the scenario short. If it runs past roughly 10 steps, or if it needs a second `When`, it is probably two scenarios. Map the keywords to Arrange, Act, and Assert, and keep them in that order:

- `Given` sets up the context. Prefer a meaningful state, such as "Given Ada is signed in as an Editor", over an imperative tour of clicks. Include only the preconditions that the reader needs.
- `When` performs the single action under test. Write one `When` per scenario. Extra data belongs in `Given`, not in more `When` steps.
- `Then` asserts an observable outcome: what changed, what the user sees, or what the system reports. Never write "it works", and never write "the user is logged in" with no visible signal.

Use `And` and `But` to extend a step type. Never use `Or`, because a branch means two separate scenarios. Write steps in the third person and the present tense, with string values in double quotes.

**Stay at the domain level.** Steps describe what the actor does and what the system does, in the terminology of the problem domain. Selectors, XPaths, URLs, "wait 2 seconds", HTTP verbs, SQL, and the internal schema do not belong in step text. The one exception is a behavior that is genuinely about that layer, such as a scenario about an API contract. Leaked mechanics couple the specification to one implementation, and they make it unreadable to people outside engineering. Two tests keep steps at the right altitude:

- **Implementation-change test**: ask whether this wording has to change when the implementation changes. The change can be a UI redesign, a move from REST to GraphQL, or a new login method. If the answer is yes, the step sits too low. Rewrite it in terms of intent.
- **1922 test**: ask whether you can describe this step to someone who worked before computers existed. Most software automates something that a person once did by hand. That phrasing strips out the technical assumptions and leaves the real business behavior.

**Use concrete and realistic data.** Believable values such as €80, "SPRING10", and "Editor" make the scenario read as a real specification. Do not use `foo`, `bar`, or `test` placeholders, unless the scenario is deliberately about garbage or invalid input.

**Background, Outline, and tables, only when they earn it.**

- `Background`: write at most one per feature, and only for state that several scenarios share. When a single scenario needs the state, put it in the `Given` of that scenario.
- `Scenario Outline` with `Examples`: use it only when one behavior runs with several input variations. When the inputs do not change the behavior, a plain `Scenario` is clearer.
- Step data tables and `Examples` tables: use them in place of long `And` chains. Keep the headers concise, and keep each table to roughly one screen. A table that grows without bound is a sign that the scenario is drifting into pure data-driven testing.

Hold to one shared language across the file. Use the same term for the same role, object, or state every time, and reuse the words that the business already uses. Do not swap "order", "purchase", and "cart" for one thing, unless the product truly distinguishes them.

## Examples

**Leaked UI mechanics, rewritten as domain-level state and action.** The "before" version is brittle and unreadable. The "after" version specifies the same behavior in product language.

```gherkin
# Before: imperative, mechanical, no clear behavior
Scenario: Login test
  Given I open "https://app.example.com/login"
  When I type "ada@example.com" into "#email"
  And I type "hunter2" into "#password"
  And I click "#submit"
  And I wait 2 seconds
  Then I see "Dashboard"

# After: declarative, observable, one behavior
Scenario: Registered user reaches their dashboard after signing in
  Given Ada is a registered user with the "Editor" role
  When she signs in with valid credentials
  Then she sees her personal dashboard
```

**Two behaviors in one scenario, split so each has an observable outcome.**

```gherkin
# Before: two behaviors, a second When, a vague assertion
Scenario: Discount code
  Given a shopper has €80 of items in their cart
  When they apply the code "SPRING10"
  Then it works
  When they apply the code "BOGUS"
  Then there is an error

# After: one behavior per scenario, concrete observable results
Scenario: Valid code reduces the order total
  Given a shopper has €80 of items in their cart
  When they apply the code "SPRING10"
  Then the order total drops to €72

Scenario: Unknown code is rejected and leaves the total unchanged
  Given a shopper has €80 of items in their cart
  When they apply the code "BOGUS"
  Then the code is rejected with the message "We don't recognize that code"
  And the order total stays at €80
```

**Input variations of one behavior, written as a `Scenario Outline`.**

```gherkin
Scenario Outline: Password strength is enforced at sign-up
  Given a visitor is creating an account
  When they set their password to "<password>"
  Then the password is "<verdict>"

  Examples:
    | password        | verdict  |
    | short           | rejected |
    | correcthorse42  | accepted |
```

## Before you finish

Re-read the draft as a skeptical teammate. Do not re-check every rule above. Hunt the four failures that survive a first pass:

- A business rule from discovery with no scenario, or an assumption you guessed instead of asking about.
- A scenario that smuggles in a second behavior or a second `When`. A `Then` with no observable signal, such as "it works" or "the user is logged in".
- A step that breaks when the implementation changes: a selector, a URL, a wait, or SQL that fails the implementation-change test.
- Drifting vocabulary, where one role, object, or state carries two different names.
