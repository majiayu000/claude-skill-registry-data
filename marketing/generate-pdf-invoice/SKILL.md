---
name: generate-pdf-invoice
description: Generate a professional PDF invoice with company branding, line items, and totals.
---

# Generate PDF Invoice

Finance teams and SaaS platforms use this recipe to generate a branded PDF invoice on demand. Define your company header, billing details, line items, and totals — ready to email or archive as part of your billing workflow.

## APIs Used

Document Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation

prompt


```bash
curl -X POST https://api.iterationlayer.com/document-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "document": {
      "metadata": {
        "title": "Invoice #2026-0142",
        "author": "Nordlicht Consulting GmbH"
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
            "text": "Nordlicht Consulting GmbH · 742 Evergreen Terrace, Suite 300, Austin, TX 78701 · acme-consulting.com"
          }]
        }
      ],
      "content": [
        {
          "type": "grid",
          "columns": [
            {
              "column_span": 6,
              "blocks": [
                {
                    "type": "headline",
                    "level": "h1",
                    "text": "Nordlicht Consulting GmbH",
                },
                { "type": "paragraph", "runs": [{
                    "text": "742 Evergreen Terrace,
                    Suite 300\nAustin,
                    TX 78701\nhello@acme-consulting.com",
                }] }
              ]
            },
            {
              "column_span": 6,
              "blocks": [
                {
                    "type": "headline",
                    "level": "h2",
                    "text": "INVOICE",
                },
                { "type": "paragraph", "runs": [
                  {
                      "text": "Invoice #: ",
                      "font_weight": "bold",
                  },
                  { "text": "2026-0142\n" },
                  {
                      "text": "Date: ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "March 1,
                      2026\n",
                  },
                  {
                      "text": "Due Date: ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "March 31,
                      2026",
                  }
                ] }
              ]
            }
          ]
        },
        { "type": "separator" },
        {
            "type": "headline",
            "level": "h3",
            "text": "Bill To",
        },
        { "type": "paragraph", "runs": [
          {
              "text": "Northwind Industries\n",
              "font_weight": "bold",
          },
          {
              "text": "Attn: Sarah Chen,
              VP of Operations\n1200 Industrial Blvd,
              Denver,
              CO 80202\nsarah.chen@northwind.com",
          }
        ] },
        { "type": "separator" },
        {
          "type": "table",
          "column_widths_in_percent": [40, 15, 20, 25],
          "header": {
            "cells": [
              { "text": "Description" },
              {
                  "text": "Qty",
                  "horizontal_alignment": "center",
              },
              {
                  "text": "Unit Price",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "Amount",
                  "horizontal_alignment": "right",
              }
            ]
          },
          "rows": [
            { "cells": [
              { "text": "Brand Strategy Workshop (2 days)" },
              {
                  "text": "1",
                  "horizontal_alignment": "center",
              },
              {
                  "text": "EUR 8,
                  500.00",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 8,
                  500.00",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "UI/UX Design Sprint (5 days)" },
              {
                  "text": "1",
                  "horizontal_alignment": "center",
              },
              {
                  "text": "EUR 15,
                  000.00",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 15,
                  000.00",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "Frontend Development" },
              {
                  "text": "120",
                  "horizontal_alignment": "center",
              },
              {
                  "text": "EUR 175.00",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 21,
                  000.00",
                  "horizontal_alignment": "right",
              }
            ] },
            { "cells": [
              { "text": "QA & User Acceptance Testing" },
              {
                  "text": "40",
                  "horizontal_alignment": "center",
              },
              {
                  "text": "EUR 150.00",
                  "horizontal_alignment": "right",
              },
              {
                  "text": "EUR 6,
                  000.00",
                  "horizontal_alignment": "right",
              }
            ] }
          ]
        },
        { "type": "separator" },
        {
          "type": "grid",
          "columns": [
            {
                "column_span": 6,
                "blocks": [],
            },
            {
              "column_span": 6,
              "blocks": [
                { "type": "paragraph", "runs": [
                  {
                      "text": "Subtotal: ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "EUR 50,
                      500.00\n",
                  },
                  {
                      "text": "Tax (8.25%): ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "EUR 4,
                      166.25\n",
                  },
                  {
                      "text": "Total Due: ",
                      "font_weight": "bold",
                  },
                  {
                      "text": "EUR 54,
                      666.25",
                  }
                ] }
              ]
            }
          ]
        },
        { "type": "separator" },
        { "type": "paragraph", "runs": [
          {
              "text": "Payment Terms: ",
              "font_weight": "bold",
          },
          {
              "text": "Net 30. Please remit payment via wire transfer to Nordlicht Consulting GmbH,
              Account #4821-7390-5512,
              Routing #021000021.",
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
      title: "Invoice #2026-0142",
      author: "Nordlicht Consulting GmbH",
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
          text: "Nordlicht Consulting GmbH · 742 Evergreen Terrace, Suite 300, Austin, TX 78701 · acme-consulting.com",
        }],
      },
    ],
    content: [
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [
              {
                  type: "headline",
                  level: "h1",
                  text: "Nordlicht Consulting GmbH",
              },
              { type: "paragraph", runs: [{
                  text: "742 Evergreen Terrace,
                  Suite 300\nAustin,
                  TX 78701\nhello@acme-consulting.com",
              }] },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                  type: "headline",
                  level: "h2",
                  text: "INVOICE",
              },
              { type: "paragraph", runs: [
                {
                    text: "Invoice #: ",
                    font_weight: "bold",
                },
                { text: "2026-0142\n" },
                {
                    text: "Date: ",
                    font_weight: "bold",
                },
                {
                    text: "March 1,
                    2026\n",
                },
                {
                    text: "Due Date: ",
                    font_weight: "bold",
                },
                {
                    text: "March 31,
                    2026",
                },
              ] },
            ],
          },
        ],
      },
      { type: "separator" },
      {
          type: "headline",
          level: "h3",
          text: "Bill To",
      },
      { type: "paragraph", runs: [
        {
            text: "Northwind Industries\n",
            font_weight: "bold",
        },
        {
            text: "Attn: Sarah Chen,
            VP of Operations\n1200 Industrial Blvd,
            Denver,
            CO 80202\nsarah.chen@northwind.com",
        },
      ] },
      { type: "separator" },
      {
        type: "table",
        column_widths_in_percent: [40, 15, 20, 25],
        header: {
          cells: [
            { text: "Description" },
            {
                text: "Qty",
                horizontal_alignment: "center",
            },
            {
                text: "Unit Price",
                horizontal_alignment: "right",
            },
            {
                text: "Amount",
                horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          { cells: [
            { text: "Brand Strategy Workshop (2 days)" },
            {
                text: "1",
                horizontal_alignment: "center",
            },
            {
                text: "EUR 8,
                500.00",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 8,
                500.00",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "UI/UX Design Sprint (5 days)" },
            {
                text: "1",
                horizontal_alignment: "center",
            },
            {
                text: "EUR 15,
                000.00",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 15,
                000.00",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "Frontend Development" },
            {
                text: "120",
                horizontal_alignment: "center",
            },
            {
                text: "EUR 175.00",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 21,
                000.00",
                horizontal_alignment: "right",
            },
          ] },
          { cells: [
            { text: "QA & User Acceptance Testing" },
            {
                text: "40",
                horizontal_alignment: "center",
            },
            {
                text: "EUR 150.00",
                horizontal_alignment: "right",
            },
            {
                text: "EUR 6,
                000.00",
                horizontal_alignment: "right",
            },
          ] },
        ],
      },
      { type: "separator" },
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [],
          },
          {
            column_span: 6,
            blocks: [
              { type: "paragraph", runs: [
                {
                    text: "Subtotal: ",
                    font_weight: "bold",
                },
                {
                    text: "EUR 50,
                    500.00\n",
                },
                {
                    text: "Tax (8.25%): ",
                    font_weight: "bold",
                },
                {
                    text: "EUR 4,
                    166.25\n",
                },
                {
                    text: "Total Due: ",
                    font_weight: "bold",
                },
                {
                    text: "EUR 54,
                    666.25",
                },
              ] },
            ],
          },
        ],
      },
      { type: "separator" },
      { type: "paragraph", runs: [
        {
            text: "Payment Terms: ",
            font_weight: "bold",
        },
        {
            text: "Net 30. Please remit payment via wire transfer to Nordlicht Consulting GmbH,
            Account #4821-7390-5512,
            Routing #021000021.",
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
            "title": "Invoice #2026-0142",
            "author": "Nordlicht Consulting GmbH",
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
                    "text": "Nordlicht Consulting GmbH · 742 Evergreen Terrace, Suite 300, Austin, TX 78701 · acme-consulting.com",
                }],
            },
        ],
        "content": [
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "headline",
                                "level": "h1",
                                "text": "Nordlicht Consulting GmbH",
                            },
                            {"type": "paragraph", "runs": [{
                                "text": "742 Evergreen Terrace,
                                Suite 300\nAustin,
                                TX 78701\nhello@acme-consulting.com",
                            }]},
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "headline",
                                "level": "h2",
                                "text": "INVOICE",
                            },
                            {"type": "paragraph", "runs": [
                                {
                                    "text": "Invoice #: ",
                                    "font_weight": "bold",
                                },
                                {"text": "2026-0142\n"},
                                {
                                    "text": "Date: ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "March 1,
                                    2026\n",
                                },
                                {
                                    "text": "Due Date: ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "March 31,
                                    2026",
                                },
                            ]},
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "headline",
                "level": "h3",
                "text": "Bill To",
            },
            {"type": "paragraph", "runs": [
                {
                    "text": "Northwind Industries\n",
                    "font_weight": "bold",
                },
                {
                    "text": "Attn: Sarah Chen,
                    VP of Operations\n1200 Industrial Blvd,
                    Denver,
                    CO 80202\nsarah.chen@northwind.com",
                },
            ]},
            {"type": "separator"},
            {
                "type": "table",
                "column_widths_in_percent": [40, 15, 20, 25],
                "header": {
                    "cells": [
                        {"text": "Description"},
                        {
                            "text": "Qty",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "Unit Price",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "Amount",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {"cells": [
                        {"text": "Brand Strategy Workshop (2 days)"},
                        {
                            "text": "1",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "EUR 8,
                            500.00",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 8,
                            500.00",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "UI/UX Design Sprint (5 days)"},
                        {
                            "text": "1",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "EUR 15,
                            000.00",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 15,
                            000.00",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "Frontend Development"},
                        {
                            "text": "120",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "EUR 175.00",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 21,
                            000.00",
                            "horizontal_alignment": "right",
                        },
                    ]},
                    {"cells": [
                        {"text": "QA & User Acceptance Testing"},
                        {
                            "text": "40",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "EUR 150.00",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "EUR 6,
                            000.00",
                            "horizontal_alignment": "right",
                        },
                    ]},
                ],
            },
            {"type": "separator"},
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {"type": "paragraph", "runs": [
                                {
                                    "text": "Subtotal: ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "EUR 50,
                                    500.00\n",
                                },
                                {
                                    "text": "Tax (8.25%): ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "EUR 4,
                                    166.25\n",
                                },
                                {
                                    "text": "Total Due: ",
                                    "font_weight": "bold",
                                },
                                {
                                    "text": "EUR 54,
                                    666.25",
                                },
                            ]},
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {"type": "paragraph", "runs": [
                {
                    "text": "Payment Terms: ",
                    "font_weight": "bold",
                },
                {
                    "text": "Net 30. Please remit payment via wire transfer to Nordlicht Consulting GmbH,
                    Account #4821-7390-5512,
                    Routing #021000021.",
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
				Title:  "Invoice #2026-0142",
				Author: "Nordlicht Consulting GmbH",
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
				il.NewHeadlineBlock("h1", "Nordlicht Consulting GmbH"),
				il.NewSeparatorBlock(),
				il.NewHeadlineBlock("h3", "Bill To"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "**Northwind Industries**\nAttn: Sarah Chen,
      VP of Operations",
    },
				il.NewSeparatorBlock(),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{{Text: "Brand Strategy Workshop (2 days)"}, {
       Text: "EUR 8,
       500.00",
     }}},
					{Cells: []il.TableCell{{Text: "UI/UX Design Sprint (5 days)"}, {
       Text: "EUR 15,
       000.00",
     }}},
					{Cells: []il.TableCell{{Text: "Frontend Development"}, {
       Text: "EUR 21,
       000.00",
     }}},
					{Cells: []il.TableCell{{Text: "QA & User Acceptance Testing"}, {
       Text: "EUR 6,
       000.00",
     }}},
				}),
				il.NewSeparatorBlock(),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "**Total Due:** EUR 54,
      666.25",
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
  "name": "Generate PDF Invoice",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate PDF Invoice\n\nFinance teams and SaaS platforms use this recipe to generate a branded PDF invoice on demand. Define your company header, billing details, line items, and totals \u2014 ready to email or archive as part of your billing workflow.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "0cd9abf1-a462-4f97-990e-f7d563bf2e39",
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
      "id": "076a7637-e187-4d69-8cc0-ff431718106a",
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
      "id": "526643d6-8e87-4847-ad00-dbebcbd0974b",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Invoice #2026-0142\",\n    \"author\": \"Nordlicht Consulting GmbH\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Nordlicht Consulting GmbH \\u00b7 742 Evergreen Terrace, Suite 300, Austin, TX 78701 \\u00b7 acme-consulting.com\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"headline\",\n              \"level\": \"h1\",\n              \"text\": \"Nordlicht Consulting GmbH\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"742 Evergreen Terrace,\\n                    Suite 300\\nAustin,\\n                    TX 78701\\nhello@acme-consulting.com\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"headline\",\n              \"level\": \"h2\",\n              \"text\": \"INVOICE\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Invoice #: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"2026-0142\\n\"\n                },\n                {\n                  \"text\": \"Date: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"March 1,\\n                      2026\\n\"\n                },\n                {\n                  \"text\": \"Due Date: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"March 31,\\n                      2026\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h3\",\n      \"text\": \"Bill To\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Northwind Industries\\n\",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"Attn: Sarah Chen,\\n              VP of Operations\\n1200 Industrial Blvd,\\n              Denver,\\n              CO 80202\\nsarah.chen@northwind.com\"\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        40,\n        15,\n        20,\n        25\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Description\"\n          },\n          {\n            \"text\": \"Qty\",\n            \"horizontal_alignment\": \"center\"\n          },\n          {\n            \"text\": \"Unit Price\",\n            \"horizontal_alignment\": \"right\"\n          },\n          {\n            \"text\": \"Amount\",\n            \"horizontal_alignment\": \"right\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Brand Strategy Workshop (2 days)\"\n            },\n            {\n              \"text\": \"1\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"EUR 8,\\n                  500.00\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 8,\\n                  500.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"UI/UX Design Sprint (5 days)\"\n            },\n            {\n              \"text\": \"1\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"EUR 15,\\n                  000.00\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 15,\\n                  000.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Frontend Development\"\n            },\n            {\n              \"text\": \"120\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"EUR 175.00\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 21,\\n                  000.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"QA & User Acceptance Testing\"\n            },\n            {\n              \"text\": \"40\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"EUR 150.00\",\n              \"horizontal_alignment\": \"right\"\n            },\n            {\n              \"text\": \"EUR 6,\\n                  000.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 6,\n          \"blocks\": []\n        },\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Subtotal: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"EUR 50,\\n                      500.00\\n\"\n                },\n                {\n                  \"text\": \"Tax (8.25%): \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"EUR 4,\\n                      166.25\\n\"\n                },\n                {\n                  \"text\": \"Total Due: \",\n                  \"font_weight\": \"bold\"\n                },\n                {\n                  \"text\": \"EUR 54,\\n                      666.25\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Payment Terms: \",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"Net 30. Please remit payment via wire transfer to Nordlicht Consulting GmbH,\\n              Account #4821-7390-5512,\\n              Routing #021000021.\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "81ae40b1-d94f-4fe1-89d5-799c16b51eb8",
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
Generate a PDF invoice for [customer name]. Use the generate_document tool with format "pdf" and these content blocks:

- Headline: [company name]
- Paragraph: company address and contact info
- Headline: Invoice details with invoice number, date, and due date
- Table: line items with columns for description, quantity, unit price, and amount
- Paragraph: subtotal, tax, and total due
- Paragraph: payment terms and bank details
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
