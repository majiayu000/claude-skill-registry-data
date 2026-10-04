---
name: remove-product-background
description: Remove the background from a product photo using AI-powered segmentation.
---

# Remove Product Background

E-commerce teams remove backgrounds from product photos for clean white-background listings or transparent PNGs for compositing. Upload a raw product photo, remove the background with AI-powered segmentation, and convert to PNG — ready for your storefront or design tool.

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
      "name": "product-photo.jpg",
      "url": "https://example.com/product-photo.jpg"
    },
    "operations": [
      {
        "type": "remove_background",
        "background_hex_color": "#FFFFFF"
      },
      {
        "type": "convert",
        "format": "png"
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
    name: "product-photo.jpg",
    url: "https://example.com/product-photo.jpg",
  },
  operations: [
    {
      type: "remove_background",
      background_hex_color: "#FFFFFF",
    },
    {
      type: "convert",
      format: "png",
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
        "name": "product-photo.jpg",
        "url": "https://example.com/product-photo.jpg",
    },
    operations=[
        {
            "type": "remove_background",
            "background_hex_color": "#FFFFFF",
        },
        {
            "type": "convert",
            "format": "png",
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
		File: il.FileInput{Type: "url", Name: "product-photo.jpg", Url: "https://example.com/product-photo.jpg"},
		Operations: []il.TransformOperation{
			{
     Type: "remove_background",
     BackgroundHexColor: "#FFFFFF",
   },
			il.NewConvertOperation("png"),
		},
	})
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Remove Product Background",
  "nodes": [
    {
      "parameters": {
        "content": "## Remove Product Background\n\nE-commerce teams remove backgrounds from product photos for clean white-background listings or transparent PNGs for compositing. Upload a raw product photo, remove the background with AI-powered segmentation, and convert to PNG \u2014 ready for your storefront or design tool.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "74cf08f0-4566-4029-9fa7-01f606fb0f57",
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
      "id": "4f91e1ce-d3d3-41a0-a88a-275391f48556",
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
      "id": "c9d0e1f2-a3b4-4c5d-6e7f-9a0b1c2d3e4f",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "product-photo.jpg",
        "fileUrl": "https://example.com/product-photo.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "remove_background",
              "hexColor": "#FFFFFF"
            },
            {
              "operationType": "convert",
              "convertFormat": "png"
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
      "id": "f2a3b4c5-d6e7-4f8a-9b0c-1d2e3f4a5b6c",
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
Remove the background from the product image at [file URL]. Use the transform_image tool with a remove_background operation (background color [hex color or transparent]) and a convert operation to PNG.
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
