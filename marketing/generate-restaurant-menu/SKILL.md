---
name: generate-restaurant-menu
description: Generate a branded restaurant menu PDF with sections, items, prices, and descriptions.
---

# Generate Restaurant Menu

Restaurants and food delivery platforms generate printable menus with categorized sections, item descriptions, and pricing — ready for in-house printing or PDF download.

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
        "title": "The Golden Fork - Menu",
        "author": "The Golden Fork"
      },
      "page": {
        "size": {
          "preset": "A4"
        },
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
          "runs": [
            {
              "text": "The Golden Fork · 88 Harbor Blvd, Berlin, DE 94111 · thegoldenfork.com"
            }
          ]
        }
      ],
      "content": [
        {
          "type": "headline",
          "level": "h1",
          "text": "The Golden Fork"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Fresh, seasonal cuisine crafted with locally sourced ingredients. Please inform your server of any allergies or dietary restrictions."
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "headline",
          "level": "h2",
          "text": "Appetizers"
        },
        {
          "type": "table",
          "column_widths_in_percent": [30, 45, 25],
          "header": {
            "cells": [
              {
                "text": "Item"
              },
              {
                "text": "Description"
              },
              {
                "text": "Price",
                "horizontal_alignment": "right"
              }
            ]
          },
          "rows": [
            {
              "cells": [
                {
                  "text": "Burrata Caprese"
                },
                {
                  "text": "Heirloom tomatoes, fresh burrata, basil oil, aged balsamic"
                },
                {
                  "text": "EUR 16.00",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Tuna Tartare"
                },
                {
                  "text": "Sushi-grade ahi, avocado, sesame, crispy wonton chips"
                },
                {
                  "text": "EUR 19.00",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "French Onion Soup"
                },
                {
                  "text": "Caramelized onion broth, Gruyère crouton"
                },
                {
                  "text": "EUR 14.00",
                  "horizontal_alignment": "right"
                }
              ]
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "headline",
          "level": "h2",
          "text": "Main Courses"
        },
        {
          "type": "table",
          "column_widths_in_percent": [30, 45, 25],
          "header": {
            "cells": [
              {
                "text": "Item"
              },
              {
                "text": "Description"
              },
              {
                "text": "Price",
                "horizontal_alignment": "right"
              }
            ]
          },
          "rows": [
            {
              "cells": [
                {
                  "text": "Pan-Seared Salmon"
                },
                {
                  "text": "Wild-caught salmon, lemon beurre blanc, roasted asparagus, fingerling potatoes"
                },
                {
                  "text": "EUR 34.00",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Filet Mignon"
                },
                {
                  "text": "8oz center-cut, truffle mash, grilled broccolini, red wine jus"
                },
                {
                  "text": "EUR 48.00",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Wild Mushroom Risotto"
                },
                {
                  "text": "Arborio rice, porcini, chanterelle, Parmigiano-Reggiano, truffle oil"
                },
                {
                  "text": "EUR 28.00",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Roasted Half Chicken"
                },
                {
                  "text": "Free-range chicken, herb jus, seasonal vegetables, garlic confit"
                },
                {
                  "text": "EUR 32.00",
                  "horizontal_alignment": "right"
                }
              ]
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Prices exclude tax and gratuity. A 20% gratuity is added for parties of 6 or more."
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
      title: "The Golden Fork - Menu",
      author: "The Golden Fork",
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
        runs: [
          {
            text: "The Golden Fork · 88 Harbor Blvd, Berlin, DE 94111 · thegoldenfork.com",
          },
        ],
      },
    ],
    content: [
      {
        type: "headline",
        level: "h1",
        text: "The Golden Fork",
      },
      {
        type: "paragraph",
        runs: [
          {
              text: "Fresh,
              seasonal cuisine crafted with locally sourced ingredients. Please inform your server of any allergies or dietary restrictions.",
          },
        ],
      },
      { type: "separator" },
      {
        type: "headline",
        level: "h2",
        text: "Appetizers",
      },
      {
        type: "table",
        column_widths_in_percent: [30, 45, 25],
        header: {
          cells: [
            { text: "Item" },
            { text: "Description" },
            {
              text: "Price",
              horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          {
            cells: [
              { text: "Burrata Caprese" },
              {
                  text: "Heirloom tomatoes,
                  fresh burrata,
                  basil oil,
                  aged balsamic",
              },
              {
                text: "EUR 16.00",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Tuna Tartare" },
              {
                  text: "Sushi-grade ahi,
                  avocado,
                  sesame,
                  crispy wonton chips",
              },
              {
                text: "EUR 19.00",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "French Onion Soup" },
              {
                  text: "Caramelized onion broth,
                  Gruyère crouton",
              },
              {
                text: "EUR 14.00",
                horizontal_alignment: "right",
              },
            ],
          },
        ],
      },
      { type: "separator" },
      {
        type: "headline",
        level: "h2",
        text: "Main Courses",
      },
      {
        type: "table",
        column_widths_in_percent: [30, 45, 25],
        header: {
          cells: [
            { text: "Item" },
            { text: "Description" },
            {
              text: "Price",
              horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          {
            cells: [
              { text: "Pan-Seared Salmon" },
              {
                  text: "Wild-caught salmon,
                  lemon beurre blanc,
                  roasted asparagus,
                  fingerling potatoes",
              },
              {
                text: "EUR 34.00",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Filet Mignon" },
              {
                  text: "8oz center-cut,
                  truffle mash,
                  grilled broccolini,
                  red wine jus",
              },
              {
                text: "EUR 48.00",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Wild Mushroom Risotto" },
              {
                  text: "Arborio rice,
                  porcini,
                  chanterelle,
                  Parmigiano-Reggiano,
                  truffle oil",
              },
              {
                text: "EUR 28.00",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Roasted Half Chicken" },
              {
                  text: "Free-range chicken,
                  herb jus,
                  seasonal vegetables,
                  garlic confit",
              },
              {
                text: "EUR 32.00",
                horizontal_alignment: "right",
              },
            ],
          },
        ],
      },
      { type: "separator" },
      {
        type: "paragraph",
        runs: [
          { text: "Prices exclude tax and gratuity. A 20% gratuity is added for parties of 6 or more." },
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
            "title": "The Golden Fork - Menu",
            "author": "The Golden Fork",
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
                "runs": [
                    {
                        "text": "The Golden Fork · 88 Harbor Blvd, Berlin, DE 94111 · thegoldenfork.com",
                    },
                ],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "The Golden Fork",
            },
            {
                "type": "paragraph",
                "runs": [
                    {
                        "text": "Fresh,
                        seasonal cuisine crafted with locally sourced ingredients. Please inform your server of any allergies or dietary restrictions.",
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "headline",
                "level": "h2",
                "text": "Appetizers",
            },
            {
                "type": "table",
                "column_widths_in_percent": [30, 45, 25],
                "header": {
                    "cells": [
                        {"text": "Item"},
                        {"text": "Description"},
                        {
                            "text": "Price",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {
                        "cells": [
                            {"text": "Burrata Caprese"},
                            {
                                "text": "Heirloom tomatoes,
                                fresh burrata,
                                basil oil,
                                aged balsamic",
                            },
                            {
                                "text": "EUR 16.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Tuna Tartare"},
                            {
                                "text": "Sushi-grade ahi,
                                avocado,
                                sesame,
                                crispy wonton chips",
                            },
                            {
                                "text": "EUR 19.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "French Onion Soup"},
                            {
                                "text": "Caramelized onion broth,
                                Gruyère crouton",
                            },
                            {
                                "text": "EUR 14.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "headline",
                "level": "h2",
                "text": "Main Courses",
            },
            {
                "type": "table",
                "column_widths_in_percent": [30, 45, 25],
                "header": {
                    "cells": [
                        {"text": "Item"},
                        {"text": "Description"},
                        {
                            "text": "Price",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {
                        "cells": [
                            {"text": "Pan-Seared Salmon"},
                            {
                                "text": "Wild-caught salmon,
                                lemon beurre blanc,
                                roasted asparagus,
                                fingerling potatoes",
                            },
                            {
                                "text": "EUR 34.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Filet Mignon"},
                            {
                                "text": "8oz center-cut,
                                truffle mash,
                                grilled broccolini,
                                red wine jus",
                            },
                            {
                                "text": "EUR 48.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Wild Mushroom Risotto"},
                            {
                                "text": "Arborio rice,
                                porcini,
                                chanterelle,
                                Parmigiano-Reggiano,
                                truffle oil",
                            },
                            {
                                "text": "EUR 28.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Roasted Half Chicken"},
                            {
                                "text": "Free-range chicken,
                                herb jus,
                                seasonal vegetables,
                                garlic confit",
                            },
                            {
                                "text": "EUR 32.00",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                ],
            },
            {"type": "separator"},
            {
                "type": "paragraph",
                "runs": [
                    {"text": "Prices exclude tax and gratuity. A 20% gratuity is added for parties of 6 or more."},
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
				Title:  "The Golden Fork - Menu",
				Author: "The Golden Fork",
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
				il.NewHeadlineBlock("h1", "The Golden Fork"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "Fresh,
      seasonal cuisine crafted with locally sourced ingredients.",
    },
				il.NewSeparatorBlock(),
				il.NewHeadlineBlock("h2", "Appetizers"),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{{Text: "Burrata Caprese"}, {
       Text: "Heirloom tomatoes,
       fresh burrata,
       basil oil",
     }, {Text: "EUR 16.00"}}},
					{Cells: []il.TableCell{{Text: "Tuna Tartare"}, {
       Text: "Sushi-grade ahi,
       avocado,
       sesame",
     }, {Text: "EUR 19.00"}}},
					{Cells: []il.TableCell{{Text: "French Onion Soup"}, {
       Text: "Caramelized onion broth,
       Gruyère crouton",
     }, {Text: "EUR 14.00"}}},
				}),
				il.NewSeparatorBlock(),
				il.NewHeadlineBlock("h2", "Main Courses"),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{{Text: "Pan-Seared Salmon"}, {
       Text: "Wild-caught salmon,
       lemon beurre blanc",
     }, {Text: "EUR 34.00"}}},
					{Cells: []il.TableCell{{Text: "Filet Mignon"}, {
       Text: "8oz center-cut,
       truffle mash,
       red wine jus",
     }, {Text: "EUR 48.00"}}},
					{Cells: []il.TableCell{{Text: "Wild Mushroom Risotto"}, {
       Text: "Arborio rice,
       porcini,
       chanterelle",
     }, {Text: "EUR 28.00"}}},
					{Cells: []il.TableCell{{Text: "Roasted Half Chicken"}, {
       Text: "Free-range chicken,
       herb jus",
     }, {Text: "EUR 32.00"}}},
				}),
				il.NewSeparatorBlock(),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "Prices exclude tax and gratuity.",
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
  "name": "Generate Restaurant Menu",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Restaurant Menu\n\nRestaurants and food delivery platforms generate printable menus with categorized sections, item descriptions, and pricing \u2014 ready for in-house printing or PDF download.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "516d4df7-0c04-42a7-b21a-afdd0e76c040",
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
      "id": "ccdd4dd4-14f2-454a-a6ca-4aa120b291a8",
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
      "id": "48209e85-603b-4e76-a54b-ae192aea12a3",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"The Golden Fork - Menu\",\n    \"author\": \"The Golden Fork\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 72,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 72\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"The Golden Fork \\u00b7 88 Harbor Blvd, Berlin, DE 94111 \\u00b7 thegoldenfork.com\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"The Golden Fork\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Fresh, seasonal cuisine crafted with locally sourced ingredients. Please inform your server of any allergies or dietary restrictions.\"\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h2\",\n      \"text\": \"Appetizers\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        30,\n        45,\n        25\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Item\"\n          },\n          {\n            \"text\": \"Description\"\n          },\n          {\n            \"text\": \"Price\",\n            \"horizontal_alignment\": \"right\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Burrata Caprese\"\n            },\n            {\n              \"text\": \"Heirloom tomatoes, fresh burrata, basil oil, aged balsamic\"\n            },\n            {\n              \"text\": \"EUR 16.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Tuna Tartare\"\n            },\n            {\n              \"text\": \"Sushi-grade ahi, avocado, sesame, crispy wonton chips\"\n            },\n            {\n              \"text\": \"EUR 19.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"French Onion Soup\"\n            },\n            {\n              \"text\": \"Caramelized onion broth, Gruy\\u00e8re crouton\"\n            },\n            {\n              \"text\": \"EUR 14.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h2\",\n      \"text\": \"Main Courses\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        30,\n        45,\n        25\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Item\"\n          },\n          {\n            \"text\": \"Description\"\n          },\n          {\n            \"text\": \"Price\",\n            \"horizontal_alignment\": \"right\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Pan-Seared Salmon\"\n            },\n            {\n              \"text\": \"Wild-caught salmon, lemon beurre blanc, roasted asparagus, fingerling potatoes\"\n            },\n            {\n              \"text\": \"EUR 34.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Filet Mignon\"\n            },\n            {\n              \"text\": \"8oz center-cut, truffle mash, grilled broccolini, red wine jus\"\n            },\n            {\n              \"text\": \"EUR 48.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Wild Mushroom Risotto\"\n            },\n            {\n              \"text\": \"Arborio rice, porcini, chanterelle, Parmigiano-Reggiano, truffle oil\"\n            },\n            {\n              \"text\": \"EUR 28.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Roasted Half Chicken\"\n            },\n            {\n              \"text\": \"Free-range chicken, herb jus, seasonal vegetables, garlic confit\"\n            },\n            {\n              \"text\": \"EUR 32.00\",\n              \"horizontal_alignment\": \"right\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Prices exclude tax and gratuity. A 20% gratuity is added for parties of 6 or more.\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "038c573c-7061-45dd-bf36-ffb29a34c09b",
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
Generate a restaurant menu PDF for [restaurant name]. Use the generate_document tool with format "pdf" and these content blocks:

- Headline: [restaurant name]
- Paragraph: restaurant tagline or description
- For each menu section (e.g., Appetizers, Entrees, Desserts):
  - Headline: section name
  - Table or paragraphs: item name, description, and price for each dish
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
