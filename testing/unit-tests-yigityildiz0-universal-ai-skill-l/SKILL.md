---
name: unit-tests
description: Generate comprehensive unit tests following FIRST principles (Fast, Independent, Repeatable, Self-validating, Timely) and AAA pattern (Arrange-Act-Assert)..
---

# Unit Tests Generation

Generate comprehensive unit tests that thoroughly validate individual functions, methods, and classes in isolation. This skill implements **Phase 2** of the 8-phase testing methodology, building on the test infrastructure established in Phase 1.

## When to Use This Skill

Use this skill when you need to:

- Create unit tests for new code
- Improve test coverage for existing code
- Implement Test-Driven Development (TDD)
- Test individual functions, methods, or classes
- Validate edge cases and error handling
- Achieve 80%+ code coverage targets
- Refactor code with test safety

**Trigger phrases**: "write unit tests", "create tests", "test this function", "test coverage", "TDD", "FIRST principles", "AAA pattern", "pytest tests", "Jest tests", "JUnit tests"

## What This Skill Does

### Core Testing Principles

#### FIRST Principles
- **Fast**: Tests execute in milliseconds (<100ms per test)
- **Independent**: Tests don't depend on each other or shared state
- **Repeatable**: Same results every time, in any environment
- **Self-validating**: Clear pass/fail without manual inspection
- **Timely**: Written before or alongside production code

#### AAA Pattern
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the function being tested
- **Assert**: Verify the expected outcome

### For All Languages

1. **Function Testing**
   - Pure functions with various inputs
   - Edge cases (empty, null, boundary values)
   - Error conditions and exceptions
   - Return value validation

2. **Class Testing**
   - Constructor behavior
   - Method interactions
   - State management
   - Inheritance and polymorphism

3. **Async Testing**
   - Async/await patterns
   - Promise handling
   - Callback testing
   - Timeout scenarios

4. **Parametrized Testing**
   - Multiple input variations
   - Boundary value analysis
   - Equivalence partitioning
   - Data-driven tests

### Language-Specific Features

#### Python (pytest)

**Basic Test Structure:**
```python
import pytest
from mymodule import calculate_discount, User, InvalidInputError

class TestCalculateDiscount:
    """Tests for the calculate_discount function."""

    def test_applies_percentage_discount(self):
        """Verify percentage discount is correctly applied."""
        # Arrange
        original_price = 100.0
        discount_rate = 0.20

        # Act
        result = calculate_discount(original_price, discount_rate)

        # Assert
        assert result == 80.0

    def test_handles_zero_discount(self):
        """Verify zero discount returns original price."""
        assert calculate_discount(100.0, 0.0) == 100.0

    def test_handles_full_discount(self):
        """Verify 100% discount returns zero."""
        assert calculate_discount(100.0, 1.0) == 0.0

    def test_raises_error_for_negative_price(self):
        """Verify negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10.0, 0.10)

    @pytest.mark.parametrize("price,rate,expected", [
        (100.0, 0.10, 90.0),
        (50.0, 0.20, 40.0),
        (200.0, 0.50, 100.0),
        (0.0, 0.25, 0.0),
    ])
    def test_discount_calculations(self, price, rate, expected):
        """Verify discount calculation with multiple inputs."""
        assert calculate_discount(price, rate) == expected


class TestUser:
    """Tests for the User class."""

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(name="John Doe", email="john@example.com", age=30)

    def test_user_initialization(self, sample_user):
        """Verify user is initialized with correct attributes."""
        assert sample_user.name == "John Doe"
        assert sample_user.email == "john@example.com"
        assert sample_user.age == 30

    def test_user_full_name(self, sample_user):
        """Verify full name property works correctly."""
        sample_user.title = "Dr."
        assert sample_user.full_name == "Dr. John Doe"

    def test_user_is_adult(self, sample_user):
        """Verify adult status based on age."""
        assert sample_user.is_adult is True

    def test_user_is_not_adult_when_under_18(self):
        """Verify minor status for users under 18."""
        minor = User(name="Jane", email="jane@example.com", age=16)
        assert minor.is_adult is False


class TestAsyncOperations:
    """Tests for async functions."""

    @pytest.mark.asyncio
    async def test_fetch_user_data(self, mocker):
        """Test async user data fetching."""
        # Arrange
        mock_response = {"id": 1, "name": "Test User"}
        mocker.patch("mymodule.http_client.get", return_value=mock_response)

        # Act
        result = await fetch_user_data(user_id=1)

        # Assert
        assert result["name"] == "Test User"

    @pytest.mark.asyncio
    async def test_fetch_user_handles_timeout(self, mocker):
        """Test timeout handling in async operations."""
        mocker.patch("mymodule.http_client.get", side_effect=TimeoutError())

        with pytest.raises(TimeoutError):
            await fetch_user_data(user_id=1)
```

#### JavaScript/TypeScript (Jest)

**Basic Test Structure:**
```typescript
import { calculateDiscount, User, fetchUserData } from './mymodule';

describe('calculateDiscount', () => {
  it('applies percentage discount correctly', () => {
    // Arrange
    const originalPrice = 100.0;
    const discountRate = 0.20;

    // Act
    const result = calculateDiscount(originalPrice, discountRate);

    // Assert
    expect(result).toBe(80.0);
  });

  it('handles zero discount', () => {
    expect(calculateDiscount(100.0, 0.0)).toBe(100.0);
  });

  it('handles full discount', () => {
    expect(calculateDiscount(100.0, 1.0)).toBe(0.0);
  });

  it('throws error for negative price', () => {
    expect(() => calculateDiscount(-10.0, 0.10)).toThrow('Price cannot be negative');
  });

  it.each([
    [100.0, 0.10, 90.0],
    [50.0, 0.20, 40.0],
    [200.0, 0.50, 100.0],
    [0.0, 0.25, 0.0],
  ])('calculates discount for price=%p, rate=%p', (price, rate, expected) => {
    expect(calculateDiscount(price, rate)).toBe(expected);
  });
});

describe('User', () => {
  let user: User;

  beforeEach(() => {
    user = new User('John Doe', 'john@example.com', 30);
  });

  it('initializes with correct attributes', () => {
    expect(user.name).toBe('John Doe');
    expect(user.email).toBe('john@example.com');
    expect(user.age).toBe(30);
  });

  it('returns correct full name with title', () => {
    user.title = 'Dr.';
    expect(user.fullName).toBe('Dr. John Doe');
  });

  it('identifies adult users correctly', () => {
    expect(user.isAdult).toBe(true);
  });

  it('identifies minors correctly', () => {
    const minor = new User('Jane', 'jane@example.com', 16);
    expect(minor.isAdult).toBe(false);
  });
});

describe('fetchUserData', () => {
  it('fetches user data successfully', async () => {
    // Arrange
    const mockResponse = { id: 1, name: 'Test User' };
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    // Act
    const result = await fetchUserData(1);

    // Assert
    expect(result.name).toBe('Test User');
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });

  it('handles network errors', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));

    await expect(fetchUserData(1)).rejects.toThrow('Network error');
  });
});
```

#### Java (JUnit 5)

**Basic Test Structure:**
```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CalculateDiscountTest {

    @Test
    @DisplayName("Should apply percentage discount correctly")
    void appliesPercentageDiscountCorrectly() {
        // Arrange
        double originalPrice = 100.0;
        double discountRate = 0.20;

        // Act
        double result = PriceCalculator.calculateDiscount(originalPrice, discountRate);

        // Assert
        assertEquals(80.0, result, 0.001);
    }

    @Test
    @DisplayName("Should handle zero discount")
    void handlesZeroDiscount() {
        assertEquals(100.0, PriceCalculator.calculateDiscount(100.0, 0.0), 0.001);
    }

    @Test
    @DisplayName("Should throw exception for negative price")
    void throwsExceptionForNegativePrice() {
        assertThrows(IllegalArgumentException.class, () ->
            PriceCalculator.calculateDiscount(-10.0, 0.10)
        );
    }

    @ParameterizedTest
    @CsvSource({
        "100.0, 0.10, 90.0",
        "50.0, 0.20, 40.0",
        "200.0, 0.50, 100.0",
        "0.0, 0.25, 0.0"
    })
    @DisplayName("Should calculate discount with multiple inputs")
    void calculatesDiscountWithMultipleInputs(double price, double rate, double expected) {
        assertEquals(expected, PriceCalculator.calculateDiscount(price, rate), 0.001);
    }
}

class UserTest {
    private User user;

    @BeforeEach
    void setUp() {
        user = new User("John Doe", "john@example.com", 30);
    }

    @Test
    @DisplayName("Should initialize with correct attributes")
    void initializesWithCorrectAttributes() {
        assertAll(
            () -> assertEquals("John Doe", user.getName()),
            () -> assertEquals("john@example.com", user.getEmail()),
            () -> assertEquals(30, user.getAge())
        );
    }

    @Test
    @DisplayName("Should identify adult users correctly")
    void identifiesAdultUsersCorrectly() {
        assertTrue(user.isAdult());
    }

    @Nested
    @DisplayName("When user is a minor")
    class MinorUser {
        private User minor;

        @BeforeEach
        void setUp() {
            minor = new User("Jane", "jane@example.com", 16);
        }

        @Test
        @DisplayName("Should not be identified as adult")
        void shouldNotBeAdult() {
            assertFalse(minor.isAdult());
        }
    }
}
```

#### C# (xUnit)

**Basic Test Structure:**
```csharp
using Xunit;
using FluentAssertions;
using Moq;

public class CalculateDiscountTests
{
    [Fact]
    public void CalculateDiscount_WithValidInputs_AppliesDiscountCorrectly()
    {
        // Arrange
        var originalPrice = 100.0m;
        var discountRate = 0.20m;

        // Act
        var result = PriceCalculator.CalculateDiscount(originalPrice, discountRate);

        // Assert
        result.Should().Be(80.0m);
    }

    [Fact]
    public void CalculateDiscount_WithZeroDiscount_ReturnsOriginalPrice()
    {
        PriceCalculator.CalculateDiscount(100.0m, 0.0m).Should().Be(100.0m);
    }

    [Fact]
    public void CalculateDiscount_WithNegativePrice_ThrowsArgumentException()
    {
        Action act = () => PriceCalculator.CalculateDiscount(-10.0m, 0.10m);
        act.Should().Throw<ArgumentException>()
           .WithMessage("*cannot be negative*");
    }

    [Theory]
    [InlineData(100.0, 0.10, 90.0)]
    [InlineData(50.0, 0.20, 40.0)]
    [InlineData(200.0, 0.50, 100.0)]
    [InlineData(0.0, 0.25, 0.0)]
    public void CalculateDiscount_WithVariousInputs_ReturnsExpectedResult(
        decimal price, decimal rate, decimal expected)
    {
        PriceCalculator.CalculateDiscount(price, rate).Should().Be(expected);
    }
}

public class UserTests : IDisposable
{
    private readonly User _user;

    public UserTests()
    {
        _user = new User("John Doe", "john@example.com", 30);
    }

    [Fact]
    public void Constructor_WithValidInputs_SetsPropertiesCorrectly()
    {
        _user.Name.Should().Be("John Doe");
        _user.Email.Should().Be("john@example.com");
        _user.Age.Should().Be(30);
    }

    [Fact]
    public void IsAdult_WhenAgeIs18OrAbove_ReturnsTrue()
    {
        _user.IsAdult.Should().BeTrue();
    }

    [Fact]
    public void IsAdult_WhenAgeIsBelow18_ReturnsFalse()
    {
        var minor = new User("Jane", "jane@example.com", 16);
        minor.IsAdult.Should().BeFalse();
    }

    public void Dispose()
    {
        // Cleanup if needed
    }
}
```

#### Go (testing)

**Basic Test Structure:**
```go
package mymodule

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCalculateDiscount(t *testing.T) {
    t.Run("applies percentage discount correctly", func(t *testing.T) {
        // Arrange
        originalPrice := 100.0
        discountRate := 0.20

        // Act
        result := CalculateDiscount(originalPrice, discountRate)

        // Assert
        assert.Equal(t, 80.0, result)
    })

    t.Run("handles zero discount", func(t *testing.T) {
        assert.Equal(t, 100.0, CalculateDiscount(100.0, 0.0))
    })

    t.Run("returns error for negative price", func(t *testing.T) {
        _, err := CalculateDiscountWithError(-10.0, 0.10)
        require.Error(t, err)
        assert.Contains(t, err.Error(), "cannot be negative")
    })
}

func TestCalculateDiscount_TableDriven(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        rate     float64
        expected float64
    }{
        {"10% off 100", 100.0, 0.10, 90.0},
        {"20% off 50", 50.0, 0.20, 40.0},
        {"50% off 200", 200.0, 0.50, 100.0},
        {"25% off 0", 0.0, 0.25, 0.0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := CalculateDiscount(tt.price, tt.rate)
            assert.Equal(t, tt.expected, result)
        })
    }
}

func TestUser(t *testing.T) {
    t.Run("initializes with correct attributes", func(t *testing.T) {
        user := NewUser("John Doe", "john@example.com", 30)

        assert.Equal(t, "John Doe", user.Name)
        assert.Equal(t, "john@example.com", user.Email)
        assert.Equal(t, 30, user.Age)
    })

    t.Run("identifies adult users correctly", func(t *testing.T) {
        user := NewUser("John", "john@example.com", 30)
        assert.True(t, user.IsAdult())
    })

    t.Run("identifies minors correctly", func(t *testing.T) {
        minor := NewUser("Jane", "jane@example.com", 16)
        assert.False(t, minor.IsAdult())
    })
}
```

#### C++ (GoogleTest)

**Basic Test Structure:**
```cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "mymodule.hpp"

class CalculateDiscountTest : public ::testing::Test {
protected:
    PriceCalculator calculator;
};

TEST_F(CalculateDiscountTest, AppliesPercentageDiscountCorrectly) {
    // Arrange
    double originalPrice = 100.0;
    double discountRate = 0.20;

    // Act
    double result = calculator.calculateDiscount(originalPrice, discountRate);

    // Assert
    EXPECT_DOUBLE_EQ(80.0, result);
}

TEST_F(CalculateDiscountTest, HandlesZeroDiscount) {
    EXPECT_DOUBLE_EQ(100.0, calculator.calculateDiscount(100.0, 0.0));
}

TEST_F(CalculateDiscountTest, ThrowsExceptionForNegativePrice) {
    EXPECT_THROW(calculator.calculateDiscount(-10.0, 0.10), std::invalid_argument);
}

class CalculateDiscountParameterizedTest
    : public ::testing::TestWithParam<std::tuple<double, double, double>> {};

TEST_P(CalculateDiscountParameterizedTest, CalculatesDiscountCorrectly) {
    auto [price, rate, expected] = GetParam();
    PriceCalculator calculator;
    EXPECT_DOUBLE_EQ(expected, calculator.calculateDiscount(price, rate));
}

INSTANTIATE_TEST_SUITE_P(
    DiscountValues,
    CalculateDiscountParameterizedTest,
    ::testing::Values(
        std::make_tuple(100.0, 0.10, 90.0),
        std::make_tuple(50.0, 0.20, 40.0),
        std::make_tuple(200.0, 0.50, 100.0),
        std::make_tuple(0.0, 0.25, 0.0)
    )
);

class UserTest : public ::testing::Test {
protected:
    void SetUp() override {
        user = std::make_unique<User>("John Doe", "john@example.com", 30);
    }

    std::unique_ptr<User> user;
};

TEST_F(UserTest, InitializesWithCorrectAttributes) {
    EXPECT_EQ("John Doe", user->getName());
    EXPECT_EQ("john@example.com", user->getEmail());
    EXPECT_EQ(30, user->getAge());
}

TEST_F(UserTest, IdentifiesAdultUsersCorrectly) {
    EXPECT_TRUE(user->isAdult());
}

TEST_F(UserTest, IdentifiesMinorsCorrectly) {
    User minor("Jane", "jane@example.com", 16);
    EXPECT_FALSE(minor.isAdult());
}
```

## Prerequisites

- Test structure established (Phase 1 completed)
- Testing framework configured
- Understanding of code to be tested
- Access to source code and documentation

## Instructions

### Step 1: Analyze Code Under Test

1. **Identify Functions/Methods to Test**
   - List public APIs and interfaces
   - Identify critical business logic
   - Note complex algorithms
   - Find error handling paths

2. **Determine Test Scenarios**
   - Happy path (normal operation)
   - Edge cases (boundaries, empty inputs)
   - Error conditions (invalid inputs, exceptions)
   - State transitions

3. **Plan Test Coverage**
   - Aim for 80%+ line coverage
   - Ensure branch coverage
   - Test all public methods

### Step 2: Write Test Cases

1. **Start with Happy Path**
   - Test normal, expected behavior
   - Use typical input values
   - Verify expected outputs

2. **Add Edge Cases**
   - Empty inputs (null, empty string, empty list)
   - Boundary values (0, -1, MAX_INT)
   - Single element collections
   - Unicode and special characters

3. **Test Error Handling**
   - Invalid inputs
   - Exception scenarios
   - Error message content

4. **Use Parametrized Tests**
   - Multiple input variations
   - Reduce code duplication
   - Improve test readability

### Step 3: Ensure Test Quality

1. **Verify FIRST Compliance**
   - Run tests and check execution time
   - Run tests in random order
   - Run tests multiple times
   - Check for clear pass/fail

2. **Review AAA Structure**
   - Clear Arrange section
   - Single Act operation
   - Focused Assert statements

3. **Check Test Independence**
   - No shared mutable state
   - No test order dependencies
   - Clean fixtures between tests

### Step 4: Run and Validate

1. **Execute Tests**
   ```bash
   # Python
   pytest -v --tb=short

   # JavaScript
   npm test -- --verbose

   # Java
   mvn test -Dtest=*Test

   # C#
   dotnet test --verbosity normal

   # Go
   go test -v ./...
   ```

2. **Check Coverage**
   ```bash
   # Python
   pytest --cov=src --cov-report=html

   # JavaScript
   npm test -- --coverage

   # Java
   mvn jacoco:report

   # Go
   go test -coverprofile=coverage.out ./...
   ```

3. **Fix Failing Tests**
   - Understand failure reason
   - Fix test or code as appropriate
   - Re-run to verify fix

## Quality Checklist

Before completing unit test generation, verify:

- [ ] All public functions/methods have tests
- [ ] Happy path scenarios covered
- [ ] Edge cases tested (empty, null, boundary)
- [ ] Error conditions tested with proper assertions
- [ ] Tests follow AAA pattern consistently
- [ ] Tests are independent (pass when run alone or together)
- [ ] Tests execute quickly (<100ms each)
- [ ] Parametrized tests used for multiple inputs
- [ ] Meaningful test names describe expected behavior
- [ ] No test pollution or shared mutable state
- [ ] Coverage meets 80%+ target

## Common Anti-Patterns to Avoid

### Testing Implementation Instead of Behavior
```python
# BAD
def test_uses_hash_map():
    cache = Cache()
    assert isinstance(cache._storage, dict)  # Implementation detail

# GOOD
def test_caches_values():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"  # Behavior
```

### Multiple Unrelated Assertions
```python
# BAD
def test_user():
    user = User("John", "john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.validate_email() is True
    assert user.age is None

# GOOD - Separate tests
def test_user_name_initialization():
    user = User("John", "john@example.com")
    assert user.name == "John"

def test_user_email_validation():
    user = User("John", "john@example.com")
    assert user.validate_email() is True
```

### Slow Tests
```python
# BAD
def test_with_delay():
    time.sleep(5)  # Don't do this
    result = operation()
    assert result is not None

# GOOD
def test_without_delay(mocker):
    mocker.patch("time.sleep")  # Mock the delay
    result = operation()
    assert result is not None
```

## Success Criteria

After using this skill, you should have:

- [ ] Comprehensive unit tests for all target code
- [ ] 80%+ code coverage achieved
- [ ] All tests passing consistently
- [ ] Tests executing in <1s total for unit tests
- [ ] Clear test documentation and naming
- [ ] No anti-patterns in test code

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Unit tests slow down development for simple functions" | Simple functions stay simple until they don't; a utility function with no tests grows into a 300-line module with 12 callers, at which point adding tests requires understanding all 12 callers before writing a single assertion. |
| "80% coverage is arbitrary — we only test the important parts" | Without a measurable threshold, "important parts" expands to mean "whatever was easy to test"; the 20% uncovered code is disproportionately the error handling paths and edge cases where real-world bugs concentrate. |
| "Mocking makes tests too fragile and tied to implementation" | Tests that do not mock external dependencies (databases, HTTP APIs) are integration tests, not unit tests; they are orders of magnitude slower, require infrastructure setup, and fail for infrastructure reasons unrelated to the logic under test. |
| "Test names don't matter as long as the assertion is correct" | When a test fails in CI, the test name is the first and often only information visible before opening the test file; descriptive names like `test_transfer_fails_when_balance_insufficient` eliminate the need to read the test body to understand the failure. |
| "We don't need tests for code that's about to be rewritten" | Code that is "about to be rewritten" typically remains in production for 6-18 months while the rewrite is deprioritized; during that period it receives changes and bug fixes without any regression protection. |

## Verification

- [ ] All new functions have corresponding test files with at least one test per public method
- [ ] Test suite passes with code 0: `pytest -q` / `npm test` / `go test ./...` exits cleanly
- [ ] Code coverage is 80% or above: `pytest --cov --cov-fail-under=80` or equivalent passes
- [ ] No test uses `time.sleep`, real HTTP calls, or filesystem writes to non-temp paths
- [ ] Every test function has a descriptive name following `test_<scenario>_<expected_outcome>` or equivalent convention
- [ ] All tests run in under 1 second for the unit test suite (verified by timing output)

## Related Skills

- `test-structure` - Set up test infrastructure (Phase 1)
- `test-cases` - Integration and E2E tests (Phase 3)
- `mocks-fixtures` - Test doubles and fixtures (Phase 4)
- `code-coverage` - Coverage analysis (Phase 7)
- `mutation-testing` - Test quality validation (Phase 8)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/unit_tests/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
