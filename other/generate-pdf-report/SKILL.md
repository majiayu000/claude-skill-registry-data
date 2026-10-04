---
name: generate-pdf-report
description: Generate a professional PDF report with title, executive summary, data table, and footer.
---

# Generate PDF Report

Business intelligence teams generate automated PDF reports with summary text, key metrics in a data table, and branded footer — ready for stakeholder distribution.

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
        "title": "Q4 Performance Report",
        "author": "Northwind Analytics"
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
            "text": "Northwind Analytics · Confidential · Generated March 14, 2026"
          }]
        }
      ],
      "content": [
        {
            "type": "headline",
            "level": "h1",
            "text": "Q4 Performance Report",
        },
        { "type": "paragraph", "runs": [
          {
              "text": "Executive Summary: ",
              "font_weight": "bold",
          },
          {
              "text": "Q4 2025 showed strong revenue growth driven by new enterprise contracts and improved retention rates. Total revenue increased 18% quarter-over-quarter,
              while operating costs remained flat. Customer acquisition cost decreased by 12%,
              reflecting improved efficiency in our go-to-market strategy.",
          }
        ] },
        { "type": "separator" },
        {
            "type": "headline",
            "level": "h2",
            "text": "Key Metrics",
        },
        {
          "type": "table",
          "column_widths_in_percent": [40, 20, 20, 20],
          "header": {
            "cells": [
              { "text": "Metric" },
              {
                  "text": "Q3",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "Q4",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "Change",
                  "horizontal_alignment": "right",
              }
            ]
          },
          "rows": [
            { "cells": [
              { "text": "Total Revenue" },
              {
                  "text": "EUR 2.4M",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 2.83M",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "+18%",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "Active Customers" },
              {
                  "text": "1,
                  240",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "1,
                  385",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "+11.7%",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "Churn Rate" },
              {
                  "text": "4.2%",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "3.1%",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "-1.1pp",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "Customer Acquisition Cost" },
              {
                  "text": "EUR 1,
                  850",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 1,
                  628",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "-12%",
                  "horizontal_alignment": "right",
              }
            ] }
          ]
        },
        { "type": "separator" },
        { "type": "paragraph", "runs": [
          {
              "text": "Report generated on March 14,
              2026 by Northwind Analytics. For questions,
              contact analytics@northwind.com.",
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
      title: "Q4 Performance Report",
      author: "Northwind Analytics",
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
          text: "Northwind Analytics · Confidential · Generated March 14, 2026",
        }],
      },
    ],
    content: [
      {
          type: "headline",
          level: "h1",
          text: "Q4 Performance Report",
      },
      { type: "paragraph", runs: [
        {
            text: "Executive Summary: ",
            font_weight: "bold",
        },
        {
            text: "Q4 2025 showed strong revenue growth driven by new enterprise contracts and improved retention rates. Total revenue increased 18% quarter-over-quarter,
            while operating costs remained flat. Customer acquisition cost decreased by 12%,
            reflecting improved efficiency in our go-to-market strategy.",
        },
      ] },
      { type: "separator" },
      {
          type: "headline",
          level: "h2",
          text: "Key Metrics",
      },
      {
        type: "table",
        column_widths_in_percent: [40, 20, 20, 20],
        header: {
          cells: [
            { text: "Metric" },
            {
                text: "Q3",
                horizontal_alignment: "right",
            },
            {
                text: "Q4",
                horizontal_alignment: "right",
            },
            {
                text: "Change",
                horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          { cells: [
            { text: "Total Revenue" },
            {
                text: "EUR 2.4M",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 2.83M",
                horizontal_alignment: "right",
            },
            {
                text: "+18%",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "Active Customers" },
            {
                text: "1,
                240",
                horizontal_alignment: "right",
            },
            {
                text: "1,
                385",
                horizontal_alignment: "right",
            },
            {
                text: "+11.7%",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "Churn Rate" },
            {
                text: "4.2%",
                horizontal_alignment: "right",
            },
            {
                text: "3.1%",
                horizontal_alignment: "right",
            },
            {
                text: "-1.1pp",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "Customer Acquisition Cost" },
            {
                text: "EUR 1,
                850",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 1,
                628",
                horizontal_alignment: "right",
            },
            {
                text: "-12%",
                horizontal_alignment: "right",
            },
          ] },
        ],
      },
      { type: "separator" },
      { type: "paragraph", runs: [
        {
            text: "Report generated on March 14,
            2026 by Northwind Analytics. For questions,
            contact analytics@northwind.com.",
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
            "title": "Q4 Performance Report",
            "author": "Northwind Analytics",
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
                    "text": "Northwind Analytics · Confidential · Generated March 14, 2026",
                }],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Q4 Performance Report",
            },
            {"type": "paragraph", "runs": [
                {
                    "text": "Executive Summary: ",
                    "font_weight": "bold",
                },
                {
                    "text": "Q4 2025 showed strong revenue growth driven by new enterprise contracts and improved retention rates. Total revenue increased 18% quarter-over-quarter,
                    while operating costs remained flat. Customer acquisition cost decreased by 12%,
                    reflecting improved efficiency in our go-to-market strategy.",
                },
            ]},
            {"type": "separator"},
            {
                "type": "headline",
                "level": "h2",
                "text": "Key Metrics",
            },
            {
                "type": "table",
                "column_widths_in_percent": [40, 20, 20, 20],
                "header": {
                    "cells": [
                        {"text": "Metric"},
                        {
                            "text": "Q3",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "Q4",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "Change",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {"cells": [
                        {"text": "Total Revenue"},
                        {
                            "text": "EUR 2.4M",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 2.83M",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "+18%",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "Active Customers"},
                        {
                            "text": "1,
                            240",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "1,
                            385",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "+11.7%",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "Churn Rate"},
                        {
                            "text": "4.2%",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "3.1%",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "-1.1pp",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "Customer Acquisition Cost"},
                        {
                            "text": "EUR 1,
                            850",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 1,
                            628",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "-12%",
                            "horizontal_alignment": "right",
                        },
                    ]},
                ],
            },
            {"type": "separator"},
            {"type": "paragraph", "runs": [
                {
                    "text": "Report generated on March 14,
                    2026 by Northwind Analytics. For questions,
                    contact analytics@northwind.com.",
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
				Title:  "Q4 Performance Report",
				Author: "Northwind Analytics",
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
				il.NewHeadlineBlock("h1", "Q4 Performance Report"),
				il.ParagraphBlock{Type: "paragraph", Runs: []il.TextRun{
					{
       Text: "Executive Summary: ",
       IsBold: true,
     },
					{Text: "Q4 2025 showed strong revenue growth driven by new enterprise contracts and improved retention rates."},
				}},
				il.NewSeparatorBlock(),
				il.NewHeadlineBlock("h2", "Key Metrics"),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{{Text: "Total Revenue"}, {Text: "EUR 2.4M"}, {Text: "EUR 2.83M"}, {Text: "+18%"}}},
					{Cells: []il.TableCell{{Text: "Active Customers"}, {
       Text: "1,
       240",
     }, {
         Text: "1,
         385",
     }, {Text: "+11.7%"}}},
					{Cells: []il.TableCell{{Text: "Churn Rate"}, {Text: "4.2%"}, {Text: "3.1%"}, {Text: "-1.1pp"}}},
					{Cells: []il.TableCell{{Text: "Customer Acquisition Cost"}, {
       Text: "EUR 1,
       850",
     }, {
         Text: "EUR 1,
         628",
     }, {Text: "-12%"}}},
				}),
				il.NewSeparatorBlock(),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "Report generated on March 14,
      2026 by Northwind Analytics.",
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
  "name": "Generate PDF Report",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate PDF Report\n\nBusiness intelligence teams generate automated PDF reports with summary text, key metrics in a data table, and branded footer \u2014 ready for stakeholder distribution.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "cdf55d40-5ee4-4450-a5cd-151cb7b10894",
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
      "id": "993a95ff-51bd-4dcb-84a0-c1e6e74949bf",
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
      "id": "30b39a07-a6ff-4d02-83f4-4e3898aa24ee",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Q4 Performance Report\",\n    \"author\": \"Northwind Analytics\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Northwind Analytics \\u00b7 Confidential \\u00b7 Generated March 14, 2026\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Q4 Performance Report\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Executive Summary: \",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"Q4 2025 showed strong revenue growth driven by new enterprise contracts and improved retention rates. Total revenue increased 18% quarter-over-quarter,\\n              while operating costs remained flat. Customer acquisition cost decreased by 12%,\\n              reflecting improved efficiency in our go-to-market strategy.\"\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h2\",\n      \"text\": \"Key Metrics\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        40,\n        20,\n        20,\n        20\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Metric\"\n          },\n          {\n            \"text\": \"Q3\",\n            \"horizontal_alignment\": \"right\"\n          },\n          {\n            \"text\": \"Q4\",\n            \"horizontal_alignment\": \"right\"\n          },\n          {\n            \"text\": \"Change\",\n            \"horizontal_alignment\": \"right\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Total Revenue\"\n            },\n            {\n              \"text\": \"EUR 2.4M\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 2.83M\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"+18%\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Active Customers\"\n            },\n            {\n              \"text\": \"1,\\n                  240\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"1,\\n                  385\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"+11.7%\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Churn Rate\"\n            },\n            {\n              \"text\": \"4.2%\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"3.1%\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"-1.1pp\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Customer Acquisition Cost\"\n            },\n            {\n              \"text\": \"EUR 1,\\n                  850\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 1,\\n                  628\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"-12%\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Report generated on March 14,\\n              2026 by Northwind Analytics. For questions,\\n              contact analytics@northwind.com.\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "d0ce635c-4465-42ff-9cd6-e956a8e2449b",
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
Generate a PDF report for [report title]. Use the generate_document tool with format "pdf" and these content blocks:

- Headline: [report title]
- Paragraph: executive summary text
- Table: key metrics with columns for metric name, current value, previous value, and change
- Separator
- Paragraph: footer with company name and report date
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
