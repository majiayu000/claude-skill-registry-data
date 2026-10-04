---
name: 2d-pixel-asset
description: >
  Generate 2D pixel art game assets using Google Gemini via Chrome browser automation.
  Triggers when the user wants to create pixel art, game sprites, tilesets, game assets,
  or edit existing game art. Supports reference image uploads for style consistency,
  model selection (Flash/Pro), resolution control, automatic background removal (chroma key,
  ML-based via BiRefNet, or Adobe Express), and rasterization to exact pixel dimensions.
  Use for requests like "create a pixel art sword", "generate a 32x32 character sprite",
  "make a tileset", or "edit this sprite".
---

# 2D Pixel Asset Generator via Gemini + Chrome

Generate pixel art game assets through Google Gemini's web interface using Chrome browser automation, then post-process them to exact pixel dimensions with transparent backgrounds.

## Prerequisites

- Chrome browser with the Claude-in-Chrome extension installed and active
- User logged into Google account at https://gemini.google.com
- Chrome MCP tools available (`mcp__claude-in-chrome__*`)
- Python 3 with Pillow installed (for post-processing)
- **For ML background removal:** `pip install transformers torch torchvision` + CUDA GPU
- **For Adobe Express removal:** User logged into Adobe account

## Tool Loading

**Before using ANY Chrome MCP tool, load it via ToolSearch first:**

```
ToolSearch: "select:mcp__claude-in-chrome__tabs_context_mcp"
ToolSearch: "select:mcp__claude-in-chrome__tabs_create_mcp"
ToolSearch: "select:mcp__claude-in-chrome__navigate"
ToolSearch: "select:mcp__claude-in-chrome__computer"
ToolSearch: "select:mcp__claude-in-chrome__find"
ToolSearch: "select:mcp__claude-in-chrome__upload_image"
```

## Tool Mapping

| Action | MCP Tool |
|--------|----------|
| Get tab context | `mcp__claude-in-chrome__tabs_context_mcp` |
| Create new tab | `mcp__claude-in-chrome__tabs_create_mcp` |
| Navigate to URL | `mcp__claude-in-chrome__navigate` |
| Click, type, screenshot, hover, wait | `mcp__claude-in-chrome__computer` |
| Find elements by description | `mcp__claude-in-chrome__find` |
| Upload reference/edit images | `mcp__claude-in-chrome__upload_image` |
| Read page content | `mcp__claude-in-chrome__read_page` |

## CLI Arguments

Parse these from user input after the skill invocation:

| Argument | Default | Description |
|----------|---------|-------------|
| *(positional)* | -- | Main prompt text (everything not a flag) |
| `--size 32` or `--size 64x32` | `32` | Target pixel dimensions for final output |
| `--output path/` | `./Assets/` | Output directory |
| `--name filename` | derived from prompt | Output filename (no extension) |
| `--model pro|flash` | `pro` | Gemini model selection |
| `--ref path1.png path2.png ...` | none | Reference images for style (up to 14) |
| `--edit path.png` | none | Existing image to edit/modify |
| `--tile` | false | Generate tileable texture (no bg removal) |
| `--resolution 1k|2k|4k` | `1k` | Gemini generation resolution |
| `--no-process` | false | Skip post-processing, keep raw output |
| `--bg-color magenta|green|white` | `magenta` | Background color for chroma key removal |
| `--ml` | false | Use BiRefNet ML model for background removal |
| `--adobe` | false | Use Adobe Express for background removal |
| `--margin N` | `1` | Transparent margin (px) around sprite in final output |

## Workflow

### Aspect Ratio Handling

**CRITICAL: Match the Gemini prompt aspect ratio to the target `--size`.**

Before constructing the prompt, run the script to get the best matching Gemini ratio:

```bash
python "path/to/2d-pixel-asset/scripts/process_asset.py" \
  --size {target_size} --suggest-ratio
```

This outputs the closest Gemini-supported ratio (e.g., `3:2`, `16:9`, `4:3`).
Use this ratio in the prompt as `Aspect ratio {ratio}`.

Examples:
- `--size 32` → `1:1`
- `--size 128x64` → `16:9`
- `--size 64x128` → `9:16`
- `--size 96x128` → `3:4`
- `--size 192x128` → `3:2`

Also add to the prompt: "The subject must be centered and fill the entire canvas from edge to edge with minimal empty space around it."

**After post-processing:** If the script outputs a WARNING about aspect ratio mismatch, inform the user and offer to either:
1. Re-generate with the correct aspect ratio prompt
2. Accept the result with transparent padding on the shorter axis

### Step 1: Initialize Browser Session

```
1. Call tabs_context_mcp to discover existing tabs
2. Call tabs_create_mcp to create a fresh tab
3. Navigate to https://gemini.google.com/app
4. Take a screenshot with computer to verify the page loaded
```

### Step 2: New Chat + Enable Image Generation

**IMPORTANT: The Gemini UI is in GERMAN.**

```
1. Use find to locate "Neuer Chat" button, click it with computer
2. Take a screenshot to confirm new chat is open
3. Use find to locate "Tools" button, click it
4. Use find to locate "Bild erstellen" toggle/option, click it to enable
5. Take a screenshot to confirm image generation is enabled
```

### Step 3: Model Selection

Default model is **Pro**. The model selector shows "Schnell" near the bottom-right of the input area.

```
If user specified --model pro (or no --model flag):
  1. Use find to locate the model dropdown showing "Schnell"
  2. Click it to open the model selector
  3. Select the option labeled with "Pro"
  4. Take a screenshot to confirm Pro is selected

If user specified --model flash or --flash:
  1. Keep "Schnell" (Flash) -- no action needed
```

### Step 4: Upload Reference Images (if --ref provided)

```
1. For each reference image path:
   a. Use upload_image to upload the file
2. Maximum 14 reference images supported
3. Take a screenshot to verify uploads appear in the input area
```

### Step 5: Upload Existing Image for Editing (if --edit provided)

```
1. Use upload_image to upload the specified image
2. The modification instructions will be included in the prompt
3. Take a screenshot to verify the image appears in the input area
```

### Step 6: Construct and Submit the Prompt

Build the prompt by combining the user's core request with pixel art defaults.

**Always include these elements:**

1. **Resolution directive:** "Generate in {resolution} resolution" (default 1K)
2. **Pixel art style:** "pixel art sprite, thick black outlines, no anti-aliasing, clean pixel edges"
3. **Background handling** (based on `--bg-color`, default magenta):
   - For sprites with **magenta** bg: "Isolated on a solid, flat, uniform magenta background. Use EXACTLY hex color #FF00FF (RGB 255, 0, 255). The entire background must be a single pure magenta color with absolutely zero variation. Flat, even, uniform lighting across the entire image."
   - For sprites with **green** bg: "Isolated on a solid, flat, uniform chromakey green background. Use EXACTLY hex color #00FF00 (RGB 0, 255, 0). The entire background must be a single pure green color with absolutely zero variation. Flat, even, uniform lighting across the entire image."
   - For sprites with **white** bg: "Isolated on a solid, flat, uniform pure white background. Flat, even, uniform lighting across the entire image."
   - For tiles (`--tile`): "seamless tileable texture, fills the entire rectangular canvas"
4. **User's core prompt** as the main subject description

**Prompt template (sprites -- default magenta):**

```
Create a pixel art sprite of {user_prompt}. Pixel art style with thick black outlines,
no anti-aliasing, clean pixel edges. The subject must be centered and fill the entire
canvas from edge to edge with minimal empty space around it. Isolated on a solid, flat,
uniform magenta background. Use EXACTLY hex color #FF00FF (RGB 255, 0, 255). The entire
background must be a single pure magenta color with absolutely zero variation. Flat, even,
uniform lighting across the entire image. Generate in {resolution} resolution.
Aspect ratio {aspect_ratio}.
```

**Prompt template (tiles):**

```
Create a seamless tileable pixel art texture of {user_prompt}. Pixel art style with
no anti-aliasing, clean pixel edges. The texture must fill the entire rectangular canvas
with no borders or margins. Seamlessly tileable in all directions. Generate in {resolution}
resolution.
```

**Prompt template (edit mode with --edit):**

```
Modify this pixel art: {user_prompt}. Maintain the pixel art style with thick black
outlines, no anti-aliasing. Keep everything else exactly the same unless specified.
Generate in {resolution} resolution.
```

**Reference:** See `references/prompting-guide.md` for detailed prompt construction strategies, style descriptors, and examples.

**Submitting:**

```
1. Use find to locate the prompt input field
2. Type the constructed prompt using computer action "type"
3. Press Enter to submit
4. Wait 10 seconds (computer wait action)
5. Wait another 10 seconds (computer wait action)
6. Take a screenshot to verify the image was generated
```

### Step 7: Download the Generated Image

```
1. Hover over the generated image using computer action "hover"
2. Look for the download button (arrow icon, top-right of image on hover)
3. Use find to locate the download button ("Bild in Originalgröße herunterladen")
4. Click the download button using the found ref
5. Wait 5 seconds for the download to complete
6. Find the downloaded file:
   ls -t ~/Downloads/*.png | head -5
```

### Step 8: Post-Processing (Background Removal + Rasterize)

Skip this step if `--no-process` is set.

#### Choose background removal strategy

**Decision logic (follow in order):**

1. If `--ml` flag: use BiRefNet ML model
2. If `--adobe` flag: use Adobe Express (Step 8b)
3. If `--tile` flag: skip background removal (`--no-remove-bg`)
4. **Default:** use chroma key with `--bg-color` (default: magenta)

**After downloading, take a screenshot of the generated image and visually inspect it.** If the background looks unclean (gradients, shadows, mixed colors) despite the magenta prompt, consider switching to `--ml` for that image.

#### 8a: Script-based removal (chroma key or ML)

```bash
# Default: Chroma key magenta
python "path/to/2d-pixel-asset/scripts/process_asset.py" \
  ~/Downloads/{downloaded_file}.png \
  --size {target_size} \
  --bg-color magenta \
  --output {output_path}/{filename}.png

# ML fallback (BiRefNet):
python "path/to/2d-pixel-asset/scripts/process_asset.py" \
  ~/Downloads/{downloaded_file}.png \
  --size {target_size} \
  --ml \
  --output {output_path}/{filename}.png

# Green chroma key:
python "path/to/2d-pixel-asset/scripts/process_asset.py" \
  ~/Downloads/{downloaded_file}.png \
  --size {target_size} \
  --bg-color green \
  --output {output_path}/{filename}.png

# Legacy white:
python "path/to/2d-pixel-asset/scripts/process_asset.py" \
  ~/Downloads/{downloaded_file}.png \
  --size {target_size} \
  --bg-color white \
  --output {output_path}/{filename}.png
```

- Default `--size`: `32` (produces 32x32). For non-square: `--size 64x32`.
- If `--tile` is set: add `--no-remove-bg` flag (tiles keep their background).

#### 8b: Adobe Express removal (if --adobe flag)

Use Chrome browser automation to remove background via Adobe Express:

```
1. Create a new tab or reuse existing
2. Navigate to https://new.express.adobe.com/home/tools/remove-background
3. Take a screenshot to verify page loaded
4. Find the upload area / "Browse" button
5. Upload the downloaded Gemini image using upload_image
6. Wait 10-15 seconds for Adobe to process
7. Take a screenshot to verify background was removed
8. Find and click the download button
9. Wait 5 seconds for download
10. Find the downloaded file:
    ls -t ~/Downloads/*.png | head -5
11. Then run process_asset.py with --no-remove-bg to only crop and rasterize:
    python "path/to/2d-pixel-asset/scripts/process_asset.py" \
      ~/Downloads/{adobe_result}.png \
      --size {target_size} \
      --no-remove-bg \
      --output {output_path}/{filename}.png
```

### Step 9: Move to Final Location

```
1. Ensure output directory exists: mkdir -p {output_dir}
2. If --no-process was set, move raw file:
   mv ~/Downloads/{file}.png {output_dir}/{name}.png
3. Report the final file path to the user
```

## Prompt Enhancement for Pixel Art

When enhancing the user's prompt, apply these pixel-art-specific principles:

- **Color palette:** Suggest limited palettes ("16-color palette", "NES palette", "earthy tones with 8 colors")
- **Perspective:** Specify view ("top-down view", "3/4 isometric view", "side-scrolling profile view", "front-facing")
- **Animation frames:** For sprite sheets, specify "single frame, static pose" unless animation is requested
- **Scale reference:** Mention intended use ("suitable for 32x32 grid", "character sprite for 2D platformer")
- **Outlines:** Always specify "thick black outlines" for sprites, optional for tiles
- **Shading:** "flat shading" or "simple 2-tone shading" -- avoid gradients
- **Positive framing:** Describe what to include, not what to exclude. Say "flat uniform lighting" instead of "no shadows"

## Error Handling

- **Page doesn't load:** Retry navigation, verify internet connection
- **Image generation fails:** Simplify the prompt, reduce complexity
- **Download button not visible:** Use find to locate "Bild in Originalgröße herunterladen" button by ref
- **File not in Downloads:** Wait 5 more seconds, check with `ls -t ~/Downloads/*.png | head -5`
- **Chroma key leaves residue:** Switch to `--ml` flag for that image
- **ML model fails to load:** Check torch/transformers installation, verify CUDA available
- **Adobe Express upload fails:** Verify user is logged into Adobe account
- **Model selector not found:** Take a screenshot, look for alternative UI elements near the input area
- **"Bild erstellen" not found:** Try searching for "Bilderstellung" or take a screenshot to identify the correct German label

## Important Notes

- Always create a NEW chat for each generation to avoid context pollution from previous prompts
- The Gemini UI is in **GERMAN** -- all button labels use German text (Neuer Chat, Tools, Bild erstellen, Schnell)
- Load Chrome MCP tools via ToolSearch before every use
- Generated images include C2PA Content Credentials and SynthID watermarks
- Default output directory is `./Assets/` relative to the user's current working directory
- Default background color is **magenta** (#FF00FF) -- avoids conflicts with common game art colors
- The `process_asset.py` script requires Python 3 and Pillow (`pip install Pillow`)
- For ML removal, install: `pip install transformers torch torchvision`
- BiRefNet model (~1GB) downloads on first use to HuggingFace cache
