---
name: extract-title-search-data
description: Extract property, owner, legal description, liens, mortgages, easements, and tax status from title search reports.
---

# Extract Title Search Data

Title companies and lenders use this recipe to extract title search report fields into structured review records for closing, underwriting, and exception handling.

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
      "name": "title-search.pdf",
      "url": "https://example.com/documents/title-search-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "legal_description",
        "type": "TEXT",
        "description": "Legal description of the property"
      },
      {
        "name": "current_owner",
        "type": "TEXT",
        "description": "Current owner or vested owner"
      },
      {
        "name": "parcel_or_tax_id",
        "type": "TEXT",
        "description": "Parcel, folio, or tax ID"
      },
      {
        "name": "search_effective_date",
        "type": "DATE",
        "description": "Title search effective date"
      },
      {
        "name": "liens_and_encumbrances",
        "type": "ARRAY",
        "description": "Liens, mortgages, judgments, easements, and other encumbrances",
        "fields": [
          {
            "name": "type",
            "type": "TEXT",
            "description": "Encumbrance type"
          },
          {
            "name": "recording_reference",
            "type": "TEXT",
            "description": "Book, page, instrument, or recording reference"
          },
          {
            "name": "recording_date",
            "type": "DATE",
            "description": "Recording date"
          },
          {
            "name": "party",
            "type": "TEXT",
            "description": "Beneficiary, claimant, lender, or affected party"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Amount if shown"
          }
        ]
      },
      {
        "name": "tax_status",
        "type": "TEXT",
        "description": "Property tax status"
      },
      {
        "name": "exceptions_summary",
        "type": "TEXT",
        "description": "Summary of exceptions or requirements"
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
      "name": "title-search.pdf",
      "url": "https://example.com/documents/title-search-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "legal_description",
        "type": "TEXT",
        "description": "Legal description of the property"
      },
      {
        "name": "current_owner",
        "type": "TEXT",
        "description": "Current owner or vested owner"
      },
      {
        "name": "parcel_or_tax_id",
        "type": "TEXT",
        "description": "Parcel, folio, or tax ID"
      },
      {
        "name": "search_effective_date",
        "type": "DATE",
        "description": "Title search effective date"
      },
      {
        "name": "liens_and_encumbrances",
        "type": "ARRAY",
        "description": "Liens, mortgages, judgments, easements, and other encumbrances",
        "fields": [
          {
            "name": "type",
            "type": "TEXT",
            "description": "Encumbrance type"
          },
          {
            "name": "recording_reference",
            "type": "TEXT",
            "description": "Book, page, instrument, or recording reference"
          },
          {
            "name": "recording_date",
            "type": "DATE",
            "description": "Recording date"
          },
          {
            "name": "party",
            "type": "TEXT",
            "description": "Beneficiary, claimant, lender, or affected party"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Amount if shown"
          }
        ]
      },
      {
        "name": "tax_status",
        "type": "TEXT",
        "description": "Property tax status"
      },
      {
        "name": "exceptions_summary",
        "type": "TEXT",
        "description": "Summary of exceptions or requirements"
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
      "name": "title-search.pdf",
      "url": "https://example.com/documents/title-search-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "property_address",
        "type": "ADDRESS",
        "description": "Property address"
      },
      {
        "name": "legal_description",
        "type": "TEXT",
        "description": "Legal description of the property"
      },
      {
        "name": "current_owner",
        "type": "TEXT",
        "description": "Current owner or vested owner"
      },
      {
        "name": "parcel_or_tax_id",
        "type": "TEXT",
        "description": "Parcel, folio, or tax ID"
      },
      {
        "name": "search_effective_date",
        "type": "DATE",
        "description": "Title search effective date"
      },
      {
        "name": "liens_and_encumbrances",
        "type": "ARRAY",
        "description": "Liens, mortgages, judgments, easements, and other encumbrances",
        "fields": [
          {
            "name": "type",
            "type": "TEXT",
            "description": "Encumbrance type"
          },
          {
            "name": "recording_reference",
            "type": "TEXT",
            "description": "Book, page, instrument, or recording reference"
          },
          {
            "name": "recording_date",
            "type": "DATE",
            "description": "Recording date"
          },
          {
            "name": "party",
            "type": "TEXT",
            "description": "Beneficiary, claimant, lender, or affected party"
          },
          {
            "name": "amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Amount if shown"
          }
        ]
      },
      {
        "name": "tax_status",
        "type": "TEXT",
        "description": "Property tax status"
      },
      {
        "name": "exceptions_summary",
        "type": "TEXT",
        "description": "Summary of exceptions or requirements"
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
				Name: "title-search.pdf",
				Url: "https://example.com/documents/title-search-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.AddressFieldConfig{
					Name: "property_address",
					Type: "ADDRESS",
					Description: "Property address",
				},
				il.TextFieldConfig{
					Name: "legal_description",
					Type: "TEXT",
					Description: "Legal description of the property",
				},
				il.TextFieldConfig{
					Name: "current_owner",
					Type: "TEXT",
					Description: "Current owner or vested owner",
				},
				il.TextFieldConfig{
					Name: "parcel_or_tax_id",
					Type: "TEXT",
					Description: "Parcel, folio, or tax ID",
				},
				il.DateFieldConfig{
					Name: "search_effective_date",
					Type: "DATE",
					Description: "Title search effective date",
				},
				il.ArrayFieldConfig{
					Name: "liens_and_encumbrances",
					Type: "ARRAY",
					Description: "Liens, mortgages, judgments, easements, and other encumbrances",
					Fields: []any{
						il.TextFieldConfig{
							Name: "type",
							Type: "TEXT",
							Description: "Encumbrance type",
						},
						il.TextFieldConfig{
							Name: "recording_reference",
							Type: "TEXT",
							Description: "Book, page, instrument, or recording reference",
						},
						il.DateFieldConfig{
							Name: "recording_date",
							Type: "DATE",
							Description: "Recording date",
						},
						il.TextFieldConfig{
							Name: "party",
							Type: "TEXT",
							Description: "Beneficiary, claimant, lender, or affected party",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Amount if shown",
						},
					},
				},
				il.TextFieldConfig{
					Name: "tax_status",
					Type: "TEXT",
					Description: "Property tax status",
				},
				il.TextFieldConfig{
					Name: "exceptions_summary",
					Type: "TEXT",
					Description: "Summary of exceptions or requirements",
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
  "name": "Extract Title Search Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Title Search Data\n\nTitle companies and lenders use this recipe to extract title search report fields into structured review records for closing, underwriting, and exception handling.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-title-search-data-overview",
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
      "id": "extract-title-search-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"property_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Property address\"\n    },\n    {\n      \"name\": \"legal_description\",\n      \"type\": \"TEXT\",\n      \"description\": \"Legal description of the property\"\n    },\n    {\n      \"name\": \"current_owner\",\n      \"type\": \"TEXT\",\n      \"description\": \"Current owner or vested owner\"\n    },\n    {\n      \"name\": \"parcel_or_tax_id\",\n      \"type\": \"TEXT\",\n      \"description\": \"Parcel, folio, or tax ID\"\n    },\n    {\n      \"name\": \"search_effective_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Title search effective date\"\n    },\n    {\n      \"name\": \"liens_and_encumbrances\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Liens, mortgages, judgments, easements, and other encumbrances\",\n      \"fields\": [\n        {\n          \"name\": \"type\",\n          \"type\": \"TEXT\",\n          \"description\": \"Encumbrance type\"\n        },\n        {\n          \"name\": \"recording_reference\",\n          \"type\": \"TEXT\",\n          \"description\": \"Book, page, instrument, or recording reference\"\n        },\n        {\n          \"name\": \"recording_date\",\n          \"type\": \"DATE\",\n          \"description\": \"Recording date\"\n        },\n        {\n          \"name\": \"party\",\n          \"type\": \"TEXT\",\n          \"description\": \"Beneficiary, claimant, lender, or affected party\"\n        },\n        {\n          \"name\": \"amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Amount if shown\"\n        }\n      ]\n    },\n    {\n      \"name\": \"tax_status\",\n      \"type\": \"TEXT\",\n      \"description\": \"Property tax status\"\n    },\n    {\n      \"name\": \"exceptions_summary\",\n      \"type\": \"TEXT\",\n      \"description\": \"Summary of exceptions or requirements\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "title-search.pdf",
              "fileUrl": "https://example.com/documents/title-search-sample.pdf"
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
      "id": "extract-title-search-data-extract",
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
Extract title search data from the file at [file URL]. Use the extract_document tool with these fields:

- property_address (ADDRESS): Property address
- legal_description (TEXT): Legal description of the property
- current_owner (TEXT): Current owner or vested owner
- parcel_or_tax_id (TEXT): Parcel, folio, or tax ID
- search_effective_date (DATE): Title search effective date
- liens_and_encumbrances (ARRAY): Each with type (TEXT), recording_reference (TEXT), recording_date (DATE), party (TEXT), amount (CURRENCY_AMOUNT)
- tax_status (TEXT): Property tax status
- exceptions_summary (TEXT): Summary of exceptions or requirements
```

### Response


```json
{
  "success": true,
  "data": {
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
    "legal_description": {
      "value": "Legal Description",
      "confidence": 0.97,
      "citations": [
        "LEGAL DESCRIPTION"
      ]
    },
    "current_owner": {
      "value": "Current Owner",
      "confidence": 0.97,
      "citations": [
        "CURRENT OWNER"
      ]
    },
    "parcel_or_tax_id": {
      "value": "Parcel Or Tax Id",
      "confidence": 0.97,
      "citations": [
        "PARCEL OR TAX ID"
      ]
    },
    "search_effective_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "liens_and_encumbrances": {
      "value": [
        {
          "type": {
            "value": "Type",
            "confidence": 0.96,
            "citations": [
              "TYPE"
            ]
          },
          "recording_reference": {
            "value": "Recording Reference",
            "confidence": 0.96,
            "citations": [
              "RECORDING REFERENCE"
            ]
          },
          "recording_date": {
            "value": "2026-04-15",
            "confidence": 0.96,
            "citations": [
              "15 Apr 2026"
            ]
          },
          "party": {
            "value": "Party",
            "confidence": 0.96,
            "citations": [
              "PARTY"
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
        "LIENS AND ENCUMBRANCES"
      ]
    },
    "tax_status": {
      "value": "Tax Status",
      "confidence": 0.97,
      "citations": [
        "TAX STATUS"
      ]
    },
    "exceptions_summary": {
      "value": "Exceptions Summary",
      "confidence": 0.97,
      "citations": [
        "EXCEPTIONS SUMMARY"
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
