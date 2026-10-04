---
name: extract-kyuyo-meisai-data
description: Extract employee, employer, allowances, deductions, taxes, and net pay from Japanese payslips.
---

# Extract Kyuyo Meisai Data

Payroll and HR teams use this recipe to extract Japanese kyuyo meisai fields into structured payroll records for review, reconciliation, and employee systems.

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
      "name": "kyuyo-meisai.pdf",
      "url": "https://example.com/documents/kyuyo-meisai-sample.pdf"
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
        "name": "employee_number",
        "type": "TEXT",
        "description": "Employee number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Salary period or payment date"
      },
      {
        "name": "payments",
        "type": "ARRAY",
        "description": "Payment and allowance rows",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Payment or allowance description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Payment amount"
          }
        ]
      },
      {
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows",
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
        "description": "Gross payment total"
      },
      {
        "name": "income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax deduction"
      },
      {
        "name": "resident_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Resident tax deduction"
      },
      {
        "name": "social_insurance",
        "type": "CURRENCY_AMOUNT",
        "description": "Social insurance deduction"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net transfer amount"
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
      "name": "kyuyo-meisai.pdf",
      "url": "https://example.com/documents/kyuyo-meisai-sample.pdf"
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
        "name": "employee_number",
        "type": "TEXT",
        "description": "Employee number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Salary period or payment date"
      },
      {
        "name": "payments",
        "type": "ARRAY",
        "description": "Payment and allowance rows",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Payment or allowance description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Payment amount"
          }
        ]
      },
      {
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows",
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
        "description": "Gross payment total"
      },
      {
        "name": "income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax deduction"
      },
      {
        "name": "resident_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Resident tax deduction"
      },
      {
        "name": "social_insurance",
        "type": "CURRENCY_AMOUNT",
        "description": "Social insurance deduction"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net transfer amount"
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
      "name": "kyuyo-meisai.pdf",
      "url": "https://example.com/documents/kyuyo-meisai-sample.pdf"
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
        "name": "employee_number",
        "type": "TEXT",
        "description": "Employee number"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer name"
      },
      {
        "name": "pay_period",
        "type": "DATE",
        "description": "Salary period or payment date"
      },
      {
        "name": "payments",
        "type": "ARRAY",
        "description": "Payment and allowance rows",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Payment or allowance description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Payment amount"
          }
        ]
      },
      {
        "name": "deductions",
        "type": "ARRAY",
        "description": "Deduction rows",
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
        "description": "Gross payment total"
      },
      {
        "name": "income_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Income tax deduction"
      },
      {
        "name": "resident_tax",
        "type": "CURRENCY_AMOUNT",
        "description": "Resident tax deduction"
      },
      {
        "name": "social_insurance",
        "type": "CURRENCY_AMOUNT",
        "description": "Social insurance deduction"
      },
      {
        "name": "net_pay",
        "type": "CURRENCY_AMOUNT",
        "description": "Net transfer amount"
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
				Name: "kyuyo-meisai.pdf",
				Url: "https://example.com/documents/kyuyo-meisai-sample.pdf",
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
					Name: "employee_number",
					Type: "TEXT",
					Description: "Employee number",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer name",
				},
				il.DateFieldConfig{
					Name: "pay_period",
					Type: "DATE",
					Description: "Salary period or payment date",
				},
				il.ArrayFieldConfig{
					Name: "payments",
					Type: "ARRAY",
					Description: "Payment and allowance rows",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Payment or allowance description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Payment amount",
						},
					},
				},
				il.ArrayFieldConfig{
					Name: "deductions",
					Type: "ARRAY",
					Description: "Deduction rows",
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
					Description: "Gross payment total",
				},
				il.CurrencyAmountFieldConfig{
					Name: "income_tax",
					Type: "CURRENCY_AMOUNT",
					Description: "Income tax deduction",
				},
				il.CurrencyAmountFieldConfig{
					Name: "resident_tax",
					Type: "CURRENCY_AMOUNT",
					Description: "Resident tax deduction",
				},
				il.CurrencyAmountFieldConfig{
					Name: "social_insurance",
					Type: "CURRENCY_AMOUNT",
					Description: "Social insurance deduction",
				},
				il.CurrencyAmountFieldConfig{
					Name: "net_pay",
					Type: "CURRENCY_AMOUNT",
					Description: "Net transfer amount",
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
  "name": "Extract Kyuyo Meisai Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Kyuyo Meisai Data\n\nPayroll and HR teams use this recipe to extract Japanese kyuyo meisai fields into structured payroll records for review, reconciliation, and employee systems.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-kyuyo-meisai-data-overview",
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
      "id": "extract-kyuyo-meisai-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee name\"\n    },\n    {\n      \"name\": \"employee_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee number\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer name\"\n    },\n    {\n      \"name\": \"pay_period\",\n      \"type\": \"DATE\",\n      \"description\": \"Salary period or payment date\"\n    },\n    {\n      \"name\": \"payments\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Payment and allowance rows\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Payment or allowance description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Payment amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"deductions\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Deduction rows\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Deduction description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Deduction amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"gross_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Gross payment total\"\n    },\n    {\n      \"name\": \"income_tax\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Income tax deduction\"\n    },\n    {\n      \"name\": \"resident_tax\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Resident tax deduction\"\n    },\n    {\n      \"name\": \"social_insurance\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Social insurance deduction\"\n    },\n    {\n      \"name\": \"net_pay\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Net transfer amount\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "kyuyo-meisai.pdf",
              "fileUrl": "https://example.com/documents/kyuyo-meisai-sample.pdf"
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
      "id": "extract-kyuyo-meisai-data-extract",
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
Extract kyuyo meisai data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_name (TEXT): Employee name
- employee_number (TEXT): Employee number
- employer_name (TEXT): Employer name
- pay_period (DATE): Salary period or payment date
- payments (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- deductions (ARRAY): Each with description (TEXT), amount (CURRENCY_AMOUNT)
- gross_pay (CURRENCY_AMOUNT): Gross payment total
- income_tax (CURRENCY_AMOUNT): Income tax deduction
- resident_tax (CURRENCY_AMOUNT): Resident tax deduction
- social_insurance (CURRENCY_AMOUNT): Social insurance deduction
- net_pay (CURRENCY_AMOUNT): Net transfer amount
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
    "employee_number": {
      "value": "Employee Number",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE NUMBER"
      ]
    },
    "employer_name": {
      "value": "Northwind GmbH",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "pay_period": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "payments": {
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
        "PAYMENTS"
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
    "income_tax": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "resident_tax": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "social_insurance": {
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
