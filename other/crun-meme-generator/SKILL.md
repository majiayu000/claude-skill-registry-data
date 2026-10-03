---
name: crun-meme-generator
description: Generate static image memes/stickers and animated GIF memes/reaction emojis using Crun image and video models. Use whenever the user asks for a meme, sticker, reaction emoji, static meme, animated GIF, reaction GIF, funny reaction animation, or requests adding text/stickers to images or converting short generated videos into GIF memes — even if they don't explicitly say "Crun".
---

# Crun Meme & Emoji Generator

Use this skill to generate static image memes/stickers and animated GIF reaction memes via Crun AI models.

- **Static Memes**: Route to Crun image generation models (`modality: "image"`), set appropriate resolution/aspect ratio, generate pure artwork (bypassing AI text rendering errors), download PNG/JPG, and overlay crisp text via `scripts/image_text_overlay.py --text "<caption_text>"`.
- **Animated GIF Memes**: Route to fast Crun video generation models (`modality: "video"`), default to the model's **lowest resolution** (e.g. `480p` / `720p`), generate pure visual motion (without asking video AI model to render text directly to avoid text distortion/garbling), download MP4, and add crisp text overlay directly onto the GIF via `scripts/video_to_gif.py --text "<caption_text>"`.
- **Interactive Button Confirmation**: For both static and GIF memes, always present confirmation details (including Model, Credits, Visual Style, Text Caption, and Resolution) and use **interactive option buttons** (e.g. `ask_question` tool) for user confirmation before task creation.

---

## Workflow Overview

Follow this end-to-end execution flow for all meme and emoji generation requests:

```text
User Request (Meme/Emoji/GIF)
   │
   ├── 1. Determine Format (Static Image vs Animated GIF)
   │
   ├── 2. Upload Input Media (If user provides reference photo/image)
   │       └─ python <root>/runtime/crun_cli.py upload <local-file>
   │
   ├── 3. Route Model & Construct Payload
   │       ├─ Static Image: modality="image", define Visual Style, resolution=1K, purely visual prompt
   │       └─ Animated GIF: modality="video", lowest resolution default, purely visual motion prompt
   │
   ├── 4. Estimate Affordability & Present Button Confirmation
   │       ├─ Estimate: python <root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
   │       └─ Ask Question: Interactive option buttons (containing Style, Caption, Resolution, Model & Credits)
   │
   ├── 5. Create Task & Poll Status (crun-task-runner)
   │       ├─ python <root>/runtime/crun_cli.py task create --model <model> --input-file <input.json>
   │       └─ python <root>/runtime/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
   │
   └── 6. Final Text Overlay & Output Formatting
           ├─ Static Image: python <skill-root>/skills/scenarios/crun-meme-generator/scripts/image_text_overlay.py <image-path> --text "<caption_text>" --output <meme-path>
           └─ Animated GIF: python <skill-root>/skills/scenarios/crun-meme-generator/scripts/video_to_gif.py <video-path> --text "<caption_text>" --output <gif-path>
```

---

## Detailed Execution Steps

### 1. Identify Format and Intent

- **Static Image Meme**:
  - User intent: Static sticker, image meme, funny reaction photo, graphic meme.
  - Output target: PNG / JPG image file.
  - Operation: `text-to-image` (new meme) or `image-edit` (modifying or adding caption to an existing photo).

- **Animated GIF Meme**:
  - User intent: Animated GIF meme, reaction GIF, motion sticker, animated reaction emoji.
  - Output target: GIF file.
  - Operation: `text-to-video` (new animated GIF) or `image-to-video` (animating a reference photo into a GIF).

---

### 2. Upload Reference Media (If Provided)

When the user provides a local reference photo (e.g. face photo, pet photo, existing image to turn into meme/GIF):

```text
python <skill-root>/runtime/crun_cli.py upload <local-file>
```

Use the returned `file_url` in the model payload. Never send raw local paths or Base64 into Crun model inputs.

---

### 3. Route Model and Build Payload

Read `skills/crun-model-router/SKILL.md` to construct routing intent:

```json
{
  "modality": "image|video",
  "operation": "text-to-image|image-edit|text-to-video|image-to-video",
  "quality": "balanced",
  "speed": "fast"
}
```

#### A) Static Image Meme Defaults & Text Overlay Strategy
- Preferred models: `openai/gpt-image-2`, `bytedance/seedream-5-pro`, `google/nano-banana-pro`, `qwen-image-2.0-pro`.
- **Visual Style**: Explicitly choose or confirm a visual style:
  - Examples: `3D Cartoon Sticker` (white die-cut border), `Realistic Reaction Photo`, `Funny Sketch/Doodle`, `Anime Reaction`, `Pixel Art Meme`.
  - Include style details in the prompt (e.g. `"cute 3D cartoon style sticker with white outline..."`).
- **Resolution & Aspect Ratio**:
  - Default to square `1:1` aspect ratio or `1K` resolution suitable for memes.
- **Text Overlay Strategy**:
  - **Do NOT rely on AI image model prompt text rendering** for complex, multi-line, or CJK text, as image models often distort typography or misspell words.
  - Keep the image prompt focused on pure visual character and expression (e.g. `"cute 3D cartoon dog looking confused with big eyes, white die-cut sticker outline, solid background"`).
  - Use `scripts/image_text_overlay.py` post-processing to overlay crisp, stroke-bordered text onto the generated image.

#### B) Animated GIF Meme Defaults & Text Overlay Strategy
- Preferred fast video models: `bytedance/seedance2-0-fast-t2v` / `bytedance/seedance2-0-fast-i2v`, `bytedance/seedance1-0-pro-fast-t2v`, `vidu/q3-turbo-t2v`, `kling/v3-turbo`.
- **Lowest Resolution Default**:
  - Inspect model schema with `crun_cli.py models describe --model <model>`.
  - **Always select the lowest resolution supported by that model** (e.g. `480p` or `720p`). Lower resolution generates faster, uses fewer credits, and reduces GIF file size.
- **Text Overlay Strategy**:
  - **Do NOT ask video AI models to render text inside the prompt** (video models scramble CJK and English text).
  - Keep video AI prompt purely visual (e.g. `"cute 3D cartoon cat looking shocked, funny looping reaction motion, clean background"`).
  - Pass the text caption to `video_to_gif.py` via `--text "<caption_text>"`.

#### C) Universal Multilingual Adaptation Strategy
- **Text Caption & Modal Language**: Dynamically mirror the user's input language for text captions and confirmation dialogs.
  - If user inputs in **English**: Caption & confirmation must be in English (e.g. `"Monday Mood"`, `"Off to work..."`).
  - If user inputs in **Chinese**: Caption & confirmation in Chinese (e.g. `"摸鱼中..."`, `"收到！"`).
  - If user inputs in **Other Languages** (Japanese, Spanish, French, Korean, etc.): Natively generate the caption in that input language.
- **AI Model Prompt Language**: Always convert the underlying visual scene description in Crun model payloads into **clear English**, as AI image/video models deliver optimal rendering quality with English visual descriptions.

---

### 4. Estimate Affordability & Button Confirmation Gate

Read `skills/crun-account-credits/SKILL.md`:

```text
python <skill-root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Verify `affordable: true`. Before calling `task create`, **call `ask_question` tool to present an interactive choice modal with confirmation buttons**.

#### Mandatory Confirmation Content Specification:

1. **For Static Image Memes**:
   - **Model**: e.g. `bytedance/seedream-5-pro`
   - **Estimated Credits**: e.g. `2.5 Credits`
   - **Visual Style**: e.g. `3D Cartoon Sticker (with white outline)`
   - **Text Caption**: e.g. `"Monday Mood"` (Clean stroke text overlay applied after image generation)
   - **Resolution & Aspect Ratio**: e.g. `1K (1:1 Square)`

2. **For Animated GIF Memes**:
   - **Model**: e.g. `bytedance/seedance2-0-fast-t2v`
   - **Estimated Credits**: e.g. `4.0 Credits`
   - **Visual Style**: e.g. `3D Cartoon Reaction Style`
   - **Text Caption**: e.g. `"Off to work..."` (Stroke text overlay applied during GIF conversion)
   - **Resolution**: e.g. `480p` (Lowest model resolution, fast & cost-efficient)
   - **Duration**: e.g. `3s` (Converted to 12fps looping GIF)

#### Interactive Confirmation Buttons:
Use `ask_question` tool to prompt the user with selectable options in their language:
- Option 1: `"Confirm & Generate"` (or `"确认按此参数生成"`)
- Option 2: `"Modify Caption/Style"` (or `"修改配文或风格"`)
- Option 3: `"Cancel"` (or `"取消生成"`)

---

### 5. Create Task and Wait for Download

Read `skills/crun-task-runner/SKILL.md`:

```text
python <skill-root>/runtime/crun_cli.py task create --model <model> --input-file <input.json>
python <skill-root>/runtime/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
```

When task completes, `crun_cli.py` automatically downloads the result media to `~/.crun/output/yyyy-mm-dd/<task_id>/`.

---

### 6. Text Overlay & Format Output

#### A) Static Image Text Overlay (`image_text_overlay.py`)
Invoke `image_text_overlay.py` to overlay text onto the static image:

```text
python <skill-root>/skills/scenarios/crun-meme-generator/scripts/image_text_overlay.py <image-path> --output <meme-path> --text "<caption_text>" --text-position bottom --style stroke
```

**Parameters for `image_text_overlay.py`**:
- `<image-path>`: Path to the downloaded image file.
- `--output` / `-o`: Output path for captioned meme image (`.png` / `.jpg`).
- `--text` / `-t`: Text caption to overlay (supports CJK & multi-language stroke text).
- `--text-position`: Position of caption overlay (`bottom`, `top`, or `center`).
- `--style`: Text style (`stroke` white text with black outline, or `banner` dark background bar).

The script returns JSON output:
```json
{
  "code": 0,
  "status": "success",
  "input_file": "/path/to/image.png",
  "output_file": "/path/to/meme.png",
  "width": 1024,
  "height": 1024,
  "text_overlay": "Monday Mood",
  "text_position": "bottom",
  "style": "stroke"
}
```

#### B) Video to Animated GIF Conversion (`video_to_gif.py`)
Invoke `video_to_gif.py` to convert MP4 to GIF and overlay text:

```text
python <skill-root>/skills/scenarios/crun-meme-generator/scripts/video_to_gif.py <video-path> --output <gif-path> --fps 12 --width 480 --text "<caption_text>" --text-position bottom
```

**Parameters for `video_to_gif.py`**:
- `<video-path>`: Path to the downloaded MP4 video file.
- `--output` / `-o`: Output path for the converted `.gif` file.
- `--fps`: Target frame rate (default: `12`).
- `--width`: Target width scaling in pixels (default: `480`).
- `--text` / `-t`: Text caption to overlay.
- `--text-position`: Position of caption overlay (`bottom`, `top`, or `center`).

The script returns JSON output:
```json
{
  "code": 0,
  "status": "success",
  "input_file": "/path/to/video.mp4",
  "output_file": "/path/to/meme.gif",
  "size_bytes": 1425600,
  "fps": 12,
  "width": 480,
  "text_overlay": "Off to work...",
  "text_position": "bottom",
  "conversion_method": "ffmpeg+PIL"
}
```

---

## Confirmation Message & Button Examples

### Example 1: Static Image Meme Confirmation (`ask_question`)
```json
{
  "questions": [
    {
      "question": "🎨 Static meme generation plan prepared for your request:\n- Model: bytedance/seedream-5-pro\n- Visual Style: 3D Cartoon Sticker (white die-cut outline)\n- Text Caption: \"Monday Mood\" (Clean stroke text overlay)\n- Resolution: 1K (1:1 Square)\n- Estimated Cost: 2.5 Credits",
      "options": [
        "Confirm & Generate",
        "Modify Caption/Style",
        "Cancel"
      ],
      "is_multi_select": false
    }
  ]
}
```

### Example 2: Animated GIF Meme Confirmation (`ask_question`)
```json
{
  "questions": [
    {
      "question": "🎬 Animated GIF meme generation plan prepared for your request:\n- Model: bytedance/seedance2-0-fast-t2v\n- Visual Style: 3D cartoon humor reaction style\n- Text Caption: \"Off to work...\" (Clean stroke text overlay)\n- Resolution: 480p (Lowest model resolution, fast & cost-efficient)\n- Duration: 3 seconds (12fps looping GIF)\n- Estimated Cost: 4.0 Credits",
      "options": [
        "Confirm & Generate",
        "Modify Caption/Style",
        "Cancel"
      ],
      "is_multi_select": false
    }
  ]
}
```

---

## Delivery and Preview

Always provide the user with clear execution details and an inline local markdown preview:

```text
✅ Meme generated successfully!
- Task ID: <task_id>
- Visual Style: <style>
- Text Caption: <caption_or_none>
- Resolution: <resolution>
- Credits Used: <credits>
- File Path: <local_gif_or_image_path>

![Meme Preview](/absolute/path/to/meme.gif)
```
