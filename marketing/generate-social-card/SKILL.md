---
name: generate-social-card
description: Generate an Open Graph social sharing card with dynamic title, description, and branding.
---

# Generate Social Card

Content platforms and developer blogs use this recipe to generate an Open Graph image for social sharing. Define a canvas with your brand background and render the article title, description, and site name — ready for an og:image meta tag with a consistent, eye-catching preview.

## APIs Used

Image Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST \
  https://api.iterationlayer.com/image-generation/v1/render \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
      "width_in_px": 1200,
      "height_in_px": 630
    },
    "output_format": "png",
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#0F172A"
      },
      {
        "index": 1,
        "type": "text",
        "text": "Building Scalable APIs with Elixir",
        "font_name": "Inter",
        "font_size_in_px": 48,
        "text_color": "#FFFFFF",
        "font_weight": "bold",
        "position": {
          "x_in_px": 80.0,
          "y_in_px": 120.0
        },
        "dimensions": {
          "width_in_px": 1040,
          "height_in_px": 200
        }
      },
      {
        "index": 2,
        "type": "text",
        "text": "A practical guide to designing fault-tolerant API services",
        "font_name": "Inter",
        "font_size_in_px": 24,
        "text_color": "#94A3B8",
        "position": {
          "x_in_px": 80.0,
          "y_in_px": 360.0
        },
        "dimensions": {
          "width_in_px": 1040,
          "height_in_px": 80
        }
      },
      {
        "index": 3,
        "type": "text",
        "text": "iterationlayer.com",
        "font_name": "Inter",
        "font_size_in_px": 20,
        "text_color": "#6366F1",
        "position": {
          "x_in_px": 80.0,
          "y_in_px": 530.0
        },
        "dimensions": {
          "width_in_px": 400,
          "height_in_px": 40
        }
      }
    ]
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.generateImage({
  dimensions: {
    width_in_px: 1200,
    height_in_px: 630,
  },
  output_format: "png",
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#0F172A",
    },
    {
      index: 1,
      type: "text",
      text: "Building Scalable APIs with Elixir",
      font_name: "Inter",
      font_size_in_px: 48,
      text_color: "#FFFFFF",
      font_weight: "bold",
      position: {
        x_in_px: 80.0,
        y_in_px: 120.0,
      },
      dimensions: {
        width_in_px: 1040,
        height_in_px: 200,
      },
    },
    {
      index: 2,
      type: "text",
      text: "A practical guide to designing fault-tolerant API services",
      font_name: "Inter",
      font_size_in_px: 24,
      text_color: "#94A3B8",
      position: {
        x_in_px: 80.0,
        y_in_px: 360.0,
      },
      dimensions: {
        width_in_px: 1040,
        height_in_px: 80,
      },
    },
    {
      index: 3,
      type: "text",
      text: "iterationlayer.com",
      font_name: "Inter",
      font_size_in_px: 20,
      text_color: "#6366F1",
      position: {
        x_in_px: 80.0,
        y_in_px: 530.0,
      },
      dimensions: {
        width_in_px: 400,
        height_in_px: 40,
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
        "width_in_px": 1200,
        "height_in_px": 630,
    },
    output_format="png",
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#0F172A",
        },
        {
            "index": 1,
            "type": "text",
            "text": "Building Scalable APIs with Elixir",
            "font_name": "Inter",
            "font_size_in_px": 48,
            "text_color": "#FFFFFF",
            "font_weight": "bold",
            "position": {
                "x_in_px": 80.0,
                "y_in_px": 120.0,
            },
            "dimensions": {
                "width_in_px": 1040,
                "height_in_px": 200,
            },
        },
        {
            "index": 2,
            "type": "text",
            "text": "A practical guide to designing fault-tolerant API services",
            "font_name": "Inter",
            "font_size_in_px": 24,
            "text_color": "#94A3B8",
            "position": {
                "x_in_px": 80.0,
                "y_in_px": 360.0,
            },
            "dimensions": {
                "width_in_px": 1040,
                "height_in_px": 80,
            },
        },
        {
            "index": 3,
            "type": "text",
            "text": "iterationlayer.com",
            "font_name": "Inter",
            "font_size_in_px": 20,
            "text_color": "#6366F1",
            "position": {
                "x_in_px": 80.0,
                "y_in_px": 530.0,
            },
            "dimensions": {
                "width_in_px": 400,
                "height_in_px": 40,
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

	result, err := client.GenerateImage(
		il.GenerateImageRequest{
			Dimensions: il.Dimensions{
				WidthInPx:  1200,
				HeightInPx: 630,
			},
			OutputFormat: "png",
			Layers: []il.Layer{
				il.NewSolidColorBackgroundLayer(0, "#0F172A"),
				il.NewTextLayer(
					1,
					"Building Scalable APIs with Elixir",
					"Inter", 48, "#FFFFFF",
					il.Position{
       XInPx: 80.0,
       YInPx: 120.0,
     },
					il.Dimensions{
       WidthInPx: 1040,
       HeightInPx: 200,
     },
				),
				il.NewTextLayer(
					2,
					"A practical guide to designing fault-tolerant API services",
					"Inter", 24, "#94A3B8",
					il.Position{
       XInPx: 80.0,
       YInPx: 360.0,
     },
					il.Dimensions{
       WidthInPx: 1040,
       HeightInPx: 80,
     },
				),
				il.NewTextLayer(
					3, "iterationlayer.com",
					"Inter", 20, "#6366F1",
					il.Position{
       XInPx: 80.0,
       YInPx: 530.0,
     },
					il.Dimensions{
       WidthInPx: 400,
       HeightInPx: 40,
     },
				),
			},
		},
	)
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Generate Social Card",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Social Card\n\nContent platforms and developer blogs use this recipe to generate an Open Graph image for social sharing. Define a canvas with your brand background and render the article title, description, and site name \u2014 ready for an og:image meta tag with a consistent, eye-catching preview.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "96376d68-9d87-4f29-82e1-7c971434dc25",
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
      "id": "77153d06-46d8-44fd-a90e-e50399008afa",
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
      "id": "f2a3b4c5-cccc-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 1200,
        "heightInPx": 630,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"solid-color\",\"hex_color\":\"#0F172A\"},{\"index\":1,\"type\":\"text\",\"text\":\"Building Scalable APIs with Elixir\",\"font_name\":\"Inter\",\"font_size_in_px\":48,\"text_color\":\"#FFFFFF\",\"font_weight\":\"bold\",\"position\":{\"x\":80.0,\"y\":120.0},\"dimensions\":{\"width\":1040,\"height\":200}},{\"index\":2,\"type\":\"text\",\"text\":\"A practical guide to designing fault-tolerant API services\",\"font_name\":\"Inter\",\"font_size_in_px\":24,\"text_color\":\"#94A3B8\",\"position\":{\"x\":80.0,\"y\":360.0},\"dimensions\":{\"width\":1040,\"height\":80}},{\"index\":3,\"type\":\"text\",\"text\":\"iterationlayer.com\",\"font_name\":\"Inter\",\"font_size_in_px\":20,\"text_color\":\"#6366F1\",\"position\":{\"x\":80.0,\"y\":530.0},\"dimensions\":{\"width\":400,\"height\":40}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "f2a3b4c5-cccc-4000-8000-000000000002",
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
Generate an Open Graph social card at 1200x630 pixels. Use the generate_image tool with these layers:

1. Background: solid-color layer with [brand background color]
2. Title: text layer with [article title] in large bold text, white
3. Description: text layer with [article description] in smaller text
4. Site name: text layer with [site name] positioned at the bottom
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
