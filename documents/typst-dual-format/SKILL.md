---
name: typst-dual-format
description: Expert in Typst dual-format content system for FINMA project. Use when creating or modifying .typ files, working with dual-format templates, presentation functions, document functions, or troubleshooting Typst compilation. Handles both presentation slides and study guide documents from single content source.
---

# Typst Dual-Format Expert

You are an expert in the FINMA Content Management dual-format Typst system. This project uses a sophisticated architecture where **a single content file** can be rendered as either a presentation (slides) or a document (study guide).

## Core Architecture

### The Dual-Format System

The project uses **three key files** that work together:

1. **`dual_format.typ`** - The orchestration layer
   - Manages output mode (presentation vs document)
   - Provides conditional content functions
   - Imports and re-exports presentation and document functions
   - Defines unified `content-block()` that adapts to mode

2. **`presentation_functions.typ`** - Slide creation functions
   - `slide()`, `title-slide()`, `section-slide()`
   - Grid layouts: `two-column-grid()`, `two-by-two-grid()`, `three-column-grid()`
   - `two-row-grid()`, `three-row-grid()`
   - `make-table()` for formatted tables

3. **`document_functions.typ`** - Study guide functions
   - `section-heading()`, `formula-block()`
   - `concept-box()`, `example-box()`, `definition-box()`
   - `takeaways-box()`, `examples-box()`

### How Content Files Work

Every content file follows this pattern:

```typst
#import "../dual_format.typ": *

#document-only[
  #pagebreak()
  #outline()
]

#section("Introduction")

#content-block(
  title: "Concept Name",
  subtext: "Brief description shown under title",
  center: false,  // true for centered layout, false for top-aligned
  summary: [
    // Content shown in PRESENTATION mode
    #two-row-grid(
      [ First section content ],
      [ Second section content ]
    )
  ],
  details: [
    // Additional content for DOCUMENT mode only
  ],
  examples: [
    // Examples shown on separate slide in presentations
    // Shown in orange box in documents
  ]
)
```

## Key Functions Reference

### Content Organization

**`content-block()`** - The main content function
- `title:` - Section title
- `subtext:` - Subtitle text (shown under title line)
- `center:` - Boolean, whether to vertically center content in presentations
- `summary:` - Content for presentation slides (and documents)
- `details:` - Additional content for documents only
- `examples:` - Examples (separate slide in presentations, orange box in documents)

**Behavior:**
- **Presentation mode**: Shows title, creates new slide, displays summary (centered or top-aligned based on `center` parameter), creates separate examples slide if examples provided
- **Document mode**: Shows all content (summary + details + examples in orange box)

### Layout Functions (Available in both modes)

**Grid Layouts:**
```typst
#two-column-grid(left, right, col-height: 1)
#two-row-grid(top, bottom, row-height: 1)
#two-by-two-grid(top-left, top-right, bottom-left, bottom-right)
#three-column-grid(left, middle, right)
#three-row-grid(top, middle, bottom)
```

**Table Builder:**
```typst
#make-table(
  columns: (1fr, 1fr, 1fr),
  row-height: (auto, 1fr, 1fr),  // Can be auto, 1fr, or array
  header-fills: (rgb("#384d81"), rgb("#384d81"), rgb("#384d81")),
  header-styles: (("Title", "subtitle"), ("Title", "subtitle"), ...),
  body-content: (
    ([ content ], [ content ], [ content ]),  // Row 1
    ([ content ], [ content ], [ content ]),  // Row 2
  ),
  border-color: gray,
  border-width: 0.5pt,
)
```

### Section Functions

```typst
#section("Section Name")  // Adapts to mode automatically
// In presentations: Creates section divider slide
// In documents: Creates heading with blue line
```

### Conditional Content

```typst
#presentation-only[ /* content only in slides */ ]
#document-only[ /* content only in study guides */ ]
#both-formats(
  /* presentation content */,
  /* document content */
)
```

## Project Structure

```
FINMA_Content_Management/
├── .claude/
│   └── skills/           # ← Project-specific skills go here
├── dual_format.typ       # Main orchestration file
├── presentation_functions.typ
├── document_functions.typ
├── test_templates/
│   ├── images/
│   ├── equity_research_content.typ    # Example content file
│   ├── equity_research_document.typ   # Document driver
│   └── equity_research_slide.typ      # Presentation driver
├── cropped_FINMA_logo.png
├── finma_bg_1.png
└── README.md
```

## Workflow: Creating New Content

### 1. Create Content File

Create `content.typ` with your content using the dual-format structure:

```typst
#import "../dual_format.typ": *

#document-only[
  #pagebreak()
  #outline()
]

#section("Your Section")

#content-block(
  title: "Your Topic",
  subtext: "Brief description",
  center: false,
  summary: [
    // Main content with layout functions
  ],
  examples: [
    // Optional examples
  ]
)
```

### 2. Create Presentation Driver

Create `presentation.typ`:

```typst
// Equity Research - Presentation Driver
// This file renders equity_research.typ in slide presentation format

#import "../dual_format.typ": *

// Set presentation mode and page format
#set page(
  width: 29.7cm,
  height: 20.999cm,
  margin: 0in,
  flipped: false,

  footer: [
    #align(right)[
      #text(size: 18pt, fill: rgb("#0a0f14"))[
        #context counter(page).display("1")
      ]
    ]
  ]
)
#set text(size: 12pt)
#set text(font: "Arial")
#set heading(numbering: none)
#set-mode("presentation")

// Presentation title slide
#title-slide(
  title: "Financial Markets Academy (finma)",
  subtitle: "Equity Research",
  author: "August 2025"
)


// Set margin for all following slides
#set page(
  width: 29.7cm,
  height: 20.999cm,
  margin: (x: 0.5in, y: 0.5in),
  flipped: false,
  header: [
    #align(right + horizon)[
      #v(0.78in)
      #image("../cropped_FINMA_logo.png", height: 0.4in)
    ]
  ],
  footer: [
    // bottom divider line
    #line(
      length: 100%,
      stroke: (paint: rgb("#609ed6"), thickness: 1.5pt)
    )
    #v(-0.2cm)

    #align(right)[
      #text(size: 12pt, fill: rgb("#0a0f14"))[
        #context counter(page).display("1")
      ]
    ]
  ]
)

#include "equity_research_content.typ"
```

### 3. Create Document Driver

Create `document.typ`:

```typst
// Week 2 Option Pricing - Document Driver (Study Guide)
// This file renders Week_2_Content.typ in long-form document format

#import "../dual_format.typ": *

// Set document mode and page format
#set page(
  paper: "a4",
  margin: (top: 0.7in, right: 0.7in, bottom: 0.7in, left: 0.7in),
  footer: [
    #v(0.1in)
    // line across the footer area
    #line(length: 100%)  
    // space after the line
    #v(-6pt)
    // footer text aligned right
    #align(center)[
      #text(size: 12pt)[#context counter(page).display("1")]
    ]
  ],
  header: [
    // Three equally spaced columns
     #text(size: 10pt)[
      #grid(
        columns: 3,
        gutter: 1fr, // spreads them evenly
        [
          FINMA
        ],
        [
          Week 2: Option Pricing Study Guide
        ],
        [
          August 2, 2025
        ]
      )
    ]
    #v(-10pt)
    #line(length: 100%)
    #v(0.2in)
  ],
)
#set text(size: 12pt)
#set heading(numbering: "1.")
#set par(justify: true)
#set-mode("document")

// Document title and metadata

#page(
  margin: (top: 2in),
  header: [
    #align(right)[#image("../cropped_FINMA_logo.png", height: 0.3in)]
    #v(0.9in)
  ],
  footer: none,
)[
  #align(center)[
    #text(size: 18pt, weight: "bold")[Week 2: Option Pricing Study Guide]
    #v(0.5em)
    #text(size: 14pt)[Black-Scholes Model and Greeks]
    #v(0.5em)
    #text(size: 12pt)[Derivatives Course - Financial Markets Academy]
    #v(0.5em)
    #text(size: 11pt)[August 2, 2025]
  ]
]

// Include the course content
#include "equity_research_content.typ"
```

### 4. Compile

```bash
# Compile presentation
typst compile presentation.typ

# Compile document
typst compile document.typ

# Watch for changes (auto-recompile)
typst watch presentation.typ
```

## Best Practices

### Content Creation

1. **Always use `content-block()` for main content**
   - This ensures proper formatting in both modes
   - Use `center: false` for content-heavy slides
   - Use `center: true` for simple concept slides

2. **Use layout functions inside summary blocks**
   - `two-column-grid()` for side-by-side content
   - `two-row-grid()` for top/bottom layouts
   - `two-by-two-grid()` for 2x2 layouts

3. **Images in grids**
   ```typst
   #two-column-grid(
     [
       Text content here
     ],
     [
       #box(width: 100%, height: 100%)[
         #align(center + horizon)[
           #image("images/your-image.png")
         ]
       ]
     ]
   )
   ```

4. **Examples are always separate**
   - In presentations: Creates new slide titled "Title (contd./Examples)"
   - In documents: Orange bordered box after main content
   - Examples are always in an orange box via `examples-box()`

5. **Use `document-only` for outlines**
   - Outlines only make sense in study guides
   - Always place after imports, before content

### Troubleshooting

**Common Issues:**

1. **Content not appearing**
   - Check mode is set correctly: `#set-mode("presentation")` or `#set-mode("document")`
   - Verify import path: `#import "../dual_format.typ": *`

2. **Slide overflow**
   - Use `center: false` parameter
   - Break content into multiple `content-block()` calls
   - Reduce text size in presentation driver

3. **Grid alignment issues**
   - Use `box(width: 100%, height: 100%)` to fill grid cells
   - Use `align(center + horizon)` for centered content in cells

4. **Table formatting**
   - Row heights: Use array like `(auto, 1fr, 1fr)` for variable heights
   - Header colors: Provide array of colors matching column count
   - Body content: Must be 2D array (rows × columns)

5. **Using \$ signs**
   - Note that typst cannot render $ signs properly, you need to call it like `\$` instead

### Colors Available

From presentation_functions.typ:
- `blue` = rgb("#1f4e79")
- `green` = rgb("#006d8f")
- `red` = rgb("#c5504b")
- `gray` = rgb("#595959")

Additional colors used:
- Title line: rgb("#609ed6") - Light blue
- Examples box: rgb("#ea580c") - Orange
- Examples background: rgb("#fed7aa") - Light orange

## Advanced Features

### Custom Table Example

```typst
#make-table(
  columns: (1fr, 1fr, 1fr),
  row-height: (auto, 1fr, 1fr),
  header-fills: (rgb("#384d81"), rgb("#384d81"), rgb("#384d81")),
  header-styles: (
    ("Feature", ""),
    ("Labour Intensive", ""),
    ("Capital Intensive", "")
  ),
  body-content: (
    (
      [Main cost type
       - Labor wages
       - Training costs],
      [- Variable labor costs
       - High turnover],
      [- Equipment
       - Facilities
       - Technology]
    ),
    (
      [Scalability
       - Harder to scale
       - Linear growth],
      [- Hire more people
       - Time-intensive],
      [- Easier to scale
       - Upfront investment]
    )
  )
)
```

### Multi-slide Content

For very long content, create multiple content blocks:

```typst
#content-block(
  title: "Topic Part 1",
  center: false,
  summary: [ /* First part */ ]
)

#content-block(
  title: "Topic Part 2",
  center: false,
  summary: [ /* Second part */ ]
)
```

## Integration with Other Skills

When working on FINMA content:
- Use **typst-dual-format** (this skill) for Typst syntax and structure
- Use **equity-research** skill for financial content and formatting
- Use **financial-documents** skill for compliance and professional standards

## Quality Checklist

Before finalizing content:
- ✓ Both presentation and document compile without errors
- ✓ Content is readable in both formats
- ✓ Images display correctly
- ✓ Tables are formatted properly
- ✓ Examples are in appropriate boxes
- ✓ Section dividers work in both modes
- ✓ Page numbers and headers/footers display correctly
- ✓ No orphaned content or layout issues