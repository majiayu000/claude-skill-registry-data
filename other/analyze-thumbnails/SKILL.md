---
name: analyze-thumbnails
description: Batch analyze YouTube thumbnails using Gemini vision API. Deconstructs designs into Background → Graphics → Text layers for pattern extraction.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Analyze YouTube Thumbnails

## Goal
Batch-analyze thumbnail images using Gemini's vision API to extract design patterns organized by layers (Background → Graphics → Text). Based on Meli Garcia's design philosophy of deconstructing designs into separate layers.

## Scripts
- `./scripts/analyze_thumbnail_images.py` - Main batch analysis script
- `./scripts/test_single_thumbnail.py` - Single-image test with cost estimation
- `./scripts/test_gemini_models.py` - List available Gemini models

## Quick Start

```bash
# Analyze all thumbnails (136 images, ~$1.67, ~15 min)
python "Nick Saraev YouTube Skills/analyze-thumbnails/scripts/analyze_thumbnail_images.py"

# Test with single image first (verify API + estimate cost)
python "Nick Saraev YouTube Skills/analyze-thumbnails/scripts/test_single_thumbnail.py"

# List available Gemini models
python "Nick Saraev YouTube Skills/analyze-thumbnails/scripts/test_gemini_models.py"
```

## Layered JSON Structure

Each thumbnail is deconstructed into 3 design layers + 2 analysis sections:

```json
{
  "layers": {
    "background_layer": {
      "type": "solid|gradient|photo|blurred_photo|graphic|pattern",
      "dominant_colors": ["#RRGGBB", "#RRGGBB", "#RRGGBB"],
      "depth_technique": "none|blur|vignette|shadow|gradient|layering",
      "description": "Brief description of the foundation"
    },
    "graphics_layer": {
      "elements_present": ["face", "icons", "shapes", "objects", "arrows"],
      "face_details": {
        "present": true,
        "position": "left|center|right",
        "size_percent": 30-80,
        "emotion": "excited|serious|surprised|enthusiastic",
        "eye_contact": true
      },
      "visual_elements": [
        {"type": "icon|shape|object", "position": "quadrant", "purpose": "emphasis", "color": "#RRGGBB"}
      ],
      "composition_technique": "rule_of_thirds|centered|asymmetric|dynamic"
    },
    "text_layer": {
      "text_present": true,
      "word_count": 3-8,
      "text_elements": [
        {"text": "content", "hierarchy": "headline|subheadline", "size": "huge|large", "color": "#RRGGBB"}
      ],
      "typography_style": "bold|outlined|shadow|3d",
      "text_effects": ["shadow", "outline", "background_box"],
      "readability_score": "excellent|good|fair|poor"
    }
  },
  "design_principles": {
    "overall_contrast": "high|medium|low",
    "visual_hierarchy": "text_first|face_first|balanced",
    "color_psychology": "urgency|warmth|authority|energy",
    "scroll_stoppers": ["face", "bright_colors", "high_contrast"],
    "click_triggers": ["promise", "benefit", "curiosity_gap"]
  },
  "effectiveness_analysis": {
    "predicted_ctr": "high|medium|low",
    "primary_hook": "What makes you want to click",
    "strengths": ["strength1", "strength2"],
    "improvements": ["improvement1"],
    "mobile_optimized": true
  }
}
```

## Key Findings (from 10-thumbnail pilot)

| Pattern | Result | Insight |
|---------|--------|---------|
| Face presence | 100% | Always include a face |
| Text presence | 100% | Always add text overlay |
| High contrast | 100% | Critical for scroll-stopping |
| Bold typography | 100% | Never use thin fonts |
| Background boxes | 90% | Text needs contrast backing |
| Word count | Avg 5.1 | Target 3-5 words |
| Asymmetric composition | 50% | Most common layout |
| Urgency emotion | 50% | Primary color psychology |
| Promise trigger | 100% | Every thumbnail makes a promise |

## Cost & Performance

| Metric | Value |
|--------|-------|
| Model | gemini-3-pro-image-preview |
| Avg tokens/image | ~2,200 (1,285 input + 910 output) |
| Cost/image | ~$0.012 |
| Cost/136 images | ~$1.67 |
| Time/image | ~15-20 seconds |
| Batch size | 5 (with 2s delay) |

## Output Location

```
Nick Saraev YouTube Skills/thumbnail-analysis-results/
├── aggregated_patterns.md          # Synthesized patterns across all thumbnails
├── analysis_log.txt                # Full execution log
└── individual/                     # Per-image JSON files
    ├── choice.json
    ├── THUMBNAILS (1).json
    └── ... (127 files)
```

## Design Philosophy

**Think sequentially like a designer building the thumbnail:**
1. **Background layer** - What's the foundation? (photo, gradient, solid)
2. **Graphics layer** - What visual elements sit on top? (face, icons, shapes)
3. **Text layer** - What text sits on the very top? (headline, subhead)

This mirrors how thumbnails are actually constructed in Canva/Photoshop and makes patterns more actionable for both manual design and programmatic generation.

## Thumbnail → Motion Graphics Bridge

The layered analysis is designed to feed into motion graphics generation:
- **Background colors** → animated background gradients
- **Face position** → safe zones for text animations
- **Typography style** → matching kinetic text overlays
- **Color psychology** → consistent emotional tone in video

See `.agent/skills/thumbnail-motion-graphics-bridge/SKILL.md` for the full integration workflow.

## Environment
```
GOOGLE_GEMINI_API_KEY=your_key
# or
GOOGLE_API_KEY=your_key
```

## Learnings

- Gemini 3 Pro Image Preview works best for detailed design analysis
- Images are only ~280 tokens (not 20k as feared) - very affordable
- The layered approach generates ~910 output tokens per image
- `google-generativeai` SDK still works but `google-genai` is the new standard
- Windows: avoid Unicode characters in print statements (cp1252 encoding)
- Use `rglob()` not `glob()` to find images in subdirectories
