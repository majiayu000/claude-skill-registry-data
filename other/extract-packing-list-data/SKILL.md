---
name: extract-packing-list-data
description: Extract shipper, consignee, order references, carton lines, weights, and package totals from packing lists.
---

# Extract Packing List Data

Logistics teams use this recipe to extract packing list fields into structured shipment records for warehouse receiving, customs checks, and inventory reconciliation.

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
      "name": "packing-list.pdf",
      "url": "https://example.com/documents/packing-list-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "packing_list_number",
        "type": "TEXT",
        "description": "Packing list number"
      },
      {
        "name": "invoice_or_order_number",
        "type": "TEXT",
        "description": "Related invoice, order, or PO number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee name"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Ship date"
      },
      {
        "name": "packages",
        "type": "ARRAY",
        "description": "Package or carton lines",
        "fields": [
          {
            "name": "package_number",
            "type": "TEXT",
            "description": "Carton, pallet, or package number"
          },
          {
            "name": "sku",
            "type": "TEXT",
            "description": "SKU or item code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity packed"
          },
          {
            "name": "net_weight_kg",
            "type": "DECIMAL",
            "description": "Net weight in kilograms"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          },
          {
            "name": "dimensions",
            "type": "TEXT",
            "description": "Package dimensions if shown"
          }
        ]
      },
      {
        "name": "total_packages",
        "type": "DECIMAL",
        "description": "Total number of packages"
      },
      {
        "name": "total_gross_weight_kg",
        "type": "DECIMAL",
        "description": "Total gross weight in kilograms"
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
      "name": "packing-list.pdf",
      "url": "https://example.com/documents/packing-list-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "packing_list_number",
        "type": "TEXT",
        "description": "Packing list number"
      },
      {
        "name": "invoice_or_order_number",
        "type": "TEXT",
        "description": "Related invoice, order, or PO number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee name"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Ship date"
      },
      {
        "name": "packages",
        "type": "ARRAY",
        "description": "Package or carton lines",
        "fields": [
          {
            "name": "package_number",
            "type": "TEXT",
            "description": "Carton, pallet, or package number"
          },
          {
            "name": "sku",
            "type": "TEXT",
            "description": "SKU or item code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity packed"
          },
          {
            "name": "net_weight_kg",
            "type": "DECIMAL",
            "description": "Net weight in kilograms"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          },
          {
            "name": "dimensions",
            "type": "TEXT",
            "description": "Package dimensions if shown"
          }
        ]
      },
      {
        "name": "total_packages",
        "type": "DECIMAL",
        "description": "Total number of packages"
      },
      {
        "name": "total_gross_weight_kg",
        "type": "DECIMAL",
        "description": "Total gross weight in kilograms"
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
      "name": "packing-list.pdf",
      "url": "https://example.com/documents/packing-list-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "packing_list_number",
        "type": "TEXT",
        "description": "Packing list number"
      },
      {
        "name": "invoice_or_order_number",
        "type": "TEXT",
        "description": "Related invoice, order, or PO number"
      },
      {
        "name": "shipper_name",
        "type": "TEXT",
        "description": "Shipper name"
      },
      {
        "name": "consignee_name",
        "type": "TEXT",
        "description": "Consignee name"
      },
      {
        "name": "ship_date",
        "type": "DATE",
        "description": "Ship date"
      },
      {
        "name": "packages",
        "type": "ARRAY",
        "description": "Package or carton lines",
        "fields": [
          {
            "name": "package_number",
            "type": "TEXT",
            "description": "Carton, pallet, or package number"
          },
          {
            "name": "sku",
            "type": "TEXT",
            "description": "SKU or item code"
          },
          {
            "name": "description",
            "type": "TEXT",
            "description": "Item description"
          },
          {
            "name": "quantity",
            "type": "DECIMAL",
            "description": "Quantity packed"
          },
          {
            "name": "net_weight_kg",
            "type": "DECIMAL",
            "description": "Net weight in kilograms"
          },
          {
            "name": "gross_weight_kg",
            "type": "DECIMAL",
            "description": "Gross weight in kilograms"
          },
          {
            "name": "dimensions",
            "type": "TEXT",
            "description": "Package dimensions if shown"
          }
        ]
      },
      {
        "name": "total_packages",
        "type": "DECIMAL",
        "description": "Total number of packages"
      },
      {
        "name": "total_gross_weight_kg",
        "type": "DECIMAL",
        "description": "Total gross weight in kilograms"
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
				Name: "packing-list.pdf",
				Url: "https://example.com/documents/packing-list-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "packing_list_number",
					Type: "TEXT",
					Description: "Packing list number",
				},
				il.TextFieldConfig{
					Name: "invoice_or_order_number",
					Type: "TEXT",
					Description: "Related invoice, order, or PO number",
				},
				il.TextFieldConfig{
					Name: "shipper_name",
					Type: "TEXT",
					Description: "Shipper name",
				},
				il.TextFieldConfig{
					Name: "consignee_name",
					Type: "TEXT",
					Description: "Consignee name",
				},
				il.DateFieldConfig{
					Name: "ship_date",
					Type: "DATE",
					Description: "Ship date",
				},
				il.ArrayFieldConfig{
					Name: "packages",
					Type: "ARRAY",
					Description: "Package or carton lines",
					Fields: []any{
						il.TextFieldConfig{
							Name: "package_number",
							Type: "TEXT",
							Description: "Carton, pallet, or package number",
						},
						il.TextFieldConfig{
							Name: "sku",
							Type: "TEXT",
							Description: "SKU or item code",
						},
						il.TextFieldConfig{
							Name: "description",
							Type: "TEXT",
							Description: "Item description",
						},
						il.DecimalFieldConfig{
							Name: "quantity",
							Type: "DECIMAL",
							Description: "Quantity packed",
						},
						il.DecimalFieldConfig{
							Name: "net_weight_kg",
							Type: "DECIMAL",
							Description: "Net weight in kilograms",
						},
						il.DecimalFieldConfig{
							Name: "gross_weight_kg",
							Type: "DECIMAL",
							Description: "Gross weight in kilograms",
						},
						il.TextFieldConfig{
							Name: "dimensions",
							Type: "TEXT",
							Description: "Package dimensions if shown",
						},
					},
				},
				il.DecimalFieldConfig{
					Name: "total_packages",
					Type: "DECIMAL",
					Description: "Total number of packages",
				},
				il.DecimalFieldConfig{
					Name: "total_gross_weight_kg",
					Type: "DECIMAL",
					Description: "Total gross weight in kilograms",
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
  "name": "Extract Packing List Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Packing List Data\n\nLogistics teams use this recipe to extract packing list fields into structured shipment records for warehouse receiving, customs checks, and inventory reconciliation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-packing-list-data-overview",
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
      "id": "extract-packing-list-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"packing_list_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Packing list number\"\n    },\n    {\n      \"name\": \"invoice_or_order_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Related invoice, order, or PO number\"\n    },\n    {\n      \"name\": \"shipper_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Shipper name\"\n    },\n    {\n      \"name\": \"consignee_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Consignee name\"\n    },\n    {\n      \"name\": \"ship_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Ship date\"\n    },\n    {\n      \"name\": \"packages\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Package or carton lines\",\n      \"fields\": [\n        {\n          \"name\": \"package_number\",\n          \"type\": \"TEXT\",\n          \"description\": \"Carton, pallet, or package number\"\n        },\n        {\n          \"name\": \"sku\",\n          \"type\": \"TEXT\",\n          \"description\": \"SKU or item code\"\n        },\n        {\n          \"name\": \"description\",\n          \"type\": \"TEXT\",\n          \"description\": \"Item description\"\n        },\n        {\n          \"name\": \"quantity\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Quantity packed\"\n        },\n        {\n          \"name\": \"net_weight_kg\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Net weight in kilograms\"\n        },\n        {\n          \"name\": \"gross_weight_kg\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Gross weight in kilograms\"\n        },\n        {\n          \"name\": \"dimensions\",\n          \"type\": \"TEXT\",\n          \"description\": \"Package dimensions if shown\"\n        }\n      ]\n    },\n    {\n      \"name\": \"total_packages\",\n      \"type\": \"DECIMAL\",\n      \"description\": \"Total number of packages\"\n    },\n    {\n      \"name\": \"total_gross_weight_kg\",\n      \"type\": \"DECIMAL\",\n      \"description\": \"Total gross weight in kilograms\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "packing-list.pdf",
              "fileUrl": "https://example.com/documents/packing-list-sample.pdf"
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
      "id": "extract-packing-list-data-extract",
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
Extract packing list data from the file at [file URL]. Use the extract_document tool with these fields:

- packing_list_number (TEXT): Packing list number
- invoice_or_order_number (TEXT): Related invoice, order, or PO number
- shipper_name (TEXT): Shipper name
- consignee_name (TEXT): Consignee name
- ship_date (DATE): Ship date
- packages (ARRAY): Each with package_number (TEXT), sku (TEXT), description (TEXT), quantity (DECIMAL), net_weight_kg (DECIMAL), gross_weight_kg (DECIMAL), dimensions (TEXT)
- total_packages (DECIMAL): Total number of packages
- total_gross_weight_kg (DECIMAL): Total gross weight in kilograms
```

### Response


```json
{
  "success": true,
  "data": {
    "packing_list_number": {
      "value": "Packing List Number",
      "confidence": 0.97,
      "citations": [
        "PACKING LIST NUMBER"
      ]
    },
    "invoice_or_order_number": {
      "value": "Invoice Or Order Number",
      "confidence": 0.97,
      "citations": [
        "INVOICE OR ORDER NUMBER"
      ]
    },
    "shipper_name": {
      "value": "Nordic Components GmbH",
      "confidence": 0.97,
      "citations": [
        "SHIPPER NAME"
      ]
    },
    "consignee_name": {
      "value": "Acme Distribution Inc.",
      "confidence": 0.97,
      "citations": [
        "CONSIGNEE NAME"
      ]
    },
    "ship_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "packages": {
      "value": [
        {
          "package_number": {
            "value": "Package Number",
            "confidence": 0.96,
            "citations": [
              "PACKAGE NUMBER"
            ]
          },
          "sku": {
            "value": "Sku",
            "confidence": 0.96,
            "citations": [
              "SKU"
            ]
          },
          "description": {
            "value": "Description",
            "confidence": 0.96,
            "citations": [
              "DESCRIPTION"
            ]
          },
          "quantity": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "QUANTITY"
            ]
          },
          "net_weight_kg": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "NET WEIGHT KG"
            ]
          },
          "gross_weight_kg": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "GROSS WEIGHT KG"
            ]
          },
          "dimensions": {
            "value": "Dimensions",
            "confidence": 0.96,
            "citations": [
              "DIMENSIONS"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "PACKAGES"
      ]
    },
    "total_packages": {
      "value": 12.5,
      "confidence": 0.97,
      "citations": [
        "TOTAL PACKAGES"
      ]
    },
    "total_gross_weight_kg": {
      "value": 12.5,
      "confidence": 0.97,
      "citations": [
        "TOTAL GROSS WEIGHT KG"
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
