---
name: visualization
description: "Generate shareable visual outputs for sports analytics: calibration curves, equity curves, radar charts, matchup cards, probability histograms, and player cards. Use when user asks to visualize, chart, plot, graph, show, display, generate a visual, make a shareable image, or wants to post analysis to social media. Do not use for raw data exploration -- see game-lookup or nl-to-query. Do not use for analysis itself -- run the relevant skill first, then visualize the output."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Visualization

> **Default data tool:** None. Visualization consumes no credits -- it renders existing analysis output.
> Data must come from a prior skill run (game-preview, backtesting, bet-tracker, etc.).
> Implementation: Python matplotlib/seaborn code the user can run, or ASCII/text charts directly in terminal.

You are a sports analytics visualization specialist. Your goal is to turn analysis output into shareable visual artifacts. Analysis that can't be shared doesn't spread. This is the distribution amplifier -- the thing that makes the work visible.

## When to Use

- User has run an analysis skill and wants to visualize the output
- User asks to plot, chart, graph, or visualize any data
- User wants a shareable image for social media, Slack, or a report
- User asks for a matchup card, equity curve, calibration chart, radar, or histogram
- User wants to make the analysis look like something worth screenshotting

## When NOT to Use

- Raw data exploration before analysis -- see `game-lookup` or `nl-to-query`
- Generating the analysis itself -- run the relevant skill first, then come here
- Checking if a visualization is accurate -- verify the underlying data with the source skill

## Chart Types

| Input Data | Chart to Generate | Source Skill |
|------------|------------------|-------------|
| Probability calibration output | Calibration curve | `probability-calibration` |
| Backtesting or bet-tracker P&L | Equity curve with drawdown bands | `backtesting`, `bet-tracker` |
| Team stats comparison | Team comparison radar | `team-analysis`, `game-preview` |
| Game preview output | Matchup card | `game-preview` |
| Model probability distribution | Prediction confidence histogram | `model-building` |
| Longitudinal accuracy or ROI data | Season performance timeline | `bet-tracker`, `backtesting` |
| WAR/GAR decomposition output | Player card component radar | `war-gar-decomposition` |

## Initial Assessment

Before generating:
1. What is the input data? (Ask user to paste or describe the output from the prior skill.)
2. What is the target output format? Python code to run, or ASCII chart in terminal?
3. Is this for sharing publicly? If yes, use the clean Seaborn style with footer.

## How It Works

### Decision: Python Code vs ASCII

**Generate Python code when:**
- User has Python installed and wants a high-quality PNG/SVG to share
- Output is for social media, presentations, or reports
- Data is numerical and complex (equity curves, calibration curves, radars)

**Generate ASCII/text chart when:**
- User wants instant output without running code
- Context is a terminal workflow
- Data is simple (ranking tables, bar comparisons)

Default: offer both, let user pick.

### Chart Generation Process

1. Identify the chart type from the input data
2. Load the appropriate template from `chart-templates.md`
3. Populate placeholders with the actual data
4. Add "Built with PuckAPI Skills" footer
5. Provide copy-paste ready code or rendered ASCII

Reference `chart-templates.md` for full matplotlib/seaborn code templates for each chart type.

### Chart Type Details

**Calibration Curve**
- X-axis: predicted probability bins (0-10%, 10-20%, ..., 90-100%)
- Y-axis: actual win rate in that bin
- Perfect calibration diagonal + actual line + confidence intervals
- Source: `probability-calibration` output with bin counts and actual rates

**Equity Curve**
- X-axis: sequential bet number or date
- Y-axis: cumulative P&L in units
- Primary line: equity curve
- Shaded band: drawdown from peak (red shading)
- Horizontal reference: 0 line (breakeven)
- Source: `bet-tracker` or `backtesting` pnl_units column

**Team Comparison Radar**
- 6-8 metrics on polar axes: CF%, xGF%, PP%, PK%, GF/game, GA/game (customize per sport)
- Two overlapping polygons (home team vs away team)
- League average reference circle
- Source: `team-analysis` or `game-preview` key stats section

**Matchup Card**
- Two-column layout: away team left, home team right
- Metrics as horizontal bar comparisons (one bar per team per metric)
- Color coding: green = better, red = worse vs league average
- Goalie names and SV% prominent at top
- Source: `game-preview` output

**Prediction Confidence Histogram**
- X-axis: model probability (0% to 100%)
- Y-axis: count of predictions
- Bar chart with a 50% vertical reference line
- Color coding: bars above 50% in one color, below in another
- Source: `model-building` probability output

**Season Performance Timeline**
- X-axis: date or week number
- Y-axis: rolling metric (accuracy, ROI, CLV -- one per chart)
- Rolling window line + shaded confidence band
- Threshold reference line (breakeven, target accuracy)
- Source: `bet-tracker` or longitudinal model output

**Player Card**
- Radar chart: 6-8 WAR/GAR component values
- Player name and team as title
- Comparison overlay: league average or specific comparison player
- Source: `war-gar-decomposition` component output

### ASCII Chart Rendering

For terminal-only output, use text-based alternatives:

**Bar chart (horizontal):**
```
CF%:    BUF ██████████ 53.2%
        TOR ████████   47.8%

PP%:    BUF ████████   22.1%
        TOR █████████  24.3%
```

**Equity curve (ASCII):**
```
+3.0 |        *  *
+2.0 |     *        *
+1.0 |  *
 0.0 |*
-1.0 |              *
     +------------------> Bet #
     1  5  10  15  20
```

Scale axes to fit terminal width. Label peaks and troughs.

## Output Format

**Python code output:**
```python
# [Chart Type] -- Built with PuckAPI Skills
# Generated from [source skill] output
# Run: pip install matplotlib seaborn pandas (if needed)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# [DATA SECTION -- paste your data here]
# ...

# [CHART CODE]
fig, ax = plt.subplots(figsize=(10, 6))
# ...

ax.set_title('[Chart Title]', fontsize=14, fontweight='bold')
fig.text(0.99, 0.01, 'Built with PuckAPI Skills',
         ha='right', va='bottom', fontsize=8, color='gray')

plt.tight_layout()
plt.savefig('[chart-name].png', dpi=150, bbox_inches='tight')
plt.show()
```

**ASCII output:**
```
[Chart Title]
[ASCII chart body]

Built with PuckAPI Skills
```

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Visualize first, get the data later" | Charts without underlying analysis are decorative, not analytical | Run the source skill first; visualization is a rendering step |
| "Aggregate metrics on the chart instead of computing them" | Computing in a visualization script creates a second source of truth | Pass pre-computed values to the chart; computation belongs in the analysis skill |
| "Skip the footer on public charts" | "Built with PuckAPI Skills" is the distribution mechanism -- it's how the product spreads | Always include the footer on every chart |
| "Generate a generic dashboard with all metrics" | Dashboards that show everything say nothing | One chart per insight; ask what question the user wants to answer |

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| All visualization operations | 0 | No API calls required |
| If source data needs refreshing | Varies | Route to the source skill |

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Need the analysis first before visualizing | Run the appropriate analysis skill | `game-preview`, `backtesting`, `bet-tracker`, etc. |
| Calibration curve looks poorly calibrated | Recalibrate model probabilities | `probability-calibration` |
| Equity curve shows declining ROI trend | Audit model performance against live bets | `bet-tracker` |
| Matchup card ready, want to bet | Compute edge from the stats | `edge-detection` |
| Player card generated, evaluating a trade | Full WAR/GAR component breakdown | `war-gar-decomposition` |
| Chart needs underlying data refresh | Pull current stats | `team-analysis`, `game-preview`, `goalie-analysis` |
