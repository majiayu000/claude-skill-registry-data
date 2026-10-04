---
name: optimize-for-shopify
description: Resize a product photo to Shopify's recommended 2048×2048px square format, sharpen, and convert to WebP for fast storefront load times.
---

# Optimize Product Image for Shopify

Shopify merchants and agencies use this recipe to normalize supplier product photos for their storefront. One API call resizes to the recommended square format, sharpens for display clarity, and outputs WebP — smaller files, faster load times, better Core Web Vitals.

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
      "name": "product.jpg",
      "url": "https://example.com/products/raw/sneaker-042.jpg"
    },
    "operations": [
      {
        "type": "resize",
        "width_in_px": 2048,
        "height_in_px": 2048,
        "fit": "contain"
      },
      {
        "type": "sharpen",
        "sigma": 1.2
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
    name: "product.jpg",
    url: "https://example.com/products/raw/sneaker-042.jpg",
  },
  operations: [
    {
      type: "resize",
      width_in_px: 2048,
      height_in_px: 2048,
      fit: "contain",
    },
    {
      type: "sharpen",
      sigma: 1.2,
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
        "name": "product.jpg",
        "url": "https://example.com/products/raw/sneaker-042.jpg",
    },
    operations=[
        {
            "type": "resize",
            "width_in_px": 2048,
            "height_in_px": 2048,
            "fit": "contain",
        },
        {
            "type": "sharpen",
            "sigma": 1.2,
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
		File: il.FileInput{Type: "url", Name: "product.jpg", Url: "https://example.com/products/raw/sneaker-042.jpg"},
		Operations: []il.TransformOperation{
			il.NewResizeOperation(2048, 2048, "contain"),
			il.NewSharpenOperation(1.2),
			il.NewConvertOperation("webp"),
		},
	})
	if err != nil {
		panic(err)
	}
	_ = result
}
```

```n8n
{
  "name": "Optimize Product Image for Shopify",
  "nodes": [
    {
      "parameters": {
        "content": "## Optimize Product Image for Shopify\n\nShopify merchants and agencies use this recipe to normalize supplier product photos for their storefront. One API call resizes to the recommended square format, sharpens for display clarity, and outputs WebP \u2014 smaller files, faster load times, better Core Web Vitals.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "927e5238-21a3-401a-9dbb-bd2678f698ba",
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
      "id": "f77f66fe-a46f-4c03-bc95-086b19b17e3d",
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
      "id": "f6a7b8c9-d0e1-4f2a-3b4c-6d7e8f9a0b1c",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "product.jpg",
        "fileUrl": "https://example.com/products/raw/sneaker-042.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "resize",
              "widthInPx": 2048,
              "heightInPx": 2048,
              "fit": "contain"
            },
            {
              "operationType": "sharpen",
              "sigma": 1.2
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
      "id": "c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f",
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
Optimize the product image at [file URL] for Shopify. Use the transform_image tool with a resize operation to 2048x2048 pixels (fit: contain), a sharpen operation, and a convert operation to WebP at quality 85.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "UklGRlYAAABXRUJQVlA4...",
    "mime_type": "image/webp"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
