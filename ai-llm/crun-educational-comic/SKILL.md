---
name: crun-educational-comic
description: Generate multi-panel educational comics, science explanatory cartoon strips, infographic storyboards, concept illustration strips, and step-by-step teaching comics using Crun AI image models and automated panel stitching. Use whenever the user asks for an educational comic, science/tech concept comic, explanatory cartoon, teaching storyboard, multi-panel knowledge strip, infographic illustration, or wants to turn any topic, concept, historical event, physics/math problem, coding logic, or story into a visual comic strip — even if they don't explicitly say "Crun" or "comic".
---

# Crun Educational Comic & Storyboard Generator

Use this skill to transform complex educational concepts, science principles, history, coding logic, business models, or user-provided scripts into high-quality, multi-panel educational comic strips with consistent visual styles, characters, title banners, and clean dialogue captions.

- **Educational Topic Deconstruction**: Deconstruct complex knowledge into a structured 3–6 panel comic narrative (Hook ➔ Breakdown ➔ Metaphor/Analogy ➔ Summary/Takeaway).
- **Visual & Character Consistency**: Enforce consistent recurring educational characters (e.g. *Professor Owl & Curious Leo*, *Dr. Byte & Apprentice Sam*, or custom user characters) and distinct art styles (*2D Flat Educational Vector*, *Infographic Manga*, *Hand-drawn Blackboard Sketch*, *Retro Comic Book*).
- **Pure Visual AI Prompting**: Construct visual prompts for Crun T2I/I2I image models in clear English (bypassing AI text rendering errors inside image models).
- **Interactive Button Confirmation**: Present complete comic breakdown (panel prompts, style, model, and credit estimate) via `ask_question` tool before task creation.
- **Automated Canvas Stitching & Captioning**: Post-process panel images using `skills/scenarios/crun-educational-comic/scripts/stitch_comic_panels.py` to produce a composite comic grid (2x2, 1x4, 2x3, etc.) featuring title banners, panel numbers, and crisp dialogue callouts in the user's language.

---

## Workflow Overview

Follow this end-to-end execution flow for all educational comic requests:

```text
User Request (Topic / Concept / Script)
   │
   ├── 1. Educational Narrative Breakdown (3–6 Panels)
   │       ├─ Establish Character Cast & Visual Style Preset
   │       └─ Structure Panels: Hook -> Concept -> Metaphor -> Summary
   │
   ├── 2. Upload Reference Media (If user provides reference character/photo)
   │       └─ python <root>/runtime/crun_cli.py upload <local-file>
   │
   ├── 3. Route Model & Construct Visual Prompts
   │       ├─ Modality: "image", Operation: "text-to-image" or "image-edit"
   │       ├─ Models: openai/gpt-image-2, bytedance/seedream-5-pro, google/nano-banana-pro
   │       └─ English visual prompts maintaining character & lighting anchors
   │
   ├── 4. Estimate Affordability & Present Button Confirmation
   │       ├─ Estimate: python <root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
   │       └─ Ask Question: Single-select buttons (Style, Panels, Captions, Model & Credits)
   │
   ├── 5. Batch Create Tasks & Poll Status (crun-task-runner)
   │       ├─ python <root>/runtime/crun_cli.py task create --model <model> --input-file <input.json>
   │       └─ python <root>/runtime/crun_cli.py task wait --task-id <task_id>
   │
   └── 6. Multi-Panel Stitching & Caption Overlay
           └─ python <skill-root>/skills/scenarios/crun-educational-comic/scripts/stitch_comic_panels.py <panel_paths...> \
                --title "<Comic_Title>" --captions "<Caption_1>" "<Caption_2>" ... --grid <2x2|1x4|2x3> -o <output.png>
```

---

## Detailed Execution Steps

### 1. Educational Narrative & Character Breakdown

Deconstruct the user's topic or request across three core structural dimensions:

#### A) Narrative Structure (3 to 6 Panels)
- **Panel 1: The Hook / Curiosity Gap**: Introduce a relatable question, common misconception, or intriguing scenario.
- **Panel 2: The Core Concept / Mechanism**: Reveal the underlying principle, scientific law, or system architecture.
- **Panel 3: The Metaphor / Visual Analogy**: Use a vivid real-world analogy (e.g. comparing computer memory to a desk, or gravity to a curved trampoline).
- **Panel 4: Summary / Actionable Takeaway**: Conclude with a clear, memorable takeaway or punchline.

#### B) Educational Character Presets
Maintain consistent characters across panel prompts by incorporating key visual anchors:
- **Professor & Student**: *"Dr. Owl, a wise anthropomorphic owl in a white lab coat with round glasses, and Leo, an eager young rabbit boy with a blue hoodie."*
- **Tech Mentor & Apprentice**: *"Dr. Byte, a friendly futuristic robot with glowing cyan eyes, and Sam, a curious young programmer girl with orange hair."*
- **Custom / Historical Characters**: Define exact hair color, clothing, face structure, and accessories, repeating these descriptions in every panel prompt.

#### C) Visual Style Presets
Explicitly specify one of the following style presets in panel prompts:
1. `2D Flat Educational Vector`: Clean line art, vibrant flat colors, modern infographic style, high readability.
2. `Infographic Manga`: Japanese anime/manga comic style, expressive facial reactions, speed lines, high energy.
3. `Hand-drawn Blackboard Sketch`: Colored chalk illustration on dark blackboard background, educational classroom feel.
4. `Retro Vintage Comic`: Pop-art halftone dot texture, classic western comic book aesthetic.

---

### 2. Upload Reference Media (If Provided)

When the user provides a custom character drawing, diagram, or photo:

```bash
python <skill-root>/runtime/crun_cli.py upload <local-file>
```

Use the returned `file_url` in Crun image-edit model payloads (`operation: "image-edit"`).

---

### 3. Route Model and Build Visual Prompts

Read `skills/crun-model-router/SKILL.md` to select image models:

- **Preferred Models**: `openai/gpt-image-2`, `bytedance/seedream-5-pro`, `google/nano-banana-pro`, `qwen-image-2.0-pro`.
- **Resolution & Aspect Ratio**:
  - Individual panels default to 1:1 square (`1024x1024` or `1K`).
- **Prompt Formula**:
  ```text
  [Style Preset] + [Character Visual Anchors] + [Panel Scene Action & Expression] + [Background & Props] + [Lighting & Composition] + "clean lighting, high quality educational comic panel, no text"
  ```
- **Text Rendering Rule**: Do NOT request AI image models to render dialogue text or CJK words inside the image prompt. Keep prompts purely visual. Text dialogues will be cleanly rendered via post-processing script.

---

### 4. Estimate Affordability & Button Confirmation Gate

Read `skills/crun-account-credits/SKILL.md`:

```bash
python <skill-root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Verify `affordable: true`. Before task creation, **call `ask_question` tool to present an interactive choice modal with confirmation buttons**.

#### Mandatory Confirmation Specification:
- **Title**: e.g., `"Educational Comic: Newton's Third Law"`
- **Total Panels**: e.g., `4 Panels (2x2 Grid)`
- **Visual Style**: e.g., `2D Flat Educational Vector`
- **Characters**: e.g., `Dr. Owl & Apprentice Leo`
- **Panel Dialogue Breakdown**:
  - Panel 1: *"Dr. Owl: Every action has an equal and opposite reaction!"*
  - Panel 2: *"Leo: Like pushing against a wall?"*
  - Panel 3: *"Dr. Owl: Exactly! And rocket propulsion works the same way."*
  - Panel 4: *"Leo: Wow, physics makes sense now!"*
- **Model & Total Credits**: e.g., `bytedance/seedream-5-pro (4 panels x 2.5 = 10.0 Credits total)`

#### Interactive Buttons (`ask_question`):
- Option 1: `"Confirm & Generate Comic"` (or `"确认生成教育漫画"`)
- Option 2: `"Modify Script/Style"` (or `"修改脚本或画风"`)
- Option 3: `"Cancel"` (or `"取消"`)

---

### 5. Task Creation & Panel Batching

Read `skills/crun-task-runner/SKILL.md`. Create a task for each panel and poll status until complete:

```bash
python <skill-root>/runtime/crun_cli.py task create --model <model> --input-file <panel_1.json>
python <skill-root>/runtime/crun_cli.py task wait --task-id <task_id_1>
```

Collect all downloaded panel image file paths: `[panel_1.png, panel_2.png, panel_3.png, panel_4.png]`.

---

### 6. Multi-Panel Stitching & Post-Processing

Invoke `stitch_comic_panels.py` to assemble the downloaded panel images into a unified comic layout with title header and text captions:

```bash
python <skill-root>/skills/scenarios/crun-educational-comic/scripts/stitch_comic_panels.py \
  <panel_1.png> <panel_2.png> <panel_3.png> <panel_4.png> \
  --title "<Comic_Title>" \
  --captions "<Caption_1>" "<Caption_2>" "<Caption_3>" "<Caption_4>" \
  --grid 2x2 \
  --output <output_comic_path.png>
```

#### Script Parameters:
- `images`: Space-separated list of downloaded panel image paths.
- `--title`: Title header banner text.
- `--captions`: Captions/dialogues in exact panel order (supports CJK & multilingual automatic line wrapping).
- `--grid`: Layout grid (`2x2`, `1x4` vertical, `2x3`, or `auto`).
- `--output` / `-o`: Output path for stitched comic image (`.png`).

---

## Delivery and Preview

Always deliver the final result with execution details and an inline local markdown preview:

```text
✅ Educational Comic Generated Successfully!
- Topic Title: <title>
- Total Panels: <panel_count> (<grid_layout>)
- Visual Style: <style_preset>
- Model Used: <model>
- Credits Used: <total_credits>
- File Path: <local_output_path>

![Educational Comic Preview](/absolute/path/to/comic_output.png)
```

---

## Canonical User Scenarios & Exemplar Breakdowns

### Scenario 1: 4-Panel Physics Comic ("Newton's Third Law")

- **Input Intent**: "Draw a 4-panel comic explaining Newton's Third Law for middle school students."
- **Visual Style Preset**: `2D Flat Educational Vector`
- **Characters**: Dr. Owl (lab coat, glasses) & Student Leo (rabbit boy, blue hoodie).
- **Panel Structure**:
  1. Panel 1: Dr. Owl introducing the concept ("Action = Reaction").
  2. Panel 2: Leo jumping off a skateboard, pushing the skateboard backward.
  3. Panel 3: Rocket ship jetting exhaust gas downward while flying upward.
  4. Panel 4: Leo & Dr. Owl high-fiving ("Physics is everywhere!").
- **Stitching Command**:
  ```bash
  python skills/scenarios/crun-educational-comic/scripts/stitch_comic_panels.py \
    panel_1.png panel_2.png panel_3.png panel_4.png \
    --title "Science Comic: Newton's Third Law" \
    --captions "Dr. Owl: For every action, there is an equal and opposite reaction!" \
               "Leo: When I jump forward, my feet push the skateboard backward!" \
               "Dr. Owl: Exactly! Space rockets fly by pushing hot gas downward." \
               "Leo: Cool! Action and reaction are everywhere in life!" \
    --grid 2x2 \
    -o output_newton_comic.png
  ```

---

### Scenario 2: 3-Panel Coding Comic ("How Git Branching Works")

- **Input Intent**: "Make an educational comic explaining Git branches vs main line."
- **Visual Style Preset**: `Infographic Manga`
- **Characters**: Dr. Byte (friendly robot) & Sam (girl programmer).
- **Panel Structure**:
  1. Panel 1: Sam worried about breaking production code on `main`.
  2. Panel 2: Dr. Byte demonstrating creating a parallel feature branch like a parallel universe track.
  3. Panel 3: Safely merging the tested feature branch back into `main`.
- **Stitching Command**:
  ```bash
  python skills/scenarios/crun-educational-comic/scripts/stitch_comic_panels.py \
    panel_1.png panel_2.png panel_3.png \
    --title "Tech Comic: Understanding Git Branching" \
    --captions "Sam: I'm scared to test new code directly on the production main branch!" \
               "Dr. Byte: Create a Git Branch! It's like a safe parallel universe to experiment." \
               "Sam: Once it works, I merge it back cleanly. No risk at all!" \
    --grid 3x1 \
    -o output_git_comic.png
  ```
