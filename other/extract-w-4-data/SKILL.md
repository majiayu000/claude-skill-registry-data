---
name: extract-w-4-data
description: Extract structured fields from w-4 documents.
---

# Extract W-4 Data

Tax and finance teams use this recipe to extract W-4 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "w-4.pdf",
      "url": "https://example.com/documents/w-4-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee full name"
      },
      {
        "name": "social_security_number",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "filing_status",
        "type": "TEXT",
        "description": "Selected filing status"
      },
      {
        "name": "dependents_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 3 dependent and other credits amount"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(a) other income"
      },
      {
        "name": "deductions",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(b) deductions"
      },
      {
        "name": "extra_withholding",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(c) extra withholding"
      },
      {
        "name": "is_signed",
        "type": "BOOLEAN",
        "description": "Whether the employee signature is present"
      },
      {
        "name": "signature_date",
        "type": "DATE",
        "description": "Date signed"
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
      "name": "w-4.pdf",
      "url": "https://example.com/documents/w-4-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee full name"
      },
      {
        "name": "social_security_number",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "filing_status",
        "type": "TEXT",
        "description": "Selected filing status"
      },
      {
        "name": "dependents_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 3 dependent and other credits amount"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(a) other income"
      },
      {
        "name": "deductions",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(b) deductions"
      },
      {
        "name": "extra_withholding",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(c) extra withholding"
      },
      {
        "name": "is_signed",
        "type": "BOOLEAN",
        "description": "Whether the employee signature is present"
      },
      {
        "name": "signature_date",
        "type": "DATE",
        "description": "Date signed"
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
      "name": "w-4.pdf",
      "url": "https://example.com/documents/w-4-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee full name"
      },
      {
        "name": "social_security_number",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "filing_status",
        "type": "TEXT",
        "description": "Selected filing status"
      },
      {
        "name": "dependents_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 3 dependent and other credits amount"
      },
      {
        "name": "other_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(a) other income"
      },
      {
        "name": "deductions",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(b) deductions"
      },
      {
        "name": "extra_withholding",
        "type": "CURRENCY_AMOUNT",
        "description": "Step 4(c) extra withholding"
      },
      {
        "name": "is_signed",
        "type": "BOOLEAN",
        "description": "Whether the employee signature is present"
      },
      {
        "name": "signature_date",
        "type": "DATE",
        "description": "Date signed"
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
				Name: "w-4.pdf",
				Url: "https://example.com/documents/w-4-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "employee_name",
					Type: "TEXT",
					Description: "Employee full name",
				},
				il.TextFieldConfig{
					Name: "social_security_number",
					Type: "TEXT",
					Description: "Employee Social Security number",
				},
				il.AddressFieldConfig{
					Name: "address",
					Type: "ADDRESS",
					Description: "Employee address",
				},
				il.TextFieldConfig{
					Name: "filing_status",
					Type: "TEXT",
					Description: "Selected filing status",
				},
				il.CurrencyAmountFieldConfig{
					Name: "dependents_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Step 3 dependent and other credits amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "other_income",
					Type: "CURRENCY_AMOUNT",
					Description: "Step 4(a) other income",
				},
				il.CurrencyAmountFieldConfig{
					Name: "deductions",
					Type: "CURRENCY_AMOUNT",
					Description: "Step 4(b) deductions",
				},
				il.CurrencyAmountFieldConfig{
					Name: "extra_withholding",
					Type: "CURRENCY_AMOUNT",
					Description: "Step 4(c) extra withholding",
				},
				il.BooleanFieldConfig{
					Name: "is_signed",
					Type: "BOOLEAN",
					Description: "Whether the employee signature is present",
				},
				il.DateFieldConfig{
					Name: "signature_date",
					Type: "DATE",
					Description: "Date signed",
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
  "name": "Extract W-4 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract W-4 Data\n\nTax and finance teams use this recipe to extract W-4 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-w-4-data-overview",
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
      "id": "extract-w-4-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee full name\"\n    },\n    {\n      \"name\": \"social_security_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee Social Security number\"\n    },\n    {\n      \"name\": \"address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Employee address\"\n    },\n    {\n      \"name\": \"filing_status\",\n      \"type\": \"TEXT\",\n      \"description\": \"Selected filing status\"\n    },\n    {\n      \"name\": \"dependents_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Step 3 dependent and other credits amount\"\n    },\n    {\n      \"name\": \"other_income\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Step 4(a) other income\"\n    },\n    {\n      \"name\": \"deductions\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Step 4(b) deductions\"\n    },\n    {\n      \"name\": \"extra_withholding\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Step 4(c) extra withholding\"\n    },\n    {\n      \"name\": \"is_signed\",\n      \"type\": \"BOOLEAN\",\n      \"description\": \"Whether the employee signature is present\"\n    },\n    {\n      \"name\": \"signature_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Date signed\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "w-4.pdf",
              "fileUrl": "https://example.com/documents/w-4-sample.pdf"
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
      "id": "extract-w-4-data-extract",
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
Extract w-4 data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_name (TEXT): Employee full name
- social_security_number (TEXT): Employee Social Security number
- address (ADDRESS): Employee address
- filing_status (TEXT): Selected filing status
- dependents_amount (CURRENCY_AMOUNT): Step 3 dependent and other credits amount
- other_income (CURRENCY_AMOUNT): Step 4(a) other income
- deductions (CURRENCY_AMOUNT): Step 4(b) deductions
- extra_withholding (CURRENCY_AMOUNT): Step 4(c) extra withholding
- is_signed (BOOLEAN): Whether the employee signature is present
- signature_date (DATE): Date signed
```

### Response


```json
{
  "success": true,
  "data": {
    "employee_name": {
      "value": "Employee Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE NAME"
      ]
    },
    "social_security_number": {
      "value": "Social Security Number",
      "confidence": 0.97,
      "citations": [
        "SOCIAL SECURITY NUMBER"
      ]
    },
    "address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "ADDRESS"
      ]
    },
    "filing_status": {
      "value": "Filing Status",
      "confidence": 0.97,
      "citations": [
        "FILING STATUS"
      ]
    },
    "dependents_amount": {
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
    "deductions": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "extra_withholding": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "is_signed": {
      "value": true,
      "confidence": 0.97,
      "citations": [
        "IS SIGNED"
      ]
    },
    "signature_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
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
