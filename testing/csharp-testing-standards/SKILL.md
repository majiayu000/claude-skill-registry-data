---
name: csharp-testing-standards
description: Defines the testing standards, patterns, and conventions for all C# unit and integration test projects. Rules cover test framework usage, naming, structure, mocking, assertions, and parameterization. Apply these rules uniformly across all test projects.
metadata:
  version: 1.1.0
---

# C# Testing Standards

## Description

Defines the testing standards, patterns, and conventions for all C# unit and integration test projects. Rules cover test framework usage, naming, structure, mocking, assertions, and parameterization. Apply these rules uniformly across all test projects.

---

## 1. Framework & Tooling

- **Test framework**: NUnit 3
- **Mocking**: Moq
- **Coverage**: coverlet.collector
- **Test runner**: `Microsoft.NET.Test.Sdk` + `NUnit3TestAdapter`

Core NUnit attributes in use:

| Attribute | Purpose |
|---|---|
| `[TestFixture]` | Marks the test class |
| `[Test]` | Marks a single test method |
| `[SetUp]` | Runs before each test |
| `[TearDown]` | Runs after each test |
| `[OneTimeSetUp]` | Runs once before all tests in the fixture |
| `[TestCase]` | Parameterized test inline values |

---

## 2. Test Class Structure

### 2.1 Visibility

Test classes are `internal`. They do not need to be `public` – NUnit discovers them via the test runner regardless.

```csharp
[TestFixture]
internal class OrderServiceTests { }
```

### 2.2 System Under Test Field

Name the field under test `_sut` (system under test) and initialize it in `[SetUp]`:

```csharp
private OrderService _sut = null!;
```

### 2.3 Mock Fields

Declare all mocks as class-level fields initialized in `[SetUp]`:

```csharp
private Mock<IOrderRepository> _orderRepositoryMock = null!;
private Mock<ILogger<OrderService>> _loggerMock = null!;
```

### 2.4 SetUp Method

- Initialize all mocks and the SUT in the `[SetUp]` method.
- Configure **happy-path** default behaviors here so individual tests only override what they specifically need.
- Keep `[SetUp]` focused – it should not contain assertions or complex logic.

```csharp
[SetUp]
public void Setup()
{
    _orderRepositoryMock = new Mock<IOrderRepository>();
    _orderRepositoryMock
        .Setup(r => r.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()))
        .ReturnsAsync((Order?)null);

    _sut = new OrderService(
        _orderRepositoryMock.Object,
        NullLogger<OrderService>.Instance);
}
```

---

## 3. Test Method Naming

### 3.1 Pattern

```
MethodName_WhenCondition_ThenExpectedBehavior
```

- **MethodName** – the method being tested (must match the implementation exactly).
- **WhenCondition** – the specific input state or pre-condition being exercised.
- **ThenExpectedBehavior** – the exact outcome that is asserted.

```csharp
// ✅ Correct
public async Task GetByIdAsync_WhenOrderDoesNotExist_ThenReturnsNull()
public async Task CreateAsync_WhenRequestIsValid_ThenPersistsAndReturnsSuccess()
public void Validate_WhenAmountIsNegative_ThenReturnsInvalidResult()

// ❌ Wrong – vague and non-descriptive
public async Task TestGetOrder()
public async Task CreateOrder_Success()
```

### 3.2 Async Test Methods

All async test methods that are `async Task` must also follow the `Async` suffix rule:

```csharp
// ✅ Correct
public async Task CreateAsync_WhenRequestIsValid_ThenReturnsSuccess()

// ❌ Wrong
public async Task Create_WhenRequestIsValid_ThenReturnsSuccess()
```

---

## 4. Arrange / Act / Assert

Every test body must follow the three-section AAA structure, with explicit comments:

```csharp
[Test]
public async Task GetByIdAsync_WhenOrderExists_ThenReturnsOrder()
{
    // Arrange
    var orderId = Guid.NewGuid();
    var order = new Order { Id = orderId, CustomerName = "Alice" };
    _orderRepositoryMock
        .Setup(r => r.GetByIdAsync(orderId, It.IsAny<CancellationToken>()))
        .ReturnsAsync(order);

    // Act
    var result = await _sut.GetByIdAsync(orderId, It.IsAny<CancellationToken>());

    // Assert
    Assert.That(result, Is.Not.Null);
    Assert.That(result!.CustomerName, Is.EqualTo("Alice"));
}
```

---

## 5. Assertions

### 5.1 Constraint Model

Always use `Assert.That(actual, constraint)` – the NUnit constraint model. Avoid the classic assertion API:

```csharp
// ✅ Correct – constraint model
Assert.That(result, Is.Not.Null);
Assert.That(result.IsValid, Is.True);
Assert.That(result.Message, Is.Null);
Assert.That(items, Has.Length.EqualTo(2));
Assert.That(items, Is.EquivalentTo(expected));

// ❌ Avoid – classic API
Assert.IsNotNull(result);
Assert.IsTrue(result.IsValid);
Assert.AreEqual(2, items.Length);
```

### 5.2 Exception Assertions

Use `Assert.ThrowsAsync<T>` for async methods that are expected to throw:

```csharp
Assert.ThrowsAsync<ArgumentNullException>(
    () => _sut.CreateAsync(null!, It.IsAny<CancellationToken>()));
```

### 5.3 Mock Verification

Use `.Verify()` only when asserting that a side-effecting call was (or was not) made. Do not use `.Verify()` as a substitute for return value assertions:

```csharp
// ✅ Correct – asserting a save was triggered exactly once
_orderRepositoryMock.Verify(
    r => r.SaveAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()),
    Times.Once);

// ✅ Correct – asserting a call was never made
_orderRepositoryMock.Verify(
    r => r.DeleteAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()),
    Times.Never);
```

---

## 6. Parameterized Tests

Use `[TestCase]` for boundary values (null, empty, whitespace, zero, negative) rather than duplicating test logic:

```csharp
[TestCase(null!)]
[TestCase("")]
[TestCase("   ")]
public async Task CreateAsync_WhenCustomerNameIsEmpty_ThenReturnsFailure(string customerName)
{
    // Arrange
    var request = new CreateOrderRequest { CustomerName = customerName };

    // Act
    var result = await _sut.CreateAsync(request, It.IsAny<CancellationToken>());

    // Assert
    Assert.That(result.IsValid, Is.False);
}
```

For multiple varying inputs, prefer `[TestCaseSource]` over stacking many `[TestCase]` attributes:

```csharp
private static IEnumerable<TestCaseData> InvalidAmounts()
{
    yield return new TestCaseData(0m).SetName("Zero");
    yield return new TestCaseData(-1m).SetName("Negative");
    yield return new TestCaseData(decimal.MinValue).SetName("MinValue");
}

[TestCaseSource(nameof(InvalidAmounts))]
public void Validate_WhenAmountIsInvalid_ThenReturnsInvalidResult(decimal amount) { ... }
```

---

## 7. Mocking Best Practices

### 7.1 Mock Only What You Control

Only mock types that your code directly depends on (interfaces, abstract classes in your own codebase). Never mock types owned by third-party libraries or the .NET runtime.

### 7.2 Loose vs Strict Mocks

Use the default **loose** mock behavior (`MockBehavior.Default`). Use `MockBehavior.Strict` only when you need to assert that no unexpected calls are made.

### 7.3 Use `It.IsAny<T>()` in SetUp

Configure broad default behaviours in `[SetUp]` using `It.IsAny<T>()`. Narrow down to exact arguments only in tests that specifically need it:

```csharp
// SetUp – broad default
_repositoryMock
    .Setup(r => r.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()))
    .ReturnsAsync((Order?)null);

// Individual test – specific input
_repositoryMock
    .Setup(r => r.GetByIdAsync(specificId, It.IsAny<CancellationToken>()))
    .ReturnsAsync(specificOrder);
```

### 7.4 Use `NullLogger<T>` in Tests

Never mock `ILogger<T>`. Use `NullLogger<T>.Instance` from `Microsoft.Extensions.Logging.Abstractions`:

```csharp
_sut = new OrderService(_repositoryMock.Object, NullLogger<OrderService>.Instance);
```

---

## 8. Test Organization

### 8.1 Test Project Naming

Each production project has a corresponding test project with `.Tests` appended to the name:

```
MyApp.Core        → MyApp.Core.Tests
MyApp.DataAccess  → MyApp.DataAccess.Tests
```

### 8.2 Folder Mirroring

Mirror the folder structure of the production project inside the test project. Each production class has a corresponding `<ClassName>Tests.cs` file in the same relative folder.

### 8.3 Test Data Builders

Extract repeated object construction into dedicated builder classes or static factory methods to keep tests readable:

```csharp
internal static class OrderBuilder
{
    public static Order Build(Guid? id = null, string customerName = "Default Customer")
    {
        return new Order
        {
            Id = id ?? Guid.NewGuid(),
            CustomerName = customerName,
            TotalAmount = 100m,
        };
    }
}
```

---

## Quick Reference Checklist

Before submitting any test file, verify:

- [ ] Test class is `internal` with `[TestFixture]`
- [ ] SUT is named `_sut` and initialized in `[SetUp]`
- [ ] All mocks declared as fields and initialized in `[SetUp]`
- [ ] Test method follows `MethodName_WhenCondition_ThenExpectedBehavior`
- [ ] Every test body has `// Arrange`, `// Act`, `// Assert` sections
- [ ] Assertions use `Assert.That(...)` constraint model
- [ ] `ILogger<T>` is not mocked – `NullLogger<T>.Instance` used instead
- [ ] `[TestCase]` used for boundary values, not duplicate test methods
- [ ] `.Verify()` used only for side-effect assertions, not return value checks
