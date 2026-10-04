---
name: convert-image-format
description: Convert an image between PNG, JPEG, and WebP formats with quality control for web optimization.
---

# Convert Image Format

Web development teams and CDN operators use this recipe to convert an image to a modern format like WebP for faster page loads. Upload an image and convert it to your target format with precise quality control — ready for optimized delivery.

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
      "name": "image.png",
      "url": "https://example.com/image.png"
    },
    "operations": [
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
    name: "image.png",
    url: "https://example.com/image.png",
  },
  operations: [
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
        "name": "image.png",
        "url": "https://example.com/image.png",
    },
    operations=[
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
		File: il.FileInput{Type: "url", Name: "image.png", Url: "https://example.com/image.png"},
		Operations: []il.TransformOperation{
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
  "name": "Convert Image Format",
  "nodes": [
    {
      "parameters": {
        "content": "## Convert Image Format\n\nWeb development teams and CDN operators use this recipe to convert an image to a modern format like WebP for faster page loads. Upload an image and convert it to your target format with precise quality control \u2014 ready for optimized delivery.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "ef1f7bf2-b40a-4c97-bee0-17be627ca355",
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
      "id": "2eb211c1-e0ce-48d1-9d35-353159ce546b",
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
      "id": "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "image.png",
        "fileUrl": "https://example.com/image.png",
        "operations": {
          "operationValues": [
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
      "id": "f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c",
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
Convert the image at [file URL] to [output format] format. Use the transform_image tool with the file URL and a convert operation specifying format "[output format]" and quality [quality].
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
