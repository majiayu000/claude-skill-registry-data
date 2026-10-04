---
name: generate-front-book-cover
description: Generate a front cover image with custom artwork, title text, and author attribution.
---

# Generate Front Book Cover

Self-publishing authors and digital bookstores use this recipe to generate a professional front book cover. Define a canvas with a gradient background, add title and author text — ready for ebook stores, print-on-demand, or preview thumbnails.

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
      "width_in_px": 600,
      "height_in_px": 900
    },
    "output_format": "png",
    "layers": [
      {
        "index": 0,
        "type": "gradient",
        "gradient_type": "linear",
        "angle_in_degrees": 180.0,
        "colors": [
          {
              "hex_color": "#1B1464",
              "position": 0.0,
          },
          {
              "hex_color": "#6C63FF",
              "position": 100.0,
          }
        ],
        "position": {
            "x_in_px": 0.0,
            "y_in_px": 0.0,
        },
        "dimensions": {
            "width_in_px": 600,
            "height_in_px": 900,
        }
      },
      {
        "index": 1,
        "type": "text",
        "text": "The Art of API Design",
        "font_name": "Playfair Display",
        "font_size_in_px": 52,
        "text_color": "#FFFFFF",
        "font_weight": "bold",
        "text_align": "center",
        "position": {
            "x_in_px": 50.0,
            "y_in_px": 200.0,
        },
        "dimensions": {
            "width_in_px": 500,
            "height_in_px": 200,
        }
      },
      {
        "index": 2,
        "type": "text",
        "text": "Alexandra Chen",
        "font_name": "Inter",
        "font_size_in_px": 24,
        "text_color": "#D4D0FF",
        "text_align": "center",
        "position": {
            "x_in_px": 50.0,
            "y_in_px": 750.0,
        },
        "dimensions": {
            "width_in_px": 500,
            "height_in_px": 40,
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
    width_in_px: 600,
    height_in_px: 900,
  },
  output_format: "png",
  layers: [
    {
      index: 0,
      type: "gradient",
      gradient_type: "linear",
      angle_in_degrees: 180.0,
      colors: [
        {
          hex_color: "#1B1464",
          position: 0.0,
        },
        {
          hex_color: "#6C63FF",
          position: 100.0,
        },
      ],
      position: {
        x_in_px: 0.0,
        y_in_px: 0.0,
      },
      dimensions: {
        width_in_px: 600,
        height_in_px: 900,
      },
    },
    {
      index: 1,
      type: "text",
      text: "The Art of API Design",
      font_name: "Playfair Display",
      font_size_in_px: 52,
      text_color: "#FFFFFF",
      font_weight: "bold",
      text_align: "center",
      position: {
        x_in_px: 50.0,
        y_in_px: 200.0,
      },
      dimensions: {
        width_in_px: 500,
        height_in_px: 200,
      },
    },
    {
      index: 2,
      type: "text",
      text: "Alexandra Chen",
      font_name: "Inter",
      font_size_in_px: 24,
      text_color: "#D4D0FF",
      text_align: "center",
      position: {
        x_in_px: 50.0,
        y_in_px: 750.0,
      },
      dimensions: {
        width_in_px: 500,
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
        "width_in_px": 600,
        "height_in_px": 900,
    },
    output_format="png",
    layers=[
        {
            "index": 0,
            "type": "gradient",
            "gradient_type": "linear",
            "angle_in_degrees": 180.0,
            "colors": [
                {
                    "hex_color": "#1B1464",
                    "position": 0.0,
                },
                {
                    "hex_color": "#6C63FF",
                    "position": 100.0,
                },
            ],
            "position": {
                "x_in_px": 0.0,
                "y_in_px": 0.0,
            },
            "dimensions": {
                "width_in_px": 600,
                "height_in_px": 900,
            },
        },
        {
            "index": 1,
            "type": "text",
            "text": "The Art of API Design",
            "font_name": "Playfair Display",
            "font_size_in_px": 52,
            "text_color": "#FFFFFF",
            "font_weight": "bold",
            "text_align": "center",
            "position": {
                "x_in_px": 50.0,
                "y_in_px": 200.0,
            },
            "dimensions": {
                "width_in_px": 500,
                "height_in_px": 200,
            },
        },
        {
            "index": 2,
            "type": "text",
            "text": "Alexandra Chen",
            "font_name": "Inter",
            "font_size_in_px": 24,
            "text_color": "#D4D0FF",
            "text_align": "center",
            "position": {
                "x_in_px": 50.0,
                "y_in_px": 750.0,
            },
            "dimensions": {
                "width_in_px": 500,
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

	result, err := client.GenerateImage(il.GenerateImageRequest{
		Dimensions:   il.Dimensions{
    WidthInPx: 600,
    HeightInPx: 900,
  },
		OutputFormat: "png",
		Layers: []il.Layer{
			il.NewGradientLayer(0, "linear", []il.GradientColor{
				{
      HexColor: "#1B1464",
      Position: 0.0,
    },
				{
      HexColor: "#6C63FF",
      Position: 100.0,
    },
			}, il.Position{
     XInPx: 0.0,
     YInPx: 0.0,
   }, il.Dimensions{
     WidthInPx: 600,
     HeightInPx: 900,
   }),
			il.NewTextLayer(1, "The Art of API Design", "Playfair Display", 52, "#FFFFFF",
				il.Position{
      XInPx: 50.0,
      YInPx: 200.0,
    }, il.Dimensions{
      WidthInPx: 500,
      HeightInPx: 200,
    }),
			il.NewTextLayer(2, "Alexandra Chen", "Inter", 24, "#D4D0FF",
				il.Position{
      XInPx: 50.0,
      YInPx: 750.0,
    }, il.Dimensions{
      WidthInPx: 500,
      HeightInPx: 40,
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
  "name": "Generate Front Book Cover",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Front Book Cover\n\nSelf-publishing authors and digital bookstores use this recipe to generate a professional front book cover. Define a canvas with a gradient background, add title and author text \u2014 ready for ebook stores, print-on-demand, or preview thumbnails.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "2f477ffc-eba2-4829-8db5-82e606bc4183",
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
      "id": "5d8a159e-9e83-45a3-b106-20223749588a",
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
      "id": "e5f6a7b8-5555-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 600,
        "heightInPx": 900,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"gradient\",\"gradient_type\":\"linear\",\"angle_in_degrees\":180.0,\"colors\":[{\"hex_color\":\"#1B1464\",\"position\":0.0},{\"hex_color\":\"#6C63FF\",\"position\":100.0}],\"position\":{\"x\":0.0,\"y\":0.0},\"dimensions\":{\"width\":600,\"height\":900}},{\"index\":1,\"type\":\"text\",\"text\":\"The Art of API Design\",\"font_name\":\"Playfair Display\",\"font_size_in_px\":52,\"text_color\":\"#FFFFFF\",\"font_weight\":\"bold\",\"text_align\":\"center\",\"position\":{\"x\":50.0,\"y\":200.0},\"dimensions\":{\"width\":500,\"height\":200}},{\"index\":2,\"type\":\"text\",\"text\":\"Alexandra Chen\",\"font_name\":\"Inter\",\"font_size_in_px\":24,\"text_color\":\"#D4D0FF\",\"text_align\":\"center\",\"position\":{\"x\":50.0,\"y\":750.0},\"dimensions\":{\"width\":500,\"height\":40}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "e5f6a7b8-5555-4000-8000-000000000002",
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
Generate a front book cover image at 1800x2700 pixels. Use the generate_image tool with these layers:

1. Background: gradient layer with [color scheme]
2. Title: text layer with [book title] in large bold serif font, centered
3. Author: text layer with [author name] positioned near the bottom
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
