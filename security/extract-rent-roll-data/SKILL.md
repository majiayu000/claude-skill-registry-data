---
name: extract-rent-roll-data
description: Extract property, unit, tenant, lease dates, rents, deposits, and occupancy fields from rent rolls.
---

# Extract Rent Roll Data

Real estate teams use this recipe to extract rent roll fields into structured portfolio data for underwriting, asset management, and lender reporting.

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
      "name": "rent-roll.pdf",
      "url": "https://example.com/documents/rent-roll-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_name",
        "type": "TEXT",
        "description": "Property name"
      },
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "as_of_date",
        "type": "DATE",
        "description": "Rent roll as-of date"
      },
      {
        "name": "units",
        "type": "ARRAY",
        "description": "Unit-level rent roll rows",
        "fields": [
          {
            "name": "unit_number",
            "type": "TEXT",
            "description": "Unit number"
          },
          {
            "name": "tenant_name",
            "type": "TEXT",
            "description": "Tenant name"
          },
          {
            "name": "unit_type",
            "type": "TEXT",
            "description": "Unit type or floor plan"
          },
          {
            "name": "square_feet",
            "type": "DECIMAL",
            "description": "Unit square feet"
          },
          {
            "name": "lease_start_date",
            "type": "DATE",
            "description": "Lease start date"
          },
          {
            "name": "lease_end_date",
            "type": "DATE",
            "description": "Lease end date"
          },
          {
            "name": "market_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Market rent"
          },
          {
            "name": "current_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Current contract rent"
          },
          {
            "name": "security_deposit",
            "type": "CURRENCY_AMOUNT",
            "description": "Security deposit"
          },
          {
            "name": "occupancy_status",
            "type": "TEXT",
            "description": "Occupied, vacant, notice, or model status"
          }
        ]
      },
      {
        "name": "total_monthly_rent",
        "type": "CURRENCY_AMOUNT",
        "description": "Total monthly rent"
      },
      {
        "name": "occupancy_rate_percent",
        "type": "DECIMAL",
        "description": "Occupancy rate percentage"
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
      "name": "rent-roll.pdf",
      "url": "https://example.com/documents/rent-roll-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_name",
        "type": "TEXT",
        "description": "Property name"
      },
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "as_of_date",
        "type": "DATE",
        "description": "Rent roll as-of date"
      },
      {
        "name": "units",
        "type": "ARRAY",
        "description": "Unit-level rent roll rows",
        "fields": [
          {
            "name": "unit_number",
            "type": "TEXT",
            "description": "Unit number"
          },
          {
            "name": "tenant_name",
            "type": "TEXT",
            "description": "Tenant name"
          },
          {
            "name": "unit_type",
            "type": "TEXT",
            "description": "Unit type or floor plan"
          },
          {
            "name": "square_feet",
            "type": "DECIMAL",
            "description": "Unit square feet"
          },
          {
            "name": "lease_start_date",
            "type": "DATE",
            "description": "Lease start date"
          },
          {
            "name": "lease_end_date",
            "type": "DATE",
            "description": "Lease end date"
          },
          {
            "name": "market_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Market rent"
          },
          {
            "name": "current_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Current contract rent"
          },
          {
            "name": "security_deposit",
            "type": "CURRENCY_AMOUNT",
            "description": "Security deposit"
          },
          {
            "name": "occupancy_status",
            "type": "TEXT",
            "description": "Occupied, vacant, notice, or model status"
          }
        ]
      },
      {
        "name": "total_monthly_rent",
        "type": "CURRENCY_AMOUNT",
        "description": "Total monthly rent"
      },
      {
        "name": "occupancy_rate_percent",
        "type": "DECIMAL",
        "description": "Occupancy rate percentage"
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
      "name": "rent-roll.pdf",
      "url": "https://example.com/documents/rent-roll-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_name",
        "type": "TEXT",
        "description": "Property name"
      },
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "as_of_date",
        "type": "DATE",
        "description": "Rent roll as-of date"
      },
      {
        "name": "units",
        "type": "ARRAY",
        "description": "Unit-level rent roll rows",
        "fields": [
          {
            "name": "unit_number",
            "type": "TEXT",
            "description": "Unit number"
          },
          {
            "name": "tenant_name",
            "type": "TEXT",
            "description": "Tenant name"
          },
          {
            "name": "unit_type",
            "type": "TEXT",
            "description": "Unit type or floor plan"
          },
          {
            "name": "square_feet",
            "type": "DECIMAL",
            "description": "Unit square feet"
          },
          {
            "name": "lease_start_date",
            "type": "DATE",
            "description": "Lease start date"
          },
          {
            "name": "lease_end_date",
            "type": "DATE",
            "description": "Lease end date"
          },
          {
            "name": "market_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Market rent"
          },
          {
            "name": "current_rent",
            "type": "CURRENCY_AMOUNT",
            "description": "Current contract rent"
          },
          {
            "name": "security_deposit",
            "type": "CURRENCY_AMOUNT",
            "description": "Security deposit"
          },
          {
            "name": "occupancy_status",
            "type": "TEXT",
            "description": "Occupied, vacant, notice, or model status"
          }
        ]
      },
      {
        "name": "total_monthly_rent",
        "type": "CURRENCY_AMOUNT",
        "description": "Total monthly rent"
      },
      {
        "name": "occupancy_rate_percent",
        "type": "DECIMAL",
        "description": "Occupancy rate percentage"
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
				Name: "rent-roll.pdf",
				Url: "https://example.com/documents/rent-roll-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "property_name",
					Type: "TEXT",
					Description: "Property name",
				},
				il.AddressFieldConfig{
					Name: "property_address",
					Type: "ADDRESS",
					Description: "Property address",
				},
				il.DateFieldConfig{
					Name: "as_of_date",
					Type: "DATE",
					Description: "Rent roll as-of date",
				},
				il.ArrayFieldConfig{
					Name: "units",
					Type: "ARRAY",
					Description: "Unit-level rent roll rows",
					Fields: []any{
						il.TextFieldConfig{
							Name: "unit_number",
							Type: "TEXT",
							Description: "Unit number",
						},
						il.TextFieldConfig{
							Name: "tenant_name",
							Type: "TEXT",
							Description: "Tenant name",
						},
						il.TextFieldConfig{
							Name: "unit_type",
							Type: "TEXT",
							Description: "Unit type or floor plan",
						},
						il.DecimalFieldConfig{
							Name: "square_feet",
							Type: "DECIMAL",
							Description: "Unit square feet",
						},
						il.DateFieldConfig{
							Name: "lease_start_date",
							Type: "DATE",
							Description: "Lease start date",
						},
						il.DateFieldConfig{
							Name: "lease_end_date",
							Type: "DATE",
							Description: "Lease end date",
						},
						il.CurrencyAmountFieldConfig{
							Name: "market_rent",
							Type: "CURRENCY_AMOUNT",
							Description: "Market rent",
						},
						il.CurrencyAmountFieldConfig{
							Name: "current_rent",
							Type: "CURRENCY_AMOUNT",
							Description: "Current contract rent",
						},
						il.CurrencyAmountFieldConfig{
							Name: "security_deposit",
							Type: "CURRENCY_AMOUNT",
							Description: "Security deposit",
						},
						il.TextFieldConfig{
							Name: "occupancy_status",
							Type: "TEXT",
							Description: "Occupied, vacant, notice, or model status",
						},
					},
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_monthly_rent",
					Type: "CURRENCY_AMOUNT",
					Description: "Total monthly rent",
				},
				il.DecimalFieldConfig{
					Name: "occupancy_rate_percent",
					Type: "DECIMAL",
					Description: "Occupancy rate percentage",
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
  "name": "Extract Rent Roll Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Rent Roll Data\n\nReal estate teams use this recipe to extract rent roll fields into structured portfolio data for underwriting, asset management, and lender reporting.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-rent-roll-data-overview",
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
      "id": "extract-rent-roll-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"property_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Property name\"\n    },\n    {\n      \"name\": \"property_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Property address\"\n    },\n    {\n      \"name\": \"as_of_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Rent roll as-of date\"\n    },\n    {\n      \"name\": \"units\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Unit-level rent roll rows\",\n      \"fields\": [\n        {\n          \"name\": \"unit_number\",\n          \"type\": \"TEXT\",\n          \"description\": \"Unit number\"\n        },\n        {\n          \"name\": \"tenant_name\",\n          \"type\": \"TEXT\",\n          \"description\": \"Tenant name\"\n        },\n        {\n          \"name\": \"unit_type\",\n          \"type\": \"TEXT\",\n          \"description\": \"Unit type or floor plan\"\n        },\n        {\n          \"name\": \"square_feet\",\n          \"type\": \"DECIMAL\",\n          \"description\": \"Unit square feet\"\n        },\n        {\n          \"name\": \"lease_start_date\",\n          \"type\": \"DATE\",\n          \"description\": \"Lease start date\"\n        },\n        {\n          \"name\": \"lease_end_date\",\n          \"type\": \"DATE\",\n          \"description\": \"Lease end date\"\n        },\n        {\n          \"name\": \"market_rent\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Market rent\"\n        },\n        {\n          \"name\": \"current_rent\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Current contract rent\"\n        },\n        {\n          \"name\": \"security_deposit\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Security deposit\"\n        },\n        {\n          \"name\": \"occupancy_status\",\n          \"type\": \"TEXT\",\n          \"description\": \"Occupied, vacant, notice, or model status\"\n        }\n      ]\n    },\n    {\n      \"name\": \"total_monthly_rent\",\n      \"type\": \"CURRENCY_AMOUNT\",\n      \"description\": \"Total monthly rent\"\n    },\n    {\n      \"name\": \"occupancy_rate_percent\",\n      \"type\": \"DECIMAL\",\n      \"description\": \"Occupancy rate percentage\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "rent-roll.pdf",
              "fileUrl": "https://example.com/documents/rent-roll-sample.pdf"
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
      "id": "extract-rent-roll-data-extract",
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
Extract rent roll data from the file at [file URL]. Use the extract_document tool with these fields:

- property_name (TEXT): Property name
- property_address (ADDRESS): Property address
- as_of_date (DATE): Rent roll as-of date
- units (ARRAY): Each with unit_number (TEXT), tenant_name (TEXT), unit_type (TEXT), square_feet (DECIMAL), lease_start_date (DATE), lease_end_date (DATE), market_rent (CURRENCY_AMOUNT), current_rent (CURRENCY_AMOUNT), security_deposit (CURRENCY_AMOUNT), occupancy_status (TEXT)
- total_monthly_rent (CURRENCY_AMOUNT): Total monthly rent
- occupancy_rate_percent (DECIMAL): Occupancy rate percentage
```

### Response


```json
{
  "success": true,
  "data": {
    "property_name": {
      "value": "Property Name",
      "confidence": 0.97,
      "citations": [
        "PROPERTY NAME"
      ]
    },
    "property_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "PROPERTY ADDRESS"
      ]
    },
    "as_of_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "units": {
      "value": [
        {
          "unit_number": {
            "value": "Unit Number",
            "confidence": 0.96,
            "citations": [
              "UNIT NUMBER"
            ]
          },
          "tenant_name": {
            "value": "Tenant Name",
            "confidence": 0.96,
            "citations": [
              "TENANT NAME"
            ]
          },
          "unit_type": {
            "value": "Unit Type",
            "confidence": 0.96,
            "citations": [
              "UNIT TYPE"
            ]
          },
          "square_feet": {
            "value": 12.5,
            "confidence": 0.96,
            "citations": [
              "SQUARE FEET"
            ]
          },
          "lease_start_date": {
            "value": "2026-04-15",
            "confidence": 0.96,
            "citations": [
              "15 Apr 2026"
            ]
          },
          "lease_end_date": {
            "value": "2026-04-15",
            "confidence": 0.96,
            "citations": [
              "15 Apr 2026"
            ]
          },
          "market_rent": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "1,234.56"
            ]
          },
          "current_rent": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "1,234.56"
            ]
          },
          "security_deposit": {
            "value": {
              "amount": "1234.56",
              "currency": "EUR"
            },
            "confidence": 0.96,
            "citations": [
              "1,234.56"
            ]
          },
          "occupancy_status": {
            "value": "Occupancy Status",
            "confidence": 0.96,
            "citations": [
              "OCCUPANCY STATUS"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "UNITS"
      ]
    },
    "total_monthly_rent": {
      "value": {
        "amount": "1234.56",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": [
        "1,234.56"
      ]
    },
    "occupancy_rate_percent": {
      "value": 12.5,
      "confidence": 0.97,
      "citations": [
        "OCCUPANCY RATE PERCENT"
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
