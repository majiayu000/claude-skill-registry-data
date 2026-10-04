---
name: optimize-product-photo
description: Resize, enhance, and compress a product photo for an e-commerce listing with consistent quality.
---

# Optimize Product Photo

E-commerce teams and marketplace sellers use this recipe to prepare a product photo for a listing. Upload a raw product photo and apply a pipeline of resize, auto-contrast, sharpen, and format conversion — ready for your storefront with consistent quality and fast load times.

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
        "type": "resize",
        "width_in_px": 1000,
        "height_in_px": 1000,
        "fit": "contain"
      },
      {
        "type": "auto_contrast"
      },
      {
        "type": "sharpen",
        "sigma": 1.5
      },
      {
        "type": "convert",
        "format": "webp",
        "quality": 85
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
      type: "resize",
      width_in_px: 1000,
      height_in_px: 1000,
      fit: "contain",
    },
    { type: "auto_contrast" },
    {
      type: "sharpen",
      sigma: 1.5,
    },
    {
      type: "convert",
      format: "webp",
      quality: 85,
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
            "type": "resize",
            "width_in_px": 1000,
            "height_in_px": 1000,
            "fit": "contain",
        },
        {"type": "auto_contrast"},
        {
            "type": "sharpen",
            "sigma": 1.5,
        },
        {
            "type": "convert",
            "format": "webp",
            "quality": 85,
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
			il.NewResizeOperation(1000, 1000, "contain"),
			{Type: "auto_contrast"},
			il.NewSharpenOperation(1.5),
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
  "name": "Optimize Product Photo",
  "nodes": [
    {
      "parameters": {
        "content": "## Optimize Product Photo\n\nE-commerce teams and marketplace sellers use this recipe to prepare a product photo for a listing. Upload a raw product photo and apply a pipeline of resize, auto-contrast, sharpen, and format conversion \u2014 ready for your storefront with consistent quality and fast load times.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "c77fd822-c61c-43e1-975c-f74004f36485",
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
      "id": "c6b4e8f5-5dd1-43bb-b02e-fe9843938db9",
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
      "id": "a7b8c9d0-e1f2-4a3b-4c5d-7e8f9a0b1c2d",
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
              "operationType": "resize",
              "widthInPx": 1000,
              "heightInPx": 1000,
              "fit": "contain"
            },
            {
              "operationType": "auto_contrast"
            },
            {
              "operationType": "sharpen",
              "sigma": 1.5
            },
            {
              "operationType": "convert",
              "convertFormat": "webp",
              "quality": 85
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
      "id": "d0e1f2a3-b4c5-4d6e-7f8a-9b0c1d2e3f4a",
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
Optimize the product photo at [file URL] for e-commerce. Use the transform_image tool with a resize operation to [width]x[height] pixels (fit: contain), an auto_contrast operation, a sharpen operation, and a convert operation to WebP at quality 85.
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
