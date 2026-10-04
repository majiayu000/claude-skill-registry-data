---
name: extract-schedule-k-1-data
description: Extract structured fields from schedule k 1 documents.
---

# Extract Schedule K 1 Data

Tax and finance teams use this recipe to extract Schedule K 1 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "schedule-k-1.pdf",
      "url": "https://example.com/documents/schedule-k-1-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Partnership, S corporation, estate, or trust name"
      },
      {
        "name": "entity_ein",
        "type": "TEXT",
        "description": "Entity employer identification number"
      },
      {
        "name": "partner_or_shareholder_name",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary name"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "profit_share_percent",
        "type": "DECIMAL",
        "description": "Profit share percentage"
      },
      {
        "name": "loss_share_percent",
        "type": "DECIMAL",
        "description": "Loss share percentage"
      },
      {
        "name": "ordinary_business_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Ordinary business income or loss"
      },
      {
        "name": "rental_real_estate_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Net rental real estate income or loss"
      },
      {
        "name": "guaranteed_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Guaranteed payments if shown"
      },
      {
        "name": "distributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Distributions if shown"
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
      "name": "schedule-k-1.pdf",
      "url": "https://example.com/documents/schedule-k-1-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Partnership, S corporation, estate, or trust name"
      },
      {
        "name": "entity_ein",
        "type": "TEXT",
        "description": "Entity employer identification number"
      },
      {
        "name": "partner_or_shareholder_name",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary name"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "profit_share_percent",
        "type": "DECIMAL",
        "description": "Profit share percentage"
      },
      {
        "name": "loss_share_percent",
        "type": "DECIMAL",
        "description": "Loss share percentage"
      },
      {
        "name": "ordinary_business_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Ordinary business income or loss"
      },
      {
        "name": "rental_real_estate_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Net rental real estate income or loss"
      },
      {
        "name": "guaranteed_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Guaranteed payments if shown"
      },
      {
        "name": "distributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Distributions if shown"
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
      "name": "schedule-k-1.pdf",
      "url": "https://example.com/documents/schedule-k-1-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "entity_name",
        "type": "TEXT",
        "description": "Partnership, S corporation, estate, or trust name"
      },
      {
        "name": "entity_ein",
        "type": "TEXT",
        "description": "Entity employer identification number"
      },
      {
        "name": "partner_or_shareholder_name",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary name"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "Partner, shareholder, or beneficiary TIN"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "profit_share_percent",
        "type": "DECIMAL",
        "description": "Profit share percentage"
      },
      {
        "name": "loss_share_percent",
        "type": "DECIMAL",
        "description": "Loss share percentage"
      },
      {
        "name": "ordinary_business_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Ordinary business income or loss"
      },
      {
        "name": "rental_real_estate_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Net rental real estate income or loss"
      },
      {
        "name": "guaranteed_payments",
        "type": "CURRENCY_AMOUNT",
        "description": "Guaranteed payments if shown"
      },
      {
        "name": "distributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Distributions if shown"
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
				Name: "schedule-k-1.pdf",
				Url: "https://example.com/documents/schedule-k-1-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "entity_name",
					Type: "TEXT",
					Description: "Partnership, S corporation, estate, or trust name",
				},
				il.TextFieldConfig{
					Name: "entity_ein",
					Type: "TEXT",
					Description: "Entity employer identification number",
				},
				il.TextFieldConfig{
					Name: "partner_or_shareholder_name",
					Type: "TEXT",
					Description: "Partner, shareholder, or beneficiary name",
				},
				il.TextFieldConfig{
					Name: "taxpayer_identification_number",
					Type: "TEXT",
					Description: "Partner, shareholder, or beneficiary TIN",
				},
				il.TextFieldConfig{
					Name: "tax_year",
					Type: "TEXT",
					Description: "Tax year",
				},
				il.DecimalFieldConfig{
					Name: "profit_share_percent",
					Type: "DECIMAL",
					Description: "Profit share percentage",
				},
				il.DecimalFieldConfig{
					Name: "loss_share_percent",
					Type: "DECIMAL",
					Description: "Loss share percentage",
				},
				il.CurrencyAmountFieldConfig{
					Name: "ordinary_business_income",
					Type: "CURRENCY_AMOUNT",
					Description: "Ordinary business income or loss",
				},
				il.CurrencyAmountFieldConfig{
					Name: "rental_real_estate_income",
					Type: "CURRENCY_AMOUNT",
					Description: "Net rental real estate income or loss",
				},
				il.CurrencyAmountFieldConfig{
					Name: "guaranteed_payments",
					Type: "CURRENCY_AMOUNT",
					Description: "Guaranteed payments if shown",
				},
				il.CurrencyAmountFieldConfig{
					Name: "distributions",
					Type: "CURRENCY_AMOUNT",
					Description: "Distributions if shown",
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
  "name": "Extract Schedule K 1 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Schedule K 1 Data\n\nTax and finance teams use this recipe to extract Schedule K 1 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-schedule-k-1-data-overview",
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
      "id": "extract-schedule-k-1-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"entity_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Partnership, S corporation, estate, or trust name\"\n    },\n    {\n      \"name\": \"entity_ein\",\n      \"type\": \"TEXT\",\n      \"description\": \"Entity employer identification number\"\n    },\n    {\n      \"name\": \"partner_or_shareholder_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Partner, shareholder, or beneficiary name\"\n    },\n    {\n      \"name\": \"taxpayer_identification_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Partner, shareholder, or beneficiary TIN\"\n    },\n    {\n      \"name\": \"tax_year\",\n      \"type\": \"TEXT\",\n      \"description\": \"Tax year\"\n    },\n    {\n      \"name\": \"profit_share_percent\",\n      \"type\": \"DECIMAL\",\n      \"description\": \"Profit share percentage\"\n    },\n    {\n      \"name\": \"loss_share_percent\",\n      \"type\": \"DECIMAL\",\n      \"description\": \"Loss share percentage\"\n    },\n    {\n      \"name\": \"ordinary_business_income\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Ordinary business income or loss\"\n    },\n    {\n      \"name\": \"rental_real_estate_income\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Net rental real estate income or loss\"\n    },\n    {\n      \"name\": \"guaranteed_payments\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Guaranteed payments if shown\"\n    },\n    {\n      \"name\": \"distributions\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Distributions if shown\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "schedule-k-1.pdf",
              "fileUrl": "https://example.com/documents/schedule-k-1-sample.pdf"
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
      "id": "extract-schedule-k-1-data-extract",
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
Extract schedule k 1 data from the file at [file URL]. Use the extract_document tool with these fields:

- entity_name (TEXT): Partnership, S corporation, estate, or trust name
- entity_ein (TEXT): Entity employer identification number
- partner_or_shareholder_name (TEXT): Partner, shareholder, or beneficiary name
- taxpayer_identification_number (TEXT): Partner, shareholder, or beneficiary TIN
- tax_year (TEXT): Tax year
- profit_share_percent (DECIMAL): Profit share percentage
- loss_share_percent (DECIMAL): Loss share percentage
- ordinary_business_income (CURRENCY_AMOUNT): Ordinary business income or loss
- rental_real_estate_income (CURRENCY_AMOUNT): Net rental real estate income or loss
- guaranteed_payments (CURRENCY_AMOUNT): Guaranteed payments if shown
- distributions (CURRENCY_AMOUNT): Distributions if shown
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
    "entity_ein": {
      "value": "Entity Ein",
      "confidence": 0.97,
      "citations": [
        "ENTITY EIN"
      ]
    },
    "partner_or_shareholder_name": {
      "value": "Partner Or Shareholder Name",
      "confidence": 0.97,
      "citations": [
        "PARTNER OR SHAREHOLDER NAME"
      ]
    },
    "taxpayer_identification_number": {
      "value": "12-3456789",
      "confidence": 0.97,
      "citations": [
        "TAXPAYER IDENTIFICATION NUMBER"
      ]
    },
    "tax_year": {
      "value": "Tax Year",
      "confidence": 0.97,
      "citations": [
        "TAX YEAR"
      ]
    },
    "profit_share_percent": {
      "value": 12.5,
      "confidence": 0.97,
      "citations": [
        "PROFIT SHARE PERCENT"
      ]
    },
    "loss_share_percent": {
      "value": 12.5,
      "confidence": 0.97,
      "citations": [
        "LOSS SHARE PERCENT"
      ]
    },
    "ordinary_business_income": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "rental_real_estate_income": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "guaranteed_payments": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "distributions": {
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
