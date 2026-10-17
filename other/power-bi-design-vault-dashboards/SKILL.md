---
name: power-bi-design-vault-dashboards
description: Expert skill for using Power BI Design Vault templates, DAX patterns, dashboard blueprints, and visual design systems for business intelligence projects.
triggers:
  - "help me customize a Power BI dashboard template"
  - "how do I apply a theme from the design vault"
  - "show me DAX patterns for dashboard measures"
  - "import a sample dataset into Power BI"
  - "adapt a retail analytics dashboard blueprint"
  - "use Power BI responsive layout templates"
  - "implement accessibility-first color palettes in dashboards"
  - "create a narrative dashboard from design vault"
---

# Power BI Design Vault Dashboards

> Skill by [ara.so](https://ara.so) — Design Skills collection

Expert guidance for leveraging the Power-Narrative Design Studio repository: a curated collection of Power BI dashboard templates, design systems, DAX libraries, and visual intelligence frameworks for modern business analytics.

## What This Project Provides

The Power BI Design Vault is a comprehensive library of:

- **Pre-built `.pbix` dashboard templates** for retail, HR, finance, and supply chain scenarios
- **Reusable JSON theme files** with accessibility-compliant color palettes
- **Sample datasets** in Parquet and CSV formats with synthetic business data
- **Annotated DAX measure libraries** with inline documentation
- **SVG icon sets and visual assets** optimized for Power BI theming
- **Responsive layout architectures** following 12-column grid systems
- **Design pattern documentation** for visual hierarchy and cognitive accessibility

Primary use case: Accelerate Power BI dashboard development by adapting pre-built blueprints rather than building from scratch.

## Installation and Setup

### Prerequisites

- Power BI Desktop (October 2025 release or later)
- Basic familiarity with Power BI data modeling and DAX
- Git or GitHub Desktop for cloning the repository

### Clone the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/Lithiumgreentek/power-bi-design-vault.git
cd power-bi-design-vault
```

### Repository Structure

```
power-bi-design-vault/
├── dashboards/
│   ├── retail-sales-opportunity/
│   │   ├── README.md
│   │   ├── retail-sales.pbix
│   │   └── assets/
│   ├── hr-attrition-forecast/
│   └── supply-chain-bottleneck/
├── datasets/
│   ├── sample-retail-clean.parquet
│   └── finance-trials.csv
├── themes/
│   ├── dark-enterprise.json
│   └── pastel-minimal.json
├── visual-assets/
│   ├── icons/
│   └── background-vectors/
└── documentation/
    ├── design-principles.md
    └── data-modeling-guide.pdf
```

## Working with Dashboard Templates

### Opening a Dashboard Template

1. Navigate to the specific dashboard folder (e.g., `dashboards/retail-sales-opportunity/`)
2. Open the `.pbix` file in Power BI Desktop
3. Review the model view to understand pre-configured relationships
4. Check the "DAX Dictionary" page for measure explanations

### Connecting Your Own Data

**Replace sample dataset with your data source:**

```powerquery
// Power Query M code to replace data source
let
    Source = Csv.Document(
        File.Contents("C:\YourPath\your-data.csv"),
        [Delimiter=",", Columns=10, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"Date", type date},
        {"Sales", type number},
        {"Product", type text}
    })
in
    ChangedTypes
```

**Using environment variables for data source paths:**

In Power Query, create a parameter:

```powerquery
// Create a parameter for flexible data source paths
DataSourcePath = Text.From(Excel.CurrentWorkbook(){[Name="DataPath"]}[Content]{0}[Column1])
```

Then reference `DataSourcePath` in your `File.Contents()` calls.

### Applying Theme Files

**Import a JSON theme:**

1. In Power BI Desktop, go to **View** → **Themes** → **Browse for themes**
2. Navigate to `themes/` folder
3. Select `dark-enterprise.json` or `pastel-minimal.json`
4. Click **Open**

**Customize theme colors programmatically:**

```json
{
  "name": "Custom Corporate Theme",
  "dataColors": [
    "#1F77B4",
    "#FF7F0E",
    "#2CA02C",
    "#D62728",
    "#9467BD"
  ],
  "background": "#FFFFFF",
  "foreground": "#333333",
  "tableAccent": "#1F77B4",
  "good": "#2CA02C",
  "neutral": "#FFC107",
  "bad": "#D62728",
  "textClasses": {
    "callout": {
      "fontSize": 45,
      "fontFace": "Segoe UI",
      "color": "#333333"
    },
    "title": {
      "fontSize": 14,
      "fontFace": "Segoe UI Semibold",
      "color": "#666666"
    }
  }
}
```

Save this as `custom-theme.json` and import via the same process.

## DAX Patterns from the Vault

### Dynamic Measure Titles

```dax
// Dynamic title that changes based on slicer selection
Dynamic Title = 
VAR SelectedPeriod = SELECTEDVALUE('Calendar'[Period], "All Periods")
VAR SelectedRegion = SELECTEDVALUE('Geography'[Region], "All Regions")
RETURN
    "Sales Performance - " & SelectedPeriod & " | " & SelectedRegion
```

### Parameter-Driven Measures

```dax
// Toggle between different metrics using a parameter table
Selected Metric = 
SWITCH(
    SELECTEDVALUE('MetricSelector'[Metric]),
    "Revenue", [Total Revenue],
    "Profit", [Total Profit],
    "Units", [Total Units Sold],
    [Total Revenue] // Default
)
```

### Time Intelligence with Fiscal Calendar

```dax
// Year-to-date calculation respecting fiscal year starting in April
Sales YTD (Fiscal) = 
CALCULATE(
    [Total Sales],
    DATESYTD(
        'Calendar'[Date],
        "3/31" // Fiscal year ends March 31
    )
)
```

### Previous Period Comparison

```dax
// Sales vs. previous period with error handling
Sales vs Previous Period = 
VAR CurrentSales = [Total Sales]
VAR PreviousSales = 
    CALCULATE(
        [Total Sales],
        DATEADD('Calendar'[Date], -1, MONTH)
    )
VAR PercentChange = 
    IF(
        ISBLANK(PreviousSales) || PreviousSales = 0,
        BLANK(),
        DIVIDE(CurrentSales - PreviousSales, PreviousSales)
    )
RETURN
    PercentChange
```

### Custom Tooltip Measure

```dax
// Rich tooltip text with conditional formatting
Tooltip Text = 
VAR ProductName = SELECTEDVALUE('Product'[Name])
VAR Sales = [Total Sales]
VAR Target = [Sales Target]
VAR Achievement = DIVIDE(Sales, Target, 0)
VAR PerformanceLabel = 
    SWITCH(
        TRUE(),
        Achievement >= 1.1, "Exceeding",
        Achievement >= 1.0, "On Target",
        Achievement >= 0.9, "Near Target",
        "Below Target"
    )
RETURN
    ProductName & UNICHAR(10) &
    "Sales: " & FORMAT(Sales, "$#,##0") & UNICHAR(10) &
    "Target: " & FORMAT(Target, "$#,##0") & UNICHAR(10) &
    "Status: " & PerformanceLabel
```

### Rank with Tie Handling

```dax
// Product rank by sales with ties resolved alphabetically
Product Rank = 
RANKX(
    ALL('Product'[Name]),
    [Total Sales] + (DIVIDE(1, UNICODE('Product'[Name]) + 1000000)),
    ,
    DESC,
    DENSE
)
```

## Responsive Layout Best Practices

### Grid System Implementation

When adapting templates, maintain the 12-column grid structure:

- **Header section**: 12 columns × 2 rows (fixed)
- **KPI cards**: 3 columns each × 2 rows (4 cards per row)
- **Main chart area**: 8 columns × 6 rows
- **Filter panel**: 4 columns × 6 rows (right sidebar)
- **Footer/details**: 12 columns × 1 row

### Mobile Layout Conversion

For mobile views, the vault templates use this pattern:

1. Stack KPI cards vertically (12 columns × 2 rows each)
2. Collapse filter panel into dropdown slicers
3. Simplify charts (e.g., clustered column → simple bar)
4. Remove decorative visual elements

**Bookmark navigation for mobile:**

Create bookmarks for:
- Overview (KPIs only)
- Trend Analysis (time series chart)
- Detail View (table with drill-through)

## Dataset Integration Patterns

### Loading Parquet Files

```powerquery
// Load Parquet file from datasets folder
let
    Source = Parquet.Document(
        File.Contents("datasets/sample-retail-clean.parquet")
    ),
    Navigation = Source{[Name="data"]}[Data]
in
    Navigation
```

### CSV Import with Type Inference

```powerquery
// Import CSV with automatic type detection
let
    Source = Csv.Document(
        File.Contents("datasets/finance-trials.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    DetectedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        List.Zip({
            Table.ColumnNames(PromotedHeaders),
            List.Transform(
                Table.ColumnNames(PromotedHeaders),
                each try Table.Schema(PromotedHeaders){[Name=_]}[TypeName] otherwise "text"
            )
        })
    )
in
    DetectedTypes
```

### Multilingual Field Handling

```dax
// Display measure value with locale-specific formatting
Localized Sales = 
VAR Sales = [Total Sales]
VAR CurrencySymbol = SELECTEDVALUE('Locale'[currency_symbol], "$")
VAR DecimalSeparator = SELECTEDVALUE('Locale'[decimal_separator], ".")
RETURN
    CurrencySymbol & FORMAT(Sales, "#,##0" & DecimalSeparator & "00")
```

## Visual Asset Integration

### Using SVG Icons

**Import SVG as image:**

1. Insert → Image
2. Browse to `visual-assets/icons/`
3. Select appropriate icon (e.g., `trending-up.svg`)
4. Set image fit to "Fit" (not "Fill")
5. Use conditional formatting to swap icons based on measure values

**Dynamic icon selection with conditional formatting:**

Create a measure that returns image file paths:

```dax
Performance Icon URL = 
VAR Performance = [Sales vs Target %]
VAR IconPath = "https://raw.githubusercontent.com/Lithiumgreentek/power-bi-design-vault/main/visual-assets/icons/"
RETURN
    SWITCH(
        TRUE(),
        Performance >= 1.1, IconPath & "trending-up.svg",
        Performance >= 0.9, IconPath & "stable.svg",
        IconPath & "trending-down.svg"
    )
```

Apply this measure to an image visual's **Image URL** field.

### Background Vector Integration

For dashboard backgrounds:

1. Canvas Settings → Canvas background → Image
2. Browse to `visual-assets/background-vectors/`
3. Set transparency to 95-98% for subtle effect
4. Use "Fit" sizing to avoid distortion

## Common Customization Workflows

### Adapting Retail Template for Different Industry

**Scenario: Convert retail dashboard to healthcare metrics**

1. **Replace dataset:**
   - Swap `sample-retail-clean.parquet` with patient admission data
   - Maintain similar schema (Date, Category, Metrics)

2. **Rename measures:**
   - `Total Sales` → `Total Admissions`
   - `Average Transaction` → `Average Length of Stay`

3. **Update visuals:**
   - Product hierarchy → Department/Condition hierarchy
   - Regional map → Hospital campus map

4. **Adjust color palette:**
   - Apply `pastel-minimal.json` theme
   - Change accent colors to healthcare-friendly blues/greens

### Creating a Drill-Through Page

```dax
// Measure to enable drill-through only when single item selected
Enable Drillthrough = 
IF(
    HASONEVALUE('Product'[Name]),
    1,
    BLANK()
)
```

Configure drill-through in Power BI:

1. Create new report page (e.g., "Product Detail")
2. Add `Product[Name]` to drill-through filters
3. Add back button: Insert → Button → Back
4. Use `Enable Drillthrough` measure in visual-level filter

### Implementing Bookmarks for Narrative Flow

**Create a guided narrative:**

1. **Bookmark 1: Executive Summary**
   - Show only KPI cards and trend chart
   - Hide detail tables and slicers

2. **Bookmark 2: Regional Breakdown**
   - Show map and regional bar chart
   - Display region slicer

3. **Bookmark 3: Product Deep Dive**
   - Show product matrix and decomposition tree
   - Display product category slicer

Add navigation buttons:
- Insert → Button → Blank
- Action → Type: Bookmark → Select corresponding bookmark
- Label buttons "Overview" → "Regions" → "Products"

## Troubleshooting

### Theme Not Applying to All Visuals

**Issue:** Custom theme colors don't affect certain chart types

**Solution:**
- Ensure theme JSON includes all visual types in `visualStyles` section
- Manually set colors for custom visuals (they may not support theming)
- Check Power BI Desktop version supports theme features used

### DAX Measures Return BLANK() Unexpectedly

**Issue:** Measures work in some visuals but return blank in others

**Checklist:**
1. Verify filter context isn't removing all rows: Use `COUNTROWS(ALL('Table'))`
2. Check for division by zero: Wrap in `DIVIDE(numerator, denominator, 0)`
3. Ensure relationships are bidirectional if needed (use sparingly)
4. Test measure in table visual with all dimensions to debug

### Dataset Path Broken After Moving Files

**Issue:** Data source paths hardcoded to specific machine

**Solution:**
```powerquery
// Use relative path from .pbix location
let
    CurrentFileFolder = Text.BeforeDelimiter(
        Text.From(Excel.CurrentWorkbook(){0}[Content]),
        Text.From(Excel.CurrentWorkbook(){0}[Name])
    ),
    DatasetPath = CurrentFileFolder & "datasets\sample-retail-clean.parquet",
    Source = Parquet.Document(File.Contents(DatasetPath))
in
    Source
```

Or use parameter with environment variable:

```bash
# Set environment variable (Windows)
setx POWERBI_DATA_PATH "C:\Projects\power-bi-design-vault\datasets"
```

Then reference in Power Query via external parameter configuration.

### Performance Issues with Large Datasets

**Optimization strategies:**

1. **Use Import mode for small datasets (<1GB)**
2. **Switch to DirectQuery for large SQL sources**
3. **Aggregate data in Power Query:**

```powerquery
// Pre-aggregate data before loading
let
    Source = Csv.Document(File.Contents("large-dataset.csv")),
    GroupedData = Table.Group(
        Source,
        {"Date", "Product"},
        {
            {"Total Sales", each List.Sum([Sales]), type number},
            {"Avg Price", each List.Average([Price]), type number}
        }
    )
in
    GroupedData
```

4. **Optimize DAX with variables:**

```dax
// Cache intermediate calculations
Optimized Margin = 
VAR TotalRevenue = [Total Revenue]
VAR TotalCost = [Total Cost]
VAR Margin = TotalRevenue - TotalCost
VAR MarginPercent = DIVIDE(Margin, TotalRevenue)
RETURN
    MarginPercent
```

### Responsive Layout Not Working on Mobile

**Common causes:**

1. **Fixed size visuals:** Convert to relative sizing
   - Select visual → Format → General → Size → Use percentage values

2. **Overlapping visuals:** Use layout grid
   - View → Gridlines → Snap to grid
   - Ensure no visuals share exact same coordinates

3. **Mobile layout not configured:**
   - View → Mobile layout
   - Manually arrange visuals for phone view
   - Remove non-essential elements

## Advanced Pattern: Custom Tooltip Page

Create reusable tooltip pages for consistent hover experiences:

**Tooltip page setup:**

1. Create new page, rename to "Product Tooltip"
2. Page Settings → Page Information → Allow use as tooltip: **On**
3. Set canvas size to 320×240 px
4. Add compact visuals (card, mini bar chart, sparkline)

**DAX for tooltip-specific measures:**

```dax
// Tooltip: Show last 6 months trend
Tooltip Sales Trend = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(
        'Calendar'[Date],
        MAX('Calendar'[Date]),
        -6,
        MONTH
    )
)
```

**Apply tooltip:**

1. Select any visual on main report page
2. Format → Tooltip → Type: Report page
3. Page: Select "Product Tooltip"
4. Hover over data points to see custom tooltip

## Working with Documentation

The vault includes extensive documentation:

**design-principles.md:** Guidelines on visual hierarchy, gestalt principles, color psychology

**data-modeling-guide.pdf:** Star schema vs snowflake, when to use calculated tables, relationship best practices

**Key takeaways to implement:**

- **Rule of thirds:** Place critical KPIs at intersection points
- **F-pattern reading:** Position navigation and filters top-left
- **Color temperature:** Warm colors (red/orange) for alerting, cool colors (blue/green) for positive trends
- **Whitespace ratio:** Maintain 30-40% empty space for visual breathing room

## Example: Complete Dashboard Customization

**Scenario:** Adapt HR Attrition dashboard for your company data

```powerquery
// Step 1: Load your HR data
let
    Source = Sql.Database(
        Environment.GetEnvironmentVariable("SQL_SERVER"),
        Environment.GetEnvironmentVariable("SQL_DATABASE")
    ),
    EmployeeTable = Source{[Schema="dbo",Item="Employees"]}[Data],
    FilteredRows = Table.SelectRows(
        EmployeeTable,
        each [TerminationDate] = null or [TerminationDate] >= #date(2024,1,1)
    )
in
    FilteredRows
```

```dax
// Step 2: Create attrition rate measure
Attrition Rate = 
VAR TotalEmployees = 
    CALCULATE(
        DISTINCTCOUNT('Employee'[EmployeeID]),
        ALL('Calendar')
    )
VAR Terminations = 
    CALCULATE(
        DISTINCTCOUNT('Employee'[EmployeeID]),
        'Employee'[Status] = "Terminated"
    )
RETURN
    DIVIDE(Terminations, TotalEmployees, 0)

// Step 3: Forecast next quarter attrition
Forecasted Attrition = 
VAR HistoricalTrend = 
    LINESTX(
        ADDCOLUMNS(
            SUMMARIZE('Calendar', 'Calendar'[Quarter]),
            "@Attrition", [Attrition Rate]
        ),
        [Quarter],
        [@Attrition]
    )
VAR Slope = [Slope]
VAR Intercept = [Intercept]
VAR NextQuarter = MAX('Calendar'[Quarter]) + 1
RETURN
    Slope * NextQuarter + Intercept
```

**Step 4:** Apply `dark-enterprise.json` theme for executive presentation

**Step 5:** Configure drill-through from department summary to individual employee analysis

This workflow demonstrates the full power of the design vault: starting with a template, integrating real data sources, applying custom DAX logic, and delivering a production-ready dashboard.

---

**Repository:** [github.com/Lithiumgreentek/power-bi-design-vault](https://github.com/Lithiumgreentek/power-bi-design-vault)

**License:** MIT — Use, modify, and redistribute freely for personal or commercial projects.
