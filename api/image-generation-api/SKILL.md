---
name: image-generation-api
description: Generate composited images from layers — solid colors, gradients, text, images, QR codes, barcodes, and layouts.
---

# Image Generation API

Generate composited images from layers — solid colors, gradients, text, images, QR codes, barcodes, and layouts.

**Cost:** 1 credits per request

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Generate composited images from layer definitions with a single API call. Define a canvas, add layers — solid colors, gradients, text, images, QR codes, barcodes, layouts — and receive the rendered image as base64-encoded JSON in the response.

## Key Features

- **Layer Types** — Solid colors (with optional angled edges and border radius), gradients (linear and radial, with border radius), text (with markdown bold/italic), images (with optional background removal and border radius), QR codes, barcodes, and layouts (horizontal/vertical flow with gap, alignment, padding, and nested children).
- **Layer Compositing** — Layers are rendered in index order and composited onto a transparent canvas with per-layer opacity and rotation.
- **Text Rendering** — Render text with custom fonts, alignment, and markdown formatting (`**bold**` and `*italic*`). Supports line wrapping, vertical alignment, and automatic font size scaling.
- **Bundled Google Fonts** — The top Google Fonts are bundled and available by default, including Inter, Roboto, OpenSans, Montserrat, Poppins, Lato, and many more. No font upload required for most text rendering needs.
- **Custom Fonts** — Upload additional fonts as base64 (TTF, OTF, WOFF, WOFF2) for text rendering.
- **QR Codes** — Generate QR codes with custom foreground and background colors.
- **Barcodes** — Generate barcodes in multiple formats: Code 128, EAN-13, EAN-8, Code 39, ITF, and Codabar.
- **Background Removal** — Automatically remove backgrounds from images using AI-powered detection.
- **Output Formats** — PNG, JPEG, WebP, TIFF, GIF, or AVIF.

## Overview

The Image Generation API composites multiple layers onto a canvas to produce a single output image. You define the canvas dimensions, optionally provide custom fonts, and specify an ordered list of layers. Each layer is rendered and composited by index order.

**Endpoint:** `POST /image-generation/v1/generate`

**Output formats:** PNG (default), JPEG, WebP, TIFF, GIF, AVIF

## Request Format

<!-- tabs -->

```bash
curl -X POST https://api.iterationlayer.com/image-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
      "width_in_px": 800,
      "height_in_px": 600
    },
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#FFFFFF"
      },
      {
        "index": 1,
        "type": "text",
        "text": "Hello World",
        "font_name": "Roboto",
        "font_size_in_px": 48,
        "text_color": "#000000",
        "position": {
          "x_in_px": 50.0,
          "y_in_px": 50.0
        },
        "dimensions": {
          "width_in_px": 700,
          "height_in_px": 100
        }
      }
    ],
    "output_format": "png"
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({
  apiKey: "YOUR_API_KEY",
});

const result = await client.generateImage({
  dimensions: {
    width_in_px: 800,
    height_in_px: 600,
  },
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#FFFFFF",
    },
    {
      index: 1,
      type: "text",
      text: "Hello World",
      font_name: "Roboto",
      font_size_in_px: 48,
      text_color: "#000000",
      position: {
        x_in_px: 50,
        y_in_px: 50,
      },
      dimensions: {
        width_in_px: 700,
        height_in_px: 100,
      },
    },
  ],
  output_format: "png",
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_image(
    dimensions={
        "width_in_px": 800,
        "height_in_px": 600,
    },
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#FFFFFF",
        },
        {
            "index": 1,
            "type": "text",
            "text": "Hello World",
            "font_name": "Roboto",
            "font_size_in_px": 48,
            "text_color": "#000000",
            "position": {
                "x_in_px": 50,
                "y_in_px": 50,
            },
            "dimensions": {
                "width_in_px": 700,
                "height_in_px": 100,
            },
        },
    ],
    output_format="png",
)
```

```go
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")

result, err := client.GenerateImage(il.GenerateImageRequest{
    Dimensions: il.Dimensions{
        WidthInPx:  800,
        HeightInPx: 600,
    },
    OutputFormat: "png",
    Layers: []il.Layer{
        il.NewSolidColorBackgroundLayer(0, "#FFFFFF"),
        il.NewTextLayer(1, "Hello World", "Roboto", 48, "#000000",
            il.Position{
                XInPx: 50,
                YInPx: 50,
            },
            il.Dimensions{
                WidthInPx:  700,
                HeightInPx: 100,
            }),
    },
})
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/png"
  }
}
```

<!-- /tabs -->

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dimensions` | object | Yes | Canvas size with `width` (integer, > 0) and `height` (integer, > 0) |
| `layers` | array | Yes | Ordered list of layer definitions (at least one) |
| `output_format` | string | No | One of: `png` (default), `jpeg`, `webp`, `tiff`, `gif`, `avif` |
| `fonts` | array | No | Custom font definitions for text layers |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

### Font Definition

The top Google Fonts are bundled and available by default. Text layers can reference any bundled font by name without providing font definitions. If a text layer references a font name that isn't found, it falls back to Inter Regular.

**Bundled fonts:**

- AlfaSlabOne
- AnekTelugu
- Anton
- Archivo
- ArchivoBlack
- Arimo
- Assistant
- Barlow
- BarlowCondensed
- BebasNeue
- Bitter
- BricolageGrotesque
- Bungee
- Cabin
- Cairo
- Caveat
- ChangaOne
- CommitMono
- CormorantGaramond
- CrimsonText
- DancingScript
- DMSans
- Dosis
- EBGaramond
- Exo2
- Figtree
- FiraSans
- FjallaOne
- GravitasOne
- Heebo
- Hind
- HindSiliguri
- IBMPlexSans
- Inconsolata
- Inter
- InterTight
- JosefinSans
- Jost
- Kanit
- Karla
- Lato
- Lexend
- LibreBaskerville
- LibreFranklin
- Lobster
- Lora
- Manrope
- Merriweather
- Montserrat
- MPLUSRounded1c
- Mukta
- Mulish
- NanumGothic
- NotoSans
- NotoSansArabic
- NotoSansJP
- NotoSansKR
- NotoSansSC
- NotoSansTC
- NotoSansTelugu
- NotoSerif
- NotoSerifJP
- Nunito
- NunitoSans
- OpenSans
- Oswald
- Outfit
- Overpass
- Oxygen
- Pacifico
- PlayfairDisplay
- PlusJakartaSans
- Poppins
- Prompt
- PTSans
- PTSerif
- PublicSans
- Quicksand
- Raleway
- Ramabhadra
- RedHatDisplay
- Roboto
- RobotoCondensed
- RobotoFlex
- RobotoMono
- RobotoSlab
- Rubik
- Saira
- SchibstedGrotesk
- ShareTech
- Slabo27px
- SmoochSans
- Sora
- SourceCodePro
- SourceSans3
- SpaceGrotesk
- StackSansHeadline
- TitilliumWeb
- Ubuntu
- WorkSans

To use additional fonts beyond the bundled set, provide them as base64-encoded font files. Fonts are matched by name, weight, and style. If a custom font file cannot be processed, Iteration Layer ignores that custom font and renders matching text with the bundled fallback font instead of failing the whole image request.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Font family name (referenced by text layers) |
| `weight` | string | Yes | Font weight: `thin`, `extralight`, `light`, `regular`, `medium`, `semibold`, `bold`, `extrabold`, `black` |
| `style` | string | Yes | One of: `normal`, `italic` |
| `buffer` | string | Yes | Base64-encoded font file (TTF, OTF, WOFF, or WOFF2) |

## Shared Layer Fields

All layer types share these base fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | integer | Yes | Render order (>= 0). Lower indices are rendered first (behind). |
| `type` | string | Yes | Layer type identifier |
| `opacity` | integer | No | Opacity percentage (0–100, default: 100) |

Layers that support positioning also include:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `position` | object | Yes | `x` (float, >= 0) and `y` (float, >= 0) offset from top-left |
| `dimensions` | object | Yes | `width` (integer, > 0) and `height` (integer, > 0) of the layer |
| `rotation_in_degrees` | float | No | Rotation angle in degrees |

## Layer Types

### solid-color

A solid color fill. When `position` and `dimensions` are omitted, fills the entire canvas. Supports rounded corners and angled edges.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hex_color` | string | Yes | Fill color (e.g., `#FF5500`) |
| `position` | object | No | Position on canvas (defaults to full canvas) |
| `dimensions` | object | No | Layer size (defaults to canvas size) |
| `rotation_in_degrees` | float | No | Rotation angle |
| `border_radius` | integer | No | Uniform corner radius in pixels |
| `border_top_left_radius` | integer | No | Top-left corner radius |
| `border_top_right_radius` | integer | No | Top-right corner radius |
| `border_bottom_left_radius` | integer | No | Bottom-left corner radius |
| `border_bottom_right_radius` | integer | No | Bottom-right corner radius |
| `angled_edges` | array | No | Angled edge definitions |

Set either `border_radius` for uniform corners or individual per-corner fields — not both.

```json
{
  "index": 0,
  "type": "solid-color",
  "hex_color": "#FFFFFF"
}
```

Positioned with rounded corners:

```json
{
  "index": 1,
  "type": "solid-color",
  "hex_color": "#3366FF",
  "position": {
    "x_in_px": 50.0,
    "y_in_px": 100.0
  },
  "dimensions": {
    "width_in_px": 300,
    "height_in_px": 200
  },
  "border_radius": 24
}
```

#### Angled Edges

Each angled edge definition cuts one side of the layer at an angle:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `edge` | string | Yes | One of: `left`, `right`, `top`, `bottom` |
| `angle_in_degrees` | float | Yes | Angle between -45.0 and 45.0 degrees |

```json
{
  "index": 1,
  "type": "solid-color",
  "hex_color": "#3366FF",
  "position": {
    "x_in_px": 50.0,
    "y_in_px": 100.0
  },
  "dimensions": {
    "width_in_px": 300,
    "height_in_px": 200
  },
  "angled_edges": [
    {
      "edge": "right",
      "angle_in_degrees": 15.0
    }
  ]
}
```

### gradient

A positioned gradient fill. Supports linear and radial gradients with configurable color stops and rounded corners.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gradient_type` | string | Yes | One of: `linear`, `radial` |
| `colors` | array | Yes | List of color stops (see below) |
| `position` | object | Yes | Position on canvas |
| `dimensions` | object | Yes | Gradient size |
| `angle_in_degrees` | float | No | Angle for linear gradients (default: 0, left-to-right) |
| `rotation_in_degrees` | float | No | Rotation angle |
| `border_radius` | integer | No | Uniform corner radius in pixels |
| `border_top_left_radius` | integer | No | Top-left corner radius |
| `border_top_right_radius` | integer | No | Top-right corner radius |
| `border_bottom_left_radius` | integer | No | Bottom-left corner radius |
| `border_bottom_right_radius` | integer | No | Bottom-right corner radius |

#### Color Stop

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hex_color` | string | Yes | Stop color (e.g., `#FF0000`) |
| `position` | float | Yes | Stop position as percentage (0.0–100.0) |

```json
{
  "index": 1,
  "type": "gradient",
  "gradient_type": "linear",
  "angle_in_degrees": 90.0,
  "colors": [
    {
      "hex_color": "#FF0000",
      "position": 0.0
    },
    {
      "hex_color": "#0000FF",
      "position": 100.0
    }
  ],
  "position": {
    "x_in_px": 0.0,
    "y_in_px": 0.0
  },
  "dimensions": {
    "width_in_px": 800,
    "height_in_px": 600
  }
}
```

### text

Render text with custom fonts, alignment, and optional markdown formatting. Supports `**bold**` and `*italic*` syntax. When `should_auto_scale` is `true`, the font size is automatically scaled down from `font_size_in_px` until the text fits within the layer dimensions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Text content (supports `**bold**` and `*italic*` markdown) |
| `font_name` | string | Yes | Font family name (any bundled font or a custom font definition) |
| `font_size_in_px` | integer | Yes | Font size in pixels (> 0) |
| `text_color` | string | Yes | Text color as hex (e.g., `#000000`) |
| `position` | object | Yes | Position on canvas |
| `dimensions` | object | Yes | Text bounding box |
| `font_weight` | string | No | Font weight: `thin`, `extralight`, `light`, `regular` (default), `medium`, `semibold`, `bold`, `extrabold`, `black` |
| `font_style` | string | No | One of: `normal`, `italic` |
| `text_align` | string | No | One of: `left`, `center`, `right` |
| `vertical_align` | string | No | One of: `top`, `center`, `bottom` |
| `is_splitting_lines` | boolean | No | Enable line wrapping (default: `true`) |
| `paragraph_spacing_in_px` | integer | No | Extra spacing between paragraphs |
| `should_auto_scale` | boolean | No | Automatically scale font size down to fit the layer dimensions (default: `false`) |
| `rotation_in_degrees` | float | No | Rotation angle |

```json
{
  "index": 2,
  "type": "text",
  "text": "**Important:** This is *formatted* text.",
  "font_name": "Inter",
  "font_size_in_px": 24,
  "text_color": "#333333",
  "text_align": "center",
  "vertical_align": "center",
  "position": {
    "x_in_px": 100.0,
    "y_in_px": 200.0
  },
  "dimensions": {
    "width_in_px": 600,
    "height_in_px": 150
  }
}
```

### image

An image layer. Provide the image as base64-encoded data or a URL. When `position` and `dimensions` are omitted, the image fills the entire canvas (cover-fit).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | object | Yes | Image source (see below) |
| `position` | object | No | Position on canvas (defaults to full canvas) |
| `dimensions` | object | No | Target dimensions (defaults to canvas size) |
| `rotation_in_degrees` | float | No | Rotation angle |
| `should_use_smart_cropping` | boolean | No | Use AI smart crop for resizing (default: `false`) |
| `should_remove_background` | boolean | No | Remove the image background using AI (default: `false`) |
| `border_radius` | integer | No | Uniform corner radius in pixels |
| `border_top_left_radius` | integer | No | Top-left corner radius |
| `border_top_right_radius` | integer | No | Top-right corner radius |
| `border_bottom_left_radius` | integer | No | Bottom-left corner radius |
| `border_bottom_right_radius` | integer | No | Bottom-right corner radius |

The `file` object supports two formats:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"base64"` or `"url"` |
| `name` | string | Filename (e.g., `"photo.png"`) |
| `base64` | string | Base64-encoded image data (when `type` is `"base64"`) |
| `url` | string | HTTPS image URL (when `type` is `"url"`). HTTP is not accepted. |

URL image inputs are fetched as website resources and respect the source site's `robots.txt`. If the site disallows crawling for the effective `User-Agent`, the request returns `400 Bad Request`; use a URL that allows crawler access or provide the image as base64 instead.

When `should_use_smart_cropping` is `true`, the image is cropped around detected faces, people, or objects using AI detection. When `false`, a standard cover-fit resize is used.

When `should_remove_background` is `true`, the image background is automatically removed using AI-powered segmentation before compositing. This is useful for placing product photos or portraits onto custom backgrounds.

Positioned with rounded corners:

```json
{
  "index": 1,
  "type": "image",
  "file": {
    "type": "base64",
    "name": "photo.png",
    "base64": "<base64-data>"
  },
  "position": {
    "x_in_px": 50.0,
    "y_in_px": 50.0
  },
  "dimensions": {
    "width_in_px": 200,
    "height_in_px": 200
  },
  "border_radius": 16,
  "should_use_smart_cropping": true
}
```

Full-canvas overlay:

```json
{
  "index": 3,
  "type": "image",
  "file": {
    "type": "base64",
    "name": "overlay.png",
    "base64": "<base64-data>"
  },
  "opacity": 50
}
```

### qr-code

Generate a QR code with custom colors.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | string | Yes | Data to encode in the QR code |
| `position` | object | Yes | Position on canvas |
| `dimensions` | object | Yes | QR code size |
| `foreground_hex_color` | string | Yes | Foreground (module) color |
| `background_hex_color` | string | Yes | Background color |
| `rotation_in_degrees` | float | No | Rotation angle |

```json
{
  "index": 2,
  "type": "qr-code",
  "value": "https://example.com",
  "position": {
    "x_in_px": 600.0,
    "y_in_px": 400.0
  },
  "dimensions": {
    "width_in_px": 150,
    "height_in_px": 150
  },
  "foreground_hex_color": "#000000",
  "background_hex_color": "#FFFFFF"
}
```

### barcode

Generate a barcode in one of the supported formats.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | string | Yes | Data to encode |
| `format` | string | Yes | One of: `code128`, `ean13`, `ean8`, `code39`, `itf`, `codabar` |
| `position` | object | Yes | Position on canvas |
| `dimensions` | object | Yes | Barcode size |
| `foreground_hex_color` | string | Yes | Bar color |
| `background_hex_color` | string | Yes | Background color |
| `rotation_in_degrees` | float | No | Rotation angle |

**Format notes:**
- `ean13` — Requires exactly 12 or 13 digits
- `ean8` — Requires exactly 7 or 8 digits
- `itf` — Requires an even number of digits
- `codabar` — Must start and end with A, B, C, or D
- `code128` — Supports alphanumeric characters
- `code39` — Supports uppercase letters, digits, and special characters

```json
{
  "index": 3,
  "type": "barcode",
  "value": "ABC123456",
  "format": "code128",
  "position": {
    "x_in_px": 100.0,
    "y_in_px": 450.0
  },
  "dimensions": {
    "width_in_px": 300,
    "height_in_px": 80
  },
  "foreground_hex_color": "#000000",
  "background_hex_color": "#FFFFFF"
}
```

### layout

A flow layout that arranges child layers horizontally or vertically. Supports gap spacing, cross-axis alignment, background color with padding and border radius, and optional fixed dimensions. Layout layers can be nested — child layers can include other layouts.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `direction` | string | No | `"horizontal"` (default) or `"vertical"` |
| `gap` | integer | No | Spacing between children in pixels (default: 0) |
| `horizontal_alignment` | string | No | Horizontal alignment: `"start"` (default), `"center"`, `"end"` |
| `vertical_alignment` | string | No | Vertical alignment: `"start"` (default), `"center"`, `"end"` |
| `layers` | array | Yes | Child layer definitions (any layer type, including layout) |
| `position` | object | No | Position on canvas |
| `dimensions` | object | No | Fixed width and height (clips if content is larger, pads with transparency if smaller) |
| `background_color` | string | No | Background color as hex (e.g., `#336699`) |
| `background_layers` | array | No | Array of layer definitions rendered behind content (overrides `background_color`) |
| `padding` | integer | No | Uniform inner padding in pixels |
| `padding_top` | integer | No | Top padding |
| `padding_right` | integer | No | Right padding |
| `padding_bottom` | integer | No | Bottom padding |
| `padding_left` | integer | No | Left padding |
| `border_radius` | integer | No | Uniform corner radius in pixels |
| `border_top_left_radius` | integer | No | Top-left corner radius |
| `border_top_right_radius` | integer | No | Top-right corner radius |
| `border_bottom_left_radius` | integer | No | Bottom-left corner radius |
| `border_bottom_right_radius` | integer | No | Bottom-right corner radius |

Set either `padding` for uniform padding or individual per-side fields — not both. Same for `border_radius` vs per-corner fields.

When `dimensions` is omitted, the layout auto-sizes to fit its content. Text layers with `"auto"` width inside a layout will shrink-wrap to their text content.

**Horizontal pill with icon and text:**

```json
{
  "index": 1,
  "type": "layout",
  "direction": "horizontal",
  "gap": 8,
  "vertical_alignment": "center",
  "background_color": "#0284c7",
  "padding": 12,
  "border_radius": 20,
  "position": {
    "x_in_px": 20.0,
    "y_in_px": 50.0
  },
  "layers": [
    {
      "type": "image",
      "file": {
        "type": "base64",
        "name": "icon.svg",
        "base64": "<base64-svg>"
      },
      "dimensions": {
        "width_in_px": 20,
        "height_in_px": 20
      }
    },
    {
      "type": "text",
      "text": "Click here",
      "font_name": "Inter",
      "font_size_in_px": 16,
      "text_color": "#FFFFFF",
      "dimensions": {
        "width_in_px": "auto",
        "height_in_px": 24
      }
    }
  ]
}
```

**Vertical card with fixed dimensions:**

```json
{
  "index": 2,
  "type": "layout",
  "direction": "vertical",
  "gap": 12,
  "background_color": "#FFFFFF",
  "padding": 24,
  "border_radius": 16,
  "dimensions": {
    "width_in_px": 300,
    "height_in_px": 200
  },
  "position": {
    "x_in_px": 50.0,
    "y_in_px": 100.0
  },
  "layers": [
    {
      "type": "text",
      "text": "Card Title",
      "font_name": "Inter",
      "font_size_in_px": 24,
      "font_weight": "bold",
      "text_color": "#1e293b",
      "dimensions": {
        "width_in_px": 252,
        "height_in_px": 32
      }
    },
    {
      "type": "text",
      "text": "Card description text goes here.",
      "font_name": "Inter",
      "font_size_in_px": 14,
      "text_color": "#64748b",
      "dimensions": {
        "width_in_px": 252,
        "height_in_px": 60
      }
    }
  ]
}
```

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

- [Generate Social Card](/recipes/generate-social-card) -- Create an Open Graph social sharing card with dynamic title, description, and branding.
- [Generate Certificate Image](/recipes/generate-certificate-image) -- Generate a certificate image with recipient name, course title, and completion date for digital sharing.
- [Generate YouTube Thumbnail](/recipes/generate-youtube-thumbnail) -- Generate a YouTube thumbnail with bold title text, gradient background, and a static image cutout.
- [Generate Product Listing Image](/recipes/generate-product-listing-image) -- Generate a product listing image with photo, price badge, and promotional text overlay.
- [Generate Event Ticket](/recipes/generate-event-ticket) -- Generate a scannable event ticket image with QR code, event details, and branding.
- [Generate Product Slide](/recipes/generate-product-slide) -- Generate a branded product slide with headline, feature pills, and CTA using layout layers.

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request (missing dimensions, missing layers, invalid hex color, unsupported barcode format, robots.txt-blocked URL input) |
| 401 | Missing or invalid API key |
| 422 | Processing error (image compositing error, text rendering error, barcode encoding error) |
| 429 | Rate limit exceeded |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/image-generation)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
