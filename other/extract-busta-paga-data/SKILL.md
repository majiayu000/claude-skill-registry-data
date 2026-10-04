---
name: extract-busta-paga-data
description: Extract employee, employer, gross pay, INPS/IRPEF deductions, and net pay from Italian payslips.
---

# Extract Busta Paga Data

Payroll and HR teams use this recipe to extract Italian busta paga fields into structured payroll records for reconciliation and employee document workflows.

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
      "name": "busta-paga.pdf",
      "url": "https://example.com/documents/busta-paga-sample.pdf"
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
        "name": "employee_tax_code",
        "type": "TEXT",
        "description": "Employee codice fiscale"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_code",
        "type": "TEXT",
        "description": "Employer tax code or VAT number"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Payslip month or period date"
      },
      {
        "name": "qualification_level",
        "type": "TEXT",
        "description": "Employee qualification, level, or contract classification"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Retribuzione lorda"
      },
      {
        "name": "earnings",
        "type": "ARRAY",
        "description": "Earnings rows",
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
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows including INPS, IRPEF, regional, and municipal deductions",
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
        "name": "taxable_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable income"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount paid"
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
      "name": "busta-paga.pdf",
      "url": "https://example.com/documents/busta-paga-sample.pdf"
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
        "name": "employee_tax_code",
        "type": "TEXT",
        "description": "Employee codice fiscale"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_code",
        "type": "TEXT",
        "description": "Employer tax code or VAT number"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Payslip month or period date"
      },
      {
        "name": "qualification_level",
        "type": "TEXT",
        "description": "Employee qualification, level, or contract classification"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Retribuzione lorda"
      },
      {
        "name": "earnings",
        "type": "ARRAY",
        "description": "Earnings rows",
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
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows including INPS, IRPEF, regional, and municipal deductions",
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
        "name": "taxable_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable income"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount paid"
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
      "name": "busta-paga.pdf",
      "url": "https://example.com/documents/busta-paga-sample.pdf"
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
        "name": "employee_tax_code",
        "type": "TEXT",
        "description": "Employee codice fiscale"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "employer_tax_code",
        "type": "TEXT",
        "description": "Employer tax code or VAT number"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Payslip month or period date"
      },
      {
        "name": "qualification_level",
        "type": "TEXT",
        "description": "Employee qualification, level, or contract classification"
      },
      {
        "name": "gross_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Retribuzione lorda"
      },
      {
        "name": "earnings",
        "type": "ARRAY",
        "description": "Earnings rows",
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
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows including INPS, IRPEF, regional, and municipal deductions",
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
        "name": "taxable_income",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable income"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net amount paid"
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
				Name: "busta-paga.pdf",
				Url: "https://example.com/documents/busta-paga-sample.pdf",
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
					Name: "employee_tax_code",
					Type: "TEXT",
					Description: "Employee codice fiscale",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer name",
				},
				il.TextFieldConfig{
					Name: "employer_tax_code",
					Type: "TEXT",
					Description: "Employer tax code or VAT number",
				},
				il.DateFieldConfig{
					Name: "pay_period",
					Type: "DATE",
					Description: "Payslip month or period date",
				},
				il.TextFieldConfig{
					Name: "qualification_level",
					Type: "TEXT",
					Description: "Employee qualification, level, or contract classification",
				},
				il.CurrencyAmountFieldConfig{
					Name: "gross_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Retribuzione lorda",
				},
				il.ArrayFieldConfig{
					Name: "earnings",
					Type: "ARRAY",
					Description: "Earnings rows",
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
					Name: "deductions",
					Type: "ARRAY",
					Description: "Deduction rows including INPS, IRPEF, regional, and municipal deductions",
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
					Name: "taxable_income",
					Type: "CURRENCY_AMOUNT",
					Description: "Taxable income",
				},
				il.CurrencyAmountFieldConfig{
					Name: "net_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Net amount paid",
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
  "name": "Extract Busta Paga Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Busta Paga Data\n\nPayroll and HR teams use this recipe to extract Italian busta paga fields into structured payroll records for reconciliation and employee document workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-busta-paga-data-overview",
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
      "id": "extract-busta-paga-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee name\"\n    },\n    {\n      \"name\": \"employee_tax_code\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee codice fiscale\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer name\"\n    },\n    {\n      \"name\": \"employer_tax_code\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer tax code or VAT number\"\n    },\n    {\n      \"name\": \"pay_period\",\n      \"type\": \"DATE\",\n      \"description\": \"Payslip month or period date\"\n    },\n    {\n      \"name\": \"qualification_level\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee qualification, level, or contract classification\"\n    },\n    {\n      \"name\": \"gross_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Retribuzione lorda\"\n    },\n    {\n      \"name\": \"earnings\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Earnings rows\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Earning description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Earning amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"deductions\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Deduction rows including INPS, IRPEF, regional, and municipal deductions\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Deduction description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Deduction amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"taxable_income\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Taxable income\"\n    },\n    {\n      \"name\": \"net_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Net amount paid\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "busta-paga.pdf",
              "fileUrl": "https://example.com/documents/busta-paga-sample.pdf"
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
      "id": "extract-busta-paga-data-extract",
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
Extract busta paga data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_name (TEXT): Employee name
- employee_tax_code (TEXT): Employee codice fiscale
- employer_name (TEXT): Employer name
- employer_tax_code (TEXT): Employer tax code or VAT number
- pay_period (DATE): Payslip month or period date
- qualification_level (TEXT): Employee qualification, level, or contract classification
- gross_pay (CURRENCY_AMOUNT): Retribuzione lorda
- earnings (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- deductions (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- taxable_income (CURRENCY_AMOUNT): Taxable income
- net_pay (CURRENCY_AMOUNT): Net amount paid
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
    "employee_tax_code": {
      "value": "Employee Tax Code",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE TAX CODE"
      ]
    },
    "employer_name": {
      "value": "Northwind GmbH",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "employer_tax_code": {
      "value": "Employer Tax Code",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER TAX CODE"
      ]
    },
    "pay_period": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "qualification_level": {
      "value": "Qualification Level",
      "confidence": 0.97,
      "citations": [
        "QUALIFICATION LEVEL"
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
    "earnings": {
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
        "EARNINGS"
      ]
    },
    "deductions": {
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
        "DEDUCTIONS"
      ]
    },
    "taxable_income": {
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
