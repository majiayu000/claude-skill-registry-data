---
name: generate-packing-slip
description: Generate a packing slip PDF with order details, item list, and shipping address.
---

# Generate Packing Slip

Fulfillment centers and e-commerce platforms generate packing slips with order number, shipping address, and itemized contents — ready for printing and including in shipments.

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
        "title": "Packing Slip - Order #WH-88421",
        "author": "Summit Outdoor Gear"
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
      "footer": [
        {
          "type": "paragraph",
          "runs": [{
            "text": "Summit Outdoor Gear · 1200 Warehouse Pkwy, Denver, CO 80216 · summitoutdoorgear.com"
          }]
        }
      ],
      "content": [
        {
            "type": "headline",
            "level": "h1",
            "text": "Packing Slip",
        },
        {
          "type": "grid",
          "columns": [
            {
              "column_span": 4,
              "blocks": [
                { "type": "paragraph", "runs": [
                  {
                      "text": "Order #: ",
                      "font_weight": "bold",
                  },
                  { "text": "WH-88421\n" },
                  {
                      "text": "Date: ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "March 14,
                      2026",
                  }
                ] }
              ]
            },
            {
              "column_span": 4,
              "blocks": [
                { "type": "paragraph", "runs": [
                  {
                      "text": "Ship To:\n",
                      "font_weight": "bold",
                  },
                  {
                      "text": "Jordan Rivera\n4521 Pine Crest Ave\nPortland,
                      OR 97201",
                  }
                ] }
              ]
            },
            {
              "column_span": 4,
              "blocks": [
                { "type": "paragraph", "runs": [
                  {
                      "text": "Shipping Method:\n",
                      "font_weight": "bold",
                  },
                  { "text": "UPS Ground\n" },
                  {
                      "text": "Tracking: ",
                      "font_weight": "bold",
                  },
                  { "text": "1Z999AA10123456784" }
                ] }
              ]
            }
          ]
        },
        { "type": "separator" },
        {
          "type": "table",
          "column_widths_in_percent": [20, 55, 25],
          "header": {
            "cells": [
              { "text": "SKU" },
              { "text": "Item" },
              {
                  "text": "Qty",
                  "horizontal_alignment": "center",
              }
            ]
          },
          "rows": [
            { "cells": [
              { "text": "SOG-TN-440" },
              { "text": "Alpine Pro 4-Person Tent" },
              {
                  "text": "1",
                  "horizontal_alignment": "center",
              }
            ] },
            { "cells": [
              { "text": "SOG-SB-220" },
              { "text": "Down Sleeping Bag (-10°C)" },
              {
                  "text": "2",
                  "horizontal_alignment": "center",
              }
            ] },
            { "cells": [
              { "text": "SOG-MP-115" },
              { "text": "Foam Sleeping Pad (Regular)" },
              {
                  "text": "2",
                  "horizontal_alignment": "center",
              }
            ] },
            { "cells": [
              { "text": "SOG-HL-330" },
              { "text": "LED Headlamp (400 Lumens)" },
              {
                  "text": "3",
                  "horizontal_alignment": "center",
              }
            ] }
          ]
        },
        { "type": "separator" },
        { "type": "paragraph", "runs": [
          {
              "text": "Total Items: ",
              "font_weight": "bold",
          },
          {
              "text": "8 · Please verify all items upon receipt. For returns or exchanges,
              visit summitoutdoorgear.com/returns or contact support@summitoutdoorgear.com within 30 days.",
          }
        ] }
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
      title: "Packing Slip - Order #WH-88421",
      author: "Summit Outdoor Gear",
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
    footer: [
      {
        type: "paragraph",
        runs: [{
          text: "Summit Outdoor Gear · 1200 Warehouse Pkwy, Denver, CO 80216 · summitoutdoorgear.com",
        }],
      },
    ],
    content: [
      {
          type: "headline",
          level: "h1",
          text: "Packing Slip",
      },
      {
        type: "grid",
        columns: [
          {
            column_span: 4,
            blocks: [
              { type: "paragraph", runs: [
                {
                    text: "Order #: ",
                    font_weight: "bold",
                },
                { text: "WH-88421\n" },
                {
                    text: "Date: ",
                    font_weight: "bold",
                },
                {
                    text: "March 14,
                    2026",
                },
              ] },
            ],
          },
          {
            column_span: 4,
            blocks: [
              { type: "paragraph", runs: [
                {
                    text: "Ship To:\n",
                    font_weight: "bold",
                },
                {
                    text: "Jordan Rivera\n4521 Pine Crest Ave\nPortland,
                    OR 97201",
                },
              ] },
            ],
          },
          {
            column_span: 4,
            blocks: [
              { type: "paragraph", runs: [
                {
                    text: "Shipping Method:\n",
                    font_weight: "bold",
                },
                { text: "UPS Ground\n" },
                {
                    text: "Tracking: ",
                    font_weight: "bold",
                },
                { text: "1Z999AA10123456784" },
              ] },
            ],
          },
        ],
      },
      { type: "separator" },
      {
        type: "table",
        column_widths_in_percent: [20, 55, 25],
        header: {
          cells: [
            { text: "SKU" },
            { text: "Item" },
            {
                text: "Qty",
                horizontal_alignment: "center",
            },
          ],
        },
        rows: [
          { cells: [
            { text: "SOG-TN-440" },
            { text: "Alpine Pro 4-Person Tent" },
            {
                text: "1",
                horizontal_alignment: "center",
            },
          ] },
          { cells: [
            { text: "SOG-SB-220" },
            { text: "Down Sleeping Bag (-10°C)" },
            {
                text: "2",
                horizontal_alignment: "center",
            },
          ] },
          { cells: [
            { text: "SOG-MP-115" },
            { text: "Foam Sleeping Pad (Regular)" },
            {
                text: "2",
                horizontal_alignment: "center",
            },
          ] },
          { cells: [
            { text: "SOG-HL-330" },
            { text: "LED Headlamp (400 Lumens)" },
            {
                text: "3",
                horizontal_alignment: "center",
            },
          ] },
        ],
      },
      { type: "separator" },
      { type: "paragraph", runs: [
        {
            text: "Total Items: ",
            font_weight: "bold",
        },
        {
            text: "8 · Please verify all items upon receipt. For returns or exchanges,
            visit summitoutdoorgear.com/returns or contact support@summitoutdoorgear.com within 30 days.",
        },
      ] },
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
            "title": "Packing Slip - Order #WH-88421",
            "author": "Summit Outdoor Gear",
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
        "footer": [
            {
                "type": "paragraph",
                "runs": [{
                    "text": "Summit Outdoor Gear · 1200 Warehouse Pkwy, Denver, CO 80216 · summitoutdoorgear.com",
                }],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Packing Slip",
            },
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 4,
                        "blocks": [
                            {"type": "paragraph", "runs": [
                                {
                                    "text": "Order #: ",
                                    "font_weight": "bold",
                                },
                                {"text": "WH-88421\n"},
                                {
                                    "text": "Date: ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "March 14,
                                    2026",
                                },
                            ]},
                        ],
                    },
                    {
                        "column_span": 4,
                        "blocks": [
                            {"type": "paragraph", "runs": [
                                {
                                    "text": "Ship To:\n",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "Jordan Rivera\n4521 Pine Crest Ave\nPortland,
                                    OR 97201",
                                },
                            ]},
                        ],
                    },
                    {
                        "column_span": 4,
                        "blocks": [
                            {"type": "paragraph", "runs": [
                                {
                                    "text": "Shipping Method:\n",
                                    "font_weight": "bold",
                                },
                                {"text": "UPS Ground\n"},
                                {
                                    "text": "Tracking: ",
                                    "font_weight": "bold",
                                },
                                {"text": "1Z999AA10123456784"},
                            ]},
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "table",
                "column_widths_in_percent": [20, 55, 25],
                "header": {
                    "cells": [
                        {"text": "SKU"},
                        {"text": "Item"},
                        {
                            "text": "Qty",
                            "horizontal_alignment": "center",
                        },
                    ],
                },
                "rows": [
                    {"cells": [
                        {"text": "SOG-TN-440"},
                        {"text": "Alpine Pro 4-Person Tent"},
                        {
                            "text": "1",
                            "horizontal_alignment": "center",
                        },
                    ]},
                    {"cells": [
                        {"text": "SOG-SB-220"},
                        {"text": "Down Sleeping Bag (-10°C)"},
                        {
                            "text": "2",
                            "horizontal_alignment": "center",
                        },
                    ]},
                    {"cells": [
                        {"text": "SOG-MP-115"},
                        {"text": "Foam Sleeping Pad (Regular)"},
                        {
                            "text": "2",
                            "horizontal_alignment": "center",
                        },
                    ]},
                    {"cells": [
                        {"text": "SOG-HL-330"},
                        {"text": "LED Headlamp (400 Lumens)"},
                        {
                            "text": "3",
                            "horizontal_alignment": "center",
                        },
                    ]},
                ],
            },
            {"type": "separator"},
            {"type": "paragraph", "runs": [
                {
                    "text": "Total Items: ",
                    "font_weight": "bold",
                },
                {
                    "text": "8 · Please verify all items upon receipt. For returns or exchanges,
                    visit summitoutdoorgear.com/returns or contact support@summitoutdoorgear.com within 30 days.",
                },
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
				Title:  "Packing Slip - Order #WH-88421",
				Author: "Summit Outdoor Gear",
			},
			Page: il.PageConfig{
				Size:    il.PageSize{Preset: "A4"},
				Margins: il.Margins{
      TopInPt: 72,
      RightInPt: 72,
      BottomInPt: 72,
      LeftInPt: 72,
    },
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "Packing Slip"),
				il.ParagraphBlock{Type: "paragraph", Runs: []il.TextRun{
					{
       Text: "Order #: ",
       IsBold: true,
     },
					{Text: "WH-88421\n"},
					{
       Text: "Date: ",
       IsBold: true,
     },
					{
       Text: "March 14,
       2026",
     },
				}},
				il.NewSeparatorBlock(),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{{Text: "SOG-TN-440"}, {Text: "Alpine Pro 4-Person Tent"}, {Text: "1"}}},
					{Cells: []il.TableCell{{Text: "SOG-SB-220"}, {Text: "Down Sleeping Bag (-10°C)"}, {Text: "2"}}},
					{Cells: []il.TableCell{{Text: "SOG-MP-115"}, {Text: "Foam Sleeping Pad (Regular)"}, {Text: "2"}}},
					{Cells: []il.TableCell{{Text: "SOG-HL-330"}, {Text: "LED Headlamp (400 Lumens)"}, {Text: "3"}}},
				}),
				il.NewSeparatorBlock(),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "**Total Items:** 8 · Please verify all items upon receipt.",
    },
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
  "name": "Generate Packing Slip",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Packing Slip\n\nFulfillment centers and e-commerce platforms generate packing slips with order number, shipping address, and itemized contents \u2014 ready for printing and including in shipments.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "bdecf206-0601-4338-bfbd-237388b4eec5",
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
      "id": "70cfc140-a7d1-4e5b-a76b-dfa2231eaf6d",
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
      "id": "527e2b3e-ca9a-4e4c-b16f-bfed7b363e0e",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Packing Slip - Order #WH-88421\",\n    \"author\": \"Summit Outdoor Gear\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Summit Outdoor Gear \\u00b7 1200 Warehouse Pkwy, Denver, CO 80216 \\u00b7 summitoutdoorgear.com\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Packing Slip\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Order #: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"WH-88421\\n\"\n                },\n                {\n                  \"text\": \"Date: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"March 14,\\n                      2026\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Ship To:\\n\",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"Jordan Rivera\\n4521 Pine Crest Ave\\nPortland,\\n                      OR 97201\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 4,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Shipping Method:\\n\",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"UPS Ground\\n\"\n                },\n                {\n                  \"text\": \"Tracking: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"1Z999AA10123456784\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        20,\n        55,\n        25\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"SKU\"\n          },\n          {\n            \"text\": \"Item\"\n          },\n          {\n            \"text\": \"Qty\",\n            \"horizontal_alignment\": \"center\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"SOG-TN-440\"\n            },\n            {\n              \"text\": \"Alpine Pro 4-Person Tent\"\n            },\n            {\n              \"text\": \"1\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"SOG-SB-220\"\n            },\n            {\n              \"text\": \"Down Sleeping Bag (-10\\u00b0C)\"\n            },\n            {\n              \"text\": \"2\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"SOG-MP-115\"\n            },\n            {\n              \"text\": \"Foam Sleeping Pad (Regular)\"\n            },\n            {\n              \"text\": \"2\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"SOG-HL-330\"\n            },\n            {\n              \"text\": \"LED Headlamp (400 Lumens)\"\n            },\n            {\n              \"text\": \"3\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Total Items: \",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"8 \\u00b7 Please verify all items upon receipt. For returns or exchanges,\\n              visit summitoutdoorgear.com/returns or contact support@summitoutdoorgear.com within 30 days.\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "a449367c-93b9-4405-b90b-041d34affc4d",
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
Generate a packing slip PDF for order [order number]. Use the generate_document tool with format "pdf" and these content blocks:

- Headline: "Packing Slip"
- Paragraph: order number and order date
- Paragraph: shipping address — [recipient name and address]
- Table: items with columns for SKU, product name, and quantity
- Paragraph: special instructions or notes
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
