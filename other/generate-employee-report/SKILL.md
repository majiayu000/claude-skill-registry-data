---
name: generate-employee-report
description: Generate an XLSX employee report with departments, salaries, hire dates, and currency formatting.
---

# Generate Employee Report

HR departments and people operations teams use this recipe to generate employee roster reports for headcount reviews, compensation analysis, or compliance audits. Each row captures key employee details with properly formatted salary and date columns.

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
        "background_color": "#1F4E79",
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
      "name": "Employee Roster",
      "columns": [
        {
          "name": "Employee ID",
          "width": 14,
        },
        {
          "name": "Full Name",
          "width": 22,
        },
        {
          "name": "Department",
          "width": 18,
        },
        {
          "name": "Title",
          "width": 28,
        },
        {
          "name": "Hire Date",
          "width": 14,
        },
        {
          "name": "Annual Salary",
          "width": 16,
        },
        {
          "name": "Location",
          "width": 18,
        }
      ],
      "rows": [
        [
          {
            "value": "EMP-1042",
          },
          {
            "value": "Sarah Mitchell",
          },
          {
            "value": "Engineering",
          },
          {
            "value": "Senior Software Engineer",
          },
          {
            "value": "2022-06-15",
            "format": "date",
          },
          {
            "value": 142000,
            "format": "currency",
          },
          {
            "value": "Berlin, DE",
          }
        ],
        [
          {
            "value": "EMP-1078",
          },
          {
            "value": "David Nakamura",
          },
          {
            "value": "Product",
          },
          {
            "value": "Product Manager",
          },
          {
            "value": "2023-01-09",
            "format": "date",
          },
          {
            "value": 128000,
            "format": "currency",
          },
          {
            "value": "Amsterdam, NL",
          }
        ],
        [
          {
            "value": "EMP-1103",
          },
          {
            "value": "Amara Osei",
          },
          {
            "value": "Design",
          },
          {
            "value": "Lead UX Designer",
          },
          {
            "value": "2023-04-22",
            "format": "date",
          },
          {
            "value": 121000,
            "format": "currency",
          },
          {
            "value": "Austin, TX",
          }
        ],
        [
          {
            "value": "EMP-1156",
          },
          {
            "value": "Carlos Reyes",
          },
          {
            "value": "Engineering",
          },
          {
            "value": "DevOps Engineer",
          },
          {
            "value": "2024-02-12",
            "format": "date",
          },
          {
            "value": 135000,
            "format": "currency",
          },
          {
            "value": "Denver, CO",
          }
        ],
        [
          {
            "value": "EMP-1189",
          },
          {
            "value": "Lin Wei",
          },
          {
            "value": "Marketing",
          },
          {
            "value": "Growth Marketing Lead",
          },
          {
            "value": "2024-08-05",
            "format": "date",
          },
          {
            "value": 115000,
            "format": "currency",
          },
          {
            "value": "Chicago, IL",
          }
        ],
        [
          {
            "value": "EMP-1201",
          },
          {
            "value": "Rachel Andersen",
          },
          {
            "value": "Finance",
          },
          {
            "value": "Financial Analyst",
          },
          {
            "value": "2025-01-13",
            "format": "date",
          },
          {
            "value": 98000,
            "format": "currency",
          },
          {
            "value": "Berlin, DE",
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
  styles: {
    header: {
      font_family: "Helvetica",
      font_size_in_pt: 11,
      is_bold: true,
      background_color: "#1F4E79",
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
      name: "Employee Roster",
      columns: [
        {
          name: "Employee ID",
          width: 14,
        },
        {
          name: "Full Name",
          width: 22,
        },
        {
          name: "Department",
          width: 18,
        },
        {
          name: "Title",
          width: 28,
        },
        {
          name: "Hire Date",
          width: 14,
        },
        {
          name: "Annual Salary",
          width: 16,
        },
        {
          name: "Location",
          width: 18,
        },
      ],
      rows: [
        [
          {
            value: "EMP-1042",
          },
          {
            value: "Sarah Mitchell",
          },
          {
            value: "Engineering",
          },
          {
            value: "Senior Software Engineer",
          },
          {
            value: "2022-06-15",
            format: "date",
          },
          {
            value: 142000,
            format: "currency",
          },
          {
            value: "Berlin, DE",
          },
        ],
        [
          {
            value: "EMP-1078",
          },
          {
            value: "David Nakamura",
          },
          {
            value: "Product",
          },
          {
            value: "Product Manager",
          },
          {
            value: "2023-01-09",
            format: "date",
          },
          {
            value: 128000,
            format: "currency",
          },
          {
            value: "Amsterdam, NL",
          },
        ],
        [
          {
            value: "EMP-1103",
          },
          {
            value: "Amara Osei",
          },
          {
            value: "Design",
          },
          {
            value: "Lead UX Designer",
          },
          {
            value: "2023-04-22",
            format: "date",
          },
          {
            value: 121000,
            format: "currency",
          },
          {
            value: "Austin, TX",
          },
        ],
        [
          {
            value: "EMP-1156",
          },
          {
            value: "Carlos Reyes",
          },
          {
            value: "Engineering",
          },
          {
            value: "DevOps Engineer",
          },
          {
            value: "2024-02-12",
            format: "date",
          },
          {
            value: 135000,
            format: "currency",
          },
          {
            value: "Denver, CO",
          },
        ],
        [
          {
            value: "EMP-1189",
          },
          {
            value: "Lin Wei",
          },
          {
            value: "Marketing",
          },
          {
            value: "Growth Marketing Lead",
          },
          {
            value: "2024-08-05",
            format: "date",
          },
          {
            value: 115000,
            format: "currency",
          },
          {
            value: "Chicago, IL",
          },
        ],
        [
          {
            value: "EMP-1201",
          },
          {
            value: "Rachel Andersen",
          },
          {
            value: "Finance",
          },
          {
            value: "Financial Analyst",
          },
          {
            value: "2025-01-13",
            format: "date",
          },
          {
            value: 98000,
            format: "currency",
          },
          {
            value: "Berlin, DE",
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
    format="xlsx",
    styles={
        "header": {
            "font_family": "Helvetica",
            "font_size_in_pt": 11,
            "is_bold": True,
            "background_color": "#1F4E79",
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
        "name": "Employee Roster",
        "columns": [
            {
                "name": "Employee ID",
                "width": 14,
            },
            {
                "name": "Full Name",
                "width": 22,
            },
            {
                "name": "Department",
                "width": 18,
            },
            {
                "name": "Title",
                "width": 28,
            },
            {
                "name": "Hire Date",
                "width": 14,
            },
            {
                "name": "Annual Salary",
                "width": 16,
            },
            {
                "name": "Location",
                "width": 18,
            },
        ],
        "rows": [
            [
                {
                    "value": "EMP-1042",
                },
                {
                    "value": "Sarah Mitchell",
                },
                {
                    "value": "Engineering",
                },
                {
                    "value": "Senior Software Engineer",
                },
                {
                    "value": "2022-06-15",
                    "format": "date",
                },
                {
                    "value": 142000,
                    "format": "currency",
                },
                {
                    "value": "Berlin, DE",
                },
            ],
            [
                {
                    "value": "EMP-1078",
                },
                {
                    "value": "David Nakamura",
                },
                {
                    "value": "Product",
                },
                {
                    "value": "Product Manager",
                },
                {
                    "value": "2023-01-09",
                    "format": "date",
                },
                {
                    "value": 128000,
                    "format": "currency",
                },
                {
                    "value": "Amsterdam, NL",
                },
            ],
            [
                {
                    "value": "EMP-1103",
                },
                {
                    "value": "Amara Osei",
                },
                {
                    "value": "Design",
                },
                {
                    "value": "Lead UX Designer",
                },
                {
                    "value": "2023-04-22",
                    "format": "date",
                },
                {
                    "value": 121000,
                    "format": "currency",
                },
                {
                    "value": "Austin, TX",
                },
            ],
            [
                {
                    "value": "EMP-1156",
                },
                {
                    "value": "Carlos Reyes",
                },
                {
                    "value": "Engineering",
                },
                {
                    "value": "DevOps Engineer",
                },
                {
                    "value": "2024-02-12",
                    "format": "date",
                },
                {
                    "value": 135000,
                    "format": "currency",
                },
                {
                    "value": "Denver, CO",
                },
            ],
            [
                {
                    "value": "EMP-1189",
                },
                {
                    "value": "Lin Wei",
                },
                {
                    "value": "Marketing",
                },
                {
                    "value": "Growth Marketing Lead",
                },
                {
                    "value": "2024-08-05",
                    "format": "date",
                },
                {
                    "value": 115000,
                    "format": "currency",
                },
                {
                    "value": "Chicago, IL",
                },
            ],
            [
                {
                    "value": "EMP-1201",
                },
                {
                    "value": "Rachel Andersen",
                },
                {
                    "value": "Finance",
                },
                {
                    "value": "Financial Analyst",
                },
                {
                    "value": "2025-01-13",
                    "format": "date",
                },
                {
                    "value": 98000,
                    "format": "currency",
                },
                {
                    "value": "Berlin, DE",
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
		Format: "xlsx",
		Styles: &il.SheetStyles{
			Header: &il.CellStyle{
				FontFamily:      "Helvetica",
				FontSizeInPt:    11,
				IsBold:          true,
				BackgroundColor: "#1F4E79",
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
			Name: "Employee Roster",
			Columns: []il.SheetColumn{
				{
					Name: "Employee ID",
					Width: 14,
				},
				{
					Name: "Full Name",
					Width: 22,
				},
				{
					Name: "Department",
					Width: 18,
				},
				{
					Name: "Title",
					Width: 28,
				},
				{
					Name: "Hire Date",
					Width: 14,
				},
				{
					Name: "Annual Salary",
					Width: 16,
				},
				{
					Name: "Location",
					Width: 18,
				},
			},
			Rows: []il.SheetRow{
				{
					{
						Value: "EMP-1042",
					},
					{
						Value: "Sarah Mitchell",
					},
					{
						Value: "Engineering",
					},
					{
						Value: "Senior Software Engineer",
					},
					{
						Value: "2022-06-15",
						Format: "date",
					},
					{
						Value: 142000,
						Format: "currency",
					},
					{
						Value: "Berlin, DE",
					},
				},
				{
					{
						Value: "EMP-1078",
					},
					{
						Value: "David Nakamura",
					},
					{
						Value: "Product",
					},
					{
						Value: "Product Manager",
					},
					{
						Value: "2023-01-09",
						Format: "date",
					},
					{
						Value: 128000,
						Format: "currency",
					},
					{
						Value: "Amsterdam, NL",
					},
				},
				{
					{
						Value: "EMP-1103",
					},
					{
						Value: "Amara Osei",
					},
					{
						Value: "Design",
					},
					{
						Value: "Lead UX Designer",
					},
					{
						Value: "2023-04-22",
						Format: "date",
					},
					{
						Value: 121000,
						Format: "currency",
					},
					{
						Value: "Austin, TX",
					},
				},
				{
					{
						Value: "EMP-1156",
					},
					{
						Value: "Carlos Reyes",
					},
					{
						Value: "Engineering",
					},
					{
						Value: "DevOps Engineer",
					},
					{
						Value: "2024-02-12",
						Format: "date",
					},
					{
						Value: 135000,
						Format: "currency",
					},
					{
						Value: "Denver, CO",
					},
				},
				{
					{
						Value: "EMP-1189",
					},
					{
						Value: "Lin Wei",
					},
					{
						Value: "Marketing",
					},
					{
						Value: "Growth Marketing Lead",
					},
					{
						Value: "2024-08-05",
						Format: "date",
					},
					{
						Value: 115000,
						Format: "currency",
					},
					{
						Value: "Chicago, IL",
					},
				},
				{
					{
						Value: "EMP-1201",
					},
					{
						Value: "Rachel Andersen",
					},
					{
						Value: "Finance",
					},
					{
						Value: "Financial Analyst",
					},
					{
						Value: "2025-01-13",
						Format: "date",
					},
					{
						Value: 98000,
						Format: "currency",
					},
					{
						Value: "Berlin, DE",
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
  "name": "Generate Employee Report",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Employee Report

HR departments and people operations teams use this recipe to generate employee roster reports for headcount reviews, compensation analysis, or compliance audits. Each row captures key employee details with properly formatted salary and date columns.

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
      "id": "464e3509-1d90-4d31-8856-fbacfeab16c4",
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
      "id": "b30cb5ff-3e27-41d6-8ece-620e1b2a8a02",
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
      "id": "3047e092-4aae-416f-abf4-43bf223b5703",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "sheetGeneration",
        "sheetFormat": "xlsx",
        "sheetsJson": "[
  {
    \"name\": \"Employee Roster\",
    \"columns\": [
      {
        \"name\": \"Employee ID\",
        \"width\": 14
      },
      {
        \"name\": \"Full Name\",
        \"width\": 22
      },
      {
        \"name\": \"Department\",
        \"width\": 18
      },
      {
        \"name\": \"Title\",
        \"width\": 28
      },
      {
        \"name\": \"Hire Date\",
        \"width\": 14
      },
      {
        \"name\": \"Annual Salary\",
        \"width\": 16
      },
      {
        \"name\": \"Location\",
        \"width\": 18
      }
    ],
    \"rows\": [
      [
        {
          \"value\": \"EMP-1042\"
        },
        {
          \"value\": \"Sarah Mitchell\"
        },
        {
          \"value\": \"Engineering\"
        },
        {
          \"value\": \"Senior Software Engineer\"
        },
        {
          \"value\": \"2022-06-15\",
          \"format\": \"date\"
        },
        {
          \"value\": 142000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Berlin, DE\"
        }
      ],
      [
        {
          \"value\": \"EMP-1078\"
        },
        {
          \"value\": \"David Nakamura\"
        },
        {
          \"value\": \"Product\"
        },
        {
          \"value\": \"Product Manager\"
        },
        {
          \"value\": \"2023-01-09\",
          \"format\": \"date\"
        },
        {
          \"value\": 128000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Amsterdam, NL\"
        }
      ],
      [
        {
          \"value\": \"EMP-1103\"
        },
        {
          \"value\": \"Amara Osei\"
        },
        {
          \"value\": \"Design\"
        },
        {
          \"value\": \"Lead UX Designer\"
        },
        {
          \"value\": \"2023-04-22\",
          \"format\": \"date\"
        },
        {
          \"value\": 121000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Austin, TX\"
        }
      ],
      [
        {
          \"value\": \"EMP-1156\"
        },
        {
          \"value\": \"Carlos Reyes\"
        },
        {
          \"value\": \"Engineering\"
        },
        {
          \"value\": \"DevOps Engineer\"
        },
        {
          \"value\": \"2024-02-12\",
          \"format\": \"date\"
        },
        {
          \"value\": 135000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Denver, CO\"
        }
      ],
      [
        {
          \"value\": \"EMP-1189\"
        },
        {
          \"value\": \"Lin Wei\"
        },
        {
          \"value\": \"Marketing\"
        },
        {
          \"value\": \"Growth Marketing Lead\"
        },
        {
          \"value\": \"2024-08-05\",
          \"format\": \"date\"
        },
        {
          \"value\": 115000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Chicago, IL\"
        }
      ],
      [
        {
          \"value\": \"EMP-1201\"
        },
        {
          \"value\": \"Rachel Andersen\"
        },
        {
          \"value\": \"Finance\"
        },
        {
          \"value\": \"Financial Analyst\"
        },
        {
          \"value\": \"2025-01-13\",
          \"format\": \"date\"
        },
        {
          \"value\": 98000,
          \"format\": \"currency\"
        },
        {
          \"value\": \"Berlin, DE\"
        }
      ]
    ]
  }
]",
        "sheetStylesJson": "{
  \"header\": {
    \"font_family\": \"Helvetica\",
    \"font_size_in_pt\": 11,
    \"is_bold\": true,
    \"background_color\": \"#1F4E79\",
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
      "id": "033ed035-a051-466d-bb7e-ee2242219b14",
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
Generate an XLSX employee report. Use the generate_sheet tool with format "xlsx" and these columns:

- Employee ID (text)
- Name (text)
- Department (text)
- Title (text)
- Hire Date (date)
- Salary (currency)
- Status (text)

Include styled headers and one row per employee with formatted salary and date values.
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
