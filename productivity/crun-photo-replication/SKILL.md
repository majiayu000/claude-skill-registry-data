---
name: crun-photo-replication
description: Replicate, restyle, or remake photos (portrait recreation, photo remake, vintage photo restoration/HD remake, pose & scene clone, style restyle) from an uploaded source photo or a text description. Use whenever the user asks for photo replication, photo recreation, photo remake, photo restyle, old photo HD remake, classic photo clone, or style restyle — even without naming Crun or a model.
---

# Crun Photo Replication & Restyle Generator

Use this skill to replicate, restyle, or remake photos through Crun image models. It handles two entry paths — with a source photo and without — and always finishes by returning the result file, selected model, and credits spent.

Use `../../../runtime/crun_cli.py`, `../../../catalog/models.json`, and the shared child skills:

- `../../crun-model-router/SKILL.md` — model routing & live schema inspection
- `../../crun-account-credits/SKILL.md` — balance & affordability estimation
- `../../crun-task-runner/SKILL.md` — task creation, monitoring, recovery, result delivery (the authority)

---

## Trigger

Activate for any of: photo replication, photo recreation, photo remake, photo restyle, portrait recreation, pose clone, style restyle, vintage photo restoration, classic photo clone, replica photo, photo restyle aesthetic — even if the user never says "Crun" or a model name.

---

## Execution Workflow

```text
[ User Request ] (Source Photo and/or Target Style Description)
    │
    ├── 1. Entry Path & Media Upload
    │       ├─ Image provided  → Upload: python <runtime>/crun_cli.py upload <local-file>
    │       └─ No image        → Proceed with text-driven replication concept
    │
    ├── 2. Mode & Style Resolution
    │       ├─ Resolve replication mode (Face Swap / Style Restyle / Old Photo Remake / Pose Clone)
    │       └─ Resolve style & aesthetic (Interactive AskUserQuestion options if unspecified)
    │
    ├── 3. Model Routing & Schema Inspection
    │       ├─ Pick image-edit model with supports_reference: true (Path A) or text-to-image (Path B)
    │       └─ Inspect live schema: python <runtime>/crun_cli.py models describe --model <model>
    │
    ├── 4. Estimate & Confirmation Gate
    │       ├─ Estimate credits (crun-account-credits): task estimate --model <model> --input-file <input.json>
    │       └─ Present summary & require explicit OK via interactive buttons before spending
    │
    └── 5. Task Creation & Result Delivery (crun-task-runner)
            ├─ Create task: python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
            ├─ Poll status: python <runtime>/crun_cli.py task wait --task-id <task_id>
            └─ Deliver local media path & inline image preview
```

---

## Entry Path Decision

1. Inspect the current conversation for an attached or linked source photo.
   - **Image present** → follow Path A (image-driven replication).
   - **No image** → follow Path B (text-driven replication).
2. Treat only resources visibly attached or explicitly linked in the current conversation as source material. A new session starts with no source material, even if prior sessions, chat history, tool traces, or generated JSON mention a media URL or local path. Never reconstruct or infer a task input from historical JSON.

---

## Replication Modes

This skill supports four canonical photo replication modes:

1. **Face & Subject Swap Replication**:
   Keep the exact framing, pose, outfit, background, and lighting of the source photo, while substituting the subject with a target person or blending facial features.
2. **Style & Aesthetic Restyle**:
   Recreate the photo's scene composition and pose in a completely new visual medium or era (e.g., 80s/90s Retro Film, Cyberpunk Neon, Anime/Comic, Claymation 3D, Studio Portrait, Cinematic Movie, Oil Painting).
3. **Classic & Old Photo Restoration/Remake**:
   Re-create vintage, blurry, faded, or damaged historical photos into ultra-crisp modern high-definition portrait photography while retaining emotional tone, posture, and facial identity.
4. **Pose & Composition Clone**:
   Clone the lens focal length, depth of field, framing, camera angle, lighting ratio, and subject posture from a reference photograph to apply onto a new creative subject or setting.

---

## Path A — Source Photo Provided

### A1. Upload the source

```text
python <root>/runtime/crun_cli.py upload <local-file>
```

Reuse an existing Crun resource URL directly. Never send Base64, data URIs, or local paths in a task input.

### A2. Resolve mode & target style online

- If the user already named a mode and style in the request (e.g., "recreate this photo in 90s vintage film style", "replicate this exact pose"), use it directly.
- Otherwise, search the web for popular photo recreation styles and present **three** concrete options via interactive buttons (`AskUserQuestion`). Use queries such as:
  - `trending photo restyle aesthetic 2025 vintage cinematic studio`
  - `popular photo replication styles retro film cyberpunk 3D animation`

Build three option cards with: option name, a one-line description, example aesthetic, and routed model.

### A3. Pick model & build payload (image-driven → `image-edit`)

Select a model from the **Replication Modes & Models** table below that has `supports_reference: true` in `catalog/models.json`.

After choosing, inspect the live schema:

```text
python <root>/runtime/crun_cli.py models describe --model <model>
```

Construct only fields the schema permits. Put the uploaded `file_url` into the reference image field defined by the live schema (e.g., `image`, `img_urls`, or `reference_image`).

---

## Path B — No Source Photo (Text-Driven)

### B1. Resolve concept, style & lighting online

Search the web for trending photo replication concepts and present choice groups via interactive option buttons (`AskUserQuestion`):

1. **Recreation Concept** — (e.g., 90s Vintage Film Photo / Cinematic Movie Still / Fine Art Studio Portrait).
2. **Target Style** — (e.g., Vintage Film / Cyberpunk Neon / Minimalist French Portrait / 3D Claymation).
3. **Lighting & Atmosphere** — (e.g., Soft Natural Lighting / Neon Night / Dramatic Stage Spotlight).

### B2. Compose prompt & pick model (text-driven → `text-to-image`)

Compose a precise **English** visual description incorporating the selected concept, subject details, pose, lighting, and style, then apply the mode prompt template. Select the model from the table below.

---

## Replication Modes, Models & Prompt Templates

Pick the model from this table based on replication mode and operation type:

| Replication Mode | Key Features | Preferred Models (Text-to-Image) | Preferred Models (Image-Edit, `supports_reference: true`) | Recommended Aspect |
|---|---|---|---|---|
| Face & Subject Swap | Preserves pose, backdrop, lighting; swaps facial identity | `bytedance/seedream-5-pro`, `qwen-image-3.0-pro` | `bytedance/seedream-5-pro`, `openai/gpt-image-2-premium`, `qwen-image-edit-2.0-pro` | 3:4 or 1:1 |
| Style & Aesthetic Restyle | Keeps composition; transforms into Anime/Film/3D/Oil art | `bytedance/seedream-5-pro`, `google/nano-banana-pro` | `bytedance/seedream-5-pro`, `openai/gpt-image-2-premium` | 3:4, 16:9, or 1:1 |
| Vintage Photo HD Remake | High-definition restoration, rich textures, vintage warmth | `bytedance/seedream-5-pro`, `qwen-image-3.0-pro` | `bytedance/seedream-5-pro`, `qwen-image-edit-2.0-pro` | Original or 3:4 |
| Pose & Composition Clone | Extracts camera angle, depth of field, pose structure | `bytedance/seedream-5-pro`, `google/nano-banana-pro` | `bytedance/seedream-5-pro`, `openai/gpt-image-2-premium` | 3:4 or 9:16 |

### Prompt Templates (English)

Fill `[SUBJECT]` with the detailed subject description and `[STYLE_DETAILS]` with lighting/color palette specifics:

- **Face & Subject Swap Replication**:
  `A high-definition photo recreation of [SUBJECT], strictly preserving the original photo composition, posture, outfit, and background environment. Professional studio lighting, sharp facial details, authentic skin texture, cinematic color grading.`
- **Style & Aesthetic Restyle**:
  `A complete photo restyle of [SUBJECT] recreated in [STYLE_DETAILS] visual art style. Replicate the identical pose, framing, and dynamic gesture from the source photo while transforming the visual texture into high-end [STYLE_DETAILS] rendering. Vibrant colors, masterpiece quality.`
- **Vintage Photo HD Remake**:
  `An ultra-realistic modern high-definition photo remake of a classic vintage photograph featuring [SUBJECT]. Preserving original posture, nostalgic mood, and subtle facial expression, updated with 8K skin micro-details, natural lens depth of field, and refined vintage color tones.`
- **Pose & Composition Clone**:
  `A photographic clone of the composition and posture featuring [SUBJECT]. Low-angle camera shot, dramatic key lighting, shallow depth of field, bokeh background, perfectly matching the original reference photo pose and golden-ratio composition.`

---

## Handle Sensitive Media

Before transforming a real person's face, likeness, or identity, or removing a watermark, require explicit user confirmation that they own or are authorized to use and transform the source media. Refuse requests involving non-consensual imagery, impersonation, fraud, or unauthorized mark removal.

---

## Estimate & Confirm

Read `../../crun-account-credits/SKILL.md`. Estimate the final model and exact input payload before creating any task:

```text
python <root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Require `affordable: true`. Present a clear confirmation summary containing:
- Selected Replication Mode
- Target Model
- Aspect Ratio & Resolution
- Estimated Credits

Wait for explicit user confirmation via interactive buttons before spending credits.

---

## Create & Deliver

Read `../../crun-task-runner/SKILL.md` for authoritative task lifecycle management. Create once and poll:

```text
python <root>/runtime/crun_cli.py task create --model <model> --input-file <input.json>
python <root>/runtime/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
```

Follow `crun-task-runner` for all timeout recovery and status checks.

---

## Delivery Format

Deliver the localized completion summary with required normalized metadata fields:

```text
✅ Photo replication completed!
- Task ID: <task_id>
- Mode: <replication_mode>
- Model: <model>
- Credits Used: <credits>
- File Path: <local_image_path>

![Photo Replication](/absolute/path/to/file.png)
```

---

## Localization

Write all user-facing content (options, labels, summary, progress, error messages, final delivery) in the user's primary language. Keep API field names, model IDs, task IDs, numeric values, file paths, and structural prompt keywords unchanged.
