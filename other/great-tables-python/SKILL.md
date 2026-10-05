---
name: great-tables-python
description: Use for writing, reviewing, debugging, or testing publication-quality display tables in Python with Great Tables, including GT construction, stub and row groups, headers and spanners, labels, numeric/date formatting, targeted styles, footnotes/source notes, HTML/LaTeX/image export, and render verification. Do not use for dataframe computation, interactive data grids, charts, or plain console tables.
argument-hint: "[Great Tables display-table task, formatting, styling, or export]"
---

# Great Tables Python

Build a display table as an output artifact. Transform and validate data before
`GT`; then use the table pipeline to communicate structure, formatting,
annotation, and emphasis without changing analytical values.

## Boundary

Use this skill when a project imports `great_tables` or explicitly requests
Great Tables. Do not use a `GT` object as a dataframe, compute business metrics
inside presentation formatting, replace an interactive grid, or route a chart
request here. Preserve the required render boundary: notebook/browser, HTML
fragment/page, LaTeX, image, or PDF.

## Know the objects

| Object | Meaning | Responsibility |
|---|---|---|
| Input dataframe | Analytical rows and columns | Own filtering, sorting, grouping calculations, joins, and typed values. |
| `GT` | Chainable display-table specification | Own visible structure, labels, formatting, annotation, styles, options, and export. |
| Stub / row group | Row-label and hierarchical row structure | Give records readable identity; not a hidden dataframe index. |
| Column label / spanner | Header hierarchy | Group contiguous related columns with stable IDs when later referenced. |
| Formatter | Converts stored values to displayed text | Currency, number, percent, date/time, missing text, locale; values remain analytical inputs. |
| `loc` / selector | Targets a structural region or subset | Scope styles/footnotes precisely. |
| Render/export method | Materializes host-specific output | HTML, LaTeX, browser/notebook display, raster/PDF with external renderer. |

Read [the display-table model](references/table-model.md) before choosing stub,
groups, column order, spanners, or annotations.

## Ordered workflow

1. Recover the audience, output host, row grain, sort order, units, locale,
   significant digits, missing-value wording, and accessibility requirements.
2. Prepare a small typed dataframe containing only display rows and fields.
   Compute totals, ranks, percentages, and flags upstream and test them there.
3. Create `GT(data, ...)`; define stub and row groups only from stable columns.
4. Establish structure before decoration: title/subtitle, column order and
   labels, spanners, stubhead, group labels, source notes, and footnotes.
5. Apply semantic formatting by column/row target. Do not convert numeric/date
   columns to strings upstream merely for commas or symbols.
6. Apply minimal targeted styling after formatting. Derive emphasis from an
   explicit data condition, not hard-coded row positions when rows can reorder.
7. Export through the method matching the artifact. Verify values and structure
   separately from the rendered appearance and environment prerequisites.

## Intent to API family

| Intent | Use | Invariant |
|---|---|---|
| Title/subtitle | `tab_header` | States subject and scope; does not repeat every column. |
| Human row identity | stub / `rowname_col` | Labels remain unique within their declared group. |
| Row sections | `groupname_col` / row-group methods | Input ordering and group membership are deliberate. |
| Group related columns | `tab_spanner` | Selected columns are contiguous or movement from `gather` is explicitly accepted. |
| Rename visible columns | column-label methods | Source field names remain traceable. |
| Currency/number/percent/date | matching `fmt_*` method | Units, locale, decimals/significant figures, and missing values are defined. |
| Conditional text/value transformation | substitution/format APIs or upstream derived field | Raw analytical meaning is preserved and tested. |
| Highlight cells | `tab_style(style=..., locations=loc...)` | Target is structural/condition-based and styling has semantic purpose. |
| Explain a value | footnote targeted to label/body location | Marker and source remain unambiguous. |
| Embed in application/email | `as_raw_html` with appropriate fragment/page/CSS mode | Raw HTML trust and host CSS policy are explicit. |
| Publication file | `gtsave`, LaTeX, or raw HTML boundary | Required browser/render dependencies and output file are verified. |

## Canonical anchor

```python
from great_tables import GT, md


def revenue_table(data):
    # variance_pct contains proportions: 0.125 means 12.5%.
    return (
        GT(data, rowname_col="region", locale="en")
        .tab_header(
            title="Regional revenue",
            subtitle=md("Reported in **USD**"),
        )
        .tab_spanner(
            label="Revenue",
            columns=["actual", "budget"],
            id="revenue",
        )
        .fmt_currency(columns=["actual", "budget"], currency="USD")
        .fmt_percent(columns="variance_pct", decimals=1)
    )
```

Return the `GT` object from builders. Do not call `show()` or write a file in a
pure table-construction function. `fmt_percent` scales proportional inputs by
100 by default. If the source already stores percentage points, declare that
contract and set the installed API's no-scaling option explicitly.

## Formatting and styling rules

- Formatting controls representation; styling controls appearance. Do not use
  CSS color to encode the only copy of a value or status.
- Prefer semantic formatter methods to upstream string formatting so sorting,
  filtering, summaries, and formatter targeting retain typed values.
- Use an explicit locale at the table or formatter boundary when separators,
  symbols, dates, or language are contractual.
- Choose decimals or significant figures from measurement precision; never
  imply precision absent from the source.
- Give later-referenced spanners explicit stable IDs. A label containing markup
  is not a reliable identifier.
- Treat `html(...)` as trusted raw markup. Do not pass untrusted data through it;
  use escaped/plain text or a sanitized policy.

Read [formatting and styling](references/format-style.md).

## Render boundary and verification

HTML fragments, full pages, email-inline CSS, LaTeX, and browser-captured
images have different requirements. Image/PDF export can require a browser and
optional renderer packages; successful `GT` construction does not prove export.
Read [render and testing](references/render-testing.md).

Inspect the installed version of Great Tables before using drift-sensitive
formatter, selector, spanner, or export signatures. The package was absent from
this foundry during authoring, so examples are official-source-grounded but not
locally rendered.

Completion requires: input values/grain/order tested upstream; visible labels,
units, locale, rounding, and missing text correct; spanner/stub/group structure
matches the contract; styles target intended cells after reordering; raw HTML is
trusted or avoided; the requested artifact exists and renders in its real host;
and missing browser/font/export evidence is reported rather than assumed.

## References

- [Display-table object model](references/table-model.md)
- [Formatting and styling](references/format-style.md)
- [Render boundaries and testing](references/render-testing.md)
