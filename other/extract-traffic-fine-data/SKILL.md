---
name: extract-traffic-fine-data
description: Extract violation details, fine amounts, vehicle information, and payment deadlines from traffic fine notices.
---

# Extract Traffic Fine Data

Fleet management agencies and logistics companies use this recipe to process traffic fine notices at scale — extracting violation details, amounts, and deadlines for centralized tracking and timely payment.

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
        "name": "traffic-fine-2026-0892.pdf",
        "url": "https://example.com/fines/traffic-fine-2026-0892.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "ticket_number",
          "type": "TEXT",
          "description": "Traffic ticket or fine reference number"
        },
        {
          "name": "issue_date",
          "type": "DATE",
          "description": "Date the fine was issued"
        },
        {
          "name": "violation_type",
          "type": "TEXT",
          "description": "Type of violation, e.g. speeding, parking, red light"
        },
        {
          "name": "violation_description",
          "type": "TEXT",
          "description": "Detailed description of the violation"
        },
        {
          "name": "vehicle_plate",
          "type": "TEXT",
          "description": "License plate number of the vehicle"
        },
        {
          "name": "vehicle_make_model",
          "type": "TEXT",
          "description": "Vehicle make and model"
        },
        {
          "name": "location",
          "type": "TEXT",
          "description": "Location where the violation occurred"
        },
        {
          "name": "fine_amount",
          "type": "CURRENCY_AMOUNT",
          "description": "Total fine amount"
        },
        {
          "name": "payment_due_date",
          "type": "DATE",
          "description": "Deadline for payment"
        },
        {
          "name": "penalty_points",
          "type": "INTEGER",
          "description": "Penalty or demerit points"
        },
        {
          "name": "issuing_authority",
          "type": "TEXT",
          "description": "Authority or agency that issued the fine"
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.extractDocument({
  files: [
    {
      type: "url",
      name: "traffic-fine-2026-0892.pdf",
      url: "https://example.com/fines/traffic-fine-2026-0892.pdf",
    },
  ],
  schema: {
    fields: [
      { name: "ticket_number", type: "TEXT", description: "Traffic ticket or fine reference number" },
      { name: "issue_date", type: "DATE", description: "Date the fine was issued" },
      { name: "violation_type", type: "TEXT", description: "Type of violation, e.g. speeding, parking, red light" },
      { name: "violation_description", type: "TEXT", description: "Detailed description of the violation" },
      { name: "vehicle_plate", type: "TEXT", description: "License plate number of the vehicle" },
      { name: "vehicle_make_model", type: "TEXT", description: "Vehicle make and model" },
      { name: "location", type: "TEXT", description: "Location where the violation occurred" },
      { name: "fine_amount", type: "CURRENCY_AMOUNT", description: "Total fine amount" },
      { name: "payment_due_date", type: "DATE", description: "Deadline for payment" },
      { name: "penalty_points", type: "INTEGER", description: "Penalty or demerit points" },
      { name: "issuing_authority", type: "TEXT", description: "Authority or agency that issued the fine" },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.extract_document(
    files=[
        {
            "type": "url",
            "name": "traffic-fine-2026-0892.pdf",
            "url": "https://example.com/fines/traffic-fine-2026-0892.pdf",
        }
    ],
    schema={
        "fields": [
            {"name": "ticket_number", "type": "TEXT", "description": "Traffic ticket or fine reference number"},
            {"name": "issue_date", "type": "DATE", "description": "Date the fine was issued"},
            {"name": "violation_type", "type": "TEXT", "description": "Type of violation, e.g. speeding, parking, red light"},
            {"name": "violation_description", "type": "TEXT", "description": "Detailed description of the violation"},
            {"name": "vehicle_plate", "type": "TEXT", "description": "License plate number of the vehicle"},
            {"name": "vehicle_make_model", "type": "TEXT", "description": "Vehicle make and model"},
            {"name": "location", "type": "TEXT", "description": "Location where the violation occurred"},
            {"name": "fine_amount", "type": "CURRENCY_AMOUNT", "description": "Total fine amount"},
            {"name": "payment_due_date", "type": "DATE", "description": "Deadline for payment"},
            {"name": "penalty_points", "type": "INTEGER", "description": "Penalty or demerit points"},
            {"name": "issuing_authority", "type": "TEXT", "description": "Authority or agency that issued the fine"},
        ]
    },
)
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
				Name: "traffic-fine-2026-0892.pdf",
				Url: "https://example.com/fines/traffic-fine-2026-0892.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "ticket_number",
					Type: "TEXT",
					Description: "Traffic ticket or fine reference number",
				},
				il.DateFieldConfig{
					Name: "issue_date",
					Type: "DATE",
					Description: "Date the fine was issued",
				},
				il.TextFieldConfig{
					Name: "violation_type",
					Type: "TEXT",
					Description: "Type of violation, e.g. speeding, parking, red light",
				},
				il.TextFieldConfig{
					Name: "violation_description",
					Type: "TEXT",
					Description: "Detailed description of the violation",
				},
				il.TextFieldConfig{
					Name: "vehicle_plate",
					Type: "TEXT",
					Description: "License plate number of the vehicle",
				},
				il.TextFieldConfig{
					Name: "vehicle_make_model",
					Type: "TEXT",
					Description: "Vehicle make and model",
				},
				il.TextFieldConfig{
					Name: "location",
					Type: "TEXT",
					Description: "Location where the violation occurred",
				},
				il.CurrencyAmountFieldConfig{
					Name: "fine_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total fine amount",
				},
				il.DateFieldConfig{
					Name: "payment_due_date",
					Type: "DATE",
					Description: "Deadline for payment",
				},
				il.IntegerFieldConfig{
					Name: "penalty_points",
					Type: "INTEGER",
					Description: "Penalty or demerit points",
				},
				il.TextFieldConfig{
					Name: "issuing_authority",
					Type: "TEXT",
					Description: "Authority or agency that issued the fine",
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
  "name": "Extract traffic fine data in Iteration Layer",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Traffic Fine Data\n\nFleet management agencies and logistics companies use this recipe to process traffic fine notices at scale — extracting violation details, amounts, and deadlines for centralized tracking and timely payment.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "f6a7b8c9-d0e1-2345-fabc-345678901201",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract Fine Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
        "height": 160,
        "width": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        475,
        100
      ],
      "id": "f6a7b8c9-d0e1-2345-fabc-345678901202",
      "name": "Step 1 Note"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ],
      "id": "f6a7b8c9-d0e1-2345-fabc-345678901203",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"ticket_number\",\"type\":\"TEXT\",\"description\":\"Traffic ticket or fine reference number\"},{\"name\":\"issue_date\",\"type\":\"DATE\",\"description\":\"Date the fine was issued\"},{\"name\":\"violation_type\",\"type\":\"TEXT\",\"description\":\"Type of violation\"},{\"name\":\"violation_description\",\"type\":\"TEXT\",\"description\":\"Detailed description of the violation\"},{\"name\":\"vehicle_plate\",\"type\":\"TEXT\",\"description\":\"License plate number\"},{\"name\":\"vehicle_make_model\",\"type\":\"TEXT\",\"description\":\"Vehicle make and model\"},{\"name\":\"location\",\"type\":\"TEXT\",\"description\":\"Location where the violation occurred\"},{\"name\":\"fine_amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Total fine amount\"},{\"name\":\"payment_due_date\",\"type\":\"DATE\",\"description\":\"Deadline for payment\"},{\"name\":\"penalty_points\",\"type\":\"INTEGER\",\"description\":\"Penalty or demerit points\"},{\"name\":\"issuing_authority\",\"type\":\"TEXT\",\"description\":\"Authority that issued the fine\"}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "traffic-fine-2026-0892.pdf",
              "fileUrl": "https://example.com/fines/traffic-fine-2026-0892.pdf"
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
      "id": "f6a7b8c9-d0e1-2345-fabc-345678901204",
      "name": "Extract Fine Data",
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
            "node": "Extract Fine Data",
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
Extract traffic fine data from the file at [file URL]. Use the extract_document tool with these fields:

- ticket_number (TEXT): Traffic ticket or fine reference number
- issue_date (DATE): Date the fine was issued
- violation_type (TEXT): Type of violation, e.g. speeding, parking, red light
- violation_description (TEXT): Detailed description of the violation
- vehicle_plate (TEXT): License plate number of the vehicle
- vehicle_make_model (TEXT): Vehicle make and model
- location (TEXT): Location where the violation occurred
- fine_amount (CURRENCY_AMOUNT): Total fine amount
- payment_due_date (DATE): Deadline for payment
- penalty_points (INTEGER): Penalty or demerit points
- issuing_authority (TEXT): Authority or agency that issued the fine
```

### Response


```json
{
  "success": true,
  "data": {
    "ticket_number": {
      "value": "VIO-2026-0892",
      "confidence": 0.99,
      "citations": [
        "Ticket No: VIO-2026-0892"
      ]
    },
    "issue_date": {
      "value": "2026-03-05",
      "confidence": 0.98,
      "citations": [
        "Issued: March 5, 2026"
      ]
    },
    "violation_type": {
      "value": "Speeding",
      "confidence": 0.97,
      "citations": [
        "Violation: Speeding — exceeding posted limit"
      ]
    },
    "violation_description": {
      "value": "Vehicle recorded at 78 km/h in a 50 km/h zone by automated speed camera",
      "confidence": 0.95,
      "citations": [
        "Recorded speed: 78 km/h in 50 km/h zone (automated camera)"
      ]
    },
    "vehicle_plate": {
      "value": "MI-4421-RZ",
      "confidence": 0.99,
      "citations": [
        "Plate: MI-4421-RZ"
      ]
    },
    "vehicle_make_model": {
      "value": "Fiat Ducato 2024",
      "confidence": 0.94,
      "citations": [
        "Vehicle: Fiat Ducato, 2024"
      ]
    },
    "location": {
      "value": "Via Emilia, km 23.4, Parma",
      "confidence": 0.96,
      "citations": [
        "Location: Via Emilia, km 23.4, Parma"
      ]
    },
    "fine_amount": {
      "value": {
        "amount": "175.00",
        "currency": "EUR"
      },
      "confidence": 0.98,
      "citations": [
        "Fine: EUR 175.00"
      ]
    },
    "payment_due_date": {
      "value": "2026-04-04",
      "confidence": 0.97,
      "citations": [
        "Payment due by: April 4, 2026"
      ]
    },
    "penalty_points": {
      "value": 3,
      "confidence": 0.96,
      "citations": [
        "Points: 3"
      ]
    },
    "issuing_authority": {
      "value": "Polizia Municipale di Parma",
      "confidence": 0.98,
      "citations": [
        "Issued by: Polizia Municipale di Parma"
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
