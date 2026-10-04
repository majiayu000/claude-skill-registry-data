---
name: extract-ryoshusho-data
description: Extract receipt number, issuer, payer, date, tax, and total from Japanese receipts.
---

# Extract Ryoshusho Data

Finance teams use this recipe to extract ryoshusho fields into structured receipt records for reimbursement, consumption-tax checks, and accounting workflows.

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
      "name": "ryoshusho.pdf",
      "url": "https://example.com/documents/ryoshusho-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number"
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
        "name": "issuer_registration_number",
        "type": "TEXT",
        "description": "Qualified invoice issuer registration number if shown"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or recipient name"
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
        "name": "consumption_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Consumption tax amount"
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
      "name": "ryoshusho.pdf",
      "url": "https://example.com/documents/ryoshusho-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number"
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
        "name": "issuer_registration_number",
        "type": "TEXT",
        "description": "Qualified invoice issuer registration number if shown"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or recipient name"
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
        "name": "consumption_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Consumption tax amount"
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
      "name": "ryoshusho.pdf",
      "url": "https://example.com/documents/ryoshusho-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "receipt_number",
        "type": "TEXT",
        "description": "Receipt number"
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
        "name": "issuer_registration_number",
        "type": "TEXT",
        "description": "Qualified invoice issuer registration number if shown"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer or recipient name"
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
        "name": "consumption_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Consumption tax amount"
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
				Name: "ryoshusho.pdf",
				Url: "https://example.com/documents/ryoshusho-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "receipt_number",
					Type: "TEXT",
					Description: "Receipt number",
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
					Name: "issuer_registration_number",
					Type: "TEXT",
					Description: "Qualified invoice issuer registration number if shown",
				},
				il.TextFieldConfig{
					Name: "payer_name",
					Type: "TEXT",
					Description: "Payer or recipient name",
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
					Name: "consumption_tax",
					Type: "CURRENCY_AMOUNT",
					Description: "Consumption tax amount",
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
  "name": "Extract Ryoshusho Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Ryoshusho Data\n\nFinance teams use this recipe to extract ryoshusho fields into structured receipt records for reimbursement, consumption-tax checks, and accounting workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-ryoshusho-data-overview",
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
      "id": "extract-ryoshusho-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"receipt_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Receipt number\"\n    },\n    {\n      \"name\": \"issuer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Issuer or merchant name\"\n    },\n    {\n      \"name\": \"issuer_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Issuer address\"\n    },\n    {\n      \"name\": \"issuer_registration_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Qualified invoice issuer registration number if shown\"\n    },\n    {\n      \"name\": \"payer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer or recipient name\"\n    },\n    {\n      \"name\": \"receipt_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Receipt date\"\n    },\n    {\n      \"name\": \"payment_method\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payment method\"\n    },\n    {\n      \"name\": \"items\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Purchased goods or services\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Item or service description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Line amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"consumption_tax\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Consumption tax amount\"\n    },\n    {\n      \"name\": \"total_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total amount paid\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "ryoshusho.pdf",
              "fileUrl": "https://example.com/documents/ryoshusho-sample.pdf"
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
      "id": "extract-ryoshusho-data-extract",
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
Extract ryoshusho data from the file at [file URL]. Use the extract_document tool with these fields:

- receipt_number (TEXT): Receipt number
- issuer_name (TEXT): Issuer or merchant name
- issuer_address (ADDRESS): Issuer address
- issuer_registration_number (TEXT): Qualified invoice issuer registration number if shown
- payer_name (TEXT): Payer or recipient name
- receipt_date (DATE): Receipt date
- payment_method (TEXT): Payment method
- items (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- consumption_tax (CURRENCY_AMOUNT): Consumption tax amount
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
    "issuer_registration_number": {
      "value": "Issuer Registration Number",
      "confidence": 0.97,
      "citations": [
        "ISSUER REGISTRATION NUMBER"
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
    "consumption_tax": {
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
