---
name: marimo
description: Reactive Python notebooks stored as pure .py files — cells form a dependency DAG, so changing one cell automatically reruns its dependents (or marks them stale under the lazy runtime) and hidden state cannot exist. Covers the notebook file format, marimo edit/run/export CLI, mo.ui interactive elements, SQL cells, running notebooks as apps or scripts, and sandboxed notebooks with PEP 723 inline dependencies. Use when creating or editing marimo notebooks, building interactive data apps or dashboards in pure Python, converting Jupyter notebooks, or when reproducibility/git-friendliness rules out .ipynb.
---

# marimo — reactive Python notebooks

## Overview

marimo is a reactive notebook: cells form a DAG based on which variables each cell
defines and reads. Run a cell and every dependent cell reruns (or is marked stale) —
no hidden state, no out-of-order execution bugs. Notebooks are pure Python files that
diff cleanly in git and double as apps and scripts. Pairs with [[pandas]]/[[polars]]
for data work and [[matplotlib]] for plots; project tooling in [[modern-python]].

```bash
uv add marimo            # or: uv tool install marimo
marimo tutorial intro    # interactive intro
marimo edit nb.py        # create/edit a notebook (browser editor)
marimo run nb.py         # serve as a read-only web app (code hidden by default)
marimo convert nb.ipynb -o nb.py   # migrate from Jupyter
marimo check nb.py       # lint/format notebook files
```

Verified against marimo 0.23.16 (Python >= 3.10).

## File format — a notebook is a Python file

```python
import marimo

app = marimo.App()

@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    n = mo.ui.slider(1, 100, value=10, label="n")
    n                      # last expression = cell output
    return (n,)

@app.cell
def _(n):
    total = sum(i**2 for i in range(n.value))
    print(total)
    return (total,)

if __name__ == "__main__":
    app.run()
```

Each cell is a function: parameters are the variables it reads, the `return` tuple is
what it defines. The editor maintains this wiring for you — hand-edit freely, marimo
re-derives the DAG from the code. `python nb.py` executes it top-of-DAG-down like a
script.

## Reactivity rules

- **A variable may be defined in only one cell.** Duplicate definitions are a
  `MultipleDefinitionError` — the file won't run. Prefix throwaway names with `_`
  to make them cell-local (`_x`, `_fig`).
- Reading a variable creates the edge; **mutations are not tracked** — `lst.append(...)`
  in another cell won't retrigger dependents. Create new objects instead of mutating.
- Cell order in the file doesn't matter; execution order comes from the DAG.
- `mo.stop(condition, mo.md("waiting..."))` short-circuits a cell; `mo.md(f"...")`
  renders markdown with interpolated values.

## UI elements (`mo.ui`)

```python
n = mo.ui.slider(1, 100, value=10)       # assign to a GLOBAL, display it
text = mo.ui.text(placeholder="query")
pick = mo.ui.dropdown(["a", "b"], value="a")
run = mo.ui.run_button()                  # gate expensive cells
mo.vstack([n, text, pick, run])           # last expression: renders the elements
```

Interacting with an element updates `element.value` and reruns cells that read it —
no callbacks. Two rules: the element must be assigned to a global variable and
displayed (as cell output or inside `mo.md`/layout), and **`.value` cannot be read in
the cell that creates the element** (a cell can't depend on itself). Others:
`mo.ui.table`, `mo.ui.dataframe`, `mo.ui.file`, `mo.ui.form`, `mo.ui.altair_chart`,
`mo.ui.checkbox`, `mo.ui.radio`, `mo.ui.date`, `mo.ui.chat`, `mo.ui.anywidget`.

## SQL cells

```python
df = mo.sql(f"SELECT city, count(*) FROM users_df GROUP BY city")
```

SQL cells (`uv add "marimo[sql]"` for DuckDB + friends) query dataframes, CSVs, or
attached databases in place; the result is a dataframe, and `{python_expr}` values
interpolate into the query. Reactivity crosses the language boundary — the SQL cell
reruns when the cell defining `users_df` reruns (rebinding, not in-place mutation).
See [[duckdb-docs]] for SQL specifics.

## Apps, scripts, exports

```bash
marimo run nb.py --host 0.0.0.0 -p 8080   # deploy as interactive app
python nb.py                               # run as a plain script
marimo run app.py -- --arg value           # pass CLI args through
marimo export html-wasm nb.py -o out.html  # self-contained, runs in browser (Pyodide)
marimo export ipynb nb.py -o nb.ipynb      # also: html, md, pdf, script
```

## Sandboxed notebooks (inline dependencies)

```bash
marimo edit --sandbox nb.py    # also: run --sandbox, new --sandbox (requires uv)
```

`--sandbox` runs the notebook in an isolated venv and records imports as PEP 723
inline metadata in the file header, so a single `.py` file carries its environment —
`uv run nb.py` recreates the environment anywhere:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==3.0.5", "altair==6.2.2"]
# ///
```

## marimo vs Jupyter

Prefer marimo when you want git-diffable notebooks, guaranteed execution order
(reproducibility), notebooks that ship as apps/scripts without rewriting, or
interactive UI without widget callback plumbing. Prefer Jupyter when you depend on
its ecosystem (nbconvert pipelines, JupyterHub, kernels for other languages) — or
convert with `marimo convert`.

## Gotchas

- **`MultipleDefinitionError`**: same name defined in two cells. Rename, or use a
  `_`-prefixed local.
- **UI element seems inert**: it wasn't assigned to a global, wasn't displayed, or
  you read `.value` in its defining cell.
- **Dependents don't rerun after mutation**: marimo tracks definitions, not
  mutations. Rebind (`df = df.assign(...)`) instead of mutating in place.
- **Expensive cells rerun too eagerly**: gate them behind `mo.ui.run_button()`, use
  `mo.stop()`, or switch runtime to lazy in settings.
- `marimo run` hides code by default — pass `--include-code` to show it.

## Related

Data wrangling with [[pandas]] / [[polars]]; plotting with [[matplotlib]]; SQL via
[[duckdb-docs]]; environments and PEP 723 scripts in [[modern-python]].
