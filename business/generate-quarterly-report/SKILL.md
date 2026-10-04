---
name: generate-quarterly-report
description: Create a structured quarterly business report with table of contents, data tables, and page numbers.
---

# Generate Quarterly Report

Operations and finance teams use this recipe to automate quarterly reporting. Build a complete business report with a table of contents, executive summary, revenue breakdown, department performance table, and consistent headers and footers with page numbers.

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
        "title": "Meridian Corp — Q1 2026 Quarterly Report",
        "author": "Meridian Corp"
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
          "font_size_in_pt": 32.0,
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
      "header": [
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
                      "text": "Meridian Corp",
                      "font_weight": "bold"
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
                      "text": "Q1 2026 Quarterly Report"
                    }
                  ]
                }
              ]
            }
          ]
        }
      ],
      "footer": [
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
                      "text": "Confidential — For Internal Use Only"
                    }
                  ]
                }
              ]
            },
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "page-number",
                  "text_alignment": "right"
                }
              ]
            }
          ]
        }
      ],
      "content": [
        {
          "type": "headline",
          "level": "h1",
          "text": "Meridian Corp — Q1 2026 Quarterly Report"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Prepared by the Office of the CFO · April 2026"
            }
          ]
        },
        {
          "type": "separator"
        },
        {
          "type": "table-of-contents",
          "levels": ["h1", "h2"],
          "leader": "dots"
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "Executive Summary"
        },
        {
          "type": "paragraph",
          "markdown": "Meridian Corp delivered **strong results in Q1 2026**, with consolidated revenue reaching **EUR 42.8M** — a 14% increase year-over-year. Gross margins improved to 68.3%, driven by operational efficiencies in the Cloud Services division. Net income rose to EUR 6.1M, reflecting disciplined cost management and continued investment in high-growth verticals."
        },
        {
          "type": "paragraph",
          "markdown": "Customer acquisition accelerated with **1,240 new enterprise accounts**, bringing total active customers to 18,650. Annual recurring revenue (ARR) crossed **EUR 165M**, positioning the company well for its full-year target of EUR 190M."
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "Financial Performance"
        },
        {
          "type": "headline",
          "level": "h2",
          "text": "Revenue Overview"
        },
        {
          "type": "paragraph",
          "markdown": "Total revenue for Q1 2026 was EUR 42.8M, compared to EUR 37.5M in Q1 2025. The growth was primarily driven by expansion in the Cloud Services and Data Analytics segments."
        },
        {
          "type": "table",
          "column_widths_in_percent": [40, 20, 20, 20],
          "header": {
            "cells": [
              {
                "text": "Metric"
              },
              {
                "text": "Q1 2026",
                "horizontal_alignment": "right"
              },
              {
                "text": "Q1 2025",
                "horizontal_alignment": "right"
              },
              {
                "text": "Change",
                "horizontal_alignment": "right"
              }
            ]
          },
          "rows": [
            {
              "cells": [
                {
                  "text": "Total Revenue"
                },
                {
                  "text": "EUR 42.8M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "EUR 37.5M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+14.1%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Gross Profit"
                },
                {
                  "text": "EUR 29.2M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "EUR 24.8M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+17.7%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Operating Expenses"
                },
                {
                  "text": "EUR 21.4M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "EUR 19.1M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+12.0%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Net Income"
                },
                {
                  "text": "EUR 6.1M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "EUR 4.3M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+41.9%",
                  "horizontal_alignment": "right"
                }
              ]
            }
          ]
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h2",
          "text": "Revenue by Division"
        },
        {
          "type": "table",
          "column_widths_in_percent": [35, 20, 20, 25],
          "header": {
            "cells": [
              {
                "text": "Division"
              },
              {
                "text": "Revenue",
                "horizontal_alignment": "right"
              },
              {
                "text": "% of Total",
                "horizontal_alignment": "right"
              },
              {
                "text": "YoY Growth",
                "horizontal_alignment": "right"
              }
            ]
          },
          "rows": [
            {
              "cells": [
                {
                  "text": "Cloud Services"
                },
                {
                  "text": "EUR 18.9M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "44.2%",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+22.1%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Data Analytics"
                },
                {
                  "text": "EUR 12.4M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "29.0%",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+16.8%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Professional Services"
                },
                {
                  "text": "EUR 7.8M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "18.2%",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "+5.4%",
                  "horizontal_alignment": "right"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Legacy Licensing"
                },
                {
                  "text": "EUR 3.7M",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "8.6%",
                  "horizontal_alignment": "right"
                },
                {
                  "text": "-8.2%",
                  "horizontal_alignment": "right"
                }
              ]
            }
          ]
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "Outlook"
        },
        {
          "type": "paragraph",
          "markdown": "Management reaffirms its full-year 2026 revenue guidance of **EUR 175M–EUR 185M** and expects continued margin expansion as the Cloud Services division scales. Key initiatives for Q2 include the launch of the Meridian AI Copilot platform and expansion into the APAC market."
        },
        {
          "type": "list",
          "variant": "unordered",
          "items": [
            {
              "text": "Launch Meridian AI Copilot in Q2 2026"
            },
            {
              "text": "Expand APAC sales team by 15 headcount"
            },
            {
              "text": "Achieve EUR 50M quarterly revenue target by Q4 2026"
            },
            {
              "text": "Complete SOC 2 Type II recertification"
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
      title: "Meridian Corp — Q1 2026 Quarterly Report",
      author: "Meridian Corp",
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
        font_size_in_pt: 32.0,
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
    header: [
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
                    text: "Meridian Corp",
                    font_weight: "bold",
                  },
                ],
              },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [{ text: "Q1 2026 Quarterly Report" }],
              },
            ],
          },
        ],
      },
    ],
    footer: [
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [
              {
                type: "paragraph",
                runs: [{ text: "Confidential — For Internal Use Only" }],
              },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                type: "page-number",
                text_alignment: "right",
              },
            ],
          },
        ],
      },
    ],
    content: [
      {
        type: "headline",
        level: "h1",
        text: "Meridian Corp — Q1 2026 Quarterly Report",
      },
      {
        type: "paragraph",
        runs: [{ text: "Prepared by the Office of the CFO · April 2026" }],
      },
      { type: "separator" },
      {
        type: "table-of-contents",
        levels: ["h1", "h2"],
        leader: "dots",
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Executive Summary",
      },
      {
        type: "paragraph",
        markdown:
          "Meridian Corp delivered **strong results in Q1 2026**, with consolidated revenue reaching **EUR 42.8M** — a 14% increase year-over-year. Gross margins improved to 68.3%, driven by operational efficiencies in the Cloud Services division. Net income rose to EUR 6.1M, reflecting disciplined cost management and continued investment in high-growth verticals.",
      },
      {
        type: "paragraph",
        markdown:
          "Customer acquisition accelerated with **1,240 new enterprise accounts**, bringing total active customers to 18,650. Annual recurring revenue (ARR) crossed **EUR 165M**, positioning the company well for its full-year target of EUR 190M.",
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Financial Performance",
      },
      {
        type: "headline",
        level: "h2",
        text: "Revenue Overview",
      },
      {
        type: "paragraph",
        markdown:
          "Total revenue for Q1 2026 was EUR 42.8M, compared to EUR 37.5M in Q1 2025. The growth was primarily driven by expansion in the Cloud Services and Data Analytics segments.",
      },
      {
        type: "table",
        column_widths_in_percent: [40, 20, 20, 20],
        header: {
          cells: [
            { text: "Metric" },
            {
              text: "Q1 2026",
              horizontal_alignment: "right",
            },
            {
              text: "Q1 2025",
              horizontal_alignment: "right",
            },
            {
              text: "Change",
              horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          {
            cells: [
              { text: "Total Revenue" },
              {
                text: "EUR 42.8M",
                horizontal_alignment: "right",
              },
              {
                text: "EUR 37.5M",
                horizontal_alignment: "right",
              },
              {
                text: "+14.1%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Gross Profit" },
              {
                text: "EUR 29.2M",
                horizontal_alignment: "right",
              },
              {
                text: "EUR 24.8M",
                horizontal_alignment: "right",
              },
              {
                text: "+17.7%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Operating Expenses" },
              {
                text: "EUR 21.4M",
                horizontal_alignment: "right",
              },
              {
                text: "EUR 19.1M",
                horizontal_alignment: "right",
              },
              {
                text: "+12.0%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Net Income" },
              {
                text: "EUR 6.1M",
                horizontal_alignment: "right",
              },
              {
                text: "EUR 4.3M",
                horizontal_alignment: "right",
              },
              {
                text: "+41.9%",
                horizontal_alignment: "right",
              },
            ],
          },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h2",
        text: "Revenue by Division",
      },
      {
        type: "table",
        column_widths_in_percent: [35, 20, 20, 25],
        header: {
          cells: [
            { text: "Division" },
            {
              text: "Revenue",
              horizontal_alignment: "right",
            },
            {
              text: "% of Total",
              horizontal_alignment: "right",
            },
            {
              text: "YoY Growth",
              horizontal_alignment: "right",
            },
          ],
        },
        rows: [
          {
            cells: [
              { text: "Cloud Services" },
              {
                text: "EUR 18.9M",
                horizontal_alignment: "right",
              },
              {
                text: "44.2%",
                horizontal_alignment: "right",
              },
              {
                text: "+22.1%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Data Analytics" },
              {
                text: "EUR 12.4M",
                horizontal_alignment: "right",
              },
              {
                text: "29.0%",
                horizontal_alignment: "right",
              },
              {
                text: "+16.8%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Professional Services" },
              {
                text: "EUR 7.8M",
                horizontal_alignment: "right",
              },
              {
                text: "18.2%",
                horizontal_alignment: "right",
              },
              {
                text: "+5.4%",
                horizontal_alignment: "right",
              },
            ],
          },
          {
            cells: [
              { text: "Legacy Licensing" },
              {
                text: "EUR 3.7M",
                horizontal_alignment: "right",
              },
              {
                text: "8.6%",
                horizontal_alignment: "right",
              },
              {
                text: "-8.2%",
                horizontal_alignment: "right",
              },
            ],
          },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Outlook",
      },
      {
        type: "paragraph",
        markdown:
          "Management reaffirms its full-year 2026 revenue guidance of **EUR 175M–EUR 185M** and expects continued margin expansion as the Cloud Services division scales. Key initiatives for Q2 include the launch of the Meridian AI Copilot platform and expansion into the APAC market.",
      },
      {
        type: "list",
        variant: "unordered",
        items: [
          { text: "Launch Meridian AI Copilot in Q2 2026" },
          { text: "Expand APAC sales team by 15 headcount" },
          { text: "Achieve EUR 50M quarterly revenue target by Q4 2026" },
          { text: "Complete SOC 2 Type II recertification" },
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
            "title": "Meridian Corp — Q1 2026 Quarterly Report",
            "author": "Meridian Corp",
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
                "font_size_in_pt": 32.0,
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
        "header": [
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
                                        "text": "Meridian Corp",
                                        "font_weight": "bold",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [{"text": "Q1 2026 Quarterly Report"}],
                            },
                        ],
                    },
                ],
            },
        ],
        "footer": [
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "paragraph",
                                "runs": [{"text": "Confidential — For Internal Use Only"}],
                            },
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "page-number",
                                "text_alignment": "right",
                            },
                        ],
                    },
                ],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Meridian Corp — Q1 2026 Quarterly Report",
            },
            {
                "type": "paragraph",
                "runs": [{"text": "Prepared by the Office of the CFO · April 2026"}],
            },
            {"type": "separator"},
            {
                "type": "table-of-contents",
                "levels": ["h1", "h2"],
                "leader": "dots",
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Executive Summary",
            },
            {
                "type": "paragraph",
                "markdown": "Meridian Corp delivered **strong results in Q1 2026**, with consolidated revenue reaching **EUR 42.8M** — a 14% increase year-over-year. Gross margins improved to 68.3%, driven by operational efficiencies in the Cloud Services division. Net income rose to EUR 6.1M, reflecting disciplined cost management and continued investment in high-growth verticals.",
            },
            {
                "type": "paragraph",
                "markdown": "Customer acquisition accelerated with **1,240 new enterprise accounts**, bringing total active customers to 18,650. Annual recurring revenue (ARR) crossed **EUR 165M**, positioning the company well for its full-year target of EUR 190M.",
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Financial Performance",
            },
            {
                "type": "headline",
                "level": "h2",
                "text": "Revenue Overview",
            },
            {
                "type": "paragraph",
                "markdown": "Total revenue for Q1 2026 was EUR 42.8M, compared to EUR 37.5M in Q1 2025. The growth was primarily driven by expansion in the Cloud Services and Data Analytics segments.",
            },
            {
                "type": "table",
                "column_widths_in_percent": [40, 20, 20, 20],
                "header": {
                    "cells": [
                        {"text": "Metric"},
                        {
                            "text": "Q1 2026",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "Q1 2025",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "Change",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {
                        "cells": [
                            {"text": "Total Revenue"},
                            {
                                "text": "EUR 42.8M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "EUR 37.5M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+14.1%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Gross Profit"},
                            {
                                "text": "EUR 29.2M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "EUR 24.8M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+17.7%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Operating Expenses"},
                            {
                                "text": "EUR 21.4M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "EUR 19.1M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+12.0%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Net Income"},
                            {
                                "text": "EUR 6.1M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "EUR 4.3M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+41.9%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h2",
                "text": "Revenue by Division",
            },
            {
                "type": "table",
                "column_widths_in_percent": [35, 20, 20, 25],
                "header": {
                    "cells": [
                        {"text": "Division"},
                        {
                            "text": "Revenue",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "% of Total",
                            "horizontal_alignment": "right",
                        },
                        {
                            "text": "YoY Growth",
                            "horizontal_alignment": "right",
                        },
                    ],
                },
                "rows": [
                    {
                        "cells": [
                            {"text": "Cloud Services"},
                            {
                                "text": "EUR 18.9M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "44.2%",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+22.1%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Data Analytics"},
                            {
                                "text": "EUR 12.4M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "29.0%",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+16.8%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Professional Services"},
                            {
                                "text": "EUR 7.8M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "18.2%",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "+5.4%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Legacy Licensing"},
                            {
                                "text": "EUR 3.7M",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "8.6%",
                                "horizontal_alignment": "right",
                            },
                            {
                                "text": "-8.2%",
                                "horizontal_alignment": "right",
                            },
                        ],
                    },
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Outlook",
            },
            {
                "type": "paragraph",
                "markdown": "Management reaffirms its full-year 2026 revenue guidance of **EUR 175M–EUR 185M** and expects continued margin expansion as the Cloud Services division scales. Key initiatives for Q2 include the launch of the Meridian AI Copilot platform and expansion into the APAC market.",
            },
            {
                "type": "list",
                "variant": "unordered",
                "items": [
                    {"text": "Launch Meridian AI Copilot in Q2 2026"},
                    {"text": "Expand APAC sales team by 15 headcount"},
                    {"text": "Achieve EUR 50M quarterly revenue target by Q4 2026"},
                    {"text": "Complete SOC 2 Type II recertification"},
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
				Title:  "Meridian Corp — Q1 2026 Quarterly Report",
				Author: "Meridian Corp",
			},
			Page: il.DocumentPage{
				Size:    il.DocPageSize{Preset: "A4"},
				Margins: il.DocMargins{
      TopInPt: 72,
      RightInPt: 72,
      BottomInPt: 72,
      LeftInPt: 72,
    },
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "Meridian Corp — Q1 2026 Quarterly Report"),
				il.NewSeparatorBlock(),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Executive Summary"),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Financial Performance"),
				il.NewHeadlineBlock("h2", "Revenue Overview"),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{
						{Text: "Total Revenue"},
						{Text: "EUR 42.8M"},
						{Text: "EUR 37.5M"},
						{Text: "+14.1%"},
					}},
					{Cells: []il.TableCell{
						{Text: "Gross Profit"},
						{Text: "EUR 29.2M"},
						{Text: "EUR 24.8M"},
						{Text: "+17.7%"},
					}},
					{Cells: []il.TableCell{
						{Text: "Net Income"},
						{Text: "EUR 6.1M"},
						{Text: "EUR 4.3M"},
						{Text: "+41.9%"},
					}},
				}),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Outlook"),
				il.NewListBlock("unordered", []il.ListItem{
					{Text: "Launch Meridian AI Copilot in Q2 2026"},
					{Text: "Expand APAC sales team by 15 headcount"},
					{Text: "Achieve EUR 50M quarterly revenue target by Q4 2026"},
					{Text: "Complete SOC 2 Type II recertification"},
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
  "name": "Generate Quarterly Report",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Quarterly Report

Operations and finance teams use this recipe to automate quarterly reporting. Build a complete business report with a table of contents, executive summary, revenue breakdown, department performance table, and consistent headers and footers with page numbers.

**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "1058bc9e-19fe-45a6-9e62-051e5e1be859",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Document
Resource: **Document Generation**

Configure the Document Generation parameters below, then connect your credentials.",
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
      "id": "7d2d938f-9a16-4aae-b4ce-bb6cf0bf8425",
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
      "id": "95d0a90c-75cf-471f-82c2-ea6b34dc2c0c",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{
  \"metadata\": {
    \"title\": \"Meridian Corp \u2014 Q1 2026 Quarterly Report\",
    \"author\": \"Meridian Corp\"
  },
  \"page\": {
    \"size\": {
      \"preset\": \"A4\"
    },
    \"margins\": {
      \"top_in_pt\": 72,
      \"right_in_pt\": 72,
      \"bottom_in_pt\": 72,
      \"left_in_pt\": 72
    }
  },
  \"styles\": {
    \"text\": {
      \"font_family\": \"Helvetica\",
      \"font_size_in_pt\": 11.0,
      \"line_height\": 1.5,
      \"color\": \"#333333\"
    },
    \"headline\": {
      \"font_family\": \"Helvetica\",
      \"font_size_in_pt\": 32.0,
      \"color\": \"#111111\",
      \"spacing_before_in_pt\": 12.0,
      \"spacing_after_in_pt\": 6.0,
      \"font_weight\": \"bold\"
    },
    \"link\": {
      \"color\": \"#0066CC\",
      \"is_underlined\": true
    },
    \"list\": {
      \"text_style\": {
        \"font_family\": \"Helvetica\",
        \"font_size_in_pt\": 11.0,
        \"line_height\": 1.5,
        \"color\": \"#333333\"
      },
      \"marker_color\": \"#333333\",
      \"marker_gap_in_pt\": 8.0
    },
    \"table\": {
      \"header\": {
        \"background_color\": \"#333333\",
        \"text_color\": \"#FFFFFF\",
        \"font_size_in_pt\": 12.0,
        \"font_weight\": \"bold\"
      },
      \"body\": {
        \"background_color\": \"#FFFFFF\",
        \"text_color\": \"#333333\",
        \"font_size_in_pt\": 12.0
      },
      \"border\": {
        \"outer\": {
          \"top\": {
            \"color\": \"#CCCCCC\",
            \"width_in_pt\": 1.0
          },
          \"right\": {
            \"color\": \"#CCCCCC\",
            \"width_in_pt\": 1.0
          },
          \"bottom\": {
            \"color\": \"#CCCCCC\",
            \"width_in_pt\": 1.0
          },
          \"left\": {
            \"color\": \"#CCCCCC\",
            \"width_in_pt\": 1.0
          }
        },
        \"inner\": {
          \"horizontal\": {
            \"color\": \"#EEEEEE\",
            \"width_in_pt\": 0.5
          },
          \"vertical\": {
            \"color\": \"#EEEEEE\",
            \"width_in_pt\": 0.5
          }
        }
      }
    },
    \"grid\": {
      \"background_color\": \"#FFFFFF\",
      \"border_color\": \"#CCCCCC\",
      \"border_width_in_pt\": 0.0,
      \"gap_in_pt\": 12.0
    },
    \"separator\": {
      \"color\": \"#CCCCCC\",
      \"thickness_in_pt\": 1.0,
      \"spacing_before_in_pt\": 12.0,
      \"spacing_after_in_pt\": 12.0
    },
    \"image\": {
      \"border_color\": \"#000000\",
      \"border_width_in_pt\": 0.0
    }
  },
  \"header\": [
    {
      \"type\": \"grid\",
      \"columns\": [
        {
          \"column_span\": 6,
          \"blocks\": [
            {
              \"type\": \"paragraph\",
              \"runs\": [
                {
                  \"text\": \"Meridian Corp\",
                  \"font_weight\": \"bold\"
                }
              ]
            }
          ]
        },
        {
          \"column_span\": 6,
          \"blocks\": [
            {
              \"type\": \"paragraph\",
              \"runs\": [
                {
                  \"text\": \"Q1 2026 Quarterly Report\"
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  \"footer\": [
    {
      \"type\": \"grid\",
      \"columns\": [
        {
          \"column_span\": 6,
          \"blocks\": [
            {
              \"type\": \"paragraph\",
              \"runs\": [
                {
                  \"text\": \"Confidential \u2014 For Internal Use Only\"
                }
              ]
            }
          ]
        },
        {
          \"column_span\": 6,
          \"blocks\": [
            {
              \"type\": \"page-number\",
              \"text_alignment\": \"right\"
            }
          ]
        }
      ]
    }
  ],
  \"content\": [
    {
      \"type\": \"headline\",
      \"level\": \"h1\",
      \"text\": \"Meridian Corp \u2014 Q1 2026 Quarterly Report\"
    },
    {
      \"type\": \"paragraph\",
      \"runs\": [
        {
          \"text\": \"Prepared by the Office of the CFO \u00b7 April 2026\"
        }
      ]
    },
    {
      \"type\": \"separator\"
    },
    {
      \"type\": \"table-of-contents\",
      \"levels\": [
        \"h1\",
        \"h2\"
      ],
      \"leader\": \"dots\"
    },
    {
      \"type\": \"page-break\"
    },
    {
      \"type\": \"headline\",
      \"level\": \"h1\",
      \"text\": \"Executive Summary\"
    },
    {
      \"type\": \"paragraph\",
      \"markdown\": \"Meridian Corp delivered **strong results in Q1 2026**, with consolidated revenue reaching **EUR 42.8M** \u2014 a 14% increase year-over-year. Gross margins improved to 68.3%, driven by operational efficiencies in the Cloud Services division. Net income rose to EUR 6.1M, reflecting disciplined cost management and continued investment in high-growth verticals.\"
    },
    {
      \"type\": \"paragraph\",
      \"markdown\": \"Customer acquisition accelerated with **1,240 new enterprise accounts**, bringing total active customers to 18,650. Annual recurring revenue (ARR) crossed **EUR 165M**, positioning the company well for its full-year target of EUR 190M.\"
    },
    {
      \"type\": \"page-break\"
    },
    {
      \"type\": \"headline\",
      \"level\": \"h1\",
      \"text\": \"Financial Performance\"
    },
    {
      \"type\": \"headline\",
      \"level\": \"h2\",
      \"text\": \"Revenue Overview\"
    },
    {
      \"type\": \"paragraph\",
      \"markdown\": \"Total revenue for Q1 2026 was EUR 42.8M, compared to EUR 37.5M in Q1 2025. The growth was primarily driven by expansion in the Cloud Services and Data Analytics segments.\"
    },
    {
      \"type\": \"table\",
      \"column_widths_in_percent\": [
        40,
        20,
        20,
        20
      ],
      \"header\": {
        \"cells\": [
          {
            \"text\": \"Metric\"
          },
          {
            \"text\": \"Q1 2026\",
            \"horizontal_alignment\": \"right\"
          },
          {
            \"text\": \"Q1 2025\",
            \"horizontal_alignment\": \"right\"
          },
          {
            \"text\": \"Change\",
            \"horizontal_alignment\": \"right\"
          }
        ]
      },
      \"rows\": [
        {
          \"cells\": [
            {
              \"text\": \"Total Revenue\"
            },
            {
              \"text\": \"EUR 42.8M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"EUR 37.5M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+14.1%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Gross Profit\"
            },
            {
              \"text\": \"EUR 29.2M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"EUR 24.8M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+17.7%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Operating Expenses\"
            },
            {
              \"text\": \"EUR 21.4M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"EUR 19.1M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+12.0%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Net Income\"
            },
            {
              \"text\": \"EUR 6.1M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"EUR 4.3M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+41.9%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        }
      ]
    },
    {
      \"type\": \"page-break\"
    },
    {
      \"type\": \"headline\",
      \"level\": \"h2\",
      \"text\": \"Revenue by Division\"
    },
    {
      \"type\": \"table\",
      \"column_widths_in_percent\": [
        35,
        20,
        20,
        25
      ],
      \"header\": {
        \"cells\": [
          {
            \"text\": \"Division\"
          },
          {
            \"text\": \"Revenue\",
            \"horizontal_alignment\": \"right\"
          },
          {
            \"text\": \"% of Total\",
            \"horizontal_alignment\": \"right\"
          },
          {
            \"text\": \"YoY Growth\",
            \"horizontal_alignment\": \"right\"
          }
        ]
      },
      \"rows\": [
        {
          \"cells\": [
            {
              \"text\": \"Cloud Services\"
            },
            {
              \"text\": \"EUR 18.9M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"44.2%\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+22.1%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Data Analytics\"
            },
            {
              \"text\": \"EUR 12.4M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"29.0%\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+16.8%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Professional Services\"
            },
            {
              \"text\": \"EUR 7.8M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"18.2%\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"+5.4%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        },
        {
          \"cells\": [
            {
              \"text\": \"Legacy Licensing\"
            },
            {
              \"text\": \"EUR 3.7M\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"8.6%\",
              \"horizontal_alignment\": \"right\"
            },
            {
              \"text\": \"-8.2%\",
              \"horizontal_alignment\": \"right\"
            }
          ]
        }
      ]
    },
    {
      \"type\": \"page-break\"
    },
    {
      \"type\": \"headline\",
      \"level\": \"h1\",
      \"text\": \"Outlook\"
    },
    {
      \"type\": \"paragraph\",
      \"markdown\": \"Management reaffirms its full-year 2026 revenue guidance of **EUR 175M\u2013EUR 185M** and expects continued margin expansion as the Cloud Services division scales. Key initiatives for Q2 include the launch of the Meridian AI Copilot platform and expansion into the APAC market.\"
    },
    {
      \"type\": \"list\",
      \"variant\": \"unordered\",
      \"items\": [
        {
          \"text\": \"Launch Meridian AI Copilot in Q2 2026\"
        },
        {
          \"text\": \"Expand APAC sales team by 15 headcount\"
        },
        {
          \"text\": \"Achieve EUR 50M quarterly revenue target by Q4 2026\"
        },
        {
          \"text\": \"Complete SOC 2 Type II recertification\"
        }
      ]
    }
  ]
}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "8361daca-8be5-4bca-9b1f-291566c1045a",
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
Generate a quarterly business report PDF. Use the generate_document tool with format "pdf" and these content blocks:

- Headline: "[Company Name] — Q[quarter] [year] Report"
- Table of contents with section links
- Headline: "Executive Summary" with summary paragraph
- Headline: "Revenue" with a table of revenue by product line and quarter
- Headline: "Department Performance" with a metrics table
- Headers and footers with company name and page numbers
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
