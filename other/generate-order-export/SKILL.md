---
name: generate-order-export
description: Export e-commerce order data to CSV with order numbers, customer details, amounts, and fulfillment status.
---

# Generate Order Export

E-commerce platforms and fulfillment teams use this recipe to export order data for accounting, warehouse operations, or third-party integrations. Generate a clean CSV with order details, customer info, and shipping status ready for import into any system.

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
    "format": "csv",
    "sheets": [
      {
      "name": "Orders",
      "columns": [
        {
          "name": "Order ID",
        },
        {
          "name": "Date",
        },
        {
          "name": "Customer",
        },
        {
          "name": "Email",
        },
        {
          "name": "Items",
        },
        {
          "name": "Subtotal",
        },
        {
          "name": "Shipping",
        },
        {
          "name": "Total",
        },
        {
          "name": "Status",
        }
      ],
      "rows": [
        [
          {
            "value": "ORD-38291",
          },
          {
            "value": "2026-03-18",
            "format": "date",
          },
          {
            "value": "Elena Rodriguez",
          },
          {
            "value": "elena.r@gmail.com",
          },
          {
            "value": 3,
            "format": "number",
          },
          {
            "value": 189.97,
            "format": "currency",
          },
          {
            "value": 12.99,
            "format": "currency",
          },
          {
            "value": 202.96,
            "format": "currency",
          },
          {
            "value": "Shipped",
          }
        ],
        [
          {
            "value": "ORD-38292",
          },
          {
            "value": "2026-03-18",
            "format": "date",
          },
          {
            "value": "James Whitfield",
          },
          {
            "value": "j.whitfield@outlook.com",
          },
          {
            "value": 1,
            "format": "number",
          },
          {
            "value": 549.00,
            "format": "currency",
          },
          {
            "value": 0,
            "format": "currency",
          },
          {
            "value": 549.00,
            "format": "currency",
          },
          {
            "value": "Processing",
          }
        ],
        [
          {
            "value": "ORD-38293",
          },
          {
            "value": "2026-03-19",
            "format": "date",
          },
          {
            "value": "Priya Sharma",
          },
          {
            "value": "priya.sharma@company.io",
          },
          {
            "value": 5,
            "format": "number",
          },
          {
            "value": 74.95,
            "format": "currency",
          },
          {
            "value": 8.99,
            "format": "currency",
          },
          {
            "value": 83.94,
            "format": "currency",
          },
          {
            "value": "Delivered",
          }
        ],
        [
          {
            "value": "ORD-38294",
          },
          {
            "value": "2026-03-19",
            "format": "date",
          },
          {
            "value": "Marcus Chen",
          },
          {
            "value": "mchen@protonmail.com",
          },
          {
            "value": 2,
            "format": "number",
          },
          {
            "value": 329.98,
            "format": "currency",
          },
          {
            "value": 15.99,
            "format": "currency",
          },
          {
            "value": 345.97,
            "format": "currency",
          },
          {
            "value": "Shipped",
          }
        ],
        [
          {
            "value": "ORD-38295",
          },
          {
            "value": "2026-03-20",
            "format": "date",
          },
          {
            "value": "Aisha Okafor",
          },
          {
            "value": "aisha.o@gmail.com",
          },
          {
            "value": 1,
            "format": "number",
          },
          {
            "value": 89.00,
            "format": "currency",
          },
          {
            "value": 5.99,
            "format": "currency",
          },
          {
            "value": 94.99,
            "format": "currency",
          },
          {
            "value": "Pending",
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
  format: "csv",
  sheets: [
    {
      name: "Orders",
      columns: [
        {
          name: "Order ID",
        },
        {
          name: "Date",
        },
        {
          name: "Customer",
        },
        {
          name: "Email",
        },
        {
          name: "Items",
        },
        {
          name: "Subtotal",
        },
        {
          name: "Shipping",
        },
        {
          name: "Total",
        },
        {
          name: "Status",
        },
      ],
      rows: [
        [
          {
            value: "ORD-38291",
          },
          {
            value: "2026-03-18",
            format: "date",
          },
          {
            value: "Elena Rodriguez",
          },
          {
            value: "elena.r@gmail.com",
          },
          {
            value: 3,
            format: "number",
          },
          {
            value: 189.97,
            format: "currency",
          },
          {
            value: 12.99,
            format: "currency",
          },
          {
            value: 202.96,
            format: "currency",
          },
          {
            value: "Shipped",
          },
        ],
        [
          {
            value: "ORD-38292",
          },
          {
            value: "2026-03-18",
            format: "date",
          },
          {
            value: "James Whitfield",
          },
          {
            value: "j.whitfield@outlook.com",
          },
          {
            value: 1,
            format: "number",
          },
          {
            value: 549.0,
            format: "currency",
          },
          {
            value: 0,
            format: "currency",
          },
          {
            value: 549.0,
            format: "currency",
          },
          {
            value: "Processing",
          },
        ],
        [
          {
            value: "ORD-38293",
          },
          {
            value: "2026-03-19",
            format: "date",
          },
          {
            value: "Priya Sharma",
          },
          {
            value: "priya.sharma@company.io",
          },
          {
            value: 5,
            format: "number",
          },
          {
            value: 74.95,
            format: "currency",
          },
          {
            value: 8.99,
            format: "currency",
          },
          {
            value: 83.94,
            format: "currency",
          },
          {
            value: "Delivered",
          },
        ],
        [
          {
            value: "ORD-38294",
          },
          {
            value: "2026-03-19",
            format: "date",
          },
          {
            value: "Marcus Chen",
          },
          {
            value: "mchen@protonmail.com",
          },
          {
            value: 2,
            format: "number",
          },
          {
            value: 329.98,
            format: "currency",
          },
          {
            value: 15.99,
            format: "currency",
          },
          {
            value: 345.97,
            format: "currency",
          },
          {
            value: "Shipped",
          },
        ],
        [
          {
            value: "ORD-38295",
          },
          {
            value: "2026-03-20",
            format: "date",
          },
          {
            value: "Aisha Okafor",
          },
          {
            value: "aisha.o@gmail.com",
          },
          {
            value: 1,
            format: "number",
          },
          {
            value: 89.0,
            format: "currency",
          },
          {
            value: 5.99,
            format: "currency",
          },
          {
            value: 94.99,
            format: "currency",
          },
          {
            value: "Pending",
          },
        ],
      ],
    },
  ],
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_sheet(
    format="csv",
    sheets=[
        {
        "name": "Orders",
        "columns": [
            {
                "name": "Order ID",
            },
            {
                "name": "Date",
            },
            {
                "name": "Customer",
            },
            {
                "name": "Email",
            },
            {
                "name": "Items",
            },
            {
                "name": "Subtotal",
            },
            {
                "name": "Shipping",
            },
            {
                "name": "Total",
            },
            {
                "name": "Status",
            },
        ],
        "rows": [
            [
                {
                    "value": "ORD-38291",
                },
                {
                    "value": "2026-03-18",
                    "format": "date",
                },
                {
                    "value": "Elena Rodriguez",
                },
                {
                    "value": "elena.r@gmail.com",
                },
                {
                    "value": 3,
                    "format": "number",
                },
                {
                    "value": 189.97,
                    "format": "currency",
                },
                {
                    "value": 12.99,
                    "format": "currency",
                },
                {
                    "value": 202.96,
                    "format": "currency",
                },
                {
                    "value": "Shipped",
                },
            ],
            [
                {
                    "value": "ORD-38292",
                },
                {
                    "value": "2026-03-18",
                    "format": "date",
                },
                {
                    "value": "James Whitfield",
                },
                {
                    "value": "j.whitfield@outlook.com",
                },
                {
                    "value": 1,
                    "format": "number",
                },
                {
                    "value": 549.00,
                    "format": "currency",
                },
                {
                    "value": 0,
                    "format": "currency",
                },
                {
                    "value": 549.00,
                    "format": "currency",
                },
                {
                    "value": "Processing",
                },
            ],
            [
                {
                    "value": "ORD-38293",
                },
                {
                    "value": "2026-03-19",
                    "format": "date",
                },
                {
                    "value": "Priya Sharma",
                },
                {
                    "value": "priya.sharma@company.io",
                },
                {
                    "value": 5,
                    "format": "number",
                },
                {
                    "value": 74.95,
                    "format": "currency",
                },
                {
                    "value": 8.99,
                    "format": "currency",
                },
                {
                    "value": 83.94,
                    "format": "currency",
                },
                {
                    "value": "Delivered",
                },
            ],
            [
                {
                    "value": "ORD-38294",
                },
                {
                    "value": "2026-03-19",
                    "format": "date",
                },
                {
                    "value": "Marcus Chen",
                },
                {
                    "value": "mchen@protonmail.com",
                },
                {
                    "value": 2,
                    "format": "number",
                },
                {
                    "value": 329.98,
                    "format": "currency",
                },
                {
                    "value": 15.99,
                    "format": "currency",
                },
                {
                    "value": 345.97,
                    "format": "currency",
                },
                {
                    "value": "Shipped",
                },
            ],
            [
                {
                    "value": "ORD-38295",
                },
                {
                    "value": "2026-03-20",
                    "format": "date",
                },
                {
                    "value": "Aisha Okafor",
                },
                {
                    "value": "aisha.o@gmail.com",
                },
                {
                    "value": 1,
                    "format": "number",
                },
                {
                    "value": 89.00,
                    "format": "currency",
                },
                {
                    "value": 5.99,
                    "format": "currency",
                },
                {
                    "value": 94.99,
                    "format": "currency",
                },
                {
                    "value": "Pending",
                },
            ],
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
		Format: "csv",
		Sheets: []il.Sheet{
			{
			Name: "Orders",
			Columns: []il.SheetColumn{
				{
					Name: "Order ID",
				},
				{
					Name: "Date",
				},
				{
					Name: "Customer",
				},
				{
					Name: "Email",
				},
				{
					Name: "Items",
				},
				{
					Name: "Subtotal",
				},
				{
					Name: "Shipping",
				},
				{
					Name: "Total",
				},
				{
					Name: "Status",
				},
			},
			Rows: []il.SheetRow{
				{
					{
						Value: "ORD-38291",
					},
					{
						Value: "2026-03-18",
						Format: "date",
					},
					{
						Value: "Elena Rodriguez",
					},
					{
						Value: "elena.r@gmail.com",
					},
					{
						Value: 3,
						Format: "number",
					},
					{
						Value: 189.97,
						Format: "currency",
					},
					{
						Value: 12.99,
						Format: "currency",
					},
					{
						Value: 202.96,
						Format: "currency",
					},
					{
						Value: "Shipped",
					},
				},
				{
					{
						Value: "ORD-38292",
					},
					{
						Value: "2026-03-18",
						Format: "date",
					},
					{
						Value: "James Whitfield",
					},
					{
						Value: "j.whitfield@outlook.com",
					},
					{
						Value: 1,
						Format: "number",
					},
					{
						Value: 549.00,
						Format: "currency",
					},
					{
						Value: 0,
						Format: "currency",
					},
					{
						Value: 549.00,
						Format: "currency",
					},
					{
						Value: "Processing",
					},
				},
				{
					{
						Value: "ORD-38293",
					},
					{
						Value: "2026-03-19",
						Format: "date",
					},
					{
						Value: "Priya Sharma",
					},
					{
						Value: "priya.sharma@company.io",
					},
					{
						Value: 5,
						Format: "number",
					},
					{
						Value: 74.95,
						Format: "currency",
					},
					{
						Value: 8.99,
						Format: "currency",
					},
					{
						Value: 83.94,
						Format: "currency",
					},
					{
						Value: "Delivered",
					},
				},
				{
					{
						Value: "ORD-38294",
					},
					{
						Value: "2026-03-19",
						Format: "date",
					},
					{
						Value: "Marcus Chen",
					},
					{
						Value: "mchen@protonmail.com",
					},
					{
						Value: 2,
						Format: "number",
					},
					{
						Value: 329.98,
						Format: "currency",
					},
					{
						Value: 15.99,
						Format: "currency",
					},
					{
						Value: 345.97,
						Format: "currency",
					},
					{
						Value: "Shipped",
					},
				},
				{
					{
						Value: "ORD-38295",
					},
					{
						Value: "2026-03-20",
						Format: "date",
					},
					{
						Value: "Aisha Okafor",
					},
					{
						Value: "aisha.o@gmail.com",
					},
					{
						Value: 1,
						Format: "number",
					},
					{
						Value: 89.00,
						Format: "currency",
					},
					{
						Value: 5.99,
						Format: "currency",
					},
					{
						Value: 94.99,
						Format: "currency",
					},
					{
						Value: "Pending",
					},
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
  "name": "Generate Order Export",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Order Export

E-commerce platforms and fulfillment teams use this recipe to export order data for accounting, warehouse operations, or third-party integrations. Generate a clean CSV with order details, customer info, and shipping status ready for import into any system.

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
      "id": "48fa6a75-d1fa-4f40-ab7e-9f8fcfa6f6da",
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
      "id": "9f832f4d-0871-49ad-8ee7-9eea831ca1b2",
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
      "id": "ea892ed0-2e79-42d5-9631-0cda081c99d3",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "sheetGeneration",
        "sheetFormat": "csv",
        "sheetsJson": "[
  {
    \"name\": \"Orders\",
    \"columns\": [
      {
        \"name\": \"Order ID\"
      },
      {
        \"name\": \"Date\"
      },
      {
        \"name\": \"Customer\"
      },
      {
        \"name\": \"Email\"
      },
      {
        \"name\": \"Items\"
      },
      {
        \"name\": \"Subtotal\"
      },
      {
        \"name\": \"Shipping\"
      },
      {
        \"name\": \"Total\"
      },
      {
        \"name\": \"Status\"
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"ORD-38291\"
        },
        {
          \"value\": \"2026-03-18\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Elena Rodriguez\"
        },
        {
          \"value\": \"elena.r@gmail.com\"
        },
        {
          \"value\": 3,
          \"format\": \"number\"
        },
        {
          \"value\": 189.97,
          \"format\": \"currency\"
        },
        {
          \"value\": 12.99,
          \"format\": \"currency\"
        },
        {
          \"value\": 202.96,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Shipped\"
        }
      ],
      [
        {
          \"value\": \"ORD-38292\"
        },
        {
          \"value\": \"2026-03-18\",
          \"format\": \"date\"
        },
        {
          \"value\": \"James Whitfield\"
        },
        {
          \"value\": \"j.whitfield@outlook.com\"
        },
        {
          \"value\": 1,
          \"format\": \"number\"
        },
        {
          \"value\": 549.0,
          \"format\": \"currency\"
        },
        {
          \"value\": 0,
          \"format\": \"currency\"
        },
        {
          \"value\": 549.0,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Processing\"
        }
      ],
      [
        {
          \"value\": \"ORD-38293\"
        },
        {
          \"value\": \"2026-03-19\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Priya Sharma\"
        },
        {
          \"value\": \"priya.sharma@company.io\"
        },
        {
          \"value\": 5,
          \"format\": \"number\"
        },
        {
          \"value\": 74.95,
          \"format\": \"currency\"
        },
        {
          \"value\": 8.99,
          \"format\": \"currency\"
        },
        {
          \"value\": 83.94,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Delivered\"
        }
      ],
      [
        {
          \"value\": \"ORD-38294\"
        },
        {
          \"value\": \"2026-03-19\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Marcus Chen\"
        },
        {
          \"value\": \"mchen@protonmail.com\"
        },
        {
          \"value\": 2,
          \"format\": \"number\"
        },
        {
          \"value\": 329.98,
          \"format\": \"currency\"
        },
        {
          \"value\": 15.99,
          \"format\": \"currency\"
        },
        {
          \"value\": 345.97,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Shipped\"
        }
      ],
      [
        {
          \"value\": \"ORD-38295\"
        },
        {
          \"value\": \"2026-03-20\",
          \"format\": \"date\"
        },
        {
          \"value\": \"Aisha Okafor\"
        },
        {
          \"value\": \"aisha.o@gmail.com\"
        },
        {
          \"value\": 1,
          \"format\": \"number\"
        },
        {
          \"value\": 89.0,
          \"format\": \"currency\"
        },
        {
          \"value\": 5.99,
          \"format\": \"currency\"
        },
        {
          \"value\": 94.99,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Pending\"
        }
      ]
    ]
  }
]",
        "sheetStylesJson": "{}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "05de560e-e7b9-434d-a31c-687ac4be7853",
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
Generate a CSV order export. Use the generate_sheet tool with format "csv" and these columns:

- Order Number (text)
- Date (date)
- Customer Name (text)
- Email (text)
- Total (currency)
- Fulfillment Status (text)
- Shipping Method (text)

Include one row per order with realistic e-commerce order data.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "T3JkZXIgSUQsRGF0ZSxDdXN0b21l...",
    "mime_type": "text/csv"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
