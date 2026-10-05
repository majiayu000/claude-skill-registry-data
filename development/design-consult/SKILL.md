---
name: design-consult
description: Full AI-powered interior design consultation — room analysis, style recommendation, color palette, materials, and furniture suggestions. Use when the user wants design advice or a complete design brief.
---

# Interior Design Consultation

Provide comprehensive design consultation by analyzing requirements and producing a complete design brief.

## Pre-flight Checks (MANDATORY — run before consultation)

**Before asking questions**, check what data already exists to avoid redundant work.

```
!ls projects/${PROJECT_NAME}/brief.md 2>/dev/null && echo "HAS_BRIEF=true" || echo "HAS_BRIEF=false"
```

```
!ls projects/${PROJECT_NAME}/style-config.yaml 2>/dev/null && echo "HAS_STYLE_CONFIG=true" || echo "HAS_STYLE_CONFIG=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

```
!ls projects/${PROJECT_NAME}/notes.md 2>/dev/null && echo "HAS_NOTES=true" || echo "HAS_NOTES=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

### Decision Logic

```
HAS_SEMANTIC=true?
└── Read semantic_analysis.json — pre-fill style, colors, materials, lighting from Gemini Vision analysis.
    Skip questions about things already known. Announce what was pre-filled.

HAS_BRIEF=true AND brief has content?
└── Read brief.md — pre-fill from existing brief. Only ask about missing/unclear sections.

HAS_STYLE_CONFIG=true?
└── Read style-config.yaml — style, palette, materials already decided. Focus on gaps.

HAS_NOTES=true?
└── Read notes.md — check for previous feedback to avoid recommending rejected options.

HAS_REFERENCE=true AND HAS_SEMANTIC=false?
└── Suggest running /preprocess-room first — Gemini Vision analysis will give much better data for consultation.
```

**Never ask what the data already shows.** Pre-fill and confirm instead of re-asking.

## Consultation Flow

### Step 1: Gather Requirements
Ask the user (if not provided via `$ARGUMENTS`):
- **Space**: Room type, approximate dimensions, existing architectural features (windows, columns, ceiling height)
- **Purpose**: Primary use, number of occupants, lifestyle needs (pets, children, work-from-home)
- **Preferences**: Liked styles, colors they're drawn to, any inspirations (photos, references)
- **Constraints**: Budget range (luxury/mid/budget), climate considerations, existing furniture to keep
- **Mood**: Desired atmosphere (cozy, energetic, serene, dramatic, professional)

### Step 2: Style Recommendation
Based on requirements, recommend 2-3 suitable styles with reasoning:
- Primary style recommendation with justification
- Alternative style that addresses the same needs differently
- Optional: fusion/hybrid style combining elements

Reference `/style-guide` for style characteristics.

### Step 3: Color Palette
Generate a cohesive color palette:
- **Primary color** (60% of space): walls, large surfaces
- **Secondary color** (30%): upholstery, curtains, rugs
- **Accent color** (10%): decorative objects, artwork, throws
- Include hex codes and color names
- Consider lighting conditions (natural light direction, artificial lighting)

### Step 4: Materials & Textures
Recommend materials appropriate to the style:
- **Flooring**: type, color, pattern
- **Wall treatments**: paint, wallpaper, paneling, texture
- **Fabrics**: upholstery, curtains, rugs — material and texture
- **Hard surfaces**: countertops, tabletops — material
- **Metals/finishes**: hardware, fixtures, frames

### Step 5: Furniture Layout Concepts
Suggest key furniture pieces:
- Essential pieces for the room type
- Style-appropriate selections with descriptions
- Spatial arrangement principles (focal point, traffic flow, zones)
- Scale guidance relative to room dimensions

### Step 6: Lighting Plan
Recommend lighting layers:
- **Ambient**: general room illumination
- **Task**: functional lighting for activities
- **Accent**: highlighting features, artwork, architecture
- **Decorative**: statement fixtures that serve as design elements
- Color temperature recommendations (warm/neutral/cool)

### Step 7: Design Brief Output
Compile everything into a structured design brief:

```
## Design Brief: [Room Name]
### Style: [Primary Style] (with [Secondary] influences)
### Color Palette: [colors with hex codes]
### Key Materials: [top 5 materials]
### Furniture Plan: [key pieces]
### Lighting: [approach summary]
### Mood: [atmosphere description]
### Next Steps: [suggest using /generate-prompt or /mood-board]
```

After delivering the brief, suggest next actions:
- `/mood-board` to generate a visual mood board description from this brief
- `/generate-prompt` to create AI rendering prompts based on this brief
- `/render` to send prompts directly to AI providers

## Session Relevant Skills

- `/mood-board` — natural next step after consultation. Takes your design brief and expands it into a rich sensory description. Use when the client wants to "feel" the space before rendering.
- `/generate-prompt` — skip mood board and go straight to prompts. Use when requirements are already detailed enough or the user is in a hurry.
- `/style-guide` — reference during Step 2 (style recommendation). Essential when the user's style preference is vague or when recommending fusion styles.
- `/render` — jump straight to rendering if the user already has a clear prompt. Rarely used directly after consult — usually goes through /generate-prompt first.
- `/edit-design` — if the user arrives with a reference image instead of starting from scratch, redirect to /edit-design. Don't try to consult on an existing image here.

## Gotchas

- **Don't skip style recommendation**: Even if the user says "I want Scandinavian", still present alternatives — they may not know about Japandi or Nordic variants that better match their mood.
- **Budget affects everything**: A "luxury Minimalist" and "budget Minimalist" produce completely different material palettes. Always clarify budget before recommending materials.
- **Climate matters for materials**: Don't recommend wool rugs for tropical climates or rattan for cold/humid areas. Cross-reference location if provided.
- **The brief is the contract**: Everything downstream (mood board, prompts, renders) builds on this brief. Incomplete or vague briefs cascade into poor renders. Be thorough here.
