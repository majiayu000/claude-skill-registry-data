---
name: TestDrivenDevelopment
description: Disciplined TDD workflow enforcing red-green-refactor cycle and the "iron law" of no production code without failing tests first. USE WHEN user wants to write tests first OR implement new feature with TDD OR fix bugs with test coverage OR explicitly requests TDD approach. Enforces systematic test-first development with verification at each step.
---

# TestDrivenDevelopment

Strict test-driven development workflow based on the red-green-refactor cycle.

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

This is non-negotiable. Even when tempted to "just quickly fix" something, you MUST:
1. Write a failing test that demonstrates the need
2. Verify the test actually fails
3. Write minimal code to make it pass
4. Verify the test passes
5. Refactor if needed

## The RED-GREEN-REFACTOR Cycle

### RED: Write Failing Test

1. Write test that describes desired behavior
2. Test MUST fail initially (if it passes, something's wrong)
3. Failure message should be clear and specific

**Example (Go):**
```go
func TestCalculateDiscount_TenPercent(t *testing.T) {
    order := Order{Subtotal: 100.0, DiscountRate: 0.10}
    got := order.CalculateTotal()
    want := 90.0
    if got != want {
        t.Errorf("CalculateTotal() = %v, want %v", got, want)
    }
}
```

### Verify RED

1. Run test suite
2. Confirm new test fails
3. Confirm failure reason matches expectation
4. **STOP if test doesn't fail** - investigate why

```bash
go test ./...
# Expected: FAIL - undefined: Order.CalculateTotal
```

### GREEN: Minimal Implementation

1. Write ONLY enough code to make test pass
2. Don't over-engineer
3. Don't add features not tested
4. Prioritize working over elegant

**Example:**
```go
func (o Order) CalculateTotal() float64 {
    return o.Subtotal * (1 - o.DiscountRate)
}
```

### Verify GREEN

1. Run full test suite
2. Confirm ALL tests pass
3. **STOP if any test fails** - fix before refactoring

```bash
go test ./...
# Expected: PASS
```

### REFACTOR

1. Improve code structure
2. Eliminate duplication
3. Enhance readability
4. **Run tests after each change**

**Example refactor:**
```go
func (o Order) CalculateTotal() float64 {
    return o.ApplyDiscount(o.Subtotal)
}

func (o Order) ApplyDiscount(amount float64) float64 {
    return amount * (1 - o.DiscountRate)
}
```

## Good vs Bad Tests

### Good Test (Tests Behavior)
```go
func TestCalculateTotal_WithDiscount(t *testing.T) {
    order := Order{Items: []Item{{Price: 100}}, Discount: 0.1}
    got := order.CalculateTotal()
    want := 90.0
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

### Bad Test (Tests Implementation)
```go
func TestCalculateTotal_CallsDiscountFunc(t *testing.T) {
    // Testing HOW instead of WHAT
    // Brittle - breaks with refactoring
    // Don't do this
}
```

### Good Test Characteristics
- Tests behavior, not implementation
- Clear, descriptive name
- Single responsibility
- Independent (no shared state)
- Fast execution
- Deterministic

## Red Flags

**STOP immediately if you catch yourself:**

- ❌ Writing production code before a failing test
- ❌ Modifying production code while tests are failing
- ❌ Skipping the "verify RED" step
- ❌ Writing overly complex implementation for green phase
- ❌ Refactoring with failing tests
- ❌ Adding features not covered by tests

**When you notice these, return to RED phase.**

## TDD Workflow Checklist

**For each feature/fix:**

- [ ] Write failing test (RED)
- [ ] Run test, verify it fails with expected error
- [ ] Write minimal code to pass (GREEN)
- [ ] Run all tests, verify they pass
- [ ] Refactor if needed
- [ ] Run all tests again
- [ ] Commit with test and implementation together

## Language-Specific Examples

### Go
```go
// RED: Test first
func TestParseConfig_ValidYAML(t *testing.T) {
    yaml := "port: 8080\nhost: localhost"
    config, err := ParseConfig([]byte(yaml))
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if config.Port != 8080 {
        t.Errorf("Port = %d, want 8080", config.Port)
    }
}

// GREEN: Minimal implementation
func ParseConfig(data []byte) (*Config, error) {
    var cfg Config
    err := yaml.Unmarshal(data, &cfg)
    return &cfg, err
}
```

### Python
```python
# RED: Test first
def test_calculate_discount_ten_percent():
    order = Order(subtotal=100.0, discount_rate=0.10)
    assert order.calculate_total() == 90.0

# GREEN: Minimal implementation
class Order:
    def __init__(self, subtotal, discount_rate):
        self.subtotal = subtotal
        self.discount_rate = discount_rate

    def calculate_total(self):
        return self.subtotal * (1 - self.discount_rate)
```

### Rust
```rust
// RED: Test first
#[test]
fn test_calculate_total_with_discount() {
    let order = Order {
        subtotal: 100.0,
        discount_rate: 0.10,
    };
    assert_eq!(order.calculate_total(), 90.0);
}

// GREEN: Minimal implementation
impl Order {
    fn calculate_total(&self) -> f64 {
        self.subtotal * (1.0 - self.discount_rate)
    }
}
```

## When NOT to Use TDD

TDD isn't always the right choice:

- **Exploratory coding**: When you're not sure what you're building yet (use Brainstorming skill first)
- **UI prototyping**: Visual design often needs iteration before solidifying behavior
- **Performance optimization**: Sometimes you need to measure first, then optimize
- **Glue code**: Simple wiring between components may not need tests

**For these cases**: Build first, then add tests for the stable parts.

## Integration with Other Skills

- **Before TDD**: Use **Brainstorming** skill to clarify requirements
- **During TDD**: Use **SystematicDebugging** if tests reveal unexpected behavior
- **After TDD**: Use code review workflows to validate test coverage

## Examples

**Example 1: Adding new feature with TDD**
```
User: "Add a discount calculation feature"
→ Invoke TestDrivenDevelopment skill
→ RED: Write test for CalculateDiscount expecting 10% off
→ Verify: Run test, fails with "undefined: CalculateDiscount"
→ GREEN: Implement minimal CalculateDiscount function
→ Verify: Run test, passes
→ REFACTOR: Extract discount logic to separate method
→ Verify: Run all tests, still pass
→ Feature complete with test coverage
```

**Example 2: Fixing a bug with TDD**
```
User: "Fix the bug where negative prices crash the app"
→ Invoke TestDrivenDevelopment skill
→ RED: Write test with negative price expecting error or zero
→ Verify: Run test, crashes (reproduces bug)
→ GREEN: Add validation to reject negative prices
→ Verify: Run test, passes
→ REFACTOR: Improve error message
→ Bug fixed with regression test preventing recurrence
```

**Example 3: User explicitly requests TDD**
```
User: "Let's use TDD to build the authentication system"
→ Invoke TestDrivenDevelopment skill
→ Guide through RED-GREEN-REFACTOR for each auth feature:
  - User registration
  - Login validation
  - Token generation
  - Token verification
→ Each feature gets test first, then implementation
→ Comprehensive test coverage from the start
→ Confidence in authentication security
```

**Example 4: Complex algorithm development**
```
User: "Implement a binary search algorithm"
→ Invoke TestDrivenDevelopment skill
→ RED: Test with sorted array, search for existing element
→ GREEN: Implement basic binary search
→ RED: Test with element not in array
→ GREEN: Handle not found case
→ RED: Test with empty array
→ GREEN: Handle edge case
→ REFACTOR: Simplify logic
→ Algorithm complete with edge case coverage
```
