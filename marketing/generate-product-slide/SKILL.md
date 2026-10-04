---
name: generate-product-slide
description: Generate a branded product slide image with headline, feature pills, and a call-to-action — all arranged with layout layers.
---

# Generate Product Slide

Marketing teams and SaaS companies use this recipe to generate branded slides at scale — for pitch decks, product launches, or social media carousels. Use layout layers to arrange headlines, feature pills, and CTAs without manual pixel positioning. Swap in your brand colors, logo, and copy to produce consistent slides across campaigns.

## APIs Used

Image Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST \
  https://api.iterationlayer.com/image-generation/v1/render \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimensions": {
      "width_in_px": 1200,
      "height_in_px": 675
    },
    "output_format": "png",
    "layers": [
      {
        "index": 0,
        "type": "solid-color",
        "hex_color": "#0F172A"
      },
      {
        "index": 1,
        "type": "text",
        "text": "Your Headline Goes Here",
        "font_name": "Inter",
        "font_size_in_px": 52,
        "text_color": "#FFFFFF",
        "font_weight": "bold",
        "position": { "x_in_px": 80.0, "y_in_px": 80.0 },
        "dimensions": { "width_in_px": 800, "height_in_px": 140 }
      },
      {
        "index": 2,
        "type": "text",
        "text": "A short subtitle that explains the value proposition in one line.",
        "font_name": "Inter",
        "font_size_in_px": 22,
        "text_color": "#94A3B8",
        "position": { "x_in_px": 80.0, "y_in_px": 240.0 },
        "dimensions": { "width_in_px": 900, "height_in_px": 40 }
      },
      {
        "index": 3,
        "type": "layout",
        "direction": "horizontal",
        "gap": 12,
        "position": { "x_in_px": 80.0, "y_in_px": 320.0 },
        "layers": [
          {
            "type": "layout",
            "direction": "horizontal",
            "background_color": "#1E293B",
            "padding": 10,
            "border_radius": 20,
            "layers": [
              {
                "type": "text",
                "text": "Feature One",
                "font_name": "Inter",
                "font_size_in_px": 14,
                "text_color": "#94A3B8",
                "dimensions": { "width_in_px": "auto", "height_in_px": 20 }
              }
            ]
          },
          {
            "type": "layout",
            "direction": "horizontal",
            "background_color": "#1E293B",
            "padding": 10,
            "border_radius": 20,
            "layers": [
              {
                "type": "text",
                "text": "Feature Two",
                "font_name": "Inter",
                "font_size_in_px": 14,
                "text_color": "#94A3B8",
                "dimensions": { "width_in_px": "auto", "height_in_px": 20 }
              }
            ]
          },
          {
            "type": "layout",
            "direction": "horizontal",
            "background_color": "#1E293B",
            "padding": 10,
            "border_radius": 20,
            "layers": [
              {
                "type": "text",
                "text": "Feature Three",
                "font_name": "Inter",
                "font_size_in_px": 14,
                "text_color": "#94A3B8",
                "dimensions": { "width_in_px": "auto", "height_in_px": 20 }
              }
            ]
          }
        ]
      },
      {
        "index": 4,
        "type": "layout",
        "direction": "vertical",
        "gap": 14,
        "position": { "x_in_px": 80.0, "y_in_px": 420.0 },
        "layers": [
          {
            "type": "text",
            "text": "Benefit number one",
            "font_name": "Inter",
            "font_size_in_px": 20,
            "text_color": "#E2E8F0",
            "dimensions": { "width_in_px": "auto", "height_in_px": 28 }
          },
          {
            "type": "text",
            "text": "Benefit number two",
            "font_name": "Inter",
            "font_size_in_px": 20,
            "text_color": "#E2E8F0",
            "dimensions": { "width_in_px": "auto", "height_in_px": 28 }
          },
          {
            "type": "text",
            "text": "Benefit number three",
            "font_name": "Inter",
            "font_size_in_px": 20,
            "text_color": "#E2E8F0",
            "dimensions": { "width_in_px": "auto", "height_in_px": 28 }
          }
        ]
      },
      {
        "index": 5,
        "type": "layout",
        "direction": "horizontal",
        "vertical_alignment": "center",
        "background_color": "#3B82F6",
        "padding": 14,
        "border_radius": 24,
        "position": { "x_in_px": 80.0, "y_in_px": 600.0 },
        "layers": [
          {
            "type": "text",
            "text": "Call to action",
            "font_name": "Inter",
            "font_size_in_px": 16,
            "font_weight": "bold",
            "text_color": "#FFFFFF",
            "dimensions": { "width_in_px": "auto", "height_in_px": 22 }
          }
        ]
      }
    ]
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const pill = (label: string) => ({
  type: "layout" as const,
  direction: "horizontal" as const,
  background_color: "#1E293B",
  padding: 10,
  border_radius: 20,
  layers: [
    {
      type: "text" as const,
      text: label,
      font_name: "Inter",
      font_size_in_px: 14,
      text_color: "#94A3B8",
      dimensions: { width_in_px: "auto", height_in_px: 20 },
    },
  ],
});

const listItem = (label: string) => ({
  type: "text" as const,
  text: label,
  font_name: "Inter",
  font_size_in_px: 20,
  text_color: "#E2E8F0",
  dimensions: { width_in_px: "auto", height_in_px: 28 },
});

const result = await client.generateImage({
  dimensions: { width_in_px: 1200, height_in_px: 675 },
  output_format: "png",
  layers: [
    {
      index: 0,
      type: "solid-color",
      hex_color: "#0F172A",
    },
    {
      index: 1,
      type: "text",
      text: "Your Headline Goes Here",
      font_name: "Inter",
      font_size_in_px: 52,
      text_color: "#FFFFFF",
      font_weight: "bold",
      position: { x_in_px: 80, y_in_px: 80 },
      dimensions: { width_in_px: 800, height_in_px: 140 },
    },
    {
      index: 2,
      type: "text",
      text: "A short subtitle that explains the value proposition in one line.",
      font_name: "Inter",
      font_size_in_px: 22,
      text_color: "#94A3B8",
      position: { x_in_px: 80, y_in_px: 240 },
      dimensions: { width_in_px: 900, height_in_px: 40 },
    },
    {
      index: 3,
      type: "layout",
      direction: "horizontal",
      gap: 12,
      position: { x_in_px: 80, y_in_px: 320 },
      layers: [pill("Feature One"), pill("Feature Two"), pill("Feature Three")],
    },
    {
      index: 4,
      type: "layout",
      direction: "vertical",
      gap: 14,
      position: { x_in_px: 80, y_in_px: 420 },
      layers: [
        listItem("Benefit number one"),
        listItem("Benefit number two"),
        listItem("Benefit number three"),
      ],
    },
    {
      index: 5,
      type: "layout",
      direction: "horizontal",
      vertical_alignment: "center",
      background_color: "#3B82F6",
      padding: 14,
      border_radius: 24,
      position: { x_in_px: 80, y_in_px: 600 },
      layers: [
        {
          type: "text",
          text: "Call to action",
          font_name: "Inter",
          font_size_in_px: 16,
          font_weight: "bold",
          text_color: "#FFFFFF",
          dimensions: { width_in_px: "auto", height_in_px: 22 },
        },
      ],
    },
  ],
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

def pill(label):
    return {
        "type": "layout",
        "direction": "horizontal",
        "background_color": "#1E293B",
        "padding": 10,
        "border_radius": 20,
        "layers": [
            {
                "type": "text",
                "text": label,
                "font_name": "Inter",
                "font_size_in_px": 14,
                "text_color": "#94A3B8",
                "dimensions": {"width_in_px": "auto", "height_in_px": 20},
            },
        ],
    }

def list_item(label):
    return {
        "type": "text",
        "text": label,
        "font_name": "Inter",
        "font_size_in_px": 20,
        "text_color": "#E2E8F0",
        "dimensions": {"width_in_px": "auto", "height_in_px": 28},
    }

result = client.generate_image(
    dimensions={"width_in_px": 1200, "height_in_px": 675},
    output_format="png",
    layers=[
        {
            "index": 0,
            "type": "solid-color",
            "hex_color": "#0F172A",
        },
        {
            "index": 1,
            "type": "text",
            "text": "Your Headline Goes Here",
            "font_name": "Inter",
            "font_size_in_px": 52,
            "text_color": "#FFFFFF",
            "font_weight": "bold",
            "position": {"x_in_px": 80, "y_in_px": 80},
            "dimensions": {"width_in_px": 800, "height_in_px": 140},
        },
        {
            "index": 2,
            "type": "text",
            "text": "A short subtitle that explains the value proposition in one line.",
            "font_name": "Inter",
            "font_size_in_px": 22,
            "text_color": "#94A3B8",
            "position": {"x_in_px": 80, "y_in_px": 240},
            "dimensions": {"width_in_px": 900, "height_in_px": 40},
        },
        {
            "index": 3,
            "type": "layout",
            "direction": "horizontal",
            "gap": 12,
            "position": {"x_in_px": 80, "y_in_px": 320},
            "layers": [
                pill("Feature One"),
                pill("Feature Two"),
                pill("Feature Three"),
            ],
        },
        {
            "index": 4,
            "type": "layout",
            "direction": "vertical",
            "gap": 14,
            "position": {"x_in_px": 80, "y_in_px": 420},
            "layers": [
                list_item("Benefit number one"),
                list_item("Benefit number two"),
                list_item("Benefit number three"),
            ],
        },
        {
            "index": 5,
            "type": "layout",
            "direction": "horizontal",
            "vertical_alignment": "center",
            "background_color": "#3B82F6",
            "padding": 14,
            "border_radius": 24,
            "position": {"x_in_px": 80, "y_in_px": 600},
            "layers": [
                {
                    "type": "text",
                    "text": "Call to action",
                    "font_name": "Inter",
                    "font_size_in_px": 16,
                    "font_weight": "bold",
                    "text_color": "#FFFFFF",
                    "dimensions": {
                        "width_in_px": "auto",
                        "height_in_px": 22,
                    },
                },
            ],
        },
    ],
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func pill(label string) il.LayoutLayer {
	padding := 10
	radius := 20
	return il.LayoutLayer{
		Type:            "layout",
		Direction:       "horizontal",
		BackgroundColor: "#1E293B",
		Padding:         &padding,
		BorderRadius:    &radius,
		Layers: []il.Layer{
			il.TextLayer{
				Type: "text", Text: label, FontName: "Inter",
				FontSizeInPx: 14, TextColor: "#94A3B8",
				Dimensions: &il.Dimensions{HeightInPx: 20},
			},
		},
	}
}

func listItem(label string) il.TextLayer {
	return il.TextLayer{
		Type: "text", Text: label, FontName: "Inter",
		FontSizeInPx: 20, TextColor: "#E2E8F0",
		Dimensions: &il.Dimensions{HeightInPx: 28},
	}
}

func main() {
	client := il.NewClient("YOUR_API_KEY")

	gap12 := 12
	gap14 := 14
	padding14 := 14
	radius24 := 24

	result, err := client.GenerateImage(
		il.GenerateImageRequest{
			Dimensions:   il.Dimensions{WidthInPx: 1200, HeightInPx: 675},
			OutputFormat: "png",
			Layers: []il.Layer{
				il.NewSolidColorBackgroundLayer(0, "#0F172A"),
				il.TextLayer{
					Type: "text", Index: 1,
					Text: "Your Headline Goes Here", FontName: "Inter",
					FontSizeInPx: 52, TextColor: "#FFFFFF", FontWeight: "bold",
					Position:   &il.Position{XInPx: 80, YInPx: 80},
					Dimensions: &il.Dimensions{WidthInPx: 800, HeightInPx: 140},
				},
				il.TextLayer{
					Type: "text", Index: 2,
					Text: "A short subtitle that explains the value proposition in one line.",
					FontName: "Inter", FontSizeInPx: 22, TextColor: "#94A3B8",
					Position:   &il.Position{XInPx: 80, YInPx: 240},
					Dimensions: &il.Dimensions{WidthInPx: 900, HeightInPx: 40},
				},
				il.LayoutLayer{
					Type: "layout", Index: 3, Direction: "horizontal",
					Gap: &gap12, Position: &il.Position{XInPx: 80, YInPx: 320},
					Layers: []il.Layer{
						pill("Feature One"),
						pill("Feature Two"),
						pill("Feature Three"),
					},
				},
				il.LayoutLayer{
					Type: "layout", Index: 4, Direction: "vertical",
					Gap: &gap14, Position: &il.Position{XInPx: 80, YInPx: 420},
					Layers: []il.Layer{
						listItem("Benefit number one"),
						listItem("Benefit number two"),
						listItem("Benefit number three"),
					},
				},
				il.LayoutLayer{
					Type: "layout", Index: 5, Direction: "horizontal",
					VerticalAlignment: "center", BackgroundColor: "#3B82F6",
					Padding: &padding14, BorderRadius: &radius24,
					Position: &il.Position{XInPx: 80, YInPx: 600},
					Layers: []il.Layer{
						il.TextLayer{
							Type: "text", Text: "Call to action", FontName: "Inter",
							FontSizeInPx: 16, FontWeight: "bold", TextColor: "#FFFFFF",
							Dimensions: &il.Dimensions{HeightInPx: 22},
						},
					},
				},
			},
		},
	)
	if err != nil {
		panic(err)
	}
	_ = result
}
```

```n8n
{
  "name": "Generate Product Slide",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate Product Slide\n\nMarketing teams and SaaS companies use this recipe to generate branded slides at scale \u2014 for pitch decks, product launches, or social media carousels. Use layout layers to arrange headlines, feature pills, and CTAs without manual pixel positioning. Swap in your brand colors, logo, and copy to produce consistent slides across campaigns.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
        "height_in_px": 280,
        "width_in_px": 500,
        "color": 2
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        200,
        40
      ],
      "id": "63adbc8c-3924-45ce-ae88-68cd0629a88e",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Image\nResource: **Image Generation**\n\nConfigure the Image Generation parameters below, then connect your credentials.",
        "height_in_px": 160,
        "width_in_px": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        475,
        100
      ],
      "id": "0fe2b118-4443-47f6-a2fe-00588d5d9c7b",
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
      "id": "c9d0e1f2-9999-4000-8000-000000000001",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "imageGeneration",
        "widthInPx": 1200,
        "heightInPx": 675,
        "outputFormat": "png",
        "layersJson": "[{\"index\":0,\"type\":\"solid-color\",\"hex_color\":\"#0F172A\"},{\"index\":1,\"type\":\"text\",\"text\":\"Your Headline Goes Here\",\"font_name\":\"Inter\",\"font_size_in_px\":52,\"text_color\":\"#FFFFFF\",\"font_weight\":\"bold\",\"position\":{\"x\":80.0,\"y\":80.0},\"dimensions\":{\"width\":800,\"height\":140}},{\"index\":2,\"type\":\"text\",\"text\":\"A short subtitle that explains the value proposition in one line.\",\"font_name\":\"Inter\",\"font_size_in_px\":22,\"text_color\":\"#94A3B8\",\"position\":{\"x\":80.0,\"y\":240.0},\"dimensions\":{\"width\":900,\"height\":40}},{\"index\":3,\"type\":\"layout\",\"direction\":\"horizontal\",\"gap\":12,\"position\":{\"x\":80.0,\"y\":320.0},\"layers\":[{\"type\":\"layout\",\"direction\":\"horizontal\",\"background_color\":\"#1E293B\",\"padding\":10,\"border_radius\":20,\"layers\":[{\"type\":\"text\",\"text\":\"Feature One\",\"font_name\":\"Inter\",\"font_size_in_px\":14,\"text_color\":\"#94A3B8\",\"dimensions\":{\"width\":\"auto\",\"height\":20}}]},{\"type\":\"layout\",\"direction\":\"horizontal\",\"background_color\":\"#1E293B\",\"padding\":10,\"border_radius\":20,\"layers\":[{\"type\":\"text\",\"text\":\"Feature Two\",\"font_name\":\"Inter\",\"font_size_in_px\":14,\"text_color\":\"#94A3B8\",\"dimensions\":{\"width\":\"auto\",\"height\":20}}]},{\"type\":\"layout\",\"direction\":\"horizontal\",\"background_color\":\"#1E293B\",\"padding\":10,\"border_radius\":20,\"layers\":[{\"type\":\"text\",\"text\":\"Feature Three\",\"font_name\":\"Inter\",\"font_size_in_px\":14,\"text_color\":\"#94A3B8\",\"dimensions\":{\"width\":\"auto\",\"height\":20}}]}]},{\"index\":4,\"type\":\"layout\",\"direction\":\"vertical\",\"gap\":14,\"position\":{\"x\":80.0,\"y\":420.0},\"layers\":[{\"type\":\"text\",\"text\":\"Benefit number one\",\"font_name\":\"Inter\",\"font_size_in_px\":20,\"text_color\":\"#E2E8F0\",\"dimensions\":{\"width\":\"auto\",\"height\":28}},{\"type\":\"text\",\"text\":\"Benefit number two\",\"font_name\":\"Inter\",\"font_size_in_px\":20,\"text_color\":\"#E2E8F0\",\"dimensions\":{\"width\":\"auto\",\"height\":28}},{\"type\":\"text\",\"text\":\"Benefit number three\",\"font_name\":\"Inter\",\"font_size_in_px\":20,\"text_color\":\"#E2E8F0\",\"dimensions\":{\"width\":\"auto\",\"height\":28}}]},{\"index\":5,\"type\":\"layout\",\"direction\":\"horizontal\",\"vertical_alignment\":\"center\",\"background_color\":\"#3B82F6\",\"padding\":14,\"border_radius\":24,\"position\":{\"x\":80.0,\"y\":600.0},\"layers\":[{\"type\":\"text\",\"text\":\"Call to action\",\"font_name\":\"Inter\",\"font_size_in_px\":16,\"font_weight\":\"bold\",\"text_color\":\"#FFFFFF\",\"dimensions\":{\"width\":\"auto\",\"height\":22}}]}]",
        "fontsJson": "[]"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "c9d0e1f2-9999-4000-8000-000000000002",
      "name": "Generate Image",
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
            "node": "Generate Image",
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
Generate a branded product slide image at 1920x1080 pixels. Use the generate_image tool with layout layers:

1. Background: gradient layer with [brand colors]
2. Headline: text layer with [headline text] in large bold font
3. Feature pills: solid-color rectangles with feature text overlays for each of [feature 1], [feature 2], [feature 3]
4. CTA button: solid-color rectangle with [CTA text] overlay
5. Logo: image layer with [logo URL] positioned in corner
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/png"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
