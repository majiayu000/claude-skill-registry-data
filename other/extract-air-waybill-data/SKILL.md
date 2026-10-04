---
name: extract-air-waybill-data
description: Extract structured fields from air waybill documents.
---

# Extract Air Waybill Data

Logistics teams use this recipe to turn Air Waybill PDFs into structured shipment records. Extract parties, route details, goods, weights, and values for customs, tracking, or transportation workflows.

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
      "name": "air-waybill.pdf",
      "url": "https://example.com/documents/air-waybill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Primary shipment or transport document number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper, exporter, or consignor name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee, importer, or recipient name"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier or logistics provider"
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
        "name": "shipment_date",
        "type": "DATE",
        "description": "Shipment, receipt, or departure date"
      },
      {
        "name": "goods",
        "type": "ARRAY",
        "description": "Goods, packages, or shipment lines",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Goods or package description"
          },
          {
            "name": "marks_and_numbers",
            "type": "TEXT",
            "description": "Container, package, seal, or tracking identifiers"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity or package count"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          }
        ]
      },
      {
        "name": "declared_value",
        "type": "CURRENCY_AMOUNT",
        "description": "Declared customs or freight value"
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
      "name": "air-waybill.pdf",
      "url": "https://example.com/documents/air-waybill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Primary shipment or transport document number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper, exporter, or consignor name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee, importer, or recipient name"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier or logistics provider"
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
        "name": "shipment_date",
        "type": "DATE",
        "description": "Shipment, receipt, or departure date"
      },
      {
        "name": "goods",
        "type": "ARRAY",
        "description": "Goods, packages, or shipment lines",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Goods or package description"
          },
          {
            "name": "marks_and_numbers",
            "type": "TEXT",
            "description": "Container, package, seal, or tracking identifiers"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity or package count"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          }
        ]
      },
      {
        "name": "declared_value",
        "type": "CURRENCY_AMOUNT",
        "description": "Declared customs or freight value"
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
      "name": "air-waybill.pdf",
      "url": "https://example.com/documents/air-waybill-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Primary shipment or transport document number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper, exporter, or consignor name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee, importer, or recipient name"
      },
      {
        "name": "carrier_name",
        "type": "TEXT",
        "description": "Carrier or logistics provider"
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
        "name": "shipment_date",
        "type": "DATE",
        "description": "Shipment, receipt, or departure date"
      },
      {
        "name": "goods",
        "type": "ARRAY",
        "description": "Goods, packages, or shipment lines",
        "fields": [
          {
            "name": "description",
            "type": "TEXT",
            "description": "Goods or package description"
          },
          {
            "name": "marks_and_numbers",
            "type": "TEXT",
            "description": "Container, package, seal, or tracking identifiers"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity or package count"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          }
        ]
      },
      {
        "name": "declared_value",
        "type": "CURRENCY_AMOUNT",
        "description": "Declared customs or freight value"
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
				Name: "air-waybill.pdf",
				Url: "https://example.com/documents/air-waybill-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "document_number",
					Type: "TEXT",
					Description: "Primary shipment or transport document number",
				},
				il.TextFieldConfig{
					Name: "shipper_name",
					Type: "TEXT",
					Description: "Shipper, exporter, or consignor name",
				},
				il.TextFieldConfig{
					Name: "consignee_name",
					Type: "TEXT",
					Description: "Consignee, importer, or recipient name",
				},
				il.TextFieldConfig{
					Name: "carrier_name",
					Type: "TEXT",
					Description: "Carrier or logistics provider",
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
				il.DateFieldConfig{
					Name: "shipment_date",
					Type: "DATE",
					Description: "Shipment, receipt, or departure date",
				},
				il.ArrayFieldConfig{
					Name: "goods",
					Type: "ARRAY",
					Description: "Goods, packages, or shipment lines",
					Fields: []any{
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Goods or package description",
						},
						il.TextFieldConfig{
							Name: "marks_and_numbers",
							Type: "TEXT",
							Description: "Container, package, seal, or tracking identifiers",
						},
						il.DecimalFieldConfig{
							Name: "quantity",
							Type: "DECIMAL",
							Description: "Quantity or package count",
						},
						il.DecimalFieldConfig{
							Name: "gross_weight_kg",
							Type: "DECIMAL",
							Description: "Gross weight in kilograms",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "declared_value",
					Type: "CURRENCY_AMOUNT",
					Description: "Declared customs or freight value",
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
  "name": "Extract Air Waybill Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Air Waybill Data\n\nLogistics teams use this recipe to turn Air Waybill PDFs into structured shipment records. Extract parties, route details, goods, weights, and values for customs, tracking, or transportation workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-air-waybill-data-overview",
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
      "id": "extract-air-waybill-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"document_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Primary shipment or transport document number\"\n    },\n    {\n      \"name\": \"shipper_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Shipper, exporter, or consignor name\"\n    },\n    {\n      \"name\": \"consignee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Consignee, importer, or recipient name\"\n    },\n    {\n      \"name\": \"carrier_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Carrier or logistics provider\"\n    },\n    {\n      \"name\": \"origin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Origin location\"\n    },\n    {\n      \"name\": \"destination\",\n      \"type\": \"TEXT\",\n      \"description\": \"Destination location\"\n    },\n    {\n      \"name\": \"shipment_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Shipment, receipt, or departure date\"\n    },\n    {\n      \"name\": \"goods\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Goods, packages, or shipment lines\",\n      \"fields\": [\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Goods or package description\"\n        },\n        {\n          \"name\": \"marks_and_numbers\",\n          \"type\": \"TEXT\",\n          \"description\": \"Container, package, seal, or tracking identifiers\"\n        },\n        {\n          \"name\": \"quantity\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Quantity or package count\"\n        },\n        {\n          \"name\": \"gross_weight_kg\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Gross weight in kilograms\"\n        }\n      ]\n    },\n    {\n      \"name\": \"declared_value\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Declared customs or freight value\"\n    },\n    {\n      \"name\": \"currency\",\n      \"type\": \"CURRENCY_CODE\",\n      \"description\": \"Currency code\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "air-waybill.pdf",
              "fileUrl": "https://example.com/documents/air-waybill-sample.pdf"
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
      "id": "extract-air-waybill-data-extract",
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
Extract air waybill data from the file at [file URL]. Use the extract_document tool with these fields:

- document_number (TEXT): Primary shipment or transport document number
- shipper_name (TEXT): Shipper, exporter, or consignor name
- consignee_name (TEXT): Consignee, importer, or recipient name
- carrier_name (TEXT): Carrier or logistics provider
- origin (TEXT): Origin location
- destination (TEXT): Destination location
- shipment_date (DATE): Shipment, receipt, or departure date
- goods (ARRAY): Each with description (TEXT), marks_and_numbers (TEXT), quantity (DECIMAL), gross_weight_kg (DECIMAL)
- declared_value (CURRENCY_AMOUNT): Declared customs or freight value
- currency (CURRENCY_CODE): Currency code
```

### Response


```json
{
  "success": true,
  "data": {
    "document_number": {
      "value": "BL-2026-00418",
      "confidence": 0.97,
      "citations": [
        "DOCUMENT NUMBER"
      ]
    },
    "shipper_name": {
      "value": "Shipper Name",
      "confidence": 0.97,
      "citations": [
        "SHIPPER NAME"
      ]
    },
    "consignee_name": {
      "value": "Consignee Name",
      "confidence": 0.97,
      "citations": [
        "CONSIGNEE NAME"
      ]
    },
    "carrier_name": {
      "value": "Carrier Name",
      "confidence": 0.97,
      "citations": [
        "CARRIER NAME"
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
    "shipment_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "goods": {
      "value": [
        {
          "description": {
            "value": "Description",
            "confidence": 0.96,
            "citations": [
              "DESCRIPTION"
            ]
          },
          "marks_and_numbers": {
            "value": "Marks And Numbers",
            "confidence": 0.96,
            "citations": [
              "MARKS AND NUMBERS"
            ]
          },
          "quantity": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "QUANTITY"
            ]
          },
          "gross_weight_kg": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "GROSS WEIGHT KG"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "GOODS"
      ]
    },
    "declared_value": {
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
