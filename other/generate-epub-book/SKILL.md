---
name: generate-epub-book
description: Generate a complete EPUB e-book with chapters, table of contents, and rich text formatting.
---

# Generate EPUB Book

Technical publishers and self-publishing platforms use this recipe to generate an EPUB e-book from structured content. Define chapters with headings, paragraphs, and a table of contents — the API handles formatting and packaging into a valid EPUB file ready for distribution.

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
    "format": "epub",
    "document": {
      "metadata": {
        "title": "Practical Guide to Event-Driven Architecture",
        "author": "Sarah Chen"
      },
      "page": {
        "size": { "preset": "A5" },
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
            "level": "h1",
            "text": "Practical Guide to Event-Driven Architecture",
        },
        {
            "type": "paragraph",
            "markdown": "*By Sarah Chen*",
        },
        { "type": "separator" },
        {
            "type": "table-of-contents",
            "levels": ["h1", "h2"],
            "leader": "dots",
        },
        { "type": "page-break" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Chapter 1: Core Concepts",
        },
        {
            "type": "paragraph",
            "markdown": "Event-driven architecture (EDA) is a software design pattern in which the flow of the program is determined by **events** — significant changes in state that the system needs to react to. Unlike traditional request-response models,
            EDA decouples producers from consumers,
            enabling systems to scale independently.",
        },
        {
            "type": "paragraph",
            "markdown": "At its core,
            every event-driven system consists of three parts: **event producers**,
            which detect and publish state changes; **event channels**,
            which transport events between components; and **event consumers**,
            which react to incoming events by executing business logic.",
        },
        { "type": "list", "variant": "unordered", "items": [
          { "text": "Loose coupling between services" },
          { "text": "Independent scalability of producers and consumers" },
          { "text": "Natural audit trail through event logs" },
          { "text": "Resilience through asynchronous processing" }
        ]},
        { "type": "page-break" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Chapter 2: Messaging Patterns",
        },
        {
            "type": "paragraph",
            "markdown": "Choosing the right messaging pattern is critical to building a reliable event-driven system. The two most common approaches are **publish-subscribe** and **event streaming**. Publish-subscribe delivers events to all interested subscribers in real time,
            while event streaming persists events in an ordered log that consumers can replay at their own pace.",
        },
        {
            "type": "paragraph",
            "markdown": "A robust messaging layer must handle **at-least-once delivery**,
            **idempotency**,
            and **ordering guarantees**. Without these properties,
            consumers may process duplicate events,
            miss events entirely,
            or see them out of order — all of which can corrupt downstream state.",
        },
        {
          "type": "table",
          "column_widths_in_percent": [30, 35, 35],
          "header": {
            "cells": [
              { "text": "Pattern" },
              { "text": "Best For" },
              { "text": "Trade-off" }
            ]
          },
          "rows": [
            { "cells": [
              { "text": "Publish-Subscribe" },
              { "text": "Real-time notifications" },
              { "text": "No replay capability" }
            ]},
            { "cells": [
              { "text": "Event Streaming" },
              {
                  "text": "Audit logs,
                  replay",
              },
              { "text": "Higher storage cost" }
            ]},
            { "cells": [
              { "text": "Request-Reply" },
              { "text": "Synchronous workflows" },
              { "text": "Tight coupling" }
            ]}
          ]
        },
        { "type": "page-break" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Chapter 3: Implementation Strategies",
        },
        {
            "type": "paragraph",
            "markdown": "When implementing event-driven architecture in production,
            start with a **single event bus** and a small number of well-defined event types. Resist the temptation to model every state change as an event. Instead,
            focus on domain events that carry business meaning — an order was placed,
            a payment was processed,
            a shipment was dispatched.",
        },
        {
            "type": "paragraph",
            "markdown": "Adopt a **schema registry** early to enforce contracts between producers and consumers. Versioned schemas prevent breaking changes from propagating through the system and make it safe for teams to evolve their events independently.",
        },
        { "type": "list", "variant": "ordered", "items": [
          { "text": "Define your domain events and their schemas" },
          { "text": "Set up a message broker with dead-letter queues" },
          { "text": "Implement idempotent consumers with deduplication" },
          { "text": "Add monitoring and alerting for consumer lag" },
          { "text": "Introduce event versioning and a schema registry" }
        ]}
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.generateDocument({
  format: "epub",
  document: {
    metadata: {
      title: "Practical Guide to Event-Driven Architecture",
      author: "Sarah Chen",
    },
    page: {
      size: { preset: "A5" },
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
          level: "h1",
          text: "Practical Guide to Event-Driven Architecture",
      },
      {
          type: "paragraph",
          markdown: "*By Sarah Chen*",
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
          text: "Chapter 1: Core Concepts",
      },
      {
          type: "paragraph",
          markdown: "Event-driven architecture (EDA) is a software design pattern in which the flow of the program is determined by **events** — significant changes in state that the system needs to react to. Unlike traditional request-response models,
          EDA decouples producers from consumers,
          enabling systems to scale independently.",
      },
      {
          type: "paragraph",
          markdown: "At its core,
          every event-driven system consists of three parts: **event producers**,
          which detect and publish state changes; **event channels**,
          which transport events between components; and **event consumers**,
          which react to incoming events by executing business logic.",
      },
      { type: "list", variant: "unordered", items: [
        { text: "Loose coupling between services" },
        { text: "Independent scalability of producers and consumers" },
        { text: "Natural audit trail through event logs" },
        { text: "Resilience through asynchronous processing" },
      ]},
      { type: "page-break" },
      {
          type: "headline",
          level: "h1",
          text: "Chapter 2: Messaging Patterns",
      },
      {
          type: "paragraph",
          markdown: "Choosing the right messaging pattern is critical to building a reliable event-driven system. The two most common approaches are **publish-subscribe** and **event streaming**. Publish-subscribe delivers events to all interested subscribers in real time,
          while event streaming persists events in an ordered log that consumers can replay at their own pace.",
      },
      {
          type: "paragraph",
          markdown: "A robust messaging layer must handle **at-least-once delivery**,
          **idempotency**,
          and **ordering guarantees**. Without these properties,
          consumers may process duplicate events,
          miss events entirely,
          or see them out of order — all of which can corrupt downstream state.",
      },
      {
        type: "table",
        column_widths_in_percent: [30, 35, 35],
        header: {
          cells: [
            { text: "Pattern" },
            { text: "Best For" },
            { text: "Trade-off" },
          ],
        },
        rows: [
          { cells: [
            { text: "Publish-Subscribe" },
            { text: "Real-time notifications" },
            { text: "No replay capability" },
          ]},
          { cells: [
            { text: "Event Streaming" },
            {
                text: "Audit logs,
                replay",
            },
            { text: "Higher storage cost" },
          ]},
          { cells: [
            { text: "Request-Reply" },
            { text: "Synchronous workflows" },
            { text: "Tight coupling" },
          ]},
        ],
      },
      { type: "page-break" },
      {
          type: "headline",
          level: "h1",
          text: "Chapter 3: Implementation Strategies",
      },
      {
          type: "paragraph",
          markdown: "When implementing event-driven architecture in production,
          start with a **single event bus** and a small number of well-defined event types. Resist the temptation to model every state change as an event. Instead,
          focus on domain events that carry business meaning — an order was placed,
          a payment was processed,
          a shipment was dispatched.",
      },
      {
          type: "paragraph",
          markdown: "Adopt a **schema registry** early to enforce contracts between producers and consumers. Versioned schemas prevent breaking changes from propagating through the system and make it safe for teams to evolve their events independently.",
      },
      { type: "list", variant: "ordered", items: [
        { text: "Define your domain events and their schemas" },
        { text: "Set up a message broker with dead-letter queues" },
        { text: "Implement idempotent consumers with deduplication" },
        { text: "Add monitoring and alerting for consumer lag" },
        { text: "Introduce event versioning and a schema registry" },
      ]},
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_document(
    format="epub",
    document={
        "metadata": {
            "title": "Practical Guide to Event-Driven Architecture",
            "author": "Sarah Chen",
        },
        "page": {
            "size": {"preset": "A5"},
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
                "level": "h1",
                "text": "Practical Guide to Event-Driven Architecture",
            },
            {
                "type": "paragraph",
                "markdown": "*By Sarah Chen*",
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
                "text": "Chapter 1: Core Concepts",
            },
            {
                "type": "paragraph",
                "markdown": "Event-driven architecture (EDA) is a software design pattern in which the flow of the program is determined by **events** — significant changes in state that the system needs to react to. Unlike traditional request-response models,
                EDA decouples producers from consumers,
                enabling systems to scale independently.",
            },
            {
                "type": "paragraph",
                "markdown": "At its core,
                every event-driven system consists of three parts: **event producers**,
                which detect and publish state changes; **event channels**,
                which transport events between components; and **event consumers**,
                which react to incoming events by executing business logic.",
            },
            {"type": "list", "variant": "unordered", "items": [
                {"text": "Loose coupling between services"},
                {"text": "Independent scalability of producers and consumers"},
                {"text": "Natural audit trail through event logs"},
                {"text": "Resilience through asynchronous processing"},
            ]},
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Chapter 2: Messaging Patterns",
            },
            {
                "type": "paragraph",
                "markdown": "Choosing the right messaging pattern is critical to building a reliable event-driven system. The two most common approaches are **publish-subscribe** and **event streaming**. Publish-subscribe delivers events to all interested subscribers in real time,
                while event streaming persists events in an ordered log that consumers can replay at their own pace.",
            },
            {
                "type": "paragraph",
                "markdown": "A robust messaging layer must handle **at-least-once delivery**,
                **idempotency**,
                and **ordering guarantees**. Without these properties,
                consumers may process duplicate events,
                miss events entirely,
                or see them out of order — all of which can corrupt downstream state.",
            },
            {
                "type": "table",
                "column_widths_in_percent": [30, 35, 35],
                "header": {
                    "cells": [
                        {"text": "Pattern"},
                        {"text": "Best For"},
                        {"text": "Trade-off"},
                    ],
                },
                "rows": [
                    {"cells": [
                        {"text": "Publish-Subscribe"},
                        {"text": "Real-time notifications"},
                        {"text": "No replay capability"},
                    ]},
                    {"cells": [
                        {"text": "Event Streaming"},
                        {
                            "text": "Audit logs,
                            replay",
                        },
                        {"text": "Higher storage cost"},
                    ]},
                    {"cells": [
                        {"text": "Request-Reply"},
                        {"text": "Synchronous workflows"},
                        {"text": "Tight coupling"},
                    ]},
                ],
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Chapter 3: Implementation Strategies",
            },
            {
                "type": "paragraph",
                "markdown": "When implementing event-driven architecture in production,
                start with a **single event bus** and a small number of well-defined event types. Resist the temptation to model every state change as an event. Instead,
                focus on domain events that carry business meaning — an order was placed,
                a payment was processed,
                a shipment was dispatched.",
            },
            {
                "type": "paragraph",
                "markdown": "Adopt a **schema registry** early to enforce contracts between producers and consumers. Versioned schemas prevent breaking changes from propagating through the system and make it safe for teams to evolve their events independently.",
            },
            {"type": "list", "variant": "ordered", "items": [
                {"text": "Define your domain events and their schemas"},
                {"text": "Set up a message broker with dead-letter queues"},
                {"text": "Implement idempotent consumers with deduplication"},
                {"text": "Add monitoring and alerting for consumer lag"},
                {"text": "Introduce event versioning and a schema registry"},
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
	Format: "epub",
	Document: il.DocumentDefinition{
		Metadata: il.DocumentMetadata{
			Title:  "Practical Guide to Event-Driven Architecture",
			Author: "Sarah Chen",
		},
		Content: []il.ContentBlock{
			il.NewHeadlineBlock("h1", "Practical Guide to Event-Driven Architecture"),
			il.ParagraphBlock{
     Type: "paragraph",
     Markdown: "*By Sarah Chen*",
   },
			il.NewSeparatorBlock(),
			il.NewPageBreakBlock(),
			il.NewHeadlineBlock("h1", "Chapter 1: Core Concepts"),
			il.ParagraphBlock{
     Type: "paragraph",
     Markdown: "Event-driven architecture (EDA) is a software design pattern...",
   },
			il.NewHeadlineBlock("h1", "Chapter 2: Messaging Patterns"),
			il.ParagraphBlock{
     Type: "paragraph",
     Markdown: "Choosing the right messaging pattern is critical...",
   },
			il.NewHeadlineBlock("h1", "Chapter 3: Implementation Strategies"),
			il.ParagraphBlock{
     Type: "paragraph",
     Markdown: "When implementing event-driven architecture in production...",
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
  "name": "Generate EPUB Book",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate EPUB Book\n\nTechnical publishers and self-publishing platforms use this recipe to generate an EPUB e-book from structured content. Define chapters with headings, paragraphs, and a table of contents \u2014 the API handles formatting and packaging into a valid EPUB file ready for distribution.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "5ef83154-90d3-4f16-aae2-2eb0792447d2",
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
      "id": "0859a215-9a92-497e-99d7-5fbffa72c539",
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
      "id": "40dd8a1c-dd01-4281-ae11-a98d806008d8",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "epub",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"Practical Guide to Event-Driven Architecture\",\n    \"author\": \"Sarah Chen\"\n  },\n  \"page\": {\n    \"size\": {\n      \"preset\": \"A5\"\n    },\n    \"margins\": {\n      \"top_in_pt\": 54,\n      \"right_in_pt\": 54,\n      \"bottom_in_pt\": 54,\n      \"left_in_pt\": 54\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.5,\n      \"color\": \"#333333\"\n    },\n    \"headline\": {\n      \"font_family\": \"Helvetica\",\n      \"font_size_in_pt\": 24.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 6.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Helvetica\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.5,\n        \"color\": \"#333333\"\n      },\n      \"marker_color\": \"#333333\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 1.0,\n      \"spacing_before_in_pt\": 12.0,\n      \"spacing_after_in_pt\": 12.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Practical Guide to Event-Driven Architecture\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"*By Sarah Chen*\"\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"table-of-contents\",\n      \"levels\": [\n        \"h1\",\n        \"h2\"\n      ],\n      \"leader\": \"dots\"\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Chapter 1: Core Concepts\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Event-driven architecture (EDA) is a software design pattern in which the flow of the program is determined by **events** \\u2014 significant changes in state that the system needs to react to. Unlike traditional request-response models,\\n            EDA decouples producers from consumers,\\n            enabling systems to scale independently.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"At its core,\\n            every event-driven system consists of three parts: **event producers**,\\n            which detect and publish state changes; **event channels**,\\n            which transport events between components; and **event consumers**,\\n            which react to incoming events by executing business logic.\"\n    },\n    {\n      \"type\": \"list\",\n      \"variant\": \"unordered\",\n      \"items\": [\n        {\n          \"text\": \"Loose coupling between services\"\n        },\n        {\n          \"text\": \"Independent scalability of producers and consumers\"\n        },\n        {\n          \"text\": \"Natural audit trail through event logs\"\n        },\n        {\n          \"text\": \"Resilience through asynchronous processing\"\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Chapter 2: Messaging Patterns\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Choosing the right messaging pattern is critical to building a reliable event-driven system. The two most common approaches are **publish-subscribe** and **event streaming**. Publish-subscribe delivers events to all interested subscribers in real time,\\n            while event streaming persists events in an ordered log that consumers can replay at their own pace.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"A robust messaging layer must handle **at-least-once delivery**,\\n            **idempotency**,\\n            and **ordering guarantees**. Without these properties,\\n            consumers may process duplicate events,\\n            miss events entirely,\\n            or see them out of order \\u2014 all of which can corrupt downstream state.\"\n    },\n    {\n      \"type\": \"table\",\n      \"column_widths_in_percent\": [\n        30,\n        35,\n        35\n      ],\n      \"header\": {\n        \"cells\": [\n          {\n            \"text\": \"Pattern\"\n          },\n          {\n            \"text\": \"Best For\"\n          },\n          {\n            \"text\": \"Trade-off\"\n          }\n        ]\n      },\n      \"rows\": [\n        {\n          \"cells\": [\n            {\n              \"text\": \"Publish-Subscribe\"\n            },\n            {\n              \"text\": \"Real-time notifications\"\n            },\n            {\n              \"text\": \"No replay capability\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Event Streaming\"\n            },\n            {\n              \"text\": \"Audit logs,\\n                  replay\"\n            },\n            {\n              \"text\": \"Higher storage cost\"\n            }\n          ]\n        },\n        {\n          \"cells\": [\n            {\n              \"text\": \"Request-Reply\"\n            },\n            {\n              \"text\": \"Synchronous workflows\"\n            },\n            {\n              \"text\": \"Tight coupling\"\n            }\n          ]\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Chapter 3: Implementation Strategies\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"When implementing event-driven architecture in production,\\n            start with a **single event bus** and a small number of well-defined event types. Resist the temptation to model every state change as an event. Instead,\\n            focus on domain events that carry business meaning \\u2014 an order was placed,\\n            a payment was processed,\\n            a shipment was dispatched.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Adopt a **schema registry** early to enforce contracts between producers and consumers. Versioned schemas prevent breaking changes from propagating through the system and make it safe for teams to evolve their events independently.\"\n    },\n    {\n      \"type\": \"list\",\n      \"variant\": \"ordered\",\n      \"items\": [\n        {\n          \"text\": \"Define your domain events and their schemas\"\n        },\n        {\n          \"text\": \"Set up a message broker with dead-letter queues\"\n        },\n        {\n          \"text\": \"Implement idempotent consumers with deduplication\"\n        },\n        {\n          \"text\": \"Add monitoring and alerting for consumer lag\"\n        },\n        {\n          \"text\": \"Introduce event versioning and a schema registry\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "e71ccba8-093a-4a70-9d9f-614bd8864e35",
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
Generate an EPUB e-book with [book title] by [author name]. Use the generate_document tool with format "epub" and these content blocks:

- Metadata: title, author, language
- Table of contents with chapter links
- Chapter content: headlines and paragraphs for each chapter with rich text formatting
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "UEsDBBQAAAAIAA...",
    "mime_type": "application/epub+zip"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
