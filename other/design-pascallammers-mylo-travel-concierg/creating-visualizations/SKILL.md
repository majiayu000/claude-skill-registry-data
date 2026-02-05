---
name: creating-visualizations
description: Component skill for creating effective visualizations (terminal-based and image-based) in DataPeeker analysis sessions
---

# Creating Visualizations

## Purpose

This component skill guides creation of clear, effective visualizations for analytics documentation. Use it when:
- Presenting query results in a more visual format
- Need to reveal patterns that are hard to see in raw numbers
- Creating reports or documentation that will be read by stakeholders
- Documenting data workflows, lineage, or database schemas
- Referenced by process skills requiring data visualization

**Supports two approaches:**
- **Terminal-based** (plotext, sparklines, etc.) - For interactive analysis
- **Image-based** (Kroki: Mermaid, GraphViz, Vega-Lite) - For reports and complex diagrams

## Prerequisites

- Query results obtained and interpreted
- Understanding of patterns to highlight (use `interpreting-results` skill)
- Analysis documented in markdown files
- Clear communication goal for the visualization

## Visualization Creation Process

Create a TodoWrite checklist for the 4-phase visualization process:

```
Phase 1: Choose Visualization Type
Phase 2: Structure Data for Display
Phase 3: Create Visualization
Phase 4: Annotate with Context
```

Mark each phase as you complete it. Include visualizations in numbered markdown files alongside queries and interpretations.

---

## Phase 1: Choose Visualization Type

**Goal:** Select the right visualization format for your data and communication goal.

### Visualization Selection Decision Tree

Ask these questions in order:

**1. What type of data am I visualizing?**

- **Single summary statistic** → Callout box or highlighted metric
- **List of values** → Table or ranked list
- **Distribution across categories** → Bar chart (ASCII or markdown)
- **Time series** → Line chart (sparkline) or time table
- **Comparison between groups** → Side-by-side table or grouped bars
- **Part-to-whole relationship** → Percentage table or ASCII pie chart
- **Correlation or relationship** → Scatter (character plot) or correlation matrix

**2. What is my primary communication goal?**

- **Show exact values** → Table with clear formatting
- **Show relative magnitudes** → Bar chart or ranked list
- **Show trends over time** → Sparkline or time series table
- **Show distribution shape** → Histogram (ASCII)
- **Show ranking** → Ordered list or horizontal bars
- **Show proportions** → Percentage table with bars

**3. How many data points?**

- **1-5 values** → Callout boxes or simple list
- **6-20 values** → Table or bar chart
- **21-50 values** → Grouped table or histogram
- **50+ values** → Summary statistics + histogram, or top/bottom N

**4. Who is the audience?**

- **Technical analysts** → Full tables with precision
- **Business stakeholders** → Simplified visuals with key takeaways
- **Mixed audience** → Visual summary + detailed table

### Available Visualization Types

**DataPeeker supports two complementary approaches:**

#### Terminal-Based Formats (Primary for analysis):
1. **Markdown Tables** - Structured data with alignment
2. **ASCII Bar Charts** - Visual magnitude comparison (plotext, termgraph)
3. **Sparklines** - Compact trend indicators (sparklines library)
4. **ASCII Histograms** - Distribution visualization (plotext)
5. **Callout Boxes** - Highlighting key metrics
6. **Ranked Lists** - Ordered items with context
7. **Comparison Tables** - Side-by-side metrics
8. **Line Plots** - Time series (plotext, asciichartpy)

#### Image-Based Formats (For reports and complex diagrams):
1. **Mermaid** - Flowcharts, Gantt charts, workflows
2. **GraphViz** - Network graphs, data lineage, hierarchies
3. **Vega-Lite** - Statistical charts (bar, line, scatter)
4. **ERD/DBML** - Database schemas

**Choose based on:**
- What pattern you want to communicate
- Where the output will be viewed (terminal vs report)
- Complexity of the visualization needed

---

## Phase 2: Structure Data for Display

**Goal:** Organize and format data for effective visualization.

### Data Preparation Checklist

Before creating visualization:

**1. Sort appropriately:**
```markdown
For ranked data:
- Sort by the metric you want to emphasize (descending for "top N")
- Consider: Alphabetical only if order doesn't matter

For time series:
- Sort chronologically (oldest to newest, or newest first if recent matters)

For categorical:
- Sort by frequency, magnitude, or logical grouping
- Avoid: Random or database-default ordering
```

**2. Round to appropriate precision:**
```markdown
Examples:
- Revenue: Round to thousands or whole dollars (not $1,234.56789)
- Percentages: 1-2 decimal places (14.3%, not 14.285714%)
- Counts: Whole numbers only (1,234 not 1234.0)
- Ratios: 2-3 significant figures (2.4x not 2.3567x)

Rule: Show precision that matches the certainty of your data
```

**3. Add calculated columns:**
```markdown
Useful additions:
- Percentage of total
- Difference from average/baseline
- Rank or percentile
- Running totals or moving averages
- Year-over-year change
```

**4. Consider grouping:**
```markdown
For large datasets:
- Show Top N + "Other" row
- Group by logical categories
- Use ranges/buckets for continuous data
- Separate outliers from main distribution
```

**5. Format for readability:**
```markdown
Best practices:
- Add thousand separators (1,234 not 1234)
- Use consistent decimal places within columns
- Align numbers right, text left
- Include units in headers ($, %, units)
```

---

## Phase 3: Create Visualization

**Goal:** Build the actual visualization using appropriate format and tools.

### Two Visualization Approaches

DataPeeker supports two complementary visualization approaches:

#### 1. Terminal-Based Visualizations (Primary)

**Use for:**
- Interactive terminal/Jupyter notebook analysis
- Quick data exploration
- Markdown documentation that stays in terminal
- Fast iteration without external dependencies

**Available formats:**
1. **Markdown Tables** - Structured data with multiple columns, exact values
2. **ASCII Bar Charts** - Visual magnitude comparison, relative sizes
3. **Sparklines** - Compact trend indicators with Unicode characters
4. **ASCII Histograms** - Distribution visualization, shape and spread
5. **Callout Boxes** - Highlighting key metrics or insights
6. **Ranked Lists** - Top/bottom N items with narrative context
7. **Comparison Tables** - Side-by-side metrics across segments or time
8. **Line Plots** - Time series and trends

**→ See [terminal-formats.md](./terminal-formats.md) for implementation**

#### 2. Image-Based Visualizations (via Kroki)

**Use for:**
- Reports and presentations (embedded images)
- Complex diagrams (workflows, data lineage, relationships)
- Database schemas and architecture
- Documentation that needs to be viewed outside terminal
- High-quality charts for stakeholder communication

**Available formats:**
1. **Mermaid** - Flowcharts, Gantt charts, sequence diagrams
2. **GraphViz** - Network graphs, data lineage, hierarchies
3. **Vega-Lite** - Statistical charts (bar, line, scatter, histograms)
4. **D2** - Modern diagrams, architecture, data models
5. **ERD/DBML** - Database schemas and relationships

**→ See [image-formats.md](./image-formats.md) for implementation**

### Choosing Between Terminal and Image Formats

**Use Terminal formats when:**
- Working interactively in analysis session
- Output stays in markdown/terminal
- Quick iteration and exploration
- Simple charts and tables

**Use Image formats when:**
- Creating final reports or presentations
- Visualizing complex relationships (data lineage, workflows)
- Documenting database schemas
- Output needs to be embedded in documents/web
- Audience views outside terminal environment

**Can use both:**
- Terminal for exploration → Image for final report
- Tables (terminal) + Diagrams (image) in same document

### ⚠️ CRITICAL: Tool Usage Requirements

**MANDATORY:** All visualizations (bar charts, line plots, histograms, sparklines, scatter plots) **MUST** use established visualization tools. **NEVER create these manually.**

**✅ ALLOWED - Manual Creation:**
- Markdown tables with exact values
- Callout boxes and formatted text
- Ranked lists with exact numbers

**❌ PROHIBITED - Manual Creation:**
- Bar charts (no manual █ characters)
- Line plots or time series (no manual * or - characters)
- Histograms
- Sparklines (no manual ▁▂▃▄▅▆▇█ characters)
- Any visualization requiring scaling or positioning

### Implementation Details

**📄 For visualization implementations, use these guides:**

#### Terminal-Based Visualizations
**[terminal-formats.md](./terminal-formats.md)**

This document provides:
- **Mandatory tool usage principles** (read this first!)
- **Quick Start guide** with tool installation (plotext, asciichartpy, termgraph, sparklines)
- **Complete code examples** for each visualization type using proper tools
- **SQLite integration examples** for generating visualizations from query results

**The rule:** If it visualizes relative magnitudes, trends, or distributions → USE A TOOL. If it's exact numbers in a table → Manual creation is fine.

#### Image-Based Visualizations
**[image-formats.md](./image-formats.md)**

This document provides:
- **Kroki overview** - Unified API for generating diagrams from text
- **Quick Start guide** with Python examples and API usage
- **Format selection guide** - When to use Mermaid vs GraphViz vs Vega-Lite
- **Complete implementation guides** for each format in `formats/` directory:
  - [Mermaid](./formats/mermaid.md) - Flowcharts, Gantt, sequences
  - [GraphViz](./formats/graphviz.md) - Network graphs, data lineage
  - [Vega-Lite](./formats/vega-lite.md) - Statistical charts
- **DataPeeker integration examples** - Visualizing data workflows and schemas

---

## Phase 4: Annotate with Context

**Goal:** Add context and guidance so visualization is self-explanatory.

### Annotation Checklist

Every visualization should include:

**1. Title/Caption:**
```markdown
## [Clear, descriptive title that states what is being shown]

Example:
✓ Good: "Monthly Revenue by Product Category (Jan-Dec 2024)"
✗ Bad: "Revenue Chart"
```

**2. Data source and date:**
```markdown
**Data source:** analytics.db, orders table
**Time period:** Q4 2024 (Oct 1 - Dec 31)
**Last updated:** 2025-11-18
```

**3. Key takeaway (above or below visualization):**
```markdown
**Key Finding:** Electronics drove 42.5% of Q4 revenue despite representing
only 15% of order volume, indicating premium product performance.
```

**4. Units and scale:**
```markdown
- Include $ or % symbols
- Clarify if values are in thousands: ($000s)
- Note if values are indexed or normalized
- Specify timezone for timestamps
```

**5. Context for interpretation:**
```markdown
**Context notes:**
- Q4 includes Black Friday/Cyber Monday (Nov 24-27)
- New product line launched Oct 15, affecting Electronics category
- Shipping delays in December may have suppressed orders
```

**6. Limitations and caveats:**
```markdown
**Caveats:**
- Data excludes returns and cancellations
- International orders converted to USD at average quarterly exchange rate
- First week of October had incomplete data due to system migration
```

**7. What to look for:**
```markdown
**What to notice:**
- Electronics peak in November (holiday season)
- Clothing shows consistent decline (investigate seasonality)
- Sports category smallest but growing fastest (+45% QoQ)
```


## Visualization Best Practices

### DO:

1. **Choose format based on communication goal, not convenience**
   - Ask: "What do I want the reader to notice first?"
   - Match visualization to insight you're highlighting

2. **Make visualizations self-contained**
   - Reader should understand without reading entire document
   - Include title, units, source, key takeaway

3. **Use consistent formatting within analysis**
   - Same bar width for all bar charts
   - Same precision for similar metrics
   - Consistent color/symbol conventions (if using)

4. **Highlight what matters**
   - Use **bold** for most important values
   - Put key finding at top or bottom
   - Add 🔥, ⚠️, ✓ symbols sparingly for emphasis

5. **Test readability**
   - View in markdown preview (not just raw markdown)
   - Check alignment and spacing
   - Ensure visualization works in different font sizes

6. **Layer detail progressively**
   - Summary visualization first (bar chart, key metrics)
   - Detailed table second (full data)
   - Technical notes third (methodology, caveats)

7. **Combine formats when helpful**
   - Bar chart + exact values table
   - Sparkline + summary statistics
   - Visualization + narrative interpretation

### DON'T:

1. **Don't create visualizations for their own sake**
   - If a simple table is clearer, use the table
   - Visualization should reveal patterns, not obscure them

2. **Don't use excessive precision**
   - Revenue in dollars, not cents ($1,234 not $1,234.56)
   - Percentages to 1 decimal place (14.3% not 14.285714%)

3. **Don't hide important caveats**
   - Data quality issues must be visible
   - Exclusions and filters must be noted
   - Sample size and time period must be clear

4. **Don't use misleading scales**
   - Bar charts should start at zero (not truncated y-axis)
   - Be explicit if using non-zero baseline

5. **Don't over-format**
   - Too many symbols/colors creates visual noise
   - Keep it simple and professional

6. **Don't assume reader knows context**
   - Define abbreviations
   - Explain what metrics mean
   - Note if using non-standard calculations

7. **Don't forget the "so what?"**
   - Every visualization needs an interpretation
   - State implications, not just observations

---

## Common Visualization Patterns

### Pattern 1: Before/After Comparison

```markdown
## Impact of Pricing Change (Oct 15, 2024)

### Before Pricing Change (Oct 1-14)
- Average Order Value: **$145.67**
- Daily Orders: **234**
- Daily Revenue: **$34,087**

### After Pricing Change (Oct 15-31)
- Average Order Value: **$127.23** (↓ $18.44, -12.7%)
- Daily Orders: **289** (↑ 55, +23.5%)
- Daily Revenue: **$36,769** (↑ $2,682, +7.9%)

**Net effect:** Lower prices increased volume enough to grow total revenue.
```

### Pattern 2: Distribution Summary

**⚠️ Use plotext to create histograms - DO NOT create manually**

Show distribution with summary statistics:

```python
import plotext as plt
import statistics

# Customer LTV values from query
ltv_values = [423, 687, 892, 2145, ...]  # Your data

plt.hist(ltv_values, bins=7)
plt.title('Customer Lifetime Value Distribution')
plt.xlabel('Customer LTV ($)')
plt.ylabel('Number of Customers')
plt.show()

# Show summary statistics
print(f"\nSummary Statistics:")
print(f"Median LTV: ${statistics.median(ltv_values):,.0f}")
print(f"Mean LTV: ${statistics.mean(ltv_values):,.0f}")
print(f"75th percentile: ${statistics.quantiles(ltv_values, n=4)[2]:,.0f}")
```

**See terminal-formats.md Format 4 for complete histogram examples.**

### Pattern 3: Segmentation Analysis

**✅ Tables are fine for exact values, use plotext/termgraph for visual breakdown**

```markdown
## Customer Segmentation by Purchase Behavior

| Segment         | Customers | Avg Orders | Avg LTV | % of Revenue | Strategy      |
|:----------------|----------:|-----------:|--------:|-------------:|:--------------|
| **Champions**   |       234 |       18.3 |  $2,145 |        18.2% | VIP treatment |
| **Loyal**       |     1,456 |        8.7 |    $892 |        47.3% | Retain & grow |
| **Potential**   |     3,678 |        2.4 |    $287 |        38.5% | Nurture       |
| **At Risk**     |       892 |        1.2 |    $156 |         5.1% | Win-back      |
| **Lost**        |     2,134 |        1.0 |     $87 |         6.8% | Low priority  |

**Key insight:** Top two segments (Champions + Loyal) are only 18% of customer
base but generate 66% of revenue. These 1,690 customers should receive majority
of retention investment.
```

**For visual breakdown, use plotext:**
```python
import plotext as plt

segments = ['Champions', 'Loyal', 'Potential', 'At Risk', 'Lost']
revenue = [501030, 1299552, 1055586, 139152, 185658]

plt.simple_bar(segments, revenue, title='Revenue by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Revenue ($)')
plt.show()
```

**See terminal-formats.md Format 2 for complete bar chart examples.**

### Pattern 4: Time Series with Annotations

**⚠️ Use plotext or asciichartpy - DO NOT create manually**

```python
import plotext as plt

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
revenue = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
           1.5, 1.6, 1.7, 1.7, 1.9, 2.0]  # Revenue in millions

plt.plot(months, revenue)
plt.title('Monthly Revenue Trend with Key Events')
plt.xlabel('Month')
plt.ylabel('Revenue ($M)')
plt.show()

print("\nKey Events:")
print("- Oct 1: Q4 begins, seasonal uptick expected")
print("- Oct 15: Pricing change (-10% on popular items)")
print("- Nov 1: New product line launched (premium segment)")
print("- Nov 24-27: Black Friday/Cyber Monday surge")
print("\nAnalysis: Revenue growth accelerated after new product launch (Nov),")
print("suggesting demand for premium options. Pricing change impact unclear due to")
print("seasonal overlap.")
```

**See terminal-formats.md Format 8 for complete line plot examples.**

### Pattern 5: Funnel Analysis

**✅ Tables for exact values, use plotext for visualization**

```markdown
## Purchase Funnel Conversion Rates

| Step              | Count   | Conversion | Drop-off | Notes |
|:------------------|--------:|-----------:|---------:|:------|
| 1. Site Visitors  | 100,000 |     100.0% |        — |       |
| 2. Product Viewers|  45,000 |      45.0% |    55.0% | High bounce rate |
| 3. Add to Cart    |  12,000 |      26.7% |    73.3% |       |
| 4. Begin Checkout |   8,500 |      70.8% |    29.2% | Cart abandonment |
| 5. Complete       |   3,200 |      37.6% |    62.4% | Payment issues? |

**Overall Conversion:** 3.2%

**Problem areas:**
1. **Bounce rate (55%):** Half of visitors leave without viewing products
   - Action: Improve landing page, clearer value proposition

2. **Cart abandonment (29%):** Losing 3,500 potential customers at checkout
   - Action: Simplify checkout, add progress indicator

3. **Checkout failure (62%):** Massive drop-off at payment
   - Action: URGENT — investigate payment gateway, error messages

**Quick win:** Fixing checkout issues could 2.6x conversion (3.2% → 8.4%)
```

**For funnel visualization, use plotext:**
```python
import plotext as plt

steps = ['Visitors', 'Viewers', 'Cart', 'Checkout', 'Purchase']
counts = [100000, 45000, 12000, 8500, 3200]

plt.simple_bar(steps, counts, title='Purchase Funnel')
plt.xlabel('Funnel Step')
plt.ylabel('Count')
plt.show()
```

**See terminal-formats.md Format 2 for complete bar chart examples.**

---

## Integration with Process Skills

Process skills reference this component skill with:

```markdown
Use the `creating-visualizations` component skill to present query results
visually, making patterns and insights more accessible to stakeholders.
```

When creating visualizations during analysis:
1. Choose format based on communication goal (Phase 1)
2. Structure data for clarity (Phase 2)
3. Build visualization with appropriate text format (Phase 3)
4. Annotate with context and interpretation (Phase 4)

This ensures analysis outputs are not just technically correct but also
effectively communicated and actionable.

---

## When to Visualize

**Visualize when:**
- Pattern is easier to see visually than in raw numbers
- Presenting to stakeholders who need quick understanding
- Comparing multiple segments, time periods, or metrics
- Distribution shape matters (histograms)
- Trend direction matters (sparklines, time series)

**Use tables when:**
- Exact values are critical
- Reader needs to reference specific numbers
- Data is already structured and scannable
- Audience is technical and prefers precision

**Use both when:**
- Visualization reveals pattern, table provides detail
- Different audiences (executive summary + appendix)
- Building progressive disclosure (overview → detail)

---

## Quality Checklist

Before finalizing any visualization, verify:

- [ ] Visualization has clear, descriptive title
- [ ] Units are labeled ($ , %, etc.)
- [ ] Data source and time period documented
- [ ] Key takeaway stated explicitly
- [ ] Appropriate precision (not over-rounded or over-precise)
- [ ] Scale is appropriate (bars from zero, etc.)
- [ ] Annotations explain what to notice
- [ ] Caveats and limitations noted
- [ ] Visualization renders correctly in markdown preview
- [ ] Numbers match source query results
- [ ] Format matches communication goal
- [ ] Audience can understand without additional context

**If any checklist item fails, revise before including in analysis.**
