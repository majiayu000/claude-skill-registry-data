---
name: markdown-to-styled-pdf
description: Generate a professionally styled PDF document from Markdown content with custom fonts, headers, and page numbers.
---

# Convert Markdown to Styled PDF

Content teams and publishing platforms use this recipe to produce PDF documents from Markdown source files. Define page layout, typography, and branding — the API renders the Markdown into a polished PDF with headers, footers, and page numbers.

## APIs Used

Document Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/document-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "document": {
      "metadata": {
        "title": "Project Proposal",
        "author": "Engineering Team"
      },
      "page": {
        "size": { "preset": "A4" },
        "margins": {
          "top_in_pt": 72,
          "right_in_pt": 72,
          "bottom_in_pt": 72,
          "left_in_pt": 72
        }
      },
      "styles": {
        "text": {
          "font_family": "Helvetica",
          "font_size_in_pt": 12.0,
          "line_height": 1.5,
          "color": "#1A1A1A"
        },
        "headline": {
          "font_family": "Helvetica",
          "font_size_in_pt": 20.0,
          "color": "#111111",
          "spacing_before_in_pt": 24.0,
          "spacing_after_in_pt": 12.0,
          "font_weight": "bold"
        },
        "link": {
          "color": "#0066CC",
          "is_underlined": true
        },
        "list": {
          "text_style": {
            "font_family": "Helvetica",
            "font_size_in_pt": 12.0,
            "line_height": 1.5,
            "color": "#1A1A1A"
          },
          "marker_color": "#1A1A1A",
          "marker_gap_in_pt": 8.0
        },
        "table": {
          "header": {
            "background_color": "#2B579A",
            "text_color": "#FFFFFF",
            "font_size_in_pt": 12.0,
            "font_weight": "bold"
          },
          "body": {
            "background_color": "#FFFFFF",
            "text_color": "#333333",
            "font_size_in_pt": 12.0
          },
          "border": {
            "outer": {
              "top": { "color": "#CCCCCC", "width_in_pt": 1.0 },
              "right": { "color": "#CCCCCC", "width_in_pt": 1.0 },
              "bottom": { "color": "#CCCCCC", "width_in_pt": 1.0 },
              "left": { "color": "#CCCCCC", "width_in_pt": 1.0 }
            },
            "inner": {
              "horizontal": { "color": "#EEEEEE", "width_in_pt": 0.5 },
              "vertical": { "color": "#EEEEEE", "width_in_pt": 0.5 }
            }
          }
        },
        "separator": {
          "color": "#CCCCCC",
          "thickness_in_pt": 0.5,
          "spacing_before_in_pt": 24.0,
          "spacing_after_in_pt": 24.0
        },
        "image": {
          "border_color": "#000000",
          "border_width_in_pt": 0.0
        }
      },
      "footer": [
        {
          "type": "paragraph",
          "runs": [{
            "text": "Page {{page_number}}"
          }]
        }
      ],
      "content": [
        {
          "type": "headline",
          "level": "h1",
          "text": "Project Proposal"
        },
        {
          "type": "paragraph",
          "markdown": "## Overview\n\nThis proposal outlines the technical approach, timeline, and resource requirements for the **Platform Modernization** initiative.\n\n## Goals\n\n- Migrate the monolithic backend to a **microservices architecture**\n- Reduce average API response time from 420ms to under 100ms\n- Achieve **99.95% uptime** SLA for all customer-facing endpoints\n- Implement automated canary deployments across all services\n\n## Timeline\n\n**Phase 1 — Foundation (Weeks 1–4)**\nService mesh setup, CI/CD pipeline migration, and observability instrumentation.\n\n**Phase 2 — Migration (Weeks 5–12)**\nIncremental extraction of domain services from the monolith, starting with authentication and billing.\n\n**Phase 3 — Optimization (Weeks 13–16)**\nPerformance tuning, load testing, and SLA validation.\n\n## Budget\n\nEstimated total: **$284,000** across infrastructure, tooling, and contractor hours."
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.generateDocument({
  format: "pdf",
  document: {
    metadata: {
      title: "Project Proposal",
      author: "Engineering Team",
    },
    page: {
      size: { preset: "A4" },
      margins: {
        top_in_pt: 72,
        right_in_pt: 72,
        bottom_in_pt: 72,
        left_in_pt: 72,
      },
    },
    styles: {
      text: {
        font_family: "Helvetica",
        font_size_in_pt: 12.0,
        line_height: 1.5,
        color: "#1A1A1A",
      },
      headline: {
        font_family: "Helvetica",
        font_size_in_pt: 20.0,
        color: "#111111",
        spacing_before_in_pt: 24.0,
        spacing_after_in_pt: 12.0,
        font_weight: "bold",
      },
      link: {
        color: "#0066CC",
        is_underlined: true,
      },
      list: {
        text_style: {
          font_family: "Helvetica",
          font_size_in_pt: 12.0,
          line_height: 1.5,
          color: "#1A1A1A",
        },
        marker_color: "#1A1A1A",
        marker_gap_in_pt: 8.0,
      },
      table: {
        header: {
          background_color: "#2B579A",
          text_color: "#FFFFFF",
          font_size_in_pt: 12.0,
          font_weight: "bold",
        },
        body: {
          background_color: "#FFFFFF",
          text_color: "#333333",
          font_size_in_pt: 12.0,
        },
        border: {
          outer: {
            top: { color: "#CCCCCC", width_in_pt: 1.0 },
            right: { color: "#CCCCCC", width_in_pt: 1.0 },
            bottom: { color: "#CCCCCC", width_in_pt: 1.0 },
            left: { color: "#CCCCCC", width_in_pt: 1.0 },
          },
          inner: {
            horizontal: { color: "#EEEEEE", width_in_pt: 0.5 },
            vertical: { color: "#EEEEEE", width_in_pt: 0.5 },
          },
        },
      },
      separator: {
        color: "#CCCCCC",
        thickness_in_pt: 0.5,
        spacing_before_in_pt: 24.0,
        spacing_after_in_pt: 24.0,
      },
      image: {
        border_color: "#000000",
        border_width_in_pt: 0.0,
      },
    },
    footer: [
      {
        type: "paragraph",
        runs: [
          {
            text: "Page {{page_number}}",
          },
        ],
      },
    ],
    content: [
      {
        type: "headline",
        level: "h1",
        text: "Project Proposal",
      },
      {
        type: "paragraph",
        markdown:
          "## Overview\n\nThis proposal outlines the technical approach, timeline, and resource requirements for the **Platform Modernization** initiative.\n\n## Goals\n\n- Migrate the monolithic backend to a **microservices architecture**\n- Reduce average API response time from 420ms to under 100ms\n- Achieve **99.95% uptime** SLA for all customer-facing endpoints\n- Implement automated canary deployments across all services\n\n## Timeline\n\n**Phase 1 — Foundation (Weeks 1–4)**\nService mesh setup, CI/CD pipeline migration, and observability instrumentation.\n\n**Phase 2 — Migration (Weeks 5–12)**\nIncremental extraction of domain services from the monolith, starting with authentication and billing.\n\n**Phase 3 — Optimization (Weeks 13–16)**\nPerformance tuning, load testing, and SLA validation.\n\n## Budget\n\nEstimated total: **$284,000** across infrastructure, tooling, and contractor hours.",
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_document(
    format="pdf",
    document={
        "metadata": {
            "title": "Project Proposal",
            "author": "Engineering Team",
        },
        "page": {
            "size": {"preset": "A4"},
            "margins": {
                "top_in_pt": 72,
                "right_in_pt": 72,
                "bottom_in_pt": 72,
                "left_in_pt": 72,
            },
        },
        "styles": {
            "text": {
                "font_family": "Helvetica",
                "font_size_in_pt": 12.0,
                "line_height": 1.5,
                "color": "#1A1A1A",
            },
            "headline": {
                "font_family": "Helvetica",
                "font_size_in_pt": 20.0,
                "color": "#111111",
                "spacing_before_in_pt": 24.0,
                "spacing_after_in_pt": 12.0,
                "font_weight": "bold",
            },
            "link": {
                "color": "#0066CC",
                "is_underlined": True,
            },
            "list": {
                "text_style": {
                    "font_family": "Helvetica",
                    "font_size_in_pt": 12.0,
                    "line_height": 1.5,
                    "color": "#1A1A1A",
                },
                "marker_color": "#1A1A1A",
                "marker_gap_in_pt": 8.0,
            },
            "table": {
                "header": {
                    "background_color": "#2B579A",
                    "text_color": "#FFFFFF",
                    "font_size_in_pt": 12.0,
                    "font_weight": "bold",
                },
                "body": {
                    "background_color": "#FFFFFF",
                    "text_color": "#333333",
                    "font_size_in_pt": 12.0,
                },
                "border": {
                    "outer": {
                        "top": {"color": "#CCCCCC", "width_in_pt": 1.0},
                        "right": {"color": "#CCCCCC", "width_in_pt": 1.0},
                        "bottom": {"color": "#CCCCCC", "width_in_pt": 1.0},
                        "left": {"color": "#CCCCCC", "width_in_pt": 1.0},
                    },
                    "inner": {
                        "horizontal": {"color": "#EEEEEE", "width_in_pt": 0.5},
                        "vertical": {"color": "#EEEEEE", "width_in_pt": 0.5},
                    },
                },
            },
            "separator": {
                "color": "#CCCCCC",
                "thickness_in_pt": 0.5,
                "spacing_before_in_pt": 24.0,
                "spacing_after_in_pt": 24.0,
            },
            "image": {
                "border_color": "#000000",
                "border_width_in_pt": 0.0,
            },
        },
        "footer": [
            {
                "type": "paragraph",
                "runs": [{
                    "text": "Page {{page_number}}",
                }],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Project Proposal",
            },
            {
                "type": "paragraph",
                "markdown": "## Overview\n\nThis proposal outlines the technical approach, timeline, and resource requirements for the **Platform Modernization** initiative.\n\n## Goals\n\n- Migrate the monolithic backend to a **microservices architecture**\n- Reduce average API response time from 420ms to under 100ms\n- Achieve **99.95% uptime** SLA for all customer-facing endpoints\n- Implement automated canary deployments across all services\n\n## Timeline\n\n**Phase 1 \u2014 Foundation (Weeks 1\u20134)**\nService mesh setup, CI/CD pipeline migration, and observability instrumentation.\n\n**Phase 2 \u2014 Migration (Weeks 5\u201312)**\nIncremental extraction of domain services from the monolith, starting with authentication and billing.\n\n**Phase 3 \u2014 Optimization (Weeks 13\u201316)**\nPerformance tuning, load testing, and SLA validation.\n\n## Budget\n\nEstimated total: **$284,000** across infrastructure, tooling, and contractor hours.",
            },
        ],
    },
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.GenerateDocument(il.GenerateDocumentRequest{
		Format: "pdf",
		Document: il.DocumentDefinition{
			Metadata: il.DocumentMetadata{
				Title:  "Project Proposal",
				Author: "Engineering Team",
			},
			Page: il.PageConfig{
				Size: il.PageSize{Preset: "A4"},
				Margins: il.Margins{
					TopInPt:    72,
					RightInPt:  72,
					BottomInPt: 72,
					LeftInPt:   72,
				},
			},
			Footer: []il.ContentBlock{
				il.ContentBlock{
					"type": "paragraph",
					"runs": []map[string]string{
						{"text": "Page {{page_number}}"},
					},
				},
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "Project Proposal"),
				il.ParagraphBlock{
					Type:     "paragraph",
					Markdown: "## Overview\n\nThis proposal outlines the technical approach, timeline, and resource requirements for the **Platform Modernization** initiative.\n\n## Goals\n\n- Migrate the monolithic backend to a **microservices architecture**\n- Reduce average API response time from 420ms to under 100ms\n- Achieve **99.95% uptime** SLA for all customer-facing endpoints\n- Implement automated canary deployments across all services\n\n## Timeline\n\n**Phase 1 \u2014 Foundation (Weeks 1\u20134)**\nService mesh setup, CI/CD pipeline migration, and observability instrumentation.\n\n**Phase 2 \u2014 Migration (Weeks 5\u201312)**\nIncremental extraction of domain services from the monolith, starting with authentication and billing.\n\n**Phase 3 \u2014 Optimization (Weeks 13\u201316)**\nPerformance tuning, load testing, and SLA validation.\n\n## Budget\n\nEstimated total: **$284,000** across infrastructure, tooling, and contractor hours.",
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
  "name": "Convert Markdown to Styled PDF",
  "nodes": [
    {
      "parameters": {
        "content": "## Convert Markdown to Styled PDF\n\nContent teams and publishing platforms use this recipe to produce PDF documents from Markdown source files. Define page layout, typography, and branding \u2014 the API renders the Markdown into a polished PDF with headers, footers, and page numbers.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "06d7da47-e6a2-45cd-a121-11139c0ad5dc",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Document\nResource: **Document Generation**\n\nConfigure the Document Generation parameters below, then connect your credentials.",
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
      "id": "2eedd640-2bc5-47f0-8380-678535611db0",
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
      "id": "aff89aa7-dcf6-4a26-bc44-b60fc9471099",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Project Proposal\",\n    \"author\": \"Engineering Team\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 12.0,\n      \"line_height\": 1.5,\n      \"color\": \"#1A1A1A\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 20.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 24.0,\n      \"spacing_after_in_pt\": 12.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 12.0,\n        \"line_height\": 1.5,\n        \"color\": \"#1A1A1A\"\n      },\n      \"marker_color\": \"#1A1A1A\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#2B579A\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 12.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 12.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 0.5,\n      \"spacing_before_in_pt\": 24.0,\n      \"spacing_after_in_pt\": 24.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Page {{page_number}}\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Project Proposal\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"## Overview\\n\\nThis proposal outlines the technical approach, timeline, and resource requirements for the **Platform Modernization** initiative.\\n\\n## Goals\\n\\n- Migrate the monolithic backend to a **microservices architecture**\\n- Reduce average API response time from 420ms to under 100ms\\n- Achieve **99.95% uptime** SLA for all customer-facing endpoints\\n- Implement automated canary deployments across all services\\n\\n## Timeline\\n\\n**Phase 1 \\u2014 Foundation (Weeks 1\\u20134)**\\nService mesh setup, CI/CD pipeline migration, and observability instrumentation.\\n\\n**Phase 2 \\u2014 Migration (Weeks 5\\u201312)**\\nIncremental extraction of domain services from the monolith, starting with authentication and billing.\\n\\n**Phase 3 \\u2014 Optimization (Weeks 13\\u201316)**\\nPerformance tuning, load testing, and SLA validation.\\n\\n## Budget\\n\\nEstimated total: **$284,000** across infrastructure, tooling, and contractor hours.\"\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "97142777-c40c-4226-a4cb-ee504821878f",
      "name": "Generate Document",
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
            "node": "Generate Document",
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
Generate a styled PDF from the following markdown content. Use the generate_document tool with format "pdf", providing the [markdown content] as the document body. Configure page size, margins, and typography styles as needed.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "JVBERi0xLjQK...",
    "mime_type": "application/pdf"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
