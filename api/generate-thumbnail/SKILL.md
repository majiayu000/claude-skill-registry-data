---
name: generate-thumbnail
description: Resize a source image to a thumbnail and convert to WebP.
---

# Generate Thumbnail

Web developers and CMS platforms use this recipe to generate a thumbnail from a high-resolution image. Upload one image, resize it to a target dimension, and convert to WebP — ready for galleries, cards, and preview grids.

## APIs Used

Image Transformation (0.5 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/image-transformation/v1/transform \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file": {
      "type": "url",
      "name": "hero-image.jpg",
      "url": "https://example.com/hero-image.jpg"
    },
    "operations": [
      {
        "type": "resize",
        "width_in_px": 300,
        "height_in_px": 200,
        "fit": "cover"
      },
      {
        "type": "convert",
        "format": "webp",
        "quality": 80
      }
    ]
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.transformImage({
  file: {
    type: "url",
    name: "hero-image.jpg",
    url: "https://example.com/hero-image.jpg",
  },
  operations: [
    {
      type: "resize",
      width_in_px: 300,
      height_in_px: 200,
      fit: "cover",
    },
    {
      type: "convert",
      format: "webp",
      quality: 80,
    },
  ],
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.transform_image(
    file={
        "type": "url",
        "name": "hero-image.jpg",
        "url": "https://example.com/hero-image.jpg",
    },
    operations=[
        {
            "type": "resize",
            "width_in_px": 300,
            "height_in_px": 200,
            "fit": "cover",
        },
        {
            "type": "convert",
            "format": "webp",
            "quality": 80,
        },
    ],
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.TransformImage(il.TransformImageRequest{
		File: il.FileInput{Type: "url", Name: "hero-image.jpg", Url: "https://example.com/hero-image.jpg"},
		Operations: []il.TransformOperation{
			il.NewResizeOperation(300, 200, "cover"),
			il.NewConvertOperation("webp"),
		},
	})
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Generate Thumbnail",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Thumbnail\n\nWeb developers and CMS platforms use this recipe to generate a thumbnail from a high-resolution image. Upload one image, resize it to a target dimension, and convert to WebP \u2014 ready for galleries, cards, and preview grids.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "9f1bcab1-5fac-4660-8ed7-2bf3cca026b9",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Transform Image\nResource: **Image Transformation**\n\nConfigure the Image Transformation parameters below, then connect your credentials.",
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
      "id": "6d86540a-cfdf-4c45-9df6-d83ab7b638c4",
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
      "id": "fbd67c8f-6e2b-45a2-bbb4-a03313963845",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "hero-image.jpg",
        "fileUrl": "https://example.com/hero-image.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "resize",
              "widthInPx": 300,
              "heightInPx": 200,
              "fit": "cover"
            },
            {
              "operationType": "convert",
              "convertFormat": "webp",
              "quality": 80
            }
          ]
        }
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "77a29fe5-007f-40cb-b42c-3a18070e3f68",
      "name": "Transform Image",
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
            "node": "Transform Image",
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
Generate a thumbnail from a source image. Use the transform_image tool with [source image URL] and apply these operations:

1. Resize to [width]x[height] pixels
2. Convert to WebP format for optimized file size
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/webp"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
