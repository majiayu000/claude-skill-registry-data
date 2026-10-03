---
name: report-template
description: Write or override a Typst export template for a console dashboard route — the lookup order, the data.json contract, the shared _lib helpers, template assets, branding, and how to compile one locally. Use whenever a task mentions a .typ file, a PDF export, apps/console/templates, CONSOLE_TEMPLATES_DIR, typst-render, or a 422 template compile error.
---

# Writing a Typst report template

A template decides **document chrome only** — header, section order, captions, page furniture. It
**cannot** decide which panels exist or what they query: `report.panels` arrives already resolved,
already queried, already formatted, in `dashboards.yaml` order.

Contract: `docs/knowledge/export-pipeline.md`. Reasoning: ADR 0015 D5, ADR 0017 D6.

## You usually do not need one

Lookup order is **per file** (`apps/console/src/server/reports/template-resolver.ts:109`):

1. `${CONSOLE_TEMPLATES_DIR}/<route>/report.typ` — an operator's mounted override
2. `apps/console/templates/<route>/report.typ` — shipped in the image
3. `apps/console/templates/_lib/default.typ` — the generic layout

Because of step 3, **a new `dashboards.yaml` route exports on the day it is added**. Write a
per-route template only when that route's document needs different chrome.

## The skeleton

Every template begins exactly like this:

```typst
#import "_lib/report.typ": *

#let report = json(sys.inputs.at("data"))

#show: report-page.with(report)

#panels-in-order(report)
```

`sys.inputs.data` is a **filename, not the payload** — the service writes the JSON beside the
template and passes `--input data=data.json`. `_lib/report.typ` is shipped as an asset with every
render job, so the import resolves inside the sandbox.

## What `_lib/report.typ` gives you

| Helper                                     | Use                                                   |
| ------------------------------------------ | ----------------------------------------------------- |
| `report-page(report, body)`                | The page setup, header, brand mark and footer         |
| `panels-in-order(report)`                  | Every panel, in `dashboards.yaml` order               |
| `panel(p, body)`                           | One panel's frame, for a bespoke layout               |
| `panel-body(report, p)`                    | The default body for one panel                        |
| `panel-chart(p)`                           | Just the SVG, bounded by `chart-max-width`/`-height`  |
| `stat-grid(stats)`                         | A stat panel's figures                                |
| `table-from-rows(report, t)`               | A table panel's rows                                  |
| `panel-unavailable(p)`                     | The "could not be loaded" line — never drop the panel |
| `ink`, `subtle`, `rule-colour`, `hairline` | The print palette                                     |

To reorder or single out panels, look them up by **panel id** — the same ids
`dashboards.yaml` declares.

## Copy is already translated

Typst has no i18n runtime. Every word printed on the **document's** own behalf arrives in
`report.labels` (`generated`, `template`, `noRows`), resolved server-side against the reader's
locale. **Never hard-code an English word in a template** — including in an operator override, which
gets translated chrome for free by reading the same fields.

## Files beside the template

Anything in the template's own directory ships with it (a logo, a watermark, a typeface), walked to
depth 4, with an **8 MiB budget** across all of them. Reference them by their relative path:
`image("watermark.png")`.

Precedence, least specific first: sibling files → configured branding → this document's panel SVGs.
A file dropped in a template directory can give the template artwork; it **cannot** shadow the data
the document is of.

Branding: the **light-theme** mark (`branding.logoLight`) is what prints, because a document is
printed on white. With no readable logo, `branding.name` prints.

## Compile it locally

```sh
# 1. Get the real payload for the route
curl -s 'http://localhost:3000/api/reports/page?path=/admin/overview&range=mtd&format=html' \
  -H 'Cookie: <your dev session>' > /tmp/report.html   # sanity: does the route resolve at all?

# 2. Run the sidecar and let it compile the PDF
pnpm --filter typst-render dev
curl -s 'http://localhost:3000/api/reports/page?path=/admin/overview&range=mtd&format=pdf' \
  -H 'Cookie: <your dev session>' -o /tmp/report.pdf
```

A compile failure comes back as **`422` with Typst's stderr verbatim** plus the file the template
was read from. Read it — it names the line.

`format=csv` and `format=html` never touch Typst, so use them to separate "my template is broken"
from "the data is wrong".

## Verify

```sh
pnpm --filter console test          # template-resolver, template-assets, report-data
pnpm --filter console typecheck
pnpm --filter console build:web     # runs build-report-charts.mjs FIRST
```

## Pitfalls

- **`@preview/...` package imports do not work.** `--package-path` points at an empty directory and
  the sidecar is expected to run with no egress. Templates must be self-contained.
- **System fonts are unavailable** (`--ignore-system-fonts`). Ship a typeface beside the template if
  you need one.
- **`[param]` route segments are written literally** in the directory name:
  `templates/admin/usage/actors/[actorId]/report.typ`.
- **The override is per FILE, not per directory.** A ConfigMap carrying one file overrides exactly
  one document; it does not blank out the others under that path.
- **A changed `ui-web` chart is not in the PDF until `scripts/build-report-charts.mjs` runs.** It is
  bundled ahead of the Next build and outside its graph.
- **Never let a template drop a panel silently.** Use `panel-unavailable` — a missing section is
  indistinguishable from a panel that had no data.
- **Do not add a per-route template just to change a title.** Titles come from `dashboards.yaml`
  keys.
