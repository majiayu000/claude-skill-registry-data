---
name: pine-script-generator
description: Generate and update TradingView Pine Script code for visualizing options positions. Use when creating or modifying Pine scripts for options trading visualization.
allowed-tools: Read, Write, Edit, Bash(python:*), Grep, Glob
---

# Pine Script Generator

This skill generates TradingView Pine Script code to visualize options positions with color-coded lines showing strikes, expirations, and strategy types.

## Instructions

When working with Pine scripts:

1. **Understand the options data**
   - Parse portfolio CSV to extract options positions
   - Identify option types (call/put)
   - Determine position direction (long/short)
   - Extract strikes and expiration dates
   - Detect strategies (synthetic, spreads, etc.)

2. **Generate Pine Script v5 code**
   - Use proper Pine Script v5 syntax
   - Create horizontal lines for each strike price
   - Color-code by option type and strategy:
     - Long calls: Green
     - Short calls: Red
     - Long puts: Blue
     - Short puts: Orange
     - Synthetic positions: Purple
   - Add labels with expiration dates

3. **Include position details in labels**
   - Strike price
   - Expiration date (formatted: YYYY-MM-DD)
   - Quantity
   - Option type and direction

4. **Handle strategy detection**
   - Synthetic long: Long stock + Long put
   - Synthetic short: Short stock + Short call
   - Covered call: Long stock + Short call
   - Protective put: Long stock + Long put
   - Spreads: Multiple options same expiration

## Pine Script Template Structure

```pine
//@version=5
indicator("Options Positions", overlay=true)

// Option position definitions
// Generated from portfolio CSV

// Long Calls (Green)
line.new(x1=bar_index[100], y1=STRIKE, x2=bar_index, y2=STRIKE,
         color=color.green, width=2)
label.new(bar_index, STRIKE, "CALL EXP", color=color.green)

// Short Calls (Red)
line.new(x1=bar_index[100], y1=STRIKE, x2=bar_index, y2=STRIKE,
         color=color.red, width=2)
label.new(bar_index, STRIKE, "CALL EXP", color=color.red)

// Long Puts (Blue)
line.new(x1=bar_index[100], y1=STRIKE, x2=bar_index, y2=STRIKE,
         color=color.blue, width=2)
label.new(bar_index, STRIKE, "PUT EXP", color=color.blue)

// Short Puts (Orange)
line.new(x1=bar_index[100], y1=STRIKE, x2=bar_index, y2=STRIKE,
         color=color.orange, width=2)
label.new(bar_index, STRIKE, "PUT EXP", color=color.orange)
```

## Key Files

- `scripts/csv_to_options_tasty.py` - Main Pine script generator
- `src/options_list.py` - Options position analyzer
- `src/parse_utils.py` - CSV parsing utilities

## Common Tasks

### Generate Pine Script from CSV
```bash
PYTHONPATH=src python scripts/csv_to_options_tasty.py
```

### Update existing Pine Script
1. Read current Pine script
2. Parse new CSV data
3. Generate new position lines
4. Replace old position definitions
5. Preserve script header and settings

### Add new strategy visualization
1. Detect the strategy in options data
2. Choose appropriate color scheme
3. Add line and label generation code
4. Document the strategy in comments

## Output Guidelines

When generating Pine scripts:
- Use Pine Script v5 syntax (`//@version=5`)
- Set `overlay=true` to display on price chart
- Use clear, consistent color coding
- Include expiration dates in labels
- Group positions by strategy type in comments
- Keep code readable with proper spacing

## Example Usage

When asked to "Generate a Pine script for my options positions":

1. Locate the latest portfolio CSV in `data/`
2. Parse options positions using `options_list.py`
3. Group by ticker (create separate scripts or use inputs)
4. Generate line and label code for each position
5. Color-code by type and strategy
6. Output the complete Pine script
7. Provide instructions for loading into TradingView

## TradingView Integration

To use the generated script:
1. Open TradingView chart for the ticker
2. Click Pine Editor (bottom panel)
3. Paste the generated script
4. Click "Add to Chart"
5. Positions will appear as colored lines with labels
