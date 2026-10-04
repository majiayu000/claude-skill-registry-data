---
name: anime-style-forge
description: >-
  Specialized in anime/2D/character stylization for image generation and conversion. Covers Japanese, Chinese, Korean, and Western art style families. Uses provenance analysis to trace reference images' style DNA, performs a 10-dimension analysis → 3-dimension collapse to precisely lock the style's essence, then matches the optimal tool and prompt approach for generation. Trigger on: "anime-ify", "2D style", "convert to anime", "cel-shading", "ghibli style", "Korean watercolor", "fantasy 3D", "chibi", "Japanese anime style", "style conversion", "manga style", "character illustration", "anime style", "webtoon style", "daily gallery", "daily image series", "daily image in same style", or any request involving converting content into a specific anime/2D art style. Key distinction: User requests generation or conversion to a specific anime/2D art style. Do NOT trigger for: photorealistic photography style, pure logo design, general image editing (crop/background removal etc.).
---
# Anime Style Forge — 2D Style Forging

User describes a character/scene + specifies an art style → generates an image in the corresponding style.
Or uploads an image + specifies an art style → converts to the target style.

## Core Philosophy

- **Style provenance-driven**: First determine which art style family the reference image/target style belongs to (era, school, production method), then match the tool and prompt approach
- **10-dimension → 3-dimension collapse**: Internally analyze anime art style features across 10 dimensions, collapse into 3 user-perceivable dimensions: Style / Character / Tone
- **Style archive library**: Each art style has a complete visual DNA archive (prompt template + negative words + parameter presets + pitfall warnings) — don't rely on the model to "guess"
- **Ultra-lightweight operation**: One sentence + one image (optional) → generate directly, deliver results first then iterate

## Conventions

- Intermediate artifacts stored in `./.anime-style-forge/{session_name}/`
- **Single image output**: Each generation outputs only 1 complete image. Prompt must never contain "grid", "collage", "2x2", "4-panel"
- **Four-panel grid cropping**: Some engines output 2x2 four-panel grids instead of single images. After generation, you **must** automatically crop to a single image (see Phase 3 single image extraction process). Users should only see the final single image
- **Information masking rules**:
  - **Do not expose specific model/engine names to the user** (e.g., any underlying image generation model names, version numbers, company names). Use capability descriptions instead (e.g., "the engine best suited for this style", "an engine that excels at 3D rendering", "an engine specialized in Japanese anime" etc.)
  - **Do not expose the agent's underlying workflow to the user** (e.g., internal call details like `read_media`, `image agent`, `editing agent`). Only show results and creative intent to the user
  - Internal routing tables (`model-knowledge-base.md`, quick reference tables, etc.) are for agent decision-making only, **not to be shown to the user**
- **Reference image strategy (differentiated by engine capability)**:
  - **Editing-type engines**: Specialized for style fine-tuning/local editing → **must pass reference image**, prompt uses edit-instruction style
  - **Face-lock engines**: Pass original image to lock facial features
  - **Text-to-image engines**: → **do not pass reference image**, use pure text prompt to reconstruct content
  - Reference images are always analyzed first to extract character features, but only editing-type/face-lock engines pass them during generation calls
- All style archives in `references/style-bank.md`
- Art style visual fingerprints in `references/style-fingerprints.md`
- Model capabilities and selection guide in `references/model-knowledge-base.md` (internal reference, not shown to the user)

---

## Pipeline

```
Phase 0  →  Phase 1  →  Phase 2  →  Phase 3  →  Phase 4  →  Phase 5
 Input      Style ID     Quick Pick   Generate    Iterate     Output
```

---

## Phase 0: Input

**Three input modes** (+ 1 series mode):

| Mode | Input | Example |
|------|-------|---------|
| **Pure text generation** | Character/scene description + target art style | "Draw a Chinese xianxia 3D fantasy style male character, black robe holding a sword" |
| **Style conversion** | Reference image + target art style | [Upload photo] "Convert to Ghibli style" |
| **Style identification** | Reference image (no specified style) | [Upload image] "What style is this? Help me generate more in the same style" |
| **Daily series** (→ ref: daily-gallery-pipeline.md) | Reference image + "daily" | "Make an image every day in this style" — endless-loop, daily variation with new prompt |

File structure:
```
.anime-style-forge/{session_name}/
├── analysis.json          # Phase 1 analysis results
├── generation_log.md      # Generation log
└── outputs/               # Generated images v1_01.png …
```

---

## Phase 1: Style Identification

### Branch Logic

- **User has specified a style** (e.g., "Chinese 3D") → Jump directly to 1c Style Matching
- **User uploaded a reference image but didn't specify** (e.g., "this style") → Execute 1a + 1b analysis
- **User said "anime-ify" without specifying which style** → Execute 1a analysis then recommend

### 1a. Style Provenance

Analyze the reference image's art style origin, cross-referencing `references/style-fingerprints.md`.

**Analysis points** (executed internally, do not expose call details to user):
- Compare one-by-one against visual fingerprints in style-fingerprints.md
- Focus areas: line treatment, coloring technique, character proportions, facial rendering, color system
- Output fields: style_family / style_id / confidence / clues / era_feel / production / alt_style

### 1b. 10-Dimension Art Style Analysis

**Analysis dimensions** (executed internally):
1. Linework: thickness, cleanliness, visibility, outline style
2. Coloring: cel-shading/gradient/watercolor/impasto/flat color
3. Proportions: head-to-body ratio, realism level, chibi level
4. Face: eye size/rendering, nose treatment, mouth style
5. Palette: saturation, color temperature, dominant hues, color logic
6. Shading: binary shadows/soft gradients/no shadows/dramatic
7. Background: realistic/simplified/solid color/atmospheric
8. Era: which era's art style characteristics
9. Medium: digital/traditional/3D/hybrid
10. Origin: Japanese/Chinese/Korean/Western/hybrid
```

### 1c. Collapse to Style / Character / Tone

| Dimension | Underlying Components | Meaning |
|-----------|----------------------|---------|
| **Style** | Linework + Coloring + Medium + Era | What technique was used to draw it |
| **Character** | Proportions + Face + Shading | What the characters look like |
| **Tone** | Palette + Background + Origin | Overall feeling |

Take weighted averages of sub-dimension scores to determine the style's **soul axis** (the 1–2 most distinctive dimensions).

### 1d. Style Matching

Match analysis results against style archives in `references/style-bank.md`.

**Matching priority**:
1. Exact style_id match
2. style_family + era_feel + production combination match
3. 10-dimension feature vector nearest-neighbor match
4. No match → List Top 3 closest styles for user to choose

### 1e. Write analysis.json

```json
{
  "origin": { "style_family": "...", "style_id": "...", "confidence": 0.85, "clues": [...] },
  "dimensions": { "linework": {...}, "coloring": {...}, ... },
  "collapsed": { "style_axis": 0.9, "character_axis": 0.7, "tone_axis": 0.8 },
  "soul": { "primary": "Style", "summary": "90s cel-shading animation, bold linework + binary shadows are the soul" }
}
```

---

## Phase 2: Quick Pick

### Display Style Identification Results (Mandatory)

When showing identification results to the user, **do not expose model names or internal routing**:

```
🎨 Style Identification
  Style: [style_name] ([style_id])
  Family: [style_family] · [era_feel] · [production]
  Confidence: [confidence]
  Evidence: [top 3 clues]
  Soul axis: [soul_summary]

🛠️ Recommended Approach
  Prompt strategy: [keyword direction for this style]
  Expected result: [visual characteristic description for this style]
```

### Task Type Dimension Decision (Must execute BEFORE style routing)

> The style routing table only solves "which style to generate with," but some tasks' core bottleneck isn't style — it's **consistency / instruction following / output format**. These three dimensions override style routing priority. Run this framework first, then check the style routing table.

#### Three Decision Questions (In Order)

**Q1: Does this image need to reference a previous image (or other generated images)?**
- Yes → Must choose an engine with `max_refs ≥ 1`, **exclude Niji 7 / MJ V7** (they have max_refs=0, cannot accept reference images)
- No → Continue to Q2

**Q2: Will this task's output be reused as a reference image for the next step?**
- Yes → Must output single image, **exclude Niji 7 / MJ V7** (they output fixed four-panel grids, must crop before passing)
- No → Continue to Q3

**Q3: Consistency vs. ultimate style — which is the top priority?**
- Consistency first → **nano_banana preferred** (strong instruction following + max_refs=10 + single image output)
- Style first → Enter the style routing table below

#### Task Type → Engine Constraint Quick Reference

| Task Type | Core Need | Engine Constraint | Recommended |
|-----------|-----------|-------------------|-------------|
| **Storyboard/multi-frame sequential** (same character/scene N≥2 images) | Cross-image consistency + lockable composition | max_refs ≥ 1, single image output | **nano_banana** |
| **Fixed composition, change variables only** (lighting/season/time) | Composition lock (pass previous frame as ref) | max_refs ≥ 1 | **nano_banana** |
| **Expression variants** (same character, multiple expressions) | Character consistency (face lock) | max_refs ≥ 1 | **nano_banana** |
| **Three-view / multi-angle character sheets** (same character) | Character consistency | max_refs ≥ 1 | **nano_banana** |
| **Single standalone image** (character sheet/avatar/scene) | Style accuracy | No constraint | → Style routing table |
| **Style conversion** (reference image → target style) | Reference passing + reconstruction | max_refs ≥ 1, text-to-image path | Target style's preferred engine |

#### nano_banana Advantages for Storyboard/Multi-Frame Tasks

- `max_refs = 10`: Each frame can pass the previous frame as a reference, anchoring character appearance and scene composition frame by frame
- Single image output: No four-panel grid cropping issues — output can be directly passed to the next frame
- Strong instruction following: Hard constraints like "keep composition unchanged, only change lighting direction" or "same character, only change expression" have high execution rates
- Supports both Chinese and English: Flexible scene detail descriptions

> ⚠️ **Common mismatch**: Seeing a "storyboard" task → directly checking the style routing table → selecting Niji 7 / MJ V7 → multi-frame character drift + cannot pass reference images. **Must go through the three decision questions first.**

### Style → Engine Routing (Internal use only, do not show to user)

> Full quick reference table in `references/model-knowledge-base.md` → "Style → Model Recommendation Quick Reference" section. Look up preferred/backup engines by style ID, then cross-validate with the "Task Type Dimension Three Decision Questions" above.

**Fallback rules**: When the preferred model is unavailable, use the backup — **keep the original style's prompt approach unchanged**.

### Generation Path Selection (Must ask)

Select path based on task type (do not mention specific engine names when describing paths to the user):

- **Text-to-image reconstruction (preferred for style conversion ⭐)**: Analyze the original image to extract all features, then use the target style's optimal engine to regenerate purely from text. Highest image quality and style depth. **Cross-style conversion must use this path.**
- **Local editing (only for minor modifications)**: Pass original image + editing instructions. Only suitable for changes like hair color/clothing color/adding accessories that **don't alter the overall style**.
- **Face lock**: Pass original image to lock facial features + style prompt. Character resemblance is highest but style conversion depth is uncertain
- **Multi-engine comparison**: Same content generated by 2–3 engines, compare and pick the best

### Content Direction Confirmation

- User has described content → Proceed directly to Phase 3
- User only gave a style without content → Ask "What do you want to draw?"
- User only gave a reference image saying "same style" → Ask "Keep the original image's content or create new content?"

**Quick commands**:
- `Switch style`: Keep content, only switch art style
- `Character sheet`: Full-body/half-body character illustration
- `Avatar`: Square avatar composition
- `Multi-style`: Same content in N different art styles for comparison
- `Multi-model`: Same style using multiple models, one image each for comparison

### Style Conversion Path Selection (Internal decision, do not show to user)

First ask the user: "Do you care more about **character resemblance** or **style accuracy**?"

| User Priority | Path |
|---------------|------|
| Want to look like the original person | Face-lock engine + target style prompt; or text-to-image engine + detailed character description |
| Want the style to be spot-on | Text-to-image path (no reference image); check KB quick reference for preferred engine |
| Want both | Generate one image via each path, let user compare and pick |

---

## Phase 3: Generate

### Prompt Construction

Load the matching style's complete archive from `references/style-bank.md`, assemble using this structure:

```
Final Prompt = [Style anchor words] + [Character/scene description] + [Style detail words] + [Quality enhancement words]
Negative Prompt = [Style-specific negative words] + [Universal negative words]
```

**How each style axis affects the prompt**:

| Soul Axis | Prompt Focus |
|-----------|-------------|
| Style | Line descriptions, coloring techniques, medium keywords, era style tags |
| Character | Head-to-body ratio, facial features, outfit details, pose and action |
| Tone | Color keywords, lighting descriptions, atmosphere adjectives, background treatment |

### Character Description Standards

Anime character descriptions should include (ordered by importance):

1. **Gender/ethnicity/age group**: girl/boy/adult/child
2. **Hairstyle and hair color**: specific description (e.g., "black long straight hair, bangs covering right eye")
3. **Eyes**: color, size, special features
4. **Outfit**: specific description of material and style (e.g., "white silk hanfu with gold embroidery")
5. **Pose/action**: static pose or dynamic action
6. **Expression**: emotional state
7. **Accessories/props**: weapons, jewelry, pets, etc.

### Size Rules

Ask the user or auto-select based on purpose:

| Purpose | Recommended Size |
|---------|-----------------|
| Avatar | 1:1 |
| Character sheet / Character card | 2:3 or 3:4 (portrait) |
| Scene / Landscape | 16:9 |
| Phone wallpaper | 9:16 |
| Vertical comic / Webtoon | 9:16 (narrow and tall) |

If there's a reference image, default to matching the original image's aspect ratio (measure with ffprobe then map — **do not guess**).

### Generation Execution

**Execute per engine**, consult `references/model-knowledge-base.md` for engine-specific prompt writing approaches.

#### Four-Panel Grid Single Image Extraction Process

Midjourney (Niji 7 / V7) outputs fixed 2x2 four-panel grids (4 variants combined in one image), **not single images**. **After every MJ generation call, you must immediately execute the following cropping steps — do not skip**:

1. After generation completes, use `read_media` to analyze the four-panel grid, evaluate the 4 panels (top-left/top-right/bottom-left/bottom-right) for quality
2. Select the best panel (number 1=top-left, 2=top-right, 3=bottom-left, 4=bottom-right)
3. **Immediately crop using bash ffmpeg command** (choose one of four below, replace `INPUT` with actual path, `OUTPUT` with target path):
   ```bash
   # Panel 1 top-left
   ffmpeg -i INPUT -vf "crop=iw/2:ih/2:0:0" OUTPUT
   # Panel 2 top-right
   ffmpeg -i INPUT -vf "crop=iw/2:ih/2:iw/2:0" OUTPUT
   # Panel 3 bottom-left
   ffmpeg -i INPUT -vf "crop=iw/2:ih/2:0:ih/2" OUTPUT
   # Panel 4 bottom-right
   ffmpeg -i INPUT -vf "crop=iw/2:ih/2:iw/2:ih/2" OUTPUT
   ```
4. The cropped single image is the final output — the original four-panel grid **must not** be shown to the user as a deliverable

⚠️ **This process cannot be skipped and must be actually executed with bash ffmpeg**. Merely describing "which panel was selected" without cropping counts as not executed. The image shown to the user must be the cropped single image path, not the four-panel grid path.

#### Per-Engine Prompt Language & Reference Image Passing (Internal reference, do not show to user)

> See `references/model-knowledge-base.md` for details; this is only a quick index.
> When explaining to the user, just say "I'll generate using the approach best suited for this style" — don't mention specific engine names.

Output saved to `.anime-style-forge/{session_name}/outputs/v{version}_{number}.png`.

Synchronously update `generation_log.md`:
```markdown
## v1 — 2026-04-27
- Style: jp_cel (Japanese cel-shading)
- Prompt: [complete prompt]
- Negative: [complete negative words]
- Results: v1_01 ~ v1_04
```

---

## Phase 4: Iteration

After displaying results, ask about satisfaction:

| Option | Action |
|--------|--------|
| ✅ Satisfied | → Phase 5 Output |
| 🔧 Fine-tune | Adjust at the prompt level, don't go back to Phase 1 |
| 🔄 Switch style | Switch to another style_id, keep the content description |
| 🎨 Mix and match | "This image's linework + that image's color palette" → combine dimensions and regenerate |

**Fine-tuning mapping table**:

| User Feedback | Prompt Action |
|---------------|--------------|
| "Make the lines thicker" | Enhance `bold outlines, thick lineart` |
| "Colors are too vibrant" | Lower saturation, add `muted`, `desaturated` |
| "Eyes don't look right" | Refine eye description, add `detailed {style} eyes` |
| "Not anime enough" | Increase style anchor word weight, add `anime, 2D` |
| "Too anime / want semi-realistic" | Reduce style words, add `semi-realistic` |
| "Background too complex" | Add `simple background, solid color bg` |
| "Pose looks unnatural" | Re-describe the pose, add `natural pose` |
| "Looks AI-generated" | Add `hand-drawn feel`, remove over-decorative words like `highly detailed` |
| "Want the feel of a specific anime/game" | Switch to that work's style archive |

---

## Phase 5: Output

Deliverable checklist:

```
📦 Delivery
  Art style: [style_name]
  Soul axis: [soul_summary]
  Generated count: [N] images ([M] iterations)
  File location: .anime-style-forge/{session_name}/outputs/
  Prompt used: [complete prompt, for reuse]
```

**Optional actions**:

- **Archive style**: Save this session's successful style parameters to `.anime-style-forge/style-library/{style_name}.md` for future reuse
- **Multi-style comparison**: Generate 2–3 art styles of the same content, create a comparison display page
- **Continue variants**: Generate more variants based on the most satisfying image

---

## File Structure

```
anime-style-forge/
├── SKILL.md                        # This file
├── references/
│   ├── style-bank.md               # Style archive library (core)
│   ├── style-fingerprints.md       # Art style visual fingerprints (for provenance)
│   ├── model-knowledge-base.md     # Image generation model capability matrix & selection guide
│   ├── benchmark-notes.md          # Benchmark test experience & known weaknesses
│   ├── analysis-example.md         # Analysis example
│   └── daily-gallery-pipeline.md   # Daily image series from reference (FAL local-path pitfall + upload workflow)
└── assets/
    └── template.html               # Result display webpage template
```

## Usage Examples

**Example 1: Specified style generation**
```
User: Draw a Chinese xianxia 3D fantasy style character, black robe holding a sword standing above a sea of clouds

→ Phase 1: Direct match to cn_xuan3d
→ Phase 2: Display style archive + confirm
→ Phase 3: Assemble prompt (Unreal Engine + Chinese fantasy elements + character description)
→ Phase 4: Generate, user fine-tunes results
→ Phase 5: Deliver + save prompt
```

**Example 2: Style conversion**
```
User: [Upload real photo] Help me anime-ify this

→ Phase 1: Default jp_cel, analyze original image's face/outfit/background
→ Phase 2: "Recommending cel-shading style, also available: Ghibli/Korean watercolor"
→ Phase 3: Text-to-image, prompt reconstructs original image content + cel-shading style words
→ Output
```

**Example 3: Style identification + same style**
```
User: [Upload a Korean manhwa screenshot] What style is this? Generate a character in the same style for me

→ Phase 1: Provenance analysis → kr_webtoon, soul axis = Style (clean linework + bright flat coloring)
→ Phase 2: Display analysis + ask for character description
→ Phase 3: Generate using kr_webtoon template
→ Output
```

**Example 4: Multi-style comparison**
```
User: Generate the same character in Ghibli, Chinese 3D, and Korean watercolor — three styles

→ Phase 1: Load jp_ghibli / cn_xuan3d / kr_watercolor in parallel
→ Phase 3: Generate 2 images per style = 6 images total
→ Phase 5: Generate comparison display page
```



**Example 5: Daily gallery / image series** (→ `references/daily-gallery-pipeline.md`)
```
User: "Mache jeden Tag ein Bild nach diesem Muster, irgendwann haben wir eine richtige Gallerie"

→ Phase 0: Detect "daily series" mode → load daily-gallery-pipeline.md
→ Phase 0.5: Setup gallery dir (mkdir + README), upload reference to public URL (freeimage.host — siehe daily-gallery-pipeline.md)
→ Phase 3: image_generate(image_url=ref, prompt="[daily theme], same character design and art style as reference")
→ Download to ~/Bilder/yuno-gallery/day-NNN-YYYY-MM-DD.png
→ Update README index
→ On subsequent days: repeat Phase 3 with new theme prompt
```


> 📋 Benchmark test experience in `references/benchmark-notes.md`
