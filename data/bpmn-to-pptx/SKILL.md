---
name: bpmn-to-pptx
version: 2.0.0
description: "Transform BPMN 2.0 process diagrams into professional, editable PowerPoint presentations. Features a 3-tier hierarchical layout with chevrons, rounded boxes, and square task boxes with detailed bullet points."
license: MIT
---

# BPMN to PowerPoint Generator

## Overview

Transforms BPMN 2.0 process diagrams into professional, editable PowerPoint presentations following consulting best practices (McKinsey/BCG standards). Automatically manages complexity by chunking processes into hierarchical slide structures with 8-10 steps per slide.

## When to Use This Skill

- Converting BPMN process maps to client-ready presentations
- Creating stakeholder review decks from technical process diagrams
- Generating hierarchical process overviews for executive audiences
- Building feedback-ready process documentation

## CRITICAL: Read Before Starting

1. This skill depends on the core `pptx` skill - ensure you understand the html2pptx workflow
2. Always validate generated presentations visually before delivering to users
3. Complex processes (40+ steps) should be reviewed for potential decomposition

## Input Requirements

### Required
- BPMN 2.0 XML file (`.bpmn` extension)

### Supported BPMN Elements

| BPMN Element | Supported | PowerPoint Representation |
|--------------|-----------|---------------------------|
| `<bpmn:startEvent>` | ✅ | Green oval |
| `<bpmn:endEvent>` | ✅ | Red oval |
| `<bpmn:userTask>` | ✅ | Rounded rectangle (blue) |
| `<bpmn:serviceTask>` | ✅ | Rounded rectangle (purple) |
| `<bpmn:exclusiveGateway>` | ✅ | Orange diamond |
| `<bpmn:parallelGateway>` | ✅ | Purple diamond with + |
| `<bpmn:subProcess>` | ✅ | Rounded rectangle with border |
| `<bpmn:sequenceFlow>` | ✅ | Connecting arrows |

### Optional Parameters

```yaml
options:
  brand: "default" | "stratfield" | path/to/config.yaml
  max_steps_per_slide: 10          # Default: 10, Range: 6-12
  include_overview: true           # Default: true
  include_decision_summary: false  # Default: false
  feedback_mode: false             # Default: false (adds input zones)
  output_filename: "process.pptx"
```

## Output Structure

The skill generates a multi-slide deck:

1. **Title Slide** - Process name and metadata
2. **Overview Slide** - Phase-level chevron diagram (max 7 phases)
3. **Phase Detail Slides** - One per phase with 3-tier hierarchical layout:
   - **Level 1 (Chevrons)**: All phases shown as chevrons, with current phase highlighted
   - **Level 2 (White Rounded Boxes)**: Task groups/categories within the phase
   - **Level 3 (Gray Square Boxes)**: Individual tasks/activities
   - **Bullet Points**: Detailed descriptions of each task below the boxes
4. **Decision Summary** - (Optional) Key decision points listed

## Usage

### Step 1: Parse the BPMN File

```python
from src.bpmn_parser import BPMNParser

parser = BPMNParser()
process = parser.parse("/path/to/process.bpmn")

print(f"Process: {process.name}")
print(f"Elements: {len(process.elements)}")
print(f"Phases: {len(process.phases)}")
```

### Step 2: Generate the Presentation

```python
from src.slide_generator import ProcessPresentationGenerator

generator = ProcessPresentationGenerator(
    brand_config="default",  # or "stratfield" or path to YAML
    max_steps_per_slide=10
)

output_path = generator.generate(process, "output.pptx")
```

### Step 3: Visual Validation

```bash
# Convert to images for review
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

## Complete Example

```python
#!/usr/bin/env python3
"""Generate PowerPoint from BPMN file."""

from src.bpmn_parser import BPMNParser
from src.slide_generator import ProcessPresentationGenerator

# Parse BPMN
parser = BPMNParser()
process = parser.parse("rochester-2g-rebuild.bpmn")

# Generate presentation
generator = ProcessPresentationGenerator(
    brand_config="default",
    max_steps_per_slide=10,
    include_overview=True
)

output_path = generator.generate(process, "carburetor-rebuild.pptx")
print(f"Generated: {output_path}")
```

## Design Principles Applied

### 1. Pyramid Principle (Barbara Minto/McKinsey)
- Action titles state the "so what" - complete sentences with insights
- Overview before details - high-level view first, then drill down
- MECE structure - Mutually Exclusive, Collectively Exhaustive phases

### 2. Cognitive Load Management
- **8-10 Step Limit** per slide (based on Miller's research)
- **Max 7 Phases** on overview slide
- Progressive disclosure through hierarchical navigation

### 3. Visual Hierarchy
- **3-Tier Layout**: Each phase slide shows chevrons → rounded boxes → square boxes
  - Level 1 (Chevrons): Phase navigation - shows all phases with current highlighted
  - Level 2 (White Rounded Boxes): Task group categories - conceptual groupings
  - Level 3 (Gray Square Boxes): Individual tasks - specific activities
- Bullet points below provide detailed descriptions for each task
- Single row per level for clean, scannable layout

### 4. Consulting Standards
- Action titles (not labels)
- 20-25% whitespace for annotations
- Numbered decision points for discussion

## BPMN Element Mapping

| BPMN Element | Shape | Default Fill | Border |
|--------------|-------|--------------|--------|
| Start Event | Oval | #C6F6D5 (green) | #38A169 |
| End Event | Oval | #FED7D7 (red) | #E53E3E |
| User Task | Rounded Rect | #EBF8FF (light blue) | #3182CE |
| Service Task | Rounded Rect | #E9D8FD (light purple) | #805AD5 |
| Decision Gateway | Diamond | #FEFCBF (yellow) | #D69E2E |
| Parallel Gateway | Diamond | #E9D8FD (purple) | #805AD5 |
| Subprocess | Rounded Rect + | #F7FAFC (gray) | #718096 |
| Merge Gateway | Diamond | #E2E8F0 (gray) | #718096 |

## Brand Configuration

Create custom brand configurations in JSON or YAML format. JSON is recommended for portability.

### JSON Style Format (Recommended)

```json
{
  "name": "My Company",
  "colors": {
    "primary": "1A365D",
    "secondary": "2B6CB0",
    "accent": "ED8936",
    "background": "FFFFFF",
    "text_primary": "1A202C",
    "text_secondary": "4A5568",

    "task_fill": "EBF8FF",
    "task_border": "3182CE",
    "decision_fill": "FEFCBF",
    "decision_border": "D69E2E",
    "parallel_fill": "E9D8FD",
    "parallel_border": "805AD5",
    "start_fill": "C6F6D5",
    "start_border": "38A169",
    "end_fill": "FED7D7",
    "end_border": "E53E3E",
    "subprocess_fill": "F7FAFC",
    "subprocess_border": "718096",
    "merge_fill": "E2E8F0",
    "merge_border": "718096"
  },
  "fonts": {
    "title": "Calibri Light",
    "heading": "Calibri",
    "body": "Calibri",
    "sizes": {
      "slide_title": 28,
      "action_title": 16,
      "phase_label": 14,
      "shape_text": 10,
      "footnote": 8
    }
  },
  "layout": {
    "slide_width": 13.333,
    "slide_height": 7.5,
    "margin_left": 0.5,
    "margin_right": 0.5,
    "margin_top": 0.75,
    "margin_bottom": 0.5,
    "shape_width": 1.4,
    "shape_height": 0.6,
    "shape_gap_h": 0.3,
    "shape_gap_v": 0.7
  }
}
```

### Color Properties Reference

| Property | Purpose | Used In |
|----------|---------|---------|
| `primary` | Main brand color | Slide titles, active chevrons, level 2 box borders |
| `secondary` | Secondary brand color | Alternating chevrons, gradients |
| `accent` | Highlight color | Call-to-action elements, emphasis |
| `background` | Slide background | All slides |
| `text_primary` | Main text color | Body text, labels |
| `text_secondary` | Muted text color | Subtitles, secondary labels |
| `task_fill` / `task_border` | Task box styling | User tasks, service tasks |
| `decision_fill` / `decision_border` | Decision diamond styling | Exclusive gateways |
| `parallel_fill` / `parallel_border` | Parallel gateway styling | Parallel gateways |
| `start_fill` / `start_border` | Start event styling | Start events |
| `end_fill` / `end_border` | End event styling | End events |
| `subprocess_fill` / `subprocess_border` | Subprocess styling | Subprocesses |
| `merge_fill` / `merge_border` | Merge gateway styling | Merge gateways |

### Pre-built Style Files

| File | Description |
|------|-------------|
| `cfa-style.json` | CFA Institute brand (deep blue/purple palette) |
| `sfc-style.json` | Stratfield Consulting brand (navy/gold palette) |
| `default.yaml` | Default blue/orange palette |
| `stratfield.yaml` | Stratfield Consulting (YAML format) |

### Usage with Style Files

```python
# Using JSON style file
generator = ProcessPresentationGenerator(
    brand_config="templates/brand_configs/cfa-style.json"
)

# Using preset name
generator = ProcessPresentationGenerator(
    brand_config="stratfield"
)
```

### YAML Format (Legacy)

```yaml
# brand_configs/my_brand.yaml
brand:
  name: "My Company"

colors:
  primary: "1A365D"
  secondary: "2B6CB0"
  accent: "ED8936"
  background: "FFFFFF"

  # Process element colors (optional - uses defaults if not specified)
  task_fill: "EBF8FF"
  task_border: "3182CE"
  decision_fill: "FEFCBF"
  decision_border: "D69E2E"

fonts:
  title: "Calibri Light"
  heading: "Calibri"
  body: "Calibri"
  sizes:
    slide_title: 28
    action_title: 16
    shape_text: 10

layout:
  slide_width: 13.333  # inches (16:9)
  slide_height: 7.5
  max_lanes: 5
  shape_width: 1.4
  shape_height: 0.6
```

## Phase Detection

The skill detects phases in this priority order:

1. **Explicit XML Comments** - `<!-- Phase 1: Name -->` markers in BPMN
2. **Subprocess Boundaries** - Each subprocess becomes a phase
3. **Auto-Chunking** - Groups of 8-10 elements with breaks at:
   - Parallel gateway splits
   - Major decision points
   - Natural process breaks

## Limitations

- Maximum 50 elements recommended (larger processes should be decomposed)
- Swimlanes not yet supported (single-lane horizontal flow only)
- Collapsed subprocesses shown as single shape (not expanded)
- Complex nested gateways may require manual adjustment

## File Structure

```
bpmn-to-pptx/
├── SKILL.md                    # This file
├── src/
│   ├── __init__.py
│   ├── bpmn_parser.py          # BPMN XML parsing
│   ├── process_model.py        # Data structures
│   ├── hierarchy_builder.py    # Phase detection & chunking
│   ├── slide_generator.py      # Main orchestration
│   ├── html_templates.py       # HTML slide templates
│   └── brand_config.py         # Brand configuration loader
├── templates/
│   └── brand_configs/
│       ├── style-schema.json   # JSON schema for style files
│       ├── cfa-style.json      # CFA Institute brand colors
│       ├── sfc-style.json      # Stratfield Consulting brand
│       ├── default.yaml        # Default brand (YAML)
│       └── stratfield.yaml     # Stratfield brand (YAML)
└── examples/
    └── rochester-2g-rebuild.bpmn
```

## Dependencies

This skill requires the core `pptx` skill and its dependencies:
- python-pptx (via pptx skill)
- lxml (for BPMN XML parsing)
- pyyaml (for brand configuration)

## Troubleshooting

### "Phase detection failed"
- Ensure BPMN file has proper sequence flows connecting all elements
- Check for orphaned elements without incoming/outgoing flows

### "Too many elements for single slide"
- Reduce `max_steps_per_slide` parameter
- Consider splitting the process into subprocesses in the BPMN source

### "Gateway layout overlap"
- Complex nested gateways may require manual HTML adjustment
- Consider simplifying the BPMN structure

## See Also

- [`/mnt/skills/public/pptx/SKILL.md`](../public/pptx/SKILL.md) - Core PowerPoint skill
- [`/mnt/skills/public/pptx/html2pptx.md`](../public/pptx/html2pptx.md) - HTML to PowerPoint conversion
- [`/mnt/skills/public/pptx/css.md`](../public/pptx/css.md) - CSS design system
