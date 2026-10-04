---
name: generate-youtube-thumbnail
description: Generate a YouTube thumbnail with bold title text, gradient background, and a static image cutout.
---

# Generate YouTube Thumbnail

Content creators and video platforms use this recipe to generate eye-catching thumbnails at scale. Define a bold gradient canvas, overlay a subject photo with background removal, and add large title text — ready for YouTube uploads, social previews, or content management systems.

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
      "width_in_px": 1280,
      "height_in_px": 720
    },
    "layers": [
      {
        "index": 0,
        "type": "gradient",
        "gradient_type": "linear",
        "angle_in_degrees": 135.0,
        "colors": [
          {
            "hex_color": "#FF6B00",
            "position": 0.0
          },
          {
            "hex_color": "#D90429",
            "position": 100.0
          }
        ],
        "position": {
          "x_in_px": 0.0,
          "y_in_px": 0.0
        },
        "dimensions": {
          "width_in_px": 1280,
          "height_in_px": 720
        }
      },
      {
        "index": 1,
        "type": "image",
        "file": {
          "type": "base64",
          "name": "subject-photo.png",
          "base64": "<base64-encoded-subject-photo>"
        },
        "should_remove_background": true,
        "position": {
          "x_in_px": 700.0,
          "y_in_px": 60.0
        }
      },
      {
        "index": 2,
        "type": "text",
        "text": "I Built an App in 24 Hours",
        "font_name": "Montserrat",
        "font_size_in_px": 64,
        "text_color": "#FFFFFF",
        "font_weight": "bold",
        "position": {
          "x_in_px": 50.0,
          "y_in_px": 120.0
        },
        "dimensions": {
          "width_in_px": 620,
          "height_in_px": 280
        }
      },
      {
        "index": 3,
        "type": "text",
        "text": "Dev With Alex",
        "font_name": "Inter",
        "font_size_in_px": 28,
        "text_color": "#FFF3E0",
        "position": {
          "x_in_px": 50.0,
          "y_in_px": 560.0
        },
        "dimensions": {
          "width_in_px": 400,
          "height_in_px": 50
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
    width_in_px: 1280,
    height_in_px: 720,
  },
  output_format: "png",
  layers: [
    {
      index: 0,
      type: "gradient",
      gradient_type: "linear",
      angle_in_degrees: 135.0,
      colors: [
        {
          hex_color: "#FF6B00",
          position: 0.0,
        },
        {
          hex_color: "#D90429",
          position: 100.0,
        },
      ],
      position: {
        x_in_px: 0,
        y_in_px: 0,
      },
      dimensions: {
        width_in_px: 1280,
        height_in_px: 720,
      },
    },
    {
      index: 1,
      type: "image",
      file: {
        type: "base64",
        name: "subject-photo.png",
        base64: "<base64-encoded-subject-photo>",
      },
      should_remove_background: true,
      position: {
        x_in_px: 700,
        y_in_px: 60,
      },
    },
    {
      index: 2,
      type: "text",
      text: "I Built an App in 24 Hours",
      font_name: "Montserrat",
      font_size_in_px: 64,
      text_color: "#FFFFFF",
      font_weight: "bold",
      position: {
        x_in_px: 50,
        y_in_px: 120,
      },
      dimensions: {
        width_in_px: 620,
        height_in_px: 280,
      },
    },
    {
      index: 3,
      type: "text",
      text: "Dev With Alex",
      font_name: "Inter",
      font_size_in_px: 28,
      text_color: "#FFF3E0",
      position: {
        x_in_px: 50,
        y_in_px: 560,
      },
      dimensions: {
        width_in_px: 400,
        height_in_px: 50,
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
        "width_in_px": 1280,
        "height_in_px": 720,
    },
    output_format="png",
    layers=[
        {
            "index": 0,
            "type": "gradient",
            "gradient_type": "linear",
            "angle_in_degrees": 135.0,
            "colors": [
                {
                    "hex_color": "#FF6B00",
                    "position": 0.0,
                },
                {
                    "hex_color": "#D90429",
                    "position": 100.0,
                },
            ],
            "position": {
                "x_in_px": 0,
                "y_in_px": 0,
            },
            "dimensions": {
                "width_in_px": 1280,
                "height_in_px": 720,
            },
        },
        {
            "index": 1,
            "type": "image",
            "file": {
                "type": "base64",
                "name": "subject-photo.png",
                "base64": "<base64-encoded-subject-photo>",
            },
            "should_remove_background": True,
            "position": {
                "x_in_px": 700,
                "y_in_px": 60,
            },
        },
        {
            "index": 2,
            "type": "text",
            "text": "I Built an App in 24 Hours",
            "font_name": "Montserrat",
            "font_size_in_px": 64,
            "text_color": "#FFFFFF",
            "font_weight": "bold",
            "position": {
                "x_in_px": 50,
                "y_in_px": 120,
            },
            "dimensions": {
                "width_in_px": 620,
                "height_in_px": 280,
            },
        },
        {
            "index": 3,
            "type": "text",
            "text": "Dev With Alex",
            "font_name": "Inter",
            "font_size_in_px": 28,
            "text_color": "#FFF3E0",
            "position": {
                "x_in_px": 50,
                "y_in_px": 560,
            },
            "dimensions": {
                "width_in_px": 400,
                "height_in_px": 50,
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
		Dimensions: il.Dimensions{
			WidthInPx:  1280,
			HeightInPx: 720,
		},
		OutputFormat: "png",
		Layers: []il.Layer{
			il.NewGradientLayer(0, "linear", []il.GradientColor{
				{
      HexColor: "#FF6B00",
      Position: 0.0,
    },
				{
      HexColor: "#D90429",
      Position: 100.0,
    },
			}, il.Position{
     XInPx: 0,
     YInPx: 0,
   }, il.Dimensions{
     WidthInPx: 1280,
     HeightInPx: 720,
   }),
			il.NewStaticImageLayer(1, il.FileInput{Buffer: "<base64-encoded-subject-photo>"},
				il.Position{
      XInPx: 700,
      YInPx: 60,
    },
				il.Dimensions{}),
			il.NewTextLayer(2, "I Built an App in 24 Hours", "Montserrat", 64, "#FFFFFF",
				il.Position{
      XInPx: 50,
      YInPx: 120,
    },
				il.Dimensions{
      WidthInPx: 620,
      HeightInPx: 280,
    }),
			il.NewTextLayer(3, "Dev With Alex", "Inter", 28, "#FFF3E0",
				il.Position{
      XInPx: 50,
      YInPx: 560,
    },
				il.Dimensions{
      WidthInPx: 400,
      HeightInPx: 50,
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
  "name": "Generate YouTube Thumbnail",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate YouTube Thumbnail\n\nContent creators and video platforms use this recipe to generate eye-catching thumbnails at scale. Define a bold gradient canvas, overlay a subject photo with background removal, and add large title text \u2014 ready for YouTube uploads, social previews, or content management systems.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "a91b7d97-7812-4174-a020-b99f92380391",
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
      "id": "b1400574-f9f8-4914-84d8-80aaa80aa203",
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
      "id": "a3b4c5d6-dddd-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 1280,
        "heightInPx": 720,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"gradient\",\"gradient_type\":\"linear\",\"angle_in_degrees\":135.0,\"colors\":[{\"hex_color\":\"#FF6B00\",\"position\":0.0},{\"hex_color\":\"#D90429\",\"position\":100.0}],\"position\":{\"x\":0.0,\"y\":0.0},\"dimensions\":{\"width\":1280,\"height\":720}},{\"index\":1,\"type\":\"image\",\"file\":{\"type\":\"base64\",\"name\":\"subject-photo.png\",\"base64\":\"<base64-encoded-subject-photo>\"},\"should_remove_background\":true,\"position\":{\"x\":700.0,\"y\":60.0}},{\"index\":2,\"type\":\"text\",\"text\":\"I Built an App in 24 Hours\",\"font_name\":\"Montserrat\",\"font_size_in_px\":64,\"text_color\":\"#FFFFFF\",\"font_weight\":\"bold\",\"position\":{\"x\":50.0,\"y\":120.0},\"dimensions\":{\"width\":620,\"height\":280}},{\"index\":3,\"type\":\"text\",\"text\":\"Dev With Alex\",\"font_name\":\"Inter\",\"font_size_in_px\":28,\"text_color\":\"#FFF3E0\",\"position\":{\"x\":50.0,\"y\":560.0},\"dimensions\":{\"width\":400,\"height\":50}}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "a3b4c5d6-dddd-4000-8000-000000000002",
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
Generate a YouTube thumbnail at 1280x720 pixels. Use the generate_image tool with these layers:

1. Background: gradient layer with [bold colors]
2. Subject cutout: image layer with [subject image URL] positioned to one side
3. Title text: text layer with [video title] in large bold text with dark outline
4. Accent elements: solid-color shapes for visual emphasis
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
