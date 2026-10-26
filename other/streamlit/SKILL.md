---
name: streamlit
description: Use when building a personal or team dashboard with Streamlit — KPI tiles with day-over-day change, multipage apps, data delivered as dated JSON files in a git repository, caching, a private deployment on Streamlit Community Cloud, and testing pages with AppTest. Also use when a page is blank or raises errors only in the cloud, the entry point runs the wrong code, or a module changed in git but the app still uses the old version.
---

# Streamlit dashboards

Default: one repository holding both the app and its data (one JSON file per day per source), a thin `app.py` entry point, pages in `pages/` or `st.navigation`, data access through cached functions, tests with `streamlit.testing.v1.AppTest`.

## Data flow that needs no server

1. Producers (scheduled jobs elsewhere) write `data/<source>/<YYYY-MM-DD>.json` and push to the main branch.
2. The app lists the files, loads them with `@st.cache_data(ttl=600)`, and shows the latest day plus trends.
3. A `?date=YYYY-MM-DD` query parameter (`st.query_params`) shows any past day.

Write only what the dashboard needs into the data files (counts, dates, categories); the repository becomes the audit log.

## Layout

- KPI row: `st.columns` with `st.metric(label, value, delta)` — delta versus the previous day.
- Below: charts of the last 30 days, then tables with links to sources.
- A one-line description under each page title saying what the page answers.

## Deployment (Community Cloud)

- Choose the Python version in the app's advanced settings to match local development.
- Keep the app private and invite viewers explicitly; check that a signed-out browser is redirected to login.
- Secrets go in the app's secrets settings, read with `st.secrets`, never in the repository.
- Notifications elsewhere (chat messages) can then carry only a short line and the dashboard URL instead of long reports.

## Entry point and imports

- Point the deployment at a small `app.py`. If the configured entry is a package `__init__.py`, Streamlit runs it as a script — guard heavy code with `if __name__ == "__main__":` or change the entry.
- After a push, the platform may reload `app.py` while helper modules stay cached in `sys.modules`; a new page calling a new function from an old module raises `AttributeError`. Avoid `importlib.reload` tricks (they can fail with `ImportError` under the runner); instead clear your package's modules from `sys.modules` at the top of the entry script before importing, or restart the app.

## Testing

```python
from streamlit.testing.v1 import AppTest
def test_overview_renders():
    at = AppTest.from_file("app.py").run(timeout=30)
    assert not at.exception
    assert at.metric[0].label == "Merged PRs"
```

Also test the cloud-like entry path (run the same entry file in a subprocess) so import-order bugs show up locally.

## Verification loop

1. `pytest` with AppTest: no exceptions on every page, with real sample data files.
2. `streamlit run app.py` and click through each page.
3. After deploy, open the URL signed out (must require login) and signed in (pages render).

## Pitfalls

- **Rerun model:** the whole script reruns on every interaction; keep expensive work in cached functions.
- **Mutable cached objects:** `st.cache_data` returns copies; `st.cache_resource` returns shared objects — do not mutate them per user.
- **Large tables** slow the browser; aggregate first.
- **Time zones:** dates in file names are in the producer's zone; label them.
