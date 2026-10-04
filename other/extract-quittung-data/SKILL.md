---
name: extract-quittung-data
description: Extract receipt number, issuer, payer, date, VAT, and total from German receipts.
---

# Extract Quittung Data

Finance teams use this recipe to extract German Quittung fields into structured receipt records for expense, tax, and accounting workflows.

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
      "name": "quittung.pdf",
      "url": "https://example.com/documents/quittung-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number or Belegnummer"
      },
      {
        "name": "issuer_name",
        "type": "TEXT",
        "description": "Issuer or merchant name"
      },
      {
        "name": "issuer_address",
        "type": "ADDRESS",
        "description": "Issuer address"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or customer name if shown"
      },
      {
        "name": "receipt_date",
        "type": "DATE",
        "description": "Receipt date"
      },
      {
        "name": "payment_method",
        "type": "TEXT",
        "description": "Payment method"
      },
      {
        "name": "items",
        "type": "ARRAY",
        "description": "Purchased goods or services",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Line amount"
          }
        ]
      },
      {
        "name": "net_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount"
      },
      {
        "name": "vat_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "VAT amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total amount paid"
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
      "name": "quittung.pdf",
      "url": "https://example.com/documents/quittung-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number or Belegnummer"
      },
      {
        "name": "issuer_name",
        "type": "TEXT",
        "description": "Issuer or merchant name"
      },
      {
        "name": "issuer_address",
        "type": "ADDRESS",
        "description": "Issuer address"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or customer name if shown"
      },
      {
        "name": "receipt_date",
        "type": "DATE",
        "description": "Receipt date"
      },
      {
        "name": "payment_method",
        "type": "TEXT",
        "description": "Payment method"
      },
      {
        "name": "items",
        "type": "ARRAY",
        "description": "Purchased goods or services",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Line amount"
          }
        ]
      },
      {
        "name": "net_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount"
      },
      {
        "name": "vat_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "VAT amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total amount paid"
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
      "name": "quittung.pdf",
      "url": "https://example.com/documents/quittung-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number or Belegnummer"
      },
      {
        "name": "issuer_name",
        "type": "TEXT",
        "description": "Issuer or merchant name"
      },
      {
        "name": "issuer_address",
        "type": "ADDRESS",
        "description": "Issuer address"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or customer name if shown"
      },
      {
        "name": "receipt_date",
        "type": "DATE",
        "description": "Receipt date"
      },
      {
        "name": "payment_method",
        "type": "TEXT",
        "description": "Payment method"
      },
      {
        "name": "items",
        "type": "ARRAY",
        "description": "Purchased goods or services",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item or service description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Line amount"
          }
        ]
      },
      {
        "name": "net_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount"
      },
      {
        "name": "vat_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "VAT amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total amount paid"
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
				Name: "quittung.pdf",
				Url: "https://example.com/documents/quittung-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "receipt_number",
					Type: "TEXT",
					Description: "Receipt number or Belegnummer",
				},
				il.TextFieldConfig{
					Name: "issuer_name",
					Type: "TEXT",
					Description: "Issuer or merchant name",
				},
				il.AddressFieldConfig{
					Name: "issuer_address",
					Type: "ADDRESS",
					Description: "Issuer address",
				},
				il.TextFieldConfig{
					Name: "payer_name",
					Type: "TEXT",
					Description: "Payer or customer name if shown",
				},
				il.DateFieldConfig{
					Name: "receipt_date",
					Type: "DATE",
					Description: "Receipt date",
				},
				il.TextFieldConfig{
					Name: "payment_method",
					Type: "TEXT",
					Description: "Payment method",
				},
				il.ArrayFieldConfig{
					Name: "items",
					Type: "ARRAY",
					Description: "Purchased goods or services",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Item or service description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Line amount",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "net_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Net amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "vat_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "VAT amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total amount paid",
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
  "name": "Extract Quittung Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Quittung Data\n\nFinance teams use this recipe to extract German Quittung fields into structured receipt records for expense, tax, and accounting workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-quittung-data-overview",
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
      "id": "extract-quittung-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"receipt_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Receipt number or Belegnummer\"\n    },\n    {\n      \"name\": \"issuer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Issuer or merchant name\"\n    },\n    {\n      \"name\": \"issuer_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Issuer address\"\n    },\n    {\n      \"name\": \"payer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer or customer name if shown\"\n    },\n    {\n      \"name\": \"receipt_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Receipt date\"\n    },\n    {\n      \"name\": \"payment_method\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payment method\"\n    },\n    {\n      \"name\": \"items\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Purchased goods or services\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Item or service description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Line amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"net_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Net amount\"\n    },\n    {\n      \"name\": \"vat_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"VAT amount\"\n    },\n    {\n      \"name\": \"total_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total amount paid\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "quittung.pdf",
              "fileUrl": "https://example.com/documents/quittung-sample.pdf"
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
      "id": "extract-quittung-data-extract",
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
Extract quittung data from the file at [file URL]. Use the extract_document tool with these fields:

- receipt_number (TEXT): Receipt number or Belegnummer
- issuer_name (TEXT): Issuer or merchant name
- issuer_address (ADDRESS): Issuer address
- payer_name (TEXT): Payer or customer name if shown
- receipt_date (DATE): Receipt date
- payment_method (TEXT): Payment method
- items (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- net_amount (CURRENCY_AMOUNT): Net amount
- vat_amount (CURRENCY_AMOUNT): VAT amount
- total_amount (CURRENCY_AMOUNT): Total amount paid
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "receipt_number": {
      "value": "Receipt Number",
      "confidence": 0.97,
      "citations": [
        "RECEIPT NUMBER"
      ]
    },
    "issuer_name": {
      "value": "Issuer Name",
      "confidence": 0.97,
      "citations": [
        "ISSUER NAME"
      ]
    },
    "issuer_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "ISSUER ADDRESS"
      ]
    },
    "payer_name": {
      "value": "Payer Name",
      "confidence": 0.97,
      "citations": [
        "PAYER NAME"
      ]
    },
    "receipt_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "payment_method": {
      "value": "Payment Method",
      "confidence": 0.97,
      "citations": [
        "PAYMENT METHOD"
      ]
    },
    "items": {
      "value": [
        {
          "description": {
            "value": "Description",
            "confidence": 0.96,
            "citations": [
              "DESCRIPTION"
            ]
          },
          "amount": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "1,234.56"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "ITEMS"
      ]
    },
    "net_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "vat_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "total_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
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
