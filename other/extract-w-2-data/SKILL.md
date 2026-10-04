---
name: extract-w-2-data
description: Extract structured fields from w-2 documents.
---

# Extract W-2 Data

Tax and finance teams use this recipe to extract W-2 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "w-2.pdf",
      "url": "https://example.com/documents/w-2-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_ssn",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "employer_ein",
        "type": "TEXT",
        "description": "Employer identification number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_address",
        "type": "ADDRESS",
        "description": "Employer address"
      },
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "wages_tips_other_compensation",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 wages, tips, and other compensation"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 federal income tax withheld"
      },
      {
        "name": "social_security_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 Social Security wages"
      },
      {
        "name": "medicare_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 5 Medicare wages and tips"
      },
      {
        "name": "state",
        "type": "TEXT",
        "description": "State code"
      },
      {
        "name": "state_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "State wages, tips, etc."
      },
      {
        "name": "state_income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "State income tax withheld"
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
      "name": "w-2.pdf",
      "url": "https://example.com/documents/w-2-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_ssn",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "employer_ein",
        "type": "TEXT",
        "description": "Employer identification number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_address",
        "type": "ADDRESS",
        "description": "Employer address"
      },
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "wages_tips_other_compensation",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 wages, tips, and other compensation"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 federal income tax withheld"
      },
      {
        "name": "social_security_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 Social Security wages"
      },
      {
        "name": "medicare_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 5 Medicare wages and tips"
      },
      {
        "name": "state",
        "type": "TEXT",
        "description": "State code"
      },
      {
        "name": "state_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "State wages, tips, etc."
      },
      {
        "name": "state_income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "State income tax withheld"
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
      "name": "w-2.pdf",
      "url": "https://example.com/documents/w-2-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_ssn",
        "type": "TEXT",
        "description": "Employee Social Security number"
      },
      {
        "name": "employer_ein",
        "type": "TEXT",
        "description": "Employer identification number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_address",
        "type": "ADDRESS",
        "description": "Employer address"
      },
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "wages_tips_other_compensation",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 1 wages, tips, and other compensation"
      },
      {
        "name": "federal_income_tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 2 federal income tax withheld"
      },
      {
        "name": "social_security_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 3 Social Security wages"
      },
      {
        "name": "medicare_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "Box 5 Medicare wages and tips"
      },
      {
        "name": "state",
        "type": "TEXT",
        "description": "State code"
      },
      {
        "name": "state_wages",
        "type": "CURRENCY_AMOUNT",
        "description": "State wages, tips, etc."
      },
      {
        "name": "state_income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "State income tax withheld"
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
				Name: "w-2.pdf",
				Url: "https://example.com/documents/w-2-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "employee_ssn",
					Type: "TEXT",
					Description: "Employee Social Security number",
				},
				il.TextFieldConfig{
					Name: "employer_ein",
					Type: "TEXT",
					Description: "Employer identification number",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer name",
				},
				il.AddressFieldConfig{
					Name: "employer_address",
					Type: "ADDRESS",
					Description: "Employer address",
				},
				il.TextFieldConfig{
					Name: "employee_name",
					Type: "TEXT",
					Description: "Employee name",
				},
				il.AddressFieldConfig{
					Name: "employee_address",
					Type: "ADDRESS",
					Description: "Employee address",
				},
				il.CurrencyAmountFieldConfig{
					Name: "wages_tips_other_compensation",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 1 wages, tips, and other compensation",
				},
				il.CurrencyAmountFieldConfig{
					Name: "federal_income_tax_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 2 federal income tax withheld",
				},
				il.CurrencyAmountFieldConfig{
					Name: "social_security_wages",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 3 Social Security wages",
				},
				il.CurrencyAmountFieldConfig{
					Name: "medicare_wages",
					Type: "CURRENCY_AMOUNT",
					Description: "Box 5 Medicare wages and tips",
				},
				il.TextFieldConfig{
					Name: "state",
					Type: "TEXT",
					Description: "State code",
				},
				il.CurrencyAmountFieldConfig{
					Name: "state_wages",
					Type: "CURRENCY_AMOUNT",
					Description: "State wages, tips, etc.",
				},
				il.CurrencyAmountFieldConfig{
					Name: "state_income_tax",
					Type: "CURRENCY_AMOUNT",
					Description: "State income tax withheld",
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
  "name": "Extract W-2 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract W-2 Data\n\nTax and finance teams use this recipe to extract W-2 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-w-2-data-overview",
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
      "id": "extract-w-2-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_ssn\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee Social Security number\"\n    },\n    {\n      \"name\": \"employer_ein\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer identification number\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer name\"\n    },\n    {\n      \"name\": \"employer_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Employer address\"\n    },\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee name\"\n    },\n    {\n      \"name\": \"employee_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Employee address\"\n    },\n    {\n      \"name\": \"wages_tips_other_compensation\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 1 wages, tips, and other compensation\"\n    },\n    {\n      \"name\": \"federal_income_tax_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 2 federal income tax withheld\"\n    },\n    {\n      \"name\": \"social_security_wages\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 3 Social Security wages\"\n    },\n    {\n      \"name\": \"medicare_wages\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Box 5 Medicare wages and tips\"\n    },\n    {\n      \"name\": \"state\",\n      \"type\": \"TEXT\",\n      \"description\": \"State code\"\n    },\n    {\n      \"name\": \"state_wages\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"State wages, tips, etc.\"\n    },\n    {\n      \"name\": \"state_income_tax\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"State income tax withheld\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "w-2.pdf",
              "fileUrl": "https://example.com/documents/w-2-sample.pdf"
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
      "id": "extract-w-2-data-extract",
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
Extract w-2 data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_ssn (TEXT): Employee Social Security number
- employer_ein (TEXT): Employer identification number
- employer_name (TEXT): Employer name
- employer_address (ADDRESS): Employer address
- employee_name (TEXT): Employee name
- employee_address (ADDRESS): Employee address
- wages_tips_other_compensation (CURRENCY_AMOUNT): Box 1 wages, tips, and other compensation
- federal_income_tax_withheld (CURRENCY_AMOUNT): Box 2 federal income tax withheld
- social_security_wages (CURRENCY_AMOUNT): Box 3 Social Security wages
- medicare_wages (CURRENCY_AMOUNT): Box 5 Medicare wages and tips
- state (TEXT): State code
- state_wages (CURRENCY_AMOUNT): State wages, tips, etc.
- state_income_tax (CURRENCY_AMOUNT): State income tax withheld
```

### Response


```json
{
  "success": true,
  "data": {
    "employee_ssn": {
      "value": "***-**-1234",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE SSN"
      ]
    },
    "employer_ein": {
      "value": "12-3456789",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER EIN"
      ]
    },
    "employer_name": {
      "value": "Employer Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "employer_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "EMPLOYER ADDRESS"
      ]
    },
    "employee_name": {
      "value": "Employee Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE NAME"
      ]
    },
    "employee_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE ADDRESS"
      ]
    },
    "wages_tips_other_compensation": {
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
    "social_security_wages": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "medicare_wages": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "state": {
      "value": "State",
      "confidence": 0.97,
      "citations": [
        "STATE"
      ]
    },
    "state_wages": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "state_income_tax": {
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
