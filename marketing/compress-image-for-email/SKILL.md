---
name: compress-image-for-email
description: Resize, sharpen, and compress an image to fit email platform size limits in a single pipeline.
---

# Compress Image for Email

Marketing teams and email platforms use this recipe to prepare images for email campaigns. Resize to email-friendly dimensions, sharpen after downscale, convert to JPEG for universal client support, and compress to a target file size — all in one API call.

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
      "name": "hero.jpg",
      "url": "https://cdn.example.com/campaign/hero.jpg"
    },
    "operations": [
      {
        "type": "resize",
        "width_in_px": 1200,
        "height_in_px": 900,
        "fit": "inside"
      },
      {
        "type": "sharpen",
        "sigma": 0.5
      },
      {
        "type": "convert",
        "format": "jpeg",
        "quality": 85
      },
      {
        "type": "compress_to_size",
        "max_file_size_in_bytes": 500000
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
    name: "hero.jpg",
    url: "https://cdn.example.com/campaign/hero.jpg",
  },
  operations: [
    {
      type: "resize",
      width_in_px: 1200,
      height_in_px: 900,
      fit: "inside",
    },
    {
      type: "sharpen",
      sigma: 0.5,
    },
    {
      type: "convert",
      format: "jpeg",
      quality: 85,
    },
    {
      type: "compress_to_size",
      max_file_size_in_bytes: 500_000,
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
        "name": "hero.jpg",
        "url": "https://cdn.example.com/campaign/hero.jpg",
    },
    operations=[
        {
            "type": "resize",
            "width_in_px": 1200,
            "height_in_px": 900,
            "fit": "inside",
        },
        {
            "type": "sharpen",
            "sigma": 0.5,
        },
        {
            "type": "convert",
            "format": "jpeg",
            "quality": 85,
        },
        {
            "type": "compress_to_size",
            "max_file_size_in_bytes": 500_000,
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
		File: il.FileInput{Type: "url", Name: "hero.jpg", Url: "https://cdn.example.com/campaign/hero.jpg"},
		Operations: []il.TransformOperation{
			il.NewResizeOperation(1200, 900, "inside"),
			il.NewSharpenOperation(0.5),
			il.NewConvertOperation("jpeg"),
			il.NewCompressToSizeOperation(500_000),
		},
	})
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Compress Image for Email",
  "nodes": [
    {
      "parameters": {
        "content": "## Compress Image for Email\n\nMarketing teams and email platforms use this recipe to prepare images for email campaigns. Resize to email-friendly dimensions, sharpen after downscale, convert to JPEG for universal client support, and compress to a target file size \u2014 all in one API call.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "0cacbc50-e82b-4267-939f-1266511f7288",
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
      "id": "d28f15fd-7c4d-465e-bbea-0de2c9d5561d",
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
      "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "hero.jpg",
        "fileUrl": "https://cdn.example.com/campaign/hero.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "resize",
              "widthInPx": 1200,
              "heightInPx": 900,
              "fit": "inside"
            },
            {
              "operationType": "sharpen",
              "sigma": 0.5
            },
            {
              "operationType": "convert",
              "convertFormat": "jpeg",
              "quality": 85
            },
            {
              "operationType": "compress_to_size",
              "maxFileSizeInBytes": 500000
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
      "id": "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a",
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
Compress the image at [file URL] for email. Use the transform_image tool with a resize operation to [width]x[height] pixels (fit: inside), a sharpen operation, a convert operation to JPEG, and a compress_to_size operation with a max file size of [max file size in bytes] bytes.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "/9j/4AAQSkZJRgABAQAAAQ...",
    "mime_type": "image/jpeg"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
