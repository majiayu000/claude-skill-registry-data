---
name: extract-invoice-data
description: Extract vendor name, line items, totals, and dates from invoice documents.
---

# Extract Invoice Data

Accounts payable teams and finance automation platforms use this recipe to use the Iteration Layer Document Extraction API as an invoice extraction API for PDF and scanned invoices. Upload an invoice in any supported format and receive structured JSON with vendor details, line items, and totals — ready to feed into your ERP or accounting system.

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
        "name": "invoice.pdf",
        "url": "https://example.com/invoices/2026-001.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "vendor",
          "type": "TEXT",
          "description": "Vendor or supplier name"
        },
        {
          "name": "invoice_number",
          "type": "TEXT",
          "description": "Invoice reference number"
        },
        {
          "name": "date",
          "type": "DATE",
          "description": "Invoice date"
        },
        {
          "name": "line_items",
          "type": "ARRAY",
          "description": "Individual line items",
          "fields": [
            {
              "name": "description",
              "type": "TEXT",
              "description": "Item description"
            },
            {
              "name": "quantity",
              "type": "INTEGER",
              "description": "Quantity ordered"
            },
            {
              "name": "unit_price",
              "type": "CURRENCY_AMOUNT",
              "description": "Price per unit"
            }
          ]
        },
        {
          "name": "total_amount",
          "type": "CURRENCY_AMOUNT",
          "description": "Total invoice amount"
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
      name: "invoice.pdf",
      url: "https://example.com/invoices/2026-001.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "vendor",
        type: "TEXT",
        description: "Vendor or supplier name",
      },
      {
        name: "invoice_number",
        type: "TEXT",
        description: "Invoice reference number",
      },
      {
        name: "date",
        type: "DATE",
        description: "Invoice date",
      },
      {
        name: "line_items",
        type: "ARRAY",
        description: "Individual line items",
        fields: [
          {
            name: "description",
            type: "TEXT",
            description: "Item description",
          },
          {
            name: "quantity",
            type: "INTEGER",
            description: "Quantity ordered",
          },
          {
            name: "unit_price",
            type: "CURRENCY_AMOUNT",
            description: "Price per unit",
          },
        ],
      },
      {
        name: "total_amount",
        type: "CURRENCY_AMOUNT",
        description: "Total invoice amount",
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
            "name": "invoice.pdf",
            "url": "https://example.com/invoices/2026-001.pdf",
        }
    ],
    schema={
        "fields": [
            {
                "name": "vendor",
                "type": "TEXT",
                "description": "Vendor or supplier name",
            },
            {
                "name": "invoice_number",
                "type": "TEXT",
                "description": "Invoice reference number",
            },
            {
                "name": "date",
                "type": "DATE",
                "description": "Invoice date",
            },
            {
                "name": "line_items",
                "type": "ARRAY",
                "description": "Individual line items",
                "fields": [
                    {
                        "name": "description",
                        "type": "TEXT",
                        "description": "Item description",
                    },
                    {
                        "name": "quantity",
                        "type": "INTEGER",
                        "description": "Quantity ordered",
                    },
                    {
                        "name": "unit_price",
                        "type": "CURRENCY_AMOUNT",
                        "description": "Price per unit",
                    },
                ],
            },
            {
                "name": "total_amount",
                "type": "CURRENCY_AMOUNT",
                "description": "Total invoice amount",
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
				Name: "invoice.pdf",
				Url: "https://example.com/invoices/2026-001.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "vendor",
					Type: "TEXT",
					Description: "Vendor or supplier name",
				},
				il.TextFieldConfig{
					Name: "invoice_number",
					Type: "TEXT",
					Description: "Invoice reference number",
				},
				il.DateFieldConfig{
					Name: "date",
					Type: "DATE",
					Description: "Invoice date",
				},
				il.ArrayFieldConfig{
					Name: "line_items",
					Type: "ARRAY",
					Description: "Individual line items",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Item description",
						},
						il.IntegerFieldConfig{
							Name: "quantity",
							Type: "INTEGER",
							Description: "Quantity ordered",
						},
						il.CurrencyAmountFieldConfig{
							Name: "unit_price",
							Type: "CURRENCY_AMOUNT",
							Description: "Price per unit",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total invoice amount",
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
  "name": "Extract Invoice Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Invoice Data\n\nAccounts payable teams and finance automation platforms use this recipe to eliminate manual invoice data entry. Upload an invoice in any supported format and receive structured JSON with vendor details, line items, and totals \u2014 ready to feed into your ERP or accounting system.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "740bbc39-f879-4a4d-b1a7-4b66dfac8f09",
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
      "id": "0ad47fa7-0338-4060-bc1b-f5c1aa248b53",
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
      "id": "c9d0e1f2-a3b4-5678-cdef-789012345678",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"vendor\",\"type\":\"TEXT\",\"description\":\"Vendor or supplier name\"},{\"name\":\"invoice_number\",\"type\":\"TEXT\",\"description\":\"Invoice reference number\"},{\"name\":\"date\",\"type\":\"DATE\",\"description\":\"Invoice date\"},{\"name\":\"line_items\",\"type\":\"ARRAY\",\"description\":\"Individual line items\",\"fields\":[{\"name\":\"description\",\"type\":\"TEXT\",\"description\":\"Item description\"},{\"name\":\"quantity\",\"type\":\"INTEGER\",\"description\":\"Quantity ordered\"},{\"name\":\"unit_price\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Price per unit\"}]},{\"name\":\"total_amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Total invoice amount\"}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "invoice.pdf",
              "fileUrl": "https://example.com/invoices/2026-001.pdf"
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
      "id": "d0e1f2a3-b4c5-6789-defa-890123456789",
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
Extract invoice data from the file at [file URL]. Use the extract_document tool with these fields:

- vendor (TEXT): Vendor or supplier name
- invoice_number (TEXT): Invoice reference number
- date (DATE): Invoice date
- line_items (ARRAY): Each with description (TEXT), quantity (INTEGER), unit_price (CURRENCY_AMOUNT)
- total_amount (CURRENCY_AMOUNT): Total invoice amount
```

### Response


```json
{
  "success": true,
  "data": {
    "vendor": {
      "value": "Alpine Office Supplies GmbH",
      "confidence": 0.97,
      "citations": ["Alpine Office Supplies GmbH"]
    },
    "invoice_number": {
      "value": "INV-2026-001",
      "confidence": 0.99,
      "citations": ["Invoice #INV-2026-001"]
    },
    "date": {
      "value": "2026-01-15",
      "confidence": 0.98,
      "citations": ["Date: January 15, 2026"]
    },
    "line_items": {
      "value": [
        {
          "description": {
            "value": "Ergonomic Desk Chair",
            "confidence": 0.96,
            "citations": ["Ergonomic Desk Chair"]
          },
          "quantity": {
            "value": 2,
            "confidence": 0.98,
            "citations": ["Qty: 2"]
          },
          "unit_price": {
            "value": {
              "amount": "349.99",
              "currency": "EUR"
            },
            "confidence": 0.97,
            "citations": ["EUR 349.99 each"]
          }
        },
        {
          "description": {
            "value": "Standing Desk Converter",
            "confidence": 0.95,
            "citations": ["Standing Desk Converter"]
          },
          "quantity": {
            "value": 1,
            "confidence": 0.99,
            "citations": ["Qty: 1"]
          },
          "unit_price": {
            "value": {
              "amount": "189.00",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": ["EUR 189.00 each"]
          }
        }
      ],
      "confidence": 0.96,
      "citations": []
    },
    "total_amount": {
      "value": {
        "amount": "888.98",
        "currency": "EUR"
      },
      "confidence": 0.98,
      "citations": ["Total Due: EUR 888.98"]
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
