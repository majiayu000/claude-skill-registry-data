---
name: sheet-generation-api
description: Generate CSV, Markdown, and XLSX spreadsheets from structured tabular data.
---

# Sheet Generation API

Generate CSV, Markdown, and XLSX spreadsheets from structured tabular data.

**Cost:** 1 credits per request

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Generate CSV, Markdown, and XLSX spreadsheets from a single API call. Send column definitions and row data as structured JSON, and receive the rendered spreadsheet as base64-encoded JSON in the response.

## Key Features

- **Three Output Formats** -- Generate CSV, Markdown tables, or XLSX from one unified input structure.
- **Positional Rows** -- Rows are arrays of cells matching column order. No key mapping needed.
- **Cell Formatting** -- Format types: text, number, decimal, currency, percentage, date, datetime, time, custom.
- **Currency Support** -- ISO 4217 currency codes with configurable number separator styles.
- **Rich Styling** -- Base styles for headers and body, with per-cell overrides for font, color, alignment, and more (XLSX).
- **Custom Fonts** -- Upload font files (base64-encoded) with weight and style metadata (XLSX).
- **Multiple Sheets** -- XLSX supports multiple worksheets. Markdown renders each sheet as a headed table. CSV supports a single sheet.
- **Merged Cells** -- Combine cells across rows and columns using from/to ranges on individual cells (XLSX).
- **Formulas** -- Any cell value starting with `=` is treated as a formula. Native in XLSX, server-evaluated for CSV and Markdown.

## Overview

The Sheet Generation API creates spreadsheets from a JSON definition. You send a format, column definitions, row data, and optional styles, and receive the rendered spreadsheet as base64-encoded JSON.

**Endpoint:** `POST /sheet-generation/v1/generate`

**Supported output formats:** CSV, Markdown, XLSX

## Request Format

<!-- tabs -->

```bash
curl -X POST \
  https://api.iterationlayer.com/sheet-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "xlsx",
    "sheets": [
      {
        "name": "Invoices",
        "columns": [
          {
            "name": "Company",
            "width": 20
          },
          {
            "name": "Total",
            "width": 15
          }
        ],
        "rows": [
          [
            {
              "value": "Acme Corp"
            },
            {
              "value": 1500.50,
              "format": "currency",
              "currency_code": "EUR"
            }
          ]
        ]
      }
    ]
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({
  apiKey: "YOUR_API_KEY",
});

const result = await client.generateSheet({
  format: "xlsx",
  sheets: [
    {
      name: "Invoices",
      columns: [
        {
          name: "Company",
          width: 20,
        },
        {
          name: "Total",
          width: 15,
        },
      ],
      rows: [
        [
          {
            value: "Acme Corp",
          },
          {
            value: 1500.50,
            format: "currency",
            currency_code: "EUR",
          },
        ],
      ],
    },
  ],
});
// result.buffer is a Uint8Array
// result.mime_type is "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_sheet(
    format="xlsx",
    sheets=[
        {
            "name": "Invoices",
            "columns": [
                {
                    "name": "Company",
                    "width": 20
                },
                {
                    "name": "Total",
                    "width": 15
                },
            ],
            "rows": [
                [
                    {
                        "value": "Acme Corp"
                    },
                    {
                        "value": 1500.50,
                        "format": "currency",
                        "currency_code": "EUR",
                    },
                ],
            ],
        },
    ],
)
# result["buffer"] is bytes
# result["mime_type"] is "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
```

```go
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")

result, err := client.GenerateSheet(
	il.GenerateSheetRequest{
		Format: "xlsx",
		Sheets: []il.Sheet{
			{
				Name: "Invoices",
				Columns: []il.SheetColumn{
					{
						Name:  "Company",
						Width: 20,
					},
					{
						Name:  "Total",
						Width: 15,
					},
				},
				Rows: [][]il.SheetCell{
					{
						{
							Value: "Acme Corp",
						},
						{
							Value:        1500.50,
							Format:       "currency",
							CurrencyCode: "EUR",
						},
					},
				},
			},
		},
	},
)
// result.Buffer is []byte
// result.MimeType is "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "buffer": "UEsDBBQAAAAIAA...",
    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  }
}
```

<!-- /tabs -->

## Request Structure

The top-level request has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format` | string | Yes | Output format: `csv`, `markdown`, or `xlsx` |
| `sheets` | array | Yes | Array of sheet definitions (see below) |
| `styles` | object | No | Base styles for headers and body cells |
| `fonts` | array | No | Custom font definitions (base64-encoded font files, XLSX only) |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

## Sheets

Each sheet definition contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Sheet name (default: "Sheet1") |
| `columns` | array | Yes | Column definitions (see below) |
| `rows` | array | No | Positional array of rows. Each row is an array of cells matching column order. |

## Columns

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display header name (min 1 character) |
| `width` | number | No | Column width (XLSX only, must be greater than 0) |

## Rows and Cells

Each row is an array of cells, where each cell's position corresponds to the column at the same index. A cell can be a bare value (string, number, boolean, or null) or a structured object with formatting:

**Bare value:**

```json
[
  "Acme Corp",
  1500.50
]
```

**Structured cells with format and styles:**

```json
[
  {
    "value": "Acme Corp"
  },
  {
    "value": 1500.50,
    "format": "currency",
    "currency_code": "EUR",
    "styles": {
      "is_bold": true,
      "font_color": "#008000"
    }
  }
]
```

You can mix bare values and structured cells in the same row. A row may have fewer cells than columns -- trailing cells default to empty.

### Cell Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | any | No | Cell value. Strings starting with `=` are treated as formulas. |
| `format` | string | No | Cell format (default: `text`). See Cell Formats below. |
| `currency_code` | string | No | ISO 4217 currency code (default: `USD`). Used with `currency` format. |
| `number_style` | string | No | Number separator style (default: `comma_period`). Used with `number`, `decimal`, and `currency` formats. |
| `date_style` | string | No | Excel date format code (e.g., `dd/mm/yyyy`). Used with `date`, `datetime`, and `time` formats. See Date Styles below. |
| `styles` | object | No | Per-cell style overrides (XLSX only). See Cell Styles below. |
| `from_col` | integer | No | Start column for merge range (0-based). See Merged Cells. |
| `to_col` | integer | No | End column for merge range (0-based). See Merged Cells. |
| `from_row` | integer | No | Start row for merge range (0-based). See Merged Cells. |
| `to_row` | integer | No | End row for merge range (0-based). See Merged Cells. |

### Cell Formats

| Format | Description | CSV/Markdown Example | XLSX Format Code |
|--------|-------------|---------------------|------------------|
| `text` | Plain text (default) | `Acme Corp` | -- |
| `number` | Integer with thousands separator | `1,500` | `#,##0` |
| `decimal` | Two decimal places | `1,500.50` | `#,##0.00` |
| `currency` | Currency symbol with decimals | `$1,500.50` | `$#,##0.00` |
| `percentage` | Multiplied by 100 with % | `75.00%` | `0.00%` |
| `date` | Date string | `2026-01-15` | `yyyy-mm-dd` (default, customizable via `date_style`) |
| `datetime` | Date and time string | `2026-01-15 10:30:00` | `yyyy-mm-dd hh:mm:ss` (default, customizable via `date_style`) |
| `time` | Time string | `10:30:00` | `hh:mm:ss` (default, customizable via `date_style`) |
| `custom` | Custom Excel format code | (as-is) | Via `number_format` in styles |

### Cell Styles

Cell-level style overrides (XLSX only, ignored for CSV/Markdown):

| Field | Type | Description |
|-------|------|-------------|
| `font_family` | string | Font family name |
| `font_size_in_pt` | number | Font size in points (>= 1) |
| `is_bold` | boolean | Bold text |
| `is_italic` | boolean | Italic text |
| `font_color` | string | Font color as hex (e.g., `#FF0000`) |
| `background_color` | string | Cell background color as hex |
| `horizontal_alignment` | string | One of: `left`, `center`, `right` |
| `number_format` | string | Custom Excel number format code (used with `format: "custom"`) |

## Styles

The top-level `styles` object defines base styles for header and body cells:

```json
{
  "styles": {
    "header": {
      "font_family": "Helvetica",
      "font_size_in_pt": 12,
      "is_bold": true,
      "background_color": "#4472C4",
      "font_color": "#FFFFFF"
    },
    "body": {
      "font_family": "Helvetica",
      "font_size_in_pt": 11,
      "font_color": "#000000"
    }
  }
}
```

Header styles apply to the column header row. Body styles apply to all data cells. Per-cell `styles` overrides take precedence.

## Custom Fonts

Upload custom fonts as base64-encoded buffers (XLSX only). Each font definition requires a name, weight, style, and the font file data.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Font family name (min 1 character) |
| `weight` | string | Yes | One of: `thin`, `extralight`, `light`, `regular`, `medium`, `semibold`, `bold`, `extrabold`, `black` |
| `style` | string | Yes | One of: `normal`, `italic` |
| `buffer` | string | Yes | Base64-encoded font file (TTF, OTF, WOFF, or WOFF2) |

## Merged Cells

Merge a range of cells by setting `from_col`, `to_col`, `from_row`, and `to_row` on the cell itself (XLSX only). The merge range is 0-based and inclusive. The cell's `value` is displayed in the merged area.

```json
{
  "format": "xlsx",
  "sheets": [
    {
      "name": "Report",
      "columns": [
        {
          "name": "A",
          "width": 20
        },
        {
          "name": "B",
          "width": 20
        },
        {
          "name": "C",
          "width": 20
        }
      ],
      "rows": [
        [
          {
            "value": "Summary",
            "from_col": 0,
            "to_col": 2,
            "from_row": 0,
            "to_row": 0,
            "styles": {
              "is_bold": true,
              "horizontal_alignment": "center"
            }
          }
        ],
        [
          "Detail A",
          "Detail B",
          "Detail C"
        ]
      ]
    }
  ]
}
```

In this example, the first row's single cell spans all three columns (columns 0 through 2). The second row has three separate cells.

## Formulas

Any cell whose `value` is a string starting with `=` is treated as a formula. No separate formula array is needed -- formulas are just cells.

```json
{
  "format": "xlsx",
  "sheets": [
    {
      "name": "Totals",
      "columns": [
        {
          "name": "Item",
          "width": 20
        },
        {
          "name": "Amount",
          "width": 15
        }
      ],
      "rows": [
        [
          "Widget A",
          {
            "value": 100.00,
            "format": "currency"
          }
        ],
        [
          "Widget B",
          {
            "value": 250.00,
            "format": "currency"
          }
        ],
        [
          {
            "value": "Total",
            "styles": {
              "is_bold": true
            }
          },
          {
            "value": "=SUM(B2:B3)",
            "format": "currency"
          }
        ]
      ]
    }
  ]
}
```

For XLSX, formulas are written natively and evaluated by Excel. For CSV and Markdown, simple aggregation formulas (SUM, AVERAGE, COUNT, MIN, MAX) are evaluated server-side. Unsupported formulas are written as raw strings.

## Multiple Sheets

XLSX and Markdown support multiple sheets. CSV supports only one sheet.

**XLSX:** Each sheet becomes a separate worksheet in the workbook.

**Markdown:** Each sheet is rendered as a `## Sheet Name` heading followed by a markdown table:

```markdown
## Invoices

| Company | Total |
| --- | --- |
| Acme Corp | EUR 1,500.50 |

## Payments

| Date | Amount |
| --- | --- |
| 2026-01-15 | $500.00 |
```

**CSV:** If more than one sheet is provided, the API returns a 400 error.

## Currency Codes

The `currency_code` field accepts any ISO 4217 currency code. It is used with the `currency` format to determine the currency symbol displayed in the cell. Defaults to `USD` if not specified.

```json
[
  {
    "value": 1500.50,
    "format": "currency",
    "currency_code": "EUR"
  },
  {
    "value": 2400.00,
    "format": "currency",
    "currency_code": "JPY"
  },
  {
    "value": 899.99,
    "format": "currency",
    "currency_code": "GBP"
  }
]
```

## Number Styles

The `number_style` field controls the thousands and decimal separators for `number`, `decimal`, and `currency` formats. Defaults to `comma_period` if not specified.

| Style | Thousands Separator | Decimal Separator | Example |
|-------|--------------------|--------------------|---------|
| `comma_period` | `,` | `.` | `1,500.50` |
| `period_comma` | `.` | `,` | `1.500,50` |
| `space_comma` | ` ` | `,` | `1 500,50` |
| `space_period` | ` ` | `.` | `1 500.50` |

```json
[
  {
    "value": 1500.50,
    "format": "decimal",
    "number_style": "period_comma"
  }
]
```

## Date Styles

The `date_style` field accepts an Excel date format code string to control how `date`, `datetime`, and `time` values are displayed. The format code is passed directly to XLSX as the cell number format, and interpreted for CSV/Markdown rendering.

| Token | Description | Example |
|-------|-------------|---------|
| `yyyy` | 4-digit year | `2026` |
| `yy` | 2-digit year | `26` |
| `mmmm` | Full month name | `March` |
| `mmm` | Abbreviated month name | `Mar` |
| `mm` | 2-digit month (or minutes after `hh`/`h`) | `03` |
| `m` | Month without leading zero (or minutes after `hh`/`h`) | `3` |
| `dd` | 2-digit day | `21` |
| `d` | Day without leading zero | `21` |
| `hh` | 2-digit hour | `14` |
| `h` | Hour without leading zero | `2` |
| `ss` | 2-digit seconds | `05` |
| `s` | Seconds without leading zero | `5` |

Default values if `date_style` is not specified:
- `date`: `yyyy-mm-dd`
- `datetime`: `yyyy-mm-dd hh:mm:ss`
- `time`: `hh:mm:ss`

```json
[
  {
    "value": "2026-03-21",
    "format": "date",
    "date_style": "dd/mm/yyyy"
  },
  {
    "value": "2026-03-21 14:30:00",
    "format": "datetime",
    "date_style": "d mmmm yyyy hh:mm:ss"
  },
  {
    "value": "14:30:00",
    "format": "time",
    "date_style": "hh:mm"
  }
]
```

## Feature Comparison by Format

| Feature | XLSX | CSV | Markdown |
|---------|------|-----|----------|
| Multiple Sheets | ✅ | ❌ | ✅ |
| Cell Formatting | ✅ | ❌ | ❌ |
| Custom Fonts | ✅ | ❌ | ❌ |
| Merged Cells | ✅ | ❌ | ❌ |
| Formulas | ✅ (native) | ✅ (server-evaluated) | ✅ (server-evaluated) |
| Number Formats | ✅ (native) | ✅ (string rendering) | ✅ (string rendering) |
| Currency Codes | ✅ | ✅ | ✅ |
| Number Styles | ✅ | ✅ | ✅ |
| Date Styles | ✅ | ✅ | ✅ |
| Column Widths | ✅ | ❌ | ❌ |
| Header/Body Styles | ✅ | ❌ | ❌ |

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request (validation errors, missing required fields, CSV with multiple sheets) |
| 401 | Missing or invalid API key |
| 422 | Processing error (spreadsheet rendering failure) |
| 429 | Rate limit exceeded |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/sheet-generation)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
