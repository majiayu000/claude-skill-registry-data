---
name: extract-cfdi-nomina-data
description: Extract structured fields from cfdi nomina documents.
---

# Extract Cfdi Nomina Data

Payroll and HR teams use this recipe to extract Cfdi Nomina fields into structured JSON for payroll checks, employee records, and finance reconciliation.

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
      "name": "cfdi-nomina.pdf",
      "url": "https://example.com/documents/cfdi-nomina-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employee_identifier",
        "type": "TEXT",
        "description": "Employee, payroll, or taxpayer identifier"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Pay period, statement, or tax year end date"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Gross pay or taxable compensation"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax withheld"
      },
      {
        "name": "social_contributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security or payroll contributions"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net pay"
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
      "name": "cfdi-nomina.pdf",
      "url": "https://example.com/documents/cfdi-nomina-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employee_identifier",
        "type": "TEXT",
        "description": "Employee, payroll, or taxpayer identifier"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Pay period, statement, or tax year end date"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Gross pay or taxable compensation"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax withheld"
      },
      {
        "name": "social_contributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security or payroll contributions"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net pay"
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
      "name": "cfdi-nomina.pdf",
      "url": "https://example.com/documents/cfdi-nomina-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_name",
        "type": "TEXT",
        "description": "Employee name"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employee_identifier",
        "type": "TEXT",
        "description": "Employee, payroll, or taxpayer identifier"
      },
      {
        "name": "period_end_date",
        "type": "DATE",
        "description": "Pay period, statement, or tax year end date"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Gross pay or taxable compensation"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax withheld"
      },
      {
        "name": "social_contributions",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security or payroll contributions"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net pay"
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
				Name: "cfdi-nomina.pdf",
				Url: "https://example.com/documents/cfdi-nomina-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "employee_name",
					Type: "TEXT",
					Description: "Employee name",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer name",
				},
				il.TextFieldConfig{
					Name: "employee_identifier",
					Type: "TEXT",
					Description: "Employee, payroll, or taxpayer identifier",
				},
				il.DateFieldConfig{
					Name: "period_end_date",
					Type: "DATE",
					Description: "Pay period, statement, or tax year end date",
				},
				il.CurrencyAmountFieldConfig{
					Name: "gross_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Gross pay or taxable compensation",
				},
				il.CurrencyAmountFieldConfig{
					Name: "tax_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "Tax withheld",
				},
				il.CurrencyAmountFieldConfig{
					Name: "social_contributions",
					Type: "CURRENCY_AMOUNT",
					Description: "Social security or payroll contributions",
				},
				il.CurrencyAmountFieldConfig{
					Name: "net_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Net pay",
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
  "name": "Extract Cfdi Nomina Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Cfdi Nomina Data\n\nPayroll and HR teams use this recipe to extract Cfdi Nomina fields into structured JSON for payroll checks, employee records, and finance reconciliation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-cfdi-nomina-data-overview",
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
      "id": "extract-cfdi-nomina-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee name\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer name\"\n    },\n    {\n      \"name\": \"employee_identifier\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee, payroll, or taxpayer identifier\"\n    },\n    {\n      \"name\": \"period_end_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Pay period, statement, or tax year end date\"\n    },\n    {\n      \"name\": \"gross_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Gross pay or taxable compensation\"\n    },\n    {\n      \"name\": \"tax_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Tax withheld\"\n    },\n    {\n      \"name\": \"social_contributions\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Social security or payroll contributions\"\n    },\n    {\n      \"name\": \"net_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Net pay\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "cfdi-nomina.pdf",
              "fileUrl": "https://example.com/documents/cfdi-nomina-sample.pdf"
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
      "id": "extract-cfdi-nomina-data-extract",
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
Extract cfdi nomina data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_name (TEXT): Employee name
- employer_name (TEXT): Employer name
- employee_identifier (TEXT): Employee, payroll, or taxpayer identifier
- period_end_date (DATE): Pay period, statement, or tax year end date
- gross_pay (CURRENCY_AMOUNT): Gross pay or taxable compensation
- tax_withheld (CURRENCY_AMOUNT): Tax withheld
- social_contributions (CURRENCY_AMOUNT): Social security or payroll contributions
- net_pay (CURRENCY_AMOUNT): Net pay
- currency (CURRENCY_CODE): Currency code
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
    "employer_name": {
      "value": "Employer Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "employee_identifier": {
      "value": "Employee Identifier",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE IDENTIFIER"
      ]
    },
    "period_end_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "gross_pay": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "tax_withheld": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "social_contributions": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "net_pay": {
      "value": {
        "amount": "1234.56",
        "currency": "USD"
      },
      "confidence": 0.97,
      "citations": [
        "$1,234.56"
      ]
    },
    "currency": {
      "value": "USD",
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
