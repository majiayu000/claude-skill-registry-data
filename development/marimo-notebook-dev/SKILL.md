---
name: marimo-notebook-dev
description: |
  ALWAYS use when: creating/editing marimo notebooks, working with any .py file containing @app.cell decorators, building reactive Python notebooks, doing exploratory data analysis in notebook form, converting Jupyter (.ipynb) to marimo, or when user mentions "marimo", "reactive notebook", or asks for an interactive Python notebook. Covers marimo CLI (edit, run, convert, export), UI components (mo.ui.*), layout functions, SQL integration, caching, state management, and wigglystuff widgets. If a task involves notebooks and Python, invoke this skill first.
---

# Marimo Notebooks

Marimo notebooks are reactive Python notebooks stored as pure `.py` files. Cells auto-execute when dependencies change, modeled as a directed acyclic graph (DAG).

## Core Concepts

### Reactivity Model
- marimo uses **static analysis** to build a dependency graph from variable references and definitions
- When a cell runs, all cells referencing its defined variables **automatically re-run**
- Execution order follows the dependency graph, **not visual cell order**
- Each global variable must be defined by **exactly one cell**
- marimo does **not track object mutations** (like `list.append()`)—mutate in the same cell that creates the object, or create new variables

### Avoiding Variable Name Conflicts
Each global variable must be defined by exactly one cell. Two strategies to avoid conflicts:

**1. Wrap code in functions (preferred for reusable patterns):**
```python
@app.cell
def _(data):
    def compute_mean_with_new_col(df):
        temp = df.copy()
        temp["new_col"] = temp["x"] * 2
        return temp.mean()

    return (compute_mean_with_new_col(data),)
```

**2. Use meaningful, unique variable names:**
```python
@app.cell
def _(model1_data):
    model1_transformed = model1_data.copy()
    model1_transformed["new_col"] = model1_transformed["x"] * 2
    return (model1_transformed,)

@app.cell
def _(model2_data):
    model2_transformed = model2_data.copy()
    model2_transformed["new_col"] = model2_transformed["x"] * 2
    return (model2_transformed,)
```

Never use underscore prefixes to generate unique variable names. No exceptions.

## Notebook Structure

```python
import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    mo.md("# Hello")
    return

if __name__ == "__main__":
    app.run()
```

Key rules:
- Each cell is a function decorated with `@app.cell`
- Variables shared by returning tuples: `return (var1, var2,)`
- Cells receive variables as parameters: `def _(mo, df):`
- Execution order follows dependency graph, not position
- Name cells descriptively for CellTour targeting: `def model_specification():`

## CLI Commands

```bash
# Create & Edit
marimo new                           # Create new notebook
marimo new "build a dashboard"       # AI-generated starter
marimo edit notebook.py              # Open editor
marimo edit notebook.py --watch      # Live reload on file changes

# Run as App
marimo run notebook.py               # Run as app (code hidden by default)
marimo run notebook.py --include-code  # Show code in app view
marimo run notebook.py --host 0.0.0.0 --port 8080  # Network accessible
marimo run notebook.py --base-url /subpath  # Deploy at subpath
marimo run notebook.py --headless    # No browser auto-open

# Run as Script
python notebook.py                   # Execute as Python script
python notebook.py -- --arg1 val1    # Pass CLI arguments (after --)

# Convert
marimo convert notebook.ipynb -o notebook.py  # Jupyter to marimo
marimo convert notebook.md -o notebook.py     # Markdown to marimo

# Export
marimo export html notebook.py -o out.html              # Static HTML
marimo export html notebook.py -o out.html --include-outputs  # With outputs
marimo export html-wasm notebook.py -o out.html         # Interactive WASM
marimo export ipynb notebook.py -o out.ipynb            # To Jupyter
marimo export ipynb notebook.py -o out.ipynb --include-outputs
marimo export script notebook.py -o out.py              # Pure Python
marimo export md notebook.py -o out.md                  # Markdown

# Utilities
marimo check notebook.py             # Lint and validate
marimo check notebook.py --fix       # Auto-fix issues
marimo tutorial intro                # Interactive tutorials
marimo tutorial markdown             # Markdown tutorial
marimo tutorial plots                # Plotting tutorial
marimo tutorial layout               # Layout tutorial
```

## Code Visibility in Run Mode

**CRITICAL FOR TUTORIALS**: By default, `marimo run` hides code. Use these options to show code:

### mo.show_code() - Per-Cell Display (Recommended)

**IMPORTANT**: Call `mo.show_code()` as a **statement on its own line**, NOT as part of the return statement. The return statement should be separate.

```python
@app.cell
def model_definition(mo, pm, X, y):
    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sigma=10)
        beta = pm.Normal("beta", mu=0, sigma=10)
        sigma = pm.HalfNormal("sigma", sigma=1)
        mu = alpha + beta * X
        likelihood = pm.Normal("y", mu=mu, sigma=sigma, observed=y)

    # Show this cell's code alongside its output - CALL AS STATEMENT, NOT IN RETURN
    mo.show_code(model, position="above")
    return (model,)

@app.cell
def sampling(mo, pm, model):
    with model:
        trace = pm.sample(1000)
    
    # Position: "above" shows code first, then output (recommended for tutorials)
    mo.show_code(trace, position="above")
    return (trace,)

@app.cell
def compute_stats(mo, data, np):
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    # For cells with no natural visual output, create one with mo.md()
    mo.show_code(mo.md(f"**Computed:** mean={mean_val:.2f}, std={std_val:.2f}"), position="above")
    return mean_val, std_val
```

Key points:
- **Call `mo.show_code(output, position="above")` as a statement before `return`**
- `position="above"` shows code first, then output (best for tutorials)
- `position="below"` shows output first, then code (default)
- The `output` argument is required—it's what displays alongside the code
- For cells without visual output, use `mo.md()` to create a summary message
- In displayed code, `mo.show_code(...)` line is hidden
- **Use for EVERY code cell in tutorials/educational notebooks**

### WRONG vs RIGHT patterns:

```python
# WRONG - do not put mo.show_code() in return statement
return mo.show_code(result)
return (mo.show_code(result), other_var)

# RIGHT - call as statement, then return separately  
mo.show_code(result, position="above")
return (result,)

# RIGHT - with multiple return values
mo.show_code(chart, position="above")
return df, model, chart
```

### CLI Flag - Show All Code
```bash
marimo run notebook.py --include-code
```

### URL Parameter - For Hosted Apps
```
https://your-app.marimo.app/app?show-code=true
```

## Markdown with mo.md()

```python
@app.cell
def _(mo):
    mo.md(r"""
    # Title

    Interpolate Python: {slider}

    **LaTeX inline**: $f(x) = e^x$

    **LaTeX block**:
    $$
    \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
    $$

    **Icons** (Iconify): ::lucide:rocket:: or ::mdi:home::
    """)
    return
```

Key features:
- Use raw strings (`r"""..."""`) for LaTeX to avoid escaping backslashes
- Interpolate UI elements directly: `f"Value: {slider}"`
- For complex objects, use `mo.as_html()`: `f"Plot: {mo.as_html(fig)}"`
- Load LaTeX macros: `mo.latex(filename="macros.tex")`
- Icons: `mo.icon("lucide:rocket", size=20, color="blue")`

## UI Components (mo.ui.*)

### Basic Inputs
```python
slider = mo.ui.slider(0, 100, value=50, label="Value")
number = mo.ui.number(0, 100, value=50)
text = mo.ui.text(value="", placeholder="Enter text")
text_area = mo.ui.text_area(value="", placeholder="Multi-line")
checkbox = mo.ui.checkbox(value=False, label="Enable")
switch = mo.ui.switch(value=False, label="Toggle")
dropdown = mo.ui.dropdown(["a", "b", "c"], value="a")
radio = mo.ui.radio(["option1", "option2"], value="option1")
multiselect = mo.ui.multiselect(["a", "b", "c"])
range_slider = mo.ui.range_slider(0, 100, value=(20, 80))
```

### Date/Time
```python
date = mo.ui.date(value="2024-01-01")
datetime = mo.ui.datetime()
date_range = mo.ui.date_range()
```

### Buttons
```python
button = mo.ui.button(label="Click")              # Simple button
run_button = mo.ui.run_button(label="Run")        # For triggering computation
refresh = mo.ui.refresh(default_interval="1s")    # Auto-refresh timer

# Counter button
counter = mo.ui.button(value=0, on_click=lambda count: count + 1)

# Toggle button
toggle = mo.ui.button(value=False, on_click=lambda v: not v)
```

### Files & Media
```python
file = mo.ui.file(kind="file", filetypes=[".csv", ".json"])
file_browser = mo.ui.file_browser(initial_path="./")
microphone = mo.ui.microphone()
```

### Data Components
```python
table = mo.ui.table(df)                    # Interactive table with selection
dataframe = mo.ui.dataframe(df)            # Editable dataframe
data_editor = mo.ui.data_editor(df)        # Full editor
data_explorer = mo.ui.data_explorer(df)    # No-code exploration
```

### Advanced
```python
code_editor = mo.ui.code_editor(value="", language="python")
chat = mo.ui.chat(model)                   # Chat interface
anywidget = mo.ui.anywidget(MyWidget())    # Custom widgets
tabs = mo.ui.tabs({"Tab1": content1, "Tab2": content2})
```

### Grouping UI Elements
```python
# Dynamic arrays
array = mo.ui.array([mo.ui.slider(0, 10) for _ in range(5)])
array.value  # List of values

# Dynamic dictionaries
dictionary = mo.ui.dictionary({"x": mo.ui.slider(0, 10), "y": mo.ui.slider(0, 10)})
dictionary.value  # Dict of values

# Forms (require submit button)
form = mo.ui.text().form()
form.value  # None until submitted

# Batch multiple elements in markdown
form = mo.md("""
**Name**: {name}
**Age**: {age}
""").batch(
    name=mo.ui.text(),
    age=mo.ui.number(0, 120)
).form()
```

## Layout Functions

```python
# Stacking
mo.hstack([el1, el2, el3], justify="center", gap=2)  # Horizontal
mo.vstack([el1, el2, el3], align="start", gap=1)     # Vertical

# Containers
mo.accordion({"Section 1": content1, "Section 2": content2})
mo.tabs({"Tab 1": content1, "Tab 2": content2})  # Use mo.ui.tabs for state
mo.callout(content, kind="info")  # info, warn, success, danger, neutral
mo.carousel([item1, item2, item3])
mo.sidebar([nav_content])

# Alignment
mo.center(content)
mo.left(content)
mo.right(content)

# Display
mo.plain(content)           # No styling
mo.tree({"a": {"b": 1}})    # Tree view
mo.json(data)               # JSON viewer
mo.stat(value="42", label="Users", caption="+5%")  # Statistic card

# Lazy loading (defer until visible)
mo.lazy(expensive_component)                      # Object
mo.lazy(lambda: compute_expensive())              # Function (deferred)
mo.lazy(async_func, show_loading_indicator=True)  # Async with spinner

# Outline/Table of Contents
mo.outline()  # Creates navigation outline

# Routing (multi-page apps)
mo.routes({
    "#/": render_home,
    "#/about": render_about,
    mo.routes.CATCH_ALL: render_home,
})

# Combined with navigation
mo.sidebar([
    mo.nav_menu({
        "#/": f"{mo.icon('lucide:home')} Home",
        "#/about": f"{mo.icon('lucide:user')} About",
    }, orientation="vertical")
])
```

## Output Functions

```python
# Dynamic output manipulation
mo.output.replace(new_content)      # Replace cell output
mo.output.append(additional)        # Append to output
mo.output.clear()                   # Clear output
mo.output.replace_at_index(val, 2)  # Replace at specific index

# Console redirection
with mo.redirect_stdout():
    print("This goes to cell output")

with mo.capture_stdout() as buffer:
    print("Captured")
    text = buffer.getvalue()
```

## Status Indicators

```python
# Progress bar (like tqdm)
for item in mo.status.progress_bar(items, title="Processing"):
    process(item)

# With manual control
with mo.status.progress_bar(total=100, title="Loading") as bar:
    for i in range(100):
        do_work()
        bar.update(title=f"Step {i}")

# Spinner
with mo.status.spinner(title="Loading...", subtitle="Please wait"):
    load_data()

# Conditional spinner
mo.status.spinner(title="Loading") if loading else mo.md("Done!")
```

## Control Flow

```python
# Stop execution conditionally
mo.stop(condition, mo.md("*Message when stopped*"))

# Example: require button click
run_button = mo.ui.run_button()
mo.stop(not run_button.value, mo.md("Click Run to execute"))
expensive_computation()

# Example: require form submission
mo.stop(form.value is None, mo.md("Submit the form first"))
process(form.value)

# Conditional output
result if condition else None
```

## Caching

```python
# In-memory cache (session only, fastest)
@mo.cache
def expensive_function(x, y):
    return compute(x, y)

# Persistent cache (survives restarts)
@mo.persistent_cache(name="embeddings")
def compute_embeddings(text):
    return model.encode(text)

# Block-style persistent cache
with mo.persistent_cache(name="data_load"):
    df = load_large_dataset()
    processed = transform(df)

# LRU cache with size limit
@mo.lru_cache(maxsize=128)
def bounded_cache(x):
    return compute(x)
```

## Model Output Caching for Data Science

For expensive MCMC sampling and Bayesian model fits, use this pattern to cache outputs and avoid unnecessary re-runs during development. This supplements marimo's built-in caching with data/parameter-aware invalidation.

### Configuration Cell

```python
@app.cell
def _():
    from pathlib import Path

    ENABLE_MODEL_CACHE = True  # Set False to force re-fitting
    CACHE_DIR = Path(".model_cache")
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR, ENABLE_MODEL_CACHE
```

### Cache Utilities with Hashing

```python
@app.cell
def _(CACHE_DIR):
    import hashlib
    from pathlib import Path

    def get_cache_path(name: str, data=None, **params) -> Path:
        """Generate cache path from name, data hash, and parameters."""
        components = [name]
        if data is not None:
            # Hash data shape and sample values for change detection
            data_repr = f"{type(data).__name__}_{getattr(data, 'shape', len(data))}"
            components.append(hashlib.md5(data_repr.encode()).hexdigest()[:6])
        if params:
            param_str = str(sorted(params.items()))
            components.append(hashlib.md5(param_str.encode()).hexdigest()[:6])
        return CACHE_DIR / f"{'_'.join(components)}.nc"

    return (get_cache_path,)
```

### PyMC Caching Pattern

```python
@app.cell
def _(mo, pm, az, X, y, ENABLE_MODEL_CACHE, get_cache_path):
    # Cache key includes data shape and sampling parameters
    cache_path = get_cache_path(
        "linear_model",
        data=y,
        n_samples=2000,
        seed=42
    )

    trace = None
    if ENABLE_MODEL_CACHE and cache_path.exists():
        trace = az.from_netcdf(cache_path)
        mo.output.append(mo.callout("Loaded trace from cache", kind="info"))

    if trace is None:
        with pm.Model() as model:
            alpha = pm.Normal("alpha", 0, 10)
            beta = pm.Normal("beta", 0, 10, shape=X.shape[1])
            sigma = pm.HalfNormal("sigma", 1)
            mu = alpha + pm.math.dot(X, beta)
            pm.Normal("y", mu, sigma, observed=y)
            trace = pm.sample(2000, nuts_sampler="nutpie", random_seed=42)

        if ENABLE_MODEL_CACHE:
            az.to_netcdf(trace, cache_path)

    return (trace,)
```

### When to Use

Use this pattern for:
- MCMC sampling (>30 seconds runtime)
- Model comparison workflows
- Iterative model development where you're modifying downstream analysis

**Not needed for**:
- Quick computations (<5 seconds)—use `@mo.cache` instead
- Computations with automatic dependency tracking—use `@mo.persistent_cache`

Toggle `ENABLE_MODEL_CACHE = False` when you need fresh fits (e.g., after model specification changes not captured in parameters).

## State Management

**Warning**: Use sparingly—over 99% of cases don't need `mo.state()`.

```python
@app.cell
def _(mo):
    get_count, set_count = mo.state(0)
    return get_count, set_count

@app.cell
def _(mo, get_count, set_count):
    mo.ui.button(
        label=f"Count: {get_count()}",
        on_click=lambda _: set_count(lambda n: n + 1)
    )
    return
```

Use `mo.state()` only when:
- Maintaining history tied to UI elements
- Synchronizing multiple UI elements bidirectionally
- Introducing cycles across cells at runtime

## SQL Integration

Install: `pip install "marimo[sql]"`

```python
@app.cell
def _(mo, threshold):
    # Query Python dataframes by name
    result = mo.sql(f"""
        SELECT * FROM my_dataframe
        WHERE value > {threshold.value}
        LIMIT 100
    """)
    return (result,)

# External sources
mo.sql("""
    SELECT * FROM 's3://bucket/file.parquet';
    SELECT * FROM read_csv('data.csv');
""")
```

SQL can query: Python dataframes (polars/pandas), DuckDB, PostgreSQL, MySQL, SQLite, Snowflake, BigQuery, Redshift, CSV/Parquet files, S3

Escape literal braces with `{{}}`:
```sql
SELECT unnest([{{'a': 42, 'b': 84}}]);
```

Output types: `native` (DuckDB relation), `lazy-polars`, `polars`, `pandas`, `auto`

## Interactive Plotting

```python
# Altair with selection
chart = alt.Chart(df).mark_point().encode(x="x", y="y")
selection = mo.ui.altair_chart(chart, chart_selection="point")
selected_data = selection.value  # DataFrame of selected points

# Plotly (scatter, treemap, sunburst)
fig = px.scatter(df, x="x", y="y")
interactive = mo.ui.plotly(fig)
interactive.value  # Selected points

# Matplotlib interactive (pan, zoom, hover)
fig, ax = plt.subplots()
ax.plot(x, y)
mo.mpl.interactive(fig)
```

Supported libraries: Matplotlib, Seaborn, Plotly, Altair, Bokeh, HoloViews, hvPlot, Leafmap

## Media Functions

```python
mo.image(src)          # URL, path, or file-like object
mo.image_compare(img1, img2)  # Side-by-side comparison
mo.video(src)
mo.audio(src)
mo.pdf(src)
mo.download(data, filename="file.csv", label="Download")
mo.plain_text(text)
```

## External Data Access

```python
# CLI arguments (after --)
args = mo.cli_args()  # Dict of arguments
size = mo.cli_args().get("size") or 100

# URL query parameters
params = mo.query_params()
params["key"]  # Read
params.set("key", "value")  # Write (updates URL, triggers reactivity)

# File watching (reactive to changes)
watched_file = mo.watch.file("config.json")  # Re-runs on file change
watched_dir = mo.watch.directory("data/")     # Re-runs on structure change
```

## App Metadata

```python
meta = mo.app_meta()
meta.mode   # "edit", "run", "script", "test", or None
meta.theme  # "light" or "dark"
meta.request  # HTTP request info (headers, cookies, params)
```

## Embedding Notebooks

```python
# Import another notebook
from other_notebook import app as other_app

@app.cell
async def _(other_app):
    # Must call from different cell than import
    result = await other_app.embed()
    return result.output, result.defs

# Run programmatically with overrides
outputs, defs = other_app.run(defs={"param": value})
```

## HTML Manipulation

```python
html = mo.Html("<div>Custom HTML</div>")
html.text  # Get underlying string

# Styling
styled = html.style({"color": "red", "font-size": "20px"})
styled = html.callout(kind="info")

# iframes (for scripts that need execution)
mo.iframe(html_with_scripts, width="100%", height="400px")
```

## Best Practices

1. **Wrap reusable code in functions** - Keeps intermediate variables local and avoids namespace pollution
2. **Use meaningful, unique variable names** - e.g., `model1_sigma`, `model2_sigma` instead of generic names
3. **Don't mutate across cells** - Mutate in same cell or create new variables
4. **Write idempotent cells** - Same inputs should produce same outputs
5. **Use mo.stop()** - Gate expensive operations behind conditions/buttons
6. **Split into modules** - Import from `.py` files, use auto-reload
7. **Use lazy loading** - `mo.lazy()` for expensive components in tabs/accordions
8. **Cache expensive ops** - `@mo.cache` for session, `@mo.persistent_cache` for disk

## CRITICAL: Pre-Edit Checklist

**BEFORE making ANY edit to a marimo notebook:**

1. **Read the current file state** — The file may have been modified by marimo's editor. Never assume your last read is current.
2. **Run `marimo check notebook.py`** — Verify the notebook is valid before and after edits.

**AFTER completing edits:**

3. **Grep for `print(`** — Find ALL print statements and replace with marimo output (`mo.md()`, `mo.stat()`, `mo.callout()`, etc.). Never just delete—always replace with equivalent marimo output.
4. **Run `marimo check notebook.py`** — Verify no errors were introduced.

## Common Gotchas

### Output & Display

- **NEVER use print() in cells**: Print statements do NOT display in run mode. Always use marimo output elements instead:
  - `mo.md(f"**Label:** {value}")` — formatted text
  - `mo.stat(value=f"{x}", label="Label")` — metric cards
  - `mo.callout(content, kind="info")` — callout boxes
  - `mo.hstack([...])` / `mo.vstack([...])` — layouts
  - Return the dataframe/object directly — automatic display

- **mo.show_code() must be called as a statement, not in return**: Call it on its own line before the return statement:
  ```python
  # WRONG - in return statement
  return mo.show_code(result)
  return (mo.show_code(result), other_var)
  
  # RIGHT - as statement before return
  mo.show_code(result, position="above")
  return (result,)
  
  # RIGHT - with multiple return values
  mo.show_code(chart, position="above")
  return df, model, chart
  
  # RIGHT - when cell has no visual output, create one
  mo.show_code(mo.md(f"**Result:** {value}"), position="above")
  return (value,)
  ```

- **Never delete output without replacing**: When removing print statements or other output, always replace with equivalent marimo output. Deleting loses information the user needs to see.

### Reactivity & Variables

- **Closures in loops**: Use default args `lambda v, i=i: ...` not `lambda v: ... i`
- **on_change handlers**: Only work if element is bound to global variable
- **Dynamic UI elements**: Must wrap in `mo.ui.array()`, `mo.ui.dictionary()`, or `mo.ui.batch()`
- **Type annotations**: Registered as references unless quoted: `x: "SomeType"`

### Libraries

- **matplotlib cut-off**: Call `plt.tight_layout()` before outputting
- **dotenv**: Use `dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))`

## Configuration

### Environment Variables
- `MARIMO_OUTPUT_MAX_BYTES` (default 8MB)
- `MARIMO_STD_STREAM_MAX_BYTES` (default 1MB)
- `MARIMO_SKIP_UPDATE_CHECK`
- `MARIMO_SQL_DEFAULT_LIMIT`

### User Config (`.marimo.toml`)
- Runtime: autorun, lazy mode, SQL output format
- Display: theme, font size, output placement
- Editor: hotkeys, vim mode, copilot, formatting

### App Config (in notebook file)
- Width, title, custom CSS, HTML head

## Deployment

```bash
# Docker
marimo run notebook.py --host 0.0.0.0 --port 8080

# Health endpoints
/health    # 200 OK
/healthz   # Alternative
/api/status  # JSON status
```

Platforms: Docker, Kubernetes, HuggingFace, Railway, SkyPilot, Slurm/HPC

## Testing

```bash
# Run as pytest
pytest notebook.py

# With doctest
python -m doctest notebook.py
```

marimo notebooks are pure Python—test like any Python module.

## Wigglystuff Widgets

Install: `pip install wigglystuff`

```python
from wigglystuff import Slider2D, Paint, SortableList, Matrix, CellTour
import marimo as mo

slider2d = mo.ui.anywidget(Slider2D())
slider2d.x, slider2d.y

paint = mo.ui.anywidget(Paint(width=400, height=300))
paint.to_pil()

sortable = mo.ui.anywidget(SortableList(items=["A", "B", "C"]))
sortable.items

matrix = mo.ui.anywidget(Matrix(rows=3, cols=3))
matrix.data

# CellTour for guided tutorials
tour = mo.ui.anywidget(CellTour(
    steps=[
        {"cell_name": "intro", "title": "Welcome", "description": "...", "position": "bottom"},
        {"cell_name": "model", "title": "Model", "description": "...", "position": "bottom"},
    ],
    auto_start=False,
    show_progress=True
))
```

Available: `Slider2D`, `Matrix`, `Paint`, `EdgeDraw`, `SortableList`, `ColorPicker`, `KeystrokeWidget`, `GamepadWidget`, `WebkitSpeechToTextWidget`, `CopyToClipboard`, `WebcamCapture`, `CellTour`

See `references/wigglystuff.md` for complete widget reference.

## Resources

- **Official docs**: https://docs.marimo.io
- **Examples**: https://github.com/marimo-team/examples
- **Tutorials**: https://github.com/Haleshot/marimo-tutorials
- **UI components**: See `references/ui_components.md`
- **Wigglystuff**: See `references/wigglystuff.md`
