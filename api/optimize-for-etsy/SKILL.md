---
name: optimize-for-etsy
description: Smart crop a product photo to Etsy's recommended 2000×2000px square format and export as JPEG.
---

# Optimize Product Image for Etsy

Etsy sellers and multi-channel commerce platforms use this recipe to normalize product photos for Etsy listings. AI smart crop detects the subject and frames it correctly before resizing — no manual cropping, no products cut off at the edges.

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
      "url": "https://example.com/products/raw/candle-019.jpg"
    },
    "operations": [
      {
        "type": "smart_crop",
        "width_in_px": 2000,
        "height_in_px": 2000
      },
      {
        "type": "sharpen",
        "sigma": 1.0
      },
      {
        "type": "convert",
        "format": "jpeg",
        "quality": 90
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
    url: "https://example.com/products/raw/candle-019.jpg",
  },
  operations: [
    {
      type: "smart_crop",
      width_in_px: 2000,
      height_in_px: 2000,
    },
    {
      type: "sharpen",
      sigma: 1.0,
    },
    {
      type: "convert",
      format: "jpeg",
      quality: 90,
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
        "url": "https://example.com/products/raw/candle-019.jpg",
    },
    operations=[
        {
            "type": "smart_crop",
            "width_in_px": 2000,
            "height_in_px": 2000,
        },
        {
            "type": "sharpen",
            "sigma": 1.0,
        },
        {
            "type": "convert",
            "format": "jpeg",
            "quality": 90,
        },
    ],
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	quality := 90
	result, err := client.TransformImage(il.TransformImageRequest{
		File: il.FileInput{Type: "url", Name: "product.jpg", Url: "https://example.com/products/raw/candle-019.jpg"},
		Operations: []il.TransformOperation{
			il.NewSmartCropOperation(2000, 2000),
			il.NewSharpenOperation(1.0),
			il.ConvertOperation{Type: "convert", Format: "jpeg", Quality: &quality},
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
  "name": "Optimize Product Image for Etsy",
  "nodes": [
    {
      "parameters": {
        "content": "## Optimize Product Image for Etsy\n\nEtsy sellers and multi-channel commerce platforms use this recipe to normalize product photos for Etsy listings. AI smart crop detects the subject and frames it correctly before resizing \u2014 no manual cropping, no products cut off at the edges.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "8f0d3b99-5925-478a-ba02-5a971053ca07",
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
      "id": "10d32f56-4bbb-4332-8c0b-57d1c1ff92bb",
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
      "id": "e5f6a7b8-c9d0-4e1f-2a3b-5c6d7e8f9a0b",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "product.jpg",
        "fileUrl": "https://example.com/products/raw/candle-019.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "smart_crop",
              "widthInPx": 2000,
              "heightInPx": 2000
            },
            {
              "operationType": "sharpen",
              "sigma": 1.0
            },
            {
              "operationType": "convert",
              "convertFormat": "jpeg",
              "quality": 90
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
      "id": "b8c9d0e1-f2a3-4b4c-5d6e-7f8a9b0c1d2e",
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
Optimize the product image at [file URL] for Etsy. Use the transform_image tool with a smart_crop operation to 2000x2000 pixels, a sharpen operation, and a convert operation to JPEG at quality 90.
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
