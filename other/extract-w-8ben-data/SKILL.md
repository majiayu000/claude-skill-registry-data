---
name: extract-w-8ben-data
description: Extract structured fields from w-8ben documents.
---

# Extract W-8BEN Data

Tax and finance teams use this recipe to extract W-8BEN fields from official forms into structured JSON for review, routing, and downstream filing preparation.

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
      "name": "w-8ben.pdf",
      "url": "https://example.com/documents/w-8ben-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "beneficial_owner_name",
        "type": "TEXT",
        "description": "Beneficial owner name"
      },
      {
        "name": "country_of_citizenship",
        "type": "COUNTRY",
        "description": "Country of citizenship"
      },
      {
        "name": "permanent_residence_address",
        "type": "ADDRESS",
        "description": "Permanent residence address"
      },
      {
        "name": "mailing_address",
        "type": "ADDRESS",
        "description": "Mailing address if different"
      },
      {
        "name": "us_tin",
        "type": "TEXT",
        "description": "U.S. taxpayer identification number if provided"
      },
      {
        "name": "foreign_tin",
        "type": "TEXT",
        "description": "Foreign tax identifying number"
      },
      {
        "name": "reference_number",
        "type": "TEXT",
        "description": "Reference number if shown"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Date of birth"
      },
      {
        "name": "treaty_country",
        "type": "COUNTRY",
        "description": "Treaty country for Part II claim"
      },
      {
        "name": "treaty_article",
        "type": "TEXT",
        "description": "Treaty article and paragraph"
      },
      {
        "name": "withholding_rate",
        "type": "TEXT",
        "description": "Claimed withholding rate"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether certification is signed"
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
      "name": "w-8ben.pdf",
      "url": "https://example.com/documents/w-8ben-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "beneficial_owner_name",
        "type": "TEXT",
        "description": "Beneficial owner name"
      },
      {
        "name": "country_of_citizenship",
        "type": "COUNTRY",
        "description": "Country of citizenship"
      },
      {
        "name": "permanent_residence_address",
        "type": "ADDRESS",
        "description": "Permanent residence address"
      },
      {
        "name": "mailing_address",
        "type": "ADDRESS",
        "description": "Mailing address if different"
      },
      {
        "name": "us_tin",
        "type": "TEXT",
        "description": "U.S. taxpayer identification number if provided"
      },
      {
        "name": "foreign_tin",
        "type": "TEXT",
        "description": "Foreign tax identifying number"
      },
      {
        "name": "reference_number",
        "type": "TEXT",
        "description": "Reference number if shown"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Date of birth"
      },
      {
        "name": "treaty_country",
        "type": "COUNTRY",
        "description": "Treaty country for Part II claim"
      },
      {
        "name": "treaty_article",
        "type": "TEXT",
        "description": "Treaty article and paragraph"
      },
      {
        "name": "withholding_rate",
        "type": "TEXT",
        "description": "Claimed withholding rate"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether certification is signed"
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
      "name": "w-8ben.pdf",
      "url": "https://example.com/documents/w-8ben-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "beneficial_owner_name",
        "type": "TEXT",
        "description": "Beneficial owner name"
      },
      {
        "name": "country_of_citizenship",
        "type": "COUNTRY",
        "description": "Country of citizenship"
      },
      {
        "name": "permanent_residence_address",
        "type": "ADDRESS",
        "description": "Permanent residence address"
      },
      {
        "name": "mailing_address",
        "type": "ADDRESS",
        "description": "Mailing address if different"
      },
      {
        "name": "us_tin",
        "type": "TEXT",
        "description": "U.S. taxpayer identification number if provided"
      },
      {
        "name": "foreign_tin",
        "type": "TEXT",
        "description": "Foreign tax identifying number"
      },
      {
        "name": "reference_number",
        "type": "TEXT",
        "description": "Reference number if shown"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Date of birth"
      },
      {
        "name": "treaty_country",
        "type": "COUNTRY",
        "description": "Treaty country for Part II claim"
      },
      {
        "name": "treaty_article",
        "type": "TEXT",
        "description": "Treaty article and paragraph"
      },
      {
        "name": "withholding_rate",
        "type": "TEXT",
        "description": "Claimed withholding rate"
      },
      {
        "name": "is_certification_signed",
        "type": "BOOLEAN",
        "description": "Whether certification is signed"
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
				Name: "w-8ben.pdf",
				Url: "https://example.com/documents/w-8ben-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "beneficial_owner_name",
					Type: "TEXT",
					Description: "Beneficial owner name",
				},
				il.CountryFieldConfig{
					Name: "country_of_citizenship",
					Type: "COUNTRY",
					Description: "Country of citizenship",
				},
				il.AddressFieldConfig{
					Name: "permanent_residence_address",
					Type: "ADDRESS",
					Description: "Permanent residence address",
				},
				il.AddressFieldConfig{
					Name: "mailing_address",
					Type: "ADDRESS",
					Description: "Mailing address if different",
				},
				il.TextFieldConfig{
					Name: "us_tin",
					Type: "TEXT",
					Description: "U.S. taxpayer identification number if provided",
				},
				il.TextFieldConfig{
					Name: "foreign_tin",
					Type: "TEXT",
					Description: "Foreign tax identifying number",
				},
				il.TextFieldConfig{
					Name: "reference_number",
					Type: "TEXT",
					Description: "Reference number if shown",
				},
				il.DateFieldConfig{
					Name: "date_of_birth",
					Type: "DATE",
					Description: "Date of birth",
				},
				il.CountryFieldConfig{
					Name: "treaty_country",
					Type: "COUNTRY",
					Description: "Treaty country for Part II claim",
				},
				il.TextFieldConfig{
					Name: "treaty_article",
					Type: "TEXT",
					Description: "Treaty article and paragraph",
				},
				il.TextFieldConfig{
					Name: "withholding_rate",
					Type: "TEXT",
					Description: "Claimed withholding rate",
				},
				il.BooleanFieldConfig{
					Name: "is_certification_signed",
					Type: "BOOLEAN",
					Description: "Whether certification is signed",
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
  "name": "Extract W-8BEN Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract W-8BEN Data\n\nTax and finance teams use this recipe to extract W-8BEN fields from official forms into structured JSON for review, routing, and downstream filing preparation.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-w-8ben-data-overview",
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
      "id": "extract-w-8ben-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"beneficial_owner_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Beneficial owner name\"\n    },\n    {\n      \"name\": \"country_of_citizenship\",\n      \"type\": \"COUNTRY\",\n      \"description\": \"Country of citizenship\"\n    },\n    {\n      \"name\": \"permanent_residence_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Permanent residence address\"\n    },\n    {\n      \"name\": \"mailing_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Mailing address if different\"\n    },\n    {\n      \"name\": \"us_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"U.S. taxpayer identification number if provided\"\n    },\n    {\n      \"name\": \"foreign_tin\",\n      \"type\": \"TEXT\",\n      \"description\": \"Foreign tax identifying number\"\n    },\n    {\n      \"name\": \"reference_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Reference number if shown\"\n    },\n    {\n      \"name\": \"date_of_birth\",\n      \"type\": \"DATE\",\n      \"description\": \"Date of birth\"\n    },\n    {\n      \"name\": \"treaty_country\",\n      \"type\": \"COUNTRY\",\n      \"description\": \"Treaty country for Part II claim\"\n    },\n    {\n      \"name\": \"treaty_article\",\n      \"type\": \"TEXT\",\n      \"description\": \"Treaty article and paragraph\"\n    },\n    {\n      \"name\": \"withholding_rate\",\n      \"type\": \"TEXT\",\n      \"description\": \"Claimed withholding rate\"\n    },\n    {\n      \"name\": \"is_certification_signed\",\n      \"type\": \"BOOLEAN\",\n      \"description\": \"Whether certification is signed\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "w-8ben.pdf",
              "fileUrl": "https://example.com/documents/w-8ben-sample.pdf"
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
      "id": "extract-w-8ben-data-extract",
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
Extract w-8ben data from the file at [file URL]. Use the extract_document tool with these fields:

- beneficial_owner_name (TEXT): Beneficial owner name
- country_of_citizenship (COUNTRY): Country of citizenship
- permanent_residence_address (ADDRESS): Permanent residence address
- mailing_address (ADDRESS): Mailing address if different
- us_tin (TEXT): U.S. taxpayer identification number if provided
- foreign_tin (TEXT): Foreign tax identifying number
- reference_number (TEXT): Reference number if shown
- date_of_birth (DATE): Date of birth
- treaty_country (COUNTRY): Treaty country for Part II claim
- treaty_article (TEXT): Treaty article and paragraph
- withholding_rate (TEXT): Claimed withholding rate
- is_certification_signed (BOOLEAN): Whether certification is signed
```

### Response


```json
{
  "success": true,
  "data": {
    "beneficial_owner_name": {
      "value": "Beneficial Owner Name",
      "confidence": 0.97,
      "citations": [
        "BENEFICIAL OWNER NAME"
      ]
    },
    "country_of_citizenship": {
      "value": "DE",
      "confidence": 0.97,
      "citations": [
        "COUNTRY OF CITIZENSHIP"
      ]
    },
    "permanent_residence_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "PERMANENT RESIDENCE ADDRESS"
      ]
    },
    "mailing_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "MAILING ADDRESS"
      ]
    },
    "us_tin": {
      "value": "Us Tin",
      "confidence": 0.97,
      "citations": [
        "US TIN"
      ]
    },
    "foreign_tin": {
      "value": "Foreign Tin",
      "confidence": 0.97,
      "citations": [
        "FOREIGN TIN"
      ]
    },
    "reference_number": {
      "value": "Reference Number",
      "confidence": 0.97,
      "citations": [
        "REFERENCE NUMBER"
      ]
    },
    "date_of_birth": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "treaty_country": {
      "value": "DE",
      "confidence": 0.97,
      "citations": [
        "TREATY COUNTRY"
      ]
    },
    "treaty_article": {
      "value": "Treaty Article",
      "confidence": 0.97,
      "citations": [
        "TREATY ARTICLE"
      ]
    },
    "withholding_rate": {
      "value": "Withholding Rate",
      "confidence": 0.97,
      "citations": [
        "WITHHOLDING RATE"
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
