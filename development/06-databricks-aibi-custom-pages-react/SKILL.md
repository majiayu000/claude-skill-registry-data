---
name: databricks-aibi-custom-pages-react
description: >
  Build full-page, high-fidelity React "custom pages" inside a Databricks AI/BI (Lakeview)
  dashboard — the mechanism behind pixel-perfect, custom-app-like dashboards (composite KPI cards,
  in-cell sparklines, custom filter chips, status pills, email-preview surfaces). A custom page is a
  single widget whose `multilineTextboxSpec.lines` carry a `<!-- @custom-page -->` marker followed by
  a JSON envelope `{code, manifest, datasetMap}`, where `code` is CommonJS React that reads dashboard
  datasets through the injected `viz.useCustomPageQuery` hook. Use ONLY when neither the built-in
  widgets (02-databricks-aibi-dashboards) nor Vega-Lite custom viz (05-databricks-aibi-custom-viz-vega)
  can express the layout. WARNING — this mechanism is NOT in official Databricks docs; treat as
  high-volatility and verify in your workspace before relying on it.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: dashboards
deploy_verb: bundle_deploy
deploy_note: "A custom page is one widget on an otherwise standard AI/BI dashboard; it deploys via the same base64 Workspace Import / `bundle deploy --target dev` path as 02-databricks-aibi-dashboards. On Genie Code, write the .lvdash.json under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`). The `code` string is embedded inside the JSON, which is embedded inside the .lvdash.json — mind the double-escaping (see references/custom-page-envelope.md)."
coverage: partial
metadata:
  author: prashanth subrahmanyam
  version: "0.1"
  domain: monitoring
  role: worker
  pipeline_stage: 7
  pipeline_stage_name: observability
  called_by:
    - observability-setup
  standalone: true
  keywords:
    - databricks
    - ai/bi
    - lakeview
    - custom page
    - custom widget
    - react
    - "@custom-page"
    - useCustomPageQuery
    - high-fidelity dashboard
    - bespoke layout
  last_verified: "2026-09-21"
  volatility: high
  status: "UNDOCUMENTED / not in public Databricks docs as of 2026-09-21. Contract below was extracted empirically from a real deployed .lvdash.json exemplar. May be private/early preview; API and availability can change without notice."
  upstream_sources:
    - name: "Empirical exemplar — deployed 4C's Operational AI/BI dashboard (.lvdash.json)"
      relationship: "reverse-engineered"
      last_synced: "2026-09-21"
---

# AI/BI Custom Pages (React)

## ⚠️ Status: undocumented — read before use

This skill documents a mechanism (`<!-- @custom-page -->` + `viz.useCustomPageQuery`) that is **not
published in the official Databricks documentation** as of 2026-09-21. The contract below was
**reverse-engineered from a real, deployed `.lvdash.json`** — it is accurate to that exemplar but is
**not an officially supported API**. Consequences:

- It may be a private/early preview; **availability is not guaranteed** in your workspace.
- The envelope keys, the `viz` runtime, and the hook shape **can change without notice**.
- Treat as `volatility: high`. **Verify it renders in your target workspace before building on it.**
- Prefer the documented tiers when they suffice: built-in widgets (`02`) → Vega-Lite custom viz (`05`)
  → this skill only for full-page bespoke layouts.

If you need a fully supported, custom React surface, a **Databricks App** (see `apps_lakebase/` and the
`databricks-apps` skill) is the documented product — it is a separate app, not an embedded dashboard page.

## Fidelity Decision Gate (read first)

Pick the **lowest** tier that meets the requirement. Escalating for looks alone is a defect.

| Need | Use | Skill |
|------|-----|-------|
| Standard chart / KPI / table / filter | Built-in widget | `02-databricks-aibi-dashboards` |
| A custom **single chart** the built-ins lack, with native cross-filter | Vega-Lite custom viz | `05-databricks-aibi-custom-viz-vega` |
| A **full-page bespoke layout** — composite multi-metric cards, in-cell sparklines, custom filter chips, status pills, narrative/email surfaces — that no single chart can express | **React custom page** | **this skill** |

**Output a Fidelity Decision Record** before authoring, listing which triggers fired, e.g.:
`Fidelity: React custom page — exec narrative surface; composite cards + inline sparklines + custom chips; built-ins and Vega single-chart both insufficient. Accepting: undocumented mechanism, no native cross-filter, JS maintenance, workspace-preview-only validation.`

## Tradeoffs (accept these explicitly)

- ❌ **No native cross-filter / drill-through** — you hand-code interactions inside React.
- ❌ **No native export / accessibility** guarantees from the platform chrome.
- ❌ **Not headless-validatable** — arbitrary React only truly verifies in a workspace preview.
- ❌ **Higher maintenance** — a large JS blob inside JSON; harder to review than declarative widgets.
- ✅ **Total layout control** — anything React can render (cards, grids, sparklines, chips, theming).

## Architecture

- Each **canvas page** hosts exactly **one** custom-page widget that owns the entire page layout.
- The widget is a `multilineTextboxSpec` whose joined `lines` are:

  ```
  <!-- @custom-page -->
  { "code": "<CommonJS React source>", "manifest": {}, "datasetMap": [ { "alias": "...", "datasetId": "..." } ] }
  ```

- Standard dashboard machinery is unchanged and reused from `02`: the `datasets[]` (with `queryLines`),
  the **Global Filters** page, parameters, `uiSettings.theme`, and deployment. Only the content pages
  are React.
- A single dashboard may **interleave** standard pages (e.g. a `PAGE_TYPE_GLOBAL_FILTERS` page with
  built-in filters) and React custom pages — this is the recommended hybrid shape.

See [`references/custom-page-envelope.md`](references/custom-page-envelope.md) for the exact envelope
and the double-escaping rules.

## Authoring the React

- **CommonJS, not ESM, no JSX.** The exemplar uses:
  ```js
  var R = require('react');
  function App(props) { /* ... */ return R.createElement(...); }
  module.exports.default = App;
  ```
  Author with `R.createElement(tag, props, ...children)`. (Whether the runtime accepts JSX/imports is
  unverified — the observed, working form is `require`/`createElement`/`module.exports.default`.)
- **`viz` is an injected runtime global** (only `react` is `require`d). Do not try to `require('viz')`.
- **Props provided to `App` and passed down:** `props.theme` (`'dark'` | `'light'`), `props.height`,
  and layout hints like `props.flex`. Branch all colors on `props.theme === 'dark'`.

## Data binding — `viz.useCustomPageQuery`

Read a dataset (by its **alias** from `datasetMap`) with the injected hook:

```js
var res = viz.useCustomPageQuery({
  query: {
    datasetName: 'commit',                         // alias from datasetMap, NOT the datasetId
    fields: [
      { fieldName: 'account_name', expression: '`account_name`' },
      { fieldName: 'pace_actual',  expression: '`pace_actual`' }
    ]
  }
});

// Return shape: { rows: [ { account_name: '...', pace_actual: 123 }, ... ] }
if (res && res.rows && res.rows.length) {
  var first = res.rows[0];
  // ...render...
}
```

- `datasetName` is the **alias** declared in `datasetMap`; the alias resolves to a dashboard
  `datasetId` (which equals a dataset's `name` in `datasets[]`).
- `fields[].fieldName` is the key you read on each row; `expression` is the backtick-quoted column.
- Always **guard** on `res && res.rows && res.rows.length` and render a loading/empty state otherwise
  (the exemplar renders skeleton shimmer tiles while data resolves).

## Theming & loading

- Derive a palette from `props.theme`; keep small helpers (`toneFg/toneBg`, currency/percent
  formatters) at module scope. See [`references/authoring-patterns.md`](references/authoring-patterns.md).
- Provide a skeleton/loading component (inject a keyframe once into `document.head`) so the page never
  flashes empty.
- Optional `data-cp-element-id` attributes on elements let the visual editor track them; they are not
  required for rendering.

## Deployment & the escaping trap

A custom page is a normal dashboard widget, so deploy exactly as in `02` (base64 Workspace Import or
`bundle deploy`). The one hazard is **triple nesting**:

1. `code` is a JS string inside
2. the `{code, manifest, datasetMap}` JSON string inside
3. the `.lvdash.json` `multilineTextboxSpec.lines` array.

Build the envelope programmatically (`json.dumps`) rather than by hand — never hand-escape the code
string. See [`references/custom-page-envelope.md`](references/custom-page-envelope.md) for a builder.

## Validation

- `scripts/validate_custom_page.py <dashboard.lvdash.json>` checks: each custom page's envelope parses;
  every `datasetName` used in `viz.useCustomPageQuery(...)` resolves via `datasetMap` to a real dataset
  in `datasets[]`; `module.exports.default` (or `module.exports`) is present; and the content survives a
  base64 round-trip.
- It **cannot** verify React correctness. Always preview in the workspace before shipping.

## Templates

- [`assets/templates/custom-page-single-metric.lvdash.json`](assets/templates/custom-page-single-metric.lvdash.json)
  — minimal 1-dataset page: one dataset, one custom page reading it, theme-aware.
- [`assets/templates/custom-page-composite.lvdash.json`](assets/templates/custom-page-composite.lvdash.json)
  — sanitized composite: KPI card row + a status list, driven by one dataset, with skeleton loading and
  light/dark theming. De-identified (generic `${catalog}.${schema}` sources; no internal names).

## Related skills

- `monitoring/02-databricks-aibi-dashboards` — built-in widgets, datasets, filters, deployment (reused).
- `monitoring/05-databricks-aibi-custom-viz-vega` — documented single-chart custom viz (prefer when a
  single chart suffices).
- `apps_lakebase/` + `databricks-apps` — the documented product for a full custom React app (separate
  from a dashboard).
