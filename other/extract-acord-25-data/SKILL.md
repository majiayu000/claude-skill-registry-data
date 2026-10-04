---
name: extract-acord-25-data
description: Extract structured fields from acord 25 documents.
---

# Extract ACORD 25 Data

Insurance teams use this recipe to extract ACORD 25 details without manually rekeying policy, claim, coverage, and loss information into claims systems.

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
      "name": "acord-25.pdf",
      "url": "https://example.com/documents/acord-25-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "producer_name",
        "type": "TEXT",
        "description": "Producer or broker name"
      },
      {
        "name": "insured_name",
        "type": "TEXT",
        "description": "Named insured"
      },
      {
        "name": "insurers_affording_coverage",
        "type": "TEXT",
        "description": "Insurers affording coverage"
      },
      {
        "name": "certificate_issue_date",
        "type": "DATE",
        "description": "Certificate issue date"
      },
      {
        "name": "coverages",
        "type": "ARRAY",
        "description": "Coverage rows on the certificate",
        "fields": [
          {
            "name": "coverage_type",
            "type": "TEXT",
            "description": "Coverage type"
          },
          {
            "name": "policy_number",
            "type": "TEXT",
            "description": "Policy number"
          },
          {
            "name": "effective_date",
            "type": "DATE",
            "description": "Policy effective date"
          },
          {
            "name": "expiration_date",
            "type": "DATE",
            "description": "Policy expiration date"
          },
          {
            "name": "limit_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Coverage limit amount"
          }
        ]
      },
      {
        "name": "certificate_holder",
        "type": "TEXT",
        "description": "Certificate holder name and address"
      },
      {
        "name": "description_of_operations",
        "type": "TEXT",
        "description": "Description of operations, locations, and vehicles"
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
      "name": "acord-25.pdf",
      "url": "https://example.com/documents/acord-25-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "producer_name",
        "type": "TEXT",
        "description": "Producer or broker name"
      },
      {
        "name": "insured_name",
        "type": "TEXT",
        "description": "Named insured"
      },
      {
        "name": "insurers_affording_coverage",
        "type": "TEXT",
        "description": "Insurers affording coverage"
      },
      {
        "name": "certificate_issue_date",
        "type": "DATE",
        "description": "Certificate issue date"
      },
      {
        "name": "coverages",
        "type": "ARRAY",
        "description": "Coverage rows on the certificate",
        "fields": [
          {
            "name": "coverage_type",
            "type": "TEXT",
            "description": "Coverage type"
          },
          {
            "name": "policy_number",
            "type": "TEXT",
            "description": "Policy number"
          },
          {
            "name": "effective_date",
            "type": "DATE",
            "description": "Policy effective date"
          },
          {
            "name": "expiration_date",
            "type": "DATE",
            "description": "Policy expiration date"
          },
          {
            "name": "limit_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Coverage limit amount"
          }
        ]
      },
      {
        "name": "certificate_holder",
        "type": "TEXT",
        "description": "Certificate holder name and address"
      },
      {
        "name": "description_of_operations",
        "type": "TEXT",
        "description": "Description of operations, locations, and vehicles"
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
      "name": "acord-25.pdf",
      "url": "https://example.com/documents/acord-25-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "producer_name",
        "type": "TEXT",
        "description": "Producer or broker name"
      },
      {
        "name": "insured_name",
        "type": "TEXT",
        "description": "Named insured"
      },
      {
        "name": "insurers_affording_coverage",
        "type": "TEXT",
        "description": "Insurers affording coverage"
      },
      {
        "name": "certificate_issue_date",
        "type": "DATE",
        "description": "Certificate issue date"
      },
      {
        "name": "coverages",
        "type": "ARRAY",
        "description": "Coverage rows on the certificate",
        "fields": [
          {
            "name": "coverage_type",
            "type": "TEXT",
            "description": "Coverage type"
          },
          {
            "name": "policy_number",
            "type": "TEXT",
            "description": "Policy number"
          },
          {
            "name": "effective_date",
            "type": "DATE",
            "description": "Policy effective date"
          },
          {
            "name": "expiration_date",
            "type": "DATE",
            "description": "Policy expiration date"
          },
          {
            "name": "limit_amount",
            "type": "CURRENCY_AMOUNT",
            "description": "Coverage limit amount"
          }
        ]
      },
      {
        "name": "certificate_holder",
        "type": "TEXT",
        "description": "Certificate holder name and address"
      },
      {
        "name": "description_of_operations",
        "type": "TEXT",
        "description": "Description of operations, locations, and vehicles"
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
				Name: "acord-25.pdf",
				Url: "https://example.com/documents/acord-25-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "producer_name",
					Type: "TEXT",
					Description: "Producer or broker name",
				},
				il.TextFieldConfig{
					Name: "insured_name",
					Type: "TEXT",
					Description: "Named insured",
				},
				il.TextFieldConfig{
					Name: "insurers_affording_coverage",
					Type: "TEXT",
					Description: "Insurers affording coverage",
				},
				il.DateFieldConfig{
					Name: "certificate_issue_date",
					Type: "DATE",
					Description: "Certificate issue date",
				},
				il.ArrayFieldConfig{
					Name: "coverages",
					Type: "ARRAY",
					Description: "Coverage rows on the certificate",
					Fields: []any{
						il.TextFieldConfig{
							Name: "coverage_type",
							Type: "TEXT",
							Description: "Coverage type",
						},
						il.TextFieldConfig{
							Name: "policy_number",
							Type: "TEXT",
							Description: "Policy number",
						},
						il.DateFieldConfig{
							Name: "effective_date",
							Type: "DATE",
							Description: "Policy effective date",
						},
						il.DateFieldConfig{
							Name: "expiration_date",
							Type: "DATE",
							Description: "Policy expiration date",
						},
						il.CurrencyAmountFieldConfig{
							Name: "limit_amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Coverage limit amount",
						},
					},
				},
				il.TextFieldConfig{
					Name: "certificate_holder",
					Type: "TEXT",
					Description: "Certificate holder name and address",
				},
				il.TextFieldConfig{
					Name: "description_of_operations",
					Type: "TEXT",
					Description: "Description of operations, locations, and vehicles",
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
  "name": "Extract ACORD 25 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract ACORD 25 Data\n\nInsurance teams use this recipe to extract ACORD 25 details without manually rekeying policy, claim, coverage, and loss information into claims systems.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-acord-25-data-overview",
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
      "id": "extract-acord-25-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"producer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Producer or broker name\"\n    },\n    {\n      \"name\": \"insured_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Named insured\"\n    },\n    {\n      \"name\": \"insurers_affording_coverage\",\n      \"type\": \"TEXT\",\n      \"description\": \"Insurers affording coverage\"\n    },\n    {\n      \"name\": \"certificate_issue_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Certificate issue date\"\n    },\n    {\n      \"name\": \"coverages\",\n      \"type\": \"ARRAY\",\n      \"description\": \"Coverage rows on the certificate\",\n      \"fields\": [\n        {\n          \"name\": \"coverage_type\",\n          \"type\": \"TEXT\",\n          \"description\": \"Coverage type\"\n        },\n        {\n          \"name\": \"policy_number\",\n          \"type\": \"TEXT\",\n          \"description\": \"Policy number\"\n        },\n        {\n          \"name\": \"effective_date\",\n          \"type\": \"DATE\",\n          \"description\": \"Policy effective date\"\n        },\n        {\n          \"name\": \"expiration_date\",\n          \"type\": \"DATE\",\n          \"description\": \"Policy expiration date\"\n        },\n        {\n          \"name\": \"limit_amount\",\n          \"type\": \"CURRENCY_AMOUNT\",\n          \"description\": \"Coverage limit amount\"\n        }\n      ]\n    },\n    {\n      \"name\": \"certificate_holder\",\n      \"type\": \"TEXT\",\n      \"description\": \"Certificate holder name and address\"\n    },\n    {\n      \"name\": \"description_of_operations\",\n      \"type\": \"TEXT\",\n      \"description\": \"Description of operations, locations, and vehicles\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "acord-25.pdf",
              "fileUrl": "https://example.com/documents/acord-25-sample.pdf"
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
      "id": "extract-acord-25-data-extract",
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
Extract acord 25 data from the file at [file URL]. Use the extract_document tool with these fields:

- producer_name (TEXT): Producer or broker name
- insured_name (TEXT): Named insured
- insurers_affording_coverage (TEXT): Insurers affording coverage
- certificate_issue_date (DATE): Certificate issue date
- coverages (ARRAY): Each with coverage_type (TEXT), policy_number (TEXT), effective_date (DATE), expiration_date (DATE), limit_amount (CURRENCY_AMOUNT)
- certificate_holder (TEXT): Certificate holder name and address
- description_of_operations (TEXT): Description of operations, locations, and vehicles
```

### Response


```json
{
  "success": true,
  "data": {
    "producer_name": {
      "value": "Producer Name",
      "confidence": 0.97,
      "citations": [
        "PRODUCER NAME"
      ]
    },
    "insured_name": {
      "value": "Insured Name",
      "confidence": 0.97,
      "citations": [
        "INSURED NAME"
      ]
    },
    "insurers_affording_coverage": {
      "value": "Insurers Affording Coverage",
      "confidence": 0.97,
      "citations": [
        "INSURERS AFFORDING COVERAGE"
      ]
    },
    "certificate_issue_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "coverages": {
      "value": [
        {
          "coverage_type": {
            "value": "Coverage Type",
            "confidence": 0.96,
            "citations": [
              "COVERAGE TYPE"
            ]
          },
          "policy_number": {
            "value": "Policy Number",
            "confidence": 0.96,
            "citations": [
              "POLICY NUMBER"
            ]
          },
          "effective_date": {
            "value": "2026-04-15",
            "confidence": 0.96,
            "citations": [
              "15 Apr 2026"
            ]
          },
          "expiration_date": {
            "value": "2026-04-15",
            "confidence": 0.96,
            "citations": [
              "15 Apr 2026"
            ]
          },
          "limit_amount": {
            "value": {
              "amount": "1234.56",
              "currency": "USD"
            },
            "confidence": 0.96,
            "citations": [
              "$1,234.56"
            ]
          }
        }
      ],
      "confidence": 0.97,
      "citations": [
        "COVERAGES"
      ]
    },
    "certificate_holder": {
      "value": "Certificate Holder",
      "confidence": 0.97,
      "citations": [
        "CERTIFICATE HOLDER"
      ]
    },
    "description_of_operations": {
      "value": "Description Of Operations",
      "confidence": 0.97,
      "citations": [
        "DESCRIPTION OF OPERATIONS"
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
