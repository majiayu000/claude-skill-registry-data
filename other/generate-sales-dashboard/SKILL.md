---
name: generate-sales-dashboard
description: Generate a multi-sheet XLSX workbook with quarterly revenue, expenses, and summary formulas.
---

# Generate Sales Dashboard

SaaS companies and analytics teams use this recipe to generate periodic financial dashboards. Two worksheets capture quarterly revenue by product line and operating expenses, with formulas computing totals and merged header cells for a polished executive-ready layout.

## APIs Used

Sheet Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/sheet-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "xlsx",
    "styles": {
      "header": {
        "font_family": "Helvetica",
        "font_size_in_pt": 11,
        "is_bold": true,
        "background_color": "#4472C4",
        "font_color": "#FFFFFF"
      },
      "body": {
        "font_family": "Helvetica",
        "font_size_in_pt": 11,
        "font_color": "#333333"
      }
    },
    "sheets": [
      {
        "name": "Revenue",
        "columns": [
          {
            "name": "Product Line",
            "width": 24,
          },
          {
            "name": "Q1 2026",
            "width": 14,
          },
          {
            "name": "Q2 2026",
            "width": 14,
          },
          {
            "name": "Q3 2026",
            "width": 14,
          },
          {
            "name": "Q4 2026",
            "width": 14,
          },
          {
            "name": "Annual Total",
            "width": 16,
          }
        ],
        "rows": [
          [
            {
              "value": "2026 Revenue by Product Line",
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 14,
              },
              "from_col": 0,
              "to_col": 5,
            }
          ],
          [
            {
              "value": "",
            }
          ],
          [
            {
              "value": "Platform Subscriptions",
            },
            {
              "value": 245000,
              "format": "currency",
            },
            {
              "value": 268000,
              "format": "currency",
            },
            {
              "value": 291000,
              "format": "currency",
            },
            {
              "value": 312000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "API Usage (Pay-as-you-go)",
            },
            {
              "value": 89000,
              "format": "currency",
            },
            {
              "value": 102000,
              "format": "currency",
            },
            {
              "value": 118000,
              "format": "currency",
            },
            {
              "value": 134000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "Enterprise Contracts",
            },
            {
              "value": 180000,
              "format": "currency",
            },
            {
              "value": 180000,
              "format": "currency",
            },
            {
              "value": 240000,
              "format": "currency",
            },
            {
              "value": 240000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "Professional Services",
            },
            {
              "value": 45000,
              "format": "currency",
            },
            {
              "value": 52000,
              "format": "currency",
            },
            {
              "value": 48000,
              "format": "currency",
            },
            {
              "value": 61000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "",
            }
          ],
          [
            {
              "value": "Quarterly Total",
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 12,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 12,
              },
            }
          ]
        ],
        "formulas": [
          {
            "row": 2,
            "col": 5,
            "expression": "=SUM(B3:E3)",
          },
          {
            "row": 3,
            "col": 5,
            "expression": "=SUM(B4:E4)",
          },
          {
            "row": 4,
            "col": 5,
            "expression": "=SUM(B5:E5)",
          },
          {
            "row": 5,
            "col": 5,
            "expression": "=SUM(B6:E6)",
          },
          {
            "row": 7,
            "col": 1,
            "expression": "=SUM(B3:B6)",
          },
          {
            "row": 7,
            "col": 2,
            "expression": "=SUM(C3:C6)",
          },
          {
            "row": 7,
            "col": 3,
            "expression": "=SUM(D3:D6)",
          },
          {
            "row": 7,
            "col": 4,
            "expression": "=SUM(E3:E6)",
          },
          {
            "row": 7,
            "col": 5,
            "expression": "=SUM(F3:F6)",
          }
        ],
        "merged_cells": [
          {
            "start_row": 0,
            "start_col": 0,
            "end_row": 0,
            "end_col": 5,
          }
        ]
      },
      {
        "name": "Expenses",
        "columns": [
          {
            "name": "Category",
            "width": 24,
          },
          {
            "name": "Q1 2026",
            "width": 14,
          },
          {
            "name": "Q2 2026",
            "width": 14,
          },
          {
            "name": "Q3 2026",
            "width": 14,
          },
          {
            "name": "Q4 2026",
            "width": 14,
          },
          {
            "name": "Annual Total",
            "width": 16,
          }
        ],
        "rows": [
          [
            {
              "value": "2026 Operating Expenses",
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 14,
              },
              "from_col": 0,
              "to_col": 5,
            }
          ],
          [
            {
              "value": "",
            }
          ],
          [
            {
              "value": "Cloud Infrastructure",
            },
            {
              "value": 42000,
              "format": "currency",
            },
            {
              "value": 45000,
              "format": "currency",
            },
            {
              "value": 48000,
              "format": "currency",
            },
            {
              "value": 51000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "Salaries & Benefits",
            },
            {
              "value": 320000,
              "format": "currency",
            },
            {
              "value": 320000,
              "format": "currency",
            },
            {
              "value": 345000,
              "format": "currency",
            },
            {
              "value": 345000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "Marketing & Advertising",
            },
            {
              "value": 28000,
              "format": "currency",
            },
            {
              "value": 35000,
              "format": "currency",
            },
            {
              "value": 32000,
              "format": "currency",
            },
            {
              "value": 40000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "Office & Operations",
            },
            {
              "value": 18000,
              "format": "currency",
            },
            {
              "value": 18000,
              "format": "currency",
            },
            {
              "value": 19000,
              "format": "currency",
            },
            {
              "value": 19000,
              "format": "currency",
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            }
          ],
          [
            {
              "value": "",
            }
          ],
          [
            {
              "value": "Quarterly Total",
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 12,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
              },
            },
            {
              "value": null,
              "styles": {
                "is_bold": true,
                "font_size_in_pt": 12,
              },
            }
          ]
        ],
        "formulas": [
          {
            "row": 2,
            "col": 5,
            "expression": "=SUM(B3:E3)",
          },
          {
            "row": 3,
            "col": 5,
            "expression": "=SUM(B4:E4)",
          },
          {
            "row": 4,
            "col": 5,
            "expression": "=SUM(B5:E5)",
          },
          {
            "row": 5,
            "col": 5,
            "expression": "=SUM(B6:E6)",
          },
          {
            "row": 7,
            "col": 1,
            "expression": "=SUM(B3:B6)",
          },
          {
            "row": 7,
            "col": 2,
            "expression": "=SUM(C3:C6)",
          },
          {
            "row": 7,
            "col": 3,
            "expression": "=SUM(D3:D6)",
          },
          {
            "row": 7,
            "col": 4,
            "expression": "=SUM(E3:E6)",
          },
          {
            "row": 7,
            "col": 5,
            "expression": "=SUM(F3:F6)",
          }
        ],
        "merged_cells": [
          {
            "start_row": 0,
            "start_col": 0,
            "end_row": 0,
            "end_col": 5,
          }
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
  styles: {
    header: {
      font_family: "Helvetica",
      font_size_in_pt: 11,
      is_bold: true,
      background_color: "#4472C4",
      font_color: "#FFFFFF",
    },
    body: {
      font_family: "Helvetica",
      font_size_in_pt: 11,
      font_color: "#333333",
    },
  },
  sheets: [
    {
      name: "Revenue",
      columns: [
        {
          name: "Product Line",
          width: 24,
        },
        {
          name: "Q1 2026",
          width: 14,
        },
        {
          name: "Q2 2026",
          width: 14,
        },
        {
          name: "Q3 2026",
          width: 14,
        },
        {
          name: "Q4 2026",
          width: 14,
        },
        {
          name: "Annual Total",
          width: 16,
        },
      ],
      rows: [
        [
          {
            value: "2026 Revenue by Product Line",
            styles: {
              is_bold: true,
              font_size_in_pt: 14,
            },
            from_col: 0,
            to_col: 5,
          },
        ],
        [
          {
            value: "",
          },
        ],
        [
          {
            value: "Platform Subscriptions",
          },
          {
            value: 245000,
            format: "currency",
          },
          {
            value: 268000,
            format: "currency",
          },
          {
            value: 291000,
            format: "currency",
          },
          {
            value: 312000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "API Usage (Pay-as-you-go)",
          },
          {
            value: 89000,
            format: "currency",
          },
          {
            value: 102000,
            format: "currency",
          },
          {
            value: 118000,
            format: "currency",
          },
          {
            value: 134000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "Enterprise Contracts",
          },
          {
            value: 180000,
            format: "currency",
          },
          {
            value: 180000,
            format: "currency",
          },
          {
            value: 240000,
            format: "currency",
          },
          {
            value: 240000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "Professional Services",
          },
          {
            value: 45000,
            format: "currency",
          },
          {
            value: 52000,
            format: "currency",
          },
          {
            value: 48000,
            format: "currency",
          },
          {
            value: 61000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "",
          },
        ],
        [
          {
            value: "Quarterly Total",
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
        ],
      ],
      formulas: [
        {
          row: 2,
          col: 5,
          expression: "=SUM(B3:E3)",
        },
        {
          row: 3,
          col: 5,
          expression: "=SUM(B4:E4)",
        },
        {
          row: 4,
          col: 5,
          expression: "=SUM(B5:E5)",
        },
        {
          row: 5,
          col: 5,
          expression: "=SUM(B6:E6)",
        },
        {
          row: 7,
          col: 1,
          expression: "=SUM(B3:B6)",
        },
        {
          row: 7,
          col: 2,
          expression: "=SUM(C3:C6)",
        },
        {
          row: 7,
          col: 3,
          expression: "=SUM(D3:D6)",
        },
        {
          row: 7,
          col: 4,
          expression: "=SUM(E3:E6)",
        },
        {
          row: 7,
          col: 5,
          expression: "=SUM(F3:F6)",
        },
      ],
      merged_cells: [
        {
          start_row: 0,
          start_col: 0,
          end_row: 0,
          end_col: 5,
        },
      ],
    },
    {
      name: "Expenses",
      columns: [
        {
          name: "Category",
          width: 24,
        },
        {
          name: "Q1 2026",
          width: 14,
        },
        {
          name: "Q2 2026",
          width: 14,
        },
        {
          name: "Q3 2026",
          width: 14,
        },
        {
          name: "Q4 2026",
          width: 14,
        },
        {
          name: "Annual Total",
          width: 16,
        },
      ],
      rows: [
        [
          {
            value: "2026 Operating Expenses",
            styles: {
              is_bold: true,
              font_size_in_pt: 14,
            },
            from_col: 0,
            to_col: 5,
          },
        ],
        [
          {
            value: "",
          },
        ],
        [
          {
            value: "Cloud Infrastructure",
          },
          {
            value: 42000,
            format: "currency",
          },
          {
            value: 45000,
            format: "currency",
          },
          {
            value: 48000,
            format: "currency",
          },
          {
            value: 51000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "Salaries & Benefits",
          },
          {
            value: 320000,
            format: "currency",
          },
          {
            value: 320000,
            format: "currency",
          },
          {
            value: 345000,
            format: "currency",
          },
          {
            value: 345000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "Marketing & Advertising",
          },
          {
            value: 28000,
            format: "currency",
          },
          {
            value: 35000,
            format: "currency",
          },
          {
            value: 32000,
            format: "currency",
          },
          {
            value: 40000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "Office & Operations",
          },
          {
            value: 18000,
            format: "currency",
          },
          {
            value: 18000,
            format: "currency",
          },
          {
            value: 19000,
            format: "currency",
          },
          {
            value: 19000,
            format: "currency",
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
        ],
        [
          {
            value: "",
          },
        ],
        [
          {
            value: "Quarterly Total",
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
        ],
      ],
      formulas: [
        {
          row: 2,
          col: 5,
          expression: "=SUM(B3:E3)",
        },
        {
          row: 3,
          col: 5,
          expression: "=SUM(B4:E4)",
        },
        {
          row: 4,
          col: 5,
          expression: "=SUM(B5:E5)",
        },
        {
          row: 5,
          col: 5,
          expression: "=SUM(B6:E6)",
        },
        {
          row: 7,
          col: 1,
          expression: "=SUM(B3:B6)",
        },
        {
          row: 7,
          col: 2,
          expression: "=SUM(C3:C6)",
        },
        {
          row: 7,
          col: 3,
          expression: "=SUM(D3:D6)",
        },
        {
          row: 7,
          col: 4,
          expression: "=SUM(E3:E6)",
        },
        {
          row: 7,
          col: 5,
          expression: "=SUM(F3:F6)",
        },
      ],
      merged_cells: [
        {
          start_row: 0,
          start_col: 0,
          end_row: 0,
          end_col: 5,
        },
      ],
    },
  ],
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_sheet(
    format="xlsx",
    styles={
        "header": {
            "font_family": "Helvetica",
            "font_size_in_pt": 11,
            "is_bold": True,
            "background_color": "#4472C4",
            "font_color": "#FFFFFF",
        },
        "body": {
            "font_family": "Helvetica",
            "font_size_in_pt": 11,
            "font_color": "#333333",
        },
    },
    sheets=[
        {
            "name": "Revenue",
            "columns": [
                {
                    "name": "Product Line",
                    "width": 24,
                },
                {
                    "name": "Q1 2026",
                    "width": 14,
                },
                {
                    "name": "Q2 2026",
                    "width": 14,
                },
                {
                    "name": "Q3 2026",
                    "width": 14,
                },
                {
                    "name": "Q4 2026",
                    "width": 14,
                },
                {
                    "name": "Annual Total",
                    "width": 16,
                },
            ],
            "rows": [
                [
                    {
                        "value": "2026 Revenue by Product Line",
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 14,
                        },
                        "from_col": 0,
                        "to_col": 5,
                    },
                ],
                [
                    {
                        "value": "",
                    },
                ],
                [
                    {
                        "value": "Platform Subscriptions",
                    },
                    {
                        "value": 245000,
                        "format": "currency",
                    },
                    {
                        "value": 268000,
                        "format": "currency",
                    },
                    {
                        "value": 291000,
                        "format": "currency",
                    },
                    {
                        "value": 312000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "API Usage (Pay-as-you-go)",
                    },
                    {
                        "value": 89000,
                        "format": "currency",
                    },
                    {
                        "value": 102000,
                        "format": "currency",
                    },
                    {
                        "value": 118000,
                        "format": "currency",
                    },
                    {
                        "value": 134000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "Enterprise Contracts",
                    },
                    {
                        "value": 180000,
                        "format": "currency",
                    },
                    {
                        "value": 180000,
                        "format": "currency",
                    },
                    {
                        "value": 240000,
                        "format": "currency",
                    },
                    {
                        "value": 240000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "Professional Services",
                    },
                    {
                        "value": 45000,
                        "format": "currency",
                    },
                    {
                        "value": 52000,
                        "format": "currency",
                    },
                    {
                        "value": 48000,
                        "format": "currency",
                    },
                    {
                        "value": 61000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "",
                    },
                ],
                [
                    {
                        "value": "Quarterly Total",
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 12,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 12,
                        },
                    },
                ],
            ],
            "formulas": [
                {
                    "row": 2,
                    "col": 5,
                    "expression": "=SUM(B3:E3)",
                },
                {
                    "row": 3,
                    "col": 5,
                    "expression": "=SUM(B4:E4)",
                },
                {
                    "row": 4,
                    "col": 5,
                    "expression": "=SUM(B5:E5)",
                },
                {
                    "row": 5,
                    "col": 5,
                    "expression": "=SUM(B6:E6)",
                },
                {
                    "row": 7,
                    "col": 1,
                    "expression": "=SUM(B3:B6)",
                },
                {
                    "row": 7,
                    "col": 2,
                    "expression": "=SUM(C3:C6)",
                },
                {
                    "row": 7,
                    "col": 3,
                    "expression": "=SUM(D3:D6)",
                },
                {
                    "row": 7,
                    "col": 4,
                    "expression": "=SUM(E3:E6)",
                },
                {
                    "row": 7,
                    "col": 5,
                    "expression": "=SUM(F3:F6)",
                },
            ],
            "merged_cells": [
                {
                    "start_row": 0,
                    "start_col": 0,
                    "end_row": 0,
                    "end_col": 5,
                },
            ],
        },
        {
            "name": "Expenses",
            "columns": [
                {
                    "name": "Category",
                    "width": 24,
                },
                {
                    "name": "Q1 2026",
                    "width": 14,
                },
                {
                    "name": "Q2 2026",
                    "width": 14,
                },
                {
                    "name": "Q3 2026",
                    "width": 14,
                },
                {
                    "name": "Q4 2026",
                    "width": 14,
                },
                {
                    "name": "Annual Total",
                    "width": 16,
                },
            ],
            "rows": [
                [
                    {
                        "value": "2026 Operating Expenses",
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 14,
                        },
                        "from_col": 0,
                        "to_col": 5,
                    },
                ],
                [
                    {
                        "value": "",
                    },
                ],
                [
                    {
                        "value": "Cloud Infrastructure",
                    },
                    {
                        "value": 42000,
                        "format": "currency",
                    },
                    {
                        "value": 45000,
                        "format": "currency",
                    },
                    {
                        "value": 48000,
                        "format": "currency",
                    },
                    {
                        "value": 51000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "Salaries & Benefits",
                    },
                    {
                        "value": 320000,
                        "format": "currency",
                    },
                    {
                        "value": 320000,
                        "format": "currency",
                    },
                    {
                        "value": 345000,
                        "format": "currency",
                    },
                    {
                        "value": 345000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "Marketing & Advertising",
                    },
                    {
                        "value": 28000,
                        "format": "currency",
                    },
                    {
                        "value": 35000,
                        "format": "currency",
                    },
                    {
                        "value": 32000,
                        "format": "currency",
                    },
                    {
                        "value": 40000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "Office & Operations",
                    },
                    {
                        "value": 18000,
                        "format": "currency",
                    },
                    {
                        "value": 18000,
                        "format": "currency",
                    },
                    {
                        "value": 19000,
                        "format": "currency",
                    },
                    {
                        "value": 19000,
                        "format": "currency",
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                ],
                [
                    {
                        "value": "",
                    },
                ],
                [
                    {
                        "value": "Quarterly Total",
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 12,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                        },
                    },
                    {
                        "value": None,
                        "styles": {
                            "is_bold": True,
                            "font_size_in_pt": 12,
                        },
                    },
                ],
            ],
            "formulas": [
                {
                    "row": 2,
                    "col": 5,
                    "expression": "=SUM(B3:E3)",
                },
                {
                    "row": 3,
                    "col": 5,
                    "expression": "=SUM(B4:E4)",
                },
                {
                    "row": 4,
                    "col": 5,
                    "expression": "=SUM(B5:E5)",
                },
                {
                    "row": 5,
                    "col": 5,
                    "expression": "=SUM(B6:E6)",
                },
                {
                    "row": 7,
                    "col": 1,
                    "expression": "=SUM(B3:B6)",
                },
                {
                    "row": 7,
                    "col": 2,
                    "expression": "=SUM(C3:C6)",
                },
                {
                    "row": 7,
                    "col": 3,
                    "expression": "=SUM(D3:D6)",
                },
                {
                    "row": 7,
                    "col": 4,
                    "expression": "=SUM(E3:E6)",
                },
                {
                    "row": 7,
                    "col": 5,
                    "expression": "=SUM(F3:F6)",
                },
            ],
            "merged_cells": [
                {
                    "start_row": 0,
                    "start_col": 0,
                    "end_row": 0,
                    "end_col": 5,
                },
            ],
        },
    ],
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	quarterlyColumns := []il.SheetColumn{
		{
			Name: "Category",
			Width: 24,
		},
		{
			Name: "Q1 2026",
			Width: 14,
		},
		{
			Name: "Q2 2026",
			Width: 14,
		},
		{
			Name: "Q3 2026",
			Width: 14,
		},
		{
			Name: "Q4 2026",
			Width: 14,
		},
		{
			Name: "Annual Total",
			Width: 16,
		},
	}

	result, err := client.GenerateSheet(il.GenerateSheetRequest{
		Format: "xlsx",
		Styles: &il.SheetStyles{
			Header: &il.CellStyle{
				FontFamily:      "Helvetica",
				FontSizeInPt:    11,
				IsBold:          true,
				BackgroundColor: "#4472C4",
				FontColor:       "#FFFFFF",
			},
			Body: &il.CellStyle{
				FontFamily:   "Helvetica",
				FontSizeInPt: 11,
				FontColor:    "#333333",
			},
		},
		Sheets: []il.Sheet{
			{
				Name:    "Revenue",
				Columns: quarterlyColumns,
				Rows: []il.SheetRow{
					{
					{
						Value: "2026 Revenue by Product Line",
						Styles: &il.CellStyle{
							IsBold:       true,
							FontSizeInPt: 14,
						},
						FromCol: intPtr(0),
						ToCol:   intPtr(5),
					},
				},
					{
					{
						Value: "",
					},
				},
					{
						{
							Value: "Platform Subscriptions",
						},
						{
							Value: 245000,
							Format: "currency",
						},
						{
							Value: 268000,
							Format: "currency",
						},
						{
							Value: 291000,
							Format: "currency",
						},
						{
							Value: 312000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "API Usage (Pay-as-you-go)",
						},
						{
							Value: 89000,
							Format: "currency",
						},
						{
							Value: 102000,
							Format: "currency",
						},
						{
							Value: 118000,
							Format: "currency",
						},
						{
							Value: 134000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "Enterprise Contracts",
						},
						{
							Value: 180000,
							Format: "currency",
						},
						{
							Value: 180000,
							Format: "currency",
						},
						{
							Value: 240000,
							Format: "currency",
						},
						{
							Value: 240000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "Professional Services",
						},
						{
							Value: 45000,
							Format: "currency",
						},
						{
							Value: 52000,
							Format: "currency",
						},
						{
							Value: 48000,
							Format: "currency",
						},
						{
							Value: 61000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
					{
						Value: "",
					},
				},
					{
						{
							Value: "Quarterly Total",
							Styles: &il.CellStyle{
								IsBold: true,
								FontSizeInPt: 12,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
								FontSizeInPt: 12,
							},
						},
					},
				},
				Formulas: []il.Formula{
					{
						Row: 2,
						Col: 5,
						Expression: "=SUM(B3:E3)",
					},
					{
						Row: 3,
						Col: 5,
						Expression: "=SUM(B4:E4)",
					},
					{
						Row: 4,
						Col: 5,
						Expression: "=SUM(B5:E5)",
					},
					{
						Row: 5,
						Col: 5,
						Expression: "=SUM(B6:E6)",
					},
					{
						Row: 7,
						Col: 1,
						Expression: "=SUM(B3:B6)",
					},
					{
						Row: 7,
						Col: 2,
						Expression: "=SUM(C3:C6)",
					},
					{
						Row: 7,
						Col: 3,
						Expression: "=SUM(D3:D6)",
					},
					{
						Row: 7,
						Col: 4,
						Expression: "=SUM(E3:E6)",
					},
					{
						Row: 7,
						Col: 5,
						Expression: "=SUM(F3:F6)",
					},
				},
				MergedCells: []il.MergedCell{
					{
						StartRow: 0,
						StartCol: 0,
						EndRow: 0,
						EndCol: 5,
					},
				},
			},
			{
				Name:    "Expenses",
				Columns: quarterlyColumns,
				Rows: []il.SheetRow{
					{
					{
						Value: "2026 Operating Expenses",
						Styles: &il.CellStyle{
							IsBold:       true,
							FontSizeInPt: 14,
						},
						FromCol: intPtr(0),
						ToCol:   intPtr(5),
					},
				},
					{
					{
						Value: "",
					},
				},
					{
						{
							Value: "Cloud Infrastructure",
						},
						{
							Value: 42000,
							Format: "currency",
						},
						{
							Value: 45000,
							Format: "currency",
						},
						{
							Value: 48000,
							Format: "currency",
						},
						{
							Value: 51000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "Salaries & Benefits",
						},
						{
							Value: 320000,
							Format: "currency",
						},
						{
							Value: 320000,
							Format: "currency",
						},
						{
							Value: 345000,
							Format: "currency",
						},
						{
							Value: 345000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "Marketing & Advertising",
						},
						{
							Value: 28000,
							Format: "currency",
						},
						{
							Value: 35000,
							Format: "currency",
						},
						{
							Value: 32000,
							Format: "currency",
						},
						{
							Value: 40000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
						{
							Value: "Office & Operations",
						},
						{
							Value: 18000,
							Format: "currency",
						},
						{
							Value: 18000,
							Format: "currency",
						},
						{
							Value: 19000,
							Format: "currency",
						},
						{
							Value: 19000,
							Format: "currency",
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
					},
					{
					{
						Value: "",
					},
				},
					{
						{
							Value: "Quarterly Total",
							Styles: &il.CellStyle{
								IsBold: true,
								FontSizeInPt: 12,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
							},
						},
						{
							Value: nil,
							Styles: &il.CellStyle{
								IsBold: true,
								FontSizeInPt: 12,
							},
						},
					},
				},
				Formulas: []il.Formula{
					{
						Row: 2,
						Col: 5,
						Expression: "=SUM(B3:E3)",
					},
					{
						Row: 3,
						Col: 5,
						Expression: "=SUM(B4:E4)",
					},
					{
						Row: 4,
						Col: 5,
						Expression: "=SUM(B5:E5)",
					},
					{
						Row: 5,
						Col: 5,
						Expression: "=SUM(B6:E6)",
					},
					{
						Row: 7,
						Col: 1,
						Expression: "=SUM(B3:B6)",
					},
					{
						Row: 7,
						Col: 2,
						Expression: "=SUM(C3:C6)",
					},
					{
						Row: 7,
						Col: 3,
						Expression: "=SUM(D3:D6)",
					},
					{
						Row: 7,
						Col: 4,
						Expression: "=SUM(E3:E6)",
					},
					{
						Row: 7,
						Col: 5,
						Expression: "=SUM(F3:F6)",
					},
				},
				MergedCells: []il.MergedCell{
					{
						StartRow: 0,
						StartCol: 0,
						EndRow: 0,
						EndCol: 5,
					},
				},
			},
		},
	})
	if err != nil {
		panic(err)
	}
	_ = result
}
```

```n8n
{
  "name": "Generate Sales Dashboard",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Sales Dashboard

SaaS companies and analytics teams use this recipe to generate periodic financial dashboards. Two worksheets capture quarterly revenue by product line and operating expenses, with formulas computing totals and merged header cells for a polished executive-ready layout.

**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
        "height": 280,
        "width": 500,
        "color": 2
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        200,
        40
      ],
      "id": "1aced21f-65a5-4b99-bd99-d2d71a425c3d",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Spreadsheet
Resource: **Sheet Generation**

Configure the Sheet Generation parameters below, then connect your credentials.",
        "height": 160,
        "width": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        475,
        100
      ],
      "id": "fc5a8300-5436-4aeb-8049-41fb128f9b40",
      "name": "Step 1 Note"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ],
      "id": "a8e323b1-e07b-4415-b619-1c3cfc3df2ab",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "sheetGeneration",
        "sheetFormat": "xlsx",
        "sheetsJson": "[
  {
    \"name\": \"Revenue\",
    \"columns\": [
      {
        \"name\": \"Product Line\",
        \"width\": 24
      },
      {
        \"name\": \"Q1 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q2 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q3 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q4 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Annual Total\",
        \"width\": 16
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"2026 Revenue by Product Line\",
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 14
          },
          \"from_col\": 0,
          \"to_col\": 5
        }
      ],
      [
        {
          \"value\": \"\"
        }
      ],
      [
        {
          \"value\": \"Platform Subscriptions\"
        },
        {
          \"value\": 245000,
          \"format\": \"currency\"
        },
        {
          \"value\": 268000,
          \"format\": \"currency\"
        },
        {
          \"value\": 291000,
          \"format\": \"currency\"
        },
        {
          \"value\": 312000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"API Usage (Pay-as-you-go)\"
        },
        {
          \"value\": 89000,
          \"format\": \"currency\"
        },
        {
          \"value\": 102000,
          \"format\": \"currency\"
        },
        {
          \"value\": 118000,
          \"format\": \"currency\"
        },
        {
          \"value\": 134000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"Enterprise Contracts\"
        },
        {
          \"value\": 180000,
          \"format\": \"currency\"
        },
        {
          \"value\": 180000,
          \"format\": \"currency\"
        },
        {
          \"value\": 240000,
          \"format\": \"currency\"
        },
        {
          \"value\": 240000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"Professional Services\"
        },
        {
          \"value\": 45000,
          \"format\": \"currency\"
        },
        {
          \"value\": 52000,
          \"format\": \"currency\"
        },
        {
          \"value\": 48000,
          \"format\": \"currency\"
        },
        {
          \"value\": 61000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"\"
        }
      ],
      [
        {
          \"value\": \"Quarterly Total\",
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        }
      ]
    ],
    \"formulas\": [
      {
        \"row\": 2,
        \"col\": 5,
        \"expression\": \"=SUM(B3:E3)\"
      },
      {
        \"row\": 3,
        \"col\": 5,
        \"expression\": \"=SUM(B4:E4)\"
      },
      {
        \"row\": 4,
        \"col\": 5,
        \"expression\": \"=SUM(B5:E5)\"
      },
      {
        \"row\": 5,
        \"col\": 5,
        \"expression\": \"=SUM(B6:E6)\"
      },
      {
        \"row\": 7,
        \"col\": 1,
        \"expression\": \"=SUM(B3:B6)\"
      },
      {
        \"row\": 7,
        \"col\": 2,
        \"expression\": \"=SUM(C3:C6)\"
      },
      {
        \"row\": 7,
        \"col\": 3,
        \"expression\": \"=SUM(D3:D6)\"
      },
      {
        \"row\": 7,
        \"col\": 4,
        \"expression\": \"=SUM(E3:E6)\"
      },
      {
        \"row\": 7,
        \"col\": 5,
        \"expression\": \"=SUM(F3:F6)\"
      }
    ],
    \"merged_cells\": [
      {
        \"start_row\": 0,
        \"start_col\": 0,
        \"end_row\": 0,
        \"end_col\": 5
      }
    ]
  },
  {
    \"name\": \"Expenses\",
    \"columns\": [
      {
        \"name\": \"Category\",
        \"width\": 24
      },
      {
        \"name\": \"Q1 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q2 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q3 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Q4 2026\",
        \"width\": 14
      },
      {
        \"name\": \"Annual Total\",
        \"width\": 16
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"2026 Operating Expenses\",
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 14
          },
          \"from_col\": 0,
          \"to_col\": 5
        }
      ],
      [
        {
          \"value\": \"\"
        }
      ],
      [
        {
          \"value\": \"Cloud Infrastructure\"
        },
        {
          \"value\": 42000,
          \"format\": \"currency\"
        },
        {
          \"value\": 45000,
          \"format\": \"currency\"
        },
        {
          \"value\": 48000,
          \"format\": \"currency\"
        },
        {
          \"value\": 51000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"Salaries & Benefits\"
        },
        {
          \"value\": 320000,
          \"format\": \"currency\"
        },
        {
          \"value\": 320000,
          \"format\": \"currency\"
        },
        {
          \"value\": 345000,
          \"format\": \"currency\"
        },
        {
          \"value\": 345000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"Marketing & Advertising\"
        },
        {
          \"value\": 28000,
          \"format\": \"currency\"
        },
        {
          \"value\": 35000,
          \"format\": \"currency\"
        },
        {
          \"value\": 32000,
          \"format\": \"currency\"
        },
        {
          \"value\": 40000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"Office & Operations\"
        },
        {
          \"value\": 18000,
          \"format\": \"currency\"
        },
        {
          \"value\": 18000,
          \"format\": \"currency\"
        },
        {
          \"value\": 19000,
          \"format\": \"currency\"
        },
        {
          \"value\": 19000,
          \"format\": \"currency\"
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        }
      ],
      [
        {
          \"value\": \"\"
        }
      ],
      [
        {
          \"value\": \"Quarterly Total\",
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        }
      ]
    ],
    \"formulas\": [
      {
        \"row\": 2,
        \"col\": 5,
        \"expression\": \"=SUM(B3:E3)\"
      },
      {
        \"row\": 3,
        \"col\": 5,
        \"expression\": \"=SUM(B4:E4)\"
      },
      {
        \"row\": 4,
        \"col\": 5,
        \"expression\": \"=SUM(B5:E5)\"
      },
      {
        \"row\": 5,
        \"col\": 5,
        \"expression\": \"=SUM(B6:E6)\"
      },
      {
        \"row\": 7,
        \"col\": 1,
        \"expression\": \"=SUM(B3:B6)\"
      },
      {
        \"row\": 7,
        \"col\": 2,
        \"expression\": \"=SUM(C3:C6)\"
      },
      {
        \"row\": 7,
        \"col\": 3,
        \"expression\": \"=SUM(D3:D6)\"
      },
      {
        \"row\": 7,
        \"col\": 4,
        \"expression\": \"=SUM(E3:E6)\"
      },
      {
        \"row\": 7,
        \"col\": 5,
        \"expression\": \"=SUM(F3:F6)\"
      }
    ],
    \"merged_cells\": [
      {
        \"start_row\": 0,
        \"start_col\": 0,
        \"end_row\": 0,
        \"end_col\": 5
      }
    ]
  }
]",
        "sheetStylesJson": "{
  \"header\": {
    \"font_family\": \"Helvetica\",
    \"font_size_in_pt\": 11,
    \"is_bold\": true,
    \"background_color\": \"#4472C4\",
    \"font_color\": \"#FFFFFF\"
  },
  \"body\": {
    \"font_family\": \"Helvetica\",
    \"font_size_in_pt\": 11,
    \"font_color\": \"#333333\"
  }
}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "2742ea6e-75be-4c3e-bddb-d44ba6237643",
      "name": "Generate Spreadsheet",
      "credentials": {
        "iterationLayerApi": {
          "id": "1",
          "name": "Iteration Layer API"
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "Generate Spreadsheet",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

```prompt
Generate a multi-sheet XLSX sales dashboard. Use the generate_sheet tool with format "xlsx" and two sheets:

1. "Revenue" sheet with columns: Product Line (text), Q1-Q4 (currency), Total (currency formula). Include merged header and total row with SUM formulas.
2. "Expenses" sheet with columns: Category (text), Q1-Q4 (currency), Total (currency formula). Include merged header and total row with SUM formulas.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "UEsDBBQAAAAIAA...",
    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
