---
name: behavior-preservation-checker
description: Verify that refactoring preserves existing behavior through before/after comparison, test coverage verification, contract checking, and semantic equivalence.
---

# Behavior Preservation Checker

Systematic verification that code refactoring, restructuring, or migration preserves the existing observable behavior of the system. This skill provides techniques for comparing before and after states, verifying test coverage, checking interface contracts, and performing semantic equivalence analysis.

## When to Use This Skill

Use this skill for:

- Verifying that a refactoring PR introduces no behavioral changes
- Reviewing Extract Method, Move Class, or Rename refactorings for correctness
- Validating that a library migration preserves API contracts
- Confirming that performance optimizations do not alter output
- Checking that dependency upgrades maintain backward compatibility
- Ensuring that code cleanup (dead code removal, formatting) has no side effects
- Auditing automated refactoring tool output for correctness

**Trigger phrases**: "behavior preservation", "verify refactoring", "check no behavior change", "before and after", "semantic equivalence", "contract check", "refactoring safety", "does this change behavior", "regression check", "safe refactoring"

## What This Skill Does

This skill provides a multi-layered verification approach:

- **Before/After Comparison**: Analyzes the diff between original and refactored code to classify each change as structural (safe) or behavioral (potentially unsafe)
- **Test Coverage Verification**: Ensures that all refactored code paths are covered by existing tests and identifies coverage gaps that could hide behavioral changes
- **Contract Checking**: Verifies that public interfaces (method signatures, return types, exception contracts, side effects) remain identical
- **Semantic Equivalence Analysis**: Performs deeper analysis to determine whether structurally different code produces the same outputs for all inputs
- **Side Effect Auditing**: Identifies changes to I/O operations, state mutations, logging, event emissions, and other observable side effects
- **Regression Risk Assessment**: Estimates the likelihood and impact of undetected behavioral changes

## Instructions

### Step 1: Classify Changes as Structural vs. Behavioral

Review each change in the diff and classify it into one of these categories.

#### Safe Structural Changes (No Behavioral Impact)

These changes are guaranteed to preserve behavior:

- Renaming local variables, parameters, or private methods (with all references updated)
- Extracting a code block into a new private method called from the original location
- Reordering private methods within a class (no change to call order)
- Adding or modifying comments and documentation
- Reformatting code (whitespace, indentation, line breaks)
- Replacing explicit type declarations with equivalent type inference (e.g., `var` in Java 10+)

#### Potentially Unsafe Changes (Require Verification)

These changes could alter behavior and must be verified:

- Changing the order of operations or statements
- Modifying loop structures (for to while, for to stream)
- Altering exception handling (catch order, exception types, finally blocks)
- Moving code between methods or classes
- Changing visibility modifiers (private to protected, package-private to public)
- Replacing one API call with another (even if "equivalent")
- Modifying conditional logic structure (if/else to switch, ternary to if)

#### Python Example: Classifying a Refactoring Diff

```python
# BEFORE
def calculate_discount(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    if total > 100:
        discount = total * 0.1
    elif total > 50:
        discount = total * 0.05
    else:
        discount = 0
    return discount

# AFTER (refactored)
def calculate_discount(order):
    total = _calculate_order_total(order)
    return _apply_discount_tiers(total)

def _calculate_order_total(order):
    return sum(item.price * item.quantity for item in order.items)

def _apply_discount_tiers(total):
    if total > 100:
        return total * 0.1
    if total > 50:
        return total * 0.05
    return 0
```

**Change classification**:

| Change | Classification | Reasoning |
|--------|---------------|-----------|
| Extract `_calculate_order_total` | Safe | Same computation, just moved to a new function |
| `for` loop to `sum()` generator | Verify | Functionally equivalent for numeric addition, but verify no side effects in `item.price` or `item.quantity` property accessors |
| Extract `_apply_discount_tiers` | Safe | Same conditional logic, identical branch order |
| `elif` to separate `if` with early return | Verify | Logically equivalent due to early returns, but verify no fall-through logic was intended |

### Step 2: Verify Test Coverage of Refactored Code

Before accepting a refactoring as behavior-preserving, confirm that tests exercise all affected code paths.

#### Coverage Verification Checklist

1. **Run the existing test suite**: all tests must pass without modification after refactoring; any test failure indicates a behavioral change
2. **Measure line coverage**: every line in both the original and refactored code should be covered; uncovered lines in the original code represent blind spots
3. **Measure branch coverage**: every conditional branch (if/else, switch cases, ternary) must be exercised by at least one test
4. **Check edge case coverage**: verify tests exist for boundary values, null/empty inputs, error conditions, and maximum/minimum values
5. **Identify coverage gaps**: if the original code had uncovered paths, write characterization tests before refactoring

#### JavaScript Example: Test Coverage Verification

```javascript
// Original function
function parseConfig(input) {
    if (typeof input === "string") {
        try {
            return JSON.parse(input);
        } catch (e) {
            return { error: e.message };
        }
    } else if (typeof input === "object" && input !== null) {
        return { ...input };
    }
    return {};
}

// Refactored function
function parseConfig(input) {
    if (typeof input === "string") {
        return parseStringConfig(input);
    }
    if (isNonNullObject(input)) {
        return cloneConfig(input);
    }
    return {};
}

function parseStringConfig(input) {
    try {
        return JSON.parse(input);
    } catch (e) {
        return { error: e.message };
    }
}

function isNonNullObject(value) {
    return typeof value === "object" && value !== null;
}

function cloneConfig(obj) {
    return { ...obj };
}
```

**Required test cases for full behavior preservation verification**:

```javascript
describe("parseConfig behavior preservation", () => {
    // String input -- valid JSON
    test("parses valid JSON string", () => {
        expect(parseConfig('{"key": "value"}')).toEqual({ key: "value" });
    });

    // String input -- invalid JSON (error path)
    test("returns error object for invalid JSON", () => {
        const result = parseConfig("not json");
        expect(result).toHaveProperty("error");
    });

    // Object input -- non-null
    test("clones object input", () => {
        const input = { a: 1, b: 2 };
        const result = parseConfig(input);
        expect(result).toEqual(input);
        expect(result).not.toBe(input); // verify it is a copy
    });

    // Null input
    test("returns empty object for null", () => {
        expect(parseConfig(null)).toEqual({});
    });

    // Undefined input
    test("returns empty object for undefined", () => {
        expect(parseConfig(undefined)).toEqual({});
    });

    // Numeric input
    test("returns empty object for number", () => {
        expect(parseConfig(42)).toEqual({});
    });

    // Array input (typeof array === "object" and array !== null)
    test("clones array input as object", () => {
        const result = parseConfig([1, 2, 3]);
        expect(result).toEqual({ 0: 1, 1: 2, 2: 3 });
    });
});
```

**Coverage gap identified**: the array input test reveals a subtle difference. In the original code, `typeof [1,2,3] === "object"` and `[1,2,3] !== null` are both true, so arrays are spread into an object. The refactored version must handle this identically. If `cloneConfig` were implemented differently (e.g., using `structuredClone`), behavior would change.

### Step 3: Check Interface Contracts

Verify that the public contract of refactored code remains unchanged across all dimensions.

#### Contract Dimensions

| Dimension | What to Check | Example Violation |
|-----------|---------------|-------------------|
| **Method Signature** | Parameter types, count, order, return type | Adding a required parameter |
| **Exception Contract** | Which exceptions are thrown and when | Catching an exception that was previously propagated |
| **Nullability** | Whether null/undefined inputs are accepted and outputs can be null | Returning `Optional.empty()` where `null` was returned before |
| **Side Effects** | Database writes, file I/O, event emissions, logging | Removing an audit log call during refactoring |
| **Ordering** | Order of elements in returned collections | Changing `HashMap` to `TreeMap` alters iteration order |
| **Thread Safety** | Synchronization, atomicity guarantees | Removing `synchronized` during extraction |
| **Idempotency** | Whether calling the method multiple times has the same effect | Introducing a cache that changes behavior on repeat calls |

#### Java Example: Contract Verification

```java
// BEFORE
public class PaymentProcessor {
    public PaymentResult processPayment(PaymentRequest request)
            throws InsufficientFundsException, PaymentGatewayException {
        validateRequest(request);          // throws IllegalArgumentException
        Account account = loadAccount(request.getAccountId());
        if (account.getBalance() < request.getAmount()) {
            throw new InsufficientFundsException(account.getBalance(), request.getAmount());
        }
        GatewayResponse response = gateway.charge(request.getAmount(), account.getToken());
        auditLogger.log("payment_processed", request.getAccountId(), request.getAmount());
        return new PaymentResult(response.getTransactionId(), response.getStatus());
    }
}

// AFTER (refactored)
public class PaymentProcessor {
    public PaymentResult processPayment(PaymentRequest request)
            throws InsufficientFundsException, PaymentGatewayException {
        validateRequest(request);
        Account account = accountService.getVerifiedAccount(request.getAccountId());
        accountService.verifyFunds(account, request.getAmount());
        GatewayResponse response = paymentGateway.charge(request);
        auditService.recordPayment(request, response);
        return PaymentResult.from(response);
    }
}
```

**Contract verification checklist**:

| Check | Status | Notes |
|-------|--------|-------|
| Method signature unchanged | PASS | Same parameters, return type, and declared exceptions |
| `IllegalArgumentException` still thrown for invalid input | VERIFY | Must confirm `validateRequest` behavior unchanged |
| `InsufficientFundsException` thrown with same fields | VERIFY | `accountService.verifyFunds` must throw with balance and amount |
| `PaymentGatewayException` propagated identically | VERIFY | `paymentGateway.charge` must throw same exception type |
| Audit log side effect preserved | VERIFY | `auditService.recordPayment` must log same event name and fields |
| Return value structure identical | VERIFY | `PaymentResult.from(response)` must map `transactionId` and `status` identically |
| No new exceptions introduced | VERIFY | `accountService.getVerifiedAccount` must not throw unexpected exceptions |

### Step 4: Perform Semantic Equivalence Analysis

For changes that are not trivially structural, determine whether the original and refactored code produce the same output for all possible inputs.

#### Equivalence Analysis Techniques

1. **Input partitioning**: identify all equivalence classes of inputs and verify both versions produce the same output for representative inputs from each class
2. **Boundary analysis**: test boundary values (0, 1, -1, MAX_INT, empty string, empty collection, null) in both versions
3. **Property-based comparison**: if feasible, express the expected behavior as properties (e.g., "output is always sorted", "output length equals input length") and verify both versions satisfy them
4. **Trace comparison**: execute both versions with identical inputs and compare execution traces (method calls, state transitions, return values)

#### Python Example: Semantic Equivalence with Property-Based Testing

```python
from hypothesis import given, strategies as st

# Original
def flatten_original(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            for sub in item:
                result.append(sub)
        else:
            result.append(item)
    return result

# Refactored
def flatten_refactored(nested):
    return [
        sub
        for item in nested
        for sub in (item if isinstance(item, list) else [item])
    ]

# Equivalence test
@given(st.lists(st.one_of(
    st.integers(),
    st.lists(st.integers(), max_size=5)
), max_size=20))
def test_flatten_equivalence(nested):
    assert flatten_original(nested) == flatten_refactored(nested)
```

### Step 5: Audit Side Effects

Catalog all observable side effects in the original code and confirm each one is preserved in the refactored version.

#### Side Effect Categories

| Category | Examples | Detection Method |
|----------|----------|-----------------|
| **I/O Operations** | File reads/writes, network calls, database queries | Search for I/O library calls |
| **State Mutations** | Setting instance fields, modifying global state | Track assignment statements to non-local variables |
| **Event Emissions** | Publishing messages, firing events, sending signals | Search for publish/emit/fire/send patterns |
| **Logging** | Log statements at any level | Search for logger/console/print calls |
| **Resource Management** | Opening/closing connections, acquiring locks | Search for open/close/acquire/release patterns |
| **External Service Calls** | API calls, RPC invocations | Search for HTTP client and RPC stub usage |

#### Java Example: Side Effect Audit

```java
// BEFORE: Side effects catalog
public void processOrder(Order order) {
    // Side effect 1: Database write
    orderRepository.save(order);

    // Side effect 2: Event emission
    eventBus.publish(new OrderCreatedEvent(order.getId()));

    // Side effect 3: External API call
    inventoryService.reserve(order.getItems());

    // Side effect 4: Logging
    logger.info("Order {} processed for customer {}", order.getId(), order.getCustomerId());

    // Side effect 5: Metric recording
    metrics.counter("orders.processed").increment();
}

// AFTER: Must preserve ALL five side effects
public void processOrder(Order order) {
    persistence.saveOrder(order);                    // SE1: verify same DB write
    notifications.orderCreated(order);               // SE2: verify same event
    inventory.reserveStock(order.getItems());         // SE3: verify same API call
    // BUG: logging side effect removed during refactoring
    monitoring.recordOrderProcessed();                // SE5: verify same metric
}
```

**Side effect audit result**: FAIL -- logging side effect (SE4) was removed during refactoring. This is a behavioral change even though it does not affect the return value.

### Step 6: Generate Preservation Report

Produce a structured report summarizing the verification results.

```
## Behavior Preservation Report

### Refactoring Summary
- **Scope**: {files and methods changed}
- **Type**: {Extract Method / Move Class / Rename / etc.}
- **Lines changed**: {count}

### Verification Results

| Check | Status | Details |
|-------|--------|---------|
| All existing tests pass | PASS/FAIL | {count} tests, {failures} |
| Line coverage >= original | PASS/FAIL | Before: {x}%, After: {y}% |
| Branch coverage >= original | PASS/FAIL | Before: {x}%, After: {y}% |
| Public interface unchanged | PASS/FAIL | {details} |
| Exception contracts preserved | PASS/FAIL | {details} |
| Side effects preserved | PASS/FAIL | {count} side effects verified |
| Semantic equivalence confirmed | PASS/FAIL | {method and evidence} |

### Risks
- {List any unverified paths or known gaps}

### Recommendation
- APPROVE: All checks pass, refactoring is behavior-preserving
- APPROVE WITH CONDITIONS: Minor gaps exist but risk is low
- REJECT: Behavioral changes detected, requires correction
```

## Best Practices

- **Write characterization tests before refactoring**: if the code under refactoring lacks adequate test coverage, write tests that capture current behavior first; these tests serve as the "golden master" that validates preservation
- **Refactor in small, verifiable steps**: each step should be independently verifiable; avoid combining multiple refactoring operations into a single commit
- **Use version control bisection**: if a behavioral change is detected after multiple refactoring steps, use `git bisect` to identify the exact commit that introduced the change
- **Preserve error behavior, not just happy paths**: exception types, error messages, and error handling order are all part of the observable behavior contract
- **Do not confuse intentional behavioral changes with refactoring**: if the goal is to change behavior (fix a bug, change a business rule), that is not a refactoring; use separate commits for behavioral changes and structural changes
- **Verify thread safety preservation**: if the original code uses synchronization, locks, or atomic operations, the refactored code must maintain the same concurrency guarantees
- **Check serialization compatibility**: if refactored classes are serialized (JSON, XML, binary), verify that the serialized form remains identical
- **Automate preservation checks**: integrate behavior preservation verification into CI/CD pipelines using snapshot testing, contract testing, or approval testing frameworks
- **Pay special attention to floating-point operations**: reordering arithmetic with floating-point numbers can produce different results due to precision; `(a + b) + c` may not equal `a + (b + c)`

## Common Pitfalls

- **Assuming "same output" means "same behavior"**: a function can produce the same return value while changing side effects (logging, database writes, event emissions); always audit side effects separately
- **Ignoring evaluation order changes**: in languages with short-circuit evaluation, reordering conditions can change which side effects execute; `if (a() && b())` is not the same as `if (b() && a())` when `a()` or `b()` have side effects
- **Overlooking null/undefined edge cases**: refactored code may handle null inputs differently than the original; always test with null, undefined, empty strings, empty collections, and zero values
- **Trusting IDE refactoring tools blindly**: automated refactoring tools are generally safe but can produce incorrect results with complex generics, reflection, or metaprogramming; always verify the output
- **Missing behavioral changes in exception handling**: changing `catch (Exception e)` to `catch (IOException e)` alters which exceptions are caught; changing `finally` block contents alters cleanup behavior
- **Assuming collection order is preserved**: refactoring that changes a `List` to a `Set` or a `LinkedHashMap` to a `HashMap` can alter iteration order, which may be an observable behavioral change
- **Forgetting about performance contracts**: if the original code had O(n) time complexity and the refactored code has O(n^2), this may be considered a behavioral change in performance-sensitive contexts, even if the output is identical
- **Not testing with production-like data**: unit tests with small inputs may not reveal behavioral differences that only manifest with large datasets, special characters, or unusual encodings
- **Skipping integration-level verification**: even if all unit tests pass, the refactored code may behave differently when integrated with other components; run integration and end-to-end tests as well

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code looks the same functionally, so no formal verification is needed" | The PaymentProcessor audit example in this skill demonstrates that a syntactically similar refactoring can silently drop an audit log side effect — a behavioral change invisible to casual reading. |
| "All unit tests pass, so behavior is preserved" | Unit tests only cover paths they were written for; if the original code had no test for null inputs and the refactored version handles null differently, the behavioral change is undetected until a production null value triggers it. |
| "We used an automated IDE refactoring tool, so it's safe" | IDE tools are correct for simple renames and extractions but fail with reflection, dynamic dispatch, metaprogramming, and complex generics; automated tools produce incorrect results in these cases and must still be verified. |
| "Refactoring and bug fixing can be done in the same commit" | Mixing behavioral changes with structural changes makes preservation verification impossible — you cannot isolate which delta introduced the behavioral difference. Industry practice (e.g., Fowler's refactoring discipline) requires separate commits. |
| "We don't have time to write characterization tests before refactoring" | Characterization tests are written once and serve as the golden master for all future refactoring of the same code; the investment is amortized across every subsequent change. Skipping them means each refactoring starts from zero. |

## Verification

- [ ] All existing tests pass before and after the refactoring: test suite exits with code 0 at both commits
- [ ] Line coverage of the refactored code paths is equal to or greater than pre-refactoring coverage
- [ ] Public interface contract is unchanged: method signatures, declared exceptions, and return types verified by diff
- [ ] Side effect audit completed: every I/O operation, event emission, and log statement in the original is present in the refactored code
- [ ] Preservation report generated with APPROVE / APPROVE WITH CONDITIONS / REJECT verdict and supporting evidence
