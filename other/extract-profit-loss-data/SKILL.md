---
name: extract-profit-loss-data
description: Extract structured fields from profit loss documents.
---

# Extract Profit Loss Data

Finance teams use this recipe to extract Profit Loss line items and totals into structured JSON for reporting, analysis, and reconciliation workflows.

## APIs Used

Document Extraction (1 credit per page)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/document-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "files": [
    {
      "type": "url",
      "name": "profit-loss.pdf",
      "url": "https://example.com/documents/profit-loss-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Company, organization, or fund name"
      },
      {
        "name": "statement_type",
        "type": "TEXT",
        "description": "Type of financial statement"
      },
      {
        "name": "period_start_date",
        "type": "DATE",
        "description": "Reporting period start date"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Reporting period end date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Financial statement line items",
        "fields": [
          {
            "name": "name",
            "type": "TEXT",
            "description": "Line item name"
          },
          {
            "name": "current_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Current period amount"
          },
          {
            "name": "prior_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Prior period or comparative amount"
          }
        ]
      },
      {
        "name": "total_assets_or_revenue",
        "type": "CURRENCY_AMOUNT",
        "description": "Total assets, revenue, income, or budgeted amount"
      },
      {
        "name": "total_liabilities_or_expenses",
        "type": "CURRENCY_AMOUNT",
        "description": "Total liabilities, expenses, or cost amount"
      },
      {
        "name": "currency",
        "type": "CURRENCY_CODE",
        "description": "Currency code"
      }
    ]
  }
}'
```

```typescript
import { IterationLayer } from "iterationlayer";

const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.extractDocument({
  "files": [
    {
      "type": "url",
      "name": "profit-loss.pdf",
      "url": "https://example.com/documents/profit-loss-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Company, organization, or fund name"
      },
      {
        "name": "statement_type",
        "type": "TEXT",
        "description": "Type of financial statement"
      },
      {
        "name": "period_start_date",
        "type": "DATE",
        "description": "Reporting period start date"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Reporting period end date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Financial statement line items",
        "fields": [
          {
            "name": "name",
            "type": "TEXT",
            "description": "Line item name"
          },
          {
            "name": "current_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Current period amount"
          },
          {
            "name": "prior_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Prior period or comparative amount"
          }
        ]
      },
      {
        "name": "total_assets_or_revenue",
        "type": "CURRENCY_AMOUNT",
        "description": "Total assets, revenue, income, or budgeted amount"
      },
      {
        "name": "total_liabilities_or_expenses",
        "type": "CURRENCY_AMOUNT",
        "description": "Total liabilities, expenses, or cost amount"
      },
      {
        "name": "currency",
        "type": "CURRENCY_CODE",
        "description": "Currency code"
      }
    ]
  }
});
```

```python
from iterationlayer import IterationLayer

client = IterationLayer(api_key="YOUR_API_KEY")

result = client.extract_document(**{
  "files": [
    {
      "type": "url",
      "name": "profit-loss.pdf",
      "url": "https://example.com/documents/profit-loss-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Company, organization, or fund name"
      },
      {
        "name": "statement_type",
        "type": "TEXT",
        "description": "Type of financial statement"
      },
      {
        "name": "period_start_date",
        "type": "DATE",
        "description": "Reporting period start date"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Reporting period end date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Financial statement line items",
        "fields": [
          {
            "name": "name",
            "type": "TEXT",
            "description": "Line item name"
          },
          {
            "name": "current_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Current period amount"
          },
          {
            "name": "prior_period_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Prior period or comparative amount"
          }
        ]
      },
      {
        "name": "total_assets_or_revenue",
        "type": "CURRENCY_AMOUNT",
        "description": "Total assets, revenue, income, or budgeted amount"
      },
      {
        "name": "total_liabilities_or_expenses",
        "type": "CURRENCY_AMOUNT",
        "description": "Total liabilities, expenses, or cost amount"
      },
      {
        "name": "currency",
        "type": "CURRENCY_CODE",
        "description": "Currency code"
      }
    ]
  }
})
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.ExtractDocument(il.ExtractDocumentRequest{
		Files: []il.FileInput{
			il.FileInput{
				Type: "url",
				Name: "profit-loss.pdf",
				Url: "https://example.com/documents/profit-loss-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "entity_name",
					Type: "TEXT",
					Description: "Company, organization, or fund name",
				},
				il.TextFieldConfig{
					Name: "statement_type",
					Type: "TEXT",
					Description: "Type of financial statement",
				},
				il.DateFieldConfig{
					Name: "period_start_date",
					Type: "DATE",
					Description: "Reporting period start date",
				},
				il.DateFieldConfig{
					Name: "period_end_date",
					Type: "DATE",
					Description: "Reporting period end date",
				},
				il.ArrayFieldConfig{
					Name: "line_items",
					Type: "ARRAY",
					Description: "Financial statement line items",
					Fields: []any{
						il.TextFieldConfig{
							Name: "name",
							Type: "TEXT",
							Description: "Line item name",
						},
						il.CurrencyAmountFieldConfig{
							Name: "current_period_amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Current period amount",
						},
						il.CurrencyAmountFieldConfig{
							Name: "prior_period_amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Prior period or comparative amount",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_assets_or_revenue",
					Type: "CURRENCY_AMOUNT",
					Description: "Total assets, revenue, income, or budgeted amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_liabilities_or_expenses",
					Type: "CURRENCY_AMOUNT",
					Description: "Total liabilities, expenses, or cost amount",
				},
				il.CurrencyCodeFieldConfig{
					Name: "currency",
					Type: "CURRENCY_CODE",
					Description: "Currency code",
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
  "name": "Extract Profit Loss Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Profit Loss Data\n\nFinance teams use this recipe to extract Profit Loss line items and totals into structured JSON for reporting, analysis, and reconciliation workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-profit-loss-data-overview",
      "name": "Overview"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ],
      "id": "extract-profit-loss-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"entity_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Company, organization, or fund name\"\n    },\n    {\n      \"name\": \"statement_type\",\n      \"type\": \"TEXT\",\n      \"description\": \"Type of financial statement\"\n    },\n    {\n      \"name\": \"period_start_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Reporting period start date\"\n    },\n    {\n      \"name\": \"period_end_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Reporting period end date\"\n    },\n    {\n      \"name\": \"line_items\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Financial statement line items\",\n      \"fields\": [\n        {\n          \"name\": \"name\",\n          \"type\": \"TEXT\",\n          \"description\": \"Line item name\"\n        },\n        {\n          \"name\": \"current_period_amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Current period amount\"\n        },\n        {\n          \"name\": \"prior_period_amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Prior period or comparative amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"total_assets_or_revenue\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total assets, revenue, income, or budgeted amount\"\n    },\n    {\n      \"name\": \"total_liabilities_or_expenses\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total liabilities, expenses, or cost amount\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "profit-loss.pdf",
              "fileUrl": "https://example.com/documents/profit-loss-sample.pdf"
            }
          ]
        }
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "extract-profit-loss-data-extract",
      "name": "Extract Data",
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
            "node": "Extract Data",
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
Extract profit loss data from the file at [file URL]. Use the extract_document tool with these fields:

- entity_name (TEXT): Company, organization, or fund name
- statement_type (TEXT): Type of financial statement
- period_start_date (DATE): Reporting period start date
- period_end_date (DATE): Reporting period end date
- line_items (ARRAY): Each with name (TEXT), current_period_amount (CURRENCY_AMOUNT), prior_period_amount (CURRENCY_AMOUNT)
- total_assets_or_revenue (CURRENCY_AMOUNT): Total assets, revenue, income, or budgeted amount
- total_liabilities_or_expenses (CURRENCY_AMOUNT): Total liabilities, expenses, or cost amount
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "entity_name": {
      "value": "Entity Name",
      "confidence": 0.97,
      "citations": [
        "ENTITY NAME"
      ]
    },
    "statement_type": {
      "value": "Statement Type",
      "confidence": 0.97,
      "citations": [
        "STATEMENT TYPE"
      ]
    },
    "period_start_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "period_end_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "line_items": {
      "value": [
        {
          "name": {
            "value": "Name",
            "confidence": 0.96,
            "citations": [
              "NAME"
            ]
          },
          "current_period_amount": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "EUR 1,234.56"
            ]
          },
          "prior_period_amount": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "EUR 1,234.56"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "LINE ITEMS"
      ]
    },
    "total_assets_or_revenue": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "EUR 1,234.56"
      ]
    },
    "total_liabilities_or_expenses": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "EUR 1,234.56"
      ]
    },
    "currency": {
      "value": "EUR",
      "confidence": 0.97,
      "citations": [
        "CURRENCY"
      ]
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
