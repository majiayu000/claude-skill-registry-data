---
name: watermark-an-image
description: Apply a text watermark to a photo using layer-based image composition for brand protection and copyright.
---

# Watermark an Image

Photography studios and content platforms use this recipe to protect an image. Use the Image Generation API to composite a base photo with a semi-transparent text watermark overlay — ready for publishing with brand protection built in.

## APIs Used

Image Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/image-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
      "width_in_px": 1200,
      "height_in_px": 800
    },
    "layers": [
      {
        "index": 0,
        "type": "image",
        "file": {
          "type": "base64",
          "name": "photo.png",
          "base64": "<base64-encoded-photo>"
        }
      },
      {
        "index": 1,
        "type": "text",
        "text": "© 2026 Your Brand",
        "font_name": "Inter",
        "font_size_in_px": 48,
        "text_color": "#FFFFFF",
        "text_align": "center",
        "vertical_align": "center",
        "position": {
          "x_in_px": 0.0,
          "y_in_px": 0.0
        },
        "dimensions": {
          "width_in_px": 1200,
          "height_in_px": 800
        },
        "opacity": 30,
        "rotation_in_degrees": -30.0
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
    width_in_px: 1200,
    height_in_px: 800,
  },
  layers: [
    {
      index: 0,
      type: "image",
      file: {
        type: "base64",
        name: "photo.png",
        base64: "<base64-encoded-photo>",
      },
    },
    {
      index: 1,
      type: "text",
      text: "\u00a9 2026 Your Brand",
      font_name: "Inter",
      font_size_in_px: 48,
      text_color: "#FFFFFF",
      text_align: "center",
      vertical_align: "center",
      position: {
        x_in_px: 0,
        y_in_px: 0,
      },
      dimensions: {
        width_in_px: 1200,
        height_in_px: 800,
      },
      opacity: 30,
      rotation_in_degrees: -30.0,
    },
  ],
  output_format: "png",
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_image(
    dimensions={
        "width_in_px": 1200,
        "height_in_px": 800,
    },
    layers=[
        {
            "index": 0,
            "type": "image",
            "file": {
                "type": "base64",
                "name": "photo.png",
                "base64": "<base64-encoded-photo>",
            },
        },
        {
            "index": 1,
            "type": "text",
            "text": "\u00a9 2026 Your Brand",
            "font_name": "Inter",
            "font_size_in_px": 48,
            "text_color": "#FFFFFF",
            "text_align": "center",
            "vertical_align": "center",
            "position": {
                "x_in_px": 0,
                "y_in_px": 0,
            },
            "dimensions": {
                "width_in_px": 1200,
                "height_in_px": 800,
            },
            "opacity": 30,
            "rotation_in_degrees": -30.0,
        },
    ],
    output_format="png",
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.GenerateImage(il.GenerateImageRequest{
		Dimensions: il.Dimensions{
			WidthInPx:  1200,
			HeightInPx: 800,
		},
		OutputFormat: "png",
		Layers: []il.Layer{
			il.NewImageOverlayLayer(0, il.FileInput{Buffer: "<base64-encoded-photo>"}),
			il.NewTextLayer(1, "\u00a9 2026 Your Brand", "Inter", 48, "#FFFFFF",
				il.Position{
      XInPx: 0,
      YInPx: 0,
    },
				il.Dimensions{
      WidthInPx: 1200,
      HeightInPx: 800,
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
  "name": "Watermark an Image",
  "nodes": [
    {
      "parameters": {
        "content": "## Watermark an Image\n\nPhotography studios and content platforms use this recipe to protect an image. Use the Image Generation API to composite a base photo with a semi-transparent text watermark overlay \u2014 ready for publishing with brand protection built in.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "9049670b-9497-40cd-b116-5546e05689ac",
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
      "id": "eeb9ad8f-c871-42bf-a922-3743978f8cf5",
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
      "id": "db37dbb5-6d26-42d3-8562-bd9118648edd",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 1200,
        "heightInPx": 800,
        "outputFormat": "png",
        "layersJson": "[\n  {\n    \"index\": 0,\n    \"type\": \"image\",\n    \"file\": {\n      \"type\": \"base64\",\n      \"name\": \"photo.png\",\n      \"base64\": \"<base64-encoded-photo>\"\n    }\n  },\n  {\n    \"index\": 1,\n    \"type\": \"text\",\n    \"text\": \"\\u00a9 2026 Your Brand\",\n    \"font_name\": \"Inter\",\n    \"font_size_in_px\": 48,\n    \"text_color\": \"#FFFFFF\",\n    \"text_align\": \"center\",\n    \"vertical_align\": \"center\",\n    \"position\": {\n      \"x\": 0.0,\n      \"y\": 0.0\n    },\n    \"dimensions\": {\n      \"width\": 1200,\n      \"height\": 800\n    },\n    \"opacity\": 30,\n    \"rotation_in_degrees\": -30.0\n  }\n]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "66c9ebb5-6532-463c-9980-3cb8b07d7e35",
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
Add a watermark to the image at [file URL]. Use the generate_image tool with an image layer for the base photo and a text layer for the watermark "[watermark text]", set to semi-transparent with rotation, output as PNG.
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
