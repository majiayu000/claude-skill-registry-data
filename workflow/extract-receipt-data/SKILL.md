---
name: extract-receipt-data
description: Extract merchant, date, line items, tax, and total from receipts.
---

# Extract Receipt Data

Finance teams and expense management apps use this recipe to automate receipt processing. Upload a receipt photo or PDF and receive structured JSON with merchant name, date, individual items, and total — ready for an expense report or reimbursement workflow.

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
        "name": "receipt.pdf",
        "url": "https://example.com/receipts/purchase-receipt.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "merchant_name",
          "type": "TEXT",
          "description": "Name of the merchant or store"
        },
        {
          "name": "date",
          "type": "DATE",
          "description": "Date of the transaction"
        },
        {
          "name": "items",
          "type": "ARRAY",
          "description": "Individual line items on the receipt",
          "fields": [
            {
              "name": "name",
              "type": "TEXT",
              "description": "Item name or description"
            },
            {
              "name": "amount",
              "type": "CURRENCY_AMOUNT",
              "description": "Item price"
            }
          ]
        },
        {
          "name": "total_amount",
          "type": "CURRENCY_AMOUNT",
          "description": "Total amount charged"
        },
        {
          "name": "currency",
          "type": "CURRENCY_CODE",
          "description": "Currency code (e.g. EUR, GBP)"
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.extractDocument({
  files: [
    {
      type: "url",
      name: "receipt.pdf",
      url: "https://example.com/receipts/purchase-receipt.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "merchant_name",
        type: "TEXT",
        description: "Name of the merchant or store",
      },
      {
        name: "date",
        type: "DATE",
        description: "Date of the transaction",
      },
      {
        name: "items",
        type: "ARRAY",
        description: "Individual line items on the receipt",
        fields: [
          {
            name: "name",
            type: "TEXT",
            description: "Item name or description",
          },
          {
            name: "amount",
            type: "CURRENCY_AMOUNT",
            description: "Item price",
          },
        ],
      },
      {
        name: "total_amount",
        type: "CURRENCY_AMOUNT",
        description: "Total amount charged",
      },
      {
        name: "currency",
        type: "CURRENCY_CODE",
        description: "Currency code (e.g. EUR, GBP)",
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.extract_document(
    files=[
        {
            "type": "url",
            "name": "receipt.pdf",
            "url": "https://example.com/receipts/purchase-receipt.pdf",
        }
    ],
    schema={
        "fields": [
            {
                "name": "merchant_name",
                "type": "TEXT",
                "description": "Name of the merchant or store",
            },
            {
                "name": "date",
                "type": "DATE",
                "description": "Date of the transaction",
            },
            {
                "name": "items",
                "type": "ARRAY",
                "description": "Individual line items on the receipt",
                "fields": [
                    {
                        "name": "name",
                        "type": "TEXT",
                        "description": "Item name or description",
                    },
                    {
                        "name": "amount",
                        "type": "CURRENCY_AMOUNT",
                        "description": "Item price",
                    },
                ],
            },
            {
                "name": "total_amount",
                "type": "CURRENCY_AMOUNT",
                "description": "Total amount charged",
            },
            {
                "name": "currency",
                "type": "CURRENCY_CODE",
                "description": "Currency code (e.g. EUR, GBP)",
            },
        ]
    },
)
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
				Name: "receipt.pdf",
				Url: "https://example.com/receipts/purchase-receipt.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "merchant_name",
					Type: "TEXT",
					Description: "Name of the merchant or store",
				},
				il.DateFieldConfig{
					Name: "date",
					Type: "DATE",
					Description: "Date of the transaction",
				},
				il.ArrayFieldConfig{
					Name: "items",
					Type: "ARRAY",
					Description: "Individual line items on the receipt",
					Fields: []any{
						il.TextFieldConfig{
							Name: "name",
							Type: "TEXT",
							Description: "Item name or description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Item price",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total amount charged",
				},
				il.CurrencyCodeFieldConfig{
					Name: "currency",
					Type: "CURRENCY_CODE",
					Description: "Currency code (e.g. EUR, GBP)",
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
  "name": "Extract Receipt Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Receipt Data\n\nFinance teams and expense management apps use this recipe to automate receipt processing. Upload a receipt photo or PDF and receive structured JSON with merchant name, date, individual items, and total \u2014 ready for an expense report or reimbursement workflow.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "4bdb62b6-66d8-4616-a7e1-6e8f48477da7",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
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
      "id": "0c6511af-1417-4e1f-9fbb-73f019a130c3",
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
      "id": "c1d2e3f4-a5b6-7890-cdef-901234567cde",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"merchant_name\",\"type\":\"TEXT\",\"description\":\"Name of the merchant or store\"},{\"name\":\"date\",\"type\":\"DATE\",\"description\":\"Date of the transaction\"},{\"name\":\"items\",\"type\":\"ARRAY\",\"description\":\"Individual line items on the receipt\",\"fields\":[{\"name\":\"name\",\"type\":\"TEXT\",\"description\":\"Item name or description\"},{\"name\":\"amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Item price\"}]},{\"name\":\"total_amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Total amount charged\"},{\"name\":\"currency\",\"type\":\"CURRENCY_CODE\",\"description\":\"Currency code (e.g. EUR, GBP)\"}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "receipt.pdf",
              "fileUrl": "https://example.com/receipts/purchase-receipt.pdf"
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
      "id": "d2e3f4a5-b6c7-8901-defa-012345678def",
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
Extract receipt data from the file at [file URL]. Use the extract_document tool with these fields:

- merchant_name (TEXT): Name of the merchant or store
- date (DATE): Date of the transaction
- items (ARRAY): Each with name (TEXT) and amount (CURRENCY_AMOUNT)
- total_amount (CURRENCY_AMOUNT): Total amount charged
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "merchant_name": {
      "value": "Whole Foods Market",
      "confidence": 0.98,
      "citations": ["WHOLE FOODS MARKET"]
    },
    "date": {
      "value": "2026-02-18",
      "confidence": 0.97,
      "citations": ["02/18/2026"]
    },
    "items": {
      "value": [
        {
          "name": {
            "value": "Organic Avocados (3pk)",
            "confidence": 0.95,
            "citations": ["Organic Avocados 3pk"]
          },
          "amount": {
            "value": {
              "amount": "5.99",
              "currency": "EUR"
            },
            "confidence": 0.97,
            "citations": ["EUR 5.99"]
          }
        },
        {
          "name": {
            "value": "Sourdough Bread",
            "confidence": 0.96,
            "citations": ["Sourdough Bread"]
          },
          "amount": {
            "value": {
              "amount": "4.49",
              "currency": "EUR"
            },
            "confidence": 0.98,
            "citations": ["EUR 4.49"]
          }
        }
      ],
      "confidence": 0.96,
      "citations": []
    },
    "total_amount": {
      "value": {
        "amount": "10.48",
        "currency": "EUR"
      },
      "confidence": 0.99,
      "citations": ["TOTAL: EUR 10.48"]
    },
    "currency": {
      "value": "EUR",
      "confidence": 0.99,
      "citations": ["$"]
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
