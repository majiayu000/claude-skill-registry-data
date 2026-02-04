---
name: notebooks-front-end
description: Use when editing docs/index.html, creating charts with Plot, adding SQL cells, loading data with FileAttachment, or building visualizations. Triggers on any editing of docs/index.html, Observable notebooks, or front-end visualization work.
---

# Observable Notebook Kit 2.0

Data Desk notebooks use Observable Notebook Kit 2.0 - standalone HTML pages with embedded JavaScript that compile to static sites.

## Cell types

```html
<!doctype html>
<notebook theme="midnight">
  <title>Research title</title>

  <!-- Markdown -->
  <script id="header" type="text/markdown">
    # Research title
  </script>

  <!-- JavaScript -->
  <script id="analysis" type="module">
    const data = await FileAttachment("../data/flows.csv").csv({typed: true});
    display(Inputs.table(data));
  </script>

  <!-- SQL (queries DuckDB) -->
  <script id="flows" output="flows" type="application/sql" database="../data/data.duckdb" hidden>
    SELECT * FROM flows ORDER BY date DESC
  </script>

  <!-- Raw HTML -->
  <script id="chart" type="text/html">
    <div id="map" style="height: 500px;"></div>
  </script>
</notebook>
```

**Key points:**
- Each `<script>` has unique `id`
- Cells are `type="module"` by default (ES6 syntax)
- Use `display()` to render output (don't rely on return values)
- Variables defined in one cell available to all others
- Use **sentence case** for all titles, headings, and chart titles (e.g., "Outages by country" not "Outages By Country")
- **Keep the "last updated" date element** - this is auto-populated from git and should not be removed

## Loading data

### FileAttachment API

Paths relative to notebook (`docs/index.html`):
- Data files in root `data/` → use `../data/`
- Assets in `docs/assets/` → use `assets/`
- Always `await` FileAttachment calls

```javascript
// CSV with type inference
const flows = await FileAttachment("../data/flows.csv").csv({typed: true});

// JSON
const projects = await FileAttachment("../data/projects.json").json();

// Parquet
const tracks = await FileAttachment("../data/tracks.parquet").parquet();

// Images
const img = await FileAttachment("assets/photo.jpg").url();
```

### DuckDB / SQL cells (preferred for data)

**Always prefer SQL cells with a DuckDB database** over loading CSV/JSON directly. SQL cells query at build time, embedding results in HTML.

```html
<script id="query" output="flows" type="application/sql" database="../data/data.duckdb" hidden>
  SELECT * FROM flows WHERE year >= 2020
</script>
```

**Attributes:**
- `type="application/sql"` - marks as SQL query
- `database="../data/data.duckdb"` - path to database (relative to notebook)
- `output="flows"` - variable name for results
- `hidden` - don't display output (optional)

Results available as JS variable:
```javascript
display(html`<p>Found ${flows.length} flows</p>`);
```

### DuckDB client (for complex/dynamic queries)

```javascript
const db = DuckDBClient.of();
const summary = await db.query(`
  SELECT year, count(*) as n, sum(volume_kt) as total
  FROM flows GROUP BY year ORDER BY year
`);
display(Inputs.table(summary));
```

## Visualization with Observable Plot

```javascript
display(Plot.plot({
  title: "Annual volumes by destination",
  x: {label: "Year"},
  y: {label: "Volume (Mt)", grid: true},
  color: {legend: true},
  marks: [
    Plot.barY(data, {x: "year", y: "volume", fill: "region", tip: true}),
    Plot.ruleY([0])
  ]
}));
```

**Common marks:** `Plot.line()`, `Plot.barY()`, `Plot.areaY()`, `Plot.dot()`
**Built-in:** automatic scales, tooltips with `tip: true`, responsive layout

## Interactive inputs

```javascript
// Toggle
const show_all = view(Inputs.toggle({label: "Show all columns"}));

// Search
const searched = view(Inputs.search(data));

// Table
display(Inputs.table(searched, {
  rows: 25,
  columns: show_all ? undefined : ["name", "date", "value"]
}));

// Slider, select, etc.
const threshold = view(Inputs.range([0, 100], {step: 1, value: 50}));
const country = view(Inputs.select(["UK", "Norway", "Sweden"]));
```

`view()` makes input reactive - other cells auto-update when value changes.

## External libraries

Load via dynamic imports or CDN:

```html
<!-- CSS -->
<script type="text/html">
  <link href="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css" rel="stylesheet" />
</script>

<!-- JS library -->
<script type="module">
  const script = document.createElement('script');
  script.src = 'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js';
  script.onload = () => initMap();
  document.head.appendChild(script);
</script>
```

## Common patterns

### Data aggregation

```javascript
// Group by and sum
const annual = d3.rollup(flows, v => d3.sum(v, d => d.volume), d => d.year);

// Map to array
const data = Array.from(annual, ([year, volume]) => ({year, volume}))
  .sort((a, b) => a.year - b.year);
```

### Formatting

```javascript
const formatDate = d3.utcFormat("%B %Y");
const formatNumber = d3.format(",.1f");
const formatCurrency = d3.format("$,.0f");
```

### Inline calculations in markdown

```javascript
// Calculate stats
const total = d3.sum(flows, d => d.volume);
const maxYear = d3.max(flows, d => d.year);
```

Reference in markdown:
```html
<script type="text/markdown">
  Analysis found ${total.toFixed(1)} Mt across ${flows.length} voyages,
  peaking in ${maxYear}.
</script>
```

### Geospatial (DuckDB Spatial)

```sql
<script type="application/sql" database="../data/flows.duckdb" output="ports">
  SELECT port_name, ST_AsGeoJSON(geometry) as geojson, count(*) as visits
  FROM port_visits GROUP BY port_name, geometry
</script>
```

Use in Mapbox/Leaflet:
```javascript
ports.forEach(p => {
  const coords = JSON.parse(p.geojson).coordinates;
  new mapboxgl.Marker().setLngLat(coords).addTo(map);
});
```

## Building and previewing

**Before building or previewing, always run `yarn` first** to install dependencies (including DuckDB). Without this, SQL queries will fail silently.

```bash
# Install dependencies (required for DuckDB queries)
yarn

# Preview with hot reload (auto-kills existing servers first)
make preview

# Build for production
make build

# Kill any orphaned preview servers
make kill
```

**For Claude Code:** Run preview in background, then kill when done:
```bash
make preview &   # Start in background
# ... do work ...
make kill        # Clean up when finished
```

## Resources

- Observable Notebook Kit: https://observablehq.com/notebook-kit/
- Observable Plot: https://observablehq.com/plot/
- Observable Inputs: https://observablehq.com/notebook-kit/inputs
- DuckDB SQL: https://duckdb.org/docs/sql/introduction
