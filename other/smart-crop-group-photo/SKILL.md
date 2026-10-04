---
name: smart-crop-group-photo
description: Use AI detection to smart-crop individual portraits from a group photo.
---

# Smart Crop Group Photo

HR platforms and event organizers extract individual headshots from team or group photos using AI-powered face detection to crop around the most prominent subject. Upload a group photo, apply smart crop to center on the detected face, and convert to JPEG — ready for employee directories, badges, or social profiles.

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
      "name": "group-photo.jpg",
      "url": "https://example.com/group-photo.jpg"
    },
    "operations": [
      {
        "type": "smart_crop",
        "width_in_px": 400,
        "height_in_px": 400
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
    name: "group-photo.jpg",
    url: "https://example.com/group-photo.jpg",
  },
  operations: [
    {
      type: "smart_crop",
      width_in_px: 400,
      height_in_px: 400,
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
        "name": "group-photo.jpg",
        "url": "https://example.com/group-photo.jpg",
    },
    operations=[
        {
            "type": "smart_crop",
            "width_in_px": 400,
            "height_in_px": 400,
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

	result, err := client.TransformImage(il.TransformImageRequest{
		File: il.FileInput{Type: "url", Name: "group-photo.jpg", Url: "https://example.com/group-photo.jpg"},
		Operations: []il.TransformOperation{
			il.NewSmartCropOperation(400, 400),
			il.NewConvertOperation("jpeg"),
		},
	})
	if err != nil {
		panic(err)
	}
}
```

```n8n
{
  "name": "Smart Crop Group Photo",
  "nodes": [
    {
      "parameters": {
        "content": "## Smart Crop Group Photo\n\nHR platforms and event organizers extract individual headshots from team or group photos using AI-powered face detection to crop around the most prominent subject. Upload a group photo, apply smart crop to center on the detected face, and convert to JPEG \u2014 ready for employee directories, badges, or social profiles.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "7d2e9c48-ab14-46c6-81df-28efb20a5e3d",
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
      "id": "98571eef-7f02-4713-a429-42f8dc8997bd",
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
      "id": "f2a3b4c5-d6e7-4f8a-9b0c-2d3e4f5a6b7c",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "group-photo.jpg",
        "fileUrl": "https://example.com/group-photo.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "smart_crop",
              "widthInPx": 400,
              "heightInPx": 400
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
      "id": "c5d6e7f8-a9b0-4c1d-2e3f-4a5b6c7d8e9f",
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
Smart crop a portrait from the group photo at [file URL]. Use the transform_image tool with a smart_crop operation to [width]x[height] pixels and a convert operation to JPEG at quality [quality].
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "/9j/4AAQSkZJRgABAQAAAQABAAD...",
    "mime_type": "image/jpeg"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
