---
name: process-real-estate-photo
description: Enhance and standardize a property listing photo with auto-contrast, sharpening, and consistent sizing.
---

# Process Real Estate Photo

Real estate agencies and property platforms use this recipe to standardize a listing photo. Upload a property photo and apply auto-contrast, sharpening, and resize operations — ready for an MLS listing with consistent quality.

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
      "name": "property-photo.jpg",
      "url": "https://example.com/property-photo.jpg"
    },
    "operations": [
      {
        "type": "resize",
        "width_in_px": 1920,
        "height_in_px": 1080,
        "fit": "cover"
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
    name: "property-photo.jpg",
    url: "https://example.com/property-photo.jpg",
  },
  operations: [
    {
      type: "resize",
      width_in_px: 1920,
      height_in_px: 1080,
      fit: "cover",
    },
    { type: "auto_contrast" },
    {
      type: "sharpen",
      sigma: 1.5,
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
        "name": "property-photo.jpg",
        "url": "https://example.com/property-photo.jpg",
    },
    operations=[
        {
            "type": "resize",
            "width_in_px": 1920,
            "height_in_px": 1080,
            "fit": "cover",
        },
        {"type": "auto_contrast"},
        {
            "type": "sharpen",
            "sigma": 1.5,
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
		File: il.FileInput{Type: "url", Name: "property-photo.jpg", Url: "https://example.com/property-photo.jpg"},
		Operations: []il.TransformOperation{
			il.NewResizeOperation(1920, 1080, "cover"),
			{Type: "auto_contrast"},
			il.NewSharpenOperation(1.5),
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
  "name": "Process Real Estate Photo",
  "nodes": [
    {
      "parameters": {
        "content": "## Process Real Estate Photo\n\nReal estate agencies and property platforms use this recipe to standardize a listing photo. Upload a property photo and apply auto-contrast, sharpening, and resize operations \u2014 ready for an MLS listing with consistent quality.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "e100cf30-cc6a-44ec-a68a-8d1d99f15e34",
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
      "id": "52cd56ec-13de-4bd9-9fcb-354172459662",
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
      "id": "b8c9d0e1-f2a3-4b4c-5d6e-8f9a0b1c2d3e",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageTransformation",
        "fileInputMode": "url",
        "fileName": "property-photo.jpg",
        "fileUrl": "https://example.com/property-photo.jpg",
        "operations": {
          "operationValues": [
            {
              "operationType": "resize",
              "widthInPx": 1920,
              "heightInPx": 1080,
              "fit": "cover"
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
      "id": "e1f2a3b4-c5d6-4e7f-8a9b-0c1d2e3f4a5b",
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
Process the real estate photo at [file URL] for a property listing. Use the transform_image tool with a resize operation to 1920x1080 pixels (fit: cover), an auto_contrast operation, a sharpen operation, and a convert operation to JPEG at quality 90.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/jpeg"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
