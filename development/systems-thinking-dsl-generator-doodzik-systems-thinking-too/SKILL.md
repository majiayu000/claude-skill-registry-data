---
name: systems-thinking-dsl-generator
description: Generates DSL code for the Systems Thinking Tool (systemsthinkingtool.com). Creates system dynamics models with stocks, flows, constants, delays, lookup tables, and graphs. Based on actual implementation at github.com/doodzik/systems-thinking-tool.
---

# Systems Thinking Tool DSL Generator

Generates DSL code for the browser-based Systems Thinking Tool. Models systems using stocks (accumulations), flows (rates of change), delays, and nonlinear relationships.

## When to Use This Skill

- Modeling systems with feedback loops and causal relationships
- Creating stock-and-flow diagrams for system dynamics
- Understanding how systems change over time
- Analyzing business, ecological, social, or technical systems
- Simulating scenarios with delays and nonlinear effects

## Core DSL Syntax

### Stocks (Accumulations)

Stocks represent quantities that accumulate over time.

**Syntax:**
```
stock StockName {
  initial: <number>
  units: "<string>"
  min: <number>
  max: <number>
}
```

**Properties:**
- `initial` (required): Starting value
- `units` (optional): Unit of measurement (e.g., "people", "dollars")
- `min` (optional): Minimum value constraint (automatically enforced)
- `max` (optional): Maximum value constraint (automatically enforced)

**Examples:**
```
stock Population {
  initial: 100
  min: 0
  units: "people"
}

stock Temperature {
  initial: 68
  min: 0
  max: 100
  units: "°F"
}
```

---

### Flows (Rates of Change)

Flows move quantities between stocks or external sources/sinks.

**Syntax:**
```
flow FlowName {
  from: <source>
  to: <target>
  rate: <expression>
  units: "<string>"
}
```

**Properties:**
- `from` (required): Stock name, `source` (infinite), or omit for null
- `to` (required): Stock name, `sink` (infinite), or omit for null  
- `rate` (required): Number or expression
- `units` (optional): Unit of measurement

**Source/Sink:**
- `source` = infinite external source (cloud icon)
- `sink` = infinite external sink (cloud icon)
- Stock name = flow between stocks

**Examples:**
```
// From infinite source to stock
flow Births {
  from: source
  to: Population
  rate: Population * 0.02
}

// Between stocks
flow Transfer {
  from: StockA
  to: StockB
  rate: StockA * 0.1
}

// To infinite sink
flow Deaths {
  from: Population
  to: sink
  rate: Population * 0.01
}
```

---

### Constants

Define reusable numeric values.

**Syntax:**
```
const ConstantName = <value>
```

**Examples:**
```
const GrowthRate = 0.05
const MaxCapacity = 1000
const DelayTime = 6
```

Use in expressions: `rate: Population * GrowthRate`

---

### Lookup Tables (1D)

Define nonlinear relationships between two variables.

**Syntax:**
```
lookup TableName {
  [x1, y1]
  [x2, y2]
  [x3, y3]
}
```

**Behavior:**
- Linear interpolation between points
- Points auto-sorted by x value
- Extrapolates with first/last value

**Usage:**
```
LOOKUP(input, TableName)
```

**Example:**
```
lookup CrowdingEffect {
  [0, 1.0]      // 0% capacity = 100% productivity
  [50, 0.95]    // 50% = slight drop
  [90, 0.60]    // 90% = major drop
  [110, 0.20]   // Overcrowded
}

flow Productivity {
  from: source
  to: Output
  rate: Workers * LOOKUP(Occupancy, CrowdingEffect)
}
```

---

### Lookup Tables (2D)

Define relationships with two input variables.

**Syntax:**
```
lookup2d TableName {
  [x1, y1]: z1
  [x2, y2]: z2
  [x3, y3]: z3
}
```

**Usage:**
```
LOOKUP2D(inputX, inputY, TableName)
```

**Example:**
```
lookup2d ReactionYield {
  [20, 1]: 10
  [20, 5]: 25
  [80, 1]: 45
  [80, 5]: 75
}

flow ChemicalYield {
  rate: LOOKUP2D(Temperature, Pressure, ReactionYield)
}
```

---

### Graphs (Visualization Config)

Define custom graphs for visualization.

**Syntax:**
```
graph GraphName {
  title: "<string>"
  variables: Var1, Var2, Var3
  type: line | area
  yAxisLabel: "<string>"
  color: "<hex_color>"
}
```

**Example:**
```
graph PopulationTrend {
  title: "Population Over Time"
  variables: Population, Capacity
  type: line
  yAxisLabel: "People"
}

graph RevenueArea {
  title: "Revenue Growth"
  variables: Revenue
  type: area
  color: "#10b981"
}
```

---

### Termination Conditions

Stop simulation when condition is met.

**Syntax:**
```
terminate {
  when: <boolean_expression>
}
```

**Example:**
```
terminate {
  when: Population <= 5 || Resources <= 0 || TIME >= 100
}
```

---

## Rate Expressions

### Operators

**Arithmetic:** `+`, `-`, `*`, `/`, `%`  
**Comparison:** `<`, `>`, `<=`, `>=`, `==`, `!=`  
**Logical:** `&&`, `||`, `!`  
**Ternary:** `condition ? valueIfTrue : valueIfFalse`

**Examples:**
```
rate: Stock1 + Stock2
rate: Stock > 100 ? 10 : 5
rate: (Stock1 / Stock2) * 0.5
rate: Stock > 0 && Stock < 100 ? Stock * 0.1 : 0
```

---

### Stock References

Reference stocks directly by name:
```
rate: Population * 0.02
rate: Resources / Population
rate: (StockA + StockB) / 2
```

---

### Math Functions

All standard JavaScript Math functions available:

**Basic:**
- `min(a, b, ...)` - Minimum
- `max(a, b, ...)` - Maximum  
- `abs(x)` - Absolute value

**Rounding:**
- `floor(x)`, `ceil(x)`, `round(x)`

**Exponential:**
- `sqrt(x)` - Square root
- `pow(base, exp)` - Exponentiation
- `exp(x)` - e^x
- `log(x)` - Natural log

**Trigonometric:**
- `sin(x)`, `cos(x)`, `tan(x)`

**Examples:**
```
rate: sqrt(MarketingBudget) * 10
rate: pow(Users, 2) * 0.001
rate: min(Demand, Capacity)
rate: max(0, Stock - 10)
```

---

### Built-in Constants

- `TIME` - Current simulation time
- `dt` - Time step (default: 1)
- `PI` - 3.14159...
- `E` - 2.71828...

**Example:**
```
rate: 10 * sin(2 * PI * TIME / 12)
```

---

## Delay Functions

### SMOOTH (Exponential Averaging)

**What it does:** Creates moving average that gradually adapts.

**When to use:**
- Perception lags
- Market awareness
- Reputation/brand value
- Noise filtering

**Syntax:**
```
SMOOTH(input, smoothingTime)
```

**Behavior:**
- Adapts immediately but gradually
- 63% adapted after 1 time period
- 95% adapted after 3 time periods

**Example:**
```
const PerceptionTime = 6

stock PerceivedQuality {
  initial: 70
}

flow PerceptionUpdate {
  from: source
  to: PerceivedQuality
  rate: (SMOOTH(ActualQuality, PerceptionTime) - PerceivedQuality) / 1
}
```

---

### DELAY (Physical Pipeline)

**What it does:** Exact time delay - what goes in now comes out N periods later.

**When to use:**
- Manufacturing pipelines
- Shipping in transit
- Construction projects
- Aging processes

**Syntax:**
```
DELAY(input, delayTime)
```

**Behavior:**
- No output change until delay passes
- Sharp transition
- Exactly preserves timing

**Example:**
```
const ShippingTime = 14

flow ProductsShipped {
  from: OrdersReceived
  to: Delivered
  rate: DELAY(OrderRate, ShippingTime)
}
```

---

### DELAY_GRADUAL (Smooth Material Delay)

**What it does:** Realistic delay with natural timing variation.

**When to use:**
- Training programs
- Multi-stage production
- Biological growth
- Information diffusion

**Syntax:**
```
DELAY_GRADUAL(input, delayTime)
```

**Behavior:**
- Smooth bell-curve response
- Peak output around 1.5× delay time
- Models real-world variation

**Example:**
```
const TrainingTime = 3

flow TrainingComplete {
  from: NewHires
  to: ProductiveEmployees
  rate: DELAY_GRADUAL(HiringRate, TrainingTime)
}
```

---

## Time-Based Patterns

Use lookup tables with TIME as input for any time pattern.

### Simple Policy Change (Step)

```
lookup BudgetPolicy {
  [0, 1000]
  [12, 1500]   // Increase at month 12
  [24, 1500]
}

flow MonthlyBudget {
  rate: LOOKUP(TIME, BudgetPolicy)
}
```

### Campaign (Pulse)

```
lookup CampaignIntensity {
  [0, 0]
  [6, 100]     // Start at month 6
  [9, 100]     // End at month 9
  [9, 0]
  [24, 0]
}

flow MarketingSpend {
  rate: LOOKUP(TIME, CampaignIntensity)
}
```

### Seasonal Pattern (Repeating)

```
lookup SeasonalMultiplier {
  [0, 1.0]
  [3, 1.2]
  [6, 1.5]     // Summer peak
  [9, 1.1]
  [12, 1.0]
}

flow SeasonalSales {
  rate: BaseSales * LOOKUP(TIME % 12, SeasonalMultiplier)
}
```

Use `TIME % period` for repeating patterns!

---

## Complete Examples

### Example 1: Population with Resource Limits

```
const BirthRate = 0.02
const BaseDeathRate = 0.01
const ConsumptionRate = 0.1
const MortalityDelay = 5

lookup ResourceStressEffect {
  [2.0, 0.00]    // Abundant resources
  [1.0, 0.02]    // Moderate stress
  [0.5, 0.05]    // High stress
  [0.0, 0.15]    // Critical
}

stock Population {
  initial: 100
  min: 0
  units: "people"
}

stock Resources {
  initial: 100
  min: 0
  units: "units"
}

flow Births {
  from: source
  to: Population
  rate: Population * BirthRate
}

flow Deaths {
  from: Population
  to: sink
  rate: Population * (BaseDeathRate + DELAY_GRADUAL(
    LOOKUP(Resources / Population, ResourceStressEffect),
    MortalityDelay
  ))
}

flow Consumption {
  from: Resources
  to: sink
  rate: Population * ConsumptionRate
}

graph PopulationVsResources {
  title: "Population vs Resources"
  variables: Population, Resources
  type: line
}
```

**System behavior:** Population grows exponentially but resource depletion increases death rate through stress. Demonstrates limits to growth archetype.

---

### Example 2: Thermostat Control

```
const TargetTemp = 70
const HeatingRate = 5
const CoolingRate = 0.5

stock Temperature {
  initial: 60
  min: 0
  max: 100
  units: "°F"
}

flow Heating {
  from: source
  to: Temperature
  rate: Temperature < TargetTemp ? HeatingRate : 0
}

flow Cooling {
  from: Temperature
  to: sink
  rate: CoolingRate
}

graph TempControl {
  title: "Temperature Control"
  variables: Temperature
  type: line
  yAxisLabel: "°F"
}
```

**System behavior:** Temperature oscillates around target. Demonstrates goal-seeking with delay.

---

### Example 3: Inventory with Order Delays

```
const OrderDelay = 7
const ReorderPoint = 20
const OrderQuantity = 50

stock Inventory {
  initial: 100
  min: 0
  units: "units"
}

stock OnOrder {
  initial: 0
  min: 0
  units: "units"
}

flow Sales {
  from: Inventory
  to: sink
  rate: 5
}

flow Orders {
  from: source
  to: OnOrder
  rate: Inventory < ReorderPoint ? OrderQuantity : 0
}

flow Deliveries {
  from: OnOrder
  to: Inventory
  rate: DELAY(Orders, OrderDelay)
}

graph InventoryStatus {
  title: "Inventory Levels"
  variables: Inventory, OnOrder
  type: line
}
```

**System behavior:** Inventory depletes, triggers reorder at threshold, delivery delayed. Can cause oscillations.

---

### Example 4: SIR Epidemic Model

```
const TransmissionRate = 0.0005
const RecoveryRate = 0.1

stock Susceptible {
  initial: 990
  min: 0
  units: "people"
}

stock Infected {
  initial: 10
  min: 0
  units: "people"
}

stock Recovered {
  initial: 0
  min: 0
  units: "people"
}

flow Infections {
  from: Susceptible
  to: Infected
  rate: Susceptible * Infected * TransmissionRate
}

flow Recoveries {
  from: Infected
  to: Recovered
  rate: Infected * RecoveryRate
}

terminate {
  when: Infected < 1
}

graph EpidemicCurve {
  title: "SIR Epidemic Model"
  variables: Susceptible, Infected, Recovered
  type: line
}
```

**System behavior:** Classic epidemic curve - exponential growth, peak, then decline as susceptible population depletes.

---

### Example 5: Business with Seasonal Sales

```
const BaseSales = 100

lookup SeasonalMultiplier {
  [0, 1.0]
  [3, 1.2]
  [6, 1.5]
  [9, 1.3]
  [12, 1.0]
}

stock Revenue {
  initial: 0
  units: "dollars"
}

flow Sales {
  from: source
  to: Revenue
  rate: BaseSales * LOOKUP(TIME % 12, SeasonalMultiplier)
}

graph RevenueOverTime {
  title: "Seasonal Revenue Pattern"
  variables: Revenue
  type: area
  color: "#3b82f6"
}
```

**System behavior:** Revenue accumulates with seasonal variation repeating annually.

---

## Best Practices

### Naming
- Use PascalCase: `CustomerBase`, `MonthlyChurn`
- Be descriptive: `AverageWaitTime` not `AvgWT`
- Use domain terminology

### Initial Values
- Base on real data when available
- Use realistic proportions
- Set `min: 0` for stocks that can't go negative

### Rate Expressions
- Keep simple when possible
- Use constants for magic numbers
- Comment complex expressions
- Use `max(0, ...)` to prevent negative flows

### Model Structure
1. Define constants first
2. Define lookup tables next
3. Define stocks
4. Define flows
5. Add graphs
6. Add termination if needed

### Testing
- Start simple, add complexity gradually
- Verify each flow makes sense
- Check stock behaviors match expectations
- Use graphs to visualize dynamics

---

## Common Patterns

### Exponential Growth
```
rate: Stock * growth_rate
```

### Exponential Decay
```
rate: Stock * decay_rate
```

### Goal-Seeking
```
rate: (Goal - Actual) * adjustment_rate
```

### Constrained Flow
```
rate: min(Desired, Available)
```

### Conditional Flow
```
rate: Stock > Threshold ? FlowRate : 0
```

### Nonlinear Effect
```
rate: Stock * LOOKUP(Factor, EffectTable)
```

---

## System Archetypes

### Limits to Growth
```
// Reinforcing loop eventually hits balancing constraint
flow Growth {
  rate: Stock * growth_rate
}
flow Constraint {
  rate: Stock * LOOKUP(Stock / Capacity, LimitingEffect)
}
```

### Balancing Loop with Delay
```
// Goal-seeking with delayed response causes oscillation
stock Actual { initial: 50 }
stock Delayed { initial: 50 }

flow Adjustment {
  rate: (DELAY(Goal, delay_time) - Actual) * response_rate
}
```

### S-Shaped Growth (Logistic)
```
flow Growth {
  rate: Stock * growth_rate * (1 - Stock / Capacity)
}
```

---

## Using Generated DSL

1. Copy the generated DSL code
2. Visit https://systemsthinkingtool.com
3. Paste into left editor panel
4. View visual diagram (right top)
5. Run simulation (bottom controls)
6. Observe behavior in graph (right bottom)

The tool automatically:
- Parses DSL and validates syntax
- Generates visual stock-flow diagram
- Enables simulation controls
- Plots stock values over time
- Shows multiple graphs if defined

---

## Troubleshooting

**Model grows too fast:**
- Reduce rate constants
- Add balancing loops
- Check for missing constraints

**Stocks go negative:**
- Add `min: 0` to stock definition
- Use `max(0, expression)` in rates

**No visible dynamics:**
- Increase rate constants
- Check initial values
- Extend simulation time

**Oscillations too large:**
- Reduce response rates
- Add smoothing/delays
- Check for missing damping

---

## Additional Resources

- Live tool: https://systemsthinkingtool.com
- Repository: https://github.com/doodzik/systems-thinking-tool
- System Dynamics: MIT System Dynamics Group
- Classic book: "Thinking in Systems" by Donella Meadows