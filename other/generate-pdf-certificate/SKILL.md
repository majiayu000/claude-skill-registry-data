---
name: generate-pdf-certificate
description: Generate a professional achievement certificate with recipient name, course details, date, and a QR code for formal download or print.
---

# Generate PDF Certificate

Online learning platforms and corporate training departments use this recipe to generate a completion certificate on demand. Define the recipient name, course title, completion date, and a QR code linking to a verification page — producing a landscape PDF ready for formal download or print.

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
        "title": "Certificate of Completion - Advanced Data Engineering",
        "author": "Horizon Academy"
      },
      "page": {
        "size": {
            "width_in_pt": 842,
            "height_in_pt": 595,
        },
        "margins": {
          "top_in_pt": 60,
          "right_in_pt": 72,
          "bottom_in_pt": 60,
          "left_in_pt": 72
        }
      },
      "styles": {
        "text": {
          "font_family": "Helvetica",
          "font_size_in_pt": 11.0,
          "line_height": 1.5,
          "color": "#333333"
        },
        "headline": {
          "font_family": "Helvetica",
          "font_size_in_pt": 24.0,
          "color": "#111111",
          "spacing_before_in_pt": 12.0,
          "spacing_after_in_pt": 6.0,
          "font_weight": "bold"
        },
        "link": {
          "color": "#0066CC",
          "is_underlined": true
        },
        "list": {
          "text_style": {
            "font_family": "Helvetica",
            "font_size_in_pt": 11.0,
            "line_height": 1.5,
            "color": "#333333"
          },
          "marker_color": "#333333",
          "marker_gap_in_pt": 8.0
        },
        "table": {
          "header": {
            "background_color": "#333333",
            "text_color": "#FFFFFF",
            "font_size_in_pt": 11.0,
            "font_weight": "bold"
          },
          "body": {
            "background_color": "#FFFFFF",
            "text_color": "#333333",
            "font_size_in_pt": 11.0
          },
          "border": {
            "outer": {
              "top": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "right": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "bottom": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "left": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              }
            },
            "inner": {
              "horizontal": {
                "color": "#EEEEEE",
                "width_in_pt": 0.5
              },
              "vertical": {
                "color": "#EEEEEE",
                "width_in_pt": 0.5
              }
            }
          }
        },
        "grid": {
          "background_color": "#FFFFFF",
          "border_color": "#CCCCCC",
          "border_width_in_pt": 0.0,
          "gap_in_pt": 12.0
        },
        "separator": {
          "color": "#CCCCCC",
          "thickness_in_pt": 1.0,
          "spacing_before_in_pt": 12.0,
          "spacing_after_in_pt": 12.0
        },
        "image": {
          "border_color": "#000000",
          "border_width_in_pt": 0.0
        }
      },
      "content": [
        {
            "type": "headline",
            "level": "h3",
            "text": "HORIZON ACADEMY",
        },
        { "type": "separator" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Certificate of Completion",
        },
        { "type": "paragraph", "runs": [{ "text": "This certificate is proudly presented to" }] },
        {
            "type": "headline",
            "level": "h1",
            "text": "James Whitfield",
        },
        { "type": "paragraph", "runs": [{ "text": "for successfully completing the course" }] },
        {
            "type": "headline",
            "level": "h2",
            "text": "Advanced Data Engineering with Apache Spark",
        },
        {
            "type": "paragraph",
            "markdown": "Completed on **March 1,
            2026** with a score of **94%** after 42 hours of coursework covering distributed data processing,
            pipeline orchestration,
            and performance optimization.",
        },
        { "type": "separator" },
        { "type": "grid", "columns": [
          { "column_span": 4, "blocks": [
            { "type": "paragraph", "runs": [{
                "text": "Certificate ID",
                "font_weight": "bold",
            }] },
            { "type": "paragraph", "runs": [{ "text": "CERT-2026-ADE-07284" }] }
          ]},
          { "column_span": 4, "blocks": [
            { "type": "paragraph", "runs": [{
                "text": "Issued By",
                "font_weight": "bold",
            }] },
            { "type": "paragraph", "runs": [{
                "text": "Dr. Elena Marchetti,
                Program Director",
            }] }
          ]},
          { "column_span": 4, "blocks": [
            {
              "type": "qr-code",
              "value": "https://verify.horizonacademy.com/cert/2026-ADE-07284",
              "width_in_pt": 80,
              "height_in_pt": 80,
              "fg_hex_color": "#000000",
              "bg_hex_color": "#FFFFFF"
            }
          ]}
        ]}
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
      title: "Certificate of Completion - Advanced Data Engineering",
      author: "Horizon Academy",
    },
    page: {
      size: {
        width_in_pt: 842,
        height_in_pt: 595,
      },
      margins: {
        top_in_pt: 60,
        right_in_pt: 72,
        bottom_in_pt: 60,
        left_in_pt: 72,
      },
    },
    styles: {
      text: {
        font_family: "Helvetica",
        font_size_in_pt: 11.0,
        line_height: 1.5,
        color: "#333333",
      },
      headline: {
        font_family: "Helvetica",
        font_size_in_pt: 24.0,
        color: "#111111",
        spacing_before_in_pt: 12.0,
        spacing_after_in_pt: 6.0,
        font_weight: "bold",
      },
      link: {
        color: "#0066CC",
        is_underlined: true,
      },
      list: {
        text_style: {
          font_family: "Helvetica",
          font_size_in_pt: 11.0,
          line_height: 1.5,
          color: "#333333",
        },
        marker_color: "#333333",
        marker_gap_in_pt: 8.0,
      },
      table: {
        header: {
          background_color: "#333333",
          text_color: "#FFFFFF",
          font_size_in_pt: 11.0,
          font_weight: "bold",
        },
        body: {
          background_color: "#FFFFFF",
          text_color: "#333333",
          font_size_in_pt: 11.0,
        },
        border: {
          outer: {
            top: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            right: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            bottom: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            left: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
          },
          inner: {
            horizontal: {
              color: "#EEEEEE",
              width_in_pt: 0.5,
            },
            vertical: {
              color: "#EEEEEE",
              width_in_pt: 0.5,
            },
          },
        },
      },
      grid: {
        background_color: "#FFFFFF",
        border_color: "#CCCCCC",
        border_width_in_pt: 0.0,
        gap_in_pt: 12.0,
      },
      separator: {
        color: "#CCCCCC",
        thickness_in_pt: 1.0,
        spacing_before_in_pt: 12.0,
        spacing_after_in_pt: 12.0,
      },
      image: {
        border_color: "#000000",
        border_width_in_pt: 0.0,
      },
    },
    content: [
      {
          type: "headline",
          level: "h3",
          text: "HORIZON ACADEMY",
      },
      { type: "separator" },
      {
          type: "headline",
          level: "h1",
          text: "Certificate of Completion",
      },
      { type: "paragraph", runs: [{ text: "This certificate is proudly presented to" }] },
      {
          type: "headline",
          level: "h1",
          text: "James Whitfield",
      },
      { type: "paragraph", runs: [{ text: "for successfully completing the course" }] },
      {
          type: "headline",
          level: "h2",
          text: "Advanced Data Engineering with Apache Spark",
      },
      {
          type: "paragraph",
          markdown: "Completed on **March 1,
          2026** with a score of **94%** after 42 hours of coursework covering distributed data processing,
          pipeline orchestration,
          and performance optimization.",
      },
      { type: "separator" },
      { type: "grid", columns: [
        { column_span: 4, blocks: [
          { type: "paragraph", runs: [{
              text: "Certificate ID",
              font_weight: "bold",
          }] },
          { type: "paragraph", runs: [{ text: "CERT-2026-ADE-07284" }] },
        ]},
        { column_span: 4, blocks: [
          { type: "paragraph", runs: [{
              text: "Issued By",
              font_weight: "bold",
          }] },
          { type: "paragraph", runs: [{
              text: "Dr. Elena Marchetti,
              Program Director",
          }] },
        ]},
        { column_span: 4, blocks: [
          {
            type: "qr-code",
            value: "https://verify.horizonacademy.com/cert/2026-ADE-07284",
            width_in_pt: 80,
            height_in_pt: 80,
            fg_hex_color: "#000000",
            bg_hex_color: "#FFFFFF",
          },
        ]},
      ]},
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
            "title": "Certificate of Completion - Advanced Data Engineering",
            "author": "Horizon Academy",
        },
        "page": {
            "size": {
                "width_in_pt": 842,
                "height_in_pt": 595,
            },
            "margins": {
                "top_in_pt": 60,
                "right_in_pt": 72,
                "bottom_in_pt": 60,
                "left_in_pt": 72,
            },
        },
        "styles": {
            "text": {
                "font_family": "Helvetica",
                "font_size_in_pt": 11.0,
                "line_height": 1.5,
                "color": "#333333",
            },
            "headline": {
                "font_family": "Helvetica",
                "font_size_in_pt": 24.0,
                "color": "#111111",
                "spacing_before_in_pt": 12.0,
                "spacing_after_in_pt": 6.0,
                "font_weight": "bold",
            },
            "link": {
                "color": "#0066CC",
                "is_underlined": True,
            },
            "list": {
                "text_style": {
                    "font_family": "Helvetica",
                    "font_size_in_pt": 11.0,
                    "line_height": 1.5,
                    "color": "#333333",
                },
                "marker_color": "#333333",
                "marker_gap_in_pt": 8.0,
            },
            "table": {
                "header": {
                    "background_color": "#333333",
                    "text_color": "#FFFFFF",
                    "font_size_in_pt": 11.0,
                    "font_weight": "bold",
                },
                "body": {
                    "background_color": "#FFFFFF",
                    "text_color": "#333333",
                    "font_size_in_pt": 11.0,
                },
                "border": {
                    "outer": {
                        "top": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "right": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "bottom": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "left": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                    },
                    "inner": {
                        "horizontal": {
                            "color": "#EEEEEE",
                            "width_in_pt": 0.5,
                        },
                        "vertical": {
                            "color": "#EEEEEE",
                            "width_in_pt": 0.5,
                        },
                    },
                },
            },
            "grid": {
                "background_color": "#FFFFFF",
                "border_color": "#CCCCCC",
                "border_width_in_pt": 0.0,
                "gap_in_pt": 12.0,
            },
            "separator": {
                "color": "#CCCCCC",
                "thickness_in_pt": 1.0,
                "spacing_before_in_pt": 12.0,
                "spacing_after_in_pt": 12.0,
            },
            "image": {
                "border_color": "#000000",
                "border_width_in_pt": 0.0,
            },
        },
        "content": [
            {
                "type": "headline",
                "level": "h3",
                "text": "HORIZON ACADEMY",
            },
            {"type": "separator"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Certificate of Completion",
            },
            {"type": "paragraph", "runs": [{"text": "This certificate is proudly presented to"}]},
            {
                "type": "headline",
                "level": "h1",
                "text": "James Whitfield",
            },
            {"type": "paragraph", "runs": [{"text": "for successfully completing the course"}]},
            {
                "type": "headline",
                "level": "h2",
                "text": "Advanced Data Engineering with Apache Spark",
            },
            {
                "type": "paragraph",
                "markdown": "Completed on **March 1,
                2026** with a score of **94%** after 42 hours of coursework covering distributed data processing,
                pipeline orchestration,
                and performance optimization.",
            },
            {"type": "separator"},
            {"type": "grid", "columns": [
                {"column_span": 4, "blocks": [
                    {"type": "paragraph", "runs": [{
                        "text": "Certificate ID",
                        "font_weight": "bold",
                    }]},
                    {"type": "paragraph", "runs": [{"text": "CERT-2026-ADE-07284"}]},
                ]},
                {"column_span": 4, "blocks": [
                    {"type": "paragraph", "runs": [{
                        "text": "Issued By",
                        "font_weight": "bold",
                    }]},
                    {"type": "paragraph", "runs": [{
                        "text": "Dr. Elena Marchetti,
                        Program Director",
                    }]},
                ]},
                {"column_span": 4, "blocks": [
                    {
                        "type": "qr-code",
                        "value": "https://verify.horizonacademy.com/cert/2026-ADE-07284",
                        "width_in_pt": 80,
                        "height_in_pt": 80,
                        "fg_hex_color": "#000000",
                        "bg_hex_color": "#FFFFFF",
                    },
                ]},
            ]},
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
				Title:  "Certificate of Completion - Advanced Data Engineering",
				Author: "Horizon Academy",
			},
			Page: il.PageConfig{
				Size:    il.PageSize{
      WidthInPt: 842,
      HeightInPt: 595,
    },
				Margins: il.Margins{
      TopInPt: 60,
      RightInPt: 72,
      BottomInPt: 60,
      LeftInPt: 72,
    },
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h3", "HORIZON ACADEMY"),
				il.NewSeparatorBlock(),
				il.NewHeadlineBlock("h1", "Certificate of Completion"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "This certificate is proudly presented to",
    },
				il.NewHeadlineBlock("h1", "James Whitfield"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "for successfully completing the course",
    },
				il.NewHeadlineBlock("h2", "Advanced Data Engineering with Apache Spark"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "Completed on **March 1,
      2026** with a score of **94%** after 42 hours of coursework.",
    },
				il.NewSeparatorBlock(),
				il.NewDocumentQrCodeBlock("https://verify.horizonacademy.com/cert/2026-ADE-07284", 80, 80),
			},
		},
	})
	if err != nil {
		panic(err)
	}

}
```

```n8n
{
  "name": "Generate PDF Certificate",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate PDF Certificate\n\nOnline learning platforms and corporate training departments use this recipe to generate a completion certificate on demand. Define the recipient name, course title, completion date, and a QR code linking to a verification page \u2014 producing a landscape PDF ready for formal download or print.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "9de906d3-89ac-4cf1-bd8e-f5952694e6d0",
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
      "id": "d592b491-e86f-4152-955f-4287a2ff40c0",
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
      "id": "1e88b559-d5e6-4613-b143-5a1aa9412f15",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Certificate of Completion - Advanced Data Engineering\",\n    \"author\": \"Horizon Academy\"\n  },\n  \"page\": {\n    \"size\": {\n      \"width_in_pt\": 842,\n      \"height_in_pt\": 595\n    },\n    \"margins\": {\n      \"top_in_pt\": 60,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 60,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h3\",\n      \"text\": \"HORIZON ACADEMY\"\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Certificate of Completion\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"This certificate is proudly presented to\"\n        }\n      ]\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"James Whitfield\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"for successfully completing the course\"\n        }\n      ]\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h2\",\n      \"text\": \"Advanced Data Engineering with Apache Spark\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Completed on **March 1,\\n            2026** with a score of **94%** after 42 hours of coursework covering distributed data processing,\\n            pipeline orchestration,\\n            and performance optimization.\"\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Certificate ID\",\n                  \"font_weight\": \"bold\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"CERT-2026-ADE-07284\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Issued By\",\n                  \"font_weight\": \"bold\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Dr. Elena Marchetti,\\n                Program Director\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"qr-code\",\n              \"value\": \"https://verify.horizonacademy.com/cert/2026-ADE-07284\",\n              \"width_in_pt\": 80,\n              \"height_in_pt\": 80,\n              \"fg_hex_color\": \"#000000\",\n              \"bg_hex_color\": \"#FFFFFF\"\n            }\n          ]\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "a859a86f-0bbc-4716-a641-32decccea99f",
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
Generate a PDF certificate of completion. Use the generate_document tool with format "pdf" in landscape orientation and these content blocks:

- Headline: "Certificate of Achievement"
- Paragraph: "This certifies that"
- Headline: [recipient name] in large text
- Paragraph: "has successfully completed"
- Headline: [course title]
- Paragraph: completion date — [date]
- Barcode: QR code linking to [verification URL]
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "JVBERi0xLjcKMSAwIG9iago8...",
    "mime_type": "application/pdf"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
