---
name: generate-pdf-manuscript
description: Generate a print-ready PDF manuscript with title page, table of contents, and chapters at 6x9 inch trim size.
---

# Generate PDF Manuscript

Self-publishing authors and publishing platforms use this recipe to generate a print-ready PDF manuscript for KDP or IngramSpark. Define a 6x9 inch page with proper margins, title page, table of contents, and chapter content — ready for print-on-demand submission.

## APIs Used

Document Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/document-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "document": {
      "metadata": {
        "title": "The Long Silence",
        "author": "Elizabeth Ashworth"
      },
      "page": {
        "size": {
          "width_in_pt": 432,
          "height_in_pt": 648
        },
        "margins": {
          "top_in_pt": 72,
          "right_in_pt": 63,
          "bottom_in_pt": 72,
          "left_in_pt": 81
        }
      },
      "styles": {
        "text": {
          "font_family": "Lora",
          "font_size_in_pt": 11.0,
          "line_height": 1.6,
          "color": "#1A1A1A"
        },
        "headline": {
          "font_family": "PlayfairDisplay",
          "font_size_in_pt": 28.0,
          "color": "#111111",
          "spacing_before_in_pt": 24.0,
          "spacing_after_in_pt": 12.0,
          "font_weight": "bold"
        },
        "link": {
          "color": "#0066CC",
          "is_underlined": true
        },
        "list": {
          "text_style": {
            "font_family": "Lora",
            "font_size_in_pt": 11.0,
            "line_height": 1.6,
            "color": "#1A1A1A"
          },
          "marker_color": "#1A1A1A",
          "marker_gap_in_pt": 8.0
        },
        "table": {
          "header": {
            "background_color": "#333333",
            "text_color": "#FFFFFF",
            "font_size_in_pt": 11.0,
            "font_weight": "bold"
          },
          "body": {
            "background_color": "#FFFFFF",
            "text_color": "#333333",
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
          "thickness_in_pt": 0.5,
          "spacing_before_in_pt": 24.0,
          "spacing_after_in_pt": 24.0
        },
        "image": {
          "border_color": "#000000",
          "border_width_in_pt": 0.0
        }
      },
      "footer": [
        {
          "type": "paragraph",
          "runs": [{
            "text": "— {{page_number}} —"
          }]
        }
      ],
      "content": [
        {
            "type": "headline",
            "level": "h1",
            "text": "The Long Silence",
        },
        { "type": "paragraph", "markdown": " " },
        { "type": "paragraph", "markdown": " " },
        { "type": "paragraph", "markdown": " " },
        { "type": "paragraph", "runs": [
          {
              "text": "Elizabeth Ashworth",
              "font_weight": "bold",
          }
        ] },
        { "type": "paragraph", "markdown": " " },
        { "type": "paragraph", "markdown": " " },
        { "type": "paragraph", "runs": [
          {
              "text": "The Ashworth Chronicles,
              Book 1",
              "is_italic": true,
          }
        ] },
        { "type": "separator" },
        { "type": "paragraph", "runs": [{ "text": "Copyright \u00a9 2026 Elizabeth Ashworth. All rights reserved." }] },
        { "type": "paragraph", "runs": [{ "text": "ISBN: 978-1-234567-89-0" }] },
        { "type": "page-break" },
        {
            "type": "table-of-contents",
            "levels": ["h1"],
            "leader": "dots",
        },
        { "type": "page-break" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Chapter 1: The Letter",
        },
        {
            "type": "paragraph",
            "markdown": "The envelope arrived on a Tuesday,
            which Eleanor would later consider the cruelest part. Tuesdays were supposed to be ordinary. Tuesdays were for faculty meetings and grading papers and reheating last night's soup. Tuesdays were not for letters that smelled faintly of cedar and bore a postmark from a town she had spent thirty years trying to forget.",
        },
        {
            "type": "paragraph",
            "markdown": "She held it at arm's length,
            as though it might detonate. The handwriting was unmistakable — the same looping cursive that had filled the margins of her college notebooks,
            the same hand that had signed the divorce papers without a single correction. Thomas. After all this time.",
        },
        {
            "type": "paragraph",
            "markdown": "The kitchen clock ticked. Outside,
            a cardinal landed on the feeder and regarded her through the window with what she could only describe as judgment. She set the letter on the counter,
            poured herself a cup of coffee she no longer wanted,
            and sat down to read.",
        },
        {
            "type": "paragraph",
            "markdown": "*Dear Eleanor,
            *",
        },
        {
            "type": "paragraph",
            "markdown": "*I know you have every reason to throw this away unread. I am writing anyway because there are things I should have told you decades ago,
            and I have recently learned that time is shorter than I assumed. The house on Meridian Street — you remember the one — still stands. I have left something there for you. Whether you retrieve it is your choice. But I think you will want to know the truth about what happened the night Daniel disappeared.*",
        },
        {
            "type": "paragraph",
            "markdown": "Eleanor read the letter three times. Then she folded it precisely along its original creases,
            placed it back in the envelope,
            and set it on the shelf beside the cookbooks where she kept things she intended to deal with later but never did.",
        },
        {
            "type": "paragraph",
            "markdown": "She lasted four hours.",
        },
        { "type": "page-break" },
        {
            "type": "headline",
            "level": "h1",
            "text": "Chapter 2: Meridian Street",
        },
        {
            "type": "paragraph",
            "markdown": "The drive from campus to Millhaven took three hours if you obeyed the speed limit,
            which Eleanor always did,
            even now,
            even with her hands white-knuckled on the steering wheel and her mind racing through every possible explanation for why Thomas Ashworth had chosen this particular moment to break three decades of silence.",
        },
        {
            "type": "paragraph",
            "markdown": "Millhaven looked smaller than she remembered. The main street had lost its hardware store and gained a coffee shop with a chalkboard menu. The library had a new wing. The gas station where she and Thomas used to buy cherry slushies on summer afternoons had become a pharmacy.",
        },
        {
            "type": "paragraph",
            "markdown": "She turned onto Meridian Street and felt her stomach drop. The house was exactly as she remembered — a two-story Victorian with peeling blue paint and a wraparound porch that sagged in the middle like a held breath. The oak tree in the front yard had doubled in size. Everything else was frozen.",
        },
        {
            "type": "paragraph",
            "markdown": "The front door was unlocked. Inside,
            the air was thick with dust and something else — the faint,
            sweet smell of old paper. Sheets covered the furniture like ghosts standing guard. Eleanor pulled one back and found the leather armchair where Thomas's father used to sit reading the evening paper,
            a glass of bourbon balanced on the armrest.",
        },
        {
            "type": "paragraph",
            "markdown": "On the mantel above the fireplace,
            propped against a stopped clock,
            was a second envelope. This one was thicker. She opened it and found a photograph she had never seen before — Daniel,
            Thomas,
            and a third person she did not recognize,
            standing in front of this very house. On the back,
            in Thomas's handwriting: *August 1994. The last good day.*",
        },
        {
            "type": "paragraph",
            "markdown": "Below the photograph was a key. Small,
            brass,
            unremarkable. And a note in Thomas's hand: *The basement. You always were the braver one.*",
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.generateDocument({
  format: "pdf",
  document: {
    metadata: {
      title: "The Long Silence",
      author: "Elizabeth Ashworth",
    },
    page: {
      size: {
        width_in_pt: 432,
        height_in_pt: 648,
      },
      margins: {
        top_in_pt: 72,
        right_in_pt: 63,
        bottom_in_pt: 72,
        left_in_pt: 81,
      },
    },
    styles: {
      text: {
        font_family: "Lora",
        font_size_in_pt: 11.0,
        line_height: 1.6,
        color: "#1A1A1A",
      },
      headline: {
        font_family: "PlayfairDisplay",
        font_size_in_pt: 28.0,
        color: "#111111",
        spacing_before_in_pt: 24.0,
        spacing_after_in_pt: 12.0,
        font_weight: "bold",
      },
      link: {
        color: "#0066CC",
        is_underlined: true,
      },
      list: {
        text_style: {
          font_family: "Lora",
          font_size_in_pt: 11.0,
          line_height: 1.6,
          color: "#1A1A1A",
        },
        marker_color: "#1A1A1A",
        marker_gap_in_pt: 8.0,
      },
      table: {
        header: {
          background_color: "#333333",
          text_color: "#FFFFFF",
          font_size_in_pt: 11.0,
          font_weight: "bold",
        },
        body: {
          background_color: "#FFFFFF",
          text_color: "#333333",
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
        thickness_in_pt: 0.5,
        spacing_before_in_pt: 24.0,
        spacing_after_in_pt: 24.0,
      },
      image: {
        border_color: "#000000",
        border_width_in_pt: 0.0,
      },
    },
    footer: [
      {
        type: "paragraph",
        runs: [{
          text: "— {{page_number}} —",
        }],
      },
    ],
    content: [
      {
          type: "headline",
          level: "h1",
          text: "The Long Silence",
      },
      { type: "paragraph", markdown: " " },
      { type: "paragraph", markdown: " " },
      { type: "paragraph", markdown: " " },
      { type: "paragraph", runs: [
        {
            text: "Elizabeth Ashworth",
            font_weight: "bold",
        },
      ] },
      { type: "paragraph", markdown: " " },
      { type: "paragraph", markdown: " " },
      { type: "paragraph", runs: [
        {
            text: "The Ashworth Chronicles,
            Book 1",
            is_italic: true,
        },
      ] },
      { type: "separator" },
      { type: "paragraph", runs: [{ text: "Copyright \u00a9 2026 Elizabeth Ashworth. All rights reserved." }] },
      { type: "paragraph", runs: [{ text: "ISBN: 978-1-234567-89-0" }] },
      { type: "page-break" },
      {
          type: "table-of-contents",
          levels: ["h1"],
          leader: "dots",
      },
      { type: "page-break" },
      {
          type: "headline",
          level: "h1",
          text: "Chapter 1: The Letter",
      },
      {
          type: "paragraph",
          markdown: "The envelope arrived on a Tuesday,
          which Eleanor would later consider the cruelest part. Tuesdays were supposed to be ordinary. Tuesdays were for faculty meetings and grading papers and reheating last night's soup. Tuesdays were not for letters that smelled faintly of cedar and bore a postmark from a town she had spent thirty years trying to forget.",
      },
      {
          type: "paragraph",
          markdown: "She held it at arm's length,
          as though it might detonate. The handwriting was unmistakable — the same looping cursive that had filled the margins of her college notebooks,
          the same hand that had signed the divorce papers without a single correction. Thomas. After all this time.",
      },
      {
          type: "paragraph",
          markdown: "The kitchen clock ticked. Outside,
          a cardinal landed on the feeder and regarded her through the window with what she could only describe as judgment. She set the letter on the counter,
          poured herself a cup of coffee she no longer wanted,
          and sat down to read.",
      },
      {
          type: "paragraph",
          markdown: "*Dear Eleanor,
          *",
      },
      {
          type: "paragraph",
          markdown: "*I know you have every reason to throw this away unread. I am writing anyway because there are things I should have told you decades ago,
          and I have recently learned that time is shorter than I assumed. The house on Meridian Street — you remember the one — still stands. I have left something there for you. Whether you retrieve it is your choice. But I think you will want to know the truth about what happened the night Daniel disappeared.*",
      },
      {
          type: "paragraph",
          markdown: "Eleanor read the letter three times. Then she folded it precisely along its original creases,
          placed it back in the envelope,
          and set it on the shelf beside the cookbooks where she kept things she intended to deal with later but never did.",
      },
      {
          type: "paragraph",
          markdown: "She lasted four hours.",
      },
      { type: "page-break" },
      {
          type: "headline",
          level: "h1",
          text: "Chapter 2: Meridian Street",
      },
      {
          type: "paragraph",
          markdown: "The drive from campus to Millhaven took three hours if you obeyed the speed limit,
          which Eleanor always did,
          even now,
          even with her hands white-knuckled on the steering wheel and her mind racing through every possible explanation for why Thomas Ashworth had chosen this particular moment to break three decades of silence.",
      },
      {
          type: "paragraph",
          markdown: "Millhaven looked smaller than she remembered. The main street had lost its hardware store and gained a coffee shop with a chalkboard menu. The library had a new wing. The gas station where she and Thomas used to buy cherry slushies on summer afternoons had become a pharmacy.",
      },
      {
          type: "paragraph",
          markdown: "She turned onto Meridian Street and felt her stomach drop. The house was exactly as she remembered — a two-story Victorian with peeling blue paint and a wraparound porch that sagged in the middle like a held breath. The oak tree in the front yard had doubled in size. Everything else was frozen.",
      },
      {
          type: "paragraph",
          markdown: "The front door was unlocked. Inside,
          the air was thick with dust and something else — the faint,
          sweet smell of old paper. Sheets covered the furniture like ghosts standing guard. Eleanor pulled one back and found the leather armchair where Thomas's father used to sit reading the evening paper,
          a glass of bourbon balanced on the armrest.",
      },
      {
          type: "paragraph",
          markdown: "On the mantel above the fireplace,
          propped against a stopped clock,
          was a second envelope. This one was thicker. She opened it and found a photograph she had never seen before — Daniel,
          Thomas,
          and a third person she did not recognize,
          standing in front of this very house. On the back,
          in Thomas's handwriting: *August 1994. The last good day.*",
      },
      {
          type: "paragraph",
          markdown: "Below the photograph was a key. Small,
          brass,
          unremarkable. And a note in Thomas's hand: *The basement. You always were the braver one.*",
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
            "title": "The Long Silence",
            "author": "Elizabeth Ashworth",
        },
        "page": {
            "size": {
                "width_in_pt": 432,
                "height_in_pt": 648,
            },
            "margins": {
                "top_in_pt": 72,
                "right_in_pt": 63,
                "bottom_in_pt": 72,
                "left_in_pt": 81,
            },
        },
        "styles": {
            "text": {
                "font_family": "Lora",
                "font_size_in_pt": 11.0,
                "line_height": 1.6,
                "color": "#1A1A1A",
            },
            "headline": {
                "font_family": "PlayfairDisplay",
                "font_size_in_pt": 28.0,
                "color": "#111111",
                "spacing_before_in_pt": 24.0,
                "spacing_after_in_pt": 12.0,
                "font_weight": "bold",
            },
            "link": {
                "color": "#0066CC",
                "is_underlined": True,
            },
            "list": {
                "text_style": {
                    "font_family": "Lora",
                    "font_size_in_pt": 11.0,
                    "line_height": 1.6,
                    "color": "#1A1A1A",
                },
                "marker_color": "#1A1A1A",
                "marker_gap_in_pt": 8.0,
            },
            "table": {
                "header": {
                    "background_color": "#333333",
                    "text_color": "#FFFFFF",
                    "font_size_in_pt": 11.0,
                    "font_weight": "bold",
                },
                "body": {
                    "background_color": "#FFFFFF",
                    "text_color": "#333333",
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
                "thickness_in_pt": 0.5,
                "spacing_before_in_pt": 24.0,
                "spacing_after_in_pt": 24.0,
            },
            "image": {
                "border_color": "#000000",
                "border_width_in_pt": 0.0,
            },
        },
        "footer": [
            {
                "type": "paragraph",
                "runs": [{
                    "text": "\u2014 {{page_number}} \u2014",
                }],
            },
        ],
        "content": [
            {
                "type": "headline",
                "level": "h1",
                "text": "The Long Silence",
            },
            {"type": "paragraph", "markdown": " "},
            {"type": "paragraph", "markdown": " "},
            {"type": "paragraph", "markdown": " "},
            {"type": "paragraph", "runs": [
                {
                    "text": "Elizabeth Ashworth",
                    "font_weight": "bold",
                },
            ]},
            {"type": "paragraph", "markdown": " "},
            {"type": "paragraph", "markdown": " "},
            {"type": "paragraph", "runs": [
                {
                    "text": "The Ashworth Chronicles,
                    Book 1",
                    "is_italic": True,
                },
            ]},
            {"type": "separator"},
            {"type": "paragraph", "runs": [{"text": "Copyright \u00a9 2026 Elizabeth Ashworth. All rights reserved."}]},
            {"type": "paragraph", "runs": [{"text": "ISBN: 978-1-234567-89-0"}]},
            {"type": "page-break"},
            {
                "type": "table-of-contents",
                "levels": ["h1"],
                "leader": "dots",
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Chapter 1: The Letter",
            },
            {
                "type": "paragraph",
                "markdown": "The envelope arrived on a Tuesday,
                which Eleanor would later consider the cruelest part. Tuesdays were supposed to be ordinary. Tuesdays were for faculty meetings and grading papers and reheating last night\u2019s soup. Tuesdays were not for letters that smelled faintly of cedar and bore a postmark from a town she had spent thirty years trying to forget.",
            },
            {
                "type": "paragraph",
                "markdown": "She held it at arm\u2019s length,
                as though it might detonate. The handwriting was unmistakable \u2014 the same looping cursive that had filled the margins of her college notebooks,
                the same hand that had signed the divorce papers without a single correction. Thomas. After all this time.",
            },
            {
                "type": "paragraph",
                "markdown": "The kitchen clock ticked. Outside,
                a cardinal landed on the feeder and regarded her through the window with what she could only describe as judgment. She set the letter on the counter,
                poured herself a cup of coffee she no longer wanted,
                and sat down to read.",
            },
            {
                "type": "paragraph",
                "markdown": "*Dear Eleanor,
                *",
            },
            {
                "type": "paragraph",
                "markdown": "*I know you have every reason to throw this away unread. I am writing anyway because there are things I should have told you decades ago,
                and I have recently learned that time is shorter than I assumed. The house on Meridian Street \u2014 you remember the one \u2014 still stands. I have left something there for you. Whether you retrieve it is your choice. But I think you will want to know the truth about what happened the night Daniel disappeared.*",
            },
            {
                "type": "paragraph",
                "markdown": "Eleanor read the letter three times. Then she folded it precisely along its original creases,
                placed it back in the envelope,
                and set it on the shelf beside the cookbooks where she kept things she intended to deal with later but never did.",
            },
            {
                "type": "paragraph",
                "markdown": "She lasted four hours.",
            },
            {"type": "page-break"},
            {
                "type": "headline",
                "level": "h1",
                "text": "Chapter 2: Meridian Street",
            },
            {
                "type": "paragraph",
                "markdown": "The drive from campus to Millhaven took three hours if you obeyed the speed limit,
                which Eleanor always did,
                even now,
                even with her hands white-knuckled on the steering wheel and her mind racing through every possible explanation for why Thomas Ashworth had chosen this particular moment to break three decades of silence.",
            },
            {
                "type": "paragraph",
                "markdown": "Millhaven looked smaller than she remembered. The main street had lost its hardware store and gained a coffee shop with a chalkboard menu. The library had a new wing. The gas station where she and Thomas used to buy cherry slushies on summer afternoons had become a pharmacy.",
            },
            {
                "type": "paragraph",
                "markdown": "She turned onto Meridian Street and felt her stomach drop. The house was exactly as she remembered \u2014 a two-story Victorian with peeling blue paint and a wraparound porch that sagged in the middle like a held breath. The oak tree in the front yard had doubled in size. Everything else was frozen.",
            },
            {
                "type": "paragraph",
                "markdown": "The front door was unlocked. Inside,
                the air was thick with dust and something else \u2014 the faint,
                sweet smell of old paper. Sheets covered the furniture like ghosts standing guard. Eleanor pulled one back and found the leather armchair where Thomas\u2019s father used to sit reading the evening paper,
                a glass of bourbon balanced on the armrest.",
            },
            {
                "type": "paragraph",
                "markdown": "On the mantel above the fireplace,
                propped against a stopped clock,
                was a second envelope. This one was thicker. She opened it and found a photograph she had never seen before \u2014 Daniel,
                Thomas,
                and a third person she did not recognize,
                standing in front of this very house. On the back,
                in Thomas\u2019s handwriting: *August 1994. The last good day.*",
            },
            {
                "type": "paragraph",
                "markdown": "Below the photograph was a key. Small,
                brass,
                unremarkable. And a note in Thomas\u2019s hand: *The basement. You always were the braver one.*",
            },
        ],
    },
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.GenerateDocument(il.GenerateDocumentRequest{
		Format: "pdf",
		Document: il.DocumentDefinition{
			Metadata: il.DocumentMetadata{
				Title:  "The Long Silence",
				Author: "Elizabeth Ashworth",
			},
			Page: il.PageConfig{
				Size: il.PageSize{Custom: &il.CustomPageSize{
					WidthInPt:  432,
					HeightInPt: 648,
				}},
				Margins: il.Margins{
					TopInPt:    72,
					RightInPt:  63,
					BottomInPt: 72,
					LeftInPt:   81,
				},
			},
			Content: []il.ContentBlock{
				il.NewHeadlineBlock("h1", "The Long Silence"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "**Elizabeth Ashworth**",
    },
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "*The Ashworth Chronicles,
      Book 1*",
    },
				il.NewSeparatorBlock(),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "Copyright \u00a9 2026 Elizabeth Ashworth. All rights reserved.\n\nISBN: 978-1-234567-89-0",
    },
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Chapter 1: The Letter"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "The envelope arrived on a Tuesday,
      which Eleanor would later consider the cruelest part. Tuesdays were supposed to be ordinary...",
    },
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "She held it at arm's length,
      as though it might detonate. The handwriting was unmistakable...",
    },
				il.NewPageBreakBlock(),
				il.NewHeadlineBlock("h1", "Chapter 2: Meridian Street"),
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "The drive from campus to Millhaven took three hours if you obeyed the speed limit...",
    },
				il.ParagraphBlock{
      Type: "paragraph",
      Markdown: "She turned onto Meridian Street and felt her stomach drop. The house was exactly as she remembered...",
    },
			},
		},
	})
	if err != nil {
		panic(err)
	}

}
```

```n8n
{
  "name": "Generate PDF Manuscript",
  "nodes": [
    {
      "parameters": {
        "content": "## Generate PDF Manuscript\n\nSelf-publishing authors and publishing platforms use this recipe to generate a print-ready PDF manuscript for KDP or IngramSpark. Define a 6x9 inch page with proper margins, title page, table of contents, and chapter content \u2014 ready for print-on-demand submission.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "4b4b6bb3-597f-4207-891c-d044984c8b49",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Generate Document\nResource: **Document Generation**\n\nConfigure the Document Generation parameters below, then connect your credentials.",
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
      "id": "88006298-54d7-411c-8c81-717e10831111",
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
      "id": "a3371f41-b72c-4764-bc2a-d962c2019b90",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"metadata\": {\n    \"title\": \"The Long Silence\",\n    \"author\": \"Elizabeth Ashworth\"\n  },\n  \"page\": {\n    \"size\": {\n      \"custom\": {\n        \"width_in_pt\": 432,\n        \"height_in_pt\": 648\n      }\n    },\n    \"margins\": {\n      \"top_in_pt\": 72,\n      \"right_in_pt\": 63,\n      \"bottom_in_pt\": 72,\n      \"left_in_pt\": 81\n    }\n  },\n  \"styles\": {\n    \"text\": {\n      \"font_family\": \"Lora\",\n      \"font_size_in_pt\": 11.0,\n      \"line_height\": 1.6,\n      \"color\": \"#1A1A1A\"\n    },\n    \"headline\": {\n      \"font_family\": \"PlayfairDisplay\",\n      \"font_size_in_pt\": 28.0,\n      \"color\": \"#111111\",\n      \"spacing_before_in_pt\": 24.0,\n      \"spacing_after_in_pt\": 12.0,\n      \"font_weight\": \"bold\"\n    },\n    \"link\": {\n      \"color\": \"#0066CC\",\n      \"is_underlined\": true\n    },\n    \"list\": {\n      \"text_style\": {\n        \"font_family\": \"Lora\",\n        \"font_size_in_pt\": 11.0,\n        \"line_height\": 1.6,\n        \"color\": \"#1A1A1A\"\n      },\n      \"marker_color\": \"#1A1A1A\",\n      \"marker_gap_in_pt\": 8.0\n    },\n    \"table\": {\n      \"header\": {\n        \"background_color\": \"#333333\",\n        \"text_color\": \"#FFFFFF\",\n        \"font_size_in_pt\": 11.0,\n        \"font_weight\": \"bold\"\n      },\n      \"body\": {\n        \"background_color\": \"#FFFFFF\",\n        \"text_color\": \"#333333\",\n        \"font_size_in_pt\": 11.0\n      },\n      \"border\": {\n        \"outer\": {\n          \"top\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"right\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"bottom\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          },\n          \"left\": {\n            \"color\": \"#CCCCCC\",\n            \"width_in_pt\": 1.0\n          }\n        },\n        \"inner\": {\n          \"horizontal\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          },\n          \"vertical\": {\n            \"color\": \"#EEEEEE\",\n            \"width_in_pt\": 0.5\n          }\n        }\n      }\n    },\n    \"grid\": {\n      \"background_color\": \"#FFFFFF\",\n      \"border_color\": \"#CCCCCC\",\n      \"border_width_in_pt\": 0.0,\n      \"gap_in_pt\": 12.0\n    },\n    \"separator\": {\n      \"color\": \"#CCCCCC\",\n      \"thickness_in_pt\": 0.5,\n      \"spacing_before_in_pt\": 24.0,\n      \"spacing_after_in_pt\": 24.0\n    },\n    \"image\": {\n      \"border_color\": \"#000000\",\n      \"border_width_in_pt\": 0.0\n    }\n  },\n  \"footer\": [\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"\\u2014 {{page_number}} \\u2014\"\n        }\n      ]\n    }\n  ],\n  \"content\": [\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"The Long Silence\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"markdown\": \" \"\n        }\n      ]\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Elizabeth Ashworth\",\n          \"font_weight\": \"bold\"\n        }\n      ]\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"markdown\": \" \"\n        }\n      ]\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"The Ashworth Chronicles,\\n              Book 1\",\n          \"is_italic\": true\n        }\n      ]\n    },\n    {\n      \"type\": \"separator\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"Copyright \\u00a9 2026 Elizabeth Ashworth. All rights reserved.\"\n        }\n      ]\n    },\n    {\n      \"type\": \"paragraph\",\n      \"runs\": [\n        {\n          \"text\": \"ISBN: 978-1-234567-89-0\"\n        }\n      ]\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"table-of-contents\",\n      \"levels\": [\n        \"h1\"\n      ],\n      \"leader\": \"dots\"\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Chapter 1: The Letter\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"The envelope arrived on a Tuesday,\\n            which Eleanor would later consider the cruelest part. Tuesdays were supposed to be ordinary. Tuesdays were for faculty meetings and grading papers and reheating last night's soup. Tuesdays were not for letters that smelled faintly of cedar and bore a postmark from a town she had spent thirty years trying to forget.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"She held it at arm's length,\\n            as though it might detonate. The handwriting was unmistakable \\u2014 the same looping cursive that had filled the margins of her college notebooks,\\n            the same hand that had signed the divorce papers without a single correction. Thomas. After all this time.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"The kitchen clock ticked. Outside,\\n            a cardinal landed on the feeder and regarded her through the window with what she could only describe as judgment. She set the letter on the counter,\\n            poured herself a cup of coffee she no longer wanted,\\n            and sat down to read.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"*Dear Eleanor,\\n            *\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"*I know you have every reason to throw this away unread. I am writing anyway because there are things I should have told you decades ago,\\n            and I have recently learned that time is shorter than I assumed. The house on Meridian Street \\u2014 you remember the one \\u2014 still stands. I have left something there for you. Whether you retrieve it is your choice. But I think you will want to know the truth about what happened the night Daniel disappeared.*\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Eleanor read the letter three times. Then she folded it precisely along its original creases,\\n            placed it back in the envelope,\\n            and set it on the shelf beside the cookbooks where she kept things she intended to deal with later but never did.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"She lasted four hours.\"\n    },\n    {\n      \"type\": \"page-break\"\n    },\n    {\n      \"type\": \"headline\",\n      \"level\": \"h1\",\n      \"text\": \"Chapter 2: Meridian Street\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"The drive from campus to Millhaven took three hours if you obeyed the speed limit,\\n            which Eleanor always did,\\n            even now,\\n            even with her hands white-knuckled on the steering wheel and her mind racing through every possible explanation for why Thomas Ashworth had chosen this particular moment to break three decades of silence.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Millhaven looked smaller than she remembered. The main street had lost its hardware store and gained a coffee shop with a chalkboard menu. The library had a new wing. The gas station where she and Thomas used to buy cherry slushies on summer afternoons had become a pharmacy.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"She turned onto Meridian Street and felt her stomach drop. The house was exactly as she remembered \\u2014 a two-story Victorian with peeling blue paint and a wraparound porch that sagged in the middle like a held breath. The oak tree in the front yard had doubled in size. Everything else was frozen.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"The front door was unlocked. Inside,\\n            the air was thick with dust and something else \\u2014 the faint,\\n            sweet smell of old paper. Sheets covered the furniture like ghosts standing guard. Eleanor pulled one back and found the leather armchair where Thomas's father used to sit reading the evening paper,\\n            a glass of bourbon balanced on the armrest.\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"On the mantel above the fireplace,\\n            propped against a stopped clock,\\n            was a second envelope. This one was thicker. She opened it and found a photograph she had never seen before \\u2014 Daniel,\\n            Thomas,\\n            and a third person she did not recognize,\\n            standing in front of this very house. On the back,\\n            in Thomas's handwriting: *August 1994. The last good day.*\"\n    },\n    {\n      \"type\": \"paragraph\",\n      \"markdown\": \"Below the photograph was a key. Small,\\n            brass,\\n            unremarkable. And a note in Thomas's hand: *The basement. You always were the braver one.*\"\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "6203ba2e-523d-46da-bafa-dc1aedd0bcd8",
      "name": "Generate Document",
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
            "node": "Generate Document",
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
Generate a print-ready PDF manuscript at 6x9 inch trim size. Use the generate_document tool with format "pdf" and these content blocks:

- Title page: book title, subtitle, and author name centered
- Table of contents with chapter listings
- Chapters: each with a headline and paragraph content, starting on a new page
- Page settings: 6x9 inches with 72pt margins for print-on-demand compliance
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "JVBERi0xLjcKMSAwIG9iago8...",
    "mime_type": "application/pdf"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
