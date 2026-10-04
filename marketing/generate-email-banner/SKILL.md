---
name: generate-email-banner
description: Generate a personalized email banner image with text, logo, and brand colors.
---

# Generate Email Banner

Marketing teams and email platforms use this recipe to generate a personalized banner image for an email campaign. Define a canvas with your brand colors, add a logo and headline text — ready for embedding in an HTML email.

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
      "height_in_px": 200
    },
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#1a1a2e"
      },
      {
        "index": 1,
        "type": "image",
        "file": {
          "type": "base64",
          "name": "logo.png",
          "base64": "<base64-encoded-logo>"
        },
        "position": {
          "x_in_px": 20.0,
          "y_in_px": 50.0
        }
      },
      {
        "index": 2,
        "type": "text",
        "text": "Summer Sale — 30% Off",
        "font_name": "Montserrat",
        "font_size_in_px": 36,
        "text_color": "#FFFFFF",
        "position": {
          "x_in_px": 150.0,
          "y_in_px": 40.0
        },
        "dimensions": {
          "width_in_px": 420,
          "height_in_px": 50
        }
      },
      {
        "index": 3,
        "type": "text",
        "text": "Shop now at example.com",
        "font_name": "Inter",
        "font_size_in_px": 18,
        "text_color": "#E94560",
        "position": {
          "x_in_px": 150.0,
          "y_in_px": 110.0
        },
        "dimensions": {
          "width_in_px": 420,
          "height_in_px": 40
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
    width_in_px: 600,
    height_in_px: 200,
  },
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#1a1a2e",
    },
    {
      index: 1,
      type: "image",
      file: {
        type: "base64",
        name: "logo.png",
        base64: "<base64-encoded-logo>",
      },
      position: {
        x_in_px: 20,
        y_in_px: 50,
      },
    },
    {
      index: 2,
      type: "text",
      text: "Summer Sale — 30% Off",
      font_name: "Montserrat",
      font_size_in_px: 36,
      text_color: "#FFFFFF",
      position: {
        x_in_px: 150,
        y_in_px: 40,
      },
      dimensions: {
        width_in_px: 420,
        height_in_px: 50,
      },
    },
    {
      index: 3,
      type: "text",
      text: "Shop now at example.com",
      font_name: "Inter",
      font_size_in_px: 18,
      text_color: "#E94560",
      position: {
        x_in_px: 150,
        y_in_px: 110,
      },
      dimensions: {
        width_in_px: 420,
        height_in_px: 40,
      },
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
        "width_in_px": 600,
        "height_in_px": 200,
    },
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#1a1a2e",
        },
        {
            "index": 1,
            "type": "image",
            "file": {
                "type": "base64",
                "name": "logo.png",
                "base64": "<base64-encoded-logo>",
            },
            "position": {
                "x_in_px": 20,
                "y_in_px": 50,
            },
        },
        {
            "index": 2,
            "type": "text",
            "text": "Summer Sale — 30% Off",
            "font_name": "Montserrat",
            "font_size_in_px": 36,
            "text_color": "#FFFFFF",
            "position": {
                "x_in_px": 150,
                "y_in_px": 40,
            },
            "dimensions": {
                "width_in_px": 420,
                "height_in_px": 50,
            },
        },
        {
            "index": 3,
            "type": "text",
            "text": "Shop now at example.com",
            "font_name": "Inter",
            "font_size_in_px": 18,
            "text_color": "#E94560",
            "position": {
                "x_in_px": 150,
                "y_in_px": 110,
            },
            "dimensions": {
                "width_in_px": 420,
                "height_in_px": 40,
            },
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
	Dimensions:   il.Dimensions{
   WidthInPx: 600,
   HeightInPx: 200,
 },
	OutputFormat: "png",
	Layers: []il.Layer{
		il.NewSolidColorBackgroundLayer(0, "#1a1a2e"),
		il.NewStaticImageLayer(1, il.FileInput{Buffer: "<base64-encoded-logo>"},
			il.Position{
     XInPx: 20,
     YInPx: 50,
   },
			il.Dimensions{}),
		il.NewTextLayer(2, "Summer Sale — 30% Off", "Montserrat", 36, "#FFFFFF",
			il.Position{
     XInPx: 150,
     YInPx: 40,
   },
			il.Dimensions{
     WidthInPx: 420,
     HeightInPx: 50,
   }),
		il.NewTextLayer(3, "Shop now at example.com", "Inter", 18, "#E94560",
			il.Position{
     XInPx: 150,
     YInPx: 110,
   },
			il.Dimensions{
     WidthInPx: 420,
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
  "name": "Generate Email Banner",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Email Banner\n\nMarketing teams and email platforms use this recipe to generate a personalized banner image for an email campaign. Define a canvas with your brand colors, add a logo and headline text \u2014 ready for embedding in an HTML email.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "2b832304-5d48-4e5c-9e83-07b063406a5b",
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
      "id": "6f305649-000c-4ba4-9b19-147a59361d0f",
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
      "id": "c3d4e5f6-3333-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 600,
        "heightInPx": 200,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"solid-color\",\"hex_color\":\"#1a1a2e\"},{\"index\":1,\"type\":\"image\",\"file\":{\"type\":\"base64\",\"name\":\"logo.png\",\"base64\":\"<base64-encoded-logo>\"},\"position\":{\"x\":20.0,\"y\":50.0}},{\"index\":2,\"type\":\"text\",\"text\":\"Summer Sale \\u2014 30% Off\",\"font_name\":\"Montserrat\",\"font_size_in_px\":36,\"text_color\":\"#FFFFFF\",\"position\":{\"x\":150.0,\"y\":40.0},\"dimensions\":{\"width\":420,\"height\":50}},{\"index\":3,\"type\":\"text\",\"text\":\"Shop now at example.com\",\"font_name\":\"Inter\",\"font_size_in_px\":18,\"text_color\":\"#E94560\",\"position\":{\"x\":150.0,\"y\":110.0},\"dimensions\":{\"width\":420,\"height\":40}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "c3d4e5f6-3333-4000-8000-000000000002",
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
Generate a personalized email banner image at 600x200 pixels. Use the generate_image tool with these layers:

1. Background: gradient layer with [brand colors]
2. Logo: image layer with [logo URL] positioned left
3. Headline: text layer with [campaign headline] in bold white text
4. Subtext: text layer with [supporting text] in smaller font
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
