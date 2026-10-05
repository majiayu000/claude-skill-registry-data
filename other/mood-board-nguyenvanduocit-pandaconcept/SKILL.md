---
name: mood-board
description: Generate detailed mood board descriptions with colors, textures, furniture, and lighting for a given interior design style. Use when the user wants to visualize a design concept before rendering.
---

# Mood Board Generator

Create rich, detailed mood board descriptions that capture the essence of a design concept — usable as creative briefs or as input for image generation.

## Pre-flight Checks (MANDATORY — run before generating mood board)

**Before generating**, check what data already exists to enrich the mood board.

```
!ls projects/${PROJECT_NAME}/style-config.yaml 2>/dev/null && echo "HAS_STYLE_CONFIG=true" || echo "HAS_STYLE_CONFIG=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

```
!ls projects/${PROJECT_NAME}/brief.md 2>/dev/null && echo "HAS_BRIEF=true" || echo "HAS_BRIEF=false"
```

```
!ls projects/${PROJECT_NAME}/notes.md 2>/dev/null && echo "HAS_NOTES=true" || echo "HAS_NOTES=false"
```

### Decision Logic

```
HAS_STYLE_CONFIG=true?
└── Read style-config.yaml — use exact colors (hex), materials, lighting settings.
    Do NOT invent colors/materials — use what's configured.

HAS_SEMANTIC=true?
└── Read semantic_analysis.json — use real room data (existing materials, colors, furniture).
    Mood board should build ON TOP of what exists, not ignore it.

HAS_BRIEF=true?
└── Read brief.md — extract mood/atmosphere, client preferences, constraints.

HAS_NOTES=true?
└── Read notes.md — check for feedback on previous mood boards or renders to avoid repeating mistakes.

None of the above?
└── Standard mode — gather all inputs from user.
```

**A mood board grounded in real project data is 10x more useful than a generic one.**

## Input

Gather from user or `$ARGUMENTS`:
- **Design style** (reference `/style-guide`)
- **Room type**
- **Mood/atmosphere**: cozy, dramatic, serene, energetic, luxurious, etc.
- **Any specific elements** to include or avoid

## Mood Board Structure

Generate a comprehensive mood board with these sections:

### 1. Concept Statement
A 2-3 sentence evocative description of the overall design vision. Written in present tense, as if describing a completed space.

### 2. Color Story
- **Dominant color** with hex + description of where it appears
- **Supporting colors** (2-3) with hex + usage
- **Accent pop** with hex + how it creates contrast
- **Overall palette mood**: warm/cool/neutral, saturated/muted

### 3. Texture Map
List 5-7 textures present in the space:
- Surface feel (smooth marble, rough linen, brushed brass)
- Visual texture (pattern, grain, weave)
- How textures create contrast and depth

### 4. Key Furniture Pieces
5-8 specific furniture items:
- Name + style description
- Material and color
- Role in the composition (focal point, supporting, functional)

### 5. Lighting Atmosphere
- Natural light quality (golden hour, overcast, bright noon)
- Artificial lighting mood (warm glow, focused spots, ambient wash)
- Shadow play and highlights

### 6. Decorative Elements
- Artwork style and placement
- Plants/greenery type and arrangement
- Accessories (vases, books, candles, sculptures)
- Textiles (throws, cushions, rugs)

### 7. Sensory Experience
Brief evocative description engaging multiple senses:
- What you see on entering
- Textures you'd want to touch
- Implied sounds (crackling fire, water feature, silence)
- Suggested scents (cedar, fresh linen, jasmine)

## Output Format

Present as a structured document with clear sections. End with:
- Suggested next step: `/generate-prompt [style] [room]` to create AI prompts from this mood board
- Note which elements are most important to capture in the prompt

## Session Relevant Skills

- `/generate-prompt` — the natural next step. Converts this mood board into provider-optimized prompts. Pass the key elements (materials, colors, furniture, lighting mood) as input.
- `/design-consult` — should have been used before this skill. If the user jumps straight to mood board without a design brief, suggest running /design-consult first to clarify requirements.
- `/style-guide` — reference when building the mood board. Use style-specific vocabulary to ensure the mood board accurately represents the chosen style.
- `/render` — after generating prompts from this mood board, /render sends them to AI providers.
- `/refine` — if a previous render didn't capture the mood board's intent, use /refine to adjust the prompt based on what went wrong.

## Gotchas

- **Mood board is not a prompt**: Don't write the mood board in prompt-style language. It should read like a creative brief — evocative, sensory, descriptive. /generate-prompt handles the translation to provider-specific format.
- **Don't overload with elements**: 5-8 furniture pieces max. Too many elements create cluttered, unrealistic renders downstream.
- **Color hex codes must be realistic**: Don't invent hex codes. Use established palettes for the style (reference /style-guide colors).
- **Sensory section is not optional**: The sensory experience section differentiates a good mood board from a shopping list. It captures atmosphere that pure keywords miss.
