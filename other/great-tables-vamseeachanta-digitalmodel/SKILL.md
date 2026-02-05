---
name: great-tables
version: 1.0.0
description: Publication-quality tables in Python with rich styling, formatting, conditional formatting, and export to HTML/images - inspired by R's gt package
author: workspace-hub
category: data-analysis
capabilities:
  - Publication-quality table rendering
  - Rich styling and formatting options
  - Conditional formatting with colors and icons
  - Grouped rows and columns
  - Spanner headers and footnotes
  - Export to HTML, PNG, and PDF
  - Integration with pandas and polars
  - Interactive HTML output
tools:
  - great_tables
  - pandas
  - polars
  - webshot
tags: [great-tables, tables, formatting, publication, styling, conditional-formatting, html-tables, data-presentation, reporting]
platforms: [python]
related_skills:
  - pandas-data-processing
  - polars
  - ydata-profiling
  - streamlit
  - plotly
---

# Great Tables Publication-Quality Tables Skill

Master Great Tables for creating beautiful, publication-quality tables in Python with rich styling, conditional formatting, and export capabilities. Inspired by R's gt package.

## When to Use This Skill

### USE Great Tables when:
- **Publication tables** - Creating tables for reports, papers, or presentations
- **Data presentation** - Professional display of analysis results
- **Conditional formatting** - Highlighting patterns with colors and icons
- **Complex layouts** - Multi-level headers, grouped rows, footnotes
- **HTML reports** - Interactive tables for web-based reports
- **Quick formatting** - Need polished tables without manual styling
- **Dashboard components** - Tables in Streamlit/Dash applications
- **Export requirements** - Need PNG or PDF output

### DON'T USE Great Tables when:
- **Large datasets** - Over 1000 rows for display (use pagination)
- **Interactive editing** - Need editable cells (use Streamlit data_editor)
- **Real-time updates** - Streaming data display
- **Complex interactivity** - Sorting, filtering (use DataTables or AG Grid)
- **Raw data exploration** - Use pandas display or ydata-profiling

## Prerequisites

```bash
# Basic installation
pip install great_tables

# With all optional dependencies
pip install great_tables pandas polars

# For image export (PNG/PDF)
pip install great_tables webshot

# Using uv (recommended)
uv pip install great_tables pandas polars

# Verify installation
python -c "from great_tables import GT; print('Great Tables ready!')"
```

## Core Capabilities

### 1. Basic Table Creation

**Simplest Usage:**
```python
from great_tables import GT
import pandas as pd

# Create sample data
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales"],
    "Salary": [95000, 78000, 88000, 92000],
    "Years": [5, 3, 4, 6]
})

# Create basic table
table = GT(df)

# Display (in Jupyter) or save
table.save("basic_table.html")
```

**With Title and Subtitle:**
```python
from great_tables import GT, md
import pandas as pd

df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Gadget X", "Gadget Y"],
    "Revenue": [150000, 220000, 180000, 95000],
    "Units": [1500, 2200, 900, 950],
    "Growth": [0.12, 0.25, 0.08, -0.05]
})

table = (
    GT(df)
    .tab_header(
        title="Q4 2025 Sales Performance",
        subtitle="Product line revenue and growth metrics"
    )
)

table.save("sales_table.html")
```

**With Source Notes:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Country": ["USA", "UK", "Germany", "Japan"],
    "GDP_Trillion": [25.5, 3.1, 4.2, 4.9],
    "Population_Million": [331, 67, 83, 125]
})

table = (
    GT(df)
    .tab_header(
        title="World Economic Indicators",
        subtitle="Top economies by GDP"
    )
    .tab_source_note(
        source_note="Source: World Bank, 2024"
    )
    .tab_source_note(
        source_note="GDP in trillion USD"
    )
)

table.save("economy_table.html")
```

### 2. Column Formatting

**Numeric Formatting:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Item": ["Product A", "Product B", "Product C"],
    "Price": [29.99, 149.50, 9.99],
    "Revenue": [1500000, 2250000, 890000],
    "Margin": [0.35, 0.42, 0.28],
    "Units": [50000, 15000, 89000]
})

table = (
    GT(df)
    .tab_header(title="Product Metrics")

    # Format as currency
    .fmt_currency(
        columns="Price",
        currency="USD"
    )

    # Format large numbers with suffixes
    .fmt_number(
        columns="Revenue",
        use_seps=True,
        decimals=0
    )

    # Format as percentage
    .fmt_percent(
        columns="Margin",
        decimals=1
    )

    # Format with thousand separators
    .fmt_integer(
        columns="Units",
        use_seps=True
    )
)

table.save("numeric_formatting.html")
```

**Date and Time Formatting:**
```python
from great_tables import GT
import pandas as pd
from datetime import datetime, date

df = pd.DataFrame({
    "Event": ["Launch", "Update", "Maintenance", "Release"],
    "Date": [
        date(2025, 1, 15),
        date(2025, 3, 22),
        date(2025, 6, 1),
        date(2025, 9, 30)
    ],
    "Timestamp": [
        datetime(2025, 1, 15, 9, 0),
        datetime(2025, 3, 22, 14, 30),
        datetime(2025, 6, 1, 2, 0),
        datetime(2025, 9, 30, 10, 0)
    ]
})

table = (
    GT(df)
    .tab_header(title="Product Timeline")

    # Format date
    .fmt_date(
        columns="Date",
        date_style="day_month_year"
    )

    # Format datetime
    .fmt_datetime(
        columns="Timestamp",
        date_style="yMd",
        time_style="Hm"
    )
)

table.save("date_formatting.html")
```

**Custom Number Formatting:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Metric": ["Users", "Revenue", "Conversion", "Avg Order"],
    "Value": [1234567, 5678901.23, 0.0342, 156.789]
})

table = (
    GT(df)
    .tab_header(title="Dashboard Metrics")

    # Custom suffixes for large numbers
    .fmt_number(
        columns="Value",
        rows=[0],  # First row only
        compact=True  # Use K, M, B suffixes
    )

    # Currency for second row
    .fmt_currency(
        columns="Value",
        rows=[1],
        currency="USD",
        decimals=0
    )

    # Percentage for third row
    .fmt_percent(
        columns="Value",
        rows=[2],
        decimals=2
    )

    # Standard number for fourth row
    .fmt_currency(
        columns="Value",
        rows=[3],
        currency="USD",
        decimals=2
    )
)

table.save("custom_formatting.html")
```

### 3. Styling and Colors

**Background Colors:**
```python
from great_tables import GT
from great_tables import style, loc
import pandas as pd

df = pd.DataFrame({
    "Category": ["Electronics", "Clothing", "Food", "Home"],
    "Q1": [150000, 95000, 120000, 85000],
    "Q2": [180000, 88000, 135000, 92000],
    "Q3": [165000, 102000, 128000, 78000],
    "Q4": [210000, 115000, 145000, 105000]
})

table = (
    GT(df)
    .tab_header(title="Quarterly Sales by Category")

    # Style header row
    .tab_style(
        style=style.fill(color="#4a86e8"),
        locations=loc.column_labels()
    )
    .tab_style(
        style=style.text(color="white", weight="bold"),
        locations=loc.column_labels()
    )

    # Alternate row colors
    .tab_style(
        style=style.fill(color="#f3f3f3"),
        locations=loc.body(rows=[1, 3])  # Even rows
    )

    # Highlight specific cell
    .tab_style(
        style=style.fill(color="#90EE90"),
        locations=loc.body(columns="Q4", rows=[0])  # Highest Q4
    )
)

table.save("styled_table.html")
```

**Text Styling:**
```python
from great_tables import GT
from great_tables import style, loc
import pandas as pd

df = pd.DataFrame({
    "Rank": [1, 2, 3, 4, 5],
    "Company": ["TechCorp", "DataInc", "CloudSoft", "AILabs", "DevHub"],
    "Revenue_B": [125.4, 98.2, 87.5, 76.3, 65.8],
    "Change": [0.15, 0.08, -0.03, 0.22, -0.12]
})

table = (
    GT(df)
    .tab_header(title="Top Companies by Revenue")

    # Bold first column
    .tab_style(
        style=style.text(weight="bold"),
        locations=loc.body(columns="Rank")
    )

    # Italic company names
    .tab_style(
        style=style.text(style="italic"),
        locations=loc.body(columns="Company")
    )

    # Color positive/negative changes
    .tab_style(
        style=style.text(color="green"),
        locations=loc.body(columns="Change", rows=[0, 1, 3])  # Positive
    )
    .tab_style(
        style=style.text(color="red"),
        locations=loc.body(columns="Change", rows=[2, 4])  # Negative
    )

    # Format numbers
    .fmt_currency(columns="Revenue_B", currency="USD", decimals=1)
    .fmt_percent(columns="Change", decimals=1)
)

table.save("text_styled.html")
```

**Borders and Spacing:**
```python
from great_tables import GT
from great_tables import style, loc
import pandas as pd

df = pd.DataFrame({
    "Section": ["Introduction", "Methods", "Results", "Discussion"],
    "Pages": [5, 12, 18, 8],
    "Figures": [2, 6, 15, 3],
    "Tables": [0, 3, 8, 1]
})

table = (
    GT(df)
    .tab_header(title="Manuscript Structure")

    # Add border below header
    .tab_style(
        style=style.borders(sides="bottom", color="black", weight="2px"),
        locations=loc.column_labels()
    )

    # Add border below last row
    .tab_style(
        style=style.borders(sides="bottom", color="black", weight="2px"),
        locations=loc.body(rows=[-1])
    )

    # Cell padding
    .tab_options(
        data_row_padding="10px",
        column_labels_padding="12px"
    )
)

table.save("bordered_table.html")
```

### 4. Conditional Formatting

**Color Scales:**
```python
from great_tables import GT
from great_tables import style, loc
from great_tables.data import countrypops
import pandas as pd

# Sample heatmap data
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "North": [85, 92, 88, 95, 91, 97],
    "South": [72, 78, 81, 75, 82, 88],
    "East": [90, 85, 92, 89, 94, 91],
    "West": [68, 75, 79, 82, 78, 85]
})

table = (
    GT(df)
    .tab_header(title="Regional Performance Scores")

    # Apply color scale to data columns
    .data_color(
        columns=["North", "South", "East", "West"],
        palette=["#FF6B6B", "#FFEB3B", "#4CAF50"],  # Red -> Yellow -> Green
        domain=[60, 100]
    )
)

table.save("color_scale.html")
```

**Conditional Icons:**
```python
from great_tables import GT, html
import pandas as pd

df = pd.DataFrame({
    "Metric": ["Revenue", "Users", "Conversion", "NPS"],
    "Current": [1250000, 85000, 3.2, 72],
    "Previous": [1180000, 78000, 3.5, 68],
    "Change_Pct": [5.9, 9.0, -8.6, 5.9]
})

def trend_icon(value):
    """Return trend icon based on value."""
    if value > 0:
        return html('<span style="color: green;">&#9650;</span>')  # Up arrow
    elif value < 0:
        return html('<span style="color: red;">&#9660;</span>')    # Down arrow
    else:
        return html('<span style="color: gray;">&#9654;</span>')   # Right arrow

# Add trend column
df["Trend"] = df["Change_Pct"].apply(trend_icon)

table = (
    GT(df)
    .tab_header(title="Key Metrics Dashboard")

    .fmt_number(columns="Current", use_seps=True, decimals=0)
    .fmt_number(columns="Previous", use_seps=True, decimals=0)
    .fmt_percent(columns="Change_Pct", decimals=1, scale_values=False)
)

table.save("conditional_icons.html")
```

**Bar Charts in Cells:**
```python
from great_tables import GT, html
import pandas as pd

df = pd.DataFrame({
    "Product": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
    "Sales": [85000, 120000, 65000, 95000, 110000],
    "Target": [100000, 100000, 100000, 100000, 100000]
})

def create_bar(value, max_value=150000):
    """Create inline bar chart."""
    width = min(value / max_value * 100, 100)
    color = "#4CAF50" if value >= 100000 else "#FF9800"
    return html(f'''
        <div style="background: #eee; width: 100px; height: 20px;">
            <div style="background: {color}; width: {width}%; height: 100%;"></div>
        </div>
    ''')

df["Progress"] = df["Sales"].apply(create_bar)

table = (
    GT(df)
    .tab_header(title="Sales Progress by Product")
    .fmt_number(columns="Sales", use_seps=True, decimals=0)
    .fmt_number(columns="Target", use_seps=True, decimals=0)
)

table.save("bar_charts.html")
```

### 5. Grouped Rows and Columns

**Row Groups:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Region": ["North", "North", "South", "South", "East", "East", "West", "West"],
    "Product": ["Widget", "Gadget", "Widget", "Gadget", "Widget", "Gadget", "Widget", "Gadget"],
    "Sales": [45000, 32000, 38000, 41000, 52000, 28000, 35000, 39000],
    "Units": [450, 160, 380, 205, 520, 140, 350, 195]
})

table = (
    GT(df, groupname_col="Region")  # Group by Region
    .tab_header(
        title="Sales by Region and Product",
        subtitle="Q4 2025 Performance"
    )
    .fmt_currency(columns="Sales", currency="USD", decimals=0)
    .fmt_integer(columns="Units", use_seps=True)

    # Style group labels
    .tab_style(
        style=[
            style.fill(color="#e8e8e8"),
            style.text(weight="bold")
        ],
        locations=loc.row_groups()
    )
)

table.save("row_groups.html")
```

**Column Spanners:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Gadget X"],
    "Q1_Sales": [25000, 32000, 18000],
    "Q1_Units": [250, 320, 90],
    "Q2_Sales": [28000, 35000, 22000],
    "Q2_Units": [280, 350, 110],
    "Q3_Sales": [31000, 38000, 25000],
    "Q3_Units": [310, 380, 125]
})

table = (
    GT(df)
    .tab_header(title="Quarterly Performance")

    # Create column spanners
    .tab_spanner(
        label="Q1",
        columns=["Q1_Sales", "Q1_Units"]
    )
    .tab_spanner(
        label="Q2",
        columns=["Q2_Sales", "Q2_Units"]
    )
    .tab_spanner(
        label="Q3",
        columns=["Q3_Sales", "Q3_Units"]
    )

    # Rename columns
    .cols_label(
        Q1_Sales="Sales",
        Q1_Units="Units",
        Q2_Sales="Sales",
        Q2_Units="Units",
        Q3_Sales="Sales",
        Q3_Units="Units"
    )

    # Format numbers
    .fmt_currency(columns=["Q1_Sales", "Q2_Sales", "Q3_Sales"], currency="USD", decimals=0)
    .fmt_integer(columns=["Q1_Units", "Q2_Units", "Q3_Units"], use_seps=True)
)

table.save("column_spanners.html")
```

**Nested Groups:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Division": ["Consumer", "Consumer", "Consumer", "Enterprise", "Enterprise", "Enterprise"],
    "Category": ["Electronics", "Home", "Fashion", "Software", "Hardware", "Services"],
    "Product": ["Phones", "Furniture", "Apparel", "Cloud", "Servers", "Consulting"],
    "Revenue": [150, 45, 78, 220, 180, 95],
    "Growth": [0.12, 0.05, -0.02, 0.25, 0.08, 0.15]
})

table = (
    GT(df, groupname_col="Division", rowname_col="Category")
    .tab_header(
        title="Business Unit Performance",
        subtitle="Annual Revenue (Millions USD)"
    )
    .fmt_currency(columns="Revenue", currency="USD", decimals=0)
    .fmt_percent(columns="Growth", decimals=1)
)

table.save("nested_groups.html")
```

### 6. Footnotes and Annotations

**Adding Footnotes:**
```python
from great_tables import GT
from great_tables import loc
import pandas as pd

df = pd.DataFrame({
    "Company": ["TechCorp", "DataInc", "CloudSoft", "AILabs"],
    "Revenue_B": [125.4, 98.2, 87.5, 76.3],
    "Employees": [45000, 28000, 15000, 8500],
    "Founded": [1985, 1998, 2010, 2015]
})

table = (
    GT(df)
    .tab_header(
        title="Tech Companies Overview",
        subtitle="Leading technology firms"
    )

    # Add footnote to title
    .tab_footnote(
        footnote="Revenue in billions USD",
        locations=loc.title()
    )

    # Add footnote to specific column
    .tab_footnote(
        footnote="Full-time employees only",
        locations=loc.column_labels(columns="Employees")
    )

    # Add footnote to specific cell
    .tab_footnote(
        footnote="Acquired by MegaCorp in 2024",
        locations=loc.body(columns="Company", rows=[2])
    )

    # Source note
    .tab_source_note(
        source_note="Data as of December 2025"
    )

    .fmt_currency(columns="Revenue_B", currency="USD", decimals=1)
    .fmt_integer(columns="Employees", use_seps=True)
)

table.save("footnotes.html")
```

**Stubhead Labels:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Year": [2022, 2023, 2024, 2025],
    "Revenue": [85.2, 92.5, 105.8, 118.3],
    "Profit": [12.5, 15.8, 19.2, 23.1],
    "Margin": [0.147, 0.171, 0.181, 0.195]
})

table = (
    GT(df, rowname_col="Year")
    .tab_header(title="Financial Summary")
    .tab_stubhead(label="Fiscal Year")  # Label for row names column

    .fmt_currency(columns=["Revenue", "Profit"], currency="USD", decimals=1)
    .fmt_percent(columns="Margin", decimals=1)
)

table.save("stubhead.html")
```

### 7. Export Options

**Export to HTML:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Item": ["A", "B", "C"],
    "Value": [100, 200, 150]
})

table = GT(df).tab_header(title="Export Demo")

# Save as HTML file
table.save("table.html")

# Get HTML string
html_string = table.as_raw_html()
print(html_string[:500])  # Preview
```

**Export to Image (PNG):**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Product": ["Widget", "Gadget", "Tool"],
    "Price": [29.99, 49.99, 19.99],
    "Stock": [150, 85, 200]
})

table = (
    GT(df)
    .tab_header(title="Product Inventory")
    .fmt_currency(columns="Price", currency="USD")
)

# Save as PNG (requires webshot/chromedriver)
# table.save("table.png")

# Alternative: Use playwright
# table.save("table.png", web_driver="playwright")
```

**Inline Display in Notebooks:**
```python
from great_tables import GT
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [95, 87, 92]
})

# In Jupyter, just return the table object
table = GT(df).tab_header(title="Test Scores")
table  # Displays inline
```

## Complete Examples

### Example 1: Financial Report Table

```python
from great_tables import GT, html
from great_tables import style, loc
import pandas as pd
import numpy as np

def create_financial_report(
    data: pd.DataFrame,
    title: str = "Financial Report",
    output_path: str = "financial_report.html"
) -> GT:
    """
    Create publication-quality financial report table.

    Args:
        data: Financial data with columns for metrics and periods
        title: Report title
        output_path: Output HTML path

    Returns:
        GT table object
    """

    # Sample financial data
    df = pd.DataFrame({
        "Metric": [
            "Revenue", "Cost of Sales", "Gross Profit",
            "Operating Expenses", "EBITDA", "Depreciation",
            "EBIT", "Interest Expense", "Pre-tax Income",
            "Taxes", "Net Income"
        ],
        "FY2023": [
            1250000, 625000, 625000,
            312500, 312500, 62500,
            250000, 25000, 225000,
            67500, 157500
        ],
        "FY2024": [
            1450000, 710500, 739500,
            348000, 391500, 72500,
            319000, 28000, 291000,
            87300, 203700
        ],
        "FY2025": [
            1680000, 806400, 873600,
            386400, 487200, 84000,
            403200, 30000, 373200,
            111960, 261240
        ],
        "Change_Pct": [
            15.9, 13.5, 18.1,
            11.0, 24.4, 15.9,
            26.4, 7.1, 28.3,
            28.3, 28.3
        ]
    })

    # Identify key rows
    key_rows = [2, 4, 6, 10]  # Gross Profit, EBITDA, EBIT, Net Income

    table = (
        GT(df)
        .tab_header(
            title=title,
            subtitle="Fiscal Year Comparison (USD)"
        )

        # Column labels
        .cols_label(
            Metric="",
            FY2023="FY 2023",
            FY2024="FY 2024",
            FY2025="FY 2025",
            Change_Pct="YoY Change"
        )

        # Format currencies
        .fmt_currency(
            columns=["FY2023", "FY2024", "FY2025"],
            currency="USD",
            decimals=0,
            use_seps=True
        )

        # Format percentage
        .fmt_percent(
            columns="Change_Pct",
            decimals=1,
            scale_values=False
        )

        # Style header
        .tab_style(
            style=[
                style.fill(color="#1a365d"),
                style.text(color="white", weight="bold")
            ],
            locations=loc.column_labels()
        )

        # Style key metric rows
        .tab_style(
            style=[
                style.fill(color="#f0f4f8"),
                style.text(weight="bold")
            ],
            locations=loc.body(rows=key_rows)
        )

        # Borders
        .tab_style(
            style=style.borders(sides="bottom", color="#1a365d", weight="2px"),
            locations=loc.column_labels()
        )
        .tab_style(
            style=style.borders(sides="top", color="#1a365d", weight="2px"),
            locations=loc.body(rows=[10])
        )

        # Positive/negative change colors
        .tab_style(
            style=style.text(color="#22543d"),
            locations=loc.body(
                columns="Change_Pct",
                rows=lambda x: x["Change_Pct"] > 0
            )
        )

        # Source note
        .tab_source_note(
            source_note="All figures in thousands USD. Change calculated FY2024 to FY2025."
        )

        # Options
        .tab_options(
            table_width="100%",
            table_font_size="14px"
        )
    )

    table.save(output_path)
    print(f"Financial report saved to: {output_path}")

    return table

# Generate report
# table = create_financial_report(df, "Annual Financial Report", "annual_report.html")
```

### Example 2: Sales Dashboard Table

```python
from great_tables import GT, html
from great_tables import style, loc
import pandas as pd
import numpy as np

def create_sales_dashboard_table(output_path: str = "sales_dashboard.html") -> GT:
    """
    Create sales dashboard table with KPIs and sparklines.
    """

    # Sample data
    np.random.seed(42)
    df = pd.DataFrame({
        "Region": ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"],
        "Revenue": [4250000, 3180000, 2890000, 1520000, 890000],
        "Target": [4000000, 3500000, 2500000, 1800000, 1000000],
        "Units": [42500, 31800, 57800, 30400, 17800],
        "Customers": [1250, 980, 1560, 620, 340],
        "Growth": [0.12, -0.05, 0.28, 0.08, 0.15],
        "Satisfaction": [4.5, 4.2, 4.7, 4.1, 4.3]
    })

    # Calculate achievement
    df["Achievement"] = df["Revenue"] / df["Target"]

    def achievement_bar(pct):
        """Create progress bar for achievement."""
        width = min(pct * 100, 100)
        if pct >= 1.0:
            color = "#22c55e"  # Green
        elif pct >= 0.9:
            color = "#eab308"  # Yellow
        else:
            color = "#ef4444"  # Red

        return html(f'''
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: #e5e7eb; width: 60px; height: 12px; border-radius: 6px;">
                    <div style="background: {color}; width: {width}%; height: 100%; border-radius: 6px;"></div>
                </div>
                <span style="font-size: 12px;">{pct*100:.0f}%</span>
            </div>
        ''')

    def growth_indicator(value):
        """Create growth indicator with arrow."""
        if value > 0:
            arrow = "&#9650;"  # Up
            color = "#22c55e"
        elif value < 0:
            arrow = "&#9660;"  # Down
            color = "#ef4444"
        else:
            arrow = "&#9654;"  # Right
            color = "#6b7280"

        return html(f'<span style="color: {color};">{arrow} {abs(value)*100:.1f}%</span>')

    def star_rating(score):
        """Create star rating display."""
        full_stars = int(score)
        half_star = score - full_stars >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)

        stars = "&#9733;" * full_stars
        if half_star:
            stars += "&#9734;"
        stars += "&#9734;" * empty_stars

        return html(f'<span style="color: #f59e0b;">{stars}</span> ({score:.1f})')

    df["Achievement_Bar"] = df["Achievement"].apply(achievement_bar)
    df["Growth_Display"] = df["Growth"].apply(growth_indicator)
    df["Rating_Display"] = df["Satisfaction"].apply(star_rating)

    table = (
        GT(df[["Region", "Revenue", "Achievement_Bar", "Units", "Customers", "Growth_Display", "Rating_Display"]])
        .tab_header(
            title="Regional Sales Performance",
            subtitle="Q4 2025 Dashboard"
        )

        .cols_label(
            Region="Region",
            Revenue="Revenue",
            Achievement_Bar="Target Achievement",
            Units="Units Sold",
            Customers="Active Customers",
            Growth_Display="YoY Growth",
            Rating_Display="CSAT Score"
        )

        # Format numbers
        .fmt_currency(columns="Revenue", currency="USD", decimals=0, use_seps=True)
        .fmt_integer(columns=["Units", "Customers"], use_seps=True)

        # Header style
        .tab_style(
            style=[
                style.fill(color="#0f172a"),
                style.text(color="white", weight="bold", size="13px")
            ],
            locations=loc.column_labels()
        )

        # Alternating rows
        .tab_style(
            style=style.fill(color="#f8fafc"),
            locations=loc.body(rows=[1, 3])
        )

        # Region column style
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(columns="Region")
        )

        .tab_source_note("Data refreshed: January 17, 2026")

        .tab_options(
            table_width="100%",
            data_row_padding="12px"
        )
    )

    table.save(output_path)
    return table

# table = create_sales_dashboard_table("sales_dashboard.html")
```

### Example 3: Scientific Data Table

```python
from great_tables import GT
from great_tables import style, loc
import pandas as pd
import numpy as np

def create_scientific_table(output_path: str = "scientific_table.html") -> GT:
    """
    Create publication-quality scientific data table.
    """

    # Experimental results data
    df = pd.DataFrame({
        "Treatment": ["Control", "Drug A (10mg)", "Drug A (50mg)", "Drug B (10mg)", "Drug B (50mg)"],
        "N": [25, 24, 26, 25, 23],
        "Mean": [45.2, 52.8, 61.3, 48.9, 58.7],
        "SD": [8.5, 9.2, 10.1, 8.9, 11.2],
        "SE": [1.7, 1.88, 1.98, 1.78, 2.34],
        "CI_Lower": [41.7, 48.9, 57.2, 45.2, 53.8],
        "CI_Upper": [48.7, 56.7, 65.4, 52.6, 63.6],
        "P_Value": [None, 0.042, 0.001, 0.185, 0.003]
    })

    def format_ci(row):
        """Format confidence interval."""
        return f"[{row['CI_Lower']:.1f}, {row['CI_Upper']:.1f}]"

    df["95% CI"] = df.apply(format_ci, axis=1)

    def format_pvalue(p):
        """Format p-value with significance markers."""
        if p is None:
            return "-"
        elif p < 0.001:
            return "<0.001***"
        elif p < 0.01:
            return f"{p:.3f}**"
        elif p < 0.05:
            return f"{p:.3f}*"
        else:
            return f"{p:.3f}"

    df["P_Formatted"] = df["P_Value"].apply(format_pvalue)

    table = (
        GT(df[["Treatment", "N", "Mean", "SD", "SE", "95% CI", "P_Formatted"]])
        .tab_header(
            title="Table 1. Treatment Effects on Primary Outcome",
            subtitle="Values represent endpoint measurements (units)"
        )

        .cols_label(
            Treatment="Treatment Group",
            N="n",
            Mean="Mean",
            SD="SD",
            SE="SE",
            P_Formatted="P-value"
        )

        # Format numbers
        .fmt_number(columns=["Mean", "SD", "SE"], decimals=1)

        # Center align numeric columns
        .cols_align(
            align="center",
            columns=["N", "Mean", "SD", "SE", "95% CI", "P_Formatted"]
        )

        # Header style (minimal, scientific)
        .tab_style(
            style=[
                style.text(weight="bold"),
                style.borders(sides="bottom", weight="2px", color="black")
            ],
            locations=loc.column_labels()
        )

        # Control row italic
        .tab_style(
            style=style.text(style="italic"),
            locations=loc.body(rows=[0], columns="Treatment")
        )

        # Significant p-values bold
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(rows=[1, 2, 4], columns="P_Formatted")
        )

        # Bottom border
        .tab_style(
            style=style.borders(sides="bottom", weight="2px", color="black"),
            locations=loc.body(rows=[-1])
        )

        # Footnotes
        .tab_footnote(
            footnote="Standard deviation",
            locations=loc.column_labels(columns="SD")
        )
        .tab_footnote(
            footnote="Standard error of the mean",
            locations=loc.column_labels(columns="SE")
        )

        .tab_source_note("*p<0.05, **p<0.01, ***p<0.001 vs. Control (Dunnett's test)")
        .tab_source_note("CI = Confidence Interval")

        .tab_options(
            table_font_names="Times New Roman, serif",
            table_font_size="12px"
        )
    )

    table.save(output_path)
    return table

# table = create_scientific_table("experiment_results.html")
```

## Integration Examples

### Great Tables with Streamlit

```python
import streamlit as st
from great_tables import GT
import pandas as pd

st.set_page_config(page_title="Table Demo", layout="wide")
st.title("Great Tables in Streamlit")

# Sample data
df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Gadget X"],
    "Price": [29.99, 49.99, 19.99],
    "Stock": [150, 85, 200],
    "Rating": [4.5, 4.2, 4.8]
})

# Create table
table = (
    GT(df)
    .tab_header(title="Product Catalog")
    .fmt_currency(columns="Price", currency="USD")
    .fmt_number(columns="Rating", decimals=1)
)

# Display in Streamlit
st.html(table.as_raw_html())
```

### Great Tables with Polars

```python
from great_tables import GT
import polars as pl

# Create Polars DataFrame
df_polars = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "score": [95, 87, 92],
    "grade": ["A", "B+", "A-"]
})

# Convert to pandas for Great Tables
df_pandas = df_polars.to_pandas()

# Create table
table = (
    GT(df_pandas)
    .tab_header(title="Student Scores")
    .cols_label(
        name="Student",
        score="Score",
        grade="Grade"
    )
)

table.save("polars_table.html")
```

## Best Practices

### 1. Keep Tables Focused

```python
# GOOD: Select relevant columns
df_display = df[["Name", "Revenue", "Growth"]]
table = GT(df_display)

# AVOID: Displaying too many columns
# table = GT(df)  # If df has 20+ columns
```

### 2. Use Appropriate Formatting

```python
# GOOD: Match format to data type
table = (
    GT(df)
    .fmt_currency(columns="Price", currency="USD")
    .fmt_percent(columns="Growth", decimals=1)
    .fmt_integer(columns="Units", use_seps=True)
)

# AVOID: Generic number format for everything
```

### 3. Limit Rows for Display

```python
# GOOD: Show summary or top N
df_top10 = df.nlargest(10, "Revenue")
table = GT(df_top10)

# AVOID: Displaying thousands of rows
```

### 4. Use Color Sparingly

```python
# GOOD: Highlight key information
table.data_color(
    columns="Performance",
    palette=["#fee2e2", "#dcfce7"],  # Subtle colors
    domain=[0, 100]
)

# AVOID: Rainbow color schemes
```

## Troubleshooting

### Common Issues

**Issue: Table not displaying in Jupyter**
```python
# Solution: Ensure rich display
from great_tables import GT
table = GT(df)
display(table)  # Or just: table
```

**Issue: HTML export looks different**
```python
# Solution: Include all styling
table.save("output.html")  # Includes CSS
```

**Issue: Image export not working**
```python
# Solution: Install webshot or use playwright
pip install webshot
# or
pip install playwright
playwright install chromium

table.save("output.png", web_driver="playwright")
```

**Issue: Slow with large DataFrames**
```python
# Solution: Limit rows
df_display = df.head(100)
table = GT(df_display)
```

**Issue: Special characters not rendering**
```python
# Solution: Use html() helper
from great_tables import html
cell_content = html("&euro; 100")  # Euro symbol
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic table creation and styling
  - Column formatting (currency, percent, date)
  - Conditional formatting and color scales
  - Row and column grouping
  - Footnotes and annotations
  - Export to HTML and images
  - Complete report examples
  - Integration with Streamlit and Polars
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://posit-dev.github.io/great-tables/
- **GitHub**: https://github.com/posit-dev/great-tables
- **PyPI**: https://pypi.org/project/great-tables/
- **Gallery**: https://posit-dev.github.io/great-tables/examples/

---

**Create publication-quality tables with Great Tables - beautiful data presentation made easy!**
