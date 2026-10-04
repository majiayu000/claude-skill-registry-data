---
name: generate-og-image
description: Generate a branded Open Graph image with a generative wave background, logo, and tagline.
---

# Generate OG Image

Sites and apps use this recipe to generate a unique, branded OG image per page. A solid-color canvas holds a decorative background image with rounded corners, a logo, the brand name, and a tagline — ready to serve as an og:image meta tag.

## APIs Used

Image Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST \
  https://api.iterationlayer.com/image-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
        "width_in_px": 1200,
        "height_in_px": 630,
    },
    "output_format": "jpeg",
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#FFFFFF"
      },
      {
        "index": 1,
        "type": "image",
        "file": {
            "type": "url",
            "name": "background.png",
            "url": "https://example.com/background.png",
        },
        "position": {
            "x_in_px": 20.0,
            "y_in_px": 20.0,
        },
        "dimensions": {
            "width_in_px": 1160,
            "height_in_px": 478,
        },
        "border_radius": 24
      },
      {
        "index": 2,
        "type": "image",
        "file": {
            "type": "url",
            "name": "logo.svg",
            "url": "https://example.com/logo.svg",
        },
        "position": {
            "x_in_px": 20.0,
            "y_in_px": 542.0,
        },
        "dimensions": {
            "width_in_px": 56,
            "height_in_px": 56,
        }
      },
      {
        "index": 3,
        "type": "text",
        "text": "Nordlicht GmbH",
        "font_name": "Inter",
        "font_size_in_px": 32,
        "font_weight": "bold",
        "text_color": "#000000",
        "text_align": "left",
        "vertical_align": "center",
        "position": {
            "x_in_px": 90.0,
            "y_in_px": 542.0,
        },
        "dimensions": {
            "width_in_px": 300,
            "height_in_px": 56,
        }
      },
      {
        "index": 4,
        "type": "text",
        "text": "Build faster with our platform",
        "font_name": "Inter",
        "font_size_in_px": 28,
        "font_weight": "medium",
        "text_color": "#6B7280",
        "text_align": "right",
        "vertical_align": "center",
        "should_auto_scale": true,
        "position": {
            "x_in_px": 20.0,
            "y_in_px": 542.0,
        },
        "dimensions": {
            "width_in_px": 1160,
            "height_in_px": 56,
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
  output_format: "jpeg",
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#FFFFFF",
    },
    {
      index: 1,
      type: "image",
      file: {
        type: "url",
        name: "background.png",
        url: "https://example.com/background.png",
      },
      position: {
        x_in_px: 20,
        y_in_px: 20,
      },
      dimensions: {
        width_in_px: 1160,
        height_in_px: 478,
      },
      border_radius: 24,
    },
    {
      index: 2,
      type: "image",
      file: {
        type: "url",
        name: "logo.svg",
        url: "https://example.com/logo.svg",
      },
      position: {
        x_in_px: 20,
        y_in_px: 542,
      },
      dimensions: {
        width_in_px: 56,
        height_in_px: 56,
      },
    },
    {
      index: 3,
      type: "text",
      text: "Nordlicht GmbH",
      font_name: "Inter",
      font_size_in_px: 32,
      font_weight: "bold",
      text_color: "#000000",
      text_align: "left",
      vertical_align: "center",
      position: {
        x_in_px: 90,
        y_in_px: 542,
      },
      dimensions: {
        width_in_px: 300,
        height_in_px: 56,
      },
    },
    {
      index: 4,
      type: "text",
      text: "Build faster with our platform",
      font_name: "Inter",
      font_size_in_px: 28,
      font_weight: "medium",
      text_color: "#6B7280",
      text_align: "right",
      vertical_align: "center",
      should_auto_scale: true,
      position: {
        x_in_px: 20,
        y_in_px: 542,
      },
      dimensions: {
        width_in_px: 1160,
        height_in_px: 56,
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
    output_format="jpeg",
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#FFFFFF",
        },
        {
            "index": 1,
            "type": "image",
            "file": {
                "type": "url",
                "name": "background.png",
                "url": "https://example.com/background.png",
            },
            "position": {
                "x_in_px": 20,
                "y_in_px": 20,
            },
            "dimensions": {
                "width_in_px": 1160,
                "height_in_px": 478,
            },
            "border_radius": 24,
        },
        {
            "index": 2,
            "type": "image",
            "file": {
                "type": "url",
                "name": "logo.svg",
                "url": "https://example.com/logo.svg",
            },
            "position": {
                "x_in_px": 20,
                "y_in_px": 542,
            },
            "dimensions": {
                "width_in_px": 56,
                "height_in_px": 56,
            },
        },
        {
            "index": 3,
            "type": "text",
            "text": "Nordlicht GmbH",
            "font_name": "Inter",
            "font_size_in_px": 32,
            "font_weight": "bold",
            "text_color": "#000000",
            "text_align": "left",
            "vertical_align": "center",
            "position": {
                "x_in_px": 90,
                "y_in_px": 542,
            },
            "dimensions": {
                "width_in_px": 300,
                "height_in_px": 56,
            },
        },
        {
            "index": 4,
            "type": "text",
            "text": "Build faster with our platform",
            "font_name": "Inter",
            "font_size_in_px": 28,
            "font_weight": "medium",
            "text_color": "#6B7280",
            "text_align": "right",
            "vertical_align": "center",
            "should_auto_scale": True,
            "position": {
                "x_in_px": 20,
                "y_in_px": 542,
            },
            "dimensions": {
                "width_in_px": 1160,
                "height_in_px": 56,
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
			Dimensions:   il.Dimensions{
     WidthInPx: 1200,
     HeightInPx: 630,
   },
			OutputFormat: "jpeg",
			Layers: []il.Layer{
				il.NewSolidColorBackgroundLayer(0, "#FFFFFF"),
				il.NewImageLayer(
					1,
					il.FileInput{Type: "url", Name: "background.png", Url: "https://example.com/background.png"},
					il.Position{
       XInPx: 20,
       YInPx: 20,
     },
					il.Dimensions{
       WidthInPx: 1160,
       HeightInPx: 478,
     },
				),
				il.NewImageLayer(
					2,
					il.FileInput{Type: "url", Name: "logo.svg", Url: "https://example.com/logo.svg"},
					il.Position{
       XInPx: 20,
       YInPx: 542,
     },
					il.Dimensions{
       WidthInPx: 56,
       HeightInPx: 56,
     },
				),
				il.NewTextLayer(
					3, "Nordlicht GmbH",
					"Inter", 32, "#000000",
					il.Position{
       XInPx: 90,
       YInPx: 542,
     },
					il.Dimensions{
       WidthInPx: 300,
       HeightInPx: 56,
     },
				),
				il.NewTextLayer(
					4, "Build faster with our platform",
					"Inter", 28, "#6B7280",
					il.Position{
       XInPx: 20,
       YInPx: 542,
     },
					il.Dimensions{
       WidthInPx: 1160,
       HeightInPx: 56,
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
  "name": "Generate OG Image",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate OG Image\n\nSites and apps use this recipe to generate a unique, branded OG image per page. A solid-color canvas holds a decorative background image with rounded corners, a logo, the brand name, and a tagline \u2014 ready to serve as an og:image meta tag.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "870009e9-dee8-4568-8367-98332d39cd2f",
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
      "id": "78a96ff7-e05d-4dc9-b20e-87457c906808",
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
      "id": "f6a7b8c9-6666-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 1200,
        "heightInPx": 630,
        "outputFormat": "jpeg",
        "layersJson": "[{\"index\":0,\"type\":\"solid-color\",\"hex_color\":\"#FFFFFF\"},{\"index\":1,\"type\":\"image\",\"file\":{\"type\":\"url\",\"name\":\"background.png\",\"url\":\"https://example.com/background.png\"},\"position\":{\"x\":20.0,\"y\":20.0},\"dimensions\":{\"width\":1160,\"height\":478},\"border_radius\":24},{\"index\":2,\"type\":\"image\",\"file\":{\"type\":\"url\",\"name\":\"logo.svg\",\"url\":\"https://example.com/logo.svg\"},\"position\":{\"x\":20.0,\"y\":542.0},\"dimensions\":{\"width\":56,\"height\":56}},{\"index\":3,\"type\":\"text\",\"text\":\"Nordlicht GmbH\",\"font_name\":\"Inter\",\"font_size_in_px\":32,\"font_weight\":\"bold\",\"text_color\":\"#000000\",\"text_align\":\"left\",\"vertical_align\":\"center\",\"position\":{\"x\":90.0,\"y\":542.0},\"dimensions\":{\"width\":300,\"height\":56}},{\"index\":4,\"type\":\"text\",\"text\":\"Build faster with our platform\",\"font_name\":\"Inter\",\"font_size_in_px\":28,\"font_weight\":\"medium\",\"text_color\":\"#6B7280\",\"text_align\":\"right\",\"vertical_align\":\"center\",\"should_auto_scale\":true,\"position\":{\"x\":20.0,\"y\":542.0},\"dimensions\":{\"width\":1160,\"height\":56}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "f6a7b8c9-6666-4000-8000-000000000002",
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
Generate a branded OG image with dimensions 1200x630 pixels. Use the generate_image tool with these layers:

1. Background: solid-color layer with [background color]
2. Background art: image layer with [background image URL] positioned with rounded corners
3. Logo: image layer with [logo URL] positioned bottom-left
4. Brand name: text layer with [brand name] in bold, 32px
5. Tagline: text layer with [tagline text] right-aligned, auto-scaled
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "/9j/4AAQSkZJRgABAQ...",
    "mime_type": "image/jpeg"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
