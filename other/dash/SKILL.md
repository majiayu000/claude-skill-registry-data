---
name: dash
version: 1.0.0
description: Build production-grade interactive dashboards with Plotly Dash - enterprise features, callbacks, and scalable deployment
author: workspace-hub
category: data-analysis
capabilities:
  - Production-ready dashboard development
  - Reactive callbacks for interactivity
  - Plotly visualization integration
  - Multi-page application architecture
  - Authentication and authorization
  - Enterprise deployment options
  - Custom components and extensions
tools:
  - dash
  - plotly
  - dash-bootstrap-components
  - dash-ag-grid
tags: [dash, dashboard, plotly, callbacks, enterprise, production, interactive, visualization]
platforms: [python, web]
related_skills:
  - plotly
  - streamlit
  - polars
  - pandas-data-processing
---

# Dash Production Dashboard Skill

Build enterprise-grade interactive dashboards with Plotly Dash. Features reactive callbacks, professional layouts, and scalable deployment for production workloads.

## When to Use This Skill

### USE Dash when:
- **Production dashboards** - Building dashboards for business users
- **Complex interactivity** - Need fine-grained control over updates
- **Enterprise requirements** - Authentication, scaling, reliability needed
- **Plotly ecosystem** - Already using Plotly for visualizations
- **Custom components** - Need to extend with JavaScript/React
- **Long-term projects** - Dashboard will be maintained and extended
- **Multi-user access** - Multiple concurrent users accessing dashboards

### DON'T USE Dash when:
- **Quick prototypes** - Use Streamlit for faster iteration
- **Simple visualizations** - Static reports may suffice
- **No interactivity needed** - Use static HTML/PDF reports
- **Limited Python knowledge** - Steeper learning curve than Streamlit
- **Single-user tools** - Jupyter notebooks may be simpler

## Prerequisites

```bash
# Basic installation
pip install dash

# With common extras
pip install dash plotly pandas dash-bootstrap-components

# Full installation
pip install dash plotly pandas polars dash-bootstrap-components dash-ag-grid gunicorn

# Using uv (recommended)
uv pip install dash plotly pandas dash-bootstrap-components dash-ag-grid
```

## Core Capabilities

### 1. Basic Application Structure

**Minimal Dash App:**
```python
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize app
app = Dash(__name__)

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "NYC", "NYC", "NYC"]
})

# Create figure
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Layout
app.layout = html.Div([
    html.H1("Hello Dash"),
    html.P("This is a simple Dash application."),
    dcc.Graph(id="example-graph", figure=fig)
])

# Run server
if __name__ == "__main__":
    app.run(debug=True)
```

**Run the app:**
```bash
python app.py
# Visit http://127.0.0.1:8050/
```

### 2. Callbacks and Interactivity

**Basic Callback:**
```python
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Sample data
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=100),
    "category": ["A", "B", "C", "D"] * 25,
    "value": range(100)
})

# Layout
app.layout = html.Div([
    html.H1("Interactive Dashboard"),

    html.Label("Select Category:"),
    dcc.Dropdown(
        id="category-dropdown",
        options=[{"label": c, "value": c} for c in df["category"].unique()],
        value="A",
        clearable=False
    ),

    dcc.Graph(id="line-chart")
])

# Callback
@callback(
    Output("line-chart", "figure"),
    Input("category-dropdown", "value")
)
def update_chart(selected_category):
    filtered_df = df[df["category"] == selected_category]

    fig = px.line(
        filtered_df,
        x="date",
        y="value",
        title=f"Values for Category {selected_category}"
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
```

**Multiple Inputs and Outputs:**
```python
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Sample data
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=365),
    "category": ["A", "B", "C"] * 122 + ["A"],
    "region": ["North", "South", "East", "West"] * 91 + ["North"],
    "value": [i + (i % 30) * 10 for i in range(365)]
})

app.layout = html.Div([
    html.H1("Multi-Input Dashboard"),

    html.Div([
        html.Div([
            html.Label("Category"),
            dcc.Dropdown(
                id="category-filter",
                options=[{"label": c, "value": c} for c in df["category"].unique()],
                value=["A", "B", "C"],
                multi=True
            )
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.Label("Region"),
            dcc.Dropdown(
                id="region-filter",
                options=[{"label": r, "value": r} for r in df["region"].unique()],
                value=["North", "South", "East", "West"],
                multi=True
            )
        ], style={"width": "45%", "display": "inline-block", "marginLeft": "5%"})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id="trend-chart")
        ], style={"width": "60%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="pie-chart")
        ], style={"width": "38%", "display": "inline-block", "marginLeft": "2%"})
    ]),

    html.Div(id="summary-stats")
])

@callback(
    [Output("trend-chart", "figure"),
     Output("pie-chart", "figure"),
     Output("summary-stats", "children")],
    [Input("category-filter", "value"),
     Input("region-filter", "value")]
)
def update_all(categories, regions):
    # Filter data
    filtered = df[
        (df["category"].isin(categories)) &
        (df["region"].isin(regions))
    ]

    # Trend chart
    trend = filtered.groupby("date")["value"].sum().reset_index()
    trend_fig = px.line(trend, x="date", y="value", title="Value Trend")

    # Pie chart
    by_category = filtered.groupby("category")["value"].sum().reset_index()
    pie_fig = px.pie(by_category, values="value", names="category", title="By Category")

    # Summary stats
    stats = html.Div([
        html.H4("Summary Statistics"),
        html.P(f"Total records: {len(filtered):,}"),
        html.P(f"Total value: {filtered['value'].sum():,}"),
        html.P(f"Average value: {filtered['value'].mean():.2f}")
    ])

    return trend_fig, pie_fig, stats

if __name__ == "__main__":
    app.run(debug=True)
```

**Chained Callbacks:**
```python
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

app = Dash(__name__)

# Hierarchical data
data = {
    "USA": {"California": ["San Francisco", "Los Angeles"], "Texas": ["Houston", "Dallas"]},
    "Canada": {"Ontario": ["Toronto", "Ottawa"], "Quebec": ["Montreal", "Quebec City"]}
}

app.layout = html.Div([
    html.H1("Chained Dropdowns"),

    html.Label("Country"),
    dcc.Dropdown(id="country-dropdown"),

    html.Label("State/Province"),
    dcc.Dropdown(id="state-dropdown"),

    html.Label("City"),
    dcc.Dropdown(id="city-dropdown"),

    html.Div(id="selection-output")
])

# Populate country dropdown
@callback(
    Output("country-dropdown", "options"),
    Input("country-dropdown", "id")  # Dummy input to trigger on load
)
def set_countries(_):
    return [{"label": c, "value": c} for c in data.keys()]

# Update state options based on country
@callback(
    Output("state-dropdown", "options"),
    Output("state-dropdown", "value"),
    Input("country-dropdown", "value")
)
def set_states(country):
    if country is None:
        return [], None
    states = data.get(country, {}).keys()
    return [{"label": s, "value": s} for s in states], None

# Update city options based on state
@callback(
    Output("city-dropdown", "options"),
    Output("city-dropdown", "value"),
    Input("country-dropdown", "value"),
    Input("state-dropdown", "value")
)
def set_cities(country, state):
    if country is None or state is None:
        return [], None
    cities = data.get(country, {}).get(state, [])
    return [{"label": c, "value": c} for c in cities], None

# Display selection
@callback(
    Output("selection-output", "children"),
    Input("country-dropdown", "value"),
    Input("state-dropdown", "value"),
    Input("city-dropdown", "value")
)
def display_selection(country, state, city):
    return f"Selected: {country or '-'} > {state or '-'} > {city or '-'}"

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. Layout Components

**HTML Components:**
```python
from dash import html

# Text elements
layout = html.Div([
    html.H1("Main Title"),
    html.H2("Subtitle"),
    html.H3("Section Header"),
    html.P("Paragraph text with ", html.Strong("bold"), " and ", html.Em("italic")),
    html.Hr(),  # Horizontal rule
    html.Br(),  # Line break

    # Lists
    html.Ul([
        html.Li("Item 1"),
        html.Li("Item 2"),
        html.Li("Item 3")
    ]),

    # Links
    html.A("Click here", href="https://example.com", target="_blank"),

    # Images
    html.Img(src="/assets/logo.png", style={"width": "200px"}),

    # Tables
    html.Table([
        html.Thead([
            html.Tr([html.Th("Name"), html.Th("Value")])
        ]),
        html.Tbody([
            html.Tr([html.Td("Item 1"), html.Td("100")]),
            html.Tr([html.Td("Item 2"), html.Td("200")])
        ])
    ])
])
```

**Core Components (dcc):**
```python
from dash import dcc

# Input components
components = html.Div([
    # Dropdown
    dcc.Dropdown(
        id="dropdown",
        options=[
            {"label": "Option A", "value": "a"},
            {"label": "Option B", "value": "b"},
            {"label": "Option C", "value": "c", "disabled": True}
        ],
        value="a",
        multi=False,
        clearable=True,
        searchable=True,
        placeholder="Select..."
    ),

    # Multi-select dropdown
    dcc.Dropdown(
        id="multi-dropdown",
        options=[{"label": f"Option {i}", "value": i} for i in range(10)],
        value=[1, 2, 3],
        multi=True
    ),

    # Slider
    dcc.Slider(
        id="slider",
        min=0,
        max=100,
        step=5,
        value=50,
        marks={0: "0", 25: "25", 50: "50", 75: "75", 100: "100"}
    ),

    # Range slider
    dcc.RangeSlider(
        id="range-slider",
        min=0,
        max=100,
        step=1,
        value=[20, 80],
        marks={i: str(i) for i in range(0, 101, 20)}
    ),

    # Input
    dcc.Input(
        id="text-input",
        type="text",
        placeholder="Enter text...",
        debounce=True  # Wait for typing to stop
    ),

    # Textarea
    dcc.Textarea(
        id="textarea",
        placeholder="Enter longer text...",
        style={"width": "100%", "height": "100px"}
    ),

    # Checklist
    dcc.Checklist(
        id="checklist",
        options=[
            {"label": "Option 1", "value": "1"},
            {"label": "Option 2", "value": "2"},
            {"label": "Option 3", "value": "3"}
        ],
        value=["1"],
        inline=True
    ),

    # Radio items
    dcc.RadioItems(
        id="radio",
        options=[
            {"label": "Small", "value": "s"},
            {"label": "Medium", "value": "m"},
            {"label": "Large", "value": "l"}
        ],
        value="m",
        inline=True
    ),

    # Date picker
    dcc.DatePickerSingle(
        id="date-picker",
        date="2025-01-01",
        display_format="YYYY-MM-DD"
    ),

    # Date range picker
    dcc.DatePickerRange(
        id="date-range",
        start_date="2025-01-01",
        end_date="2025-12-31",
        display_format="YYYY-MM-DD"
    ),

    # Upload
    dcc.Upload(
        id="upload",
        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center"
        }
    ),

    # Tabs
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Tab 1", value="tab-1"),
        dcc.Tab(label="Tab 2", value="tab-2")
    ]),

    # Loading indicator
    dcc.Loading(
        id="loading",
        type="default",  # default, graph, cube, circle, dot
        children=html.Div(id="loading-output")
    ),

    # Interval (for periodic updates)
    dcc.Interval(
        id="interval-component",
        interval=1000,  # milliseconds
        n_intervals=0
    ),

    # Store (client-side data storage)
    dcc.Store(id="data-store", storage_type="session"),  # memory, session, local

    # Graph
    dcc.Graph(
        id="graph",
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"]
        }
    )
])
```

### 4. Bootstrap Components

**Using Dash Bootstrap Components:**
```python
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Initialize with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=100),
    "sales": [100 + i * 2 + (i % 7) * 10 for i in range(100)],
    "orders": [50 + i + (i % 5) * 5 for i in range(100)]
})

# Layout with Bootstrap components
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Sales Dashboard", className="text-primary"),
            html.P("Interactive analytics powered by Dash", className="lead")
        ])
    ], className="mb-4"),

    # Metrics row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Sales", className="card-title"),
                    html.H2(f"${df['sales'].sum():,}", className="text-success")
                ])
            ])
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Orders", className="card-title"),
                    html.H2(f"{df['orders'].sum():,}", className="text-info")
                ])
            ])
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Order Value", className="card-title"),
                    html.H2(f"${df['sales'].sum() / df['orders'].sum():.2f}", className="text-warning")
                ])
            ])
        ], md=4)
    ], className="mb-4"),

    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    dbc.Label("Date Range"),
                    dcc.DatePickerRange(
                        id="date-range",
                        start_date=df["date"].min(),
                        end_date=df["date"].max(),
                        className="mb-3"
                    ),
                    dbc.Label("Metric"),
                    dcc.Dropdown(
                        id="metric-dropdown",
                        options=[
                            {"label": "Sales", "value": "sales"},
                            {"label": "Orders", "value": "orders"}
                        ],
                        value="sales"
                    )
                ])
            ])
        ], md=3),
        dbc.Col([
            dcc.Graph(id="main-chart")
        ], md=9)
    ]),

    # Tabs
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Daily Data", tab_id="daily"),
                dbc.Tab(label="Summary", tab_id="summary")
            ], id="tabs", active_tab="daily"),
            html.Div(id="tab-content", className="mt-3")
        ])
    ], className="mt-4")

], fluid=True)

@callback(
    Output("main-chart", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("metric-dropdown", "value")]
)
def update_chart(start_date, end_date, metric):
    filtered = df[
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ]

    fig = px.line(
        filtered,
        x="date",
        y=metric,
        title=f"{metric.title()} Over Time"
    )
    fig.update_layout(template="plotly_white")

    return fig

@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab(tab):
    if tab == "daily":
        return dbc.Table.from_dataframe(
            df.tail(10),
            striped=True,
            bordered=True,
            hover=True
        )
    elif tab == "summary":
        return html.Div([
            html.P(f"Total Records: {len(df)}"),
            html.P(f"Date Range: {df['date'].min()} to {df['date'].max()}"),
            html.P(f"Sales Range: ${df['sales'].min()} - ${df['sales'].max()}")
        ])

if __name__ == "__main__":
    app.run(debug=True)
```

### 5. Multi-Page Applications

**Project Structure:**
```
my_dash_app/
├── app.py              # Main entry point
├── pages/
│   ├── __init__.py
│   ├── home.py
│   ├── analytics.py
│   └── settings.py
├── components/
│   ├── __init__.py
│   ├── navbar.py
│   └── footer.py
├── utils/
│   ├── __init__.py
│   └── data.py
└── assets/
    ├── style.css
    └── logo.png
```

**Main App (app.py):**
```python
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
        dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
    ],
    brand="My Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)

# Layout with navigation and page container
app.layout = html.Div([
    navbar,
    dbc.Container([
        page_container
    ], fluid=True, className="mt-4")
])

if __name__ == "__main__":
    app.run(debug=True)
```

**Home Page (pages/home.py):**
```python
from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/", name="Home")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Welcome to the Dashboard"),
            html.P("Select a page from the navigation bar to get started."),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Quick Links"),
                    dbc.ListGroup([
                        dbc.ListGroupItem("Analytics", href="/analytics"),
                        dbc.ListGroupItem("Settings", href="/settings")
                    ])
                ])
            ])
        ])
    ])
])
```

**Analytics Page (pages/analytics.py):**
```python
from dash import html, dcc, callback, Output, Input, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

register_page(__name__, path="/analytics", name="Analytics")

# Generate sample data
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=365),
    "value": [100 + i + (i % 30) * 5 for i in range(365)]
})

layout = dbc.Container([
    html.H1("Analytics"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Chart Type"),
            dcc.Dropdown(
                id="chart-type",
                options=[
                    {"label": "Line", "value": "line"},
                    {"label": "Bar", "value": "bar"},
                    {"label": "Area", "value": "area"}
                ],
                value="line"
            )
        ], md=4)
    ], className="mb-4"),

    dcc.Graph(id="analytics-chart")
])

@callback(
    Output("analytics-chart", "figure"),
    Input("chart-type", "value")
)
def update_chart(chart_type):
    if chart_type == "line":
        fig = px.line(df, x="date", y="value")
    elif chart_type == "bar":
        monthly = df.resample("M", on="date")["value"].sum().reset_index()
        fig = px.bar(monthly, x="date", y="value")
    else:
        fig = px.area(df, x="date", y="value")

    return fig
```

### 6. Authentication

**Basic Authentication:**
```python
from dash import Dash, html, dcc
import dash_auth

app = Dash(__name__)

# Basic authentication
VALID_USERNAME_PASSWORD_PAIRS = {
    "admin": "admin123",
    "user": "user123"
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1("Protected Dashboard"),
    html.P("You are authenticated!")
])

if __name__ == "__main__":
    app.run(debug=True)
```

**Custom Login (with session):**
```python
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from flask import session

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server.secret_key = "your-secret-key-here"

# Login form
login_form = dbc.Card([
    dbc.CardBody([
        html.H4("Login"),
        dbc.Input(id="username", placeholder="Username", className="mb-2"),
        dbc.Input(id="password", type="password", placeholder="Password", className="mb-2"),
        dbc.Button("Login", id="login-btn", color="primary"),
        html.Div(id="login-message")
    ])
], style={"maxWidth": "400px", "margin": "100px auto"})

# Main content
main_content = html.Div([
    html.H1("Dashboard"),
    html.P("Welcome! You are logged in."),
    dbc.Button("Logout", id="logout-btn", color="secondary")
])

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if session.get("authenticated"):
        return main_content
    return login_form

@callback(
    [Output("login-message", "children"),
     Output("url", "pathname")],
    Input("login-btn", "n_clicks"),
    [State("username", "value"),
     State("password", "value")],
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    # Simple validation (use proper auth in production)
    if username == "admin" and password == "admin123":
        session["authenticated"] = True
        return "", "/"
    return dbc.Alert("Invalid credentials", color="danger"), "/"

@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    session.clear()
    return "/"

if __name__ == "__main__":
    app.run(debug=True)
```

## Complete Examples

### Example 1: Sales Analytics Dashboard

```python
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Generate sample data
np.random.seed(42)
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
n_days = len(dates)

df = pd.DataFrame({
    "date": dates,
    "revenue": np.cumsum(np.random.randn(n_days) * 100 + 500),
    "orders": np.random.poisson(100, n_days),
    "customers": np.random.poisson(80, n_days),
    "region": np.random.choice(["North", "South", "East", "West"], n_days),
    "category": np.random.choice(["Electronics", "Clothing", "Food", "Home"], n_days)
})

# Calculate previous period metrics
current_revenue = df[df["date"] >= "2025-01-01"]["revenue"].sum()
prev_revenue = df[df["date"] < "2025-01-01"]["revenue"].sum()
revenue_change = ((current_revenue - prev_revenue) / prev_revenue * 100)

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Sales Analytics Dashboard", className="text-primary mb-0"),
            html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", className="text-muted")
        ], md=8),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("Export", outline=True, color="primary"),
                dbc.Button("Refresh", outline=True, color="secondary")
            ])
        ], md=4, className="text-end")
    ], className="mb-4 mt-3"),

    # Date filter
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Date Range"),
                            dcc.DatePickerRange(
                                id="date-filter",
                                start_date="2025-01-01",
                                end_date="2025-12-31",
                                display_format="YYYY-MM-DD"
                            )
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Region"),
                            dcc.Dropdown(
                                id="region-filter",
                                options=[{"label": r, "value": r} for r in df["region"].unique()],
                                value=df["region"].unique().tolist(),
                                multi=True
                            )
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Category"),
                            dcc.Dropdown(
                                id="category-filter",
                                options=[{"label": c, "value": c} for c in df["category"].unique()],
                                value=df["category"].unique().tolist(),
                                multi=True
                            )
                        ], md=4)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),

    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Revenue", className="text-muted"),
                    html.H3(id="kpi-revenue", className="text-success"),
                    html.Small(id="kpi-revenue-change", className="text-muted")
                ])
            ], color="light")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Orders", className="text-muted"),
                    html.H3(id="kpi-orders", className="text-info"),
                    html.Small(id="kpi-orders-change", className="text-muted")
                ])
            ], color="light")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Unique Customers", className="text-muted"),
                    html.H3(id="kpi-customers", className="text-warning"),
                    html.Small(id="kpi-customers-change", className="text-muted")
                ])
            ], color="light")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg Order Value", className="text-muted"),
                    html.H3(id="kpi-aov", className="text-primary"),
                    html.Small(id="kpi-aov-change", className="text-muted")
                ])
            ], color="light")
        ], md=3)
    ], className="mb-4"),

    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Revenue Trend"),
                dbc.CardBody([
                    dcc.Graph(id="revenue-trend")
                ])
            ])
        ], md=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Revenue by Category"),
                dbc.CardBody([
                    dcc.Graph(id="category-pie")
                ])
            ])
        ], md=4)
    ], className="mb-4"),

    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Regional Performance"),
                dbc.CardBody([
                    dcc.Graph(id="regional-bar")
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Orders vs Customers"),
                dbc.CardBody([
                    dcc.Graph(id="scatter-chart")
                ])
            ])
        ], md=6)
    ], className="mb-4"),

    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Detailed Data"),
                dbc.CardBody([
                    html.Div(id="data-table")
                ])
            ])
        ])
    ])

], fluid=True)

# Callbacks
@callback(
    [Output("kpi-revenue", "children"),
     Output("kpi-orders", "children"),
     Output("kpi-customers", "children"),
     Output("kpi-aov", "children"),
     Output("revenue-trend", "figure"),
     Output("category-pie", "figure"),
     Output("regional-bar", "figure"),
     Output("scatter-chart", "figure"),
     Output("data-table", "children")],
    [Input("date-filter", "start_date"),
     Input("date-filter", "end_date"),
     Input("region-filter", "value"),
     Input("category-filter", "value")]
)
def update_dashboard(start_date, end_date, regions, categories):
    # Filter data
    filtered = df[
        (df["date"] >= start_date) &
        (df["date"] <= end_date) &
        (df["region"].isin(regions)) &
        (df["category"].isin(categories))
    ]

    # KPIs
    revenue = f"${filtered['revenue'].sum():,.0f}"
    orders = f"{filtered['orders'].sum():,}"
    customers = f"{filtered['customers'].sum():,}"
    aov = f"${filtered['revenue'].sum() / filtered['orders'].sum():.2f}" if filtered['orders'].sum() > 0 else "$0"

    # Revenue trend
    daily_revenue = filtered.groupby("date")["revenue"].sum().reset_index()
    trend_fig = px.line(
        daily_revenue,
        x="date",
        y="revenue",
        title=None
    )
    trend_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified"
    )

    # Category pie
    by_category = filtered.groupby("category")["revenue"].sum().reset_index()
    pie_fig = px.pie(
        by_category,
        values="revenue",
        names="category",
        title=None
    )
    pie_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    # Regional bar
    by_region = filtered.groupby("region").agg({
        "revenue": "sum",
        "orders": "sum"
    }).reset_index()
    bar_fig = px.bar(
        by_region,
        x="region",
        y="revenue",
        color="region",
        title=None
    )
    bar_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    # Scatter
    scatter_fig = px.scatter(
        filtered.groupby("date").agg({"orders": "sum", "customers": "sum"}).reset_index(),
        x="orders",
        y="customers",
        title=None,
        trendline="ols"
    )
    scatter_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    # Table
    table = dbc.Table.from_dataframe(
        filtered.groupby(["region", "category"]).agg({
            "revenue": "sum",
            "orders": "sum",
            "customers": "sum"
        }).reset_index().round(2),
        striped=True,
        bordered=True,
        hover=True,
        responsive=True
    )

    return revenue, orders, customers, aov, trend_fig, pie_fig, bar_fig, scatter_fig, table

if __name__ == "__main__":
    app.run(debug=True)
```

### Example 2: Real-Time Monitoring Dashboard

```python
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from collections import deque
import random
from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Initialize data stores
MAX_POINTS = 50
time_data = deque(maxlen=MAX_POINTS)
cpu_data = deque(maxlen=MAX_POINTS)
memory_data = deque(maxlen=MAX_POINTS)
network_data = deque(maxlen=MAX_POINTS)

# Layout
app.layout = dbc.Container([
    html.H1("Real-Time System Monitor", className="text-center my-4"),

    # Status indicators
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("CPU Usage"),
                    html.H2(id="cpu-value", className="text-info"),
                    dbc.Progress(id="cpu-progress", value=0, max=100)
                ])
            ])
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Memory Usage"),
                    html.H2(id="memory-value", className="text-warning"),
                    dbc.Progress(id="memory-progress", value=0, max=100)
                ])
            ])
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Network I/O"),
                    html.H2(id="network-value", className="text-success"),
                    dbc.Progress(id="network-progress", value=0, max=100)
                ])
            ])
        ], md=4)
    ], className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("System Metrics (Last 50 Updates)"),
                dbc.CardBody([
                    dcc.Graph(id="live-graph", animate=True)
                ])
            ])
        ])
    ]),

    # Interval component for updates
    dcc.Interval(
        id="interval-component",
        interval=1000,  # 1 second
        n_intervals=0
    )
], fluid=True)

@callback(
    [Output("cpu-value", "children"),
     Output("memory-value", "children"),
     Output("network-value", "children"),
     Output("cpu-progress", "value"),
     Output("memory-progress", "value"),
     Output("network-progress", "value"),
     Output("live-graph", "figure")],
    Input("interval-component", "n_intervals")
)
def update_metrics(n):
    # Simulate metrics
    cpu = random.uniform(20, 80)
    memory = random.uniform(40, 90)
    network = random.uniform(10, 60)

    # Update data stores
    time_data.append(datetime.now())
    cpu_data.append(cpu)
    memory_data.append(memory)
    network_data.append(network)

    # Create figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(time_data),
        y=list(cpu_data),
        name="CPU",
        mode="lines",
        line=dict(color="#17a2b8")
    ))

    fig.add_trace(go.Scatter(
        x=list(time_data),
        y=list(memory_data),
        name="Memory",
        mode="lines",
        line=dict(color="#ffc107")
    ))

    fig.add_trace(go.Scatter(
        x=list(time_data),
        y=list(network_data),
        name="Network",
        mode="lines",
        line=dict(color="#28a745")
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[0, 100], title="Usage %"),
        xaxis=dict(title="Time"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=50, r=20, t=30, b=50),
        uirevision="constant"  # Preserve zoom/pan on update
    )

    return (
        f"{cpu:.1f}%",
        f"{memory:.1f}%",
        f"{network:.1f}%",
        cpu,
        memory,
        network,
        fig
    )

if __name__ == "__main__":
    app.run(debug=True)
```

### Example 3: Data Table with AG Grid

```python
from dash import Dash, html, callback, Output, Input
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Generate sample data
np.random.seed(42)
df = pd.DataFrame({
    "ID": range(1, 1001),
    "Name": [f"Product {i}" for i in range(1, 1001)],
    "Category": np.random.choice(["Electronics", "Clothing", "Food", "Home"], 1000),
    "Price": np.random.uniform(10, 500, 1000).round(2),
    "Stock": np.random.randint(0, 100, 1000),
    "Rating": np.random.uniform(1, 5, 1000).round(1),
    "Last Updated": pd.date_range("2025-01-01", periods=1000, freq="H")
})

# Column definitions
column_defs = [
    {"field": "ID", "filter": "agNumberColumnFilter", "width": 80},
    {"field": "Name", "filter": "agTextColumnFilter"},
    {
        "field": "Category",
        "filter": "agSetColumnFilter",
        "cellStyle": {"fontWeight": "bold"}
    },
    {
        "field": "Price",
        "filter": "agNumberColumnFilter",
        "valueFormatter": {"function": "'$' + params.value.toFixed(2)"},
        "cellStyle": {
            "function": "params.value > 300 ? {'color': 'red'} : {'color': 'green'}"
        }
    },
    {
        "field": "Stock",
        "filter": "agNumberColumnFilter",
        "cellStyle": {
            "function": "params.value < 10 ? {'backgroundColor': '#ffcccc'} : {}"
        }
    },
    {
        "field": "Rating",
        "filter": "agNumberColumnFilter",
        "cellRenderer": "agSparklineCellRenderer",
        "cellRendererParams": {
            "sparklineOptions": {
                "type": "bar",
                "fill": "#5470c6"
            }
        }
    },
    {
        "field": "Last Updated",
        "filter": "agDateColumnFilter",
        "valueFormatter": {"function": "new Date(params.value).toLocaleDateString()"}
    }
]

# Layout
app.layout = dbc.Container([
    html.H1("Product Inventory", className="my-4"),

    dbc.Row([
        dbc.Col([
            dbc.Input(
                id="search-input",
                placeholder="Quick search...",
                className="mb-3"
            )
        ], md=4),
        dbc.Col([
            dbc.Button("Export CSV", id="export-btn", color="primary")
        ], md=2)
    ]),

    dag.AgGrid(
        id="inventory-grid",
        columnDefs=column_defs,
        rowData=df.to_dict("records"),
        defaultColDef={
            "sortable": True,
            "filter": True,
            "resizable": True,
            "floatingFilter": True
        },
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "rowSelection": "multiple",
            "animateRows": True
        },
        style={"height": "600px"}
    ),

    html.Div(id="selection-output", className="mt-3")
], fluid=True)

@callback(
    Output("inventory-grid", "dashGridOptions"),
    Input("search-input", "value")
)
def update_search(search_value):
    return {
        "pagination": True,
        "paginationPageSize": 20,
        "rowSelection": "multiple",
        "animateRows": True,
        "quickFilterText": search_value
    }

@callback(
    Output("selection-output", "children"),
    Input("inventory-grid", "selectedRows")
)
def display_selection(selected):
    if selected:
        return dbc.Alert(
            f"Selected {len(selected)} items. Total value: ${sum(r['Price'] for r in selected):,.2f}",
            color="info"
        )
    return ""

if __name__ == "__main__":
    app.run(debug=True)
```

## Deployment Patterns

### Gunicorn Production Server

```python
# wsgi.py
from app import app

server = app.server

if __name__ == "__main__":
    server.run()
```

```bash
# Run with Gunicorn
gunicorn wsgi:server -b 0.0.0.0:8050 -w 4
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["gunicorn", "wsgi:server", "-b", "0.0.0.0:8050", "-w", "4"]
```

```yaml
# docker-compose.yml
version: "3.8"
services:
  dash:
    build: .
    ports:
      - "8050:8050"
    environment:
      - DASH_DEBUG=false
    restart: unless-stopped
```

### Cloud Deployment (Heroku)

```txt
# Procfile
web: gunicorn wsgi:server

# requirements.txt
dash>=2.14.0
dash-bootstrap-components>=1.5.0
plotly>=5.18.0
pandas>=2.0.0
gunicorn>=21.0.0
```

## Best Practices

### 1. Optimize Callback Performance

```python
# Use prevent_initial_call when appropriate
@callback(
    Output("output", "children"),
    Input("button", "n_clicks"),
    prevent_initial_call=True
)
def handle_click(n_clicks):
    return f"Clicked {n_clicks} times"

# Use State for non-triggering inputs
@callback(
    Output("output", "children"),
    Input("submit-btn", "n_clicks"),
    State("input-field", "value")  # Doesn't trigger callback
)
def submit_form(n_clicks, value):
    return f"Submitted: {value}"
```

### 2. Efficient Data Loading

```python
# Cache expensive computations
from flask_caching import Cache

cache = Cache(app.server, config={"CACHE_TYPE": "simple"})

@cache.memoize(timeout=300)
def load_data():
    return pd.read_parquet("large_file.parquet")
```

### 3. Modular Callbacks

```python
# Separate callbacks into modules
# callbacks/analytics.py
from dash import callback, Output, Input

def register_callbacks(app):
    @callback(
        Output("chart", "figure"),
        Input("dropdown", "value")
    )
    def update_chart(value):
        return create_figure(value)
```

### 4. Error Handling

```python
from dash import callback, Output, Input
from dash.exceptions import PreventUpdate

@callback(
    Output("output", "children"),
    Input("input", "value")
)
def safe_callback(value):
    if value is None:
        raise PreventUpdate

    try:
        result = process(value)
        return result
    except Exception as e:
        return html.Div(f"Error: {str(e)}", className="text-danger")
```

## Troubleshooting

### Common Issues

**Issue: Callback not firing**
```python
# Check component IDs match exactly
# Verify Input/Output/State decorators
# Check for circular dependencies
```

**Issue: Slow initial load**
```python
# Use loading states
dcc.Loading(
    children=[dcc.Graph(id="graph")],
    type="circle"
)
```

**Issue: Memory leaks**
```python
# Clear caches periodically
# Use background callbacks for long operations
# Limit data in client-side stores
```

**Issue: Multiple callback outputs**
```python
# Use allow_duplicate=True for same output
@callback(
    Output("output", "children", allow_duplicate=True),
    Input("button2", "n_clicks"),
    prevent_initial_call=True
)
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Core application structure
  - Callbacks and interactivity
  - Layout components (HTML, DCC, Bootstrap)
  - Multi-page applications
  - Authentication patterns
  - Complete dashboard examples
  - Real-time monitoring example
  - AG Grid integration
  - Deployment patterns
  - Best practices and troubleshooting

## Resources

- **Official Docs**: https://dash.plotly.com/
- **Components**: https://dash.plotly.com/dash-core-components
- **Bootstrap Components**: https://dash-bootstrap-components.opensource.faculty.ai/
- **AG Grid**: https://dash.plotly.com/dash-ag-grid
- **Enterprise**: https://plotly.com/dash/
- **GitHub**: https://github.com/plotly/dash

---

**Build enterprise-grade interactive dashboards with Python and Plotly!**
