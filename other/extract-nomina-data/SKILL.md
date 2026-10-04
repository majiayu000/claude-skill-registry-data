---
name: extract-nomina-data
description: Extract employee, employer, earnings, deductions, tax, and net pay from Spanish or Latin American payroll slips.
---

# Extract Nomina Data

Payroll and finance teams use this recipe to extract nomina fields into structured JSON for payroll checks, employee portals, and accounting reconciliation.

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
      "name": "nomina.pdf",
      "url": "https://example.com/documents/nomina-sample.pdf"
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
        "name": "employee_tax_id",
        "type": "TEXT",
        "description": "Employee tax or national ID"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_id",
        "type": "TEXT",
        "description": "Employer tax ID"
      },
      {
        "name": "pay_period_start",
        "type": "DATE",
        "description": "Pay period start date"
      },
      {
        "name": "pay_period_end",
        "type": "DATE",
        "description": "Pay period end date"
      },
      {
        "name": "percepciones",
        "type": "ARRAY",
        "description": "Earnings or percepciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Earning description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Earning amount"
          }
        ]
      },
      {
        "name": "deducciones",
        "type": "ARRAY",
        "description": "Deductions or deducciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Deduction description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Deduction amount"
          }
        ]
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Total percepciones or gross pay"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax withheld"
      },
      {
        "name": "social_security",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security contribution"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Neto a pagar"
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
      "name": "nomina.pdf",
      "url": "https://example.com/documents/nomina-sample.pdf"
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
        "name": "employee_tax_id",
        "type": "TEXT",
        "description": "Employee tax or national ID"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_id",
        "type": "TEXT",
        "description": "Employer tax ID"
      },
      {
        "name": "pay_period_start",
        "type": "DATE",
        "description": "Pay period start date"
      },
      {
        "name": "pay_period_end",
        "type": "DATE",
        "description": "Pay period end date"
      },
      {
        "name": "percepciones",
        "type": "ARRAY",
        "description": "Earnings or percepciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Earning description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Earning amount"
          }
        ]
      },
      {
        "name": "deducciones",
        "type": "ARRAY",
        "description": "Deductions or deducciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Deduction description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Deduction amount"
          }
        ]
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Total percepciones or gross pay"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax withheld"
      },
      {
        "name": "social_security",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security contribution"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Neto a pagar"
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
      "name": "nomina.pdf",
      "url": "https://example.com/documents/nomina-sample.pdf"
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
        "name": "employee_tax_id",
        "type": "TEXT",
        "description": "Employee tax or national ID"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_id",
        "type": "TEXT",
        "description": "Employer tax ID"
      },
      {
        "name": "pay_period_start",
        "type": "DATE",
        "description": "Pay period start date"
      },
      {
        "name": "pay_period_end",
        "type": "DATE",
        "description": "Pay period end date"
      },
      {
        "name": "percepciones",
        "type": "ARRAY",
        "description": "Earnings or percepciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Earning description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Earning amount"
          }
        ]
      },
      {
        "name": "deducciones",
        "type": "ARRAY",
        "description": "Deductions or deducciones",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Deduction description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Deduction amount"
          }
        ]
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Total percepciones or gross pay"
      },
      {
        "name": "tax_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax withheld"
      },
      {
        "name": "social_security",
        "type": "CURRENCY_AMOUNT",
        "description": "Social security contribution"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Neto a pagar"
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
				Name: "nomina.pdf",
				Url: "https://example.com/documents/nomina-sample.pdf",
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
					Name: "employee_tax_id",
					Type: "TEXT",
					Description: "Employee tax or national ID",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer name",
				},
				il.TextFieldConfig{
					Name: "employer_tax_id",
					Type: "TEXT",
					Description: "Employer tax ID",
				},
				il.DateFieldConfig{
					Name: "pay_period_start",
					Type: "DATE",
					Description: "Pay period start date",
				},
				il.DateFieldConfig{
					Name: "pay_period_end",
					Type: "DATE",
					Description: "Pay period end date",
				},
				il.ArrayFieldConfig{
					Name: "percepciones",
					Type: "ARRAY",
					Description: "Earnings or percepciones",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Earning description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Earning amount",
						},
					},
				},
				il.ArrayFieldConfig{
					Name: "deducciones",
					Type: "ARRAY",
					Description: "Deductions or deducciones",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Deduction description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Deduction amount",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "gross_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Total percepciones or gross pay",
				},
				il.CurrencyAmountFieldConfig{
					Name: "tax_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "Income tax withheld",
				},
				il.CurrencyAmountFieldConfig{
					Name: "social_security",
					Type: "CURRENCY_AMOUNT",
					Description: "Social security contribution",
				},
				il.CurrencyAmountFieldConfig{
					Name: "net_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Neto a pagar",
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
  "name": "Extract Nomina Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Nomina Data\n\nPayroll and finance teams use this recipe to extract nomina fields into structured JSON for payroll checks, employee portals, and accounting reconciliation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-nomina-data-overview",
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
      "id": "extract-nomina-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee name\"\n    },\n    {\n      \"name\": \"employee_tax_id\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee tax or national ID\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer name\"\n    },\n    {\n      \"name\": \"employer_tax_id\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer tax ID\"\n    },\n    {\n      \"name\": \"pay_period_start\",\n      \"type\": \"DATE\",\n      \"description\": \"Pay period start date\"\n    },\n    {\n      \"name\": \"pay_period_end\",\n      \"type\": \"DATE\",\n      \"description\": \"Pay period end date\"\n    },\n    {\n      \"name\": \"percepciones\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Earnings or percepciones\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Earning description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Earning amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"deducciones\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Deductions or deducciones\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Deduction description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Deduction amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"gross_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total percepciones or gross pay\"\n    },\n    {\n      \"name\": \"tax_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Income tax withheld\"\n    },\n    {\n      \"name\": \"social_security\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Social security contribution\"\n    },\n    {\n      \"name\": \"net_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Neto a pagar\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "nomina.pdf",
              "fileUrl": "https://example.com/documents/nomina-sample.pdf"
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
      "id": "extract-nomina-data-extract",
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
Extract nomina data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_name (TEXT): Employee name
- employee_tax_id (TEXT): Employee tax or national ID
- employer_name (TEXT): Employer name
- employer_tax_id (TEXT): Employer tax ID
- pay_period_start (DATE): Pay period start date
- pay_period_end (DATE): Pay period end date
- percepciones (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- deducciones (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- gross_pay (CURRENCY_AMOUNT): Total percepciones or gross pay
- tax_withheld (CURRENCY_AMOUNT): Income tax withheld
- social_security (CURRENCY_AMOUNT): Social security contribution
- net_pay (CURRENCY_AMOUNT): Neto a pagar
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "employee_name": {
      "value": "Maria Keller",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE NAME"
      ]
    },
    "employee_tax_id": {
      "value": "Employee Tax Id",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE TAX ID"
      ]
    },
    "employer_name": {
      "value": "Northwind GmbH",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "employer_tax_id": {
      "value": "Employer Tax Id",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER TAX ID"
      ]
    },
    "pay_period_start": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "pay_period_end": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "percepciones": {
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
        "PERCEPCIONES"
      ]
    },
    "deducciones": {
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
        "DEDUCCIONES"
      ]
    },
    "gross_pay": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "tax_withheld": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "social_security": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "net_pay": {
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
