---
name: extract-w-9-data
description: Extract structured fields from w-9 documents.
---

# Extract W-9 Data

Tax and finance teams use this recipe to extract W-9 fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "w-9.pdf",
      "url": "https://example.com/documents/w-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "legal_name",
        "type": "TEXT",
        "description": "Name as shown on the income tax return"
      },
      {
        "name": "business_name",
        "type": "TEXT",
        "description": "Business name or disregarded entity name if different"
      },
      {
        "name": "federal_tax_classification",
        "type": "TEXT",
        "description": "Selected federal tax classification"
      },
      {
        "name": "exempt_payee_code",
        "type": "TEXT",
        "description": "Exempt payee code if provided"
      },
      {
        "name": "fatca_exemption_code",
        "type": "TEXT",
        "description": "FATCA reporting exemption code if provided"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Taxpayer street address, city, state, and ZIP code"
      },
      {
        "name": "requester_name_address",
        "type": "TEXT",
        "description": "Requester name and address if shown"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "SSN or employer identification number"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether the certification signature is present"
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
      "name": "w-9.pdf",
      "url": "https://example.com/documents/w-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "legal_name",
        "type": "TEXT",
        "description": "Name as shown on the income tax return"
      },
      {
        "name": "business_name",
        "type": "TEXT",
        "description": "Business name or disregarded entity name if different"
      },
      {
        "name": "federal_tax_classification",
        "type": "TEXT",
        "description": "Selected federal tax classification"
      },
      {
        "name": "exempt_payee_code",
        "type": "TEXT",
        "description": "Exempt payee code if provided"
      },
      {
        "name": "fatca_exemption_code",
        "type": "TEXT",
        "description": "FATCA reporting exemption code if provided"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Taxpayer street address, city, state, and ZIP code"
      },
      {
        "name": "requester_name_address",
        "type": "TEXT",
        "description": "Requester name and address if shown"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "SSN or employer identification number"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether the certification signature is present"
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
      "name": "w-9.pdf",
      "url": "https://example.com/documents/w-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "legal_name",
        "type": "TEXT",
        "description": "Name as shown on the income tax return"
      },
      {
        "name": "business_name",
        "type": "TEXT",
        "description": "Business name or disregarded entity name if different"
      },
      {
        "name": "federal_tax_classification",
        "type": "TEXT",
        "description": "Selected federal tax classification"
      },
      {
        "name": "exempt_payee_code",
        "type": "TEXT",
        "description": "Exempt payee code if provided"
      },
      {
        "name": "fatca_exemption_code",
        "type": "TEXT",
        "description": "FATCA reporting exemption code if provided"
      },
      {
        "name": "address",
        "type": "ADDRESS",
        "description": "Taxpayer street address, city, state, and ZIP code"
      },
      {
        "name": "requester_name_address",
        "type": "TEXT",
        "description": "Requester name and address if shown"
      },
      {
        "name": "taxpayer_identification_number",
        "type": "TEXT",
        "description": "SSN or employer identification number"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether the certification signature is present"
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
				Name: "w-9.pdf",
				Url: "https://example.com/documents/w-9-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "legal_name",
					Type: "TEXT",
					Description: "Name as shown on the income tax return",
				},
				il.TextFieldConfig{
					Name: "business_name",
					Type: "TEXT",
					Description: "Business name or disregarded entity name if different",
				},
				il.TextFieldConfig{
					Name: "federal_tax_classification",
					Type: "TEXT",
					Description: "Selected federal tax classification",
				},
				il.TextFieldConfig{
					Name: "exempt_payee_code",
					Type: "TEXT",
					Description: "Exempt payee code if provided",
				},
				il.TextFieldConfig{
					Name: "fatca_exemption_code",
					Type: "TEXT",
					Description: "FATCA reporting exemption code if provided",
				},
				il.AddressFieldConfig{
					Name: "address",
					Type: "ADDRESS",
					Description: "Taxpayer street address, city, state, and ZIP code",
				},
				il.TextFieldConfig{
					Name: "requester_name_address",
					Type: "TEXT",
					Description: "Requester name and address if shown",
				},
				il.TextFieldConfig{
					Name: "taxpayer_identification_number",
					Type: "TEXT",
					Description: "SSN or employer identification number",
				},
				il.BooleanFieldConfig{
					Name: "is_certification_signed",
					Type: "BOOLEAN",
					Description: "Whether the certification signature is present",
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
  "name": "Extract W-9 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract W-9 Data\n\nTax and finance teams use this recipe to extract W-9 fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-w-9-data-overview",
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
      "id": "extract-w-9-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"legal_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Name as shown on the income tax return\"\n    },\n    {\n      \"name\": \"business_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Business name or disregarded entity name if different\"\n    },\n    {\n      \"name\": \"federal_tax_classification\",\n      \"type\": \"TEXT\",\n      \"description\": \"Selected federal tax classification\"\n    },\n    {\n      \"name\": \"exempt_payee_code\",\n      \"type\": \"TEXT\",\n      \"description\": \"Exempt payee code if provided\"\n    },\n    {\n      \"name\": \"fatca_exemption_code\",\n      \"type\": \"TEXT\",\n      \"description\": \"FATCA reporting exemption code if provided\"\n    },\n    {\n      \"name\": \"address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Taxpayer street address, city, state, and ZIP code\"\n    },\n    {\n      \"name\": \"requester_name_address\",\n      \"type\": \"TEXT\",\n      \"description\": \"Requester name and address if shown\"\n    },\n    {\n      \"name\": \"taxpayer_identification_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"SSN or employer identification number\"\n    },\n    {\n      \"name\": \"is_certification_signed\",\n      \"type\": \"BOOLEAN\",\n      \"description\": \"Whether the certification signature is present\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "w-9.pdf",
              "fileUrl": "https://example.com/documents/w-9-sample.pdf"
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
      "id": "extract-w-9-data-extract",
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
Extract w-9 data from the file at [file URL]. Use the extract_document tool with these fields:

- legal_name (TEXT): Name as shown on the income tax return
- business_name (TEXT): Business name or disregarded entity name if different
- federal_tax_classification (TEXT): Selected federal tax classification
- exempt_payee_code (TEXT): Exempt payee code if provided
- fatca_exemption_code (TEXT): FATCA reporting exemption code if provided
- address (ADDRESS): Taxpayer street address, city, state, and ZIP code
- requester_name_address (TEXT): Requester name and address if shown
- taxpayer_identification_number (TEXT): SSN or employer identification number
- is_certification_signed (BOOLEAN): Whether the certification signature is present
```

### Response


```json
{
  "success": true,
  "data": {
    "legal_name": {
      "value": "Maria Keller Consulting LLC",
      "confidence": 0.97,
      "citations": [
        "LEGAL NAME"
      ]
    },
    "business_name": {
      "value": "Business Name",
      "confidence": 0.97,
      "citations": [
        "BUSINESS NAME"
      ]
    },
    "federal_tax_classification": {
      "value": "Federal Tax Classification",
      "confidence": 0.97,
      "citations": [
        "FEDERAL TAX CLASSIFICATION"
      ]
    },
    "exempt_payee_code": {
      "value": "Exempt Payee Code",
      "confidence": 0.97,
      "citations": [
        "EXEMPT PAYEE CODE"
      ]
    },
    "fatca_exemption_code": {
      "value": "Fatca Exemption Code",
      "confidence": 0.97,
      "citations": [
        "FATCA EXEMPTION CODE"
      ]
    },
    "address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "ADDRESS"
      ]
    },
    "requester_name_address": {
      "value": "Requester Name Address",
      "confidence": 0.97,
      "citations": [
        "REQUESTER NAME ADDRESS"
      ]
    },
    "taxpayer_identification_number": {
      "value": "12-3456789",
      "confidence": 0.97,
      "citations": [
        "TAXPAYER IDENTIFICATION NUMBER"
      ]
    },
    "is_certification_signed": {
      "value": true,
      "confidence": 0.97,
      "citations": [
        "IS CERTIFICATION SIGNED"
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
