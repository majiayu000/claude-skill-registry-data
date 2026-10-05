---
name: directed-test-input-generator
description: Generate targeted test inputs to reach specific code paths using path condition analysis, symbolic execution concepts, constraint solving, and.
---

# Directed Test Input Generator

Generate test inputs that are specifically crafted to exercise targeted code paths, reach hard-to-trigger branches, and satisfy complex preconditions. Unlike random fuzzing that explores the input space broadly, directed test input generation analyzes the code structure to produce inputs that reach specific locations in the program, enabling precise testing of error handlers, deep conditional logic, and rarely executed code paths.

## When to Use This Skill

Use this skill when you need to:

- Reach specific branches or code paths that random testing does not cover
- Generate inputs that satisfy complex multi-condition predicates
- Test error handling paths that require specific failure conditions
- Achieve coverage targets for specific uncovered lines or branches
- Exercise deeply nested conditional logic
- Generate inputs for functions with complex validation rules
- Create regression tests that reproduce specific execution paths
- Test code paths that require specific combinations of configuration and input

**Trigger phrases**: "reach this branch", "cover this path", "generate input for", "path coverage", "branch coverage", "directed testing", "targeted input", "constraint solving", "symbolic execution", "path condition", "cover specific code", "test this error path"

## What This Skill Does

### Core Concepts

#### Path Conditions

A path condition is the conjunction of all branch conditions that must be true (or false) for execution to reach a specific program point. To generate an input that reaches that point, you solve the path condition to find satisfying values.

**Example:**
```python
def classify(x, y):
    if x > 0:           # Condition 1
        if y > x:        # Condition 2
            if x + y > 100:  # Condition 3
                return "high"  # Target path
```

Path condition to reach "high": `x > 0 AND y > x AND x + y > 100`
Satisfying input: `x = 40, y = 70` (because 40 > 0, 70 > 40, and 40 + 70 > 100)

#### Symbolic Execution

Symbolic execution treats program inputs as symbolic variables rather than concrete values. It traces execution paths symbolically, building path conditions that can be solved by constraint solvers (SMT solvers like Z3).

#### Coverage-Directed Generation

Analyze which branches or lines are not covered by existing tests, determine the path conditions needed to reach them, and generate inputs that satisfy those conditions.

### Approach

1. **Identify the target**: The specific line, branch, or code path you want to reach
2. **Trace the path**: Walk backward from the target to the function entry, collecting all branch conditions
3. **Formulate constraints**: Express the path condition as a set of logical constraints
4. **Solve constraints**: Find concrete input values that satisfy all constraints
5. **Generate the test**: Create a test case using the solved values
6. **Verify coverage**: Run the test with coverage instrumentation to confirm the target is reached

## Instructions

### Step 1: Analyze Path Conditions Manually

Before using automated tools, practice identifying path conditions by reading the code.

**Python (target function with complex branching):**
```python
def calculate_shipping(weight: float, distance: float, priority: str,
                       member: bool, coupon_code: str = None) -> float:
    """Calculate shipping cost with complex business rules.

    Multiple code paths based on weight, distance, priority, membership,
    and coupon validity.
    """
    if weight <= 0 or distance <= 0:
        raise ValueError("Weight and distance must be positive")

    base_rate = 5.0

    # Weight tiers
    if weight <= 1.0:
        weight_multiplier = 1.0
    elif weight <= 5.0:
        weight_multiplier = 1.5
    elif weight <= 20.0:
        weight_multiplier = 2.5
    else:
        weight_multiplier = 4.0  # PATH A: heavy package

    # Distance tiers
    if distance <= 50:
        distance_factor = 1.0
    elif distance <= 500:
        distance_factor = 2.0
    else:
        distance_factor = 3.5  # PATH B: long distance

    cost = base_rate * weight_multiplier * distance_factor

    # Priority surcharge
    if priority == "express":
        cost *= 2.0
    elif priority == "overnight":
        cost *= 3.0                # PATH C: overnight

    # Member discount
    if member and cost > 50:       # PATH D: member discount on expensive orders
        cost *= 0.85

    # Coupon processing
    if coupon_code is not None:
        if coupon_code == "FREESHIP2024" and cost < 100:
            cost = 0.0             # PATH E: free shipping coupon
        elif coupon_code == "HALF50" and cost >= 50:
            cost *= 0.5            # PATH F: 50% off coupon
        elif coupon_code.startswith("FLAT"):
            try:
                flat_amount = float(coupon_code[4:])
                if flat_amount > 0 and flat_amount <= cost:
                    cost -= flat_amount  # PATH G: flat discount coupon
            except ValueError:
                pass  # PATH H: invalid coupon format

    return round(cost, 2)
```

**Directed tests for each path:**
```python
import pytest


class TestCalculateShippingDirectedPaths:
    """Directed tests that target specific code paths."""

    # PATH A: heavy package (weight > 20)
    def test_path_a_heavy_package_multiplier(self):
        # Path condition: weight > 20, distance <= 50
        result = calculate_shipping(
            weight=25.0, distance=30, priority="standard", member=False
        )
        # base_rate(5) * weight_mult(4.0) * dist_factor(1.0) = 20.0
        assert result == 20.0

    # PATH B: long distance (distance > 500)
    def test_path_b_long_distance_factor(self):
        # Path condition: weight <= 1, distance > 500
        result = calculate_shipping(
            weight=0.5, distance=600, priority="standard", member=False
        )
        # base_rate(5) * weight_mult(1.0) * dist_factor(3.5) = 17.5
        assert result == 17.5

    # PATH C: overnight priority
    def test_path_c_overnight_surcharge(self):
        # Path condition: priority == "overnight"
        result = calculate_shipping(
            weight=2.0, distance=100, priority="overnight", member=False
        )
        # base_rate(5) * weight_mult(1.5) * dist_factor(2.0) * overnight(3.0) = 45.0
        assert result == 45.0

    # PATH D: member discount on expensive order
    def test_path_d_member_discount_expensive_order(self):
        # Path condition: member=True AND cost > 50
        # Need: base * weight * dist * priority > 50
        result = calculate_shipping(
            weight=25.0, distance=600, priority="express", member=True
        )
        # base(5) * weight(4.0) * dist(3.5) * express(2.0) = 140.0
        # member discount: 140.0 * 0.85 = 119.0
        assert result == 119.0

    # PATH E: free shipping coupon (cost < 100)
    def test_path_e_free_shipping_coupon(self):
        # Path condition: coupon == "FREESHIP2024" AND cost < 100
        result = calculate_shipping(
            weight=1.0, distance=50, priority="standard",
            member=False, coupon_code="FREESHIP2024"
        )
        # base(5) * weight(1.0) * dist(1.0) = 5.0 < 100
        assert result == 0.0

    # PATH F: half-off coupon (cost >= 50)
    def test_path_f_half_off_coupon(self):
        # Path condition: coupon == "HALF50" AND cost >= 50
        result = calculate_shipping(
            weight=25.0, distance=600, priority="standard",
            member=False, coupon_code="HALF50"
        )
        # base(5) * weight(4.0) * dist(3.5) = 70.0 >= 50
        # 70.0 * 0.5 = 35.0
        assert result == 35.0

    # PATH G: flat discount coupon (valid format, amount <= cost)
    def test_path_g_flat_discount_coupon(self):
        # Path condition: coupon starts with "FLAT", parseable number, > 0, <= cost
        result = calculate_shipping(
            weight=10.0, distance=100, priority="standard",
            member=False, coupon_code="FLAT10"
        )
        # base(5) * weight(2.5) * dist(2.0) = 25.0
        # 25.0 - 10.0 = 15.0
        assert result == 15.0

    # PATH H: invalid flat coupon format
    def test_path_h_invalid_flat_coupon_format(self):
        # Path condition: coupon starts with "FLAT", not parseable as float
        result = calculate_shipping(
            weight=2.0, distance=100, priority="standard",
            member=False, coupon_code="FLATabc"
        )
        # base(5) * weight(1.5) * dist(2.0) = 15.0 (coupon ignored)
        assert result == 15.0
```

**JavaScript:**
```javascript
describe("calculateShipping directed path tests", () => {
  // PATH A: heavy package (weight > 20)
  test("path A: heavy package weight multiplier", () => {
    const result = calculateShipping(25.0, 30, "standard", false);
    expect(result).toBe(20.0);
  });

  // PATH B: long distance (distance > 500)
  test("path B: long distance factor", () => {
    const result = calculateShipping(0.5, 600, "standard", false);
    expect(result).toBe(17.5);
  });

  // PATH C: overnight priority
  test("path C: overnight surcharge", () => {
    const result = calculateShipping(2.0, 100, "overnight", false);
    expect(result).toBe(45.0);
  });

  // PATH D: member discount on expensive order
  test("path D: member discount when cost > 50", () => {
    const result = calculateShipping(25.0, 600, "express", true);
    expect(result).toBe(119.0);
  });

  // PATH E: free shipping coupon
  test("path E: FREESHIP2024 coupon with cost < 100", () => {
    const result = calculateShipping(1.0, 50, "standard", false, "FREESHIP2024");
    expect(result).toBe(0.0);
  });

  // PATH F: half-off coupon
  test("path F: HALF50 coupon with cost >= 50", () => {
    const result = calculateShipping(25.0, 600, "standard", false, "HALF50");
    expect(result).toBe(35.0);
  });

  // PATH G: valid flat discount coupon
  test("path G: flat discount coupon", () => {
    const result = calculateShipping(10.0, 100, "standard", false, "FLAT10");
    expect(result).toBe(15.0);
  });

  // PATH H: invalid flat coupon format
  test("path H: invalid flat coupon ignored", () => {
    const result = calculateShipping(2.0, 100, "standard", false, "FLATabc");
    expect(result).toBe(15.0);
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculateShippingDirectedTest {

    @Test
    void pathA_heavyPackageWeightMultiplier() {
        double result = ShippingCalculator.calculate(25.0, 30, "standard", false, null);
        assertEquals(20.0, result, 0.01);
    }

    @Test
    void pathB_longDistanceFactor() {
        double result = ShippingCalculator.calculate(0.5, 600, "standard", false, null);
        assertEquals(17.5, result, 0.01);
    }

    @Test
    void pathC_overnightSurcharge() {
        double result = ShippingCalculator.calculate(2.0, 100, "overnight", false, null);
        assertEquals(45.0, result, 0.01);
    }

    @Test
    void pathD_memberDiscountOnExpensiveOrder() {
        double result = ShippingCalculator.calculate(25.0, 600, "express", true, null);
        assertEquals(119.0, result, 0.01);
    }

    @Test
    void pathE_freeShippingCoupon() {
        double result = ShippingCalculator.calculate(1.0, 50, "standard", false, "FREESHIP2024");
        assertEquals(0.0, result, 0.01);
    }

    @Test
    void pathF_halfOffCoupon() {
        double result = ShippingCalculator.calculate(25.0, 600, "standard", false, "HALF50");
        assertEquals(35.0, result, 0.01);
    }

    @Test
    void pathG_flatDiscountCoupon() {
        double result = ShippingCalculator.calculate(10.0, 100, "standard", false, "FLAT10");
        assertEquals(15.0, result, 0.01);
    }

    @Test
    void pathH_invalidFlatCouponIgnored() {
        double result = ShippingCalculator.calculate(2.0, 100, "standard", false, "FLATabc");
        assertEquals(15.0, result, 0.01);
    }
}
```

### Step 2: Use Constraint Solving for Complex Path Conditions

**Python (using Z3 solver):**
```python
from z3 import Int, Real, String, Solver, sat, And, Or, Not, If


def solve_path_condition_for_discount():
    """Use Z3 to find inputs that reach the member discount path.

    Path condition: member=True AND cost > 50
    Where cost = base(5) * weight_mult * dist_factor * priority_mult
    """
    solver = Solver()

    weight = Real("weight")
    distance = Real("distance")

    # Constraints from the code
    solver.add(weight > 0)
    solver.add(distance > 0)

    # Weight multiplier (choose the weight > 20 tier for a large cost)
    weight_mult = If(weight <= 1, 1.0,
                  If(weight <= 5, 1.5,
                  If(weight <= 20, 2.5, 4.0)))

    # Distance factor (choose distance > 500 for a large cost)
    dist_factor = If(distance <= 50, 1.0,
                  If(distance <= 500, 2.0, 3.5))

    # Priority multiplier (use "express" = 2.0)
    priority_mult = Real("priority_mult")
    solver.add(priority_mult == 2.0)

    # Cost calculation
    cost = 5.0 * weight_mult * dist_factor * priority_mult

    # Target: member discount path (cost > 50)
    solver.add(cost > 50)

    # Solve
    if solver.check() == sat:
        model = solver.model()
        print(f"weight = {model[weight]}")
        print(f"distance = {model[distance]}")
        return {
            "weight": float(model[weight].as_fraction()),
            "distance": float(model[distance].as_fraction()),
        }
    else:
        print("No satisfying input found")
        return None


# Generate test from solved constraints
solved = solve_path_condition_for_discount()
if solved:
    print(f"Generated test input: weight={solved['weight']}, distance={solved['distance']}")
```

### Step 3: Use Coverage Analysis to Identify Uncovered Paths

**Python (using coverage.py to find gaps):**
```python
import subprocess
import json
from pathlib import Path


def find_uncovered_branches(module_path: str, test_path: str) -> list[dict]:
    """Run tests with branch coverage and identify uncovered branches."""
    # Run pytest with coverage in JSON format
    subprocess.run([
        "python", "-m", "pytest", test_path,
        "--cov", module_path,
        "--cov-branch",
        "--cov-report", "json:coverage.json",
        "--no-header", "-q",
    ], capture_output=True)

    # Parse coverage report
    report = json.loads(Path("coverage.json").read_text())

    uncovered = []
    for filename, data in report.get("files", {}).items():
        missing_lines = data.get("missing_lines", [])
        missing_branches = data.get("missing_branches", [])

        for line in missing_lines:
            uncovered.append({
                "file": filename,
                "line": line,
                "type": "line",
            })
        for branch in missing_branches:
            uncovered.append({
                "file": filename,
                "branch_from": branch[0],
                "branch_to": branch[1],
                "type": "branch",
            })

    return uncovered


def generate_directed_test_for_branch(source_code: str, branch_from: int,
                                       branch_to: int) -> str:
    """Analyze the branch condition and suggest a directed test input.

    This function reads the source code around the branch point to understand
    the condition that must be satisfied.
    """
    lines = source_code.splitlines()
    condition_line = lines[branch_from - 1].strip()

    return f"""
# Directed test for uncovered branch at line {branch_from} -> {branch_to}
# Branch condition: {condition_line}
# TODO: Determine input values that make this condition {'True' if branch_to == branch_from + 1 else 'False'}
def test_directed_branch_{branch_from}_to_{branch_to}():
    # Solve the path condition to reach this branch
    # Condition: {condition_line}
    pass  # Replace with concrete test
"""


# Usage: find and generate tests for uncovered branches
uncovered = find_uncovered_branches("mymodule", "tests/")
for gap in uncovered[:5]:
    if gap["type"] == "branch":
        print(f"Uncovered branch: line {gap['branch_from']} -> {gap['branch_to']}")
```

**JavaScript (using Istanbul/nyc for coverage gaps):**
```javascript
// Script to analyze coverage gaps and suggest directed tests
const fs = require("fs");
const path = require("path");

function findUncoveredBranches(coverageFile) {
  const coverage = JSON.parse(fs.readFileSync(coverageFile, "utf-8"));
  const gaps = [];

  for (const [file, data] of Object.entries(coverage)) {
    // Analyze branch coverage
    if (data.branchMap) {
      for (const [branchId, branchInfo] of Object.entries(data.branchMap)) {
        const counts = data.b[branchId];
        counts.forEach((count, idx) => {
          if (count === 0) {
            gaps.push({
              file,
              branchId,
              branchType: branchInfo.type,
              location: branchInfo.locations[idx],
              uncoveredArm: idx,
            });
          }
        });
      }
    }
  }

  return gaps;
}

// After running: npx nyc --reporter=json jest
// Parse .nyc_output/coverage.json to find gaps
const gaps = findUncoveredBranches(".nyc_output/coverage-final.json");
gaps.forEach((gap) => {
  console.log(
    `Uncovered: ${gap.file} branch ${gap.branchId} arm ${gap.uncoveredArm} ` +
    `at line ${gap.location.start.line}`
  );
});
```

### Step 4: Apply Coverage-Directed Test Generation Strategy

**Python:**
```python
import pytest
from hypothesis import given, strategies as st, assume


class TestDirectedCoverageGeneration:
    """Generate tests directed at specific uncovered branches."""

    # Suppose coverage analysis reveals that the "weight > 20 AND distance > 500
    # AND priority == overnight AND member AND coupon == HALF50" path is uncovered.
    # This is a 5-condition conjunction.

    def test_all_conditions_simultaneously(self):
        """Directed test: reach the path where all conditions align."""
        result = calculate_shipping(
            weight=30.0,      # weight > 20 -> multiplier = 4.0
            distance=1000,    # distance > 500 -> factor = 3.5
            priority="overnight",  # priority == "overnight" -> *3.0
            member=True,      # member=True
            coupon_code="HALF50",  # coupon == "HALF50"
        )
        # base(5) * 4.0 * 3.5 * 3.0 = 210.0
        # member discount (cost > 50): 210.0 * 0.85 = 178.5
        # HALF50 (cost >= 50): 178.5 * 0.5 = 89.25
        assert result == 89.25

    # Use Hypothesis to find inputs that satisfy complex constraints
    @given(
        weight=st.floats(min_value=20.01, max_value=100.0),
        distance=st.floats(min_value=500.01, max_value=5000.0),
    )
    def test_heavy_long_distance_path_always_expensive(self, weight, distance):
        """Directed exploration of the heavy + long distance quadrant."""
        result = calculate_shipping(
            weight=weight,
            distance=distance,
            priority="standard",
            member=False,
        )
        # base(5) * 4.0 * 3.5 = 70.0 minimum
        assert result >= 70.0

    @given(
        weight=st.floats(min_value=0.01, max_value=1.0),
        distance=st.floats(min_value=0.01, max_value=50.0),
    )
    def test_light_short_path_always_cheap(self, weight, distance):
        """Directed exploration of the light + short distance quadrant."""
        result = calculate_shipping(
            weight=weight,
            distance=distance,
            priority="standard",
            member=False,
        )
        # base(5) * 1.0 * 1.0 = 5.0 exactly
        assert result == 5.0
```

### Step 5: Generate Tests for Error Handling Paths

**Python:**
```python
class TestErrorPathGeneration:
    """Directed tests for error handling and exception paths."""

    def test_weight_zero_raises_value_error(self):
        """Path: weight <= 0 branch."""
        with pytest.raises(ValueError, match="Weight and distance must be positive"):
            calculate_shipping(0, 100, "standard", False)

    def test_weight_negative_raises_value_error(self):
        """Path: weight <= 0 branch (negative value)."""
        with pytest.raises(ValueError, match="Weight and distance must be positive"):
            calculate_shipping(-5.0, 100, "standard", False)

    def test_distance_zero_raises_value_error(self):
        """Path: distance <= 0 branch."""
        with pytest.raises(ValueError, match="Weight and distance must be positive"):
            calculate_shipping(1.0, 0, "standard", False)

    def test_distance_negative_raises_value_error(self):
        """Path: distance <= 0 branch (negative value)."""
        with pytest.raises(ValueError, match="Weight and distance must be positive"):
            calculate_shipping(1.0, -100, "standard", False)

    def test_both_invalid_raises_on_first_check(self):
        """Path: both weight and distance invalid."""
        with pytest.raises(ValueError):
            calculate_shipping(-1.0, -1.0, "standard", False)
```

**JavaScript:**
```javascript
describe("error path directed tests", () => {
  test("weight = 0 throws ValueError", () => {
    expect(() => calculateShipping(0, 100, "standard", false)).toThrow(
      "Weight and distance must be positive"
    );
  });

  test("negative weight throws ValueError", () => {
    expect(() => calculateShipping(-5.0, 100, "standard", false)).toThrow(
      "Weight and distance must be positive"
    );
  });

  test("distance = 0 throws ValueError", () => {
    expect(() => calculateShipping(1.0, 0, "standard", false)).toThrow(
      "Weight and distance must be positive"
    );
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ErrorPathDirectedTest {

    @Test
    void weightZeroThrowsIllegalArgument() {
        assertThrows(IllegalArgumentException.class,
                () -> ShippingCalculator.calculate(0, 100, "standard", false, null));
    }

    @Test
    void negativeWeightThrowsIllegalArgument() {
        assertThrows(IllegalArgumentException.class,
                () -> ShippingCalculator.calculate(-5.0, 100, "standard", false, null));
    }

    @Test
    void distanceZeroThrowsIllegalArgument() {
        assertThrows(IllegalArgumentException.class,
                () -> ShippingCalculator.calculate(1.0, 0, "standard", false, null));
    }

    @Test
    void bothInvalidThrowsOnFirstCheck() {
        assertThrows(IllegalArgumentException.class,
                () -> ShippingCalculator.calculate(-1.0, -1.0, "standard", false, null));
    }
}
```

### Step 6: Systematic Branch Targeting with Decision Tables

**Python:**
```python
import pytest


class TestDecisionTableDirected:
    """Use a decision table to systematically cover all branch combinations."""

    @pytest.mark.parametrize(
        "weight_tier, distance_tier, priority, member, coupon, description",
        [
            # Each row targets a unique combination of branches
            ("light",  "short", "standard",  False, None,           "minimal path"),
            ("light",  "short", "express",   False, None,           "express on cheap"),
            ("light",  "short", "overnight", False, None,           "overnight on cheap"),
            ("light",  "medium", "standard", False, None,           "medium distance"),
            ("light",  "long",  "standard",  False, None,           "long distance"),
            ("medium", "short", "standard",  False, None,           "medium weight"),
            ("heavy",  "short", "standard",  False, None,           "heavy weight"),
            ("extra",  "long",  "overnight", True,  None,           "max cost path"),
            ("extra",  "long",  "overnight", True,  "HALF50",       "max cost + coupon"),
            ("light",  "short", "standard",  False, "FREESHIP2024", "free shipping"),
            ("light",  "short", "standard",  False, "FLAT5",        "flat discount"),
            ("light",  "short", "standard",  False, "FLATabc",      "invalid flat coupon"),
        ],
    )
    def test_branch_combination(self, weight_tier, distance_tier, priority,
                                 member, coupon, description):
        weight_map = {"light": 0.5, "medium": 3.0, "heavy": 15.0, "extra": 30.0}
        distance_map = {"short": 25, "medium": 200, "long": 800}

        weight = weight_map[weight_tier]
        distance = distance_map[distance_tier]

        result = calculate_shipping(weight, distance, priority, member, coupon)
        assert result >= 0, f"Negative shipping cost for {description}"
```

## Best Practices

- **Map the code's control flow graph before writing tests**: Understanding all branches and their conditions is a prerequisite for directed generation; draw the CFG or use a tool to visualize it
- **Use coverage reports to identify gaps**: Do not guess which paths are uncovered; use coverage tools (coverage.py, Istanbul/nyc, JaCoCo) to identify exact gaps
- **Solve path conditions manually for small functions**: For functions with fewer than 10 branches, manual analysis is faster and more reliable than automated tools
- **Use constraint solvers (Z3) for complex conditions**: When path conditions involve arithmetic, string operations, or 10+ conjuncts, automated solving prevents errors
- **Create decision tables for systematic coverage**: For functions with n independent boolean conditions, a decision table with 2^n rows (or a reduced set using pairwise coverage) ensures all combinations are tested
- **Document the path condition in each test**: Write a comment explaining which branch condition each test input is designed to satisfy; this makes the test maintainable
- **Verify coverage after writing directed tests**: Always run coverage analysis after adding directed tests to confirm you reached the intended path
- **Combine with random testing**: Directed tests reach specific paths; random testing finds unexpected bugs; use both together for comprehensive coverage

## Common Pitfalls

- **Targeting lines instead of branches**: Line coverage can be 100% while branch coverage is below 50%; always target branch coverage, which requires both true and false evaluations of each condition
- **Ignoring implicit branches**: Exception handling (`try`/`catch`), short-circuit evaluation (`a && b`), and ternary operators (`x ? y : z`) create branches that are easy to miss
- **Not considering path feasibility**: Some branches may be infeasible (dead code) because their path conditions are unsatisfiable; do not spend time trying to reach unreachable paths
- **Generating inputs without verifying the path**: A directed test input that you believe reaches a target may actually take a different path due to a miscalculation; always verify with coverage instrumentation
- **Over-relying on constraint solvers**: Constraint solvers struggle with floating-point arithmetic, string operations, and external dependencies; use them for integer and boolean constraints where they excel
- **Forgetting compound conditions**: A branch like `if a > 0 and b < 10 and c != ""` requires all three conjuncts to be true; missing any one causes the test to take the wrong path
- **Not testing both sides of every branch**: Directing a test to reach the `if` branch is only half the job; you also need a test that takes the `else` branch
- **Confusing path coverage with correctness**: Reaching a code path does not guarantee correctness; you still need meaningful assertions about the output
