---
name: notebook-to-module
category: notebooks
description: Use when a task touches a Jupyter or marimo notebook, asks to productionise or schedule notebook logic, or when you are tempted to do the work in a notebook — extract logic into tested modules, keep the notebook thin and reproducible, and commit it the way the repo does
tech_stack: Notebooks
source: original; informed by openai/skills jupyter-notebook (ideas only) and the jupytext, nbstripout, papermill, nbmake and marimo documentation (cited, not reproduced)
---
# Notebook to Module

## Overview

Notebooks are good for looking at data and bad at being software: hidden state from out-of-order cells, no tests, diffs full of JSON and base64 images. In this role a notebook is never the deliverable. Logic moves into an importable module with tests; the notebook imports it and shows results (rule no-notebook-only-logic).

**Core principle:** if a test, a pipeline or a service needs it, it lives in `src/`; the notebook only calls it.

## 1. Run it before you change it

Find out whether the notebook works today, on a fresh kernel, top to bottom:

```bash
mkdir -p /tmp/tt-<task key>
uv run jupyter nbconvert --to notebook --execute notebooks/churn.ipynb --output-dir /tmp/tt-<task key>/
# or, when the notebook has a parameters cell
uv run papermill notebooks/churn.ipynb /tmp/tt-<task key>/churn.out.ipynb -p sample_frac 0.01
```

Record the result: runs, fails at cell N, or cannot run here (needs warehouse credentials, a GPU, a file not in the repo). If it could not be executed, say so explicitly in the closing message — never describe a notebook as working because it looks right.

## 2. Extract, test-first

For each cell that computes something (load, clean, feature, train, evaluate):

1. Name the function and its inputs and outputs — every global the cell read becomes a parameter.
2. Write the test first on a small hand-built fixture with a hand-derived expected result (ml-testing-strategy).
3. Move the logic into the module, make the test pass.
4. Replace the cell body with a call.

```python
# ❌ notebook cell — nothing can test or reuse this
df = pd.read_csv("/Users/ana/data/orders.csv")
df = df[df.status != "test"]
df["value"] = df.qty * df.price
monthly = df.groupby(df.ordered_at.str[:7]).value.sum()
```

```python
# ✅ src/shop/metrics.py
def monthly_revenue(orders: pd.DataFrame) -> pd.Series:
    real = orders[orders["status"] != "test"]
    value = real["qty"] * real["price"]
    month = real["ordered_at"].dt.to_period("M")
    return value.groupby(month).sum().rename("revenue")
```

```python
# ✅ tests/test_metrics.py
def test_monthly_revenue_excludes_test_orders_and_groups_by_month() -> None:
    orders = pd.DataFrame({
        "status": ["ok", "test", "ok"],
        "qty": [2, 1, 1],
        "price": [5.0, 100.0, 3.0],
        "ordered_at": pd.to_datetime(["2026-01-31", "2026-01-15", "2026-02-01"]),
    })
    assert monthly_revenue(orders).to_dict() == {
        pd.Period("2026-01", "M"): 10.0,
        pd.Period("2026-02", "M"): 3.0,
    }
```

```python
# ✅ notebook cell afterwards
orders = load_orders(Settings())
monthly_revenue(orders).plot.bar()
```

Bugs you find while extracting (a string-sliced month, a filter that drops nulls) get their own failing test first, and a line in the closing message — the numbers the notebook used to show change.

## 3. What a thin notebook looks like

- First cell: imports from the package and settings; no function definitions longer than a few lines.
- One step per cell, with a short markdown line saying what it shows.
- No `!pip install`, no `%cd`, no absolute paths, no credentials — configuration comes from settings or environment variables.
- Small outputs: summaries and plots, not 10,000-row frames.
- Runs top to bottom on a fresh kernel; restart-and-run-all is the only way it is ever checked.

## 4. Committing notebooks — follow the repository

| Repo uses | Do |
|---|---|
| nbstripout (git filter or pre-commit hook) | commit with outputs stripped; never bypass the hook |
| jupytext pairing | edit either side, then `jupytext --sync notebooks/churn.ipynb`; review the `.py` diff |
| marimo | notebooks are plain `.py` files: `marimo edit`, run as a script with `python notebooks/churn.py`, convert with `marimo convert churn.ipynb > churn.py` only if the task asks |
| nothing yet | strip outputs before committing and say so; adding a notebook tool is a separate decision (rule repo-conventions-win) |

## 5. Scheduled or parameterised notebooks

If a notebook must run on a schedule, prefer turning it into a pipeline entrypoint that calls the module (data-pipeline-orchestration). Where the repository already runs notebooks with papermill, keep a single cell tagged `parameters`, keep the logic in the package, and write outputs to a path derived from the parameters.

## 6. Notebooks in the test suite

When the repository executes notebooks in CI (`pytest --nbmake notebooks/` or an nbconvert step), keep that green: the notebook must run on the fixture or a tiny sample, fast, without credentials. Otherwise the notebook's logic is covered by the module tests, and the notebook itself is checked by running it once as in section 1.

## Common Mistakes

- Copying cells into a module without tests "to refactor later".
- Leaving a duplicate of the logic in the notebook after extracting it, so the two drift.
- Committing a notebook with outputs that contain data samples or credentials.
- A notebook that only works after running cells in a particular non-linear order.
- Reporting numbers from a notebook run that nobody can reproduce from the diff.

## Red Flags

- A function defined in a notebook and imported elsewhere via `%run`.
- A pipeline or service that reads a file only a notebook writes.
- A notebook diff of thousands of lines for a one-line change.
- "The notebook works" with no execution in this run.
