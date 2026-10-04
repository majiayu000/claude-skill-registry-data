---
name: extract-vat100-data
description: Extract structured fields from vat100 documents.
---

# Extract VAT100 Data

Tax and finance teams use this recipe to extract VAT100 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "vat100.pdf",
      "url": "https://example.com/documents/vat100-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "taxpayer_name",
        "type": "TEXT",
        "description": "Taxpayer, filer, or recipient name"
      },
      {
        "name": "taxpayer_identifier",
        "type": "TEXT",
        "description": "Taxpayer identifier"
      },
      {
        "name": "issuer_or_authority",
        "type": "TEXT",
        "description": "Employer, payer, or tax authority"
      },
      {
        "name": "tax_period",
        "type": "TEXT",
        "description": "Tax year or filing period"
      },
      {
        "name": "tax_lines",
        "type": "ARRAY",
        "description": "Reported tax lines",
        "fields": [
          {
            "name": "code",
            "type": "TEXT",
            "description": "Box, line, or tax code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Line description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Reported amount"
          }
        ]
      },
      {
        "name": "taxable_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable amount or tax base"
      },
      {
        "name": "tax_due_or_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax due, assessed, or withheld"
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
      "name": "vat100.pdf",
      "url": "https://example.com/documents/vat100-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "taxpayer_name",
        "type": "TEXT",
        "description": "Taxpayer, filer, or recipient name"
      },
      {
        "name": "taxpayer_identifier",
        "type": "TEXT",
        "description": "Taxpayer identifier"
      },
      {
        "name": "issuer_or_authority",
        "type": "TEXT",
        "description": "Employer, payer, or tax authority"
      },
      {
        "name": "tax_period",
        "type": "TEXT",
        "description": "Tax year or filing period"
      },
      {
        "name": "tax_lines",
        "type": "ARRAY",
        "description": "Reported tax lines",
        "fields": [
          {
            "name": "code",
            "type": "TEXT",
            "description": "Box, line, or tax code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Line description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Reported amount"
          }
        ]
      },
      {
        "name": "taxable_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable amount or tax base"
      },
      {
        "name": "tax_due_or_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax due, assessed, or withheld"
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
      "name": "vat100.pdf",
      "url": "https://example.com/documents/vat100-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "taxpayer_name",
        "type": "TEXT",
        "description": "Taxpayer, filer, or recipient name"
      },
      {
        "name": "taxpayer_identifier",
        "type": "TEXT",
        "description": "Taxpayer identifier"
      },
      {
        "name": "issuer_or_authority",
        "type": "TEXT",
        "description": "Employer, payer, or tax authority"
      },
      {
        "name": "tax_period",
        "type": "TEXT",
        "description": "Tax year or filing period"
      },
      {
        "name": "tax_lines",
        "type": "ARRAY",
        "description": "Reported tax lines",
        "fields": [
          {
            "name": "code",
            "type": "TEXT",
            "description": "Box, line, or tax code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Line description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Reported amount"
          }
        ]
      },
      {
        "name": "taxable_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Taxable amount or tax base"
      },
      {
        "name": "tax_due_or_withheld",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax due, assessed, or withheld"
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
				Name: "vat100.pdf",
				Url: "https://example.com/documents/vat100-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "taxpayer_name",
					Type: "TEXT",
					Description: "Taxpayer, filer, or recipient name",
				},
				il.TextFieldConfig{
					Name: "taxpayer_identifier",
					Type: "TEXT",
					Description: "Taxpayer identifier",
				},
				il.TextFieldConfig{
					Name: "issuer_or_authority",
					Type: "TEXT",
					Description: "Employer, payer, or tax authority",
				},
				il.TextFieldConfig{
					Name: "tax_period",
					Type: "TEXT",
					Description: "Tax year or filing period",
				},
				il.ArrayFieldConfig{
					Name: "tax_lines",
					Type: "ARRAY",
					Description: "Reported tax lines",
					Fields: []any{
						il.TextFieldConfig{
							Name: "code",
							Type: "TEXT",
							Description: "Box, line, or tax code",
						},
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Line description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Reported amount",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "taxable_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Taxable amount or tax base",
				},
				il.CurrencyAmountFieldConfig{
					Name: "tax_due_or_withheld",
					Type: "CURRENCY_AMOUNT",
					Description: "Tax due, assessed, or withheld",
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
  "name": "Extract VAT100 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract VAT100 Data\n\nTax and finance teams use this recipe to extract VAT100 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-vat100-data-overview",
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
      "id": "extract-vat100-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"taxpayer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Taxpayer, filer, or recipient name\"\n    },\n    {\n      \"name\": \"taxpayer_identifier\",\n      \"type\": \"TEXT\",\n      \"description\": \"Taxpayer identifier\"\n    },\n    {\n      \"name\": \"issuer_or_authority\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer, payer, or tax authority\"\n    },\n    {\n      \"name\": \"tax_period\",\n      \"type\": \"TEXT\",\n      \"description\": \"Tax year or filing period\"\n    },\n    {\n      \"name\": \"tax_lines\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Reported tax lines\",\n      \"fields\": [\n        {\n          \"name\": \"code\",\n          \"type\": \"TEXT\",\n          \"description\": \"Box, line, or tax code\"\n        },\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Line description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Reported amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"taxable_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Taxable amount or tax base\"\n    },\n    {\n      \"name\": \"tax_due_or_withheld\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Tax due, assessed, or withheld\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "vat100.pdf",
              "fileUrl": "https://example.com/documents/vat100-sample.pdf"
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
      "id": "extract-vat100-data-extract",
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
Extract vat100 data from the file at [file URL]. Use the extract_document tool with these fields:

- taxpayer_name (TEXT): Taxpayer, filer, or recipient name
- taxpayer_identifier (TEXT): Taxpayer identifier
- issuer_or_authority (TEXT): Employer, payer, or tax authority
- tax_period (TEXT): Tax year or filing period
- tax_lines (ARRAY): Each with code (TEXT), description (TEXT), amount (CURRENCY_AMOUNT)
- taxable_amount (CURRENCY_AMOUNT): Taxable amount or tax base
- tax_due_or_withheld (CURRENCY_AMOUNT): Tax due, assessed, or withheld
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "taxpayer_name": {
      "value": "Taxpayer Name",
      "confidence": 0.97,
      "citations": [
        "TAXPAYER NAME"
      ]
    },
    "taxpayer_identifier": {
      "value": "Taxpayer Identifier",
      "confidence": 0.97,
      "citations": [
        "TAXPAYER IDENTIFIER"
      ]
    },
    "issuer_or_authority": {
      "value": "Issuer Or Authority",
      "confidence": 0.97,
      "citations": [
        "ISSUER OR AUTHORITY"
      ]
    },
    "tax_period": {
      "value": "Tax Period",
      "confidence": 0.97,
      "citations": [
        "TAX PERIOD"
      ]
    },
    "tax_lines": {
      "value": [
        {
          "code": {
            "value": "Code",
            "confidence": 0.96,
            "citations": [
              "CODE"
            ]
          },
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
              "currency": "GBP"
            },
            "confidence": 0.96,
            "citations": [
              "GBP 1,234.56"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "TAX LINES"
      ]
    },
    "taxable_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "GBP"
      },
      "confidence": 0.97,
      "citations": [
        "GBP 1,234.56"
      ]
    },
    "tax_due_or_withheld": {
      "value": {
        "amount": "1234.56",
        "currency": "GBP"
      },
      "confidence": 0.97,
      "citations": [
        "GBP 1,234.56"
      ]
    },
    "currency": {
      "value": "GBP",
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
