---
name: smart-crop-product-image
description: AI-powered subject-aware crop that centers on the product regardless of its position in the frame.
---

# Smart Crop Product Image

E-commerce platforms and marketplaces use this recipe to normalize supplier product photos to consistent square thumbnails. AI detects the product and crops around it — no manual positioning, no lost products at the edges.

## APIs Used

Image Transformation (0.5 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST \
  https://api.iterationlayer.com/image-transformation/v1/transform \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file": {
      "type": "url",
      "name": "supplier-image.jpg",
      "url": "https://cdn.example.com/supplier/product-001.jpg"
    },
    "operations": [
      {
        "type": "smart_crop",
        "width_in_px": 1000,
        "height_in_px": 1000
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
    name: "supplier-image.jpg",
    url: "https://cdn.example.com/supplier/product-001.jpg",
  },
  operations: [
    {
      type: "smart_crop",
      width_in_px: 1000,
      height_in_px: 1000,
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
        "name": "supplier-image.jpg",
        "url": "https://cdn.example.com/supplier/product-001.jpg",
    },
    operations=[
        {
            "type": "smart_crop",
            "width_in_px": 1000,
            "height_in_px": 1000,
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
		File: il.FileInput{Type: "url", Name: "supplier-image.jpg", Url: "https://cdn.example.com/supplier/product-001.jpg"},
		Operations: []il.TransformOperation{
			il.NewSmartCropOperation(1000, 1000),
		},
	})
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Smart Crop Product Image",
  "nodes": [
    {
      "parameters": {
        "content": "## Smart Crop Product Image\n\nE-commerce platforms and marketplaces use this recipe to normalize supplier product photos to consistent square thumbnails. AI detects the product and crops around it \u2014 no manual positioning, no lost products at the edges.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "c1f1d6cd-3e16-4933-9557-caf1d498b9e5",
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
      "id": "b548438b-de0a-4f2d-ab16-50b012f9669b",
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
      "id": "a3b4c5d6-e7f8-4a9b-0c1d-3e4f5a6b7c8d",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "supplier-image.jpg",
        "fileUrl": "https://cdn.example.com/supplier/product-001.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "smart_crop",
              "widthInPx": 1000,
              "heightInPx": 1000
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
      "id": "d6e7f8a9-b0c1-4d2e-3f4a-5b6c7d8e9f0a",
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
Smart crop the product image at [file URL] to center on the product. Use the transform_image tool with a smart_crop operation to [width]x[height] pixels.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "/9j/4AAQSkZJRgABAQEASABI...",
    "mime_type": "image/jpeg"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
