---
name: document-generation-api
description: Generate PDF, DOCX, EPUB, and PPTX documents from structured content blocks.
---

# Document Generation API

Generate PDF, DOCX, EPUB, and PPTX documents from structured content blocks.

**Cost:** 1 credits per request

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Generate PDF, DOCX, EPUB, and PPTX documents from a single API call. Send a structured document definition with metadata, page settings, styles, and content blocks, and receive the rendered document as base64-encoded JSON in the response.

## Key Features

- **Multi-Format Output** -- Generate PDF, DOCX, EPUB, and PPTX from one unified document structure.
- **Rich Content Blocks** -- Paragraphs with rich text runs, headlines (h1-h6), images, tables, grids, lists, QR codes, barcodes, and more.
- **12-Column Grid Layout** -- Arrange content blocks side by side using a flexible 12-column grid system.
- **Optional Styles with Sensible Defaults** -- Styles and page settings are optional. Defaults use PlusJakartaSans for body text, Outfit for headings, black text, sky-500 links, A4 pages with 72pt margins.
- **Font Weight Support** -- Full range from thin to black, not just bold/not-bold. PDF and EPUB render all weights; DOCX and PPTX map semibold and above to bold.
- **Two-Layer Style System** -- Define document-wide default styles, then override per block for full control.
- **Headers and Footers** -- Repeating headers and footers with the same block types as body content, plus page numbers.
- **Bundled Google Fonts + Custom Fonts** -- The top Google Fonts are bundled and available by default. Upload additional font files (base64-encoded) with weight and style metadata for full typographic control.
- **Page Size Presets** -- Built-in presets (A0-A6, B0-B6, Letter, Legal, Tabloid, Executive, Statement) plus custom dimensions.
- **Table of Contents** -- Auto-generated from headlines with configurable levels and dot leaders.
- **PPTX Slide Support** -- Each page-break creates a new slide in PowerPoint output.

## Overview

The Document Generation API renders structured documents from a JSON definition. You send a format, document metadata, and an ordered list of content blocks, and receive the rendered document as base64-encoded JSON. Page settings and styles are optional -- sensible defaults are applied automatically (A4 with 72pt margins, PlusJakartaSans body, Outfit headings, black text, sky-500 links).

**Endpoint:** `POST /document-generation/v1/generate`

**Supported output formats:** PDF, DOCX, EPUB, PPTX

## Request Format

<!-- tabs -->

```bash
curl -X POST \
  https://api.iterationlayer.com/document-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "document": {
      "metadata": {
        "title": "Quarterly Report",
        "author": "Acme Corp",
        "language": "en"
      },
      "page": {
        "size": {
          "preset": "A4"
        },
        "margins": {
          "top_in_pt": 72.0,
          "right_in_pt": 72.0,
          "bottom_in_pt": 72.0,
          "left_in_pt": 72.0
        }
      },
      "styles": {
        "text": {
          "font_family": "Helvetica",
          "font_size_in_pt": 12.0,
          "line_height": 1.5,
          "color": "#000000"
        },
        "headline": {
          "font_family": "Helvetica",
          "font_size_in_pt": 24.0,
          "color": "#111111",
          "spacing_before_in_pt": 12.0,
          "spacing_after_in_pt": 6.0,
          "font_weight": "bold"
        },
        "link": {
          "color": "#0066CC",
          "is_underlined": true
        },
        "list": {
          "text_style": {
            "font_family": "Helvetica",
            "font_size_in_pt": 12.0,
            "line_height": 1.5,
            "color": "#000000"
          },
          "marker_color": "#000000",
          "marker_gap_in_pt": 8.0
        },
        "table": {
          "header": {
            "background_color": "#333333",
            "text_color": "#FFFFFF",
            "font_size_in_pt": 12.0,
            "font_weight": "bold"
          },
          "body": {
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "font_size_in_pt": 11.0
          },
          "border": {
            "outer": {
              "top": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "right": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "bottom": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              },
              "left": {
                "color": "#CCCCCC",
                "width_in_pt": 1.0
              }
            },
            "inner": {
              "horizontal": {
                "color": "#EEEEEE",
                "width_in_pt": 0.5
              },
              "vertical": {
                "color": "#EEEEEE",
                "width_in_pt": 0.5
              }
            }
          }
        },
        "grid": {
          "background_color": "#FFFFFF",
          "border_color": "#CCCCCC",
          "border_width_in_pt": 0.0,
          "gap_in_pt": 12.0
        },
        "separator": {
          "color": "#CCCCCC",
          "thickness_in_pt": 1.0,
          "spacing_before_in_pt": 12.0,
          "spacing_after_in_pt": 12.0
        },
        "image": {
          "border_color": "#000000",
          "border_width_in_pt": 0.0
        }
      },
      "content": [
        {
          "type": "headline",
          "level": "h1",
          "text": "Quarterly Report"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "This is "
            },
            {
              "text": "bold text",
              "font_weight": "bold"
            },
            {
              "text": " in a paragraph."
            }
          ]
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({
  apiKey: "YOUR_API_KEY",
});

const result = await client.generateDocument({
  format: "pdf",
  document: {
    metadata: {
      title: "Quarterly Report",
      author: "Acme Corp",
      language: "en",
    },
    page: {
      size: {
        preset: "A4",
      },
      margins: {
        top_in_pt: 72.0,
        right_in_pt: 72.0,
        bottom_in_pt: 72.0,
        left_in_pt: 72.0,
      },
    },
    styles: {
      text: {
        font_family: "Helvetica",
        font_size_in_pt: 12.0,
        line_height: 1.5,
        color: "#000000",
      },
      headline: {
        font_family: "Helvetica",
        font_size_in_pt: 24.0,
        color: "#111111",
        spacing_before_in_pt: 12.0,
        spacing_after_in_pt: 6.0,
        font_weight: "bold",
      },
      link: {
        color: "#0066CC",
        is_underlined: true,
      },
      list: {
        text_style: {
          font_family: "Helvetica",
          font_size_in_pt: 12.0,
          line_height: 1.5,
          color: "#000000",
        },
        marker_color: "#000000",
        marker_gap_in_pt: 8.0,
      },
      table: {
        header: {
          background_color: "#333333",
          text_color: "#FFFFFF",
          font_size_in_pt: 12.0,
          font_weight: "bold",
        },
        body: {
          background_color: "#FFFFFF",
          text_color: "#000000",
          font_size_in_pt: 11.0,
        },
        border: {
          outer: {
            top: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            right: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            bottom: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
            left: {
              color: "#CCCCCC",
              width_in_pt: 1.0,
            },
          },
          inner: {
            horizontal: {
              color: "#EEEEEE",
              width_in_pt: 0.5,
            },
            vertical: {
              color: "#EEEEEE",
              width_in_pt: 0.5,
            },
          },
        },
      },
      grid: {
        background_color: "#FFFFFF",
        border_color: "#CCCCCC",
        border_width_in_pt: 0.0,
        gap_in_pt: 12.0,
      },
      separator: {
        color: "#CCCCCC",
        thickness_in_pt: 1.0,
        spacing_before_in_pt: 12.0,
        spacing_after_in_pt: 12.0,
      },
      image: {
        border_color: "#000000",
        border_width_in_pt: 0.0,
      },
    },
    content: [
      {
        type: "headline",
        level: "h1",
        text: "Quarterly Report",
      },
      {
        type: "paragraph",
        runs: [
          {
            text: "This is ",
          },
          {
            text: "bold text",
            font_weight: "bold",
          },
          {
            text: " in a paragraph.",
          },
        ],
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.generate_document(
    format="pdf",
    document={
        "metadata": {
            "title": "Quarterly Report",
            "author": "Acme Corp",
            "language": "en",
        },
        "page": {
            "size": {
                "preset": "A4",
            },
            "margins": {
                "top_in_pt": 72.0,
                "right_in_pt": 72.0,
                "bottom_in_pt": 72.0,
                "left_in_pt": 72.0,
            },
        },
        "styles": {
            "text": {
                "font_family": "Helvetica",
                "font_size_in_pt": 12.0,
                "line_height": 1.5,
                "color": "#000000",
            },
            "headline": {
                "font_family": "Helvetica",
                "font_size_in_pt": 24.0,
                "color": "#111111",
                "spacing_before_in_pt": 12.0,
                "spacing_after_in_pt": 6.0,
                "font_weight": "bold",
            },
            "link": {
                "color": "#0066CC",
                "is_underlined": True,
            },
            "list": {
                "text_style": {
                    "font_family": "Helvetica",
                    "font_size_in_pt": 12.0,
                    "line_height": 1.5,
                    "color": "#000000",
                },
                "marker_color": "#000000",
                "marker_gap_in_pt": 8.0,
            },
            "table": {
                "header": {
                    "background_color": "#333333",
                    "text_color": "#FFFFFF",
                    "font_size_in_pt": 12.0,
                    "font_weight": "bold",
                },
                "body": {
                    "background_color": "#FFFFFF",
                    "text_color": "#000000",
                    "font_size_in_pt": 11.0,
                },
                "border": {
                    "outer": {
                        "top": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "right": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "bottom": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                        "left": {
                            "color": "#CCCCCC",
                            "width_in_pt": 1.0,
                        },
                    },
                    "inner": {
                        "horizontal": {
                            "color": "#EEEEEE",
                            "width_in_pt": 0.5,
                        },
                        "vertical": {
                            "color": "#EEEEEE",
                            "width_in_pt": 0.5,
                        },
                    },
                },
            },
            "grid": {
                "background_color": "#FFFFFF",
                "border_color": "#CCCCCC",
                "border_width_in_pt": 0.0,
                "gap_in_pt": 12.0,
            },
            "separator": {
                "color": "#CCCCCC",
                "thickness_in_pt": 1.0,
                "spacing_before_in_pt": 12.0,
                "spacing_after_in_pt": 12.0,
            },
            "image": {
                "border_color": "#000000",
                "border_width_in_pt": 0.0,
            },
        },
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "Quarterly Report",
            },
            {
                "type": "paragraph",
                "runs": [
                    {
                        "text": "This is ",
                    },
                    {
                        "text": "bold text",
                        "font_weight": "bold",
                    },
                    {
                        "text": " in a paragraph.",
                    },
                ],
            },
        ],
    },
)
```

```go
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")

result, err := client.GenerateDocument(
	il.GenerateDocumentRequest{
		Format: "pdf",
		Document: il.DocumentDefinition{
			Metadata: il.DocumentMetadata{
				Title:    "Quarterly Report",
				Author:   "Acme Corp",
				Language: "en",
			},
			Page: il.DocumentPage{
				Size: il.DocPageSize{
				Preset: "A4",
			},
				Margins: il.DocMargins{
					TopInPt:    72,
					RightInPt:  72,
					BottomInPt: 72,
					LeftInPt:   72,
				},
			},
			Styles: il.DocumentStyles{
				Text: il.TextStyle{
					FontFamily:  "Helvetica",
					FontSizeInPt: 12,
					Color:       "#000000",
					LineHeight:  1.5,
				},
				Headline: il.HeadlineStyle{
					FontFamily:        "Helvetica",
					FontSizeInPt:      24,
					Color:             "#111111",
					SpacingBeforeInPt: 12,
					SpacingAfterInPt:  6,
					FontWeight:        "bold",
				},
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "Quarterly Report"),
				il.ParagraphBlock{
					Type: "paragraph",
					Runs: []il.TextRun{
						{
							Text: "This is ",
						},
						{
							Text:       "bold text",
							FontWeight: "bold",
						},
						{
							Text: " in a paragraph.",
						},
					},
				},
			},
		},
	},
)
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "buffer": "JVBERi0xLjcKMSAwIG9iago8...",
    "mime_type": "application/pdf"
  }
}
```

<!-- /tabs -->

## Document Structure

The top-level request has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format` | string | Yes | Output format: `pdf`, `docx`, `epub`, or `pptx` |
| `document` | object | Yes | The full document definition (see below) |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

The `document` object contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `metadata` | object | Yes | Document metadata (title, author, language) |
| `page` | object | No | Page size and margins. Defaults to A4 with 72pt margins |
| `fonts` | array | No | Custom font definitions (base64-encoded font files) |
| `styles` | object | No | Document-wide default styles. Defaults to PlusJakartaSans body, Outfit headings, black text, sky-500 links |
| `header` | array | No | Content blocks rendered at the top of every page |
| `footer` | array | No | Content blocks rendered at the bottom of every page |
| `header_distance_from_edge_in_pt` | float | No | Distance from the page edge to the header |
| `footer_distance_from_edge_in_pt` | float | No | Distance from the page edge to the footer |
| `content` | array | Yes | Ordered list of content blocks |

### Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Document title (min 1 character) |
| `author` | string | No | Document author |
| `language` | string | No | Language code (min 2 characters, e.g., `"en"`) |

```json
{
  "metadata": {
    "title": "Annual Report 2025",
    "author": "Acme Corp",
    "language": "en"
  }
}
```

### Page Settings

The `page` object controls page dimensions, margins, and background color.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `size` | object | Yes | Page size (preset or custom dimensions) |
| `margins` | object | Yes | Page margins |
| `background_color` | string | No | Hex color for the page background (e.g., `#FFFFFF`) |

**Page size** -- use a preset or provide custom dimensions:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `preset` | string | No | One of: `A0`-`A6`, `B0`-`B6`, `Letter`, `Legal`, `Tabloid`, `Executive`, `Statement` |
| `width_in_pt` | float | No | Custom width in points (>= 1) |
| `height_in_pt` | float | No | Custom height in points (>= 1) |

Use either `preset` or both `width_in_pt` and `height_in_pt`.

**Margins:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `top_in_pt` | float | Yes | Top margin in points (>= 0) |
| `right_in_pt` | float | Yes | Right margin in points (>= 0) |
| `bottom_in_pt` | float | Yes | Bottom margin in points (>= 0) |
| `left_in_pt` | float | Yes | Left margin in points (>= 0) |

```json
{
  "page": {
    "size": {
      "preset": "A4"
    },
    "margins": {
      "top_in_pt": 72.0,
      "right_in_pt": 72.0,
      "bottom_in_pt": 72.0,
      "left_in_pt": 72.0
    },
    "background_color": "#FFFFFF"
  }
}
```

### Custom Fonts

The top Google Fonts are bundled and available by default. Documents can reference any bundled font by name without providing font definitions. If a font name isn't found, it falls back to Inter Regular.

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

To use additional fonts beyond the bundled set, upload them as base64-encoded font files. Each font definition requires a name, weight, style, and the font file data.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Font family name (min 1 character) |
| `weight` | string | Yes | One of: `thin`, `extralight`, `light`, `regular`, `medium`, `semibold`, `bold`, `extrabold`, `black` |
| `style` | string | Yes | One of: `normal`, `italic` |
| `buffer` | string | Yes | Base64-encoded font file (TTF, OTF, WOFF, or WOFF2) |

```json
{
  "fonts": [
    {
      "name": "CustomFont",
      "weight": "regular",
      "style": "normal",
      "buffer": "<base64-encoded-font-file>"
    },
    {
      "name": "CustomFont",
      "weight": "bold",
      "style": "normal",
      "buffer": "<base64-encoded-font-file>"
    }
  ]
}
```

## Style System

The style system uses a two-layer merge approach: you define document-wide default styles in the `styles` object, and optionally override any property per content block using the block's `styles` field.

The `styles` object contains defaults for all block types:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | object | No | Default text/paragraph style |
| `headline` | object | No | Default headline style |
| `link` | object | No | Default link style |
| `list` | object | No | Default list style |
| `table` | object | No | Default table style |
| `grid` | object | No | Default grid style |
| `separator` | object | No | Default separator style |
| `image` | object | No | Default image style |

### Text Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `font_family` | string | Yes | Font family name |
| `font_size_in_pt` | float | Yes | Font size in points (>= 1) |
| `line_height` | float | Yes | Line height multiplier (>= 0.5) |
| `color` | string | Yes | Text color as hex (e.g., `#000000`) |
| `font_weight` | string | No | Font weight: `thin`, `extralight`, `light`, `regular`, `medium`, `semibold`, `bold`, `extrabold`, `black`. PDF/EPUB render all weights. DOCX/PPTX map `semibold` and above to bold. |
| `is_italic` | boolean | No | Italic text |

### Headline Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `font_family` | string | Yes | Font family name |
| `font_size_in_pt` | float | Yes | Font size in points (>= 1) |
| `color` | string | Yes | Headline color as hex |
| `spacing_before_in_pt` | float | Yes | Space before the headline (>= 0) |
| `spacing_after_in_pt` | float | Yes | Space after the headline (>= 0) |
| `font_weight` | string | No | Font weight: `thin`, `extralight`, `light`, `regular`, `medium`, `semibold`, `bold`, `extrabold`, `black`. PDF/EPUB render all weights. DOCX/PPTX map `semibold` and above to bold. |
| `is_italic` | boolean | No | Italic text |

### Link Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `color` | string | Yes | Link color as hex |
| `is_underlined` | boolean | No | Whether links are underlined |

### List Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text_style` | object | Yes | Text style for list items (same fields as text style) |
| `marker_color` | string | Yes | Bullet/number color as hex |
| `marker_gap_in_pt` | float | Yes | Gap between marker and text (>= 0) |

### Table Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `header` | object | Yes | Header row style: `background_color`, `text_color`, `font_size_in_pt`, `font_weight` |
| `body` | object | Yes | Body row style: `background_color`, `text_color`, `font_size_in_pt` |
| `border` | object | Yes | Border style with `outer` (top, right, bottom, left) and `inner` (horizontal, vertical) -- each with `color` and `width_in_pt` |

### Grid Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `background_color` | string | Yes | Grid background color as hex |
| `border_color` | string | Yes | Grid border color as hex |
| `border_width_in_pt` | float | Yes | Border width in points (>= 0) |
| `gap_in_pt` | float | Yes | Gap between columns in points (>= 0) |

### Separator Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `color` | string | Yes | Line color as hex |
| `thickness_in_pt` | float | Yes | Line thickness in points (>= 0) |
| `spacing_before_in_pt` | float | Yes | Space before the separator (>= 0) |
| `spacing_after_in_pt` | float | Yes | Space after the separator (>= 0) |

### Image Style

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `border_color` | string | Yes | Border color as hex |
| `border_width_in_pt` | float | Yes | Border width in points (>= 0) |

## Content Blocks

Content blocks are the building blocks of your document. They are provided as an ordered array in the `content` field and rendered sequentially.

### paragraph

A text paragraph composed of one or more rich text runs. Each run can have independent bold, italic, and link formatting. Alternatively, use `markdown` for simple Markdown-formatted text.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"paragraph"` |
| `runs` | array | No | Array of text runs (see below) |
| `markdown` | string | No | Markdown-formatted text (alternative to `runs`) |
| `text_alignment` | string | No | One of: `left`, `center`, `right`, `justify` |
| `styles` | object | No | Text style overrides |

**Text run:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | The text content (min 1 character) |
| `font_weight` | string | No | Font weight (same values as text style) |
| `is_italic` | boolean | No | Italic formatting |
| `link_url` | string | No | Makes the run a hyperlink |

```json
{
  "type": "paragraph",
  "runs": [
    {
      "text": "Visit our "
    },
    {
      "text": "website",
      "font_weight": "bold",
      "link_url": "https://example.com"
    },
    {
      "text": " for details."
    }
  ],
  "text_alignment": "justify"
}
```

### headline

A heading from level h1 to h6. Optionally participates in the table of contents.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"headline"` |
| `level` | string | Yes | One of: `h1`, `h2`, `h3`, `h4`, `h5`, `h6` |
| `text` | string | Yes | Headline text (min 1 character) |
| `styles` | object | No | Headline style overrides |
| `table_of_contents` | object | No | Table of contents settings (see below) |

**Table of contents options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_included` | boolean | No | Whether this headline appears in the TOC |
| `label_override` | string | No | Custom label in the TOC (min 1 character) |
| `level_override` | string | No | Override the TOC indentation level (`h1`-`h6`) |

```json
{
  "type": "headline",
  "level": "h2",
  "text": "Chapter 1: Introduction",
  "table_of_contents": {
    "is_included": true
  }
}
```

### image

An inline image with specified dimensions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"image"` |
| `buffer` | string | Yes | Base64-encoded image data |
| `width_in_pt` | float | Yes | Display width in points (>= 1) |
| `height_in_pt` | float | Yes | Display height in points (>= 1) |
| `fit` | string | No | One of: `cover`, `contain` |
| `styles` | object | No | Image style overrides |

```json
{
  "type": "image",
  "buffer": "<base64-encoded-image>",
  "width_in_pt": 400.0,
  "height_in_pt": 300.0,
  "fit": "contain"
}
```

### table

A data table with optional header row, column widths, and cell-level formatting.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"table"` |
| `header` | object | No | Header row with `cells` array |
| `rows` | array | Yes | Array of row objects, each with a `cells` array |
| `column_widths_in_percent` | array | No | Column width percentages (each >= 1) |
| `styles` | object | No | Table style overrides |

**Table cell:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Cell content (min 1 character) |
| `horizontal_alignment` | string | No | One of: `left`, `center`, `right` |
| `column_span` | integer | No | Number of columns to span (>= 1) |
| `row_span` | integer | No | Number of rows to span (>= 1) |
| `styles` | object | No | Cell-level style overrides: `background_color`, `text_color`, `font_size_in_pt`, `font_weight`, `is_italic` |

```json
{
  "type": "table",
  "header": {
    "cells": [
      {
        "text": "Product"
      },
      {
        "text": "Qty",
        "horizontal_alignment": "right"
      },
      {
        "text": "Price",
        "horizontal_alignment": "right"
      }
    ]
  },
  "rows": [
    {
      "cells": [
        {
          "text": "Widget A"
        },
        {
          "text": "100",
          "horizontal_alignment": "right"
        },
        {
          "text": "$9.99",
          "horizontal_alignment": "right"
        }
      ]
    }
  ],
  "column_widths_in_percent": [50.0, 25.0, 25.0]
}
```

### grid

A 12-column grid layout for placing content blocks side by side. Each column specifies a `column_span` (1-12) and contains its own array of content blocks.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"grid"` |
| `columns` | array | Yes | Array of column objects (see below) |
| `horizontal_alignment` | string | No | One of: `left`, `center`, `right` |
| `vertical_alignment` | string | No | One of: `top`, `center`, `bottom` |
| `styles` | object | No | Grid style overrides |

**Grid column:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `column_span` | integer | Yes | Number of columns to span (1-12) |
| `horizontal_alignment` | string | No | One of: `left`, `center`, `right` |
| `vertical_alignment` | string | No | One of: `top`, `center`, `bottom` |
| `blocks` | array | Yes | Content blocks within the column |

```json
{
  "type": "grid",
  "columns": [
    {
      "column_span": 6,
      "blocks": [
        {
          "type": "headline",
          "level": "h3",
          "text": "Left Column"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Content on the left."
            }
          ]
        }
      ]
    },
    {
      "column_span": 6,
      "blocks": [
        {
          "type": "headline",
          "level": "h3",
          "text": "Right Column"
        },
        {
          "type": "paragraph",
          "runs": [
            {
              "text": "Content on the right."
            }
          ]
        }
      ]
    }
  ]
}
```

### list

An ordered or unordered list with support for nested items.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"list"` |
| `variant` | string | Yes | `"ordered"` or `"unordered"` |
| `items` | array | Yes | Array of list items (see below) |
| `styles` | object | No | List style overrides |

**List item:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Item text (min 1 character) |
| `children` | array | No | Nested list items |

```json
{
  "type": "list",
  "variant": "unordered",
  "items": [
    {
      "text": "First item"
    },
    {
      "text": "Second item",
      "children": [
        {
          "text": "Nested item A"
        },
        {
          "text": "Nested item B"
        }
      ]
    },
    {
      "text": "Third item"
    }
  ]
}
```

### table-of-contents

An auto-generated table of contents built from headline blocks that have `table_of_contents.is_included` set to `true`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"table-of-contents"` |
| `levels` | array | Yes | Which headline levels to include (e.g., `["h1", "h2", "h3"]`) |
| `leader` | string | Yes | Leader style between title and page number: `"dots"` or `"none"` |
| `text_alignment` | string | No | One of: `left`, `center`, `right`, `justify` |
| `styles` | object | No | Text style overrides |

```json
{
  "type": "table-of-contents",
  "levels": ["h1", "h2", "h3"],
  "leader": "dots"
}
```

### page-break

Forces a page break at this point. In PPTX output, each page-break creates a new slide.

```json
{
  "type": "page-break"
}
```

### separator

A horizontal rule/divider line.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"separator"` |
| `styles` | object | No | Separator style overrides |

```json
{
  "type": "separator"
}
```

### page-number

Renders the current page number. Only valid in headers and footers.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"page-number"` |
| `text_alignment` | string | No | One of: `left`, `center`, `right`, `justify` |
| `styles` | object | No | Text style overrides |

```json
{
  "type": "page-number",
  "text_alignment": "center"
}
```

### qr-code

Renders a QR code from a string value.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"qr-code"` |
| `value` | string | Yes | Data to encode (min 1 character) |
| `width_in_pt` | integer | Yes | Width in points (>= 1) |
| `height_in_pt` | integer | Yes | Height in points (>= 1) |
| `fg_hex_color` | string | Yes | Foreground color as hex (e.g., `#000000`) |
| `bg_hex_color` | string | Yes | Background color as hex (e.g., `#FFFFFF`) |

```json
{
  "type": "qr-code",
  "value": "https://example.com",
  "width_in_pt": 100,
  "height_in_pt": 100,
  "fg_hex_color": "#000000",
  "bg_hex_color": "#FFFFFF"
}
```

### barcode

Renders a barcode in one of several standard formats.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"barcode"` |
| `value` | string | Yes | Data to encode (min 1 character) |
| `format` | string | Yes | One of: `code128`, `ean13`, `ean8`, `code39`, `itf`, `codabar` |
| `width_in_pt` | integer | Yes | Width in points (>= 1) |
| `height_in_pt` | integer | Yes | Height in points (>= 1) |
| `fg_hex_color` | string | Yes | Foreground color as hex |
| `bg_hex_color` | string | Yes | Background color as hex |

```json
{
  "type": "barcode",
  "value": "1234567890128",
  "format": "ean13",
  "width_in_pt": 200,
  "height_in_pt": 80,
  "fg_hex_color": "#000000",
  "bg_hex_color": "#FFFFFF"
}
```

## Headers and Footers

Headers and footers accept the same content block types as the document body, with the addition of `page-number` and the exclusion of `table-of-contents` and `page-break`. They are rendered on every page.

**Supported block types in headers/footers:** `paragraph`, `headline`, `image`, `table`, `grid`, `list`, `page-number`, `separator`, `qr-code`, `barcode`

```json
{
  "header": [
    {
      "type": "paragraph",
      "runs": [
        {
          "text": "Acme Corp -- Confidential"
        }
      ],
      "text_alignment": "right"
    }
  ],
  "footer": [
    {
      "type": "grid",
      "columns": [
        {
          "column_span": 6,
          "blocks": [
            {
              "type": "paragraph",
              "runs": [
                {
                  "text": "Acme Corp"
                }
              ]
            }
          ]
        },
        {
          "column_span": 6,
          "blocks": [
            {
              "type": "page-number",
              "text_alignment": "right"
            }
          ]
        }
      ]
    }
  ],
  "header_distance_from_edge_in_pt": 36.0,
  "footer_distance_from_edge_in_pt": 36.0
}
```

## PPTX Notes

When generating PPTX (PowerPoint) output:

- The initial content before the first `page-break` becomes the first slide.
- Each `page-break` block creates a new slide.
- All content blocks between page breaks are placed on the same slide.
- Page size settings map to slide dimensions.

## Format Compatibility

Not all features are supported equally across output formats. The table below shows per-format feature support:

| Feature | PDF | DOCX | PPTX | EPUB |
|---------|-----|------|------|------|
| Paragraph (rich text) | ✅ | ✅ | ✅ | ✅ |
| Headline (h1-h6 sizes) | ✅ | ✅ | ✅ | ✅ |
| Image | ✅ | ✅ | ✅ | ✅ |
| QR Code | ✅ | ✅ | ✅ | ✅ |
| Barcode | ✅ | ✅ | ✅ | ✅ |
| Table | ✅ | ✅ | ✅ | ✅ |
| Grid (columns) | ✅ | ✅ | ✅ | ✅ |
| List (ordered/unordered) | ✅ | ✅ | ✅ | ✅ |
| Nested lists | ✅ | ✅ | ✅ | ✅ |
| Table of Contents | ✅ | ✅ | ✅ | ✅ |
| Page Break | ✅ | ✅ | ✅ | ✅ |
| Separator | ✅ | ✅ | ✅ | ✅ |
| Page Number | ✅ | ✅ | ✅ | ❌ |
| Header / Footer | ✅ | ✅ | ❌ | ❌ |
| Font Weight (thin–black) | ✅ | ⚠️ | ⚠️ | ✅ |
| Custom Fonts | ✅ | ✅ | ✅ | ✅ |
| Page Background Color | ✅ | ✅ | ✅ | ❌ |
| Table Cell Backgrounds | ✅ | ✅ | ✅ | ✅ |

**Notes:**

- **Font Weight (DOCX/PPTX):** DOCX and PPTX only support bold on/off. Weights `semibold`, `bold`, `extrabold`, and `black` render as bold. All lighter weights (`thin` through `medium`) render as normal. PDF and EPUB render the full 100--900 numeric weight range, so all weights are visually distinct when the font supports them.
- **Table of Contents (DOCX):** DOCX table of contents entries are inserted as static text. To make them interactive with page numbers in Microsoft Word, right-click the TOC and select "Update Field" after opening the document.

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

- [Generate PDF Invoice](/recipes/generate-pdf-invoice) -- Generate a professional PDF invoice with company branding, line items, and totals.
- [Generate PDF Report](/recipes/generate-pdf-report) -- Generate a professional PDF report with title, executive summary, data table, and footer.
- [Generate DOCX Contract](/recipes/generate-docx-contract) -- Generate an editable DOCX service agreement with parties, terms, and payment schedule.
- [Generate Shipping Label](/recipes/generate-shipping-label) -- Generate a compact PDF shipping label with sender and recipient addresses, barcode, and tracking number.
- [Generate Restaurant Menu](/recipes/generate-restaurant-menu) -- Generate a branded restaurant menu PDF with sections, items, prices, and descriptions.

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request (validation errors, missing required fields, invalid base64 font data) |
| 401 | Missing or invalid API key |
| 422 | Processing error (document rendering failure) |
| 429 | Rate limit exceeded |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/document-generation)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
