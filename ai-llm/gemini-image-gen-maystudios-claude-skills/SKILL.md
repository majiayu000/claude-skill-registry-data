---
name: gemini-image-gen
description: >
  Generate images using Google Gemini via Chrome browser automation. This skill should be
  used when the user wants to create, generate, or produce images with Gemini, Google AI,
  or Imagen. Supports resolution control (0.5K, 1K, 2K, 4K), aspect ratios, up to 14
  reference images, style transfer, text rendering, image editing, and inpainting.
  Automatically downloads generated images and moves them to the desired location.
  Triggers on requests like "generate an image", "create a picture with Gemini",
  "make me a 4K image", or "use Gemini to create artwork".
---

# Gemini Image Generation via Chrome

Generate images through Google Gemini's web interface using Chrome browser automation. Built on the Nano Banana / Gemini 3 image generation models.

## Prerequisites

- Chrome browser with the Claude-in-Chrome extension installed and active
- User must be logged into their Google account at https://gemini.google.com
- Chrome MCP tools available (`mcp__claude-in-chrome__*`)

## Tool Mapping

| Action | MCP Tool |
|--------|----------|
| Get tab context | `mcp__claude-in-chrome__tabs_context_mcp` |
| Create new tab | `mcp__claude-in-chrome__tabs_create_mcp` |
| Navigate to URL | `mcp__claude-in-chrome__navigate` |
| Click, type, screenshot, hover, scroll, wait | `mcp__claude-in-chrome__computer` |
| Find elements by description | `mcp__claude-in-chrome__find` |
| Read page accessibility tree | `mcp__claude-in-chrome__read_page` |
| Set form values | `mcp__claude-in-chrome__form_input` |
| Upload reference images | `mcp__claude-in-chrome__upload_image` |
| Extract page text | `mcp__claude-in-chrome__get_page_text` |

## Workflow

### Step 1: Initialize Browser Session

```
1. Call tabs_context_mcp to discover existing tabs
2. Call tabs_create_mcp to create a fresh tab
3. Navigate to https://gemini.google.com/app
4. Take a screenshot to verify the page loaded
```

### Step 2: Start a New Chat with Image Generation Enabled

```
1. Use find to locate the "New chat" button (top-left area / sidebar), then click it with computer
2. Take a screenshot with computer to confirm the new chat is open
3. Use find to locate the "Tools" or settings area in the chat interface
4. Enable "Image generation" / "Bilderstellung" tool by clicking it
5. Take a screenshot to confirm image generation is enabled
```

### Step 3: Upload Reference Images (if provided)

If the user provides reference images (up to 14 supported), upload them BEFORE submitting the prompt:

```
1. Use find to locate the attachment/upload button in the chat input area
2. For each reference image:
   a. Click the upload button with computer
   b. Use upload_image to upload the file to the file input or drop zone
3. Supported formats: PNG, JPEG, WebP, HEIC, HEIF
4. Verify uploads appear in the chat input area via screenshot
```

### Step 4: Construct and Submit the Prompt

Build the prompt using the structured framework below, then type and submit it.

**Prompt Construction Formula:**

For text-to-image (no references):
```
[Subject] + [Action] + [Location/Context] + [Composition] + [Style]
```

For multimodal generation (with references):
```
[Reference images] + [Relationship instruction] + [New scenario]
```

**Include in the prompt when the user specifies:**

- **Resolution:** Append the desired resolution naturally, e.g. "Generate this in 4K resolution" or "Create a 2K image of..."
  - Available: 0.5K (512px), 1K, 2K, 4K
- **Aspect Ratio:** Specify the ratio, e.g. "in 16:9 aspect ratio"
  - Available: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:4, 4:1, 1:8, 8:1
- **Style:** Use photographic/cinematic language from the prompting guide

**Submitting:**
```
1. Use find to locate the prompt input field (textarea / chat input)
2. Type the constructed prompt using computer action "type"
3. Press Enter or click the send button via computer to submit
4. Wait for the image to generate (use computer wait action, 15-30 seconds typical, up to 60s for 4K)
5. Take a screenshot with computer to verify the image was generated
```

### Step 5: Download the Generated Image

```
1. Take a screenshot with computer to see the generated image
2. Hover over the generated image using computer action "hover" to reveal download controls
3. Look for "Download original size" / "Originalgröße herunterladen" button
   (appears top-right corner of the image on hover)
4. Click the download button with computer
5. Wait 3-5 seconds (computer wait action) for the download to complete
6. The file will be saved to the user's Downloads folder
```

### Step 6: Move the Downloaded File

```
1. Find the most recently downloaded file in the Downloads folder:
   ls -t ~/Downloads/ | head -5
2. Move the file to the user's specified destination using Bash:
   mv ~/Downloads/filename.png "/desired/destination/filename.png"
3. Report the final file location to the user
```

## Prompt Enhancement Guidelines

When the user provides a basic prompt, enhance it using these principles:

1. **Be specific:** Add concrete details on subject, lighting, composition
2. **Use positive framing:** Describe what you want, not what you don't want ("empty street" not "no cars")
3. **Control the camera:** Use photographic terms like "low angle", "aerial view", "macro lens"
4. **Start with a strong verb:** "Create", "Generate", "Design", "Photograph"
5. **Describe narratively:** Write scene descriptions, not keyword lists

**Lighting terms:** three-point softbox, chiaroscuro, golden hour backlighting, Rembrandt lighting
**Camera terms:** GoPro (distorted/immersive), Fujifilm (color science), macro lens (detail), wide-angle (scale)
**Film/color:** "1980s color film, slightly grainy", "cinematic muted teal tones", "high saturation editorial"
**Materiality:** Specify textures -- "navy blue tweed" not just "jacket", "ornate elven plate armor, etched with silver leaf" not just "armor"

**For text rendering in images:**
- Enclose text in quotes: "Happy Birthday"
- Specify font: "bold white sans-serif font" or "Century Gothic 12px"
- Supports 10+ languages for multilingual text

## Resolution and Aspect Ratio Quick Reference

| Resolution | Pixels | Best For |
|------------|--------|----------|
| 0.5K | ~512px | Quick drafts, thumbnails |
| 1K | ~1024px | Web use, social media |
| 2K | ~2048px | High-quality prints, presentations |
| 4K | ~4096px | Large prints, professional use |

| Aspect Ratio | Use Case |
|--------------|----------|
| 1:1 | Social media posts, profile pictures |
| 16:9 | Widescreen, YouTube thumbnails, presentations |
| 9:16 | Phone wallpapers, Instagram/TikTok stories |
| 3:2 | Photography standard |
| 4:3 | Classic display ratio |
| 21:9 | Ultra-wide, cinematic |
| 4:5 | Instagram portrait |
| 1:4 / 4:1 | Banners, panoramic |
| 1:8 / 8:1 | Extreme banners |

## Prompting Frameworks

For detailed prompting strategies covering all five frameworks (Image Generation, Image Editing, Real-Time Web Search, Text Rendering, Creative Direction), consult the bundled reference:

**Reference:** `references/prompting-guide.md` -- comprehensive prompting guide with examples for every framework

## Image Editing (Follow-up Prompts)

After generating an image, the user can request edits in the same chat:

- **Inpainting:** "Remove the person from the background" (semantic masking via text)
- **Style transfer:** "Recreate this in watercolor style"
- **Adding elements:** "Add a red umbrella to the scene"
- **Upscaling:** "Upscale this to 4K"

Be explicit about what to keep: "Keep everything else exactly the same, only change..."

## Error Handling

- If the page doesn't load: retry navigation, check internet connection
- If image generation fails: simplify the prompt, remove complex instructions
- If download button doesn't appear: try scrolling, hovering more precisely over the image
- If the file isn't in Downloads after 10 seconds: check with `ls -t ~/Downloads/ | head -5`
- If tools/image generation toggle isn't found: take a screenshot and look for alternative UI paths

## Notes

- All Gemini-generated images include C2PA Content Credentials and SynthID watermarks
- The models have a knowledge cutoff of January 2025 but can use real-time web search
- Maximum input: 131,072 tokens (Flash) / 65,536 tokens (Pro)
- Maximum output: 32,768 tokens for both models
- Supported input file types for references: PNG, JPEG, WebP, HEIC, HEIF
- PDF and text file inputs are also supported (up to 50MB)
