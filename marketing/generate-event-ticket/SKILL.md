---
name: generate-event-ticket
description: Generate an event ticket image with QR code, event name, date, venue, and seat information.
---

# Generate Event Ticket

Event platforms and ticketing services use this recipe to generate branded, scannable tickets at scale. Define a dark canvas with a gradient accent bar, render the event name, date, venue, and seat details alongside a QR code — ready for mobile wallets, email delivery, or print-at-home.

## APIs Used

Image Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/image-generation/v1/render \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
        "width_in_px": 900,
        "height_in_px": 400,
    },
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#1E1B4B"
      },
      {
        "index": 1,
        "type": "gradient",
        "gradient_type": "linear",
        "angle_in_degrees": 90.0,
        "colors": [
          {
              "hex_color": "#7C3AED",
              "position": 0.0,
          },
          {
              "hex_color": "#EC4899",
              "position": 100.0,
          }
        ],
        "position": {
            "x_in_px": 0.0,
            "y_in_px": 0.0,
        },
        "dimensions": {
            "width_in_px": 900,
            "height_in_px": 8,
        }
      },
      {
        "index": 2,
        "type": "text",
        "text": "React Summit 2026",
        "font_name": "Inter",
        "font_size_in_px": 36,
        "text_color": "#FFFFFF",
        "font_weight": "bold",
        "position": {
            "x_in_px": 40.0,
            "y_in_px": 40.0,
        },
        "dimensions": {
            "width_in_px": 560,
            "height_in_px": 50,
        }
      },
      {
        "index": 3,
        "type": "text",
        "text": "June 15, 2026 — CityCube, Berlin",
        "font_name": "Inter",
        "font_size_in_px": 18,
        "text_color": "#A5B4FC",
        "position": {
            "x_in_px": 40.0,
            "y_in_px": 110.0,
        },
        "dimensions": {
            "width_in_px": 560,
            "height_in_px": 30,
        }
      },
      {
        "index": 4,
        "type": "text",
        "text": "Section B · Row 12 · Seat 7",
        "font_name": "Inter",
        "font_size_in_px": 22,
        "text_color": "#E0E7FF",
        "font_weight": "bold",
        "position": {
            "x_in_px": 40.0,
            "y_in_px": 180.0,
        },
        "dimensions": {
            "width_in_px": 560,
            "height_in_px": 40,
        }
      },
      {
        "index": 5,
        "type": "qr-code",
        "value": "TKT-2026-RS-04821",
        "position": {
            "x_in_px": 660.0,
            "y_in_px": 60.0,
        },
        "dimensions": {
            "width_in_px": 180,
            "height_in_px": 180,
        },
        "foreground_hex_color": "#FFFFFF",
        "background_hex_color": "#1E1B4B"
      },
      {
        "index": 6,
        "type": "text",
        "text": "Presented by React Summit Europe GmbH",
        "font_name": "Inter",
        "font_size_in_px": 14,
        "text_color": "#6366F1",
        "position": {
            "x_in_px": 40.0,
            "y_in_px": 340.0,
        },
        "dimensions": {
            "width_in_px": 400,
            "height_in_px": 30,
        }
      }
    ],
    "output_format": "png"
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.generateImage({
  dimensions: {
    width_in_px: 900,
    height_in_px: 400,
  },
  output_format: "png",
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#1E1B4B",
    },
    {
      index: 1,
      type: "gradient",
      gradient_type: "linear",
      angle_in_degrees: 90.0,
      colors: [
        {
          hex_color: "#7C3AED",
          position: 0.0,
        },
        {
          hex_color: "#EC4899",
          position: 100.0,
        },
      ],
      position: {
        x_in_px: 0,
        y_in_px: 0,
      },
      dimensions: {
        width_in_px: 900,
        height_in_px: 8,
      },
    },
    {
      index: 2,
      type: "text",
      text: "React Summit 2026",
      font_name: "Inter",
      font_size_in_px: 36,
      text_color: "#FFFFFF",
      font_weight: "bold",
      position: {
        x_in_px: 40,
        y_in_px: 40,
      },
      dimensions: {
        width_in_px: 560,
        height_in_px: 50,
      },
    },
    {
      index: 3,
      type: "text",
      text: "June 15, 2026 — CityCube, Berlin",
      font_name: "Inter",
      font_size_in_px: 18,
      text_color: "#A5B4FC",
      position: {
        x_in_px: 40,
        y_in_px: 110,
      },
      dimensions: {
        width_in_px: 560,
        height_in_px: 30,
      },
    },
    {
      index: 4,
      type: "text",
      text: "Section B · Row 12 · Seat 7",
      font_name: "Inter",
      font_size_in_px: 22,
      text_color: "#E0E7FF",
      font_weight: "bold",
      position: {
        x_in_px: 40,
        y_in_px: 180,
      },
      dimensions: {
        width_in_px: 560,
        height_in_px: 40,
      },
    },
    {
      index: 5,
      type: "qr-code",
      value: "TKT-2026-RS-04821",
      position: {
        x_in_px: 660,
        y_in_px: 60,
      },
      dimensions: {
        width_in_px: 180,
        height_in_px: 180,
      },
      foreground_hex_color: "#FFFFFF",
      background_hex_color: "#1E1B4B",
    },
    {
      index: 6,
      type: "text",
      text: "Presented by React Summit Europe GmbH",
      font_name: "Inter",
      font_size_in_px: 14,
      text_color: "#6366F1",
      position: {
        x_in_px: 40,
        y_in_px: 340,
      },
      dimensions: {
        width_in_px: 400,
        height_in_px: 30,
      },
    },
  ],
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_image(
    dimensions={
        "width_in_px": 900,
        "height_in_px": 400,
    },
    output_format="png",
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#1E1B4B",
        },
        {
            "index": 1,
            "type": "gradient",
            "gradient_type": "linear",
            "angle_in_degrees": 90.0,
            "colors": [
                {
                    "hex_color": "#7C3AED",
                    "position": 0.0,
                },
                {
                    "hex_color": "#EC4899",
                    "position": 100.0,
                },
            ],
            "position": {
                "x_in_px": 0,
                "y_in_px": 0,
            },
            "dimensions": {
                "width_in_px": 900,
                "height_in_px": 8,
            },
        },
        {
            "index": 2,
            "type": "text",
            "text": "React Summit 2026",
            "font_name": "Inter",
            "font_size_in_px": 36,
            "text_color": "#FFFFFF",
            "font_weight": "bold",
            "position": {
                "x_in_px": 40,
                "y_in_px": 40,
            },
            "dimensions": {
                "width_in_px": 560,
                "height_in_px": 50,
            },
        },
        {
            "index": 3,
            "type": "text",
            "text": "June 15, 2026 — CityCube, Berlin",
            "font_name": "Inter",
            "font_size_in_px": 18,
            "text_color": "#A5B4FC",
            "position": {
                "x_in_px": 40,
                "y_in_px": 110,
            },
            "dimensions": {
                "width_in_px": 560,
                "height_in_px": 30,
            },
        },
        {
            "index": 4,
            "type": "text",
            "text": "Section B · Row 12 · Seat 7",
            "font_name": "Inter",
            "font_size_in_px": 22,
            "text_color": "#E0E7FF",
            "font_weight": "bold",
            "position": {
                "x_in_px": 40,
                "y_in_px": 180,
            },
            "dimensions": {
                "width_in_px": 560,
                "height_in_px": 40,
            },
        },
        {
            "index": 5,
            "type": "qr-code",
            "value": "TKT-2026-RS-04821",
            "position": {
                "x_in_px": 660,
                "y_in_px": 60,
            },
            "dimensions": {
                "width_in_px": 180,
                "height_in_px": 180,
            },
            "foreground_hex_color": "#FFFFFF",
            "background_hex_color": "#1E1B4B",
        },
        {
            "index": 6,
            "type": "text",
            "text": "Presented by React Summit Europe GmbH",
            "font_name": "Inter",
            "font_size_in_px": 14,
            "text_color": "#6366F1",
            "position": {
                "x_in_px": 40,
                "y_in_px": 340,
            },
            "dimensions": {
                "width_in_px": 400,
                "height_in_px": 30,
            },
        },
    ],
)

```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.GenerateImage(il.GenerateImageRequest{
		Dimensions:   il.Dimensions{
    WidthInPx: 900,
    HeightInPx: 400,
  },
		OutputFormat: "png",
		Layers: []il.Layer{
			il.NewSolidColorBackgroundLayer(0, "#1E1B4B"),
			il.NewGradientLayer(1, "linear", []il.GradientColor{
				{
      HexColor: "#7C3AED",
      Position: 0.0,
    },
				{
      HexColor: "#EC4899",
      Position: 100.0,
    },
			}, il.Position{
     XInPx: 0,
     YInPx: 0,
   }, il.Dimensions{
     WidthInPx: 900,
     HeightInPx: 8,
   }),
			il.NewTextLayer(2, "React Summit 2026", "Inter", 36, "#FFFFFF",
				il.Position{
      XInPx: 40,
      YInPx: 40,
    },
				il.Dimensions{
      WidthInPx: 560,
      HeightInPx: 50,
    }),
			il.NewTextLayer(3, "June 15, 2026 — CityCube, Berlin", "Inter", 18, "#A5B4FC",
				il.Position{
      XInPx: 40,
      YInPx: 110,
    },
				il.Dimensions{
      WidthInPx: 560,
      HeightInPx: 30,
    }),
			il.NewTextLayer(4, "Section B · Row 12 · Seat 7", "Inter", 22, "#E0E7FF",
				il.Position{
      XInPx: 40,
      YInPx: 180,
    },
				il.Dimensions{
      WidthInPx: 560,
      HeightInPx: 40,
    }),
			il.NewQRCodeLayer(5, "TKT-2026-RS-04821", "#FFFFFF", "#1E1B4B",
				il.Position{
      XInPx: 660,
      YInPx: 60,
    },
				il.Dimensions{
      WidthInPx: 180,
      HeightInPx: 180,
    }),
			il.NewTextLayer(6, "Presented by React Summit Europe GmbH", "Inter", 14, "#6366F1",
				il.Position{
      XInPx: 40,
      YInPx: 340,
    },
				il.Dimensions{
      WidthInPx: 400,
      HeightInPx: 30,
    }),
		},
	})
	if err != nil {
		panic(err)
	}

}
```

```n8n
{
  "name": "Generate Event Ticket",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Event Ticket\n\nEvent platforms and ticketing services use this recipe to generate branded, scannable tickets at scale. Define a dark canvas with a gradient accent bar, render the event name, date, venue, and seat details alongside a QR code \u2014 ready for mobile wallets, email delivery, or print-at-home.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
        "height_in_px": 280,
        "width_in_px": 500,
        "color": 2
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        200,
        40
      ],
      "id": "22f3834a-43ba-4002-8404-2918fb53e4b7",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Image\nResource: **Image Generation**\n\nConfigure the Image Generation parameters below, then connect your credentials.",
        "height_in_px": 160,
        "width_in_px": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        475,
        100
      ],
      "id": "77469b6c-df54-4b25-81e7-c1864b91f48b",
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
      "id": "d4e5f6a7-4444-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 900,
        "heightInPx": 400,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"solid-color\",\"hex_color\":\"#1E1B4B\"},{\"index\":1,\"type\":\"gradient\",\"gradient_type\":\"linear\",\"angle_in_degrees\":90.0,\"colors\":[{\"hex_color\":\"#7C3AED\",\"position\":0.0},{\"hex_color\":\"#EC4899\",\"position\":100.0}],\"position\":{\"x\":0.0,\"y\":0.0},\"dimensions\":{\"width\":900,\"height\":8}},{\"index\":2,\"type\":\"text\",\"text\":\"React Summit 2026\",\"font_name\":\"Inter\",\"font_size_in_px\":36,\"text_color\":\"#FFFFFF\",\"font_weight\":\"bold\",\"position\":{\"x\":40.0,\"y\":40.0},\"dimensions\":{\"width\":560,\"height\":50}},{\"index\":3,\"type\":\"text\",\"text\":\"June 15, 2026 \\u2014 CityCube, Berlin\",\"font_name\":\"Inter\",\"font_size_in_px\":18,\"text_color\":\"#A5B4FC\",\"position\":{\"x\":40.0,\"y\":110.0},\"dimensions\":{\"width\":560,\"height\":30}},{\"index\":4,\"type\":\"text\",\"text\":\"Section B \\u00b7 Row 12 \\u00b7 Seat 7\",\"font_name\":\"Inter\",\"font_size_in_px\":22,\"text_color\":\"#E0E7FF\",\"font_weight\":\"bold\",\"position\":{\"x\":40.0,\"y\":180.0},\"dimensions\":{\"width\":560,\"height\":40}},{\"index\":5,\"type\":\"qr-code\",\"value\":\"TKT-2026-RS-04821\",\"position\":{\"x\":660.0,\"y\":60.0},\"dimensions\":{\"width\":180,\"height\":180},\"foreground_hex_color\":\"#FFFFFF\",\"background_hex_color\":\"#1E1B4B\"},{\"index\":6,\"type\":\"text\",\"text\":\"Presented by React Summit Europe GmbH\",\"font_name\":\"Inter\",\"font_size_in_px\":14,\"text_color\":\"#6366F1\",\"position\":{\"x\":40.0,\"y\":340.0},\"dimensions\":{\"width\":400,\"height\":30}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "d4e5f6a7-4444-4000-8000-000000000002",
      "name": "Generate Image",
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
            "node": "Generate Image",
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
Generate an event ticket image at 1200x500 pixels. Use the generate_image tool with these layers:

1. Background: solid-color layer with dark color
2. Accent bar: gradient layer as a decorative stripe
3. Event name: text layer with [event name] in large bold text
4. Date and time: text layer with [event date and time]
5. Venue: text layer with [venue name and address]
6. Seat info: text layer with [section, row, seat]
7. QR code: barcode layer with [ticket ID] in QR format for scanning
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/png"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
