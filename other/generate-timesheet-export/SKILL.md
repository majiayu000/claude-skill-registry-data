---
name: generate-timesheet-export
description: Generate an XLSX timesheet with logged hours, hourly rates, per-entry amount formulas, and totals for client billing or payroll.
---

# Generate Timesheet Export

Project management and freelancing platforms use this recipe to export logged hours as XLSX for client billing or payroll processing. Define your time entries with projects, tasks, and rates, and let formulas compute per-entry amounts and totals automatically.

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
        "background_color": "#0D47A1",
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
      "name": "Timesheet — March 17–21, 2026",
      "columns": [
        {
          "name": "Date",
          "width": 14,
        },
        {
          "name": "Project",
          "width": 28,
        },
        {
          "name": "Task",
          "width": 32,
        },
        {
          "name": "Hours",
          "width": 10,
        },
        {
          "name": "Hourly Rate",
          "width": 14,
        },
        {
          "name": "Amount",
          "width": 14,
        }
      ],
      "rows": [
        [
          {
            "value": "2026-03-17",
            "format": "date",
          },
          {
            "value": "Oakwood E-Commerce Redesign",
          },
          {
            "value": "Homepage wireframes",
          },
          {
            "value": 4.5,
            "format": "number",
          },
          {
            "value": 125,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-17",
            "format": "date",
          },
          {
            "value": "Oakwood E-Commerce Redesign",
          },
          {
            "value": "Stakeholder feedback meeting",
          },
          {
            "value": 1.5,
            "format": "number",
          },
          {
            "value": 125,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-18",
            "format": "date",
          },
          {
            "value": "Oakwood E-Commerce Redesign",
          },
          {
            "value": "Product listing page design",
          },
          {
            "value": 6.0,
            "format": "number",
          },
          {
            "value": 125,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-18",
            "format": "date",
          },
          {
            "value": "Meridian Mobile App",
          },
          {
            "value": "API integration debugging",
          },
          {
            "value": 2.0,
            "format": "number",
          },
          {
            "value": 150,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-19",
            "format": "date",
          },
          {
            "value": "Meridian Mobile App",
          },
          {
            "value": "Push notification service setup",
          },
          {
            "value": 5.0,
            "format": "number",
          },
          {
            "value": 150,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-19",
            "format": "date",
          },
          {
            "value": "Oakwood E-Commerce Redesign",
          },
          {
            "value": "Checkout flow prototype",
          },
          {
            "value": 3.0,
            "format": "number",
          },
          {
            "value": 125,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-20",
            "format": "date",
          },
          {
            "value": "Meridian Mobile App",
          },
          {
            "value": "User authentication flow",
          },
          {
            "value": 7.0,
            "format": "number",
          },
          {
            "value": 150,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-21",
            "format": "date",
          },
          {
            "value": "Oakwood E-Commerce Redesign",
          },
          {
            "value": "Design review and revisions",
          },
          {
            "value": 3.5,
            "format": "number",
          },
          {
            "value": 125,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "2026-03-21",
            "format": "date",
          },
          {
            "value": "Meridian Mobile App",
          },
          {
            "value": "QA testing and bug fixes",
          },
          {
            "value": 4.0,
            "format": "number",
          },
          {
            "value": 150,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "",
          }
        ],
        [
          {
            "value": "",
          },
          {
            "value": "",
          },
          {
            "value": "Total",
            "styles": {
              "is_bold": true,
              "font_size_in_pt": 12,
            },
          },
          {
            "value": null,
            "styles": {
              "is_bold": true,
              "font_size_in_pt": 12,
            },
          },
          {
            "value": "",
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
          "row": 1,
          "col": 5,
          "expression": "=D2*E2",
        },
        {
          "row": 2,
          "col": 5,
          "expression": "=D3*E3",
        },
        {
          "row": 3,
          "col": 5,
          "expression": "=D4*E4",
        },
        {
          "row": 4,
          "col": 5,
          "expression": "=D5*E5",
        },
        {
          "row": 5,
          "col": 5,
          "expression": "=D6*E6",
        },
        {
          "row": 6,
          "col": 5,
          "expression": "=D7*E7",
        },
        {
          "row": 7,
          "col": 5,
          "expression": "=D8*E8",
        },
        {
          "row": 8,
          "col": 5,
          "expression": "=D9*E9",
        },
        {
          "row": 9,
          "col": 5,
          "expression": "=D10*E10",
        },
        {
          "row": 11,
          "col": 3,
          "expression": "=SUM(D2:D10)",
        },
        {
          "row": 11,
          "col": 5,
          "expression": "=SUM(F2:F10)",
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
      background_color: "#0D47A1",
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
      name: "Timesheet — March 17–21, 2026",
      columns: [
        {
          name: "Date",
          width: 14,
        },
        {
          name: "Project",
          width: 28,
        },
        {
          name: "Task",
          width: 32,
        },
        {
          name: "Hours",
          width: 10,
        },
        {
          name: "Hourly Rate",
          width: 14,
        },
        {
          name: "Amount",
          width: 14,
        },
      ],
      rows: [
        [
          {
            value: "2026-03-17",
            format: "date",
          },
          {
            value: "Oakwood E-Commerce Redesign",
          },
          {
            value: "Homepage wireframes",
          },
          {
            value: 4.5,
            format: "number",
          },
          {
            value: 125,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-17",
            format: "date",
          },
          {
            value: "Oakwood E-Commerce Redesign",
          },
          {
            value: "Stakeholder feedback meeting",
          },
          {
            value: 1.5,
            format: "number",
          },
          {
            value: 125,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-18",
            format: "date",
          },
          {
            value: "Oakwood E-Commerce Redesign",
          },
          {
            value: "Product listing page design",
          },
          {
            value: 6.0,
            format: "number",
          },
          {
            value: 125,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-18",
            format: "date",
          },
          {
            value: "Meridian Mobile App",
          },
          {
            value: "API integration debugging",
          },
          {
            value: 2.0,
            format: "number",
          },
          {
            value: 150,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-19",
            format: "date",
          },
          {
            value: "Meridian Mobile App",
          },
          {
            value: "Push notification service setup",
          },
          {
            value: 5.0,
            format: "number",
          },
          {
            value: 150,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-19",
            format: "date",
          },
          {
            value: "Oakwood E-Commerce Redesign",
          },
          {
            value: "Checkout flow prototype",
          },
          {
            value: 3.0,
            format: "number",
          },
          {
            value: 125,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-20",
            format: "date",
          },
          {
            value: "Meridian Mobile App",
          },
          {
            value: "User authentication flow",
          },
          {
            value: 7.0,
            format: "number",
          },
          {
            value: 150,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-21",
            format: "date",
          },
          {
            value: "Oakwood E-Commerce Redesign",
          },
          {
            value: "Design review and revisions",
          },
          {
            value: 3.5,
            format: "number",
          },
          {
            value: 125,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "2026-03-21",
            format: "date",
          },
          {
            value: "Meridian Mobile App",
          },
          {
            value: "QA testing and bug fixes",
          },
          {
            value: 4.0,
            format: "number",
          },
          {
            value: 150,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "",
          },
        ],
        [
          {
            value: "",
          },
          {
            value: "",
          },
          {
            value: "Total",
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
          {
            value: null,
            styles: {
              is_bold: true,
              font_size_in_pt: 12,
            },
          },
          {
            value: "",
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
          row: 1,
          col: 5,
          expression: "=D2*E2",
        },
        {
          row: 2,
          col: 5,
          expression: "=D3*E3",
        },
        {
          row: 3,
          col: 5,
          expression: "=D4*E4",
        },
        {
          row: 4,
          col: 5,
          expression: "=D5*E5",
        },
        {
          row: 5,
          col: 5,
          expression: "=D6*E6",
        },
        {
          row: 6,
          col: 5,
          expression: "=D7*E7",
        },
        {
          row: 7,
          col: 5,
          expression: "=D8*E8",
        },
        {
          row: 8,
          col: 5,
          expression: "=D9*E9",
        },
        {
          row: 9,
          col: 5,
          expression: "=D10*E10",
        },
        {
          row: 11,
          col: 3,
          expression: "=SUM(D2:D10)",
        },
        {
          row: 11,
          col: 5,
          expression: "=SUM(F2:F10)",
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
            "background_color": "#0D47A1",
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
        "name": "Timesheet — March 17–21, 2026",
        "columns": [
            {
                "name": "Date",
                "width": 14,
            },
            {
                "name": "Project",
                "width": 28,
            },
            {
                "name": "Task",
                "width": 32,
            },
            {
                "name": "Hours",
                "width": 10,
            },
            {
                "name": "Hourly Rate",
                "width": 14,
            },
            {
                "name": "Amount",
                "width": 14,
            },
        ],
        "rows": [
            [
                {
                    "value": "2026-03-17",
                    "format": "date",
                },
                {
                    "value": "Oakwood E-Commerce Redesign",
                },
                {
                    "value": "Homepage wireframes",
                },
                {
                    "value": 4.5,
                    "format": "number",
                },
                {
                    "value": 125,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-17",
                    "format": "date",
                },
                {
                    "value": "Oakwood E-Commerce Redesign",
                },
                {
                    "value": "Stakeholder feedback meeting",
                },
                {
                    "value": 1.5,
                    "format": "number",
                },
                {
                    "value": 125,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-18",
                    "format": "date",
                },
                {
                    "value": "Oakwood E-Commerce Redesign",
                },
                {
                    "value": "Product listing page design",
                },
                {
                    "value": 6.0,
                    "format": "number",
                },
                {
                    "value": 125,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-18",
                    "format": "date",
                },
                {
                    "value": "Meridian Mobile App",
                },
                {
                    "value": "API integration debugging",
                },
                {
                    "value": 2.0,
                    "format": "number",
                },
                {
                    "value": 150,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-19",
                    "format": "date",
                },
                {
                    "value": "Meridian Mobile App",
                },
                {
                    "value": "Push notification service setup",
                },
                {
                    "value": 5.0,
                    "format": "number",
                },
                {
                    "value": 150,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-19",
                    "format": "date",
                },
                {
                    "value": "Oakwood E-Commerce Redesign",
                },
                {
                    "value": "Checkout flow prototype",
                },
                {
                    "value": 3.0,
                    "format": "number",
                },
                {
                    "value": 125,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-20",
                    "format": "date",
                },
                {
                    "value": "Meridian Mobile App",
                },
                {
                    "value": "User authentication flow",
                },
                {
                    "value": 7.0,
                    "format": "number",
                },
                {
                    "value": 150,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-21",
                    "format": "date",
                },
                {
                    "value": "Oakwood E-Commerce Redesign",
                },
                {
                    "value": "Design review and revisions",
                },
                {
                    "value": 3.5,
                    "format": "number",
                },
                {
                    "value": 125,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "2026-03-21",
                    "format": "date",
                },
                {
                    "value": "Meridian Mobile App",
                },
                {
                    "value": "QA testing and bug fixes",
                },
                {
                    "value": 4.0,
                    "format": "number",
                },
                {
                    "value": 150,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "",
                },
            ],
            [
                {
                    "value": "",
                },
                {
                    "value": "",
                },
                {
                    "value": "Total",
                    "styles": {
                        "is_bold": True,
                        "font_size_in_pt": 12,
                    },
                },
                {
                    "value": None,
                    "styles": {
                        "is_bold": True,
                        "font_size_in_pt": 12,
                    },
                },
                {
                    "value": "",
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
                "row": 1,
                "col": 5,
                "expression": "=D2*E2",
            },
            {
                "row": 2,
                "col": 5,
                "expression": "=D3*E3",
            },
            {
                "row": 3,
                "col": 5,
                "expression": "=D4*E4",
            },
            {
                "row": 4,
                "col": 5,
                "expression": "=D5*E5",
            },
            {
                "row": 5,
                "col": 5,
                "expression": "=D6*E6",
            },
            {
                "row": 6,
                "col": 5,
                "expression": "=D7*E7",
            },
            {
                "row": 7,
                "col": 5,
                "expression": "=D8*E8",
            },
            {
                "row": 8,
                "col": 5,
                "expression": "=D9*E9",
            },
            {
                "row": 9,
                "col": 5,
                "expression": "=D10*E10",
            },
            {
                "row": 11,
                "col": 3,
                "expression": "=SUM(D2:D10)",
            },
            {
                "row": 11,
                "col": 5,
                "expression": "=SUM(F2:F10)",
            },
        ],
    }
    ],
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.GenerateSheet(il.GenerateSheetRequest{
		Format: "xlsx",
		Styles: &il.SheetStyles{
			Header: &il.CellStyle{
				FontFamily:      "Helvetica",
				FontSizeInPt:    11,
				IsBold:          true,
				BackgroundColor: "#0D47A1",
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
			Name: "Timesheet — March 17–21, 2026",
			Columns: []il.SheetColumn{
				{
					Name:  "Date",
					Width: 14,
				},
				{
					Name:  "Project",
					Width: 28,
				},
				{
					Name:  "Task",
					Width: 32,
				},
				{
					Name:  "Hours",
					Width: 10,
				},
				{
					Name:  "Hourly Rate",
					Width: 14,
				},
				{
					Name:  "Amount",
					Width: 14,
				},
			},
			Rows: []il.SheetRow{
				{
					{
						Value:  "2026-03-17",
						Format: "date",
					},
					{
						Value: "Oakwood E-Commerce Redesign",
					},
					{
						Value: "Homepage wireframes",
					},
					{
						Value:  4.5,
						Format: "number",
					},
					{
						Value:  125,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-17",
						Format: "date",
					},
					{
						Value: "Oakwood E-Commerce Redesign",
					},
					{
						Value: "Stakeholder feedback meeting",
					},
					{
						Value:  1.5,
						Format: "number",
					},
					{
						Value:  125,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-18",
						Format: "date",
					},
					{
						Value: "Oakwood E-Commerce Redesign",
					},
					{
						Value: "Product listing page design",
					},
					{
						Value:  6.0,
						Format: "number",
					},
					{
						Value:  125,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-18",
						Format: "date",
					},
					{
						Value: "Meridian Mobile App",
					},
					{
						Value: "API integration debugging",
					},
					{
						Value:  2.0,
						Format: "number",
					},
					{
						Value:  150,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-19",
						Format: "date",
					},
					{
						Value: "Meridian Mobile App",
					},
					{
						Value: "Push notification service setup",
					},
					{
						Value:  5.0,
						Format: "number",
					},
					{
						Value:  150,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-19",
						Format: "date",
					},
					{
						Value: "Oakwood E-Commerce Redesign",
					},
					{
						Value: "Checkout flow prototype",
					},
					{
						Value:  3.0,
						Format: "number",
					},
					{
						Value:  125,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-20",
						Format: "date",
					},
					{
						Value: "Meridian Mobile App",
					},
					{
						Value: "User authentication flow",
					},
					{
						Value:  7.0,
						Format: "number",
					},
					{
						Value:  150,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-21",
						Format: "date",
					},
					{
						Value: "Oakwood E-Commerce Redesign",
					},
					{
						Value: "Design review and revisions",
					},
					{
						Value:  3.5,
						Format: "number",
					},
					{
						Value:  125,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value:  "2026-03-21",
						Format: "date",
					},
					{
						Value: "Meridian Mobile App",
					},
					{
						Value: "QA testing and bug fixes",
					},
					{
						Value:  4.0,
						Format: "number",
					},
					{
						Value:  150,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "",
					},
				},
				{
					{
						Value: "",
					},
					{
						Value: "",
					},
					{
						Value: "Total",
						Styles: &il.CellStyle{
							IsBold:       true,
							FontSizeInPt: 12,
						},
					},
					{
						Value: nil,
						Styles: &il.CellStyle{
							IsBold:       true,
							FontSizeInPt: 12,
						},
					},
					{
						Value: "",
					},
					{
						Value: nil,
						Styles: &il.CellStyle{
							IsBold:       true,
							FontSizeInPt: 12,
						},
					},
				},
			},
			Formulas: []il.Formula{
				{
					Row:        1,
					Col:        5,
					Expression: "=D2*E2",
				},
				{
					Row:        2,
					Col:        5,
					Expression: "=D3*E3",
				},
				{
					Row:        3,
					Col:        5,
					Expression: "=D4*E4",
				},
				{
					Row:        4,
					Col:        5,
					Expression: "=D5*E5",
				},
				{
					Row:        5,
					Col:        5,
					Expression: "=D6*E6",
				},
				{
					Row:        6,
					Col:        5,
					Expression: "=D7*E7",
				},
				{
					Row:        7,
					Col:        5,
					Expression: "=D8*E8",
				},
				{
					Row:        8,
					Col:        5,
					Expression: "=D9*E9",
				},
				{
					Row:        9,
					Col:        5,
					Expression: "=D10*E10",
				},
				{
					Row:        11,
					Col:        3,
					Expression: "=SUM(D2:D10)",
				},
				{
					Row:        11,
					Col:        5,
					Expression: "=SUM(F2:F10)",
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
  "name": "Generate Timesheet Export",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Timesheet Export

Project management and freelancing platforms use this recipe to export logged hours as XLSX for client billing or payroll processing. Define your time entries with projects, tasks, and rates, and let formulas compute per-entry amounts and totals automatically.

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
      "id": "8b654845-8369-4258-a409-e078f3b278ea",
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
      "id": "5f3c945c-466a-44ca-8ea6-02af9852c5a7",
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
      "id": "0c9ab43b-38fb-458f-9471-96a62ec23b05",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "sheetGeneration",
        "sheetFormat": "xlsx",
        "sheetsJson": "[
  {
    \"name\": \"Timesheet \u2014 March 17\u201321, 2026\",
    \"columns\": [
      {
        \"name\": \"Date\",
        \"width\": 14
      },
      {
        \"name\": \"Project\",
        \"width\": 28
      },
      {
        \"name\": \"Task\",
        \"width\": 32
      },
      {
        \"name\": \"Hours\",
        \"width\": 10
      },
      {
        \"name\": \"Hourly Rate\",
        \"width\": 14
      },
      {
        \"name\": \"Amount\",
        \"width\": 14
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"2026-03-17\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Oakwood E-Commerce Redesign\"
        },
        {
          \"value\": \"Homepage wireframes\"
        },
        {
          \"value\": 4.5,
          \"format\": \"number\"
        },
        {
          \"value\": 125,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-17\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Oakwood E-Commerce Redesign\"
        },
        {
          \"value\": \"Stakeholder feedback meeting\"
        },
        {
          \"value\": 1.5,
          \"format\": \"number\"
        },
        {
          \"value\": 125,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-18\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Oakwood E-Commerce Redesign\"
        },
        {
          \"value\": \"Product listing page design\"
        },
        {
          \"value\": 6.0,
          \"format\": \"number\"
        },
        {
          \"value\": 125,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-18\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Meridian Mobile App\"
        },
        {
          \"value\": \"API integration debugging\"
        },
        {
          \"value\": 2.0,
          \"format\": \"number\"
        },
        {
          \"value\": 150,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-19\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Meridian Mobile App\"
        },
        {
          \"value\": \"Push notification service setup\"
        },
        {
          \"value\": 5.0,
          \"format\": \"number\"
        },
        {
          \"value\": 150,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-19\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Oakwood E-Commerce Redesign\"
        },
        {
          \"value\": \"Checkout flow prototype\"
        },
        {
          \"value\": 3.0,
          \"format\": \"number\"
        },
        {
          \"value\": 125,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-20\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Meridian Mobile App\"
        },
        {
          \"value\": \"User authentication flow\"
        },
        {
          \"value\": 7.0,
          \"format\": \"number\"
        },
        {
          \"value\": 150,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-21\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Oakwood E-Commerce Redesign\"
        },
        {
          \"value\": \"Design review and revisions\"
        },
        {
          \"value\": 3.5,
          \"format\": \"number\"
        },
        {
          \"value\": 125,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"2026-03-21\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Meridian Mobile App\"
        },
        {
          \"value\": \"QA testing and bug fixes\"
        },
        {
          \"value\": 4.0,
          \"format\": \"number\"
        },
        {
          \"value\": 150,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"\"
        }
      ],
      [
        {
          \"value\": \"\"
        },
        {
          \"value\": \"\"
        },
        {
          \"value\": \"Total\",
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        },
        {
          \"value\": null,
          \"styles\": {
            \"is_bold\": true,
            \"font_size_in_pt\": 12
          }
        },
        {
          \"value\": \"\"
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
        \"row\": 1,
        \"col\": 5,
        \"expression\": \"=D2*E2\"
      },
      {
        \"row\": 2,
        \"col\": 5,
        \"expression\": \"=D3*E3\"
      },
      {
        \"row\": 3,
        \"col\": 5,
        \"expression\": \"=D4*E4\"
      },
      {
        \"row\": 4,
        \"col\": 5,
        \"expression\": \"=D5*E5\"
      },
      {
        \"row\": 5,
        \"col\": 5,
        \"expression\": \"=D6*E6\"
      },
      {
        \"row\": 6,
        \"col\": 5,
        \"expression\": \"=D7*E7\"
      },
      {
        \"row\": 7,
        \"col\": 5,
        \"expression\": \"=D8*E8\"
      },
      {
        \"row\": 8,
        \"col\": 5,
        \"expression\": \"=D9*E9\"
      },
      {
        \"row\": 9,
        \"col\": 5,
        \"expression\": \"=D10*E10\"
      },
      {
        \"row\": 11,
        \"col\": 3,
        \"expression\": \"=SUM(D2:D10)\"
      },
      {
        \"row\": 11,
        \"col\": 5,
        \"expression\": \"=SUM(F2:F10)\"
      }
    ]
  }
]",
        "sheetStylesJson": "{
  \"header\": {
    \"font_family\": \"Helvetica\",
    \"font_size_in_pt\": 11,
    \"is_bold\": true,
    \"background_color\": \"#0D47A1\",
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
      "id": "ab98eaa1-d340-4fda-aff8-50021c741c68",
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
Generate an XLSX timesheet export. Use the generate_sheet tool with format "xlsx" and these columns:

- Date (date)
- Project (text)
- Task (text)
- Hours (number)
- Rate (currency)
- Amount (currency, formula: Hours x Rate)

Include a merged header with [employee/contractor name] and billing period, one row per time entry, and a total row with SUM formula for hours and amount.
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
