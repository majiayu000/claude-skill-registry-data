---
name: extract-i-9-data
description: Extract structured fields from i-9 documents.
---

# Extract I-9 Data

Finance teams use this recipe to extract I-9 fields into structured JSON for accounts receivable, accounts payable, tax, and ERP workflows.

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
      "name": "i-9.pdf",
      "url": "https://example.com/documents/i-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_last_name",
        "type": "TEXT",
        "description": "Employee last name"
      },
      {
        "name": "employee_first_name",
        "type": "TEXT",
        "description": "Employee first name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Employee date of birth"
      },
      {
        "name": "citizenship_status",
        "type": "TEXT",
        "description": "Selected citizenship or immigration status"
      },
      {
        "name": "alien_registration_or_uscis_number",
        "type": "TEXT",
        "description": "Alien Registration Number or USCIS Number if provided"
      },
      {
        "name": "document_title",
        "type": "TEXT",
        "description": "List A, B, or C document title"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Document number"
      },
      {
        "name": "document_expiration_date",
        "type": "DATE",
        "description": "Document expiration date"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer or authorized representative name"
      },
      {
        "name": "employer_signature_date",
        "type": "DATE",
        "description": "Employer certification date"
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
      "name": "i-9.pdf",
      "url": "https://example.com/documents/i-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_last_name",
        "type": "TEXT",
        "description": "Employee last name"
      },
      {
        "name": "employee_first_name",
        "type": "TEXT",
        "description": "Employee first name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Employee date of birth"
      },
      {
        "name": "citizenship_status",
        "type": "TEXT",
        "description": "Selected citizenship or immigration status"
      },
      {
        "name": "alien_registration_or_uscis_number",
        "type": "TEXT",
        "description": "Alien Registration Number or USCIS Number if provided"
      },
      {
        "name": "document_title",
        "type": "TEXT",
        "description": "List A, B, or C document title"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Document number"
      },
      {
        "name": "document_expiration_date",
        "type": "DATE",
        "description": "Document expiration date"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer or authorized representative name"
      },
      {
        "name": "employer_signature_date",
        "type": "DATE",
        "description": "Employer certification date"
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
      "name": "i-9.pdf",
      "url": "https://example.com/documents/i-9-sample.pdf"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "employee_last_name",
        "type": "TEXT",
        "description": "Employee last name"
      },
      {
        "name": "employee_first_name",
        "type": "TEXT",
        "description": "Employee first name"
      },
      {
        "name": "employee_address",
        "type": "ADDRESS",
        "description": "Employee address"
      },
      {
        "name": "date_of_birth",
        "type": "DATE",
        "description": "Employee date of birth"
      },
      {
        "name": "citizenship_status",
        "type": "TEXT",
        "description": "Selected citizenship or immigration status"
      },
      {
        "name": "alien_registration_or_uscis_number",
        "type": "TEXT",
        "description": "Alien Registration Number or USCIS Number if provided"
      },
      {
        "name": "document_title",
        "type": "TEXT",
        "description": "List A, B, or C document title"
      },
      {
        "name": "document_number",
        "type": "TEXT",
        "description": "Document number"
      },
      {
        "name": "document_expiration_date",
        "type": "DATE",
        "description": "Document expiration date"
      },
      {
        "name": "employer_name",
        "type": "TEXT",
        "description": "Employer or authorized representative name"
      },
      {
        "name": "employer_signature_date",
        "type": "DATE",
        "description": "Employer certification date"
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
				Name: "i-9.pdf",
				Url: "https://example.com/documents/i-9-sample.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "employee_last_name",
					Type: "TEXT",
					Description: "Employee last name",
				},
				il.TextFieldConfig{
					Name: "employee_first_name",
					Type: "TEXT",
					Description: "Employee first name",
				},
				il.AddressFieldConfig{
					Name: "employee_address",
					Type: "ADDRESS",
					Description: "Employee address",
				},
				il.DateFieldConfig{
					Name: "date_of_birth",
					Type: "DATE",
					Description: "Employee date of birth",
				},
				il.TextFieldConfig{
					Name: "citizenship_status",
					Type: "TEXT",
					Description: "Selected citizenship or immigration status",
				},
				il.TextFieldConfig{
					Name: "alien_registration_or_uscis_number",
					Type: "TEXT",
					Description: "Alien Registration Number or USCIS Number if provided",
				},
				il.TextFieldConfig{
					Name: "document_title",
					Type: "TEXT",
					Description: "List A, B, or C document title",
				},
				il.TextFieldConfig{
					Name: "document_number",
					Type: "TEXT",
					Description: "Document number",
				},
				il.DateFieldConfig{
					Name: "document_expiration_date",
					Type: "DATE",
					Description: "Document expiration date",
				},
				il.TextFieldConfig{
					Name: "employer_name",
					Type: "TEXT",
					Description: "Employer or authorized representative name",
				},
				il.DateFieldConfig{
					Name: "employer_signature_date",
					Type: "DATE",
					Description: "Employer certification date",
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
  "name": "Extract I-9 Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract I-9 Data\n\nFinance teams use this recipe to extract I-9 fields into structured JSON for accounts receivable, accounts payable, tax, and ERP workflows.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "extract-i-9-data-overview",
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
      "id": "extract-i-9-data-trigger",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\n  \"fields\": [\n    {\n      \"name\": \"employee_last_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee last name\"\n    },\n    {\n      \"name\": \"employee_first_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employee first name\"\n    },\n    {\n      \"name\": \"employee_address\",\n      \"type\": \"ADDRESS\",\n      \"description\": \"Employee address\"\n    },\n    {\n      \"name\": \"date_of_birth\",\n      \"type\": \"DATE\",\n      \"description\": \"Employee date of birth\"\n    },\n    {\n      \"name\": \"citizenship_status\",\n      \"type\": \"TEXT\",\n      \"description\": \"Selected citizenship or immigration status\"\n    },\n    {\n      \"name\": \"alien_registration_or_uscis_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Alien Registration Number or USCIS Number if provided\"\n    },\n    {\n      \"name\": \"document_title\",\n      \"type\": \"TEXT\",\n      \"description\": \"List A, B, or C document title\"\n    },\n    {\n      \"name\": \"document_number\",\n      \"type\": \"TEXT\",\n      \"description\": \"Document number\"\n    },\n    {\n      \"name\": \"document_expiration_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Document expiration date\"\n    },\n    {\n      \"name\": \"employer_name\",\n      \"type\": \"TEXT\",\n      \"description\": \"Employer or authorized representative name\"\n    },\n    {\n      \"name\": \"employer_signature_date\",\n      \"type\": \"DATE\",\n      \"description\": \"Employer certification date\"\n    }\n  ]\n}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "i-9.pdf",
              "fileUrl": "https://example.com/documents/i-9-sample.pdf"
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
      "id": "extract-i-9-data-extract",
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
Extract i-9 data from the file at [file URL]. Use the extract_document tool with these fields:

- employee_last_name (TEXT): Employee last name
- employee_first_name (TEXT): Employee first name
- employee_address (ADDRESS): Employee address
- date_of_birth (DATE): Employee date of birth
- citizenship_status (TEXT): Selected citizenship or immigration status
- alien_registration_or_uscis_number (TEXT): Alien Registration Number or USCIS Number if provided
- document_title (TEXT): List A, B, or C document title
- document_number (TEXT): Document number
- document_expiration_date (DATE): Document expiration date
- employer_name (TEXT): Employer or authorized representative name
- employer_signature_date (DATE): Employer certification date
```

### Response


```json
{
  "success": true,
  "data": {
    "employee_last_name": {
      "value": "Employee Last Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE LAST NAME"
      ]
    },
    "employee_first_name": {
      "value": "Employee First Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE FIRST NAME"
      ]
    },
    "employee_address": {
      "value": {
        "street": "100 Market Street",
        "city": "Berlin",
        "postal_code": "10115",
        "country": "DE"
      },
      "confidence": 0.97,
      "citations": [
        "EMPLOYEE ADDRESS"
      ]
    },
    "date_of_birth": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "citizenship_status": {
      "value": "Citizenship Status",
      "confidence": 0.97,
      "citations": [
        "CITIZENSHIP STATUS"
      ]
    },
    "alien_registration_or_uscis_number": {
      "value": "Alien Registration Or Uscis Number",
      "confidence": 0.97,
      "citations": [
        "ALIEN REGISTRATION OR USCIS NUMBER"
      ]
    },
    "document_title": {
      "value": "Document Title",
      "confidence": 0.97,
      "citations": [
        "DOCUMENT TITLE"
      ]
    },
    "document_number": {
      "value": "BL-2026-00418",
      "confidence": 0.97,
      "citations": [
        "DOCUMENT NUMBER"
      ]
    },
    "document_expiration_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
      ]
    },
    "employer_name": {
      "value": "Employer Name",
      "confidence": 0.97,
      "citations": [
        "EMPLOYER NAME"
      ]
    },
    "employer_signature_date": {
      "value": "2026-04-15",
      "confidence": 0.97,
      "citations": [
        "15 Apr 2026"
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
