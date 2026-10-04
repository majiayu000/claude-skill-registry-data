---
name: extract-freight-bill-data
description: Extract carrier invoice, shipment references, rates, accessorials, taxes, and total charges from freight bills.
---

# Extract Freight Bill Data

Logistics finance teams use this recipe to extract freight bill fields into structured billing records for audit, accruals, and carrier payment workflows.

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
      "name": "freight-bill.pdf",
      "url": "https://example.com/documents/freight-bill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "freight_bill_number",
        "type": "TEXT",
        "description": "Freight bill or carrier invoice number"
      },
      {
        "name": "invoice_date",
        "type": "DATE",
        "description": "Invoice date"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier name"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Bill-to or payer name"
      },
      {
        "name": "shipment_reference",
        "type": "TEXT",
        "description": "Shipment, PRO, BOL, or tracking reference"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Shipment date"
      },
      {
        "name": "origin",
        "type": "TEXT",
        "description": "Origin location"
      },
      {
        "name": "destination",
        "type": "TEXT",
        "description": "Destination location"
      },
      {
        "name": "charges",
        "type": "ARRAY",
        "description": "Freight and accessorial charges",
        "fields": [
          {
            "name": "charge_code",
            "type": "TEXT",
            "description": "Charge or accessorial code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Charge description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Charge amount"
          }
        ]
      },
      {
        "name": "fuel_surcharge",
        "type": "CURRENCY_AMOUNT",
        "description": "Fuel surcharge"
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total freight bill amount"
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
      "name": "freight-bill.pdf",
      "url": "https://example.com/documents/freight-bill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "freight_bill_number",
        "type": "TEXT",
        "description": "Freight bill or carrier invoice number"
      },
      {
        "name": "invoice_date",
        "type": "DATE",
        "description": "Invoice date"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier name"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Bill-to or payer name"
      },
      {
        "name": "shipment_reference",
        "type": "TEXT",
        "description": "Shipment, PRO, BOL, or tracking reference"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Shipment date"
      },
      {
        "name": "origin",
        "type": "TEXT",
        "description": "Origin location"
      },
      {
        "name": "destination",
        "type": "TEXT",
        "description": "Destination location"
      },
      {
        "name": "charges",
        "type": "ARRAY",
        "description": "Freight and accessorial charges",
        "fields": [
          {
            "name": "charge_code",
            "type": "TEXT",
            "description": "Charge or accessorial code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Charge description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Charge amount"
          }
        ]
      },
      {
        "name": "fuel_surcharge",
        "type": "CURRENCY_AMOUNT",
        "description": "Fuel surcharge"
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total freight bill amount"
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
      "name": "freight-bill.pdf",
      "url": "https://example.com/documents/freight-bill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "freight_bill_number",
        "type": "TEXT",
        "description": "Freight bill or carrier invoice number"
      },
      {
        "name": "invoice_date",
        "type": "DATE",
        "description": "Invoice date"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier name"
      },
      {
        "name": "payer_name",
        "type": "TEXT",
        "description": "Bill-to or payer name"
      },
      {
        "name": "shipment_reference",
        "type": "TEXT",
        "description": "Shipment, PRO, BOL, or tracking reference"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Shipment date"
      },
      {
        "name": "origin",
        "type": "TEXT",
        "description": "Origin location"
      },
      {
        "name": "destination",
        "type": "TEXT",
        "description": "Destination location"
      },
      {
        "name": "charges",
        "type": "ARRAY",
        "description": "Freight and accessorial charges",
        "fields": [
          {
            "name": "charge_code",
            "type": "TEXT",
            "description": "Charge or accessorial code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Charge description"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Charge amount"
          }
        ]
      },
      {
        "name": "fuel_surcharge",
        "type": "CURRENCY_AMOUNT",
        "description": "Fuel surcharge"
      },
      {
        "name": "tax_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Tax amount"
      },
      {
        "name": "total_amount",
        "type": "CURRENCY_AMOUNT",
        "description": "Total freight bill amount"
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
				Name: "freight-bill.pdf",
				Url: "https://example.com/documents/freight-bill-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "freight_bill_number",
					Type: "TEXT",
					Description: "Freight bill or carrier invoice number",
				},
				il.DateFieldConfig{
					Name: "invoice_date",
					Type: "DATE",
					Description: "Invoice date",
				},
				il.TextFieldConfig{
					Name: "carrier_name",
					Type: "TEXT",
					Description: "Carrier name",
				},
				il.TextFieldConfig{
					Name: "payer_name",
					Type: "TEXT",
					Description: "Bill-to or payer name",
				},
				il.TextFieldConfig{
					Name: "shipment_reference",
					Type: "TEXT",
					Description: "Shipment, PRO, BOL, or tracking reference",
				},
				il.DateFieldConfig{
					Name: "ship_date",
					Type: "DATE",
					Description: "Shipment date",
				},
				il.TextFieldConfig{
					Name: "origin",
					Type: "TEXT",
					Description: "Origin location",
				},
				il.TextFieldConfig{
					Name: "destination",
					Type: "TEXT",
					Description: "Destination location",
				},
				il.ArrayFieldConfig{
					Name: "charges",
					Type: "ARRAY",
					Description: "Freight and accessorial charges",
					Fields: []any{
						il.TextFieldConfig{
							Name: "charge_code",
							Type: "TEXT",
							Description: "Charge or accessorial code",
						},
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Charge description",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Charge amount",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "fuel_surcharge",
					Type: "CURRENCY_AMOUNT",
					Description: "Fuel surcharge",
				},
				il.CurrencyAmountFieldConfig{
					Name: "tax_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Tax amount",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total freight bill amount",
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
  "name": "Extract Freight Bill Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Freight Bill Data\n\nLogistics finance teams use this recipe to extract freight bill fields into structured billing records for audit, accruals, and carrier payment workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-freight-bill-data-overview",
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
      "id": "extract-freight-bill-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"freight_bill_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Freight bill or carrier invoice number\"\n    },\n    {\n      \"name\": \"invoice_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Invoice date\"\n    },\n    {\n      \"name\": \"carrier_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Carrier name\"\n    },\n    {\n      \"name\": \"payer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Bill-to or payer name\"\n    },\n    {\n      \"name\": \"shipment_reference\",\n      \"type\": \"TEXT\",\n      \"description\": \"Shipment, PRO, BOL, or tracking reference\"\n    },\n    {\n      \"name\": \"ship_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Shipment date\"\n    },\n    {\n      \"name\": \"origin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Origin location\"\n    },\n    {\n      \"name\": \"destination\",\n      \"type\": \"TEXT\",\n      \"description\": \"Destination location\"\n    },\n    {\n      \"name\": \"charges\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Freight and accessorial charges\",\n      \"fields\": [\n        {\n          \"name\": \"charge_code\",\n          \"type\": \"TEXT\",\n          \"description\": \"Charge or accessorial code\"\n        },\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Charge description\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Charge amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"fuel_surcharge\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Fuel surcharge\"\n    },\n    {\n      \"name\": \"tax_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Tax amount\"\n    },\n    {\n      \"name\": \"total_amount\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total freight bill amount\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "freight-bill.pdf",
              "fileUrl": "https://example.com/documents/freight-bill-sample.pdf"
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
      "id": "extract-freight-bill-data-extract",
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
Extract freight bill data from the file at [file URL]. Use the extract_document tool with these fields:

- freight_bill_number (TEXT): Freight bill or carrier invoice number
- invoice_date (DATE): Invoice date
- carrier_name (TEXT): Carrier name
- payer_name (TEXT): Bill-to or payer name
- shipment_reference (TEXT): Shipment, PRO, BOL, or tracking reference
- ship_date (DATE): Shipment date
- origin (TEXT): Origin location
- destination (TEXT): Destination location
- charges (ARRAY): Each with charge_code (TEXT), description (TEXT), amount (CURRENCY_AMOUNT)
- fuel_surcharge (CURRENCY_AMOUNT): Fuel surcharge
- tax_amount (CURRENCY_AMOUNT): Tax amount
- total_amount (CURRENCY_AMOUNT): Total freight bill amount
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "freight_bill_number": {
      "value": "Freight Bill Number",
      "confidence": 0.97,
      "citations": [
        "FREIGHT BILL NUMBER"
      ]
    },
    "invoice_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "carrier_name": {
      "value": "DHL Freight",
      "confidence": 0.97,
      "citations": [
        "CARRIER NAME"
      ]
    },
    "payer_name": {
      "value": "Payer Name",
      "confidence": 0.97,
      "citations": [
        "PAYER NAME"
      ]
    },
    "shipment_reference": {
      "value": "Shipment Reference",
      "confidence": 0.97,
      "citations": [
        "SHIPMENT REFERENCE"
      ]
    },
    "ship_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "origin": {
      "value": "Origin",
      "confidence": 0.97,
      "citations": [
        "ORIGIN"
      ]
    },
    "destination": {
      "value": "Destination",
      "confidence": 0.97,
      "citations": [
        "DESTINATION"
      ]
    },
    "charges": {
      "value": [
        {
          "charge_code": {
            "value": "Charge Code",
            "confidence": 0.96,
            "citations": [
              "CHARGE CODE"
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
        "CHARGES"
      ]
    },
    "fuel_surcharge": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "tax_amount": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "total_amount": {
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
