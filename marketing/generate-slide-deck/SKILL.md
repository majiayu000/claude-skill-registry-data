---
name: generate-slide-deck
description: Build a PowerPoint slide deck with title slide, content slides, and call-to-action page.
---

# Generate Slide Deck

Sales and marketing teams use this recipe to generate a branded slide deck programmatically. Build a complete presentation with a title slide, problem and solution framing, feature highlights, pricing tables, and a call to action — delivered as a ready-to-present PPTX file.

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
    "format": "pptx",
    "document": {
      "metadata": {
        "title": "Launchpad Analytics — Product Launch",
        "author": "Launchpad Analytics GmbH"
      },
      "page": {
        "size": {
          "preset": "A4"
        },
        "margins": {
          "top_in_pt": 54,
          "right_in_pt": 54,
          "bottom_in_pt": 54,
          "left_in_pt": 54
        }
      },
      "styles": {
        "text": {
          "font_family": "Helvetica",
          "font_size_in_pt": 14.0,
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
            "font_size_in_pt": 14.0,
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
      "content": [
        {
          "type": "headline",
          "level": "h1",
          "text": "Launchpad Analytics"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Real-time product analytics for teams that ship fast.",
              "font_weight": "bold"
            }
          ]
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Product Launch — Q2 2026"
            }
          ]
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "The Problem"
        },
        {
          "type": "paragraph",
          "markdown": "Product teams today are **flying blind**. Existing analytics tools are built for data engineers, not product managers. Teams wait days for answers to simple questions like *\"Which feature drives retention?\"* or *\"Where do users drop off in onboarding?\"*"
        },
        {
          "type": "list",
          "variant": "unordered",
          "items": [
            {
              "text": "Average time to insight: 3–5 business days"
            },
            {
              "text": "72% of product managers rely on engineers for data queries"
            },
            {
              "text": "Only 18% of companies act on analytics within the same sprint"
            }
          ]
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "Our Solution"
        },
        {
          "type": "paragraph",
          "markdown": "Launchpad Analytics gives product teams **instant answers** without writing SQL. Our AI-powered query engine translates natural language questions into real-time insights, delivered as interactive dashboards that update as your users interact with your product."
        },
        {
          "type": "list",
          "variant": "unordered",
          "items": [
            {
              "text": "Ask questions in plain English — no SQL required"
            },
            {
              "text": "Real-time event streaming with sub-second latency"
            },
            {
              "text": "Auto-generated dashboards for onboarding, retention, and feature adoption"
            },
            {
              "text": "One-click integration with Segment, Amplitude, and Mixpanel"
            }
          ]
        },
        {
          "type": "page-break"
        },
        {
          "type": "headline",
          "level": "h1",
          "text": "Key Features"
        },
        {
          "type": "grid",
          "columns": [
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "headline",
                  "level": "h3",
                  "text": "Natural Language Queries"
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Ask \"What percentage of users completed onboarding last week?\" and get an instant chart. No SQL, no waiting."
                    }
                  ]
                },
                {
                  "type": "headline",
                  "level": "h3",
                  "text": "Funnel Analysis"
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Visualize user journeys from signup to conversion. Identify drop-off points and A/B test improvements in real time."
                    }
                  ]
                }
              ]
            },
            {
              "column_span": 6,
              "blocks": [
                {
                  "type": "headline",
                  "level": "h3",
                  "text": "Cohort Retention"
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Track retention by signup cohort, plan tier, or acquisition channel. See trends over 7, 30, and 90-day windows."
                    }
                  ]
                },
                {
                  "type": "headline",
                  "level": "h3",
                  "text": "Team Collaboration"
                },
                {
                  "type": "paragraph",
                  "runs": [
                    {
                      "text": "Share dashboards with your team via link. Add annotations, set alerts, and comment on data points directly."
                    }
                  ]
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
          "text": "Pricing"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Simple, transparent pricing that scales with your product."
            }
          ]
        },
        {
          "type": "table",
          "column_widths_in_percent": [25, 25, 25, 25],
          "header": {
            "cells": [
              {
                "text": "Feature"
              },
              {
                "text": "Starter",
                "horizontal_alignment": "center"
              },
              {
                "text": "Growth",
                "horizontal_alignment": "center"
              },
              {
                "text": "Enterprise",
                "horizontal_alignment": "center"
              }
            ]
          },
          "rows": [
            {
              "cells": [
                {
                  "text": "Monthly Price"
                },
                {
                  "text": "EUR 299/mo",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "EUR 799/mo",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Custom",
                  "horizontal_alignment": "center"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Monthly Events"
                },
                {
                  "text": "5M",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "50M",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Unlimited",
                  "horizontal_alignment": "center"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Team Members"
                },
                {
                  "text": "5",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "25",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Unlimited",
                  "horizontal_alignment": "center"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Data Retention"
                },
                {
                  "text": "12 months",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "24 months",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Unlimited",
                  "horizontal_alignment": "center"
                }
              ]
            },
            {
              "cells": [
                {
                  "text": "Support"
                },
                {
                  "text": "Email",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Priority",
                  "horizontal_alignment": "center"
                },
                {
                  "text": "Dedicated CSM",
                  "horizontal_alignment": "center"
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
          "text": "Get Started Today"
        },
        {
          "type": "paragraph",
          "markdown": "Join **340+ product teams** already using Launchpad Analytics to ship better products, faster."
        },
        {
          "type": "list",
          "variant": "ordered",
          "items": [
            {
              "text": "Sign up for a free 14-day trial at launchpad-analytics.com"
            },
            {
              "text": "Connect your event source in under 5 minutes"
            },
            {
              "text": "Ask your first question and get instant insights"
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
              "text": "Contact us: ",
              "font_weight": "bold"
            },
            {
              "text": "sales@launchpad-analytics.com · (415) 555-0192 · launchpad-analytics.com"
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
  format: "pptx",
  document: {
    metadata: {
      title: "Launchpad Analytics — Product Launch",
      author: "Launchpad Analytics GmbH",
    },
    page: {
      size: { preset: "A4" },
      margins: {
        top_in_pt: 54,
        right_in_pt: 54,
        bottom_in_pt: 54,
        left_in_pt: 54,
      },
    },
    styles: {
      text: {
        font_family: "Helvetica",
        font_size_in_pt: 14.0,
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
          font_size_in_pt: 14.0,
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
    content: [
      {
        type: "headline",
        level: "h1",
        text: "Launchpad Analytics",
      },
      {
        type: "paragraph",
        runs: [
          {
            text: "Real-time product analytics for teams that ship fast.",
            font_weight: "bold",
          },
        ],
      },
      {
        type: "paragraph",
        runs: [{ text: "Product Launch — Q2 2026" }],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "The Problem",
      },
      {
        type: "paragraph",
        markdown: "Product teams today are **flying blind**. Existing analytics tools are built for data engineers, not product managers. Teams wait days for answers to simple questions like *\"Which feature drives retention?\"* or *\"Where do users drop off in onboarding?\"*",
      },
      {
        type: "list",
        variant: "unordered",
        items: [
          { text: "Average time to insight: 3–5 business days" },
          { text: "72% of product managers rely on engineers for data queries" },
          { text: "Only 18% of companies act on analytics within the same sprint" },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Our Solution",
      },
      {
        type: "paragraph",
        markdown: "Launchpad Analytics gives product teams **instant answers** without writing SQL. Our AI-powered query engine translates natural language questions into real-time insights, delivered as interactive dashboards that update as your users interact with your product.",
      },
      {
        type: "list",
        variant: "unordered",
        items: [
          { text: "Ask questions in plain English — no SQL required" },
          { text: "Real-time event streaming with sub-second latency" },
          {
              text: "Auto-generated dashboards for onboarding,
              retention,
              and feature adoption",
          },
          {
              text: "One-click integration with Segment,
              Amplitude,
              and Mixpanel",
          },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Key Features",
      },
      {
        type: "grid",
        columns: [
          {
            column_span: 6,
            blocks: [
              {
                type: "headline",
                level: "h3",
                text: "Natural Language Queries",
              },
              {
                type: "paragraph",
                runs: [{
                    text: "Ask \"What percentage of users completed onboarding last week?\" and get an instant chart. No SQL,
                    no waiting.",
                }],
              },
              {
                type: "headline",
                level: "h3",
                text: "Funnel Analysis",
              },
              {
                type: "paragraph",
                runs: [{ text: "Visualize user journeys from signup to conversion. Identify drop-off points and A/B test improvements in real time." }],
              },
            ],
          },
          {
            column_span: 6,
            blocks: [
              {
                type: "headline",
                level: "h3",
                text: "Cohort Retention",
              },
              {
                type: "paragraph",
                runs: [{
                    text: "Track retention by signup cohort,
                    plan tier,
                    or acquisition channel. See trends over 7,
                    30,
                    and 90-day windows.",
                }],
              },
              {
                type: "headline",
                level: "h3",
                text: "Team Collaboration",
              },
              {
                type: "paragraph",
                runs: [{
                    text: "Share dashboards with your team via link. Add annotations,
                    set alerts,
                    and comment on data points directly.",
                }],
              },
            ],
          },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Pricing",
      },
      {
        type: "paragraph",
        runs: [{
            text: "Simple,
            transparent pricing that scales with your product.",
        }],
      },
      {
        type: "table",
        column_widths_in_percent: [25, 25, 25, 25],
        header: {
          cells: [
            { text: "Feature" },
            {
              text: "Starter",
              horizontal_alignment: "center",
            },
            {
              text: "Growth",
              horizontal_alignment: "center",
            },
            {
              text: "Enterprise",
              horizontal_alignment: "center",
            },
          ],
        },
        rows: [
          {
            cells: [
              { text: "Monthly Price" },
              {
                text: "EUR 299/mo",
                horizontal_alignment: "center",
              },
              {
                text: "EUR 799/mo",
                horizontal_alignment: "center",
              },
              {
                text: "Custom",
                horizontal_alignment: "center",
              },
            ],
          },
          {
            cells: [
              { text: "Monthly Events" },
              {
                text: "5M",
                horizontal_alignment: "center",
              },
              {
                text: "50M",
                horizontal_alignment: "center",
              },
              {
                text: "Unlimited",
                horizontal_alignment: "center",
              },
            ],
          },
          {
            cells: [
              { text: "Team Members" },
              {
                text: "5",
                horizontal_alignment: "center",
              },
              {
                text: "25",
                horizontal_alignment: "center",
              },
              {
                text: "Unlimited",
                horizontal_alignment: "center",
              },
            ],
          },
          {
            cells: [
              { text: "Data Retention" },
              {
                text: "12 months",
                horizontal_alignment: "center",
              },
              {
                text: "24 months",
                horizontal_alignment: "center",
              },
              {
                text: "Unlimited",
                horizontal_alignment: "center",
              },
            ],
          },
          {
            cells: [
              { text: "Support" },
              {
                text: "Email",
                horizontal_alignment: "center",
              },
              {
                text: "Priority",
                horizontal_alignment: "center",
              },
              {
                text: "Dedicated CSM",
                horizontal_alignment: "center",
              },
            ],
          },
        ],
      },
      { type: "page-break" },
      {
        type: "headline",
        level: "h1",
        text: "Get Started Today",
      },
      {
        type: "paragraph",
        markdown: "Join **340+ product teams** already using Launchpad Analytics to ship better products, faster.",
      },
      {
        type: "list",
        variant: "ordered",
        items: [
          { text: "Sign up for a free 14-day trial at launchpad-analytics.com" },
          { text: "Connect your event source in under 5 minutes" },
          { text: "Ask your first question and get instant insights" },
        ],
      },
      { type: "separator" },
      {
        type: "paragraph",
        runs: [
          {
            text: "Contact us: ",
            font_weight: "bold",
          },
          { text: "sales@launchpad-analytics.com · (415) 555-0192 · launchpad-analytics.com" },
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
    format="pptx",
    document={
        "metadata": {
            "title": "Launchpad Analytics — Product Launch",
            "author": "Launchpad Analytics GmbH",
        },
        "page": {
            "size": {"preset": "A4"},
            "margins": {
                "top_in_pt": 54,
                "right_in_pt": 54,
                "bottom_in_pt": 54,
                "left_in_pt": 54,
            },
        },
        "styles": {
            "text": {
                "font_family": "Helvetica",
                "font_size_in_pt": 14.0,
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
                    "font_size_in_pt": 14.0,
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
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Launchpad Analytics",
            },
            {
                "type": "paragraph",
                "runs": [
                    {
                        "text": "Real-time product analytics for teams that ship fast.",
                        "font_weight": "bold",
                    },
                ],
            },
            {
                "type": "paragraph",
                "runs": [{"text": "Product Launch — Q2 2026"}],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "The Problem",
            },
            {
                "type": "paragraph",
                "markdown": "Product teams today are **flying blind**. Existing analytics tools are built for data engineers, not product managers. Teams wait days for answers to simple questions like *\"Which feature drives retention?\"* or *\"Where do users drop off in onboarding?\"*",
            },
            {
                "type": "list",
                "variant": "unordered",
                "items": [
                    {"text": "Average time to insight: 3–5 business days"},
                    {"text": "72% of product managers rely on engineers for data queries"},
                    {"text": "Only 18% of companies act on analytics within the same sprint"},
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Our Solution",
            },
            {
                "type": "paragraph",
                "markdown": "Launchpad Analytics gives product teams **instant answers** without writing SQL. Our AI-powered query engine translates natural language questions into real-time insights, delivered as interactive dashboards that update as your users interact with your product.",
            },
            {
                "type": "list",
                "variant": "unordered",
                "items": [
                    {"text": "Ask questions in plain English — no SQL required"},
                    {"text": "Real-time event streaming with sub-second latency"},
                    {
                        "text": "Auto-generated dashboards for onboarding,
                        retention,
                        and feature adoption",
                    },
                    {
                        "text": "One-click integration with Segment,
                        Amplitude,
                        and Mixpanel",
                    },
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Key Features",
            },
            {
                "type": "grid",
                "columns": [
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "headline",
                                "level": "h3",
                                "text": "Natural Language Queries",
                            },
                            {
                                "type": "paragraph",
                                "runs": [{
                                    "text": "Ask \"What percentage of users completed onboarding last week?\" and get an instant chart. No SQL,
                                    no waiting.",
                                }],
                            },
                            {
                                "type": "headline",
                                "level": "h3",
                                "text": "Funnel Analysis",
                            },
                            {
                                "type": "paragraph",
                                "runs": [{"text": "Visualize user journeys from signup to conversion. Identify drop-off points and A/B test improvements in real time."}],
                            },
                        ],
                    },
                    {
                        "column_span": 6,
                        "blocks": [
                            {
                                "type": "headline",
                                "level": "h3",
                                "text": "Cohort Retention",
                            },
                            {
                                "type": "paragraph",
                                "runs": [{
                                    "text": "Track retention by signup cohort,
                                    plan tier,
                                    or acquisition channel. See trends over 7,
                                    30,
                                    and 90-day windows.",
                                }],
                            },
                            {
                                "type": "headline",
                                "level": "h3",
                                "text": "Team Collaboration",
                            },
                            {
                                "type": "paragraph",
                                "runs": [{
                                    "text": "Share dashboards with your team via link. Add annotations,
                                    set alerts,
                                    and comment on data points directly.",
                                }],
                            },
                        ],
                    },
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Pricing",
            },
            {
                "type": "paragraph",
                "runs": [{
                    "text": "Simple,
                    transparent pricing that scales with your product.",
                }],
            },
            {
                "type": "table",
                "column_widths_in_percent": [25, 25, 25, 25],
                "header": {
                    "cells": [
                        {"text": "Feature"},
                        {
                            "text": "Starter",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "Growth",
                            "horizontal_alignment": "center",
                        },
                        {
                            "text": "Enterprise",
                            "horizontal_alignment": "center",
                        },
                    ],
                },
                "rows": [
                    {
                        "cells": [
                            {"text": "Monthly Price"},
                            {
                                "text": "EUR 299/mo",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "EUR 799/mo",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Custom",
                                "horizontal_alignment": "center",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Monthly Events"},
                            {
                                "text": "5M",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "50M",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Unlimited",
                                "horizontal_alignment": "center",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Team Members"},
                            {
                                "text": "5",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "25",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Unlimited",
                                "horizontal_alignment": "center",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Data Retention"},
                            {
                                "text": "12 months",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "24 months",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Unlimited",
                                "horizontal_alignment": "center",
                            },
                        ],
                    },
                    {
                        "cells": [
                            {"text": "Support"},
                            {
                                "text": "Email",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Priority",
                                "horizontal_alignment": "center",
                            },
                            {
                                "text": "Dedicated CSM",
                                "horizontal_alignment": "center",
                            },
                        ],
                    },
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Get Started Today",
            },
            {
                "type": "paragraph",
                "markdown": "Join **340+ product teams** already using Launchpad Analytics to ship better products, faster.",
            },
            {
                "type": "list",
                "variant": "ordered",
                "items": [
                    {"text": "Sign up for a free 14-day trial at launchpad-analytics.com"},
                    {"text": "Connect your event source in under 5 minutes"},
                    {"text": "Ask your first question and get instant insights"},
                ],
            },
            {"type": "separator"},
            {
                "type": "paragraph",
                "runs": [
                    {
                        "text": "Contact us: ",
                        "font_weight": "bold",
                    },
                    {"text": "sales@launchpad-analytics.com · (415) 555-0192 · launchpad-analytics.com"},
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
		Format: "pptx",
		Document: il.DocumentDefinition{
			Metadata: il.DocumentMetadata{
				Title:  "Launchpad Analytics — Product Launch",
				Author: "Launchpad Analytics GmbH",
			},
			Page: il.DocumentPage{
				Size:    il.DocPageSize{Preset: "A4"},
				Margins: il.DocMargins{
      TopInPt: 54,
      RightInPt: 54,
      BottomInPt: 54,
      LeftInPt: 54,
    },
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "Launchpad Analytics"),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "The Problem"),
				il.NewListBlock("unordered", []il.ListItem{
					{Text: "Average time to insight: 3–5 business days"},
					{Text: "72% of product managers rely on engineers for data queries"},
					{Text: "Only 18% of companies act on analytics within the same sprint"},
				}),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Our Solution"),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Pricing"),
				il.NewTableBlock([]il.TableRow{
					{Cells: []il.TableCell{
						{Text: "Monthly Price"},
						{Text: "EUR 299/mo"},
						{Text: "EUR 799/mo"},
						{Text: "Custom"},
					}},
					{Cells: []il.TableCell{
						{Text: "Monthly Events"},
						{Text: "5M"},
						{Text: "50M"},
						{Text: "Unlimited"},
					}},
					{Cells: []il.TableCell{
						{Text: "Team Members"},
						{Text: "5"},
						{Text: "25"},
						{Text: "Unlimited"},
					}},
				}),
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Get Started Today"),
				il.NewListBlock("ordered", []il.ListItem{
					{Text: "Sign up for a free 14-day trial at launchpad-analytics.com"},
					{Text: "Connect your event source in under 5 minutes"},
					{Text: "Ask your first question and get instant insights"},
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
  "name": "Generate Slide Deck",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Slide Deck\n\nSales and marketing teams use this recipe to generate a branded slide deck programmatically. Build a complete presentation with a title slide, problem and solution framing, feature highlights, pricing tables, and a call to action \u2014 delivered as a ready-to-present PPTX file.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "861d1ea7-09f8-4f18-8211-f2d8181e6dbe",
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
      "id": "af119061-423a-4234-b9f3-90ee441cffd4",
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
      "id": "f871e742-a288-4b9b-af6d-91d192c8e72d",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pptx",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Launchpad Analytics \\u2014 Product Launch\",\n    \"author\": \"Launchpad Analytics GmbH\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A4\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 54,\n      \"right_in_pt\": 54,\n      \"bottom_in_pt\": 54,\n      \"left_in_pt\": 54\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 14.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 32.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 14.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 12.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 12.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Launchpad Analytics\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Real-time product analytics for teams that ship fast.\",\n          \"font_weight\": \"bold\"\n        }\n      ]\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Product Launch \\u2014 Q2 2026\"\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"The Problem\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Product teams today are **flying blind**. Existing analytics tools are built for data engineers, not product managers. Teams wait days for answers to simple questions like *\\\"Which feature drives retention?\\\"* or *\\\"Where do users drop off in onboarding?\\\"*\"\n    },\n    {\n      \"type\": \"list\",\n      \"variant\": \"unordered\",\n      \"items\": [\n        {\n          \"text\": \"Average time to insight: 3\\u20135 business days\"\n        },\n        {\n          \"text\": \"72% of product managers rely on engineers for data queries\"\n        },\n        {\n          \"text\": \"Only 18% of companies act on analytics within the same sprint\"\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Our Solution\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Launchpad Analytics gives product teams **instant answers** without writing SQL. Our AI-powered query engine translates natural language questions into real-time insights, delivered as interactive dashboards that update as your users interact with your product.\"\n    },\n    {\n      \"type\": \"list\",\n      \"variant\": \"unordered\",\n      \"items\": [\n        {\n          \"text\": \"Ask questions in plain English \\u2014 no SQL required\"\n        },\n        {\n          \"text\": \"Real-time event streaming with sub-second latency\"\n        },\n        {\n          \"text\": \"Auto-generated dashboards for onboarding, retention, and feature adoption\"\n        },\n        {\n          \"text\": \"One-click integration with Segment, Amplitude, and Mixpanel\"\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Key Features\"\n    },\n    {\n      \"type\": \"grid\",\n      \"columns\": [\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"headline\",\n              \"level\": \"h3\",\n              \"text\": \"Natural Language Queries\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Ask \\\"What percentage of users completed onboarding last week?\\\" and get an instant chart. No SQL, no waiting.\"\n                }\n              ]\n            },\n            {\n              \"type\": \"headline\",\n              \"level\": \"h3\",\n              \"text\": \"Funnel Analysis\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Visualize user journeys from signup to conversion. Identify drop-off points and A/B test improvements in real time.\"\n                }\n              ]\n            }\n          ]\n        },\n        {\n          \"column_span\": 6,\n          \"blocks\": [\n            {\n              \"type\": \"headline\",\n              \"level\": \"h3\",\n              \"text\": \"Cohort Retention\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Track retention by signup cohort, plan tier, or acquisition channel. See trends over 7, 30, and 90-day windows.\"\n                }\n              ]\n            },\n            {\n              \"type\": \"headline\",\n              \"level\": \"h3\",\n              \"text\": \"Team Collaboration\"\n            },\n            {\n              \"type\": \"paragraph\",\n              \"runs\": [\n                {\n                  \"text\": \"Share dashboards with your team via link. Add annotations, set alerts, and comment on data points directly.\"\n                }\n              ]\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Pricing\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Simple, transparent pricing that scales with your product.\"\n        }\n      ]\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        25,\n        25,\n        25,\n        25\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Feature\"\n          },\n          {\n            \"text\": \"Starter\",\n            \"horizontal_alignment\": \"center\"\n          },\n          {\n            \"text\": \"Growth\",\n            \"horizontal_alignment\": \"center\"\n          },\n          {\n            \"text\": \"Enterprise\",\n            \"horizontal_alignment\": \"center\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Monthly Price\"\n            },\n            {\n              \"text\": \"EUR 299/mo\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"EUR 799/mo\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Custom\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Monthly Events\"\n            },\n            {\n              \"text\": \"5M\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"50M\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Unlimited\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Team Members\"\n            },\n            {\n              \"text\": \"5\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"25\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Unlimited\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Data Retention\"\n            },\n            {\n              \"text\": \"12 months\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"24 months\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Unlimited\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Support\"\n            },\n            {\n              \"text\": \"Email\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Priority\",\n              \"horizontal_alignment\": \"center\"\n            },\n            {\n              \"text\": \"Dedicated CSM\",\n              \"horizontal_alignment\": \"center\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Get Started Today\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Join **340+ product teams** already using Launchpad Analytics to ship better products, faster.\"\n    },\n    {\n      \"type\": \"list\",\n      \"variant\": \"ordered\",\n      \"items\": [\n        {\n          \"text\": \"Sign up for a free 14-day trial at launchpad-analytics.com\"\n        },\n        {\n          \"text\": \"Connect your event source in under 5 minutes\"\n        },\n        {\n          \"text\": \"Ask your first question and get instant insights\"\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Contact us: \",\n          \"font_weight\": \"bold\"\n        },\n        {\n          \"text\": \"sales@launchpad-analytics.com \\u00b7 (415) 555-0192 \\u00b7 launchpad-analytics.com\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "99164575-b006-4ca5-85a6-9af29ee5cf97",
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
Generate a PPTX slide deck. Use the generate_document tool with format "pptx" and these slides:

1. Title slide: [presentation title] and [subtitle/company name]
2. Problem slide: headline and bullet points describing the problem
3. Solution slide: headline and bullet points with your approach
4. Features slide: headline with a feature comparison table
5. Pricing slide: headline with a pricing table
6. CTA slide: call-to-action headline with contact details
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "UEsDBBQAAAAIAA...",
    "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
