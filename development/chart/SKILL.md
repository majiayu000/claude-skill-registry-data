---
name: chart
description: Generate ASCII or SVG charts from data (bar, line, scatter, histogram, pie)
version: 0.1.0
execution-mode: advisory
argument-hint: "[--type bar|line|scatter|hist|pie] [--data FILE] [--title TITLE]"
category: dev-tools
status: candidate
---
# Chart

Generate visual charts from data as ASCII art (for terminal display) or SVG (for embedding in docs). Supports bar, line, scatter, histogram, and pie chart types using stdlib only.

## When to Use
- You have numeric data and need a quick visual representation
- You want to include a chart in a document, briefing, or presentation
- You need to compare distributions, trends, or proportions visually
- After running `[csv-analyze]` and want to visualize the findings

## Execution
1. Parse `$ARGUMENTS` for chart type, data source, and title
2. If `--data FILE` provided, load and parse the data file (CSV, JSON, TSV)
3. If no file, accept inline data from the conversation context
4. Auto-detect appropriate chart type if not specified (categorical=bar, time series=line, distribution=hist)
5. Normalize data ranges and compute axis labels
6. Generate ASCII chart for terminal output (default) or SVG if requested
7. Include summary statistics below the chart (min, max, mean for numeric axes)

## Output Format
```
Chart | <title>

<ASCII or SVG chart>

Stats: min=<val>  max=<val>  mean=<val>  points=<N>

Source: <filename or "inline data">
Next action: <recommendation>
```

## Skill Chains
| After this skill... | Consider... |
|--------------------|-------------|
| Chart reveals a trend | `[docgen]` to include in a report |
| Chart is for a pitch | `[pitch]` to build the narrative around it |
| Chart shows financial data | `[investor-update]` to draft stakeholder communication |
