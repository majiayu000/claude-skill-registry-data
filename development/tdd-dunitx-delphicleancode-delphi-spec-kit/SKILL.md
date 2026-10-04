---
name: Delphi Test-Driven Development (TDD) and DUnitX
description: Guidelines on how the AI ​​should act and code when the user requests TDD, unit tests, DUnitX or fakes/mocks using Interfaces in Delphi.
---

# Test-Driven Development (TDD) in Delphi with DUnitX

This skill guides behavioral expectations for test-driven development (TDD) using the modern Delphi ecosystem.

When operating under the scope of TDD, AI MUST ALWAYS prioritize the **Red-Green-Refactor** cycle. If the user requests TDD, DO NOT write the business implementation before writing the test that will fail.

## The Red-Green-Refactor Cycle (Interaction Rules)

1. **Red (Failed Test):** Start by declaring the skeleton of the target class/interface in the `interface` section just to compile. Then, immediately write a complete DUnitX Test Case calling out the non-existent behavior or asserting an expected result. The test will logically fail.
2. **Green (Minimal Code):** Write the minimum and raw actual implementation, enough to make the test `Assert` pass.
3. **Refactor (Cleaning):** Improve the code (Clean Code, duplication removal, optimizations) ensuring that the test does not break.

## DUnitX Best Practices

### Test Structure
- **Test Class:** The test case must be annotated with `[TestFixture]`.
- **Setup and TearDown:** Use `[Setup]` to instantiate Classes and Fakes. Use `[TearDown]` to clean up instances that do not use ARC (Interfaces).
- **No Memory Leaks in Tests:** `[TearDown]` and injection via Interface (ARC) are mandatory to keep the suite watertight.

### Nomenclature of Test Methods
Embrace context conventions like **Action_Condition_ExpectedResult**:
```pascal
[Test]
procedure ComputeDiscount_LoyalCustomer_ReturnsTenPercent;
```

### Modern Assertions
Replace manual Boolean validations (`Assert.IsTrue(A = B)`) with fluent and specific `Assert`:
- `Assert.AreEqual(100.0, FInvoice.Total)`
- `Assert.IsNotNull(FCustomer)`
- `Assert.WillRaise(procedure begin FSut.DoInvalid; end, EBusinessRuleException)`
- `Assert.Contains('Error', LMessage)`

### Dependency Injection and Mocks (Test Doubles)
To isolate the class under test (SUT - System Under Test) from the infrastructure (Database, APIs, View), apply **Strict Dependency Inversion (DIP)** by injecting `Interfaces` into the SUT via constructor.

As Delphi does not have a built-in Mocking Framework in RTL, write local "Fake/Mock" Classes implementing the Interface to simulate the dependency within the test's `implementation` session.

```pascal
//Fake is created only in the test file
TFakeEmailService = class(TInterfacedObject, IEmailService)
public
  SentCount: Integer;
  procedure Send(const AMsg: string);
end;
```

## AntiPatterns that AI should Avoid

1. ❌ Direct coupling to the database (`TFDQuery`) in the tested class. Always abstract database access into a `IRepository` and create a `TFakeRepository` for DUnitX.
2. ❌ Test UI. Restrict the scope of DUnitX to the Domain and Application Services Layer.
3. ❌ Write the entire class along with the tests. The user must be followed step-by-step in TDD. If the AI ​​is required to provide everything, send the Tests first in the output.
4. ❌ Swallowing Exceptions (`try..except on E: Exception do`) in methods being tested, this breaks `Assert.WillRaise()`.
