---
name: csharp-xunit
description: 'Write, review, or refactor C# unit tests using XUnit v3, NSubstitute, FluentAssertions, and Atc.Test. Use this skill whenever the user asks to create tests, add test coverage, fix failing tests, mock dependencies with NSubstitute, or follow the ClassName_MethodUnderTest_ExpectedBehavior naming convention in a .NET/C# project.'
user-invocable: false
---

# C# Unit Testing with XUnit v3

Follow these practices when writing, reviewing, or refactoring C# unit tests. The stack is XUnit v3 + NSubstitute + FluentAssertions + Atc.Test. Do not use Moq.

When adding tests to an existing project, read nearby test files first and match the established style before applying these defaults.

## Naming and Structure

Name tests `ClassName_MethodUnderTest_ExpectedBehavior` so the test runner output reads like a specification.

Every test follows the Arrange-Act-Assert pattern with explicit comments:

```csharp
[Fact]
public void OrderService_CalculateTotal_ReturnsZero_WhenCartIsEmpty()
{
    // Arrange
    var sut = new OrderService();
    var emptyCart = new Cart();

    // Act
    var result = sut.CalculateTotal(emptyCart);

    // Assert
    result.Should().Be(0m);
}
```

- One behavior per test -- if you need the word "and" in the test name, split it into two tests.
- Keep tests independent and idempotent (runnable in any order).
- Use constructor injection for setup and `IDisposable`/`IAsyncDisposable` for teardown.

## Project Setup

- Test project naming convention: `[ProjectName].Tests`
- Required packages: `Microsoft.NET.Test.Sdk`, `xunit` (v3), `xunit.runner.visualstudio`
- Preferred packages: `FluentAssertions`, `NSubstitute`, `Atc.Test`
- Test class naming: `[ClassUnderTest]Tests` (e.g., `OrderServiceTests` for `OrderService`)
- Run tests with `dotnet test`

## Assertions with FluentAssertions

Prefer FluentAssertions over built-in `Assert.*` because they produce clearer failure messages and read more naturally.

```csharp
// Value equality
result.Should().Be(expected);
result.Should().NotBe(unexpected);

// String assertions
name.Should().StartWith("Order");
name.Should().Contain("active");
name.Should().BeNullOrEmpty();

// Collection assertions
items.Should().HaveCount(3);
items.Should().Contain(x => x.IsActive);
items.Should().BeInAscendingOrder(x => x.Name);
items.Should().BeEmpty();

// Null checks
result.Should().NotBeNull();
result.Should().BeNull();

// Type checks
result.Should().BeOfType<OrderConfirmation>();
result.Should().BeAssignableTo<IConfirmation>();

// Exception assertions
var act = () => sut.Process(null!);
act.Should().Throw<ArgumentNullException>()
   .WithParameterName("order");

// Async exception assertions
var act = async () => await sut.ProcessAsync(null!);
await act.Should().ThrowAsync<ArgumentNullException>();
```

Fall back to built-in `Assert.*` only when FluentAssertions does not cover the scenario.

## Mocking with NSubstitute

Use NSubstitute to create test doubles. The goal is to isolate the system under test from its dependencies so each test verifies exactly one unit of behavior.

```csharp
[Fact]
public async Task OrderService_PlaceOrderAsync_SavesOrder_WhenValid()
{
    // Arrange
    var repository = Substitute.For<IOrderRepository>();
    repository.SaveAsync(Arg.Any<Order>(), Arg.Any<CancellationToken>())
        .Returns(Task.CompletedTask);

    var sut = new OrderService(repository);
    var order = new Order { Id = 1, Total = 99.95m };

    // Act
    await sut.PlaceOrderAsync(order, CancellationToken.None);

    // Assert
    await repository.Received(1)
        .SaveAsync(Arg.Is<Order>(o => o.Id == 1), Arg.Any<CancellationToken>());
}
```

Key patterns:
- `Substitute.For<T>()` to create mocks from interfaces
- `.Returns(value)` and `.ReturnsForAnyArgs(value)` to configure return values
- `.Received(n)` / `.DidNotReceive()` to verify interactions
- `Arg.Any<T>()`, `Arg.Is<T>(predicate)` for argument matching
- Pass `CancellationToken` through -- never drop it silently

## Data-Driven Tests

Use `[Theory]` when the same logic needs to be verified against multiple inputs.

```csharp
[Theory]
[InlineData(0, 0, 0)]
[InlineData(1, 2, 3)]
[InlineData(-1, 1, 0)]
public void Calculator_Add_ReturnsExpectedSum(int a, int b, int expected)
{
    // Arrange
    var sut = new Calculator();

    // Act
    var result = sut.Add(a, b);

    // Assert
    result.Should().Be(expected);
}
```

- `[InlineData]` for simple inline values
- `[MemberData(nameof(TestData))]` for method/property-based data (useful when data is complex or reused)
- `[ClassData(typeof(MyTestData))]` for class-based data sources
- Use meaningful parameter names so failure output is self-explanatory

## Async Test Patterns

XUnit v3 supports async tests natively -- return `Task` and use `async`/`await`:

```csharp
[Fact]
public async Task UserService_GetByIdAsync_ReturnsNull_WhenUserNotFound()
{
    // Arrange
    var repo = Substitute.For<IUserRepository>();
    repo.GetByIdAsync(Arg.Any<int>(), Arg.Any<CancellationToken>())
        .Returns((User?)null);
    var sut = new UserService(repo);

    // Act
    var result = await sut.GetByIdAsync(999, CancellationToken.None);

    // Assert
    result.Should().BeNull();
}
```

- Always pass and propagate `CancellationToken` in async method signatures
- Use `await act.Should().ThrowAsync<T>()` for async exception testing

## Atc.Test Utilities

The `Atc.Test` package provides helpers that reduce test boilerplate. Leverage it for common testing utilities and assertions when available in the project.

## Test Organization

- Group tests by feature or component
- Use `IClassFixture<T>` for shared context within a test class (e.g., database setup)
- Use `ICollectionFixture<T>` for shared context across multiple test classes
- Use `[Trait("Category", "CategoryName")]` for categorization and selective test runs
- Use `ITestOutputHelper` for diagnostic output during test execution
- Skip tests conditionally: `[Fact(Skip = "reason")]` or `[Theory(Skip = "reason")]`

## Edge Cases to Cover

Good test suites include tests for boundary conditions:
- Null inputs and empty strings
- Empty and single-element collections
- Min/max boundary values
- Concurrent access scenarios (where relevant)
- Exception and error handling paths
