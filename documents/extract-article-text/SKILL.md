---
name: extract-article-text
description: Extract clean article content — title, author, date, and body text — from PDFs, Word docs, and web pages.
---

# Extract Article Text

Content aggregators and newsletter platforms use this recipe to extract clean article content from PDFs, Word documents, and saved web pages. Define fields for title, author, date, body, and summary — the parser pulls the content and ignores headers, footers, navigation, and sidebars.

## APIs Used

Document Extraction (1 credit per page)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST \
  https://api.iterationlayer.com/document-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "type": "url",
        "name": "article.pdf",
        "url": "https://example.com/article.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "title",
          "type": "TEXT",
          "description": "Article title or headline",
          "is_required": true
        },
        {
          "name": "author",
          "type": "TEXT",
          "description": "Author name"
        },
        {
          "name": "publish_date",
          "type": "DATE",
          "description": "Publication date of the article"
        },
        {
          "name": "body",
          "type": "TEXTAREA",
          "description": "Main article text content, excluding headers, footers, sidebars, and navigation",
          "is_required": true
        },
        {
          "name": "summary",
          "type": "TEXT",
          "description": "Brief summary or abstract",
          "max_length": 500
        },
        {
          "name": "category",
          "type": "TEXT",
          "description": "Article category or section"
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
      name: "article.pdf",
      url: "https://example.com/article.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "title",
        type: "TEXT",
        description: "Article title or headline",
        is_required: true,
      },
      {
        name: "author",
        type: "TEXT",
        description: "Author name",
      },
      {
        name: "publish_date",
        type: "DATE",
        description: "Publication date of the article",
      },
      {
        name: "body",
        type: "TEXTAREA",
        description: "Main article text content, excluding headers, footers, sidebars, and navigation",
        is_required: true,
      },
      {
        name: "summary",
        type: "TEXT",
        description: "Brief summary or abstract",
        max_length: 500,
      },
      {
        name: "category",
        type: "TEXT",
        description: "Article category or section",
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
            "name": "article.pdf",
            "url": "https://example.com/article.pdf",
        }
    ],
    schema={
        "fields": [
            {
                "name": "title",
                "type": "TEXT",
                "description": "Article title or headline",
                "is_required": True,
            },
            {
                "name": "author",
                "type": "TEXT",
                "description": "Author name",
            },
            {
                "name": "publish_date",
                "type": "DATE",
                "description": "Publication date of the article",
            },
            {
                "name": "body",
                "type": "TEXTAREA",
                "description": "Main article text content, excluding headers, footers, sidebars, and navigation",
                "is_required": True,
            },
            {
                "name": "summary",
                "type": "TEXT",
                "description": "Brief summary or abstract",
                "max_length": 500,
            },
            {
                "name": "category",
                "type": "TEXT",
                "description": "Article category or section",
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
				Name: "article.pdf",
				Url: "https://example.com/article.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "title",
					Type: "TEXT",
					Description: "Article title or headline",
				},
				il.TextFieldConfig{
					Name: "author",
					Type: "TEXT",
					Description: "Author name",
				},
				il.DateFieldConfig{
					Name: "publish_date",
					Type: "DATE",
					Description: "Publication date of the article",
				},
				il.TextareaFieldConfig{
					Name: "body",
					Type: "TEXTAREA",
					Description: "Main article text content, excluding headers, footers, sidebars, and navigation",
				},
				il.TextFieldConfig{
					Name: "summary",
					Type: "TEXT",
					Description: "Brief summary or abstract",
				},
				il.TextFieldConfig{
					Name: "category",
					Type: "TEXT",
					Description: "Article category or section",
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
  "name": "Extract Article Text",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Article Text\n\nContent aggregators and newsletter platforms use this recipe to extract clean article content from PDFs, Word documents, and saved web pages. Define fields for title, author, date, body, and summary \u2014 the parser pulls the content and ignores headers, footers, navigation, and sidebars.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "97f247db-41d8-4eae-95c9-d65cc3b2124d",
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
      "id": "a0acbdab-4287-4466-8b64-95bd9d4e3e49",
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
      "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"title\",\"type\":\"TEXT\",\"description\":\"Article title or headline\",\"is_required\":true},{\"name\":\"author\",\"type\":\"TEXT\",\"description\":\"Author name\"},{\"name\":\"publish_date\",\"type\":\"DATE\",\"description\":\"Publication date of the article\"},{\"name\":\"body\",\"type\":\"TEXTAREA\",\"description\":\"Main article text content, excluding headers, footers, sidebars, and navigation\",\"is_required\":true},{\"name\":\"summary\",\"type\":\"TEXT\",\"description\":\"Brief summary or abstract\",\"max_length\":500},{\"name\":\"category\",\"type\":\"TEXT\",\"description\":\"Article category or section\"}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "article.pdf",
              "fileUrl": "https://example.com/article.pdf"
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
      "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
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
Extract article content from the file at [file URL]. Use the extract_document tool with these fields:

- title (TEXT, required): Article title or headline
- author (TEXT): Author name
- publish_date (DATE): Publication date of the article
- body (TEXTAREA, required): Main article text content, excluding headers, footers, sidebars, and navigation
- summary (TEXT): Brief summary or abstract
- category (TEXT): Article category or section
```

### Response


```json
{
  "success": true,
  "data": {
    "title": {
      "value": "The Quiet Revolution in Battery Chemistry",
      "confidence": 0.97,
      "citations": ["The Quiet Revolution in Battery Chemistry"],
      "source": "article.pdf"
    },
    "author": {
      "value": "James Park",
      "confidence": 0.94,
      "citations": ["James Park"],
      "source": "article.pdf"
    },
    "publish_date": {
      "value": "2026-01-15",
      "confidence": 0.93,
      "citations": ["January 15, 2026"],
      "source": "article.pdf"
    },
    "body": {
      "value": "Solid-state batteries have been five years away for the last twenty years. But the latest generation of prototypes from three independent labs suggests the timeline might finally be real...",
      "confidence": 0.91,
      "citations": ["Solid-state batteries have been five years away"],
      "source": "article.pdf"
    },
    "summary": {
      "value": "Recent advances in solid-state battery technology suggest commercial viability within three years, driven by breakthroughs in solid electrolyte materials.",
      "confidence": 0.88,
      "citations": ["solid-state battery technology"],
      "source": "article.pdf"
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
