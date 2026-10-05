---
name: plotly
version: 1.0.0
description: Create interactive scientific and analytical charts with Plotly (JavaScript & Python)
author: workspace-hub
category: data-visualization
tags: [charts, plotly, scientific, 3d, interactive, python, javascript]
platforms: [web, python, r]
---

# Plotly Interactive Visualization Skill

Create professional, interactive charts with 40+ chart types including 3D plots, statistical graphs, and scientific visualizations.

## When to Use This Skill

Use Plotly when you need:
- **Scientific visualizations** - 3D plots, contours, heatmaps
- **Statistical charts** - Box plots, violin plots, histograms
- **Large datasets** - Efficient rendering of 100k+ points with WebGL
- **Python/R integration** - Seamless integration with data science workflows
- **Quick interactive plots** - High-level API with sensible defaults
- **Dashboards** - Interactive dashboards with Plotly Dash

**Avoid when:**
- Maximum customization needed (use D3.js)
- Extremely simple charts (use Chart.js)
- File size is critical concern

## Core Capabilities

### 1. JavaScript Implementation

#### Basic Line Chart
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
</head>
<body>
  <div id="chart"></div>
  <script>
    const trace = {
      x: [1, 2, 3, 4, 5],
      y: [10, 15, 13, 17, 20],
      type: 'scatter',
      mode: 'lines+markers',
      marker: { color: 'rgb(219, 64, 82)', size: 12 },
      line: { color: 'rgb(55, 128, 191)', width: 3 }
    };

    const layout = {
      title: 'Interactive Line Chart',
      xaxis: { title: 'X Axis' },
      yaxis: { title: 'Y Axis' },
      hovermode: 'closest'
    };

    Plotly.newPlot('chart', [trace], layout, {
      responsive: true,
      displayModeBar: true
    });
  </script>
</body>
</html>
```

#### Multiple Traces
```javascript
const trace1 = {
  x: [1, 2, 3, 4, 5],
  y: [1, 6, 3, 6, 8],
  type: 'scatter',
  mode: 'lines',
  name: 'Series 1'
};

const trace2 = {
  x: [1, 2, 3, 4, 5],
  y: [5, 1, 6, 9, 2],
  type: 'scatter',
  mode: 'lines+markers',
  name: 'Series 2'
};

const layout = {
  title: 'Multi-Series Chart',
  showlegend: true,
  legend: { x: 1, y: 1 }
};

Plotly.newPlot('chart', [trace1, trace2], layout);
```

### 2. Python Implementation

#### Quick Start with Plotly Express
```python
import plotly.express as px
import pandas as pd

# Load data from CSV
df = pd.read_csv('../data/processed/results.csv')

# Create interactive scatter plot
fig = px.scatter(
    df,
    x='time',
    y='value',
    color='category',
    size='magnitude',
    hover_data=['additional_info'],
    title='Interactive Analysis Results'
)

# Customize layout
fig.update_layout(
    template='plotly_white',
    hovermode='x unified',
    height=600,
    font=dict(size=12)
)

# Save as HTML
fig.write_html('../reports/analysis_plot.html')

# Or display in Jupyter
fig.show()
```

#### Plotly Graph Objects (More Control)
```python
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('../data/processed/timeseries.csv')

fig = go.Figure()

# Add trace
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['value'],
    mode='lines+markers',
    name='Value',
    line=dict(color='rgb(55, 128, 191)', width=2),
    marker=dict(size=8, color='rgb(219, 64, 82)'),
    hovertemplate='<b>Date</b>: %{x}<br>' +
                  '<b>Value</b>: %{y:.2f}<br>' +
                  '<extra></extra>'
))

# Update layout
fig.update_layout(
    title='Time Series Analysis',
    xaxis_title='Date',
    yaxis_title='Value',
    template='plotly_dark',
    hovermode='x unified'
)

fig.write_html('../reports/timeseries.html')
```

## Complete Examples

### Example 1: 3D Scatter Plot
```python
import plotly.express as px
import numpy as np

# Generate 3D data
n = 500
x = np.random.randn(n)
y = np.random.randn(n)
z = np.random.randn(n)
colors = np.random.rand(n)

fig = px.scatter_3d(
    x=x, y=y, z=z,
    color=colors,
    size=np.abs(z) * 10,
    title='Interactive 3D Scatter Plot',
    labels={'x': 'X Axis', 'y': 'Y Axis', 'z': 'Z Axis'}
)

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig.write_html('../reports/3d_scatter.html')
```

### Example 2: Statistical Box Plot with Violin
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

df = pd.read_csv('../data/processed/measurements.csv')

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Box Plot', 'Violin Plot')
)

# Box plot
fig.add_trace(
    go.Box(y=df['value'], name='Box', boxmean='sd'),
    row=1, col=1
)

# Violin plot
fig.add_trace(
    go.Violin(y=df['value'], name='Violin', box_visible=True, meanline_visible=True),
    row=1, col=2
)

fig.update_layout(
    title_text='Statistical Distribution Analysis',
    showlegend=False,
    height=500
)

fig.write_html('../reports/statistical_analysis.html')
```

### Example 3: Animated Time Series
```python
import plotly.express as px
import pandas as pd

df = pd.read_csv('../data/processed/timeseries_multi.csv')

fig = px.line(
    df,
    x='date',
    y='value',
    color='category',
    animation_frame='year',
    animation_group='category',
    title='Animated Time Series by Category',
    range_y=[0, df['value'].max() * 1.1]
)

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Value',
    hovermode='x unified'
)

fig.write_html('../reports/animated_timeseries.html')
```

### Example 4: Interactive Heatmap with Annotations
```python
import plotly.graph_objects as go
import numpy as np

# Generate correlation matrix
data = np.random.rand(10, 10)
labels = [f'Var {i+1}' for i in range(10)]

fig = go.Figure(data=go.Heatmap(
    z=data,
    x=labels,
    y=labels,
    colorscale='Viridis',
    text=np.round(data, 2),
    texttemplate='%{text}',
    textfont={"size": 10},
    hovertemplate='%{y} vs %{x}<br>Value: %{z:.3f}<extra></extra>'
))

fig.update_layout(
    title='Correlation Heatmap',
    xaxis_title='Variables',
    yaxis_title='Variables',
    width=700,
    height=700
)

fig.write_html('../reports/heatmap.html')
```

### Example 5: Multi-Axis Chart
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Temperature (primary y-axis)
fig.add_trace(
    go.Scatter(x=[1, 2, 3, 4, 5], y=[20, 22, 25, 23, 24],
               name="Temperature (°C)", mode='lines+markers'),
    secondary_y=False,
)

# Humidity (secondary y-axis)
fig.add_trace(
    go.Scatter(x=[1, 2, 3, 4, 5], y=[65, 70, 60, 75, 68],
               name="Humidity (%)", mode='lines+markers'),
    secondary_y=True,
)

fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
fig.update_yaxes(title_text="Humidity (%)", secondary_y=True)

fig.update_layout(title_text="Multi-Axis Chart", hovermode='x unified')

fig.write_html('../reports/multi_axis.html')
```

### Example 6: Large Dataset with WebGL
```python
import plotly.graph_objects as go
import numpy as np

# Generate large dataset (100,000 points)
n = 100000
x = np.random.randn(n)
y = np.random.randn(n)

# Use Scattergl for performance
fig = go.Figure(data=go.Scattergl(
    x=x,
    y=y,
    mode='markers',
    marker=dict(
        size=2,
        color=np.random.randn(n),
        colorscale='Viridis',
        showscale=True
    )
))

fig.update_layout(
    title='Large Dataset (100k points) with WebGL',
    xaxis_title='X',
    yaxis_title='Y'
)

fig.write_html('../reports/large_dataset.html')
```

## Dashboard with Plotly Dash

```python
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('../data/processed/dashboard_data.csv')

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Interactive Dashboard'),

    html.Div([
        html.Label('Select Category:'),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
            value=df['category'].unique()[0]
        )
    ], style={'width': '50%'}),

    dcc.Graph(id='main-chart'),
    dcc.Graph(id='histogram')
])

# Callbacks
@app.callback(
    [Output('main-chart', 'figure'),
     Output('histogram', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_charts(selected_category):
    filtered_df = df[df['category'] == selected_category]

    # Line chart
    line_fig = px.line(
        filtered_df,
        x='date',
        y='value',
        title=f'Trend for {selected_category}'
    )

    # Histogram
    hist_fig = px.histogram(
        filtered_df,
        x='value',
        nbins=30,
        title=f'Distribution for {selected_category}'
    )

    return line_fig, hist_fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Best Practices

### 1. Use Plotly Express for Quick Plots
```python
# Simple and readable
fig = px.scatter(df, x='x', y='y', color='category', title='Quick Scatter')
```

### 2. Graph Objects for Complex Customization
```python
# More control
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='markers'))
fig.update_layout(title='Custom Chart')
```

### 3. Optimize for Large Datasets
```python
# Use Scattergl for >10k points
fig = go.Figure(data=go.Scattergl(x=x, y=y, mode='markers'))
```

### 4. Responsive Design
```python
fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=20)
)
```

### 5. Custom Hover Templates
```python
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)
```

## Chart Types Available

### Basic Charts
- Line, Scatter, Bar, Histogram, Box, Violin

### Scientific Charts
- Contour, Heatmap, 3D Surface, 3D Scatter, Streamline

### Financial Charts
- Candlestick, OHLC, Waterfall, Funnel

### Statistical Charts
- Box, Violin, Histogram, Density Heatmap, 2D Histogram

### Maps
- Scatter Mapbox, Choropleth, Density Mapbox

### 3D Charts
- 3D Scatter, 3D Line, 3D Surface, 3D Mesh

## Installation

### JavaScript (CDN)
```html
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
```

### Python
```bash
pip install plotly
# or
uv pip install plotly

# For Dash
pip install dash
```

### R
```r
install.packages("plotly")
```

## Performance Tips

1. **Use WebGL for large datasets** - Scattergl, Scattermapbox
2. **Limit animation frames** - Keep under 50 frames
3. **Simplify traces** - Reduce number of data points for complex charts
4. **Disable hover** - For static exports: `hovermode=False`
5. **Optimize layout updates** - Batch updates when possible

## Export Options

### HTML (Recommended for Reports)
```python
fig.write_html('report.html', include_plotlyjs='cdn')
```

### Static Images
```python
# Requires kaleido
fig.write_image('chart.png', width=1200, height=800)
fig.write_image('chart.pdf')
fig.write_image('chart.svg')
```

### JSON
```python
import json
fig.write_json('chart.json')
```

## Integration Examples

### With Pandas
```python
import plotly.express as px
df = pd.read_csv('data.csv')
fig = px.line(df, x='date', y='value')
```

### With NumPy
```python
import numpy as np
import plotly.graph_objects as go

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = go.Figure(data=go.Scatter(x=x, y=y))
```

### With Jupyter Notebooks
```python
# Automatically displays in cell output
fig.show()

# Or use widget mode
import plotly.graph_objects as go
fig = go.FigureWidget()
```

## Resources

- **Official Docs**: https://plotly.com/python/
- **JavaScript Docs**: https://plotly.com/javascript/
- **Dash Docs**: https://dash.plotly.com/
- **Gallery**: https://plotly.com/python/plotly-express/
- **GitHub**: https://github.com/plotly/plotly.py

## Theming

### Built-in Templates
```python
# Available templates: plotly, plotly_white, plotly_dark, ggplot2, seaborn, simple_white
fig.update_layout(template='plotly_dark')
```

### Custom Theme
```python
custom_template = go.layout.Template(
    layout=dict(
        font=dict(family='Arial', size=14),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='white'
    )
)

fig.update_layout(template=custom_template)
```

---

**Use this skill for professional, interactive scientific and analytical visualizations with minimal code!**
