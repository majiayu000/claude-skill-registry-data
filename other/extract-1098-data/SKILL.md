---
name: extract-1098-data
description: Extract structured fields from 1098 documents.
---

# Extract 1098 Data

Tax and finance teams use this recipe to extract 1098 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "1098.pdf",
      "url": "https://example.com/documents/1098-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_borrower_name",
        "type": "TEXT",
        "description": "Payer or borrower name"
      },
      {
        "name": "payer_borrower_tin",
        "type": "TEXT",
        "description": "Payer or borrower TIN"
      },
      {
        "name": "recipient_lender_name",
        "type": "TEXT",
        "description": "Recipient or lender name"
      },
      {
        "name": "recipient_lender_tin",
        "type": "TEXT",
        "description": "Recipient or lender TIN"
      },
      {
        "name": "mortgage_account_number",
        "type": "TEXT",
        "description": "Mortgage account number"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "mortgage_interest_received",
        "type": "CURRENCY_AMOUNT",
        "description": "Mortgage interest received from payer"
      },
      {
        "name": "outstanding_mortgage_principal",
        "type": "CURRENCY_AMOUNT",
        "description": "Outstanding mortgage principal"
      },
      {
        "name": "mortgage_origination_date",
        "type": "DATE",
        "description": "Mortgage origination date"
      },
      {
        "name": "points_paid",
        "type": "CURRENCY_AMOUNT",
        "description": "Points paid on purchase of principal residence"
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
      "name": "1098.pdf",
      "url": "https://example.com/documents/1098-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_borrower_name",
        "type": "TEXT",
        "description": "Payer or borrower name"
      },
      {
        "name": "payer_borrower_tin",
        "type": "TEXT",
        "description": "Payer or borrower TIN"
      },
      {
        "name": "recipient_lender_name",
        "type": "TEXT",
        "description": "Recipient or lender name"
      },
      {
        "name": "recipient_lender_tin",
        "type": "TEXT",
        "description": "Recipient or lender TIN"
      },
      {
        "name": "mortgage_account_number",
        "type": "TEXT",
        "description": "Mortgage account number"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "mortgage_interest_received",
        "type": "CURRENCY_AMOUNT",
        "description": "Mortgage interest received from payer"
      },
      {
        "name": "outstanding_mortgage_principal",
        "type": "CURRENCY_AMOUNT",
        "description": "Outstanding mortgage principal"
      },
      {
        "name": "mortgage_origination_date",
        "type": "DATE",
        "description": "Mortgage origination date"
      },
      {
        "name": "points_paid",
        "type": "CURRENCY_AMOUNT",
        "description": "Points paid on purchase of principal residence"
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
      "name": "1098.pdf",
      "url": "https://example.com/documents/1098-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "payer_borrower_name",
        "type": "TEXT",
        "description": "Payer or borrower name"
      },
      {
        "name": "payer_borrower_tin",
        "type": "TEXT",
        "description": "Payer or borrower TIN"
      },
      {
        "name": "recipient_lender_name",
        "type": "TEXT",
        "description": "Recipient or lender name"
      },
      {
        "name": "recipient_lender_tin",
        "type": "TEXT",
        "description": "Recipient or lender TIN"
      },
      {
        "name": "mortgage_account_number",
        "type": "TEXT",
        "description": "Mortgage account number"
      },
      {
        "name": "tax_year",
        "type": "TEXT",
        "description": "Tax year"
      },
      {
        "name": "mortgage_interest_received",
        "type": "CURRENCY_AMOUNT",
        "description": "Mortgage interest received from payer"
      },
      {
        "name": "outstanding_mortgage_principal",
        "type": "CURRENCY_AMOUNT",
        "description": "Outstanding mortgage principal"
      },
      {
        "name": "mortgage_origination_date",
        "type": "DATE",
        "description": "Mortgage origination date"
      },
      {
        "name": "points_paid",
        "type": "CURRENCY_AMOUNT",
        "description": "Points paid on purchase of principal residence"
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
				Name: "1098.pdf",
				Url: "https://example.com/documents/1098-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "payer_borrower_name",
					Type: "TEXT",
					Description: "Payer or borrower name",
				},
				il.TextFieldConfig{
					Name: "payer_borrower_tin",
					Type: "TEXT",
					Description: "Payer or borrower TIN",
				},
				il.TextFieldConfig{
					Name: "recipient_lender_name",
					Type: "TEXT",
					Description: "Recipient or lender name",
				},
				il.TextFieldConfig{
					Name: "recipient_lender_tin",
					Type: "TEXT",
					Description: "Recipient or lender TIN",
				},
				il.TextFieldConfig{
					Name: "mortgage_account_number",
					Type: "TEXT",
					Description: "Mortgage account number",
				},
				il.TextFieldConfig{
					Name: "tax_year",
					Type: "TEXT",
					Description: "Tax year",
				},
				il.CurrencyAmountFieldConfig{
					Name: "mortgage_interest_received",
					Type: "CURRENCY_AMOUNT",
					Description: "Mortgage interest received from payer",
				},
				il.CurrencyAmountFieldConfig{
					Name: "outstanding_mortgage_principal",
					Type: "CURRENCY_AMOUNT",
					Description: "Outstanding mortgage principal",
				},
				il.DateFieldConfig{
					Name: "mortgage_origination_date",
					Type: "DATE",
					Description: "Mortgage origination date",
				},
				il.CurrencyAmountFieldConfig{
					Name: "points_paid",
					Type: "CURRENCY_AMOUNT",
					Description: "Points paid on purchase of principal residence",
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
  "name": "Extract 1098 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract 1098 Data\n\nTax and finance teams use this recipe to extract 1098 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-1098-data-overview",
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
      "id": "extract-1098-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"payer_borrower_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer or borrower name\"\n    },\n    {\n      \"name\": \"payer_borrower_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Payer or borrower TIN\"\n    },\n    {\n      \"name\": \"recipient_lender_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Recipient or lender name\"\n    },\n    {\n      \"name\": \"recipient_lender_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Recipient or lender TIN\"\n    },\n    {\n      \"name\": \"mortgage_account_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Mortgage account number\"\n    },\n    {\n      \"name\": \"tax_year\",\n      \"type\": \"TEXT\",\n      \"description\": \"Tax year\"\n    },\n    {\n      \"name\": \"mortgage_interest_received\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Mortgage interest received from payer\"\n    },\n    {\n      \"name\": \"outstanding_mortgage_principal\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Outstanding mortgage principal\"\n    },\n    {\n      \"name\": \"mortgage_origination_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Mortgage origination date\"\n    },\n    {\n      \"name\": \"points_paid\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Points paid on purchase of principal residence\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "1098.pdf",
              "fileUrl": "https://example.com/documents/1098-sample.pdf"
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
      "id": "extract-1098-data-extract",
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
Extract 1098 data from the file at [file URL]. Use the extract_document tool with these fields:

- payer_borrower_name (TEXT): Payer or borrower name
- payer_borrower_tin (TEXT): Payer or borrower TIN
- recipient_lender_name (TEXT): Recipient or lender name
- recipient_lender_tin (TEXT): Recipient or lender TIN
- mortgage_account_number (TEXT): Mortgage account number
- tax_year (TEXT): Tax year
- mortgage_interest_received (CURRENCY_AMOUNT): Mortgage interest received from payer
- outstanding_mortgage_principal (CURRENCY_AMOUNT): Outstanding mortgage principal
- mortgage_origination_date (DATE): Mortgage origination date
- points_paid (CURRENCY_AMOUNT): Points paid on purchase of principal residence
```

### Response


```json
{
  "success": true,
  "data": {
    "payer_borrower_name": {
      "value": "Payer Borrower Name",
      "confidence": 0.97,
      "citations": [
        "PAYER BORROWER NAME"
      ]
    },
    "payer_borrower_tin": {
      "value": "Payer Borrower Tin",
      "confidence": 0.97,
      "citations": [
        "PAYER BORROWER TIN"
      ]
    },
    "recipient_lender_name": {
      "value": "Recipient Lender Name",
      "confidence": 0.97,
      "citations": [
        "RECIPIENT LENDER NAME"
      ]
    },
    "recipient_lender_tin": {
      "value": "Recipient Lender Tin",
      "confidence": 0.97,
      "citations": [
        "RECIPIENT LENDER TIN"
      ]
    },
    "mortgage_account_number": {
      "value": "Mortgage Account Number",
      "confidence": 0.97,
      "citations": [
        "MORTGAGE ACCOUNT NUMBER"
      ]
    },
    "tax_year": {
      "value": "Tax Year",
      "confidence": 0.97,
      "citations": [
        "TAX YEAR"
      ]
    },
    "mortgage_interest_received": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "outstanding_mortgage_principal": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "mortgage_origination_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "points_paid": {
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
