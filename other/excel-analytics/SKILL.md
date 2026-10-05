---
name: excel-analytics
description: Use when analyzing Xiaohongshu data with Excel, creating spreadsheets for performance tracking, building data dashboards, conducting manual analysis, or learning spreadsheet skills for social media analytics
---

# Excel Analytics (Excel数据分析)

## Overview

Excel analytics is the systematic use of spreadsheet software to organize, analyze, visualize, and report on Xiaohongshu performance data, enabling custom analysis, flexible reporting, and data-driven insights without requiring specialized analytics tools.

## When to Use

**Use when**:
- Building custom tracking spreadsheets for Xiaohongshu data
- Analyzing exported data from platform analytics
- Creating personalized dashboards and reports
- Conducting custom calculations and metrics
- Visualizing performance trends and patterns
- Learning data analysis fundamentals
- Comparing multiple time periods or content types
- Creating executive summaries for stakeholders

**Do NOT use when**:
- Real-time monitoring needed (use platform analytics)
- Complex statistical analysis required (use specialized tools)
- Automated reporting at scale (use BI tools)
- Simple quick checks (use platform native analytics)

## Core Pattern

**Before** (manual, scattered, inefficient):
```
❌ "Data scattered across screenshots and exports"
❌ "Manual calculator for engagement rates"
❌ "No visual trends, just numbers in cells"
❌ "Recreating same reports from scratch every week"
```

**After** (organized, automated, insightful):
```
✅ "All data in one structured master spreadsheet"
✅ "Automatic calculations update when data changes"
✅ "Interactive charts show trends at glance"
✅ "Reusable dashboard template saves hours weekly"
```

**Excel Analytics Workflow**:
1. **Import** - Bring data from Xiaohongshu into Excel
2. **Clean** - Structure and format data properly
3. **Calculate** - Create metrics and KPIs with formulas
4. **Visualize** - Build charts and dashboards
5. **Analyze** - Extract insights and identify patterns
6. **Report** - Summarize findings for decision-making

## Quick Reference

| Excel Feature | Use Case | Complexity | Time Saved |
|---------------|----------|------------|-------------|
| **Pivot Tables** | Summarize large datasets | Medium | 2-3 hours/week |
| **VLOOKUP/XLOOKUP** | Match data across sheets | Medium | 1-2 hours/week |
| **Charts** | Visualize trends | Simple | 1 hour/week |
| **Conditional Formatting** | Highlight insights | Simple | 30 min/week |
| **Formulas** | Calculate metrics | Medium | 2-3 hours/week |
| **Macros** | Automate repetitive tasks | Advanced | 5+ hours/week |

## Implementation

### Step 1: Set Up Master Spreadsheet

**Spreadsheet Architecture**:
```

Workbook Structure (Separate Sheets/Tabs):

Sheet 1: README
- Purpose of spreadsheet
- How to use guide
- Definitions of metrics
- Contact for questions

Sheet 2: Raw Data Import
- Direct export from Xiaohongshu
- Date stamps for each import
- Raw, unmanipulated data
- Historical archive

Sheet 3: Content Performance Log
- One row per post
- Columns: Date, Content Type, Topic, Reach, Impressions, Likes, Comments, Shares, Saves, Engagement Rate
- Ongoing manual or automated entry

Sheet 4: Follower Growth Tracker
- Daily/weekly follower counts
- Growth rate calculations
- Follower acquisition sources
- Churn tracking

Sheet 5: Key Metrics Dashboard
- Executive summary
- Top-level KPIs
- Traffic light indicators (Green/Yellow/Red)
- Trend visualizations

Sheet 6: Content Analysis
- Performance by content type
- Performance by topic
- Top/bottom performing posts
- A/B test results

Sheet 7: Time Analysis
- Performance by day of week
- Performance by time of day
- Seasonal patterns
- Best posting times

Sheet 8: Competitor Tracking
- Competitor metrics
- Comparative analysis
- Market share
- Benchmarking

Sheet 9: Goals and Targets
- Target metrics by period
- Progress vs goals
- Gap analysis
- Forecasting

Sheet 10: Charts and Visualizations
- Trend charts
- Comparison charts
- Distribution charts
- Custom dashboards
```

**Data Dictionary (Column Definitions)**:
```

Essential Columns for Content Log:

A: Date (YYYY-MM-DD format)
B: Content_ID (Unique identifier)
C: Content_Type (Post, Video, Story, Live)
D: Topic (Primary theme/category)
E: Title (Post title or description)
F: Publish_Time (HH:MM format)
G: Day_of_Week (Monday-Sunday)
H: Reach (Unique users who saw content)
I: Impressions (Total displays)
J: Likes (❤️ reactions)
K: Comments (💬 responses)
L: Shares (📤 forwards)
M: Saves (📑 bookmarks)
N: Profile_Visits (👁️ profile clicks)
O: Follows_Gained (📈 new followers from post)
P: Engagement_Rate (Calculated)
Q: CTR (Click-through rate if applicable)
R: Conversion_Signups (Email, purchase, etc.)
S: Cost (If paid promotion)
T: Notes (Campaign context, etc.)

Optional Advanced Columns:
U: Hashtag_1, Hashtag_2, Hashtag_3
V: Product_Mentioned
W: Promo_Code_Used
X: A/B_Test_Variant
Y: Season (Spring/Summer/Fall/Winter)
Z: Campaign_Name
```

### Step 2: Import and Clean Data

**Data Import Methods**:
```

Method 1: Manual Entry
Best for: Small accounts, <50 posts/week
Process:
- Create template with required columns
- Manual entry from Xiaohongshu analytics
- Time required: 30-60 minutes/week

Pros: Complete control, no technical skill needed
Cons: Time-consuming, human error risk

Method 2: Export and Import
Best for: Medium accounts, 50-200 posts/week
Process:
- Export from Xiaohongshu Pro analytics
- Download CSV file
- Import into Excel
- Map columns to your structure

Steps:
1. Xiaohongshu Pro → Analytics → Content Performance
2. Select date range
3. Export as CSV
4. Excel → Data → From Text/CSV
5. Select file and import
6. Transform data to match your structure

Pros: Faster, less error-prone
Cons: Requires export capability, some cleanup needed

Method 3: API Integration (Advanced)
Best for: Large accounts, 200+ posts/week
Process:
- Use Xiaohongshu API (if available)
- Connect Excel to API (Power Query)
- Automated data refresh
- Real-time or scheduled updates

Pros: Automated, real-time, scalable
Cons: Technical setup, may require developer

Data Cleaning Checklist:
✅ Remove duplicate entries
✅ Fix date formats (consistent YYYY-MM-DD)
✅ Handle missing values (0 or NA)
✅ Remove special characters from text
✅ Standardize text casing (proper or upper)
✅ Verify data accuracy (spot check)
✅ Create backup before manipulation
```

### Step 3: Create Calculated Metrics

**Essential Excel Formulas**:
```

Engagement Rate Formula:
```
=IF(H2>0, (J2+K2+L2+M2)/H2, 0)
```
Where H=Reach, J=Likes, K=Comments, L=Shares, M=Saves

Follower Growth Rate Formula:
```
=(O2/SUM($O$1:O2))*100
```
Where O=Follows Gained, calculates cumulative growth rate

Week-over-Week Growth Formula:
```
=(SUM(H2:H8)-SUM(H9:H15))/SUM(H9:H15)
```
Compares this week to last week

Moving Average Formula (7-day):
```
=AVERAGE(J2:J8)
```
Smooths daily fluctuations

Percentage Change Formula:
```
=(J2-J1)/J1
```
Shows change from previous period

Conditional Formatting Rules:
Highlight top performers:
- Engagement rate > 10%: Green
- Engagement rate 5-10%: Yellow
- Engagement rate < 5%: Red

Highlight outliers:
- Values > 2x standard deviation: Bold
- Values = 0: Gray text

Identify best performing content type:
```
=MAXIFS(P:P, C:C, "Video")
```
Returns max engagement rate for Video content

Calculate content type averages:
```
=AVERAGEIF(C:C, "Video", P:P)
```
Average engagement rate for Video posts
```

Advanced Formulas (Pivot Tables):
Create dynamic summaries:
- Total engagement by content type
- Average reach by topic
- Best posting times by day
- Monthly performance comparisons
- Top 10 posts by engagement

Pivot Table Steps:
1. Select data range (including headers)
2. Insert → Pivot Table
3. Choose rows (e.g., Content_Type)
4. Choose values (e.g., Average of Engagement_Rate)
5. Add filters (e.g., Date range)
6. Format and style pivot table
7. Refresh when data updates
```

### Step 4: Build Visualizations

**Chart Creation Guide**:
```

Chart Type Selection:

Line Chart (Trend Analysis)
Best for: Metrics over time
Data: Date on X-axis, Metric on Y-axis
Examples:
- Follower growth trend
- Engagement rate over time
- Reach vs Impressions comparison

Bar Chart (Comparisons)
Best for: Comparing categories
Data: Categories on X-axis, Metric on Y-axis
Examples:
- Engagement by content type
- Reach by topic
- Performance by day of week

Column Chart (Rankings)
Best for: Top/bottom performers
Data: Items ranked by metric
Examples:
- Top 10 posts by engagement
- Bottom 5 posts (identify issues)
- Hashtag performance ranking

Pie Chart (Distributions)
Best for: Showing proportions
Data: Category and percentage
Examples:
- Content type distribution
- Topic mix percentage
- Traffic source breakdown

Scatter Plot (Correlations)
Best for: Relationship between two metrics
Data: Metric 1 on X-axis, Metric 2 on Y-axis
Examples:
- Reach vs Engagement Rate
- Post Length vs Engagement
- Time of Day vs Reach

Combo Chart (Multiple Metrics)
Best for: Related metrics with different scales
Data: Two chart types combined
Examples:
- Reach (bar) + Engagement Rate (line)
- Impressions (bar) + CTR (line)

Chart Best Practices:
✅ Clear title describing what chart shows
✅ Axis labels with units (%, K, M)
✅ Legend for multi-series charts
✅ Data labels for key points
✅ Consistent color scheme (on-brand)
✅ Not too much data (cluttered)
✅ Appropriate chart type for data
❌ Avoid 3D charts (harder to read)
❌ Avoid excessive colors (3-4 max)
❌ Don't clutter with gridlines
❌ No decorative elements (distracting)
```

**Dashboard Design**:
```

Executive Dashboard Layout:

Row 1: Header and Date Range
- Dashboard Title: "Xiaohongshu Performance Dashboard"
- Date Range Selector: Dropdown or cell reference
- Last Updated: Timestamp

Row 2: Key Performance Indicators (Big Numbers)
- Total Followers: [Value] [Growth %]
- Total Engagement: [Sum] [Avg per post]
- Avg Engagement Rate: [%] [vs last period]
- Total Reach: [Sum] [Avg per post]
- Top Post: [Title] [Engagement Rate]

Row 3-4: Trend Charts (Left - Right)
- Line chart: Follower growth (30 days)
- Line chart: Engagement rate trend (30 days)

Row 5-6: Comparison Charts
- Bar chart: Performance by content type
- Bar chart: Performance by day of week

Row 7-8: Rankings
- Top 10 posts table (linked to data)
- Bottom 5 posts table (troubleshooting)

Row 9: Goals and Progress
- Goal vs Actual comparison
- Traffic light status (Green/Yellow/Red)

Interactive Elements:
- Drop-down for content type filter
- Date range selectors (start/end cells)
- Slicers for dynamic filtering
- Buttons to refresh data
- Hyperlinks to detailed sheets

Conditional Formatting:
- KPIs > Goal: Green background
- KPIs 80-100% of Goal: Yellow background
- KPIs < 80% of Goal: Red background
- Trends up: Green arrow
- Trends down: Red arrow

Auto-Refresh Setup (if using external data):
1. Data → Get Data → From File
2. Select data source
3. Set refresh properties (e.g., every 24 hours)
4. Protect formula cells
5. Allow refresh on open
```

### Step 5: Analyze and Extract Insights

**Analysis Framework**:
```

Weekly Analysis Routine:

1. Update Data (15 min)
- Import new data from Xiaohongshu
- Paste into Raw Data sheet
- Refresh calculations and pivot tables
- Verify data integrity

2. Review Dashboard (10 min)
- Check KPIs vs goals
- Review trend charts for anomalies
- Identify top/bottom performers
- Note significant changes

3. Deep Dive Analysis (20 min)
- Content Type Analysis
  * Which types performed best?
  * Any types underperforming?
  * Seasonal patterns?

- Topic Analysis
  * Which topics resonated?
  * Any surprises?
  * Content gaps identified?

- Timing Analysis
  * Best/worst posting times
  * Day-of-week patterns
  * Optimal posting schedule

- Competitive Analysis
  * How do we compare?
  * Any competitor wins to learn from?
  * Market shifts?

4. Document Insights (15 min)
- Key findings: What worked, what didn't
- Recommendations: Action items for next week
- Tests running: A/B tests in progress
- Questions raised: Unknowns to investigate

5. Report Creation (20 min)
- Executive summary (1 page)
- Detailed analysis (2-3 pages)
- Visualizations (charts, graphs)
- Appendices (raw data if needed)

Total Time: ~80 minutes per week
Saves: 3-4 hours vs manual analysis

Insight Extraction Techniques:

Performance Analysis:
- Calculate growth rates (week-over-week, month-over-month)
- Compare to benchmarks (past performance, goals, competitors)
- Identify outliers (exceptionally good/bad)
- Spot trends (improving, declining, stable)

Correlation Analysis:
- Post time vs Engagement
- Content length vs Reach
- Hashtag count vs Saves
- Topic vs Follower growth

Segmentation Analysis:
- Performance by content type
- Performance by topic
- Performance by time of day
- Performance by day of week
- Performance by season

Gap Analysis:
- Goal vs Actual (performance gaps)
- Competitor comparison (market gaps)
- Audience demand vs Content supply (content gaps)
- Resource allocation vs ROI (efficiency gaps)
```

### Step 6: Report and Communicate Findings

**Report Structure**:
```

Weekly Performance Report (1-2 pages):

Page 1: Executive Summary
- Key metrics overview
- Progress toward goals
- Top 3 wins this week
- Top 3 challenges/learnings
- 3-5 recommendations for next week

Page 2: Detailed Analysis
- Content performance breakdown
- Engagement quality analysis
- Follower growth analysis
- Competitive comparison
- Testing and learnings

Monthly Performance Report (5-8 pages):

Page 1: Executive Dashboard
- All KPIs visualized
- Month-over-month comparison
- Goal progress
- Traffic light status

Page 2: Content Deep Dive
- Performance by content type
- Top performing posts
- Underperforming content analysis
- Content recommendations

Page 3: Audience Insights
- Follower growth analysis
- Audience demographics (if available)
- Engagement quality
- Audience feedback themes

Page 4: Timing and Seasonality
- Best posting times
- Day-of-week performance
- Seasonal patterns
- Holiday/event impacts

Page 5: Competitive Analysis
- Market position
- Competitor benchmarking
- Share of voice
- Opportunities/threats

Page 6: Goals and Forecast
- Goal progress
- Forecasting (next 30/60/90 days)
- Resource allocation recommendations
- Strategic initiatives

Page 7: Appendices
- Detailed data tables
- Methodology
- Definitions
- Raw data (if needed)

Presentation Tips:
✅ Start with key insights (executive summary first)
✅ Use visuals (charts, graphs, dashboards)
✅ Keep text minimal (let data speak)
✅ Highlight key numbers (color, size, bold)
✅ Tell story with data (context, insights, actions)
✅ Include recommendations (actionable next steps)
✅ Know your audience (execs need summaries, analysts need detail)
❌ Don't overwhelm with data (curate for relevance)
❌ Don't present without interpretation (add insights)
❌ Don't omit context (explain why numbers matter)
```

## Common Mistakes

| Mistake | Why Happens | Fix |
|---------|-------------|-----|
| Not updating data regularly | Time pressure, forget | Schedule weekly update, set reminders |
| Poor data structure | Started without plan | Design structure before collecting data |
| Wrong formulas | Excel knowledge gap | Validate formulas, test with known data |
| Over-complicating dashboards | Want everything visible | Focus on key metrics, keep simple |
| Not backing up data | Complacency | Save backup copies regularly |
| Manual data entry errors | Human error | Use data validation, double-check |
| Ignoring data quality | Trust exports blindly | Clean and validate imported data |
| Too many charts | Want comprehensive analysis | Fewer, more focused visualizations |
| Not documenting metrics | Assumes everyone knows | Create data dictionary |
| Forgetting to refresh | Static dashboard | Set refresh schedule, note last update |

## Real-World Impact

**Case Study: Excel Analytics Transformation**

A brand manager created Excel analytics system replacing manual reporting.

**Before Excel Analytics**:
- Manual data collection from screenshots
- Calculator for engagement rates
- No visual trends, just numbers
- 4 hours weekly for basic reporting
- Inconsistent metrics (different definitions)
- No historical analysis
- Poor insights, missed opportunities

**After Excel Implementation** (3 months):

System Setup (Month 1):
- Created master spreadsheet with 10 sheets
- Automated imports from Xiaohongshu
- Built formulas for 15 calculated metrics
- Created executive dashboard
- Set up conditional formatting
- Documented data dictionary

Analysis and Refinement (Months 2-3):
- Added competitor tracking
- Created content type analysis
- Built time-of-day analysis
- Developed A/B testing templates
- Automated weekly report generation
- Created monthly deep-dive templates

**Results** (12 months):
Time Savings:
- Weekly reporting: 4 hours → 45 minutes (82% reduction)
- Monthly analysis: 8 hours → 2 hours (75% reduction)
- Annual savings: 250+ hours

Improved Insights:
- Identified optimal posting time: 7-9 PM (+40% engagement)
- Discovered top content type: Video tutorials (3x engagement)
- Found underserved topic: Ingredient education (filled gap, +25% growth)
- Spent less time on reporting, more time on strategy

Business Impact:
- Engagement rate: +35% from optimization
- Follower growth: +50% from data-driven content
- Content efficiency: 40% improvement (fewer posts, better results)
- Team productivity: +15% (time saved reinvested)
- Decision quality: Evidence-based, not gut feeling

Spreadsheet Capabilities Built:
- Automated data import (saves 1 hour/week)
- 15 calculated metrics (instant vs manual)
- Interactive dashboard (real-time insights)
- 12 visualization templates (consistent reporting)
- Competitor benchmarking (market intelligence)
- A/B test tracker (systematic testing)

**Data-Backed Insights**:
- Excel automation saves 75-85% of reporting time
- Visual dashboards improve insight speed by 3-5x
- Calculated metrics prevent errors and ensure consistency
- Historical data enables trend analysis and forecasting
- Competitor tracking identifies 30-40% more opportunities
- A/B testing in Excel increases optimization rate by 2x
- Conditional formatting highlights insights instantly
- Pivot tables enable multi-dimensional analysis in minutes
- Well-structured spreadsheets are scalable for years of data
- Excel skills transfer to other tools and platforms

## Related Skills

**REQUIRED**: Use data-analytics (understand metrics to track)
**REQUIRED**: Use data-metrics-understanding (know what metrics mean)
**REQUIRED**: Use data-report (communicate findings)

**Recommended for Excel mastery**:
- **pivot-tables** - Advanced data summarization and analysis
- **data-visualization** - Chart and dashboard design principles
- **advanced-formulas** - Complex calculations and lookups
- **macros-automation** - VBA and automation for Excel
- **power-query** - Data import and transformation
- **spreadsheet-design** - Structure and architecture best practices
