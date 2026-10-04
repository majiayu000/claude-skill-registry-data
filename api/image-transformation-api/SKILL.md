---
name: image-transformation-api
description: Transform images with resize, crop, smart crop, upscale, remove background, and 20+ operations.
---

# Image Transformation API

Transform images with resize, crop, smart crop, upscale, remove background, and 20+ operations.

**Cost:** 0.5 credits per request

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Transform images with a single API call. Send a file and an ordered list of operations — resize, crop, blur, sharpen, convert, and more — and receive the transformed image as base64-encoded JSON in the response.

## Key Features

- **AI Smart Crop** — Automatically crop around faces, people, and animals using AI object detection. Priority: face > person > animal > object.
- **AI Upscaling** — Upscale images 2-4x with AI-powered super resolution for sharp, artifact-free results.
- **AI Background Removal** — Remove image backgrounds using AI segmentation. Output transparent PNG or composite onto a solid color.
- **Full Operation Set** — Resize, crop, blur, sharpen, rotate, modulate, tint, threshold, denoise, opacity, and more.
- **Pipeline Composition** — Chain up to 30 operations in a single request, executed sequentially.
- **Compress to Size** — Iteratively compress an image to fit within a target file size in bytes.
- **Format Conversion** — Convert between PNG, JPEG, WebP, AVIF, and HEIF with quality control.

## Overview

The Image Transformation API applies a pipeline of operations to an image. You send a file (base64 or URL) and an ordered list of operations, and receive the transformed image as base64-encoded JSON in the response.

**Endpoint:** `POST /image-transformation/v1/transform`

**Supported formats:** JPEG, PNG, WebP, GIF, AVIF, HEIF, SVG

**Limits:**
- Max file size: 50 MB
- Max request body: 60 MB
- Max operations per request: 30

## Request Format

<!-- tabs -->

```bash
curl -X POST https://api.iterationlayer.com/image-transformation/v1/transform \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file": {
      "type": "base64",
      "name": "photo.jpg",
      "base64": "<base64-encoded-image>"
    },
    "operations": [
      {
        "type": "resize",
        "width_in_px": 800,
        "height_in_px": 600,
        "fit": "cover"
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
const client = new IterationLayer({
  apiKey: "YOUR_API_KEY",
});

const result = await client.transformImage({
  file: {
    type: "base64",
    name: "photo.jpg",
    base64: new Uint8Array([/* image bytes */]),
  },
  operations: [
    {
      type: "resize",
      width_in_px: 800,
      height_in_px: 600,
      fit: "cover",
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
        "type": "base64",
        "name": "photo.jpg",
        "base64": b"...",
    },
    operations=[
        {
            "type": "resize",
            "width_in_px": 800,
            "height_in_px": 600,
            "fit": "cover",
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
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")

result, err := client.TransformImage(il.TransformImageRequest{
    File: il.FileInput{Type: "base64", Name: "photo.jpg", Base64: []byte{ /* image bytes */ }},
    Operations: []il.TransformOperation{
        il.NewResizeOperation(800, 600, "cover"),
        il.NewConvertOperation("webp"),
    },
})
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/webp"
  }
}
```

<!-- /tabs -->

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | object | Yes | Image file to transform (see File Input below) |
| `operations` | array | Yes | Ordered list of operations to apply (max 30) |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

### File Input

Provide the image as either base64 or a URL:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Filename with extension (e.g., `photo.jpg`) |
| `base64` | string | One of base64/url | Base64-encoded file content |
| `url` | string | One of base64/url | HTTPS URL to fetch the file from. HTTP is not accepted. |

### URL Example

```json
{
  "file": {
    "name": "photo.jpg",
    "url": "https://example.com/photo.jpg"
  },
  "operations": [
    {
      "type": "grayscale"
    }
  ]
}
```

## Operations

Operations are applied sequentially in the order provided.

### resize

Resize the image to target dimensions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `width` | integer | Yes | Target width (> 0) |
| `height` | integer | Yes | Target height (> 0) |
| `fit` | string | Yes | One of: `cover`, `contain`, `fill`, `inside`, `outside` |

**Fit modes:**
- `cover` — Scale and crop to fill the target dimensions exactly
- `contain` — Scale to fit within dimensions, padding with black
- `fill` — Stretch to fill dimensions (may distort)
- `inside` — Scale down only if larger than target
- `outside` — Scale up only if smaller than target

```json
{
  "type": "resize",
  "width_in_px": 400,
  "height_in_px": 300,
  "fit": "cover"
}
```

### crop

Extract a rectangular region from the image.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `left_in_px` | integer | Yes | Left offset (>= 0) |
| `top_in_px` | integer | Yes | Top offset (>= 0) |
| `width` | integer | Yes | Crop width (> 0) |
| `height` | integer | Yes | Crop height (> 0) |

```json
{
  "type": "crop",
  "left_in_px": 100,
  "top_in_px": 50,
  "width_in_px": 400,
  "height_in_px": 300
}
```

### smart_crop

Intelligent crop that centers on detected objects (faces, people, animals). Falls back to center crop when no objects are detected. Uses AI object detection.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `width` | integer | Yes | Target width (> 0) |
| `height` | integer | Yes | Target height (> 0) |

**Priority order:** face > person > animal > object

```json
{
  "type": "smart_crop",
  "width_in_px": 300,
  "height_in_px": 300
}
```

### extend

Add padding around the image with a background color.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `top_in_px` | integer | Yes | Top padding (>= 0) |
| `bottom_in_px` | integer | Yes | Bottom padding (>= 0) |
| `left_in_px` | integer | Yes | Left padding (>= 0) |
| `right_in_px` | integer | Yes | Right padding (>= 0) |
| `hex_color` | string | Yes | Background color (e.g., `#FF0000`) |

```json
{
  "type": "extend",
  "top_in_px": 20,
  "bottom_in_px": 20,
  "left_in_px": 20,
  "right_in_px": 20,
  "hex_color": "#FFFFFF"
}
```

### trim

Remove borders from the image based on a color similarity threshold.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `threshold` | integer | Yes | Color difference threshold (>= 0) |

```json
{
  "type": "trim",
  "threshold": 10
}
```

### rotate

Rotate the image by any angle. Non-90-degree rotations expand the canvas.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `angle_in_degrees` | float | Yes | Rotation angle |
| `hex_color` | string | No | Background color for exposed areas (default: black) |

```json
{
  "type": "rotate",
  "angle_in_degrees": 45.0,
  "hex_color": "#FFFFFF"
}
```

### flip

Mirror the image vertically (top to bottom).

```json
{
  "type": "flip"
}
```

### flop

Mirror the image horizontally (left to right).

```json
{
  "type": "flop"
}
```

### blur

Apply Gaussian blur.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sigma` | float | Yes | Blur radius (> 0) |

```json
{
  "type": "blur",
  "sigma": 3.0
}
```

### sharpen

Sharpen the image.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sigma` | float | Yes | Sharpen intensity (> 0) |

```json
{
  "type": "sharpen",
  "sigma": 2.0
}
```

### modulate

Adjust brightness, saturation, and/or hue. At least one parameter must be provided.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brightness` | float | No | Brightness multiplier (1.0 = unchanged) |
| `saturation` | float | No | Saturation multiplier (1.0 = unchanged) |
| `hue` | float | No | Hue rotation in degrees |

```json
{
  "type": "modulate",
  "brightness": 1.2,
  "saturation": 0.8
}
```

### tint

Apply a color tint to the image.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hex_color` | string | Yes | Tint color (e.g., `#FF6600`) |

```json
{
  "type": "tint",
  "hex_color": "#FF6600"
}
```

### grayscale

Convert the image to grayscale.

```json
{
  "type": "grayscale"
}
```

### invert_colors

Invert all colors in the image.

```json
{
  "type": "invert_colors"
}
```

### auto_contrast

Automatically adjust contrast by normalizing the histogram.

```json
{
  "type": "auto_contrast"
}
```

### gamma

Apply gamma correction.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gamma` | float | Yes | Gamma value (> 0, typical: 0.5-3.0) |

```json
{
  "type": "gamma",
  "gamma": 2.2
}
```

### remove_transparency

Flatten the alpha channel against a background color. No-op if the image has no alpha channel.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hex_color` | string | Yes | Background color |

```json
{
  "type": "remove_transparency",
  "hex_color": "#FFFFFF"
}
```

### threshold

Convert pixels to black or white based on a brightness threshold.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | integer | Yes | Threshold value (0-255) |
| `is_grayscale` | boolean | Yes | Convert to grayscale before thresholding |

```json
{
  "type": "threshold",
  "value": 128,
  "is_grayscale": true
}
```

### denoise

Reduce noise using a median filter.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `size` | integer | Yes | Filter window size (> 0, odd numbers recommended) |

```json
{
  "type": "denoise",
  "size": 3
}
```

### opacity

Adjust the image opacity.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `opacity_in_percent` | integer | Yes | Opacity level (0-100) |

```json
{
  "type": "opacity",
  "opacity_in_percent": 50
}
```

### convert

Convert the image to a different format.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format` | string | Yes | One of: `png`, `jpeg`, `webp`, `avif`, `heif` |
| `quality` | integer | No | Compression quality (1-100, for jpeg/webp) |

```json
{
  "type": "convert",
  "format": "webp",
  "quality": 85
}
```

### upscale

Upscale the image using AI-powered super resolution.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `factor` | integer | Yes | Scale factor: 2, 3, or 4 |

```json
{
  "type": "upscale",
  "factor": 4
}
```

### compress_to_size

Iteratively compress an image to fit within a target file size. For lossy formats (JPEG, WebP) reduces quality first, then dimensions. For lossless formats (PNG, GIF) reduces dimensions only.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `max_file_size_in_bytes` | integer | Yes | Maximum output size in bytes |

```json
{
  "type": "compress_to_size",
  "max_file_size_in_bytes": 500000
}
```

### remove_background

Remove the image background using AI segmentation. Isolates the foreground subject and composites against a solid color or produces a transparent result.

The output format matches the input format. For formats that do not support transparency (JPEG, GIF), the background is filled with white unless `hex_color` is specified. To get a transparent result, convert to PNG or WebP first using the `convert` operation.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `background_hex_color` | string | No | Background replacement color (e.g., `#FFFFFF`). Omit for transparent (PNG/WebP only). |

```json
{
  "type": "remove_background"
}
```

With background color:

```json
{
  "type": "remove_background",
  "background_hex_color": "#FFFFFF"
}
```

Transparent output (convert to PNG first if input is JPEG):

```json
[
  {
    "type": "convert",
    "format": "png"
  },
  {
    "type": "remove_background"
  }
]
```

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

- [Smart Crop Group Photo](/recipes/smart-crop-group-photo) -- Use AI detection to smart-crop individual portraits from a group photo.
- [Upscale Low-Resolution Image](/recipes/upscale-low-resolution-image) -- Upscale a low-resolution image using AI super-resolution for print or high-DPI display.
- [Watermark an Image](/recipes/watermark-an-image) -- Apply a text watermark to a photo using layer-based image composition for brand protection.
- [Remove Product Background](/recipes/remove-product-background) -- Remove the background from a product photo using AI-powered segmentation.
- [Resize Image for Social Media](/recipes/resize-image-for-social-media) -- Resize and crop an image for different social media platform dimensions.

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request (missing file, invalid operations, unsupported format) |
| 401 | Missing or invalid API key |
| 422 | Processing error (image too small for crop, invalid color, etc.) |
| 429 | Rate limit exceeded |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/image-transformation)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
