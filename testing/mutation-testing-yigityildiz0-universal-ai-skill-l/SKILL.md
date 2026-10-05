---
name: mutation-testing
description: Validate test quality through mutation testing to detect weak tests and reward hacking patterns. Use when verifying test suite effectiveness, improving test.
---

# Mutation Testing

Validate test suite quality by introducing code mutations and verifying tests detect them. This skill implements **Phase 8** of the 8-phase testing methodology - the final validation phase.

## When to Use This Skill

Use this skill when you need to:

- Validate test suite effectiveness
- Detect weak or superficial tests
- Find "reward hacking" patterns
- Improve test quality beyond coverage
- Verify tests catch real bugs
- Identify tests that always pass
- Strengthen assertions

**Trigger phrases**: "mutation testing", "test quality", "reward hacking", "mutants", "test effectiveness", "weak tests", "mutation score", "pitest", "mutmut"

## What This Skill Does

### What is Mutation Testing?

Mutation testing validates test quality by:
1. Making small changes (mutations) to source code
2. Running tests against mutated code
3. Checking if tests detect (kill) the mutations
4. Measuring mutation score (% killed)

### Mutation Types

| Mutation | Original | Mutated |
|----------|----------|---------|
| **Arithmetic** | `a + b` | `a - b` |
| **Relational** | `a < b` | `a <= b` |
| **Boolean** | `a && b` | `a \|\| b` |
| **Return Value** | `return x` | `return null` |
| **Void Method** | `call()` | removed |
| **Constant** | `MAX = 100` | `MAX = 101` |

### Language-Specific Examples

#### Python (mutmut / pytest-mutagen)

```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run --paths-to-mutate=src/

# View results
mutmut results

# Show surviving mutants
mutmut show <mutant_id>

# Generate HTML report
mutmut html
```

```python
# Example: Detecting weak tests

# Original code
def calculate_discount(price: float, rate: float) -> float:
    """Calculate discounted price."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if rate < 0 or rate > 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * (1 - rate)

# WEAK TEST - Would pass with mutations
def test_discount_weak():
    """This test is too weak - mutants survive."""
    result = calculate_discount(100, 0.1)
    assert result is not None  # Too weak!
    assert result > 0  # Doesn't verify exact value

# STRONG TEST - Kills mutations
def test_discount_strong():
    """This test catches mutations."""
    assert calculate_discount(100, 0.1) == 90.0  # Exact value
    assert calculate_discount(100, 0.5) == 50.0  # Another case
    assert calculate_discount(0, 0.5) == 0.0     # Edge case

def test_discount_validates_price():
    """Catches removed validation mutations."""
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_discount(-10, 0.1)

def test_discount_validates_rate():
    """Catches boundary mutations."""
    with pytest.raises(ValueError, match="between 0 and 1"):
        calculate_discount(100, -0.1)
    with pytest.raises(ValueError, match="between 0 and 1"):
        calculate_discount(100, 1.5)

# mutmut.conf
def pre_mutation(context):
    """Skip certain mutations."""
    if context.current_source_line.strip().startswith('#'):
        context.skip = True

# Run mutation testing for specific module
# mutmut run --paths-to-mutate=src/pricing.py
```

#### JavaScript/TypeScript (Stryker)

```javascript
// stryker.conf.js
module.exports = {
  mutator: 'typescript',
  packageManager: 'npm',
  reporters: ['html', 'clear-text', 'progress', 'dashboard'],
  testRunner: 'jest',
  coverageAnalysis: 'perTest',
  jest: {
    projectType: 'custom',
    configFile: 'jest.config.js',
    enableFindRelatedTests: true,
  },
  thresholds: {
    high: 80,
    low: 60,
    break: 50  // Fail if mutation score below 50%
  },
  mutate: [
    'src/**/*.ts',
    '!src/**/*.test.ts',
    '!src/**/*.d.ts'
  ],
  timeoutMS: 60000,
  concurrency: 4
};

// Run Stryker
// npx stryker run
```

```typescript
// Example: Weak vs Strong Tests

// Source code
function calculateDiscount(price: number, rate: number): number {
  if (price < 0) throw new Error('Price cannot be negative');
  if (rate < 0 || rate > 1) throw new Error('Rate must be between 0 and 1');
  return price * (1 - rate);
}

// WEAK TEST - Mutants survive
describe('calculateDiscount - weak', () => {
  it('returns a number', () => {
    const result = calculateDiscount(100, 0.1);
    expect(typeof result).toBe('number'); // Doesn't verify value
  });

  it('returns positive value', () => {
    expect(calculateDiscount(100, 0.1)).toBeGreaterThan(0); // Too vague
  });
});

// STRONG TEST - Kills mutants
describe('calculateDiscount - strong', () => {
  it('calculates 10% discount correctly', () => {
    expect(calculateDiscount(100, 0.1)).toBe(90); // Exact value
  });

  it('calculates 50% discount correctly', () => {
    expect(calculateDiscount(200, 0.5)).toBe(100); // Another exact case
  });

  it('handles zero price', () => {
    expect(calculateDiscount(0, 0.5)).toBe(0); // Edge case
  });

  it('handles zero discount', () => {
    expect(calculateDiscount(100, 0)).toBe(100); // Boundary
  });

  it('handles full discount', () => {
    expect(calculateDiscount(100, 1)).toBe(0); // Boundary
  });

  it('rejects negative price', () => {
    expect(() => calculateDiscount(-10, 0.1))
      .toThrow('Price cannot be negative');
  });

  it('rejects negative rate', () => {
    expect(() => calculateDiscount(100, -0.1))
      .toThrow('Rate must be between 0 and 1');
  });

  it('rejects rate above 1', () => {
    expect(() => calculateDiscount(100, 1.5))
      .toThrow('Rate must be between 0 and 1');
  });
});
```

#### Java (PIT / PITest)

```xml
<!-- pom.xml PIT configuration -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <dependencies>
        <dependency>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-junit5-plugin</artifactId>
            <version>1.2.0</version>
        </dependency>
    </dependencies>
    <configuration>
        <targetClasses>
            <param>com.example.service.*</param>
        </targetClasses>
        <targetTests>
            <param>com.example.service.*Test</param>
        </targetTests>
        <mutators>
            <mutator>DEFAULTS</mutator>
            <mutator>STRONGER</mutator>
        </mutators>
        <mutationThreshold>80</mutationThreshold>
        <coverageThreshold>80</coverageThreshold>
        <outputFormats>
            <outputFormat>HTML</outputFormat>
            <outputFormat>XML</outputFormat>
        </outputFormats>
        <timestampedReports>false</timestampedReports>
    </configuration>
</plugin>

<!-- Run PIT: mvn test-compile pitest:mutationCoverage -->
```

```java
// Example: Weak vs Strong Tests

public class PriceCalculator {
    public double calculateDiscount(double price, double rate) {
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        if (rate < 0 || rate > 1) {
            throw new IllegalArgumentException("Rate must be between 0 and 1");
        }
        return price * (1 - rate);
    }
}

// WEAK TEST - Many mutants survive
class PriceCalculatorWeakTest {
    @Test
    void discount_returns_value() {
        PriceCalculator calc = new PriceCalculator();
        double result = calc.calculateDiscount(100, 0.1);
        assertNotNull(result); // Too weak
        assertTrue(result > 0); // Doesn't verify exact value
    }
}

// STRONG TEST - Kills mutants
class PriceCalculatorStrongTest {
    private PriceCalculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new PriceCalculator();
    }

    @Test
    void calculateDiscount_with10Percent_returns90() {
        assertEquals(90.0, calculator.calculateDiscount(100, 0.1), 0.001);
    }

    @Test
    void calculateDiscount_with50Percent_returnsHalfPrice() {
        assertEquals(100.0, calculator.calculateDiscount(200, 0.5), 0.001);
    }

    @Test
    void calculateDiscount_withZeroPrice_returnsZero() {
        assertEquals(0.0, calculator.calculateDiscount(0, 0.5), 0.001);
    }

    @Test
    void calculateDiscount_withZeroRate_returnsOriginalPrice() {
        assertEquals(100.0, calculator.calculateDiscount(100, 0), 0.001);
    }

    @Test
    void calculateDiscount_withFullDiscount_returnsZero() {
        assertEquals(0.0, calculator.calculateDiscount(100, 1), 0.001);
    }

    @ParameterizedTest
    @CsvSource({
        "100, 0.1, 90.0",
        "200, 0.25, 150.0",
        "50, 0.5, 25.0"
    })
    void calculateDiscount_variousInputs(double price, double rate, double expected) {
        assertEquals(expected, calculator.calculateDiscount(price, rate), 0.001);
    }

    @Test
    void calculateDiscount_withNegativePrice_throwsException() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateDiscount(-10, 0.1));
    }

    @Test
    void calculateDiscount_withNegativeRate_throwsException() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateDiscount(100, -0.1));
    }

    @Test
    void calculateDiscount_withRateAboveOne_throwsException() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateDiscount(100, 1.5));
    }
}
```

## Prerequisites

- High code coverage achieved (Phase 7)
- Unit tests comprehensive
- Understanding of mutation testing concepts

## Instructions

### Step 1: Install Mutation Testing Tool

```bash
# Python
pip install mutmut

# JavaScript/TypeScript
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner

# Java - add PIT plugin to pom.xml

# Go
go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
```

### Step 2: Configure and Run

1. **Configure Target Code**
   - Specify source directories
   - Exclude generated code
   - Set timeout values

2. **Run Mutation Tests**
   ```bash
   # Python
   mutmut run

   # JavaScript
   npx stryker run

   # Java
   mvn pitest:mutationCoverage
   ```

### Step 3: Analyze Results

1. **Review Surviving Mutants**
   - Identify weak assertions
   - Find missing edge cases
   - Note untested branches

2. **Strengthen Tests**
   - Add specific assertions
   - Test boundary conditions
   - Cover error paths

### Step 4: Set Thresholds

1. **Configure Minimums**
   - Target: 80%+ mutation score
   - Warning: Below 60%
   - Fail: Below 50%

## Quality Checklist

- [ ] Mutation tool configured
- [ ] Initial mutation score measured
- [ ] Surviving mutants analyzed
- [ ] Weak tests strengthened
- [ ] Mutation score at 80%+
- [ ] CI/CD threshold configured

## Common Weak Test Patterns

### 1. Vague Assertions
```python
# BAD
assert result is not None

# GOOD
assert result == expected_value
```

### 2. Missing Boundary Tests
```python
# BAD - Only tests middle values
assert func(50) == expected

# GOOD - Tests boundaries
assert func(0) == 0
assert func(100) == max_value
```

### 3. Missing Error Tests
```python
# BAD - Only happy path
assert func(valid_input) == result

# GOOD - Tests error paths
with pytest.raises(ValueError):
    func(invalid_input)
```

## Related Skills

- `code-coverage` - Coverage analysis (Phase 7)
- `unit-tests` - Unit testing (Phase 2)
- `test-cases` - Integration tests (Phase 3)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/reward_hacking/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
