---
name: crun-character-reference
description: Generate character reference sheets (nine-grid pose sheets, turnarounds, expression sheets, design sheets, hero portraits) from either an uploaded reference image or a text description. Use whenever the user asks for a character reference, character sheet, turnaround / multi-view, pose grid, nine-grid, expression sheet, or character design reference — even without naming Crun or a model. Searches trending formats/styles online and lets the user pick before generation.
---

# Crun Character Reference Generator

Use this skill to produce character reference artwork through Crun image models. It handles two entry paths — with a source image and without — and always finishes by returning the result file, selected model, and credits spent.

Use `../../../runtime/crun_cli.py`, `../../../catalog/models.json`, and the shared child skills:

- `../../crun-model-router/SKILL.md` — model routing & live schema inspection
- `../../crun-account-credits/SKILL.md` — balance & affordability estimation
- `../../crun-task-runner/SKILL.md` — task creation, monitoring, recovery, result delivery (the authority)

## Trigger

Activate for any of: character reference, character sheet, turnaround, multi-view, pose grid, nine-grid / 9-grid, expression sheet, emotion sheet, character design sheet, OC reference, 设定图, 角色参考, 三视图, 九宫格, 表情集设定, 立绘 — even if the user never says "Crun" or a model name.

## Entry path decision

1. Inspect the current conversation for an attached or linked source image.
   - **Image present** → follow Path A (image-driven).
   - **No image** → follow Path B (text-driven).
2. Treat only resources visibly attached or explicitly linked in the current conversation as source material. A new session starts with no source material, even if prior sessions, chat history, tool traces, or generated JSON mention a media URL or local path. Never reconstruct or infer a task input from historical JSON.

## Path A — source image provided

### A1. Upload the source

```text
python <root>/runtime/crun_cli.py upload <local-file>
```

Reuse an existing Crun resource URL directly. Never send Base64, data URIs, or local paths in a task input.

### A2. Resolve the format

- If the user already named a format in the original request (e.g. "九宫格", "三视图", "expression sheet"), use it directly and skip the search.
- Otherwise, search the web for trending character-reference formats and distill **three** concrete options. Use queries such as:
  - `热门角色参考图格式 九宫格 三视图 表情集`
  - `trending character sheet formats 2025 pose grid turnaround expression sheet`

  Build three option cards, each with: format name, a one-line description, an example use, and the model it will route to.

Present the three formats via interactive option buttons (use the `AskUserQuestion` tool) and let the user pick exactly one. Mirror the user's language for all labels and descriptions.

### A3. Pick model & build payload (image-driven → `image-edit`)

The operation is `image-edit` — the goal is to keep character identity from the source while producing the chosen layout. Select the model by format from the table in "Format → model & prompt" below. Every image-edit candidate must have `supports_reference: true` in the catalog.

After choosing, inspect the live schema:

```text
python <root>/runtime/crun_cli.py models describe --model <model>
```

Construct only fields the schema permits. Put the uploaded `file_url` into the reference-image field the schema defines (commonly `image`, `img_urls`, or `reference_image` — confirm from the live schema, never guess).

## Path B — no source image (text-driven)

### B1. Resolve style / gender / format online

Search the web for currently trending character styles, common gender options, and reference formats. Use queries such as:

- `热门角色风格 2025 赛博朋克 国风 二次元`
- `trending character art styles 2025`
- `character reference sheet popular layouts`

Distill the results into choice groups and present them via interactive option buttons (`AskUserQuestion`):

1. **Style** — three trending styles (for example 赛博朋克 / 国风仙侠 / 日系二次元).
2. **Gender** — at least male / female; add neutral or other culturally relevant options when appropriate.
3. **Format** — three formats (for example 九宫格 / 三视图 / 表情集).

If the user already stated a style, gender, or format in the original request, preselect it and only ask for the groups that remain undecided. Mirror the user's language.

### B2. Build the character prompt & pick model (text-driven → `text-to-image`)

Compose a clear **English** visual description from the chosen style + gender + any details the user added, then apply the format prompt template (see below). The operation is `text-to-image`. Select the model by format from the table.

## Format → model & prompt

Pick the model from the table by format. The operation column assumes the entry path; if a chosen model does not support the needed operation, fall back to `../../crun-model-router/SKILL.md`.

| Format | Layout | Aspect / resolution | Preferred models (text-to-image) | Preferred models (image-edit, needs `supports_reference`) |
|---|---|---|---|---|
| Nine-grid pose sheet 九宫格 | 3×3 grid, 9 poses/expressions | 1:1, 2k | `bytedance/seedream-5-pro`, `openai/gpt-image-2` | `bytedance/seedream-5-pro`, `openai/gpt-image-2` |
| Turnaround / multi-view 三视图 | front + side + back, side by side | 16:9, 2k | `openai/gpt-image-2`, `google/nano-banana-pro` | `bytedance/seedream-5-pro`, `openai/gpt-image-2` |
| Expression sheet 表情集 | grid of headshots, varied emotions | 1:1, 2k | `bytedance/seedream-5-pro`, `qwen-image-2.0-pro` | `bytedance/seedream-5-pro`, `openai/gpt-image-2` |
| Design sheet 设定表 | annotated refs, color palette | 3:2, 2k | `openai/gpt-image-2` (handles short text labels) | `openai/gpt-image-2` |
| Hero portrait 单张立绘 | single full-body key art | 3:4 or 9:16, 2k | `google/nano-banana-pro`, `bytedance/seedream-5-pro` | `bytedance/seedream-5-pro` |

Prompt templates — fill `[CHAR]` with the English character description; keep the structural English verbatim, because image models render multi-panel layouts most reliably from English:

- **Nine-grid**: `A 3x3 grid character reference sheet of [CHAR]. Nine equal panels in a 3 by 3 layout with thin dividing lines, each panel showing the same character in a different pose and expression. Clean white background. Consistent character design across all panels.`
- **Turnaround**: `Character turnaround reference sheet of [CHAR]. Three full-body views side by side: front view, side view, back view. Even spacing, consistent proportions, plain background, professional character design reference.`
- **Expression sheet**: `Expression sheet of [CHAR]. Multiple head-and-shoulder shots arranged in a grid, each showing a different emotion: happy, angry, sad, surprised, neutral, laughing, serious, shy, confused. Consistent character design, clean background.`
- **Design sheet**: `Character design sheet of [CHAR]. Multiple views plus detail callouts, a color palette with swatches, and short text labels. Professional concept-art layout, clean background.`
- **Hero portrait**: `Full-body character key art of [CHAR]. Dynamic pose, dramatic lighting, detailed costume, clean background, high-quality illustration.`

Do not ask the image model to render long CJK text inside the artwork. For the design sheet, prefer models that handle short labels (`openai/gpt-image-2`) and keep labels minimal. If the user wants a caption or watermark on the final image, overlay it in post-processing rather than relying on the model.

## Estimate & confirm

Read `../../crun-account-credits/SKILL.md`. Estimate the final model and exact input before creating any task:

```text
python <root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Require `affordable: true`. Because the model was chosen by this skill (not explicitly named by the user), present a confirmation summary with model, format, style/gender (when relevant), aspect/resolution, and estimated credits, then wait for explicit OK via interactive buttons before spending. Do not treat the earlier format/style selection as the spend confirmation.

## Create & deliver

Read `../../crun-task-runner/SKILL.md` for the authoritative execution rules. Create once, capture `task_id`, and poll in short resumable rounds:

```text
python <root>/runtime/crun_cli.py task create --model <model> --input-file <input.json>
python <root>/runtime/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
```

Follow `crun-task-runner` for all timeout, failure, and recovery rules. `CreateTask` charges credits and is never retried automatically.

## Delivery format

Return a localized summary plus the normalized fields. The result, model, and credits spent are mandatory in every delivery:

```text
✅ Character reference generated!
- Task ID: <task_id>
- Format: <format>
- Model: <model>
- Credits Used: <credits>
- File Path: <local_image_path>

![Character Reference](/absolute/path/to/file.png)
```

Prefer the local media path. Where the client renders inline media, preview the image with an absolute forward-slash path. Use the remote URL only as a fallback and identify any download error instead of claiming a failed download is local.

## Localization

Write every user-facing string — search-result option cards, interactive buttons, confirmation summary, progress updates, errors, and the final delivery — in the user's language. Keep API field names, model IDs, task IDs, numeric values, file paths, and the structural English of the prompt templates unchanged.
