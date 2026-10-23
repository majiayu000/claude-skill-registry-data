---
name: reqnroll-testing
description: "Configures Reqnroll (the canonical .NET BDD framework) - install via `dotnet add package Reqnroll`, author `.feature` files in Gherkin, write step bindings as `[Given/When/Then]`-decorated methods in any C# class, runs via `dotnet test`. Reqnroll is the SpecFlow successor (SpecFlow reached end-of-life 2024-12-31); covers the SpecFlow-to-Reqnroll migration path, and references/specflow-legacy.md maintains not-yet-migrated SpecFlow projects. Use for .NET projects starting BDD, migrating from SpecFlow, or maintaining legacy SpecFlow suites."
---

# reqnroll-testing

## Overview

Per [reqnroll-home][rh]:

[rh]: https://reqnroll.net/

> "**Reqnroll** is described as 'an open-source Cucumber-style BDD
> test automation framework for .NET. It has been created as a
> reboot of the SpecFlow project.'"

The "reboot" framing is the key: SpecFlow's maintenance slowed in
2023; the community forked into Reqnroll, which has continued
active development.

## When to use

- A new .NET project starts BDD - pick Reqnroll over SpecFlow.
- An existing SpecFlow project plans to migrate (SpecFlow-compatible;
  see Step 9).
- The team needs full Gherkin support including Rule blocks
  (per [reqnroll-home][rh]: "Full Gherkin support with tagged
  Rule blocks").

For SpecFlow-locked legacy projects mid-migration (packages, bindings,
EOL background), see
[references/specflow-legacy.md](references/specflow-legacy.md).

## Worked example

A checkout team adds one BDD scenario, "Apply valid promo," to a new xUnit
project.

1. `dotnet add package Reqnroll.xUnit` and
   `dotnet add package Reqnroll.Tools.MsBuild.Generation`.
2. `Features/Cart.feature` declares the scenario under
   `Rule: Promo codes apply only when valid`, with
   `When I enter "WELCOME10" in the promo input` / `Then the subtotal updates
   to $22.49`.
3. `Steps/CartSteps.cs` binds each line - `[When(@"I enter ""([^""]*)"" in the
   promo input")]` calls `_page.EnterPromoAsync(code)`, and the `Then` asserts
   `Assert.Equal(22.49m, _page.GetSubtotal(), 2)`.
4. `dotnet test --filter "FullyQualifiedName~Cart"` runs only that feature.
5. Result: the scenario turns green, and the MSBuild generator has produced the
   runnable test class from the `.feature` file - no glue code beyond the
   bindings.

## Step 1 - Install

```bash
# In the test project directory
dotnet add package Reqnroll.xUnit                    # or Reqnroll.NUnit / Reqnroll.MsTest
dotnet add package Reqnroll.Tools.MsBuild.Generation  # generates code from .feature files
```

Per [reqnroll-home][rh]: "Works across common operating systems
and .NET versions (including .NET 8.0)."

**Verify:** `dotnet build` succeeds and restores both packages before you
author features. If code generation does not run, confirm
`Reqnroll.Tools.MsBuild.Generation` is referenced in the test project.

## Step 2 - Author a Feature

```gherkin
# Features/Cart.feature
Feature: Apply promo code at checkout

  Background:
    Given a logged-in user with email confirmed
    And the cart contains 1 of "BOOK-001" at $24.99

  Rule: Promo codes apply only when valid

    Scenario: Apply valid promo
      When I enter "WELCOME10" in the promo input
      And I click "Apply"
      Then the subtotal updates to $22.49

    Scenario Outline: Reject invalid codes
      When I enter "<code>" in the promo input
      And I click "Apply"
      Then an error appears: "<error>"

      Examples:
        | code       | error                 |
        | EXPIRED50  | This code has expired |
        | NOTREAL    | Code not found        |
```

`Rule:` blocks (Gherkin 6+) group related scenarios; per
[reqnroll-home][rh] this is supported.

## Step 3 - Step bindings

Write step bindings as `[Given/When/Then]`-decorated methods in a `[Binding]`
class. Per [reqnroll-home][rh]: "Supports flexible step definitions using regex
or cucumber expressions" - regex is more flexible, cucumber expressions
(`{int}`, `{string}`, `{double}`) more readable. Full `CartSteps` binding class
and the cucumber-expression variant:
[references/bindings-and-hooks.md](references/bindings-and-hooks.md).

## Step 4 - Async support

Per [reqnroll-home][rh]: "Async step definitions and hooks."

```csharp
[Then("the order arrives within (\\d+) minutes")]
public async Task ThenOrderArrives(int minutes)
{
    await EmailInbox.WaitForOrderConfirmation(TimeSpan.FromMinutes(minutes));
}
```

`async Task` step methods work transparently; no special config.

## Step 5 - Hooks

Use `[BeforeTestRun]`, `[BeforeScenario]` / `[AfterScenario]`, and tag-scoped
hooks (e.g. `[BeforeScenario("@browser")]`) for setup and teardown; wrap each
scenario in a transaction and roll back in `[AfterScenario]` so state does not
leak between scenarios. Full hook class:
[references/bindings-and-hooks.md](references/bindings-and-hooks.md).

## Step 6 - Tags

```gherkin
@critical @regression
Scenario: Apply valid promo
  ...

@browser @wip
Scenario: New checkout flow
  ...
```

```bash
dotnet test --filter "Category=critical"
dotnet test --filter "Category!=wip"
```

## Step 7 - Run

```bash
# All tests
dotnet test

# Specific feature
dotnet test --filter "FullyQualifiedName~Cart"

# Generate JUnit XML for CI
dotnet test --logger "junit;LogFilePath=reports/test-results.xml"
```

If a scenario fails or reports an undefined step, fix the matching binding in
the `[Binding]` class and re-run until it turns green.

## Step 8 - IDE support

Per [reqnroll-home][rh]: "IDE support for Visual Studio 2022, VS
Code, and Rider."

The Reqnroll plugin enables:

- Step navigation (Gherkin → step binding).
- Scaffolding (auto-generate step from undefined Gherkin line).
- Run/debug per-scenario.

## Step 9 - Migrate from SpecFlow

Per [reqnroll-home][rh]: "Compatible with SpecFlow, allowing quick
migration of existing projects."

Migration path:

1. Replace `SpecFlow.*` NuGet packages with `Reqnroll.*` equivalents.
2. Update `using SpecFlow` → `using Reqnroll` (single find/replace).
3. Update `[Binding]` (compatible) and step decorators (mostly
   compatible).
4. Run tests; fix any compatibility issues.

Most SpecFlow projects migrate in <1 day for typical scope.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Starting new .NET BDD with SpecFlow in 2026+                          | SpecFlow's maintenance has slowed; Reqnroll is the active fork.          | Pick Reqnroll (Step 1). |
| Mixing SpecFlow + Reqnroll in one solution                            | Two BDD runners; double maintenance.                                     | Migrate everything (Step 9). |
| Regex-only steps when cucumber expressions would work                  | Less readable; harder to maintain.                                       | Cucumber expressions for typical cases (Step 3). |
| No `[BeforeScenario]` cleanup                                          | State leaks between scenarios.                                           | Per-scenario hook + transaction rollback (Step 5). |
| Sync step methods that block on async                                  | Deadlocks in xUnit / NUnit / MsTest.                                     | `async Task` step methods (Step 4). |

## Limitations

- **Newer than SpecFlow.** Some third-party SpecFlow plugins
  haven't been ported yet.
- **Per-test-framework variant.** xUnit / NUnit / MsTest each have
  their own Reqnroll package; pin matching versions.
- **Gherkin parser quirks.** Some edge cases differ between
  Reqnroll and Cucumber-JVM; cross-port scenarios need verification.

## References

- [rh][rh] - Reqnroll overview: SpecFlow reboot, Gherkin Rule
  blocks, SpecFlow-compatible migration, async hooks, IDE support
  (VS / VS Code / Rider).
- [references/bindings-and-hooks.md](references/bindings-and-hooks.md) - full
  step-binding class, cucumber-expression variant, and hook class.
- [references/specflow-legacy.md](references/specflow-legacy.md) - legacy
  SpecFlow support + EOL background + full migration path.
- `cucumber-testing`,
  `behave-testing` - sibling language
  wrappers.
- `bdd-step-library-curator` - addresses step proliferation.
