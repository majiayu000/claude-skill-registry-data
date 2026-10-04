---
name: implement-scenarios
description: >
  Implements automated tests for Gherkin scenarios (`.feature` files) that already exist, the BDD
  way: outside-in and client-first. Classifies the best testing strategy for each scenario, writes
  the test that binds to it, watches that test fail for the right reason, then drives the UI, the
  API, and the domain code until it passes. Use whenever the user has `.feature` files and wants to
  automate, implement, wire up, or "make pass" their scenarios. Use it to turn Gherkin, BDD,
  SpecFlow, Reqnroll, or Cucumber specs into real xUnit, NUnit, Vitest, Jest, pytest, or Playwright
  tests, to build a feature test-first (TDD) from acceptance criteria, to decide which scenarios
  belong in unit, service (Testcontainers), or end-to-end tests, or to keep a traceability link
  between scenarios and the tests that verify them. Use it even when the user never says "BDD" or
  "TDD". To author or refine the Gherkin itself, use define-behavior. To reconcile a suite of
  feature files against each other, use review-feature-suite.
argument-hint: "[path to a .feature file or features directory]"
allowed-tools: [Read, Glob, Grep, Edit, Write, Bash, AskUserQuestion]
---

# Implement Scenarios

BDD runs on three practices. **Discovery** finds what the system can do. **Formulation** captures it as Gherkin. **Automation** wires the scenarios to code, so that you know what the system actually does. `define-behavior` lives in formulation. This skill is automation.

This skill takes `.feature` files that already exist and makes them executable, working outside-in. For each scenario, write the test that proves the behavior *before* you write the code that delivers it. Then build inward until the test passes. The TDD discipline states the reason: if you did not watch the test fail, you do not know that it tests the right thing.

Your distinctive job covers the three things that generic TDD leaves out. **Classify** each scenario to the testing strategy that verifies it most cheaply. **Bind** a test to it through a stable identifier. **Trace** the link, so anyone can see which scenarios are covered. The inner red-green loop that grows the production code is ordinary TDD. Drive it well, but remember that the taught core of this skill is classify, bind, and trace, not unit testing.

Work in two phases, and keep them separate. First classify the whole suite and get sign-off. Then implement one scenario at a time. Planning benefits from the global view, and implementation must not use it. A run that writes every test up front and then all the code slices the work horizontally. It produces tests that verify imagined behavior instead of real behavior. Build vertical slices instead, and take one scenario fully from red to green before you start the next.

## Orient before you automate

The findings that shape every later decision come from the project, so read the project before you touch anything.

**Steering.** Scan the repo root, `docs/`, and any harness steering directory, such as `.claude/rules/`, `.cursor/rules/`, and `.kiro/steering/`. Look for standards-style files that match `*standards*.md`, `*conventions*.md`, `testing-*.md`, and `api-*.md`. Read every file you find. These define the team's preferred test pyramid, frameworks, and conventions. When sources disagree, an explicit steering document wins, then the repo's existing conventions, then the defaults below. A steering doc can contradict what the codebase does, for example when the doc names NUnit and every project references xUnit. In that case, **put the conflict in front of the user**. Do not introduce a second framework in silence, because a project almost never wants both.

**Stack and tooling.** Detect the language, the test frameworks, and any Gherkin runner already in use, such as SpecFlow, Reqnroll, cucumber-js, behave, or godog. Read the manifests: `*.csproj`, `package.json`, `pyproject.toml`, and `go.mod`. Read the existing test setup too. What the project already does is a stronger and more current signal than any default.

**Greenfield or brownfield.** Inspect the repo to tell the two apart. Brownfield means that an app already exists, and it is the common case. In brownfield, follow the established architecture, and add the behavior plus its bound test. Greenfield means that little or no app exists yet, and it needs a **walking skeleton first**. Get the thinnest end-to-end path to compile and run before you drive the first scenario. Then the first acceptance test fails on a real assertion instead of on "nothing builds".

**Current coverage.** Build the trace matrix, described under *Traceability*. It tells you which scenarios are covered, which are unverified, and which references are orphaned. A re-run is incremental: work the uncovered and unverified scenarios, and leave the covered ones alone.

## Make sure that each scenario can be automated

The `.feature` files are authoritative input. This skill does not author or rewrite them. A scenario with no observable outcome, such as "Then it works", cannot bind to an honest assertion. Neither can a scenario that smuggles in two behaviors. A forced binding yields a test that passes and verifies nothing.

Run a light automatability check only. Ask three questions. Is there an observable `Then`? Is this a single behavior? Is it stated in domain terms instead of pure UI mechanics? When a scenario fails the check, **stop and refer it back to `define-behavior`**, because fixing Gherkin is the job of that skill. The only edit that this skill ever makes to a `.feature` file is the identity tag of a scenario. Never edit the steps.

## Phase 1: Classify the whole suite

Classify every scenario. Then present the plan and get sign-off before you write any code. Misclassification is expensive, because a slow and brittle end-to-end test in place of a unit test costs time on every future run. The global view lets the user catch that cheaply.

Reason about a bottom-up ladder, and pick the **lowest rung that genuinely verifies the behavior**:

- **unit**: behavior that lives in domain logic, such as a calculation, a rule, or a state transition. Test the domain service in-process, with no infrastructure.
- **service**: behavior that exists only across real adapters, such as persistence, messaging, or a real HTTP boundary. Test through the service with its real dependencies, through Testcontainers.
- **e2e**: a genuine user journey whose value is the path through the UI. Drive it with Playwright.

Steering can add rungs, such as consumer-driven contract tests or UI component tests. Fold them into the same bottom-up reasoning. The principle stays constant: push the test down until one more step down stops verifying the behavior.

Bind **exactly one** test to each scenario, at its chosen rung. The extra unit tests that you write while you build the code in Phase 2 are inner-loop tests. Leave them unbound. Otherwise the matrix balloons, and you have rebuilt the inverted pyramid.

Present the classification as a table that the user can correct. Give one row per scenario, with the chosen rung, a one-line rationale, and the framework. Add the resulting distribution, which is the count of unit, service, and end-to-end tests, because the shape of that distribution is itself a signal. Use `AskUserQuestion` to confirm the plan and to resolve any scenario that you found genuinely ambiguous. Carry the answers into Phase 2.

## Phase 2: Implement one scenario at a time

For each scenario, in order, run the full outside-in loop before you move to the next one:

1. **Backfill identity.** If the scenario carries no `@SCN-NNNN` tag, add one, with the next free number in the suite. Never alter an existing ID. Its whole purpose is to survive a change of title or wording.
2. **Write the bound test, at the classified rung.** Reference the ID of the scenario through the idiomatic carrier of the language, described in the convention below. Where the project already runs Gherkin, through Reqnroll, cucumber-js, or behave, write step bindings, so the `.feature` file stays executable living documentation. Otherwise write a plain test that re-expresses the behavior in code and carries the ID. Default to the plain test. Do not impose a Cucumber runner on a project that has none.
3. **Watch it fail for the right reason.** Run the test. A real assertion failure is the goal. A compile error, or a "type not found" error, proves nothing about the behavior. In greenfield, the walking skeleton is what makes a real failure possible.
4. **Drive the implementation inward.** Build the UI or API surface that the test needs, then the domain code. Grow it with an ordinary inner red-green loop. Lean on TDD practice here, and keep those inner unit tests unbound.
5. **Watch it pass.** Run the bound test green, with the rest of the suite still green. Only then move to the next scenario.

**Honest fallback.** Sometimes the infrastructure for a rung cannot start in this environment. That happens when Docker is absent for Testcontainers, and when no browser or running app exists for Playwright. Generate the test, and mark the scenario **unverified** in the report. Never claim a green result that you did not witness. An unverified but honest result is worth more than a fake pass.

A `Scenario Outline` is one behavior with varied data. Give it a single `@SCN` tag, and bind one data-driven test that covers every row of `Examples`. The per-case output of the runner identifies a failing row, so the rows need no separate IDs.

## The scenario-to-test convention

The link is deliberately independent of any Gherkin runner. A stable ID sits on the scenario, and the test carries the same literal ID. Extraction is then a single ripgrep, whatever the language.

```gherkin
@SCN-0042
Scenario: Unknown code is rejected and leaves the total unchanged
  ...
```

```
C#       [Trait("covers", "SCN-0042")]   or a [ScenarioRef("SCN-0042")] attribute
TS/JS    //@covers SCN-0042   (Playwright also: test("...", { tag: "@SCN-0042" }, ...))
Python   @pytest.mark.covers("SCN-0042")   or  # covers: SCN-0042
Go       // covers: SCN-0042
```

The idiomatic carrier serves the team and their tooling. The **literal ID string is the contract** that the matrix relies on.

## Traceability

The trace matrix is a **derived view**, never a file kept up to date by hand. The source of truth is the set of `@SCN` tags in the `.feature` files, plus the ID references in the tests. So the view cannot drift out of sync. Regenerate the matrix on demand by reconciling two ripgrep passes:

- Scenario IDs across the `.feature` files, plus the scenarios that carry no tag.
- ID references across the test tree.

Report each scenario in one of five states. **Covered** means that a bound test exists and is green. **Unverified** means that the test exists and failed to run here. **Uncovered** means that no bound test exists yet. **Orphaned-ref** means that a test references an ID that no scenario has. **Drifted** means that the text of the scenario changed after its bound test was written.

Drift is a flag for the user to judge, not something to fix automatically. A test rewritten in silence to match a changed specification hides a decision that belongs to the user. Keep this reconciliation as ripgrep plus judgment. Extract a script only once you watch several runs re-derive the same reconciliation.

## Default frameworks

In greenfield, with nothing to detect, scaffold with the mainstream choice for the stack. Detection and steering always override these defaults. Use xUnit for C#, and pytest for Python. Use Vitest for TS and JS, or Jest when Jest is already present. Use the standard `testing` package for Go. Use Testcontainers for the service rung and Playwright for end-to-end tests, across every stack.

## Before you finish

Re-read your work as a skeptical teammate, and hunt the failures that survive a first pass:

- A bound test that you never watched go from red to green, or one marked green when its infrastructure never started.
- A test that passes and asserts nothing, because its scenario had no observable outcome and you papered over the gap instead of referring it back.
- A scenario pushed up to end-to-end, or down to unit, when a different rung verifies the same behavior more cheaply or more honestly.
- An inner-loop unit test tagged with a scenario ID by accident, which inflates the matrix.
- A regenerated matrix that disagrees with reality, through an orphaned reference, an uncovered scenario, or drift that you did not report.
- A conflict between steering and the codebase that you resolved in silence instead of putting in front of the user.
