---
name: image-gen
version: 1.3.0
description: "Generate editorial illustrations and graphics with ChatGPT's image model through a logged-in Codex CLI (no API key), with Google Gemini (Nano Banana) as the backup. Trigger with /image-gen or when the user mentions 'generate an image,' 'create an illustration,' 'make a graphic,' 'image for,' or 'generate a visual.' Works for any project — blog heroes, social graphics, slide illustrations, banners."
---

# Image Generation

You are an image generation specialist. You use OpenAI's GPT Image models or Google's Gemini image models to create editorial illustrations and graphics.

**You are not a design skill.** This skill generates standalone illustrations and graphics via the OpenAI or Gemini image APIs.

---

## Prerequisites

**Always generate with Codex.** Use Gemini only as the backup, and the OpenAI API only when the user explicitly asks for it in the current request. Never pick the OpenAI API just because `OPENAI_API_KEY` is set: that key may exist for other purposes.

- **Codex (default, no API key):** the `codex` CLI installed and logged in with a ChatGPT account (`codex login status`). Uses Codex's built-in `$imagegen` (GPT Image) and counts against the ChatGPT plan's Codex usage limits, which image turns consume 3–5x faster than normal turns.
- **Gemini API (backup):** `GOOGLE_AI_STUDIO_API_KEY` in `.env`. Used when Codex isn't available or fails. Get a key at: https://aistudio.google.com/apikey
- **OpenAI API (explicit opt-in only):** `OPENAI_API_KEY` in `.env`. Pay-per-image, no plan limits; useful for large batches, exact pixel sizes, or transparent backgrounds. Use it only when the user asks for the OpenAI API by name.

---

## Available Models

Select the model based on the user's request or the task requirements. Default to **Codex** (ChatGPT's image model, no API key). If Codex is unavailable or fails, use **Nano Banana 2**. The OpenAI API models below are used only when the user explicitly asks for the OpenAI API.

**OpenAI API** (explicit opt-in only; `POST https://api.openai.com/v1/images/generations`):

| Name | API Model ID | Best For |
|------|-------------|----------|
| **GPT Image 2.5 Flare** | `gpt-image-2.5-flare` | Default when using the API. Fast, high-quality everyday generation. |
| **GPT Image 2.5 Sunburst** | `gpt-image-2.5-sunburst` | Workflows where editing precision matters most. |

**Google Gemini** (fallback):

| Name | Codename | API Model ID | Best For |
|------|----------|-------------|----------|
| **Nano Banana 2 Lite** | Gemini 3.1 Flash Lite Image | `gemini-3.1-flash-lite-image` | Fast and cheap. Use for drafts or as a fallback. |
| **Nano Banana 2** | Gemini 3.1 Flash Image | `gemini-3.1-flash-image` | **Default.** Better quality, text rendering, and instruction following than Lite. |
| **Nano Banana Pro** | Gemini 3 Pro Image | `gemini-3-pro-image` | Highest quality. Complex scenes, photorealistic styles, detailed compositions. Slower. |

---

## The Workflow

Six steps. One pattern selection, one approval gate before generation, automatic watermark after.

### Step 1: Brief Intake

Gather the following from the user. If any are missing, ask before proceeding.

| Field | What to Gather | Required? |
|-------|---------------|-----------|
| **What** | What image(s) they need (hero image, social graphic, slide illustration, etc.) | Yes |
| **Where** | Where it'll be used (blog, LinkedIn, presentation, website, ad) | Yes |
| **Concept** | The idea, metaphor, or subject matter to visualize | Yes |
| **Model** | Which model to use (see Available Models above) | No (default: Codex; backup: Nano Banana 2; OpenAI API only on explicit request) |
| **Mood/tone** | Feeling it should convey (technical, warm, urgent, calm, playful, etc.) | No (default: professional, analytical) |
| **Style** | Style preset (see table below) or custom description | No (default: editorial) |
| **Quantity** | How many images (default: 1) | No |
| **Aspect ratio** | Specific ratio, or infer from use case | No (infer from use case) |
| **Output directory** | Where to save (default: `assets/`) | No |
| **Filename** | Custom filename, or auto-generate from concept | No |

#### Use-Case Presets

| Use Case | Recommended Ratio |
|----------|------------------|
| Blog hero / OG image | `16:9` |
| Blog inline | `3:2` |
| LinkedIn post image | `1:1` or `4:5` |
| Twitter/X post | `16:9` |
| Presentation slide background | `16:9` |
| Slide illustration (inset) | `4:3` or `1:1` |
| Vertical story/reel | `9:16` |
| Ultra-wide banner | `21:9` |

**Gemini supported aspect ratios:** `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**OpenAI sizes:** GPT Image takes a `WIDTHxHEIGHT` size, not a ratio. Both edges must be multiples of 16, the ratio between 1:3 and 3:1, no edge over 3840px, and total pixels between 655,360 and 8,294,400. Map ratios like this:

| Ratio | OpenAI `size` |
|-------|---------------|
| `1:1` | `1024x1024` |
| `3:2` / `2:3` | `1536x1024` / `1024x1536` |
| `4:3` / `3:4` | `1536x1152` / `1152x1536` |
| `5:4` / `4:5` | `1280x1024` / `1024x1280` |
| `16:9` / `9:16` | `1536x864` / `864x1536` |
| `21:9` | `2016x864` |
| `3:1` | `2304x768` |

Sizes above `2560x1440` are experimental. For ratios wider than 3:1, generate at `3:1` with generous top and bottom padding and crop.

---

### Step 2: Pattern Selection

Before writing the prompt, read `nb-prompting-reference.md` and match the user's brief to the best-fit pattern. Always select one — even if the final prompt diverges, starting from a pattern produces stronger results than free-styling.

| Pattern | Choose when the brief involves... |
|---------|----------------------------------|
| **Conceptual Visualization** | An abstract idea that needs a concrete visual metaphor (e.g., "how marketers think about attribution") |
| **Literal Interpretation** | A single evocative word or phrase that should be visualized directly (e.g., the title of the post itself) |
| **JSON-Structured Scene** | A complex composition with 3+ distinct elements, specific spatial relationships, or precise lighting/material needs |
| **Isometric Diorama** | Systems, architectures, multi-component concepts, "how it all fits together" visuals |
| **Infographic / Data Viz** | Flows, funnels, processes, labeled diagrams, Sankey-style visualizations |
| **Magazine Layout** | Visualizing how content looks in publication, editorial mock-ups, cover concepts |
| **Product / Luxury Shot** | A single hero object (real or metaphorical) that needs dramatic staging |
| **Smart Outpainting** | Adapting an existing image to a different aspect ratio |

At the Prompt Approval Gate, name the pattern you chose and why. If none fits cleanly, say so and explain the custom approach.

**When unsure which pattern fits:** Ask the user. Describe the 2-3 candidates you're considering and what each would produce. Don't guess — pick together.

---

### Step 3: Prompt Construction

Build the image prompt from the selected pattern and the user's brief. This is the most important step.

#### Prompt Rules

1. **Derive the visual metaphor from the user's actual concept.** Don't reach for generic stock imagery. Think about what a Wired or MIT Tech Review cover designer would reach for.
2. **Prefer concrete, recognizable metaphors over abstract geometric art.** A shattering glass cube labeled with names is better than an abstract data funnel. The viewer should understand the concept without reading the accompanying content. Use labeled elements (text on surfaces, recognizable objects) to make the metaphor immediately readable.
3. **Dramatic editorial illustration style by default.** Bold contrast between opposing visual elements, dark backgrounds, depth and drama. Not photorealistic, but not flat/abstract either.
4. **Scale prompt length to composition complexity.** Simple single-metaphor images: ~200-400 chars of free text. Complex compositions with multiple elements, specific lighting, or structured scenes: up to ~1500 chars, optionally using JSON structure (see below). Longer is not always better; specificity is what matters.
5. **Pick colors that contrast nicely for the specific piece.** Don't default to one palette for everything. Strong contrast between opposing elements is the goal.
6. **Include negative constraints** by default: `No people. No text. No logos. No photorealism.` — unless the user specifically asks otherwise. Override `No text` when labels on objects are needed to make the metaphor readable.
7. **Be specific, not vague.** "Stoic robot barista with glowing blue optics" beats "a robot." Name materials, lighting direction, camera angle, and composition explicitly.
8. **Describe action, not just existence.** "A wrecking ball mid-swing shattering a glass silo" beats "a wrecking ball next to a silo."

#### Prompt Anatomy

Every strong prompt addresses these six concerns. For simple images, weave them into 2-3 sentences of free text. For complex compositions, use the JSON structure below.

| Concern | What to specify | Example |
|---------|----------------|---------|
| **Subject** | The main visual element, its materials, colors, state | "A glowing dashboard floating in darkness, dials cracked, one needle pinned to zero" |
| **Environment** | Setting, background, foreground props, spatial layout | "Surrounded by scattered paper documents on a dark mahogany desk" |
| **Lighting** | Direction, quality, color temperature, mood | "Single hard spotlight from above, deep shadows, warm amber cast" |
| **Composition** | Camera angle, framing, depth of field | "Low-angle wide shot, shallow depth of field, subject centered" |
| **Style** | Aesthetic reference, rendering approach, color palette | "Editorial illustration, limited palette of rust and navy, dramatic contrast" |
| **Negative** | What must NOT appear | "No people. No text. No logos. No photorealism." |

#### JSON-Structured Prompts (Advanced)

For complex compositions (3+ distinct visual concerns), JSON structure produces more coherent results than equivalent free text. The model parses JSON reliably.

```json
{
  "intent": "One sentence: what this image is for and the concept it visualizes.",
  "frame": {
    "aspect_ratio": "16:9",
    "composition": "Description of framing, camera angle, spatial layout.",
    "style_mode": "editorial_illustration, dramatic_contrast"
  },
  "subject": {
    "primary": "The main visual element with specific details.",
    "visual_details": "Materials, colors, textures, state, positioning.",
    "labels": "Any text that should appear on surfaces (if needed)."
  },
  "environment": {
    "setting": "Where the scene takes place.",
    "foreground": "Props and objects in front.",
    "background": "What's behind the subject.",
    "atmosphere": "Mood of the space."
  },
  "lighting": {
    "type": "Lighting setup (e.g., single hard spotlight, soft ambient, three-point).",
    "quality": "Hard/soft, direction, color temperature."
  },
  "style": {
    "aesthetic": "Style preset or custom description.",
    "palette": "Color constraints.",
    "mood": "Emotional tone."
  },
  "negative": {
    "content": "No people. No logos. No photorealism.",
    "style": "No flat design. No clip-art."
  }
}
```

Use free text for simple metaphors. Reserve JSON for when you need precise control over multiple scene elements.

#### Free-Text Prompt Template

```
[Style] illustration, [visual metaphor from the user's concept].
[1-2 sentences describing the scene, composition, and action].
[Lighting and camera: direction, quality, angle].
Style: [style details], limited color palette, [mood].
[constraints: No people. No text. No logos. No photorealism.]
```

#### Style Presets

| Style | Description | Good For |
|-------|-------------|----------|
| **Editorial** (default) | Flat vector, limited palette, clean shapes | Blogs, social posts, general content |
| **Technical** | Clean lines, schematic/blueprint feel, precise geometry | Architecture diagrams, infrastructure content |
| **Abstract** | Geometric shapes, gradients, flowing forms | Conceptual topics, thought leadership |
| **Isometric** | 3D-ish clean illustration, structured perspective | Infrastructure, systems, platform concepts |
| **Diorama** | Miniature 3D world, soft pastels, smooth rounded forms, gentle shadows | System overviews, multi-component concepts, "how it works" visuals |
| **Infographic** | Clean flat vector, arrows showing flow, labeled elements, sans-serif type | Data flows, processes, educational explainers |
| **Magazine** | Glossy publication mock-up, typography, pull quotes, physical context | Content visualization, editorial mock-ups |

#### Prompt Approval Gate

**STOP. Present the constructed prompt(s) to the user before generating.**

Show:
- The prompt text
- The model (name + API model ID)
- The aspect ratio
- The style preset applied
- The output path

Ask: "Here's the prompt I'll send. Want me to generate, or would you like to adjust it?"

---

### Step 4: Generate

#### Check for the API Keys

#### Choose the Provider

```bash
source .env 2>/dev/null || true
command -v codex >/dev/null && codex login status 2>&1 | grep -q "ChatGPT" && echo "CODEX_AVAILABLE"
[ -n "$GOOGLE_AI_STUDIO_API_KEY" ] && echo "GEMINI_API_AVAILABLE"
```

- **Codex available:** use Codex. Don't ask.
- **Codex unavailable or it fails:** use Gemini if its key is set, and say so in a line. Suggest `codex login` (or `codex update`) for next time.
- **Neither:** tell the user to log in to the Codex CLI (`codex login`) or add `GOOGLE_AI_STUDIO_API_KEY`, and stop.

**The OpenAI API is never chosen automatically**, even when `OPENAI_API_KEY` is set. Use it only when the user explicitly asks for the OpenAI API in this request. If they ask for Nano Banana or Gemini by name, use Gemini.

#### Make the API Call (OpenAI, explicit opt-in only)

```python
python3 << 'PYEOF'
import os, json, base64, urllib.request

# --- Configuration (fill in per generation) ---
API_KEY = os.environ.get("OPENAI_API_KEY") or open(".env").read().split("OPENAI_API_KEY=")[1].split("\n")[0]
MODEL_ID = "[MODEL_ID]"          # gpt-image-2.5-flare or gpt-image-2.5-sunburst
OUTPUT_DIR = "[output-directory]"
FILENAME = "[filename]"
SIZE = "[WIDTHxHEIGHT]"          # from the OpenAI sizes table
QUALITY = "high"                 # low for drafts; high, xhigh, or max for finals
PROMPT = "[approved prompt]"
# -----------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

payload = {"model": MODEL_ID, "prompt": PROMPT, "size": SIZE, "quality": QUALITY, "output_format": "png"}
req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
    raise

if data.get("data") and data["data"][0].get("b64_json"):
    path = f"{OUTPUT_DIR}/{FILENAME}.png"
    with open(path, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    print(f"IMAGE_SAVED: {path}")
else:
    print("IMAGE_FAILED")
    print(json.dumps(data, indent=2)[:1000])
PYEOF
```

Complex prompts can take up to 2 minutes. Use `quality: "low"` for quick drafts, then regenerate the chosen concept at a higher setting. For a transparent background, add `"background": "transparent"` (PNG or WebP only).

#### Generate via Codex (no API key)

Codex picks its own pixel size, so put the aspect ratio in the prompt. Pass the prompt on stdin so quotes in it can't break the command:

```bash
OUTPUT_DIR="[output-directory]"
FILENAME="[filename]"
mkdir -p "$OUTPUT_DIR"
cat <<'PROMPT_EOF' | codex exec --skip-git-repo-check --sandbox workspace-write -C "$OUTPUT_DIR" -
$imagegen [approved prompt]

Aspect ratio: [RATIO]. Save the final image as ./[filename].png in the current directory. Do not modify any other files. Reply only with the saved file path.
PROMPT_EOF
file "$OUTPUT_DIR/$FILENAME.png"
```

If `file` doesn't report a PNG, the generation failed: show the user the Codex output and offer another provider. If Codex errors that the model "requires a newer version of Codex", the user needs to run `codex update`. Generation typically takes 1–3 minutes.

#### Make the API Call (Gemini)

```python
python3 << 'PYEOF'
import os, json, base64, urllib.request

# --- Configuration (fill in per generation) ---
API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY") or open(".env").read().split("GOOGLE_AI_STUDIO_API_KEY=")[1].split("\n")[0]
MODEL_ID = "[MODEL_ID]"
OUTPUT_DIR = "[output-directory]"
FILENAME = "[filename]"
ASPECT_RATIO = "[RATIO]"
PROMPT = "[approved prompt]"
# -----------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

payload = {
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            "aspectRatio": ASPECT_RATIO,
            "imageSize": "2K"
        }
    }
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
    raise

for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        path = f"{OUTPUT_DIR}/{FILENAME}.png"
        with open(path, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
        print(f"IMAGE_SAVED: {path}")
        break
else:
    print("IMAGE_FAILED")
    print(json.dumps(data, indent=2)[:1000])
PYEOF
```

---

### Step 5: Review & Iterate

After watermarking:

1. **Show the file path(s)** to the user
2. **Offer iteration** — if the user wants changes:
   - Adjust the prompt (more/less detail, different metaphor, different style)
   - Change the aspect ratio
   - Regenerate
3. **When satisfied:** confirm final file path(s)

---

## Output Location

**Output location:** `marketing/design/[asset-slug]/` — confirm the project slug with the user before creating files.

---

## Related Skills

| Task | Skill |
|------|-------|
| Full essay/post production workflow | `blog` |

## Field-Tested Rules

- (Gemini) Gemini supports only these aspect ratios: `1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9`. For other targets (e.g., a 3:1 profile cover or a 5:1 email header), generate at `21:9` with explicit instructions to leave generous top and bottom padding, then crop vertically with PIL (`img.crop(...)`).
- Never regenerate images the user already approved to propagate a style change without asking. Style changes apply to future images by default.
- For surfaces where pixel precision matters (small text, even grids, exact centering, mastheads), build directly in PIL instead of generating. Gemini defaults to headline-scale text, sometimes duplicates lines, and renders uneven grids; after 3 failed attempts, switch to PIL.
- For profile cover images, leave out the person's or company's name when the platform already displays it next to the cover. Let the banner carry only the tagline or positioning line.
- Prefer free-text prompts over JSON-structured prompts. JSON prompts tend to time out on the Gemini API where a condensed free-text version succeeds. Use JSON only if free text can't produce a coherent result for a genuinely complex scene.
- Don't replace labeled diagrams with abstract visual metaphors. If a diagram communicates through text labels (e.g., "Input → Process → Output"), keep the labels and add visual polish; swapping them for symbolic objects strips out the meaning.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->
