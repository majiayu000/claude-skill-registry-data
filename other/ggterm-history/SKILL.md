---
name: ggterm-history
description: Search and retrieve plots from history. Use when the user asks about previous plots, wants to find a plot they made earlier, re-display a past visualization, or export a historical plot.
allowed-tools: Bash(bun:*), Read
---

# Plot History Management

Search, retrieve, and export plots from the persistent history.

## When to Use This Skill

Use this skill when the user:
- Asks about a plot they made before ("show me the scatter plot from yesterday")
- Wants to find a specific visualization ("find my sales chart")
- Needs to export a previous plot ("export that histogram to PNG")
- Asks what plots exist ("what plots have I made?")
- Wants to compare or reference earlier work

## IMPORTANT: Check History First

Before recreating a plot from scratch, ALWAYS check if it already exists in history:

```bash
bun packages/core/src/cli-plot.ts history
```

This saves time and ensures consistency with what the user previously created.

## CLI Commands

### List All Plots

```bash
bun packages/core/src/cli-plot.ts history
```

Output:
```
Plot History:

ID              Date        Description
─────────────────────────────────────────────────────────────────────────
2024-01-26-001  2024-01-26  Scatter plot of price vs sqft by region - "Housing"
2024-01-26-002  2024-01-26  Histogram of income - "Income Distribution"
2024-01-27-001  2024-01-27  Line chart of revenue vs date by product - "Sales"

Total: 3 plot(s)
```

### Search History

```bash
bun packages/core/src/cli-plot.ts history <search-term>
```

Searches across:
- Plot descriptions
- Data file names
- Geom types (scatter, histogram, line, etc.)

Examples:
```bash
bun packages/core/src/cli-plot.ts history scatter     # Find scatter plots
bun packages/core/src/cli-plot.ts history sales       # Find plots with "sales"
bun packages/core/src/cli-plot.ts history histogram   # Find histograms
bun packages/core/src/cli-plot.ts history iris.csv    # Find plots using iris.csv
```

### Re-render a Plot

```bash
bun packages/core/src/cli-plot.ts show <plot-id>
```

Displays the plot in the terminal exactly as it was originally created.

### Export a Plot

```bash
bun packages/core/src/cli-plot.ts export <plot-id> [output.html]
```

Creates an interactive HTML file with PNG/SVG download buttons.

## Natural Language → Commands

| User Request | Command |
|-------------|---------|
| "What plots have I made?" | `history` |
| "Show me my scatter plots" | `history scatter` |
| "Find the plot with sales data" | `history sales` |
| "Display plot 2024-01-26-001" | `show 2024-01-26-001` |
| "Show me yesterday's histogram" | `history histogram` → find by date → `show <id>` |
| "Export the iris plot" | `history iris` → `export <id> iris-plot.html` |
| "Re-export that last chart" | `history` → get latest → `export <id>` |

## Workflow Examples

### Example 1: "Show me the plot I made with the housing data"

```bash
# Step 1: Search for it
bun packages/core/src/cli-plot.ts history housing

# Output shows: 2024-01-26-001  Scatter plot of price vs sqft - "Housing Prices"

# Step 2: Display it
bun packages/core/src/cli-plot.ts show 2024-01-26-001
```

### Example 2: "Export my histogram to PNG"

```bash
# Step 1: Find histograms
bun packages/core/src/cli-plot.ts history histogram

# Output shows: 2024-01-26-002  Histogram of income - "Income Distribution"

# Step 2: Export to HTML (user can download PNG from browser)
bun packages/core/src/cli-plot.ts export 2024-01-26-002 income-histogram.html

# Step 3: Tell user to open in browser and click "Download PNG"
```

### Example 3: "What did I plot last week?"

```bash
# List all and filter by date visually
bun packages/core/src/cli-plot.ts history

# Look for entries with dates from last week in the output
```

## Plot ID Format

IDs follow the pattern: `YYYY-MM-DD-NNN`

- `YYYY-MM-DD` - Date the plot was created
- `NNN` - Sequence number for that day (001, 002, etc.)

Example: `2024-01-26-003` = Third plot created on January 26, 2024

## Provenance Information

Each stored plot includes:
- **timestamp**: When it was created
- **dataFile**: Path to the data file used
- **command**: The exact CLI command that created it
- **description**: Auto-generated summary of the plot
- **geomTypes**: List of geometries used (point, line, histogram, etc.)
- **aesthetics**: Mapped variables (x, y, color, etc.)

To see full provenance, read the plot file directly:
```bash
cat .ggterm/plots/2024-01-26-001.json
```

## Tips

1. **Be generous with search terms** - The search is case-insensitive and matches partial strings
2. **Check dates** - If user says "yesterday" or "last week", look at the Date column
3. **Multiple matches** - If search returns multiple plots, ask user to clarify or show the list
4. **Missing plots** - If nothing matches, the plot may not exist; offer to create it

$ARGUMENTS
