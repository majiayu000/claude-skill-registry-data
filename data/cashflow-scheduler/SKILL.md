---
name: cashflow-scheduler
description: Optimize 30-day work schedules for cashflow management using CP-SAT and DP solvers. Use this skill when users need to plan work schedules around bills, deposits, and target balances while minimizing workdays and maximizing rest distribution.
---

# Cashflow Scheduler

## Overview

This skill provides constraint-based work schedule optimization for 30-day cashflow planning. It solves the problem: "Given my bills, deposits, and target ending balance, what's the optimal work schedule that minimizes workdays while maintaining positive daily balances?"

**Key Features:**
- **Dual solvers:** CP-SAT (OR-Tools) primary with automatic DP fallback
- **Lexicographic optimization:** Minimize workdays → back-to-back work → distance from target
- **Constraint validation:** Ensures non-negative balances, rent guard, and final band requirements
- **Self-contained:** Works immediately, no installation required (OR-Tools optional)

**When to use this skill:**
- User needs to plan gig work schedule (e.g., DoorDash, Uber, freelance)
- Optimizing work-life balance while meeting financial obligations
- Ensuring enough cash for rent while saving towards target
- Comparing different financial scenarios
- Validating existing schedules against constraints

## Quick Start

### Generate a Default Schedule (Fastest)

**Want to see it work immediately?** Run this:

```python
from core import solve, Plan, Bill, Deposit, to_cents, cents_to_str

# Default plan from plan.json (real-world example)
plan = Plan(
    start_balance_cents=to_cents(90.50),
    target_end_cents=to_cents(90.50),
    band_cents=to_cents(100.0),
    rent_guard_cents=to_cents(1636.0),
    deposits=[
        Deposit(day=10, amount_cents=to_cents(1021.0)),
        Deposit(day=24, amount_cents=to_cents(1021.0))
    ],
    bills=[
        Bill(day=1, name="Auto Insurance", amount_cents=to_cents(108.0)),
        Bill(day=2, name="YouTube Premium", amount_cents=to_cents(8.0)),
        Bill(day=5, name="Groceries", amount_cents=to_cents(112.5)),
        Bill(day=5, name="Weed", amount_cents=to_cents(20.0)),
        Bill(day=6, name="Electric", amount_cents=to_cents(139.0)),
        Bill(day=8, name="Paramount Plus", amount_cents=to_cents(12.0)),
        Bill(day=8, name="iPad AppleCare", amount_cents=to_cents(8.49)),
        Bill(day=10, name="Streaming Svcs", amount_cents=to_cents(230.0)),
        Bill(day=10, name="AI Subscription", amount_cents=to_cents(220.0)),
        Bill(day=11, name="Cat Food", amount_cents=to_cents(40.0)),
        Bill(day=12, name="Groceries", amount_cents=to_cents(112.5)),
        Bill(day=12, name="Weed", amount_cents=to_cents(20.0)),
        Bill(day=14, name="iPad AppleCare", amount_cents=to_cents(8.49)),
        Bill(day=16, name="Cat Food", amount_cents=to_cents(40.0)),
        Bill(day=19, name="Groceries", amount_cents=to_cents(112.5)),
        Bill(day=19, name="Weed", amount_cents=to_cents(20.0)),
        Bill(day=22, name="Cell Phone", amount_cents=to_cents(177.0)),
        Bill(day=23, name="Cat Food", amount_cents=to_cents(40.0)),
        Bill(day=25, name="Ring Subscription", amount_cents=to_cents(10.0)),
        Bill(day=26, name="Groceries", amount_cents=to_cents(112.5)),
        Bill(day=26, name="Weed", amount_cents=to_cents(20.0)),
        Bill(day=28, name="iPhone AppleCare", amount_cents=to_cents(13.49)),
        Bill(day=29, name="Internet", amount_cents=to_cents(30.0)),
        Bill(day=29, name="Cat Food", amount_cents=to_cents(40.0)),
        Bill(day=30, name="Rent", amount_cents=to_cents(1636.0))
    ],
    actions=[None] * 30,
    manual_adjustments=[],
    locks=[],
    metadata={}
)

schedule = solve(plan)

# Show results
w, b2b, diff = schedule.objective
print(f"✅ Schedule created!")
print(f"Workdays: {w}")
print(f"Schedule: {' '.join(schedule.actions)}")
print(f"Work on days: {[i+1 for i, a in enumerate(schedule.actions) if a == 'Spark']}")
```

**Or use the helper script:** `python examples/create_default.py`

**Then customize it!** Adjust bills, deposits, or target balance and re-solve.

---

### Adjust Mid-Month (Primary Use Case)

**Scenario:** You're on day 20 and have $230 actual balance. What should you do for the rest of the month?

**Use `adjust_from_day()`:** This function handles mid-month adjustments automatically.

```python
from core import adjust_from_day

# Your original plan (from above, or load from JSON)
# plan = Plan(...)

# Adjust from current day with actual balance
new_schedule = adjust_from_day(
    original_plan=plan,
    current_day=20,
    current_eod_balance=230.00  # Your actual balance today
)

# See what to do for days 21-30
print(f"Days 21-30: {' '.join(new_schedule.actions[20:])}")
work_days_remaining = [i+1 for i, a in enumerate(new_schedule.actions[20:], start=20) if a == 'Spark']
print(f"Work on days: {work_days_remaining}")
```

**How it works:**
1. Solves baseline schedule for the full month
2. Locks days 1-20 to baseline schedule
3. Adds adjustment to match your actual $230 balance on day 20
4. Re-solves days 21-30 optimally

**Result:** You get an updated schedule that accounts for your actual financial position!

---

### Basic Usage

```python
from core import solve, Plan, Bill, Deposit, to_cents, cents_to_str

# Create a plan
plan = Plan(
    start_balance_cents=to_cents(100.00),
    target_end_cents=to_cents(500.00),
    band_cents=to_cents(25.0),
    rent_guard_cents=to_cents(1600.0),
    deposits=[
        Deposit(day=11, amount_cents=to_cents(1021.0)),
        Deposit(day=25, amount_cents=to_cents(1021.0))
    ],
    bills=[
        Bill(day=1, name="Insurance", amount_cents=to_cents(177.0)),
        Bill(day=30, name="Rent", amount_cents=to_cents(1636.0))
    ],
    actions=[None] * 30,  # Let solver decide all days
    manual_adjustments=[],
    locks=[],
    metadata={}
)

# Solve (auto-selects CP-SAT, falls back to DP if OR-Tools unavailable)
schedule = solve(plan)

# Display results
print(f"Workdays: {schedule.objective[0]}")
print(f"Back-to-back pairs: {schedule.objective[1]}")
print(f"Distance from target: ${cents_to_str(schedule.objective[2])}")
print(f"Schedule: {' '.join(schedule.actions)}")
```

### Loading from JSON

```python
import json
from pathlib import Path
from core import Plan, Bill, Deposit, to_cents, solve

def load_plan(path: Path) -> Plan:
    with open(path) as f:
        data = json.load(f)

    return Plan(
        start_balance_cents=to_cents(data['start_balance']),
        target_end_cents=to_cents(data['target_end']),
        band_cents=to_cents(data['band']),
        rent_guard_cents=to_cents(data['rent_guard']),
        deposits=[Deposit(day=d['day'], amount_cents=to_cents(d['amount']))
                  for d in data['deposits']],
        bills=[Bill(day=b['day'], name=b['name'],
                    amount_cents=to_cents(b['amount']))
               for b in data['bills']],
        actions=data.get('actions', [None] * 30),
        manual_adjustments=[],
        locks=[],
        metadata=data.get('metadata', {})
    )

# Usage
plan = load_plan(Path('plan.json'))
schedule = solve(plan)
```

## Core Concepts

### Plan Object

Defines the problem constraints:
- **start_balance_cents:** Starting cash on Day 1
- **target_end_cents:** Desired ending balance on Day 30
- **band_cents:** Tolerance around target (final must be in [target-band, target+band])
- **rent_guard_cents:** Minimum balance required before paying rent on Day 30
- **deposits:** List of scheduled cash inflows (paychecks, deposits)
- **bills:** List of scheduled cash outflows (rent, utilities, etc.)
- **actions:** Optional pre-filled days (None = solver decides, "O" = off, "Spark" = work)
- **manual_adjustments:** One-time corrections (e.g., refunds, found money)

### Schedule Object

Contains the solution:
- **actions:** 30-element list of "O" (off) or "Spark" (work at $100/day)
- **objective:** Tuple of (workdays, back_to_back_pairs, abs_diff_from_target)
- **final_closing_cents:** Final balance on Day 30
- **ledger:** Daily ledger entries with opening/closing balances

### Constraints

**Hard constraints (must satisfy):**
1. Day 1 must be "Spark" (work day)
2. Daily closing balances must be ≥ 0
3. Day 30 pre-rent balance must be ≥ rent_guard
4. Final balance must be in [target - band, target + band]

**Soft constraints (optimized lexicographically):**
1. Minimize total workdays
2. Minimize back-to-back work pairs (prefer alternating work/rest)
3. Minimize absolute difference from exact target

## Solver Selection

The skill includes two solvers with automatic selection:

```python
# Auto-select (default): Try CP-SAT, fall back to DP
schedule = solve(plan)  # Recommended

# Force DP only
schedule = solve(plan, solver="dp")

# Force CP-SAT (raises error if OR-Tools unavailable)
schedule = solve(plan, solver="cpsat")
```

**Solver comparison:**
- **CP-SAT:** Faster on complex plans, requires OR-Tools (`pip install ortools`)
- **DP:** Pure Python, always available, slightly slower on large problems
- **Both produce identical optimal results** (proven equivalent)

## Validation

Always validate schedules before trusting them:

```python
from core import validate

report = validate(plan, schedule)

if report.ok:
    print("✅ Schedule is valid")
else:
    print("❌ Validation failed:")
    for name, ok, detail in report.checks:
        if not ok:
            print(f"  ✗ {name}: {detail}")
```

Validation checks:
- Day 1 is "Spark"
- All daily balances non-negative
- Final balance within band
- Day 30 pre-rent guard satisfied

## Example Workflows

### Workflow 1: Basic Schedule Optimization

**User request:** "I need to plan my October work schedule. I have rent on the 30th and want to save $500."

**Steps:**
1. Create Plan with bills, deposits, targets
2. Solve with `solve(plan)`
3. Validate result
4. Display work schedule

**See:** `examples/solve_basic.py`

### Workflow 2: Load Existing Plan

**User request:** "Here's my plan.json file, can you optimize it?"

**Steps:**
1. Load JSON into Plan object
2. Solve
3. Show ledger with daily balances

**See:** `examples/solve_from_json.py`

### Workflow 3: Compare Scenarios

**User request:** "What if I delay my internet bill to the 15th instead of the 5th?"

**Steps:**
1. Create two Plan variants
2. Solve both
3. Compare objectives and schedules

**See:** `examples/compare_solvers.py` (adapt for scenario comparison)

### Workflow 4: Interactive Plan Creation

**User request:** "Help me create a plan from scratch."

**Steps:**
1. Use `examples/interactive_create.py` for guided prompts
2. Build Plan incrementally
3. Solve and save to JSON

**See:** `examples/interactive_create.py`

### Workflow 5: Iterative Adjustments

**User request:** "Can you make me work less?" or "What if I move my internet bill to the 15th?"

**The skill is designed for iterative refinement:**

```python
# 1. Start with a schedule
schedule = solve(plan)
print(f"Current: {schedule.objective[0]} workdays")

# 2. User wants fewer workdays? Increase target tolerance
plan.band_cents = to_cents(150.0)  # Was 100.0
schedule = solve(plan)
print(f"Adjusted: {schedule.objective[0]} workdays")

# 3. User wants to move a bill? Update and re-solve
# Find and update bill
for bill in plan.bills:
    if bill.name == "Internet":
        plan.bills.remove(bill)
        plan.bills.append(Bill(day=15, name="Internet", amount_cents=bill.amount_cents))
        break

schedule = solve(plan)
print(f"After moving bill: {schedule.objective[0]} workdays")

# 4. User wants specific days off? Lock them
plan.actions[5:8] = ["O", "O", "O"]  # Lock days 6-8 as off
schedule = solve(plan)
print(f"With days 6-8 off: {schedule.objective[0]} workdays")
```

**Common adjustment patterns:**
- **Fewer workdays?** Increase `band_cents` or lower `target_end_cents`
- **Different work days?** Lock specific days with `plan.actions[day-1] = "Spark"` or `"O"`
- **Move bills?** Modify `plan.bills` list and re-solve
- **Add income?** Append to `plan.deposits` and re-solve
- **Account for one-time cash?** Use `plan.manual_adjustments`

## Common Issues

### "No feasible schedule found"

**Causes:**
- Bills exceed available income (start + deposits + max work income)
- target_end too high relative to available funds
- band too tight (try increasing from $25 to $50)
- rent_guard too high (reduce to just cover rent)

**Solutions:**
1. Increase band: `plan.band_cents = to_cents(50.0)`
2. Lower target: `plan.target_end_cents = to_cents(450.0)`
3. Add deposit: `plan.deposits.append(Deposit(day=15, amount_cents=to_cents(200.0)))`
4. Reduce bills or remove locked actions

**See:** [references/troubleshooting.md](references/troubleshooting.md)

### "OR-Tools CP-SAT not installed"

**Cause:** OR-Tools library missing and `dp_fallback=False`

**Solution:**
```bash
pip install ortools
```

Or use auto-fallback:
```python
schedule = solve(plan)  # Auto-falls back to DP
```

### Schedule has negative balance

**Cause:** Validation bug (should be impossible with correct solver)

**Solution:** Re-solve with fresh Plan, report as bug if persistent

## Available Resources

### Example Plans
Located in `assets/example_plans/`:
- `simple_plan.json` - Basic example with minimal bills

### Example Scripts
Located in `examples/`:
- `solve_basic.py` - Basic solve workflow
- `solve_from_json.py` - Load and solve JSON plans
- `compare_solvers.py` - Benchmark DP vs CP-SAT
- `interactive_create.py` - Interactive plan builder

### Reference Documentation
Located in `references/`:
- `plan_schema.md` - Complete JSON schema documentation
- `constraints.md` - Constraint system details
- `troubleshooting.md` - Common issues and solutions

## API Reference

### Core Functions

#### `solve(plan, solver="auto", **kwargs)`
Main solver entry point for full-month scheduling.

**Args:**
- `plan` (Plan): Problem definition
- `solver` (str): "auto", "dp", or "cpsat"
- `**kwargs`: Solver-specific options

**Returns:** Schedule object

**Raises:** RuntimeError if no solution exists

#### `adjust_from_day(original_plan, current_day, current_eod_balance, solver="auto", **kwargs)`
**PRIMARY FUNCTION for mid-month adjustments.** Use when you know your actual balance on a specific day.

**Args:**
- `original_plan` (Plan): The original full-month plan
- `current_day` (int): Current day number (1-30)
- `current_eod_balance` (float): Your actual end-of-day balance in dollars
- `solver` (str): "auto", "dp", or "cpsat"
- `**kwargs`: Solver-specific options

**Returns:** Schedule object with days 1-current_day locked and days current_day+1 to 30 re-optimized

**Raises:**
- ValueError if current_day not in 1-30
- RuntimeError if no feasible schedule exists

**Example:**
```python
# You're on day 20 with $230 actual balance
new_schedule = adjust_from_day(plan, current_day=20, current_eod_balance=230.0)
print(f"Days 21-30: {' '.join(new_schedule.actions[20:])}")
```

#### `validate(plan, schedule)`
Validate a schedule against constraints.

**Returns:** ValidationReport with ok status and check details

#### `to_cents(amount)`
Convert dollars to integer cents.

**Args:** amount (float | int | str | Decimal)

**Returns:** int (cents)

#### `cents_to_str(cents)`
Convert integer cents to dollar string.

**Args:** cents (int)

**Returns:** str (e.g., "123.45")

### Data Classes

#### `Plan`
Problem definition.

**Fields:** start_balance_cents, target_end_cents, band_cents, rent_guard_cents, deposits, bills, actions, manual_adjustments, locks, metadata

#### `Schedule`
Solution.

**Fields:** actions, objective, final_closing_cents, ledger

#### `Bill`
Scheduled outflow.

**Fields:** day (1-30), name (str), amount_cents (int)

#### `Deposit`
Scheduled inflow.

**Fields:** day (1-30), amount_cents (int)

## Advanced Usage

### Using CP-SAT Options

```python
from core.cpsat_solver import CPSATSolveOptions

options = CPSATSolveOptions(
    max_time_seconds=30.0,
    num_search_workers=4,
    log_search_progress=True
)

schedule = solve(plan, solver="cpsat", options=options)
```

### Locking Specific Days

```python
# Force Day 1 to work, Day 2 to off, let solver decide rest
plan.actions = ["Spark", "O"] + [None] * 28

schedule = solve(plan)
```

### Manual Adjustments

```python
from core import Adjustment

# One-time correction on Day 15
plan.manual_adjustments = [
    Adjustment(day=15, amount_cents=to_cents(-50.0), note="Venmo refund")
]

schedule = solve(plan)
```

## Tips for Success

1. **Start simple:** Use example plans as templates
2. **Validate always:** Check `report.ok` before trusting results
3. **Use auto-fallback:** Default `solver="auto"` ensures robustness
4. **Increase band if infeasible:** Try $50+ instead of $25
5. **Check total funds:** Ensure start + deposits >= bills + target
6. **Prefer fewer locks:** Only lock days if absolutely necessary

## See Also

- [plan_schema.md](references/plan_schema.md) - Complete JSON format
- [constraints.md](references/constraints.md) - Constraint system deep dive
- [troubleshooting.md](references/troubleshooting.md) - Debugging guide
- Example scripts in `examples/` for working code
