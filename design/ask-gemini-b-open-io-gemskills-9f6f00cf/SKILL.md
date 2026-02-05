---
name: ask-gemini
description: Ask Gemini 3.0 Pro Preview for design advice, spatial awareness analysis, and visual/design questions. Use when you need expert design feedback, want to review design intentions or changes, need spatial understanding of layouts, or want a second opinion on visual aesthetics. Gemini excels at design critique, layout analysis, and understanding visual relationships. Supports up to 10 images per request for comparison.
allowed-tools: "Bash(bun:*)"
---

# Ask Gemini

Ask Gemini 3.0 Pro Preview text questions with optional images (up to 10) for design and spatial awareness analysis.

## When to Use

- Design review and critique
- Spatial layout analysis
- Visual hierarchy assessment
- Color scheme evaluation
- Typography feedback
- UI/UX design guidance
- Comparing design alternatives (send multiple images)
- Three.js/WebGL composition analysis

## Usage

Run the ask_gemini script with your question and optional images:

```bash
# Text-only question
bun run /path/to/skills/ask-gemini/scripts/ask_gemini.ts "Your question here"

# With single image
bun run /path/to/skills/ask-gemini/scripts/ask_gemini.ts screenshot.png "Analyze this design"

# With multiple images - compare designs
bun run /path/to/skills/ask-gemini/scripts/ask_gemini.ts current.png target.png "Compare these Two designs - what are the key differences?"
```

## Requirements

- `GEMINI_API_KEY` environment variable must be set
- Get an API key from https://aistudio.google.com/apikey

## Image Support

- Maximum 10 images per request
- Total request size limit: 20 MB
- Supports: PNG, JPG, JPEG, GIF, WEBP, BMP
- Images scaled to max 3072x3072 while preserving aspect ratio

## Model

Uses **gemini-3-pro-preview** - specifically optimized for:
- Design and spatial awareness
- Visual critique and comparison
- Layout understanding
- Multi-image analysis
