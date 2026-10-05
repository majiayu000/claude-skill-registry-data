---
name: gemini-image-executor
type: executor
description: "Generate production-quality raster PNG graphics via Gemini native image generation. For atmospheric visuals, social media, event posters, and marketing hero images."
version: 0.1.0
---

# Gemini Image Executor Skill

Generate production-quality raster PNG assets via Google's Gemini image generation API. Claude orchestrates — constructing the prompt, mapping aspect ratios, gating on text fidelity — while Gemini renders the image.

## Use When
- Planner spec has `Recommended executor: gemini-image-executor`
- Task needs atmospheric visual quality: organic gradients, flowing shapes, visual depth
- Output is a social media graphic, event poster, hero image, or marketing visual
- Platform-ready PNG is the desired deliverable

## Do Not Use When
- Task requires data accuracy, proportional integrity, or source citations → use `infographic-executor`
- Task requires precision, verifiable values, or editability → use `graphic-design-executor`
- Task requires accessible text (screen readers) → use `graphic-design-executor`
- Task requires vector scalability → use `graphic-design-executor`
- No `GOOGLE_API_KEY` environment variable is available

## Paired With
- `graphic-design-planner`: Upstream — produces the spec with `## Executor Routing`
- `graphic-design-critic`: Downstream — reviews the output (format-aware)

## Execution Protocol

### Phase 1: Input Validation & API Readiness

1. Detect input: planner spec (has `## Executor Routing`) or direct request
2. Extract parameters: asset type, brand tokens, content inventory, visual direction, format/dimensions
3. **API Gate:** Check for `GOOGLE_API_KEY`:
   ```bash
   [ -n "$GOOGLE_API_KEY" ] && echo "API key present" || echo "MISSING"
   ```
   If missing: STOP. Surface: "GOOGLE_API_KEY not found. Set it or fall back to graphic-design-executor (SVG-in-HTML). The output format changes from atmospheric raster to precision vector."
4. Verify API connectivity:
   ```bash
   curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
     -H "x-goog-api-key: $GOOGLE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"gemini-3.1-flash-image-preview","input":"test","response_format":{"type":"image","image_size":"512"}}' \
     | jq '.error // "OK"'
   ```

### Phase 2: Prompt Construction

Convert the planner spec into a narrative prompt. Gemini requires descriptive prose, not structured specs.

Rules:
- **All text content in quotes.** Every string that must appear in the image gets double-quoted in the prompt. This is the single most important text fidelity measure.
- **Typography as prose:** "large, bold, white sans-serif headline" not "font-size: 48px; font-weight: bold"
- **Colors as descriptions with hex:** "deep navy background (#0F172A)" not "background-color: var(--color-bg)"
- **Layout as spatial narrative:** "the headline dominates the upper third, with three feature columns evenly spaced below"
- **Visual direction as atmosphere:** describe the feeling, lighting, depth — use photographic/cinematic terminology
- **No keyword lists.** Full sentences describing what the viewer should see.

### Phase 3: Aspect Ratio & Resolution Mapping

Map the spec's format requirements to Gemini API parameters:

| Format | API aspect_ratio | API image_size |
|--------|------------------|----------------|
| Instagram post (1080×1080) | 1:1 | 2K |
| Instagram story (1080×1920) | 9:16 | 2K |
| LinkedIn post (1200×628) | 16:9 | 2K |
| Twitter/X post (1600×900) | 16:9 | 2K |
| Facebook OG (1200×630) | 16:9 | 2K |
| Event poster portrait | 9:16 or 3:4 | 2K |
| Hero banner (1920×1080) | 16:9 | 2K |
| Presentation slide | 16:9 | 2K |
| Square card | 1:1 | 2K |
| Tall infographic | 2:3 | 2K |

Supported aspect ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

If the spec requests a non-standard ratio, pick the closest supported ratio and document the deviation.

### Phase 4: API Invocation

Single call to the Interactions API:

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image-preview",
    "input": "<NARRATIVE_PROMPT>",
    "response_format": {
      "type": "image",
      "aspect_ratio": "<RATIO>",
      "image_size": "2K"
    }
  }' > /tmp/gemini-response.json
```

Extract and save:
```bash
jq -r '.outputs[] | select(.type == "image") | .data' /tmp/gemini-response.json \
  | base64 -d > <OUTPUT_PATH>/output.png
```

Record metadata:
```bash
jq '{model: .model, usage: .usage}' /tmp/gemini-response.json
```

**Error handling:**
- HTTP errors or `.error` in response → surface exact error, offer retry or fallback
- Empty `.outputs` → check for safety/recitation filter, log and report
- For multi-asset campaigns, make one API call per asset (each aspect ratio is a separate generation)

### Phase 5: Text Fidelity Risk Assessment

Gemini has a ~20% text garbling rate on text-heavy designs. After generation:

1. List every text string from the planner spec's content inventory
2. Rate risk level:
   - **LOW:** 3 or fewer distinct text strings
   - **MEDIUM:** 4–5 distinct text strings
   - **HIGH:** 6+ distinct text strings
3. Flag HIGH risk outputs for mandatory visual verification before critic handoff
4. Note: text accuracy cannot be machine-verified in raster output — visual inspection is required

### Phase 6: Quality Self-Check & Critic Handoff

- Were all spec hex colors included in the narrative prompt?
- Was the style vocabulary translated into atmospheric description?
- Does the output match the requested aspect ratio?
- Write Deviation Log for any spec requirements that could not be expressed in narrative form
- Propose DESIGN_MEMORY.md entry if applicable
- Provide critic handoff command

## Hard Gates
- No generation without `GOOGLE_API_KEY` present — never silently fall back
- No generation without narrative prompt containing all text content in quotes
- No generation without aspect ratio mapping from the spec's format requirements
- No delivery without Text Fidelity Risk assessment
- No delivery without Reference Inventory and Source/Provenance Notes
- No public reference copying

## Required Output Contract
Use these top-level headings exactly:
- `## Parameter Extraction`
- `## Prompt Construction`
- `## API Response`
- `## Generated Files`
- `## Text Fidelity Risk`
- `## Verification Notes`
- `## Design Memory Notes`
- `## Deviation Log`
- `## Execution Summary`
