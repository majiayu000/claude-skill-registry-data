---
name: generate-shipping-label
description: Generate a compact PDF shipping label with sender and recipient addresses, barcode, and tracking number.
---

# Generate Shipping Label

E-commerce platforms and fulfillment centers use this recipe to generate a shipping label on demand. Define sender and recipient addresses in a grid layout with a barcode for scanning — ready to print and attach to an outgoing package.

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
        "title": "Shipping Label - TRK-84729105",
        "author": "Greenfield Fulfillment Co."
      },
      "page": {
        "size": {
          "width_in_pt": 288,
          "height_in_pt": 432
        },
        "margins": {
          "top_in_pt": 18,
          "right_in_pt": 18,
          "bottom_in_pt": 18,
          "left_in_pt": 18
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
          "text": "GREENFIELD FULFILLMENT CO."
        },
        {
          "type": "separator"
        },
        {
          "type": "grid",
          "columns": [
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "FROM:",
                      "font_weight": "bold"
                    }
                  ]
                },
                {
                  "type": "paragraph",
                  "markdown": "Greenfield Fulfillment Co.\n1200 Commerce Blvd, Unit 4\nAustin, TX 78701\nUnited States"
                }
              ]
            },
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "TO:",
                      "font_weight": "bold"
                    }
                  ]
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Maria Vasquez",
                      "font_weight": "bold"
                    },
                    {
                      "text": "\n742 Evergreen Terrace, Apt 3B\nPortland, OR 97205\nUnited States"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "grid",
          "columns": [
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Service: ",
                      "font_weight": "bold"
                    },
                    {
                      "text": "Priority 2-Day"
                    }
                  ]
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Weight: ",
                      "font_weight": "bold"
                    },
                    {
                      "text": "2.4 lbs"
                    }
                  ]
                }
              ]
            },
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Order: ",
                      "font_weight": "bold"
                    },
                    {
                      "text": "GF-2026-48291"
                    }
                  ]
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Date: ",
                      "font_weight": "bold"
                    },
                    {
                      "text": "2026-03-06"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "barcode",
          "value": "TRK84729105204839",
          "format": "code128",
          "width_in_pt": 200,
          "height_in_pt": 60,
          "fg_hex_color": "#000000",
          "bg_hex_color": "#FFFFFF"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Tracking: ",
              "font_weight": "bold"
            },
            {
              "text": "TRK-8472-9105-2048-39"
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

const result = await client.generateDocument({
  format: "pdf",
  document: {
    metadata: {
      title: "Shipping Label - TRK-84729105",
      author: "Greenfield Fulfillment Co.",
    },
    page: {
      size: {
        width_in_pt: 288,
        height_in_pt: 432,
      },
      margins: {
        top_in_pt: 18,
        right_in_pt: 18,
        bottom_in_pt: 18,
        left_in_pt: 18,
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
        text: "GREENFIELD FULFILLMENT CO.",
      },
      { type: "separator" },
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [
                  {
                    text: "FROM:",
                    font_weight: "bold",
                  },
                ],
              },
              {
                type: "paragraph",
                markdown:
                  "Greenfield Fulfillment Co.\n1200 Commerce Blvd, Unit 4\nAustin, TX 78701\nUnited States",
              },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [
                  {
                    text: "TO:",
                    font_weight: "bold",
                  },
                ],
              },
              {
                type: "paragraph",
                runs: [
                  {
                    text: "Maria Vasquez",
                    font_weight: "bold",
                  },
                  {
                    text: "\n742 Evergreen Terrace, Apt 3B\nPortland, OR 97205\nUnited States",
                  },
                ],
              },
            ],
          },
        ],
      },
      { type: "separator" },
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [
                  {
                    text: "Service: ",
                    font_weight: "bold",
                  },
                  { text: "Priority 2-Day" },
                ],
              },
              {
                type: "paragraph",
                runs: [
                  {
                    text: "Weight: ",
                    font_weight: "bold",
                  },
                  { text: "2.4 lbs" },
                ],
              },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [
                  {
                    text: "Order: ",
                    font_weight: "bold",
                  },
                  { text: "GF-2026-48291" },
                ],
              },
              {
                type: "paragraph",
                runs: [
                  {
                    text: "Date: ",
                    font_weight: "bold",
                  },
                  { text: "2026-03-06" },
                ],
              },
            ],
          },
        ],
      },
      { type: "separator" },
      {
        type: "barcode",
        value: "TRK84729105204839",
        format: "code128",
        width_in_pt: 200,
        height_in_pt: 60,
        fg_hex_color: "#000000",
        bg_hex_color: "#FFFFFF",
      },
      {
        type: "paragraph",
        runs: [
          {
            text: "Tracking: ",
            font_weight: "bold",
          },
          { text: "TRK-8472-9105-2048-39" },
        ],
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
            "title": "Shipping Label - TRK-84729105",
            "author": "Greenfield Fulfillment Co.",
        },
        "page": {
            "size": {
                "width_in_pt": 288,
                "height_in_pt": 432,
            },
            "margins": {
                "top_in_pt": 18,
                "right_in_pt": 18,
                "bottom_in_pt": 18,
                "left_in_pt": 18,
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
                "text": "GREENFIELD FULFILLMENT CO.",
            },
            {"type": "separator"},
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "FROM:",
                                        "font_weight": "bold",
                                    },
                                ],
                            },
                            {
                                "type": "paragraph",
                                "markdown": "Greenfield Fulfillment Co.\n1200 Commerce Blvd, Unit 4\nAustin, TX 78701\nUnited States",
                            },
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "TO:",
                                        "font_weight": "bold",
                                    },
                                ],
                            },
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "Maria Vasquez",
                                        "font_weight": "bold",
                                    },
                                    {
                                        "text": "\n742 Evergreen Terrace, Apt 3B\nPortland, OR 97205\nUnited States",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "Service: ",
                                        "font_weight": "bold",
                                    },
                                    {"text": "Priority 2-Day"},
                                ],
                            },
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "Weight: ",
                                        "font_weight": "bold",
                                    },
                                    {"text": "2.4 lbs"},
                                ],
                            },
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "Order: ",
                                        "font_weight": "bold",
                                    },
                                    {"text": "GF-2026-48291"},
                                ],
                            },
                            {
                                "type": "paragraph",
                                "runs": [
                                    {
                                        "text": "Date: ",
                                        "font_weight": "bold",
                                    },
                                    {"text": "2026-03-06"},
                                ],
                            },
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "barcode",
                "value": "TRK84729105204839",
                "format": "code128",
                "width_in_pt": 200,
                "height_in_pt": 60,
                "fg_hex_color": "#000000",
                "bg_hex_color": "#FFFFFF",
            },
            {
                "type": "paragraph",
                "runs": [
                    {
                        "text": "Tracking: ",
                        "font_weight": "bold",
                    },
                    {"text": "TRK-8472-9105-2048-39"},
                ],
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
				Title:  "Shipping Label - TRK-84729105",
				Author: "Greenfield Fulfillment Co.",
			},
			Page: il.DocumentPage{
				Size:    il.DocPageSize{
      WidthInPt: 288,
      HeightInPt: 432,
    },
				Margins: il.DocMargins{
      TopInPt: 18,
      RightInPt: 18,
      BottomInPt: 18,
      LeftInPt: 18,
    },
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h3", "GREENFIELD FULFILLMENT CO."),
				il.NewSeparatorBlock(),
				il.NewGridBlock([]il.GridColumn{
					{ColumnSpan: 6, Blocks: []il.ContentBlock{
						il.NewParagraphBlock(),
					}},
					{ColumnSpan: 6, Blocks: []il.ContentBlock{
						il.NewParagraphBlock(),
					}},
				}),
				il.NewSeparatorBlock(),
				il.NewBarcodeBlock(0, "TRK84729105204839", "code128", "#000000", "#FFFFFF",
					il.Position{},
					il.Dimensions{
       Width: 200,
       Height: 60,
     }),
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
  "name": "Generate Shipping Label",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Shipping Label\n\nE-commerce platforms and fulfillment centers use this recipe to generate a shipping label on demand. Define sender and recipient addresses in a grid layout with a barcode for scanning \u2014 ready to print and attach to an outgoing package.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "86842502-62a3-48d2-9621-9e4852498c89",
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
      "id": "74bf5afb-c939-4012-8c61-fb33b4e72d5c",
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
      "id": "bdc062a7-2c0d-4994-8b2b-c4cd715715e3",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Shipping Label - TRK-84729105\",\n    \"author\": \"Greenfield Fulfillment Co.\"\n  },\n  \"page\": {\n    \"size\": {\n      \"width_in_pt\": 288,\n      \"height_in_pt\": 432\n    },\n    \"margins\": {\n      \"top_in_pt\": 18,\n      \"right_in_pt\": 18,\n      \"bottom_in_pt\": 18,\n      \"left_in_pt\": 18\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h3\",\n      \"text\": \"GREENFIELD FULFILLMENT CO.\"\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"FROM:\",\n                  \"font_weight\": \"bold\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"markdown\": \"Greenfield Fulfillment Co.\\n1200 Commerce Blvd, Unit 4\\nAustin, TX 78701\\nUnited States\"\n            }\n          ]\n        },\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"TO:\",\n                  \"font_weight\": \"bold\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Maria Vasquez\",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"\\n742 Evergreen Terrace, Apt 3B\\nPortland, OR 97205\\nUnited States\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Service: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"Priority 2-Day\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Weight: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"2.4 lbs\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Order: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"GF-2026-48291\"\n                }\n              ]\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Date: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"2026-03-06\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"barcode\",\n      \"value\": \"TRK84729105204839\",\n      \"format\": \"code128\",\n      \"width_in_pt\": 200,\n      \"height_in_pt\": 60,\n      \"fg_hex_color\": \"#000000\",\n      \"bg_hex_color\": \"#FFFFFF\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Tracking: \",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"TRK-8472-9105-2048-39\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "15d21268-02cf-4da2-b765-c6ad06fb1745",
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
Generate a shipping label PDF. Use the generate_document tool with format "pdf" and a compact page size with these content blocks:

- Paragraph: "FROM" with [sender name and address]
- Separator
- Paragraph: "TO" with [recipient name and address] in bold
- Barcode: Code 128 barcode with [tracking number]
- Paragraph: tracking number text and shipping method
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
