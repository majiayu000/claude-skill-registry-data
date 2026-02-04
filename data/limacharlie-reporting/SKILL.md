---
name: limacharlie-reporting
description: Use this skill when users need interactive HTML reports, dashboards, charts, or visualizations for LimaCharlie data. You generate the HTML, this skill serves it on localhost.
---

# LimaCharlie Reporting Skill

## Overview

This skill lets you create rich, interactive HTML reports that open in a browser instead of displaying in the terminal. **You generate whatever HTML you want** - tables, charts, dashboards, visualizations - and this skill serves it on localhost.

## When to Use This Skill

Use this when users want:
- Visual reports, dashboards, or charts
- Billing analysis with graphs
- Interactive tables with sorting/filtering
- MITRE ATT&CK coverage heatmaps
- Any data visualization that's better in a browser than text

## How It Works

**Three simple steps:**

1. **You generate HTML** (with any charts, tables, styling you want)
2. **Call `create_and_serve_report(html)`** - This spawns Python's `http.server` as a background subprocess
3. **User opens the localhost URL in their browser**

The implementation uses Python's built-in `http.server` module running as a subprocess, serving files directly from `/tmp`. This approach is simple, reliable, and requires no complex threading or process management. You have complete freedom to generate whatever HTML makes sense.

## Basic Usage

```python
import sys
sys.path.insert(0, '/full/path/to/skills/limacharlie-reporting')

from lib import create_and_serve_report

# Generate your HTML however you want
html = """
<h1>My Report</h1>
<p>Some analysis here...</p>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td>Sensors</td><td>45</td></tr>
  <tr><td>Cost</td><td>$1,234</td></tr>
</table>
"""

# Serve it
url = create_and_serve_report(html, title="My Report")
print(f"\nReport ready: {url}")
```

The URL will be something like `http://localhost:8080/report-abc123.html`.

## Adding Charts with Chart.js

Chart.js is a simple, popular charting library. Here's how to use it:

```python
html = """
<h1>Billing Trend</h1>
<canvas id="myChart" width="400" height="200"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
const ctx = document.getElementById('myChart');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [{
      label: 'Monthly Cost ($)',
      data: [800, 950, 1100, 1234],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Cost Trend'
      }
    }
  }
});
</script>
"""

url = create_and_serve_report(html, title="Billing Dashboard")
```

**Chart.js Quick Reference:**
- **Line charts**: `type: 'line'`
- **Bar charts**: `type: 'bar'`
- **Pie/Donut**: `type: 'pie'` or `type: 'doughnut'`
- Docs: https://www.chartjs.org/docs/latest/

## Creating Interactive Tables

For sortable, filterable tables, you can generate simple HTML tables or use libraries like DataTables:

```python
# Simple HTML table (users can still sort/filter in browser with Ctrl+F)
html = """
<h1>Sensor Inventory</h1>
<table border="1" style="width:100%; border-collapse: collapse;">
  <thead>
    <tr style="background: #f0f0f0;">
      <th>Hostname</th>
      <th>Platform</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>web-01</td><td>linux</td><td>online</td></tr>
    <tr><td>db-01</td><td>linux</td><td>online</td></tr>
    <tr><td>win-dc01</td><td>windows</td><td>offline</td></tr>
  </tbody>
</table>
"""

url = create_and_serve_report(html, title="Sensors")
```

## Styling Your Reports

You can include CSS inline or link to frameworks:

```python
html = """
<style>
  .metric-card {
    display: inline-block;
    padding: 20px;
    margin: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    text-align: center;
  }
  .metric-value {
    font-size: 2em;
    font-weight: bold;
  }
</style>

<h1>Overview</h1>
<div class="metric-card">
  <div class="metric-value">$1,234</div>
  <div>Total Cost</div>
</div>
<div class="metric-card">
  <div class="metric-value">45</div>
  <div>Active Sensors</div>
</div>
"""

url = create_and_serve_report(html, title="Dashboard")
```

## Using Other Visualization Libraries

You can use any JavaScript library from a CDN:

- **ApexCharts**: Modern, interactive charts - https://apexcharts.com/
- **Plotly**: Scientific/statistical visualizations - https://plotly.com/javascript/
- **ECharts**: Rich enterprise charts - https://echarts.apache.org/
- **D3.js**: Custom data visualizations - https://d3js.org/

Just include the CDN script tag and use the library's API in your HTML.

## API Reference

### `create_and_serve_report(html_content, title="Report", filename=None, wrap=True, include_chart_js=False)`

**Parameters:**
- `html_content` (str): Your HTML content
- `title` (str): Page title (used if wrap=True)
- `filename` (str, optional): Custom filename (e.g., "billing" → "billing.html")
- `wrap` (bool): If True, wraps content in minimal HTML template. If False, uses content as complete HTML document.
- `include_chart_js` (bool): If True (and wrap=True), automatically includes Chart.js CDN script

**Returns:**
- (str): URL where report can be accessed (e.g., `http://localhost:8080/report-abc123.html`)

### Helper: `wrap_html(content, title, include_chart_js=False)`

Wraps your content in a minimal HTML document with basic styling. Called automatically if `wrap=True` in `create_and_serve_report`.

## Complete Example: Billing Report

```python
import sys
sys.path.insert(0, '/full/path/to/skills/limacharlie-reporting')

from lib import create_and_serve_report

# Assume we fetched billing data from LimaCharlie MCP
total_cost = 1234.56
services = [
    {'name': 'Detection & Response', 'cost': 500.00},
    {'name': 'Artifact Collection', 'cost': 300.00},
    {'name': 'Outputs', 'cost': 434.56}
]

# Generate HTML with inline Chart.js
html = f"""
<h1>Billing Dashboard</h1>
<p>Current billing cycle: <strong>${total_cost:,.2f}</strong></p>

<h2>Cost by Service</h2>
<canvas id="costChart" width="400" height="200"></canvas>

<h2>Service Breakdown</h2>
<table border="1" style="width:100%; border-collapse: collapse;">
  <thead>
    <tr style="background: #f0f0f0;">
      <th>Service</th>
      <th>Cost</th>
    </tr>
  </thead>
  <tbody>
    {''.join(f'<tr><td>{s["name"]}</td><td>${s["cost"]:,.2f}</td></tr>' for s in services)}
  </tbody>
</table>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('costChart'), {{
  type: 'doughnut',
  data: {{
    labels: {[s['name'] for s in services]},
    datasets: [{{
      data: {[s['cost'] for s in services]},
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{
      title: {{ display: true, text: 'Cost Distribution' }}
    }}
  }}
}});
</script>
"""

url = create_and_serve_report(html, title="Billing Report")
print(f"\n✅ Billing report ready: {url}")
```

## Best Practices

1. **Keep it simple**: Generate clean HTML, don't over-engineer
2. **Use CDNs**: Link to Chart.js, Plotly, etc. from CDN (no local dependencies)
3. **Inline styles**: Put CSS in `<style>` tags for self-contained reports
4. **Test in browser**: Open the URL to verify charts render correctly
5. **Progressive enhancement**: Start with basic HTML tables, add charts if needed

## Troubleshooting

**Port already in use:**
- The server tries ports 8080-8090
- If all are busy, you'll get an error
- Solution: Close other local servers or check `lsof -i :8080-8090`

**Charts not rendering:**
- Check browser console for JavaScript errors
- Verify CDN scripts are loading (requires internet connection)
- Ensure Chart.js script loads before your chart code

**Report URL doesn't open:**
- Server prints "Report server started at http://localhost:PORT"
- If you don't see this, check for errors in Python execution
- Try the URL manually in a browser

## See Also

- **EXAMPLES.md**: Real-world report examples
- **REFERENCE.md**: Advanced techniques and tips
