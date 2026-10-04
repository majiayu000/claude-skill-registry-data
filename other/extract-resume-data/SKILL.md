---
name: extract-resume-data
description: Extract candidate name, contact details, work history, and skills from resumes.
---

# Extract Resume Data

Recruiting teams and HR platforms use this recipe to use the Iteration Layer Document Extraction API as a resume parser API for PDF and DOCX resumes. Upload a resume and receive structured JSON with candidate name, email, work history, and skills — ready for your ATS or candidate pipeline.

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
        "name": "resume.pdf",
        "url": "https://example.com/resumes/resume.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "name",
          "type": "TEXT",
          "description": "Full name of the candidate"
        },
        {
          "name": "email",
          "type": "EMAIL",
          "description": "Candidate email address"
        },
        {
          "name": "experience",
          "type": "ARRAY",
          "description": "Work experience entries",
          "fields": [
            {
              "name": "company",
              "type": "TEXT",
              "description": "Employer or company name"
            },
            {
              "name": "role",
              "type": "TEXT",
              "description": "Job title or role"
            },
            {
              "name": "start_date",
              "type": "DATE",
              "description": "Start date of employment"
            },
            {
              "name": "end_date",
              "type": "DATE",
              "description": "End date of employment"
            }
          ]
        },
        {
          "name": "skills",
          "type": "ARRAY",
          "description": "List of candidate skills",
          "fields": [
            {
              "name": "skill",
              "type": "TEXT",
              "description": "Skill name"
            }
          ]
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
      name: "resume.pdf",
      url: "https://example.com/resumes/resume.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "name",
        type: "TEXT",
        description: "Full name of the candidate",
      },
      {
        name: "email",
        type: "EMAIL",
        description: "Candidate email address",
      },
      {
        name: "experience",
        type: "ARRAY",
        description: "Work experience entries",
        fields: [
          {
            name: "company",
            type: "TEXT",
            description: "Employer or company name",
          },
          {
            name: "role",
            type: "TEXT",
            description: "Job title or role",
          },
          {
            name: "start_date",
            type: "DATE",
            description: "Start date of employment",
          },
            {
              name: "end_date",
              type: "DATE",
              description: "End date of employment",
            },
          ],
      },
      {
        name: "skills",
        type: "ARRAY",
        description: "List of candidate skills",
        fields: [
          {
            name: "skill",
            type: "TEXT",
            description: "Skill name",
          },
        ],
      },
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
            "name": "resume.pdf",
            "url": "https://example.com/resumes/resume.pdf",
        }
    ],
    schema={
        "fields": [
            {
                "name": "name",
                "type": "TEXT",
                "description": "Full name of the candidate",
            },
            {
                "name": "email",
                "type": "EMAIL",
                "description": "Candidate email address",
            },
            {
                "name": "experience",
                "type": "ARRAY",
                "description": "Work experience entries",
                "fields": [
                    {
                        "name": "company",
                        "type": "TEXT",
                        "description": "Employer or company name",
                    },
                    {
                        "name": "role",
                        "type": "TEXT",
                        "description": "Job title or role",
                    },
                    {
                        "name": "start_date",
                        "type": "DATE",
                        "description": "Start date of employment",
                      },
                      {
                          "name": "end_date",
                          "type": "DATE",
                          "description": "End date of employment",
                      },
                    ],
            },
            {
                "name": "skills",
                "type": "ARRAY",
                "description": "List of candidate skills",
                "fields": [
                    {
                        "name": "skill",
                        "type": "TEXT",
                        "description": "Skill name",
                    },
                ],
            },
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
				Name: "resume.pdf",
				Url: "https://example.com/resumes/resume.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "name",
					Type: "TEXT",
					Description: "Full name of the candidate",
				},
				il.EmailFieldConfig{
					Name: "email",
					Type: "EMAIL",
					Description: "Candidate email address",
				},
				il.ArrayFieldConfig{
					Name: "experience",
					Type: "ARRAY",
					Description: "Work experience entries",
					Fields: []any{
						il.TextFieldConfig{
							Name: "company",
							Type: "TEXT",
							Description: "Employer or company name",
						},
						il.TextFieldConfig{
							Name: "role",
							Type: "TEXT",
							Description: "Job title or role",
						},
						il.DateFieldConfig{
							Name: "start_date",
							Type: "DATE",
							Description: "Start date of employment",
						},
						il.DateFieldConfig{
							Name: "end_date",
							Type: "DATE",
							Description: "End date of employment",
						},
					},
				},
				il.ArrayFieldConfig{
					Name: "skills",
					Type: "ARRAY",
					Description: "List of candidate skills",
					Fields: []any{
						il.TextFieldConfig{
							Name: "skill",
							Type: "TEXT",
							Description: "Skill name",
						},
					},
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
  "name": "Extract Resume Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Resume Data\n\nRecruiting teams and HR platforms use this recipe to automate resume screening. Upload a resume in PDF or DOCX format and receive structured JSON with candidate name, email, work history, and skills \u2014 ready for your ATS or candidate pipeline.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "9ff8f73c-a387-4f6b-b9c0-3be0d7602f6c",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
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
      "id": "9268c275-4ae6-4e58-bf98-1b51dbcbb45a",
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
      "id": "a5b6c7d8-e9f0-1234-abcd-345678901abc",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"name\",\"type\":\"TEXT\",\"description\":\"Full name of the candidate\"},{\"name\":\"email\",\"type\":\"EMAIL\",\"description\":\"Candidate email address\"},{\"name\":\"experience\",\"type\":\"ARRAY\",\"description\":\"Work experience entries\",\"fields\":[{\"name\":\"company\",\"type\":\"TEXT\",\"description\":\"Employer or company name\"},{\"name\":\"role\",\"type\":\"TEXT\",\"description\":\"Job title or role\"},{\"name\":\"start_date\",\"type\":\"DATE\",\"description\":\"Start date of employment\"},{\"name\":\"end_date\",\"type\":\"DATE\",\"description\":\"End date of employment\"}]},{\"name\":\"skills\",\"type\":\"ARRAY\",\"description\":\"List of candidate skills\",\"fields\":[{\"name\":\"skill\",\"type\":\"TEXT\",\"description\":\"Skill name\"}]}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "resume.pdf",
              "fileUrl": "https://example.com/resumes/resume.pdf"
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
      "id": "b6c7d8e9-f0a1-2345-bcde-456789012bcd",
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
Extract resume data from the file at [file URL]. Use the extract_document tool with these fields:

- name (TEXT): Full name of the candidate
- email (EMAIL): Candidate email address
- experience (ARRAY): Each with company (TEXT), role (TEXT), start_date (DATE), end_date (DATE)
- skills (ARRAY): Each with skill (TEXT)
```

### Response


```json
{
  "success": true,
  "data": {
    "name": {
      "value": "Sarah Chen",
      "confidence": 0.99,
      "citations": ["Sarah Chen"]
    },
    "email": {
      "value": "sarah.chen@email.com",
      "confidence": 0.98,
      "citations": ["sarah.chen@email.com"]
    },
    "experience": {
      "value": [
        {
          "company": {
            "value": "Stripe",
            "confidence": 0.97,
            "citations": ["Stripe, Inc."]
          },
          "role": {
            "value": "Senior Software Engineer",
            "confidence": 0.98,
            "citations": ["Senior Software Engineer"]
          },
          "start_date": {
            "value": "2022-03-01",
            "confidence": 0.94,
            "citations": ["March 2022"]
          },
          "end_date": {
            "value": "2025-11-01",
            "confidence": 0.93,
            "citations": ["November 2025"]
          }
        },
        {
          "company": {
            "value": "Shopify",
            "confidence": 0.97,
            "citations": ["Shopify"]
          },
          "role": {
            "value": "Software Engineer",
            "confidence": 0.96,
            "citations": ["Software Engineer"]
          },
          "start_date": {
            "value": "2019-06-01",
            "confidence": 0.93,
            "citations": ["June 2019"]
          },
          "end_date": {
            "value": "2022-02-01",
            "confidence": 0.92,
            "citations": ["February 2022"]
          }
        }
      ],
      "confidence": 0.95,
      "citations": []
    },
    "skills": {
      "value": [
        {
          "skill": {
            "value": "TypeScript",
            "confidence": 0.97,
            "citations": ["TypeScript"]
          }
        },
        {
          "skill": {
            "value": "React",
            "confidence": 0.97,
            "citations": ["React"]
          }
        }
      ],
      "confidence": 0.96,
      "citations": []
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
