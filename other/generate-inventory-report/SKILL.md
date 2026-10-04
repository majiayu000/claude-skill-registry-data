---
name: generate-inventory-report
description: Generate an XLSX inventory report with stock levels, reorder points, unit costs, and total value formulas for purchasing teams.
---

# Generate Inventory Report

E-commerce platforms and warehouse management systems use this recipe to export current stock levels, reorder points, and inventory valuation to XLSX for purchasing teams. Define your product catalog with quantities and costs, and let formulas compute total value per item automatically.

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
        "background_color": "#1B5E20",
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
      "name": "Inventory Report — March 2026",
      "columns": [
        {
          "name": "SKU",
          "width": 16,
        },
        {
          "name": "Product Name",
          "width": 35,
        },
        {
          "name": "Category",
          "width": 18,
        },
        {
          "name": "Qty In Stock",
          "width": 14,
        },
        {
          "name": "Reorder Point",
          "width": 14,
        },
        {
          "name": "Unit Cost",
          "width": 14,
        },
        {
          "name": "Total Value",
          "width": 16,
        }
      ],
      "rows": [
        [
          {
            "value": "EL-1001",
          },
          {
            "value": "Wireless Bluetooth Headphones",
          },
          {
            "value": "Electronics",
          },
          {
            "value": 342,
            "format": "number",
          },
          {
            "value": 100,
            "format": "number",
          },
          {
            "value": 24.99,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "EL-1002",
          },
          {
            "value": "USB-C Charging Cable (2m)",
          },
          {
            "value": "Electronics",
          },
          {
            "value": 1580,
            "format": "number",
          },
          {
            "value": 500,
            "format": "number",
          },
          {
            "value": 3.49,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "CL-2010",
          },
          {
            "value": "Men's Cotton Crew T-Shirt (Black, L)",
          },
          {
            "value": "Clothing",
          },
          {
            "value": 87,
            "format": "number",
          },
          {
            "value": 150,
            "format": "number",
          },
          {
            "value": 6.75,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "CL-2015",
          },
          {
            "value": "Women's Running Shorts (Navy, M)",
          },
          {
            "value": "Clothing",
          },
          {
            "value": 214,
            "format": "number",
          },
          {
            "value": 80,
            "format": "number",
          },
          {
            "value": 11.20,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "HG-3005",
          },
          {
            "value": "Stainless Steel Water Bottle (750ml)",
          },
          {
            "value": "Home & Garden",
          },
          {
            "value": 463,
            "format": "number",
          },
          {
            "value": 200,
            "format": "number",
          },
          {
            "value": 8.50,
            "format": "currency",
          },
          {
            "value": null,
          }
        ],
        [
          {
            "value": "EL-1018",
          },
          {
            "value": "Portable Power Bank (10000mAh)",
          },
          {
            "value": "Electronics",
          },
          {
            "value": 56,
            "format": "number",
          },
          {
            "value": 75,
            "format": "number",
          },
          {
            "value": 18.30,
            "format": "currency",
          },
          {
            "value": null,
          }
        ]
      ],
      "formulas": [
        {
          "row": 1,
          "col": 6,
          "expression": "=D2*F2",
        },
        {
          "row": 2,
          "col": 6,
          "expression": "=D3*F3",
        },
        {
          "row": 3,
          "col": 6,
          "expression": "=D4*F4",
        },
        {
          "row": 4,
          "col": 6,
          "expression": "=D5*F5",
        },
        {
          "row": 5,
          "col": 6,
          "expression": "=D6*F6",
        },
        {
          "row": 6,
          "col": 6,
          "expression": "=D7*F7",
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
      background_color: "#1B5E20",
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
      name: "Inventory Report — March 2026",
      columns: [
        {
          name: "SKU",
          width: 16,
        },
        {
          name: "Product Name",
          width: 35,
        },
        {
          name: "Category",
          width: 18,
        },
        {
          name: "Qty In Stock",
          width: 14,
        },
        {
          name: "Reorder Point",
          width: 14,
        },
        {
          name: "Unit Cost",
          width: 14,
        },
        {
          name: "Total Value",
          width: 16,
        },
      ],
      rows: [
        [
          {
            value: "EL-1001",
          },
          {
            value: "Wireless Bluetooth Headphones",
          },
          {
            value: "Electronics",
          },
          {
            value: 342,
            format: "number",
          },
          {
            value: 100,
            format: "number",
          },
          {
            value: 24.99,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "EL-1002",
          },
          {
            value: "USB-C Charging Cable (2m)",
          },
          {
            value: "Electronics",
          },
          {
            value: 1580,
            format: "number",
          },
          {
            value: 500,
            format: "number",
          },
          {
            value: 3.49,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "CL-2010",
          },
          {
            value: "Men's Cotton Crew T-Shirt (Black, L)",
          },
          {
            value: "Clothing",
          },
          {
            value: 87,
            format: "number",
          },
          {
            value: 150,
            format: "number",
          },
          {
            value: 6.75,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "CL-2015",
          },
          {
            value: "Women's Running Shorts (Navy, M)",
          },
          {
            value: "Clothing",
          },
          {
            value: 214,
            format: "number",
          },
          {
            value: 80,
            format: "number",
          },
          {
            value: 11.2,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "HG-3005",
          },
          {
            value: "Stainless Steel Water Bottle (750ml)",
          },
          {
            value: "Home & Garden",
          },
          {
            value: 463,
            format: "number",
          },
          {
            value: 200,
            format: "number",
          },
          {
            value: 8.5,
            format: "currency",
          },
          {
            value: null,
          },
        ],
        [
          {
            value: "EL-1018",
          },
          {
            value: "Portable Power Bank (10000mAh)",
          },
          {
            value: "Electronics",
          },
          {
            value: 56,
            format: "number",
          },
          {
            value: 75,
            format: "number",
          },
          {
            value: 18.3,
            format: "currency",
          },
          {
            value: null,
          },
        ],
      ],
      formulas: [
        {
          row: 1,
          col: 6,
          expression: "=D2*F2",
        },
        {
          row: 2,
          col: 6,
          expression: "=D3*F3",
        },
        {
          row: 3,
          col: 6,
          expression: "=D4*F4",
        },
        {
          row: 4,
          col: 6,
          expression: "=D5*F5",
        },
        {
          row: 5,
          col: 6,
          expression: "=D6*F6",
        },
        {
          row: 6,
          col: 6,
          expression: "=D7*F7",
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
            "background_color": "#1B5E20",
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
        "name": "Inventory Report — March 2026",
        "columns": [
            {
                "name": "SKU",
                "width": 16,
            },
            {
                "name": "Product Name",
                "width": 35,
            },
            {
                "name": "Category",
                "width": 18,
            },
            {
                "name": "Qty In Stock",
                "width": 14,
            },
            {
                "name": "Reorder Point",
                "width": 14,
            },
            {
                "name": "Unit Cost",
                "width": 14,
            },
            {
                "name": "Total Value",
                "width": 16,
            },
        ],
        "rows": [
            [
                {
                    "value": "EL-1001",
                },
                {
                    "value": "Wireless Bluetooth Headphones",
                },
                {
                    "value": "Electronics",
                },
                {
                    "value": 342,
                    "format": "number",
                },
                {
                    "value": 100,
                    "format": "number",
                },
                {
                    "value": 24.99,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "EL-1002",
                },
                {
                    "value": "USB-C Charging Cable (2m)",
                },
                {
                    "value": "Electronics",
                },
                {
                    "value": 1580,
                    "format": "number",
                },
                {
                    "value": 500,
                    "format": "number",
                },
                {
                    "value": 3.49,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "CL-2010",
                },
                {
                    "value": "Men's Cotton Crew T-Shirt (Black, L)",
                },
                {
                    "value": "Clothing",
                },
                {
                    "value": 87,
                    "format": "number",
                },
                {
                    "value": 150,
                    "format": "number",
                },
                {
                    "value": 6.75,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "CL-2015",
                },
                {
                    "value": "Women's Running Shorts (Navy, M)",
                },
                {
                    "value": "Clothing",
                },
                {
                    "value": 214,
                    "format": "number",
                },
                {
                    "value": 80,
                    "format": "number",
                },
                {
                    "value": 11.20,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "HG-3005",
                },
                {
                    "value": "Stainless Steel Water Bottle (750ml)",
                },
                {
                    "value": "Home & Garden",
                },
                {
                    "value": 463,
                    "format": "number",
                },
                {
                    "value": 200,
                    "format": "number",
                },
                {
                    "value": 8.50,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
            [
                {
                    "value": "EL-1018",
                },
                {
                    "value": "Portable Power Bank (10000mAh)",
                },
                {
                    "value": "Electronics",
                },
                {
                    "value": 56,
                    "format": "number",
                },
                {
                    "value": 75,
                    "format": "number",
                },
                {
                    "value": 18.30,
                    "format": "currency",
                },
                {
                    "value": None,
                },
            ],
        ],
        "formulas": [
            {
                "row": 1,
                "col": 6,
                "expression": "=D2*F2",
            },
            {
                "row": 2,
                "col": 6,
                "expression": "=D3*F3",
            },
            {
                "row": 3,
                "col": 6,
                "expression": "=D4*F4",
            },
            {
                "row": 4,
                "col": 6,
                "expression": "=D5*F5",
            },
            {
                "row": 5,
                "col": 6,
                "expression": "=D6*F6",
            },
            {
                "row": 6,
                "col": 6,
                "expression": "=D7*F7",
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
				BackgroundColor: "#1B5E20",
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
			Name: "Inventory Report — March 2026",
			Columns: []il.SheetColumn{
				{
					Name:  "SKU",
					Width: 16,
				},
				{
					Name:  "Product Name",
					Width: 35,
				},
				{
					Name:  "Category",
					Width: 18,
				},
				{
					Name:  "Qty In Stock",
					Width: 14,
				},
				{
					Name:  "Reorder Point",
					Width: 14,
				},
				{
					Name:  "Unit Cost",
					Width: 14,
				},
				{
					Name:  "Total Value",
					Width: 16,
				},
			},
			Rows: []il.SheetRow{
				{
					{
						Value: "EL-1001",
					},
					{
						Value: "Wireless Bluetooth Headphones",
					},
					{
						Value: "Electronics",
					},
					{
						Value:  342,
						Format: "number",
					},
					{
						Value:  100,
						Format: "number",
					},
					{
						Value:  24.99,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "EL-1002",
					},
					{
						Value: "USB-C Charging Cable (2m)",
					},
					{
						Value: "Electronics",
					},
					{
						Value:  1580,
						Format: "number",
					},
					{
						Value:  500,
						Format: "number",
					},
					{
						Value:  3.49,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "CL-2010",
					},
					{
						Value: "Men's Cotton Crew T-Shirt (Black, L)",
					},
					{
						Value: "Clothing",
					},
					{
						Value:  87,
						Format: "number",
					},
					{
						Value:  150,
						Format: "number",
					},
					{
						Value:  6.75,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "CL-2015",
					},
					{
						Value: "Women's Running Shorts (Navy, M)",
					},
					{
						Value: "Clothing",
					},
					{
						Value:  214,
						Format: "number",
					},
					{
						Value:  80,
						Format: "number",
					},
					{
						Value:  11.20,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "HG-3005",
					},
					{
						Value: "Stainless Steel Water Bottle (750ml)",
					},
					{
						Value: "Home & Garden",
					},
					{
						Value:  463,
						Format: "number",
					},
					{
						Value:  200,
						Format: "number",
					},
					{
						Value:  8.50,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
				{
					{
						Value: "EL-1018",
					},
					{
						Value: "Portable Power Bank (10000mAh)",
					},
					{
						Value: "Electronics",
					},
					{
						Value:  56,
						Format: "number",
					},
					{
						Value:  75,
						Format: "number",
					},
					{
						Value:  18.30,
						Format: "currency",
					},
					{
						Value: nil,
					},
				},
			},
			Formulas: []il.Formula{
				{
					Row:        1,
					Col:        6,
					Expression: "=D2*F2",
				},
				{
					Row:        2,
					Col:        6,
					Expression: "=D3*F3",
				},
				{
					Row:        3,
					Col:        6,
					Expression: "=D4*F4",
				},
				{
					Row:        4,
					Col:        6,
					Expression: "=D5*F5",
				},
				{
					Row:        5,
					Col:        6,
					Expression: "=D6*F6",
				},
				{
					Row:        6,
					Col:        6,
					Expression: "=D7*F7",
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
  "name": "Generate Inventory Report",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Inventory Report

E-commerce platforms and warehouse management systems use this recipe to export current stock levels, reorder points, and inventory valuation to XLSX for purchasing teams. Define your product catalog with quantities and costs, and let formulas compute total value per item automatically.

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
      "id": "4e89e082-3e95-417a-9afb-f6230649de45",
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
      "id": "856b2fe2-a643-4095-93f9-d424c7e49a15",
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
      "id": "d68c1d3f-afce-4339-9f02-952244fafcb5",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "sheetGeneration",
        "sheetFormat": "xlsx",
        "sheetsJson": "[
  {
    \"name\": \"Inventory Report \u2014 March 2026\",
    \"columns\": [
      {
        \"name\": \"SKU\",
        \"width\": 16
      },
      {
        \"name\": \"Product Name\",
        \"width\": 35
      },
      {
        \"name\": \"Category\",
        \"width\": 18
      },
      {
        \"name\": \"Qty In Stock\",
        \"width\": 14
      },
      {
        \"name\": \"Reorder Point\",
        \"width\": 14
      },
      {
        \"name\": \"Unit Cost\",
        \"width\": 14
      },
      {
        \"name\": \"Total Value\",
        \"width\": 16
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"EL-1001\"
        },
        {
          \"value\": \"Wireless Bluetooth Headphones\"
        },
        {
          \"value\": \"Electronics\"
        },
        {
          \"value\": 342,
          \"format\": \"number\"
        },
        {
          \"value\": 100,
          \"format\": \"number\"
        },
        {
          \"value\": 24.99,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"EL-1002\"
        },
        {
          \"value\": \"USB-C Charging Cable (2m)\"
        },
        {
          \"value\": \"Electronics\"
        },
        {
          \"value\": 1580,
          \"format\": \"number\"
        },
        {
          \"value\": 500,
          \"format\": \"number\"
        },
        {
          \"value\": 3.49,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"CL-2010\"
        },
        {
          \"value\": \"Men's Cotton Crew T-Shirt (Black, L)\"
        },
        {
          \"value\": \"Clothing\"
        },
        {
          \"value\": 87,
          \"format\": \"number\"
        },
        {
          \"value\": 150,
          \"format\": \"number\"
        },
        {
          \"value\": 6.75,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"CL-2015\"
        },
        {
          \"value\": \"Women's Running Shorts (Navy, M)\"
        },
        {
          \"value\": \"Clothing\"
        },
        {
          \"value\": 214,
          \"format\": \"number\"
        },
        {
          \"value\": 80,
          \"format\": \"number\"
        },
        {
          \"value\": 11.2,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"HG-3005\"
        },
        {
          \"value\": \"Stainless Steel Water Bottle (750ml)\"
        },
        {
          \"value\": \"Home & Garden\"
        },
        {
          \"value\": 463,
          \"format\": \"number\"
        },
        {
          \"value\": 200,
          \"format\": \"number\"
        },
        {
          \"value\": 8.5,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ],
      [
        {
          \"value\": \"EL-1018\"
        },
        {
          \"value\": \"Portable Power Bank (10000mAh)\"
        },
        {
          \"value\": \"Electronics\"
        },
        {
          \"value\": 56,
          \"format\": \"number\"
        },
        {
          \"value\": 75,
          \"format\": \"number\"
        },
        {
          \"value\": 18.3,
          \"format\": \"currency\"
        },
        {
          \"value\": null
        }
      ]
    ],
    \"formulas\": [
      {
        \"row\": 1,
        \"col\": 6,
        \"expression\": \"=D2*F2\"
      },
      {
        \"row\": 2,
        \"col\": 6,
        \"expression\": \"=D3*F3\"
      },
      {
        \"row\": 3,
        \"col\": 6,
        \"expression\": \"=D4*F4\"
      },
      {
        \"row\": 4,
        \"col\": 6,
        \"expression\": \"=D5*F5\"
      },
      {
        \"row\": 5,
        \"col\": 6,
        \"expression\": \"=D6*F6\"
      },
      {
        \"row\": 6,
        \"col\": 6,
        \"expression\": \"=D7*F7\"
      }
    ]
  }
]",
        "sheetStylesJson": "{
  \"header\": {
    \"font_family\": \"Helvetica\",
    \"font_size_in_pt\": 11,
    \"is_bold\": true,
    \"background_color\": \"#1B5E20\",
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
      "id": "5f85dfc0-c158-4920-a08f-e7817aebdb4b",
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
Generate an XLSX inventory report. Use the generate_sheet tool with format "xlsx" and these columns:

- SKU (text)
- Product Name (text)
- Category (text)
- In Stock (number)
- Reorder Point (number)
- Unit Cost (currency)
- Total Value (currency, formula: In Stock x Unit Cost)

Include styled headers and one row per product with formulas computing total value per item.
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
