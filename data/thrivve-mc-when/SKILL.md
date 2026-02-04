---
name: thrivve-mc-when
description: Thrivve Partners Monte Carlo simulation to forecast completion date based on remaining work and historical throughput. Use when the user asks "when will I complete [N] stories/tasks" with historical daily throughput data. Requires at least 10 days of throughput history, a count of remaining items, and optional confidence level (default 85%).
---

# Thrivve Partners Monte Carlo 'When' Forecasting

Forecast when a specific number of stories or tasks will be completed using Monte Carlo simulation based on historical throughput data.

## When to Use

Use this skill when the user provides:
1. Historical throughput data (daily counts for at least 10 days)
2. Number of stories/tasks remaining to complete
3. A desired confidence level (optional, defaults to 85%)
4. A start date (optional, defaults to today)

Common trigger patterns:
- "In the last X days, the throughput has been [counts] - when will I complete [N] stories with [confidence]% confidence?"
- "Based on throughput of [counts], when will we finish [N] stories if we start [date / 'today']?"
- "Run Monte Carlo simulation for [counts] to complete [N] stories"
- "I have [N] stories left, when will I be done?"

## Quick Start

Execute the Monte Carlo simulation script:

```bash
python scripts/thrivve-mc-when.py "<comma-separated-throughput>" <stories-remaining> <confidence-level> "<start-date>"
```

Example:
```bash
python scripts/thrivve-mc-when.py "3,5,4,2,6,4,5,3,7,4,5,6,3,4,5" 100 85 "2025-10-27"
```

## Input Requirements

1. **Throughput data**: Minimum 10 days of daily completion counts
   - Format: Comma-separated integers (e.g., "3,5,4,2,6,4,5,3,7,4")
   - More data = better predictions (15-30 days recommended)

2. **Stories remaining**: Integer count of items to complete
   - Must be greater than 0
   - Typical range: 10-500 (larger numbers may take longer)

3. **Confidence level**: Percentage between 0-99 (default: 85)
   - 25%: Optimistic outcome (earlier date, lower certainty)
   - 50%: Median outcome (equal chance of earlier or later)
   - 70%: Balanced outcome
   - 85%: Conservative (commonly used in agile forecasting)
   - 95%: Very conservative (high certainty, later date)
   - 99%: Maximum practical confidence (extremely conservative)
   - Note: 100% confidence is not possible in probabilistic forecasting
   
4. **Start date**: A date in any common format (default: today)
   - Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, "Month DD, YYYY", etc. 

## Output Format

The script provides:
- **Primary answer**: Completion date at specified confidence level
- **Percentile forecasts**: P25, P50, P70, P85, P95, P99 (dates)
- **Statistical summary**: Mean, min, max dates across all simulations
- **Days analysis**: Days required at different confidence levels
- **Throughput analysis**: Statistics about historical data
- **Process variation check**: Assessment of data stability for forecasting
- **JSON output**: Structured data for further processing

## Process Variation Checking

The skill automatically validates whether your throughput data exhibits stable, predictable variation suitable for forecasting using **XMR (Individual and Moving Range) control charts** from Statistical Process Control.

### When It Runs

- **20+ data points**: Full variation check runs, calculating control limits (UNPL, LNPL, URL)
- **10-19 data points**: Simulation runs, but shows info message that variation cannot be verified
- **< 10 data points**: Simulation cannot run (insufficient data)

### What It Checks

1. **Individual Values (UNPL/LNPL)**: Identifies unusually high or low throughput days
2. **Moving Ranges (URL)**: Detects unstable day-to-day variation
3. **Process Stability**: Determines if historical data represents predictable future behavior

### Understanding the Messages

**✓ Process Stability Confirmed** (Green Light)
- All throughput values within natural process limits
- Data is suitable for forecasting
- Past patterns reliably predict future performance

**ℹ️ Variation Check Skipped** (Informational)
- Less than 20 data points provided
- Simulation runs but process stability cannot be verified
- Consider gathering more data for validation

**⚠️ Variation Warning** (Caution Required)
- Outliers detected exceeding control limits
- Displays specific outlier values and calculated limits
- Forecast reliability may be compromised
- **Recommendation**: Investigate outliers before trusting forecast
  - Are they one-time events (holiday, outage, reorganization)?
  - Do they represent a changed process (new workflow, team size)?
  - Should they be excluded from forecasting data?

### Why It Matters

Monte Carlo simulation assumes your historical data represents future behavior. **Outliers violate this assumption**:
- May inflate variability, making forecasts unnecessarily pessimistic
- May skew averages, distorting expected completion times
- Signal process instability, making predictions unreliable

As documented in ProKanban research: "If there are values outside of LNPL or UNPL lines, the system is objectively unstable therefore it shouldn't be used for forecasting."

### What to Do About Outliers

1. **Investigate**: Understand why the outlier occurred
2. **Classify**: One-time event or permanent process change?
3. **Decide**:
   - Exclude if non-recurring (e.g., holiday shutdown)
   - Keep if representative of new normal (e.g., increased team capacity)
4. **Re-run**: Update forecast with adjusted data

For detailed statistical explanation, see `references/methodology.md`.

## Workflow

1. Parse user's throughput data from their message
2. Extract stories remaining and confidence level
3. Run the Monte Carlo script with parsed parameters
4. Present results in clear, actionable format
5. Explain what the confidence level means in context

## Interpreting Results

- **At X% confidence**: "There's an X% chance you'll be done ON OR BEFORE this date" (uses the percentile: X)
- **P50 (median)**: Half of simulations finished earlier, half later
- **P85**: 85% of simulations finished on or before this date
- **P95**: 95% of simulations finished on or before this date
- **Range**: Shows fastest and slowest completion from all simulations

**Example**: At 85% confidence, you'll complete the work on or before December 15th (P85), meaning there's an 85% chance of finishing on or before that date (and only a 15% chance it will take longer).

## Advanced Usage

Optional parameters:
- `num_simulations`: Number of Monte Carlo runs (default: 10,000)
  - Higher values increase accuracy but take longer
  - 10,000 is typically sufficient for reliable results

## Methodology

For detailed explanation of Monte Carlo simulation methodology, assumptions, and limitations, see `references/methodology.md`.

Key points:
- Uses random sampling from historical throughput
- Runs thousands of simulations to build probability distribution
- Assumes past patterns continue into the future
- Does not account for trends or changing conditions

## Example Interaction

User: "In the last 15 days, the throughput has been 3,5,4,2,6,4,5,3,7,4,5,6,3,4,5 - when will I complete 100 stories with 85% confidence, if I start today?"

Response steps:
1. Parse throughput: [3,5,4,2,6,4,5,3,7,4,5,6,3,4,5]
2. Parse stories remaining: 100
3. Parse confidence: 85%
4. Parse start date: today (2025-10-27)
5. Run simulation
6. Present results: "Given your start date of today (October 27, 2025), at 85% confidence you will complete 100 stories on or before November 19, 2025 (there's only a 15% chance it will take longer)"
7. Provide percentile context and explain the forecast
