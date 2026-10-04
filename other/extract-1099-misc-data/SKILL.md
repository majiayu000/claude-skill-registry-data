---
name: extract-1099-misc-data
description: Extract structured fields from 1099-misc documents.
---

# Extract 1099-MISC Data

Tax and finance teams use this recipe to extract 1099-MISC fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "1099-misc.pdf",
      "url": "https://example.com/documents/1099-misc-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer name"
      },
      {
        "name": "payer_tin",
        "type": "TEXT",
        "description": "Payer TIN"
      },
      {
        "name": "recipient_name",
        "type": "TEXT",
        "description": "Recipient name"
      },
      {
        "name": "recipient_tin",
        "type": "TEXT",
        "description": "Recipient TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "rents",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 rents"
      },
      {
        "name": "royalties",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 royalties"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 other income"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 4 federal income tax withheld"
      },
      {
        "name": "medical_healthcare_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 6 medical and healthcare payments"
      },
      {
        "name": "state_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "State tax withheld"
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
      "name": "1099-misc.pdf",
      "url": "https://example.com/documents/1099-misc-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer name"
      },
      {
        "name": "payer_tin",
        "type": "TEXT",
        "description": "Payer TIN"
      },
      {
        "name": "recipient_name",
        "type": "TEXT",
        "description": "Recipient name"
      },
      {
        "name": "recipient_tin",
        "type": "TEXT",
        "description": "Recipient TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "rents",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 rents"
      },
      {
        "name": "royalties",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 royalties"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 other income"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 4 federal income tax withheld"
      },
      {
        "name": "medical_healthcare_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 6 medical and healthcare payments"
      },
      {
        "name": "state_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "State tax withheld"
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
      "name": "1099-misc.pdf",
      "url": "https://example.com/documents/1099-misc-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Payer name"
      },
      {
        "name": "payer_tin",
        "type": "TEXT",
        "description": "Payer TIN"
      },
      {
        "name": "recipient_name",
        "type": "TEXT",
        "description": "Recipient name"
      },
      {
        "name": "recipient_tin",
        "type": "TEXT",
        "description": "Recipient TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "rents",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 rents"
      },
      {
        "name": "royalties",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 royalties"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 other income"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 4 federal income tax withheld"
      },
      {
        "name": "medical_healthcare_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 6 medical and healthcare payments"
      },
      {
        "name": "state_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "State tax withheld"
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
				Name: "1099-misc.pdf",
				Url: "https://example.com/documents/1099-misc-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "payer_name",
					Type: "TEXT",
					Description: "Payer name",
				},
				il.TextFieldConfig{
					Name: "payer_tin",
					Type: "TEXT",
					Description: "Payer TIN",
				},
				il.TextFieldConfig{
					Name: "recipient_name",
					Type: "TEXT",
					Description: "Recipient name",
				},
				il.TextFieldConfig{
					Name: "recipient_tin",
					Type: "TEXT",
					Description: "Recipient TIN",
				},
				il.TextFieldConfig{
					Name: "tax_year",
					Type: "TEXT",
					Description: "Tax year",
				},
				il.CurrencyAmountFieldConfig{
					Name: "rents",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 1 rents",
				},
				il.CurrencyAmountFieldConfig{
					Name: "royalties",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 2 royalties",
				},
				il.CurrencyAmountFieldConfig{
					Name: "other_income",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 3 other income",
				},
				il.CurrencyAmountFieldConfig{
					Name: "federal_income_tax_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 4 federal income tax withheld",
				},
				il.CurrencyAmountFieldConfig{
					Name: "medical_healthcare_payments",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 6 medical and healthcare payments",
				},
				il.CurrencyAmountFieldConfig{
					Name: "state_tax_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "State tax withheld",
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
  "name": "Extract 1099-MISC Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract 1099-MISC Data\n\nTax and finance teams use this recipe to extract 1099-MISC fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-1099-misc-data-overview",
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
      "id": "extract-1099-misc-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"payer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer name\"\n    },\n    {\n      \"name\": \"payer_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer TIN\"\n    },\n    {\n      \"name\": \"recipient_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Recipient name\"\n    },\n    {\n      \"name\": \"recipient_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Recipient TIN\"\n    },\n    {\n      \"name\": \"tax_year\",\n      \"type\": \"TEXT\",\n      \"description\": \"Tax year\"\n    },\n    {\n      \"name\": \"rents\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 1 rents\"\n    },\n    {\n      \"name\": \"royalties\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 2 royalties\"\n    },\n    {\n      \"name\": \"other_income\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 3 other income\"\n    },\n    {\n      \"name\": \"federal_income_tax_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 4 federal income tax withheld\"\n    },\n    {\n      \"name\": \"medical_healthcare_payments\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 6 medical and healthcare payments\"\n    },\n    {\n      \"name\": \"state_tax_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"State tax withheld\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "1099-misc.pdf",
              "fileUrl": "https://example.com/documents/1099-misc-sample.pdf"
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
      "id": "extract-1099-misc-data-extract",
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
Extract 1099-misc data from the file at [file URL]. Use the extract_document tool with these fields:

- payer_name (TEXT): Payer name
- payer_tin (TEXT): Payer TIN
- recipient_name (TEXT): Recipient name
- recipient_tin (TEXT): Recipient TIN
- tax_year (TEXT): Tax year
- rents (CURRENCY_AMOUNT): Box 1 rents
- royalties (CURRENCY_AMOUNT): Box 2 royalties
- other_income (CURRENCY_AMOUNT): Box 3 other income
- federal_income_tax_withheld (CURRENCY_AMOUNT): Box 4 federal income tax withheld
- medical_healthcare_payments (CURRENCY_AMOUNT): Box 6 medical and healthcare payments
- state_tax_withheld (CURRENCY_AMOUNT): State tax withheld
```

### Response


```json
{
  "success": true,
  "data": {
    "payer_name": {
      "value": "Payer Name",
      "confidence": 0.97,
      "citations": [
        "PAYER NAME"
      ]
    },
    "payer_tin": {
      "value": "Payer Tin",
      "confidence": 0.97,
      "citations": [
        "PAYER TIN"
      ]
    },
    "recipient_name": {
      "value": "Recipient Name",
      "confidence": 0.97,
      "citations": [
        "RECIPIENT NAME"
      ]
    },
    "recipient_tin": {
      "value": "Recipient Tin",
      "confidence": 0.97,
      "citations": [
        "RECIPIENT TIN"
      ]
    },
    "tax_year": {
      "value": "Tax Year",
      "confidence": 0.97,
      "citations": [
        "TAX YEAR"
      ]
    },
    "rents": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "royalties": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "other_income": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "federal_income_tax_withheld": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "medical_healthcare_payments": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "state_tax_withheld": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
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
