---
name: extract-facture-data
description: Extract structured fields from facture documents.
---

# Extract Facture Data

Finance teams use this recipe to extract Facture fields into structured JSON for accounts receivable, accounts payable, tax, and ERP workflows.

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
      "name": "facture.pdf",
      "url": "https://example.com/documents/facture-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "seller_name",
        "type": "TEXT",
        "description": "Seller, supplier, or issuer name"
      },
      {
        "name": "buyer_name",
        "type": "TEXT",
        "description": "Buyer, customer, or recipient name"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Invoice or fiscal document number"
      },
      {
        "name": "issue_date",
        "type": "DATE",
        "description": "Issue date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Line items, services, or taxable supplies",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity"
          },
          {
            "name": "unit_price",
            "type": "CURRENCY_AMOUNT",
            "description": "Unit price"
          },
          {
            "name": "line_total",
            "type": "CURRENCY_AMOUNT",
            "description": "Line total"
          }
        ]
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total payable amount"
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
      "name": "facture.pdf",
      "url": "https://example.com/documents/facture-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "seller_name",
        "type": "TEXT",
        "description": "Seller, supplier, or issuer name"
      },
      {
        "name": "buyer_name",
        "type": "TEXT",
        "description": "Buyer, customer, or recipient name"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Invoice or fiscal document number"
      },
      {
        "name": "issue_date",
        "type": "DATE",
        "description": "Issue date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Line items, services, or taxable supplies",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity"
          },
          {
            "name": "unit_price",
            "type": "CURRENCY_AMOUNT",
            "description": "Unit price"
          },
          {
            "name": "line_total",
            "type": "CURRENCY_AMOUNT",
            "description": "Line total"
          }
        ]
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total payable amount"
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
      "name": "facture.pdf",
      "url": "https://example.com/documents/facture-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "seller_name",
        "type": "TEXT",
        "description": "Seller, supplier, or issuer name"
      },
      {
        "name": "buyer_name",
        "type": "TEXT",
        "description": "Buyer, customer, or recipient name"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Invoice or fiscal document number"
      },
      {
        "name": "issue_date",
        "type": "DATE",
        "description": "Issue date"
      },
      {
        "name": "line_items",
        "type": "ARRAY",
        "description": "Line items, services, or taxable supplies",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity"
          },
          {
            "name": "unit_price",
            "type": "CURRENCY_AMOUNT",
            "description": "Unit price"
          },
          {
            "name": "line_total",
            "type": "CURRENCY_AMOUNT",
            "description": "Line total"
          }
        ]
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total payable amount"
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
				Name: "facture.pdf",
				Url: "https://example.com/documents/facture-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "seller_name",
					Type: "TEXT",
					Description: "Seller, supplier, or issuer name",
				},
				il.TextFieldConfig{
					Name: "buyer_name",
					Type: "TEXT",
					Description: "Buyer, customer, or recipient name",
				},
				il.TextFieldConfig{
					Name: "document_number",
					Type: "TEXT",
					Description: "Invoice or fiscal document number",
				},
				il.DateFieldConfig{
					Name: "issue_date",
					Type: "DATE",
					Description: "Issue date",
				},
				il.ArrayFieldConfig{
					Name: "line_items",
					Type: "ARRAY",
					Description: "Line items, services, or taxable supplies",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Item or service description",
						},
						il.DecimalFieldConfig{
							Name: "quantity",
							Type: "DECIMAL",
							Description: "Quantity",
						},
						il.CurrencyAmountFieldConfig{
							Name: "unit_price",
							Type: "CURRENCY_AMOUNT",
							Description: "Unit price",
						},
						il.CurrencyAmountFieldConfig{
							Name: "line_total",
							Type: "CURRENCY_AMOUNT",
							Description: "Line total",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "tax_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Tax amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total payable amount",
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
  "name": "Extract Facture Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Facture Data\n\nFinance teams use this recipe to extract Facture fields into structured JSON for accounts receivable, accounts payable, tax, and ERP workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-facture-data-overview",
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
      "id": "extract-facture-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"seller_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Seller, supplier, or issuer name\"\n    },\n    {\n      \"name\": \"buyer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Buyer, customer, or recipient name\"\n    },\n    {\n      \"name\": \"document_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Invoice or fiscal document number\"\n    },\n    {\n      \"name\": \"issue_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Issue date\"\n    },\n    {\n      \"name\": \"line_items\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Line items, services, or taxable supplies\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Item or service description\"\n        },\n        {\n          \"name\": \"quantity\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Quantity\"\n        },\n        {\n          \"name\": \"unit_price\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Unit price\"\n        },\n        {\n          \"name\": \"line_total\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Line total\"\n        }\n      ]\n    },\n    {\n      \"name\": \"tax_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Tax amount\"\n    },\n    {\n      \"name\": \"total_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total payable amount\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "facture.pdf",
              "fileUrl": "https://example.com/documents/facture-sample.pdf"
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
      "id": "extract-facture-data-extract",
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
Extract facture data from the file at [file URL]. Use the extract_document tool with these fields:

- seller_name (TEXT): Seller, supplier, or issuer name
- buyer_name (TEXT): Buyer, customer, or recipient name
- document_number (TEXT): Invoice or fiscal document number
- issue_date (DATE): Issue date
- line_items (ARRAY): Each with description (TEXT), quantity (DECIMAL), unit_price (CURRENCY_AMOUNT), line_total (CURRENCY_AMOUNT)
- tax_amount (CURRENCY_AMOUNT): Tax amount
- total_amount (CURRENCY_AMOUNT): Total payable amount
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "seller_name": {
      "value": "Seller Name",
      "confidence": 0.97,
      "citations": [
        "SELLER NAME"
      ]
    },
    "buyer_name": {
      "value": "Buyer Name",
      "confidence": 0.97,
      "citations": [
        "BUYER NAME"
      ]
    },
    "document_number": {
      "value": "BL-2026-00418",
      "confidence": 0.97,
      "citations": [
        "DOCUMENT NUMBER"
      ]
    },
    "issue_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "line_items": {
      "value": [
        {
          "description": {
            "value": "Description",
            "confidence": 0.96,
            "citations": [
              "DESCRIPTION"
            ]
          },
          "quantity": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "QUANTITY"
            ]
          },
          "unit_price": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "EUR 1,234.56"
            ]
          },
          "line_total": {
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
    "tax_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "EUR 1,234.56"
      ]
    },
    "total_amount": {
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
