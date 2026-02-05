---
name: test-case-design
description: Apply systematic test case design techniques including equivalence partitioning, boundary value analysis, decision tables, and state transition testing.
allowed-tools: Read, Write, Glob, Grep, Task, WebSearch, WebFetch
---

# Test Case Design Techniques

## When to Use This Skill

Use this skill when:

- **Test Case Design tasks** - Working on apply systematic test case design techniques including equivalence partitioning, boundary value analysis, decision tables, and state transition testing
- **Planning or design** - Need guidance on Test Case Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Systematic test case design techniques ensure thorough coverage while minimizing test case count. These black-box techniques derive test cases from specifications without knowledge of internal implementation.

## Equivalence Partitioning

Divide input data into equivalent classes where any value should produce the same behavior.

### Process

1. Identify input conditions
2. Divide into valid and invalid partitions
3. Select one representative value from each partition
4. Create test cases for each partition

### Example: Age Validation (18-65)

| Partition | Range | Representative | Expected |
|-----------|-------|----------------|----------|
| Invalid (below) | < 18 | 10 | Reject |
| Valid | 18-65 | 30 | Accept |
| Invalid (above) | > 65 | 70 | Reject |

**Test Cases**:

- TC1: age = 10 → Reject (invalid below)
- TC2: age = 30 → Accept (valid)
- TC3: age = 70 → Reject (invalid above)

### Multiple Input Partitions

Combine partitions systematically:

```text
Input A: {Valid, Invalid}
Input B: {Valid, Invalid}

Combinations:
1. A-Valid, B-Valid → Expected: Success
2. A-Valid, B-Invalid → Expected: Error for B
3. A-Invalid, B-Valid → Expected: Error for A
4. A-Invalid, B-Invalid → Expected: Error for both
```

## Boundary Value Analysis

Test at and around partition boundaries where defects commonly occur.

### Process

1. Identify boundaries from equivalence partitions
2. Test at minimum, just below, just above, and maximum
3. Include special values (0, empty, null)

### Example: Age Validation (18-65)

| Boundary | Test Values | Expected |
|----------|-------------|----------|
| Below minimum | 17 | Reject |
| At minimum | 18 | Accept |
| Above minimum | 19 | Accept |
| Normal | 40 | Accept |
| Below maximum | 64 | Accept |
| At maximum | 65 | Accept |
| Above maximum | 66 | Reject |

**Extended Boundaries**:

- 0 (edge case)
- -1 (negative)
- MAX_INT (overflow)
- null (missing)

### .NET Example

```csharp
public class AgeValidationTests
{
    [Theory]
    [InlineData(17, false)]  // Below minimum
    [InlineData(18, true)]   // At minimum
    [InlineData(19, true)]   // Above minimum
    [InlineData(40, true)]   // Normal
    [InlineData(64, true)]   // Below maximum
    [InlineData(65, true)]   // At maximum
    [InlineData(66, false)]  // Above maximum
    [InlineData(0, false)]   // Zero
    [InlineData(-1, false)]  // Negative
    public void ValidateAge_ReturnsExpected(int age, bool expected)
    {
        var result = _validator.IsValidAge(age);
        Assert.Equal(expected, result);
    }
}
```

## Decision Table Testing

Test complex business rules with multiple conditions systematically.

### Process

1. Identify conditions (inputs)
2. Identify actions (outputs)
3. Create table with all condition combinations
4. Simplify using "don't care" conditions

### Example: Discount Calculation

**Conditions**:

- Is member? (Y/N)
- Order > $100? (Y/N)
- Has coupon? (Y/N)

**Actions**:

- Apply member discount (10%)
- Apply bulk discount (5%)
- Apply coupon discount (15%)

| Rule | Member | Order>$100 | Coupon | Member% | Bulk% | Coupon% |
|------|--------|------------|--------|---------|-------|---------|
| R1 | Y | Y | Y | X | X | X |
| R2 | Y | Y | N | X | X | - |
| R3 | Y | N | Y | X | - | X |
| R4 | Y | N | N | X | - | - |
| R5 | N | Y | Y | - | X | X |
| R6 | N | Y | N | - | X | - |
| R7 | N | N | Y | - | - | X |
| R8 | N | N | N | - | - | - |

### .NET Example

```csharp
public class DiscountCalculationTests
{
    public static TheoryData<bool, decimal, bool, decimal> DiscountScenarios => new()
    {
        { true, 150m, true, 0.30m },   // R1: Member + Bulk + Coupon
        { true, 150m, false, 0.15m },  // R2: Member + Bulk
        { true, 50m, true, 0.25m },    // R3: Member + Coupon
        { true, 50m, false, 0.10m },   // R4: Member only
        { false, 150m, true, 0.20m },  // R5: Bulk + Coupon
        { false, 150m, false, 0.05m }, // R6: Bulk only
        { false, 50m, true, 0.15m },   // R7: Coupon only
        { false, 50m, false, 0.00m },  // R8: No discount
    };

    [Theory]
    [MemberData(nameof(DiscountScenarios))]
    public void CalculateDiscount_ReturnsExpected(
        bool isMember, decimal orderTotal, bool hasCoupon, decimal expectedDiscount)
    {
        var discount = _calculator.Calculate(isMember, orderTotal, hasCoupon);
        Assert.Equal(expectedDiscount, discount);
    }
}
```

## State Transition Testing

Test systems with distinct states and transitions between them.

### Process

1. Identify states
2. Identify valid transitions
3. Create state transition table/diagram
4. Design tests for each transition
5. Include invalid transition tests

### Example: Order State Machine

```text
         ┌──────────┐
         │  Draft   │
         └────┬─────┘
              │ submit()
              ▼
         ┌──────────┐
    ┌────│ Pending  │────┐
    │    └────┬─────┘    │
    │         │ approve()│ reject()
    │         ▼          ▼
    │    ┌──────────┐  ┌──────────┐
    │    │ Approved │  │ Rejected │
    │    └────┬─────┘  └──────────┘
    │         │ ship()
    │         ▼
    │    ┌──────────┐
    └────│ Shipped  │
         └────┬─────┘
              │ deliver()
              ▼
         ┌──────────┐
         │Delivered │
         └──────────┘
```

### State Transition Table

| Current State | Event | Next State | Valid |
|---------------|-------|------------|-------|
| Draft | submit | Pending | ✓ |
| Draft | approve | - | ✗ |
| Pending | approve | Approved | ✓ |
| Pending | reject | Rejected | ✓ |
| Approved | ship | Shipped | ✓ |
| Shipped | deliver | Delivered | ✓ |
| Delivered | * | - | ✗ |

### .NET Example

```csharp
public class OrderStateTests
{
    [Fact]
    public void Draft_Submit_TransitionsToPending()
    {
        var order = new Order { Status = OrderStatus.Draft };
        order.Submit();
        Assert.Equal(OrderStatus.Pending, order.Status);
    }

    [Fact]
    public void Draft_Approve_ThrowsInvalidStateException()
    {
        var order = new Order { Status = OrderStatus.Draft };
        Assert.Throws<InvalidOperationException>(() => order.Approve());
    }

    [Fact]
    public void Delivered_AnyAction_ThrowsFinalStateException()
    {
        var order = new Order { Status = OrderStatus.Delivered };
        Assert.Throws<InvalidOperationException>(() => order.Cancel());
    }
}
```

## Pairwise Testing

Efficiently test combinations when full combinatorial testing is impractical.

### Concept

Most defects are caused by interactions between 2 parameters. Testing all pairs covers most risks with fewer tests.

### Example: Browser Compatibility

**Parameters**:

- Browser: Chrome, Firefox, Safari, Edge
- OS: Windows, macOS, Linux
- Version: Latest, Previous

Full combinations: 4 × 3 × 2 = 24 tests
Pairwise coverage: 8-12 tests (covers all pairs)

### Pairwise Test Set

| Test | Browser | OS | Version |
|------|---------|-----|---------|
| 1 | Chrome | Windows | Latest |
| 2 | Firefox | macOS | Previous |
| 3 | Safari | macOS | Latest |
| 4 | Edge | Windows | Previous |
| 5 | Chrome | Linux | Previous |
| 6 | Firefox | Windows | Latest |
| 7 | Chrome | macOS | Latest |
| 8 | Edge | Linux | Latest |

Use tools like PICT, AllPairs, or online generators.

## Error Guessing

Experience-based technique to identify likely defect areas.

### Common Error Patterns

| Category | Examples |
|----------|----------|
| **Null/Empty** | null input, empty string, empty collection |
| **Boundaries** | off-by-one, overflow, underflow |
| **Format** | Invalid date, malformed email, wrong encoding |
| **State** | Race conditions, stale data, concurrency |
| **Resources** | Memory exhaustion, connection limits, timeouts |
| **Security** | SQL injection, XSS, path traversal |

### Error Guessing Checklist

- [ ] What if input is null?
- [ ] What if input is empty?
- [ ] What if input contains special characters?
- [ ] What if input exceeds maximum length?
- [ ] What if concurrent requests occur?
- [ ] What if external service fails?
- [ ] What if database connection drops?
- [ ] What if input is negative?
- [ ] What if list has duplicates?

## Technique Selection Guide

| Scenario | Recommended Technique |
|----------|----------------------|
| Range validation | Boundary Value + Equivalence |
| Complex business rules | Decision Table |
| State-dependent behavior | State Transition |
| Multi-parameter input | Pairwise |
| Error handling | Error Guessing |
| Critical calculations | All techniques combined |

## Integration Points

**Inputs from**:

- Requirements → Test conditions
- `test-strategy-planning` skill → Coverage targets

**Outputs to**:

- `acceptance-criteria-authoring` skill → Scenario coverage
- Test automation → Test data
