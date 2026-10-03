---
name: create-image
description: Generate new images locally with FLUX.2 or Anima on ROCm 7.2. Use for /create-image and text-to-image requests, including photoreal, anime, illustration, PVC figures, and consistent-character anime storyboards with Anima ControlNet-LLLite. For editing, restyling, or converting an uploaded photo—especially Fuji/film looks—use photo-editing instead.
---

# Create Image

Generate **new** images only. Image-to-image, retouching, restyling, and uploaded-photo requests belong to `photo-editing`.

## Mandatory research

Before every request, web-search unfamiliar or meaningful names, characters, locations, franchises, products, memes, and styles. For named characters, verify their design and turn the reference into a detailed visual description; do not assume the model knows the name.

## Run

Use the deployed script only—do not write a Diffusers/SD script or download models.

```bash
cd /home/chihmin/models-work/flux2
source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python ~/.hermes/skills/create-image/scripts/create_image.py "YOUR PROMPT"
```

The script prints JSON. Attach its `final_path` in the same Discord reply:

```text
[[image: /absolute/path/to/result.png]]
```

## Choose a generation mode

| Request | Flags |
|---|---|
| Photoreal / general | none — FLUX.2 9B, default 16:9 1080p output |
| Quick draft | `--fast-preview` (4B) |
| Native high-quality | `--native-1080p` (for photo aspect normally also `--aspect-ratio 3:2`) |
| Anime / illustration / waifu (text only) | `--anime` — mandatory Anima backend |
| High-quality anime | `--anime --native-1080p` |
| PVC / figure / 手辦 / フィギュア | `--anime`; include `pvc figure` in prompt (the script switches checkpoint) |
| 二次元像素風 / pixel art / sprite / ドット絵 | `--anime`; pixel keyword auto-loads the Elin pixel-sprite LoRA + `pixel art, chibi, white background, simple background` (drops the background words when the prompt asks for a scene) |
| Text-only Fuji / analog film look | film wording in prompt (auto LoRA), or `--film` |
| **Photo → anime / 二次元風格化** | **`--anime --image <photo> --strength <value>`** — see below |
| **固定角色／二次元分鏡／same character in new scenes** | **Anima ControlNet-LLLite via `scripts/anima_lllite.py`** — see below |

### Fixed-character anime storyboards with LLLite

When the user asks to keep a character design across storyboard frames while changing the scene, camera angle, or action, use the dedicated **Anima ControlNet-LLLite CLI** instead of plain Anima img2img. This workflow keeps `anima_baseV10.safetensors` untouched and applies `anima-lllite-any-test-like-v2.safetensors` at runtime.

LLLite is structural guidance rather than a true identity encoder. It worked best in local tests for sharp storyboard frames, camera perspective, and action adherence, but the prompt must repeat the complete character design in every frame: hair, eyes, ears, ribbons, outfit, colors, and accessories.

#### Mandatory character-sheet-first workflow

Whenever the user requests **storyboards**, **the same/recurring character**, or **character consistency across images**, do not generate scene frames first. Always create a clean white-background character setting sheet, then use that generated sheet as the `--reference` for every LLLite scene.

1. Research any named character or source design and write the complete visual description.
2. Generate the master setting sheet with plain Anima text-to-image (`create_image.py --anime`), **not** with LLLite.
3. Put exactly one full-body, front-facing, neutral-pose depiction of each recurring character on a pure white background. For multiple characters, use one wide lineup sheet with fixed left/center/right order.
4. Inspect the full-resolution sheet before continuing: exact character count, unobstructed silhouette, face, hair, eyes, ears/tails, outfit colors, hands, feet, and signature accessories must be correct.
5. Use that generated sheet—never an arbitrary scene frame—as the `--reference` for all subsequent `anima_lllite.py` storyboard images.
6. Repeat every character's complete design in every scene prompt; the reference image does not replace textual identity descriptions.

Do not put turnarounds, repeated views of the same character, face insets, color swatches, labels, captions, scenery, furniture, or floating props on the master sheet. Those elements can be interpreted by LLLite as duplicate people or scene structure. Keep figures fully separated with generous white space and no overlapping hair, ears, tails, weapons, or clothing.

Single-character master-sheet example:

```bash
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "masterpiece, best quality, score_7, safe, exactly one recurring young adult anime rabbit woman, full-body front-facing neutral standing pose, long silver-white twin-tail hair, small red ribbons, tall white rabbit ears, golden eyes, white blouse with navy bow, red frilly cafe apron, navy pleated skirt, black loafers, arms relaxed, entire ears and shoes visible, centered with generous margins, pure white seamless background, clean character setting sheet, no text, no props, no inset, no additional views, no scenery" \
  --anime --aspect-ratio 16:9 \
  --out-dir /absolute/path/to/project/character-sheets \
  --prefix rabbit-master
```

For a multi-character sheet, begin with `exactly N recurring characters, no extra people`, describe every character completely in fixed screen order, and end with `separate full-body neutral poses, no overlap, pure white seamless background`.

#### One-time environment setup

ComfyUI must expose the built-in `ModelPatchLoader` and `AnimaLLLiteApply` nodes. The deployed installation already has them. Install the independent LLLite weight under `models/model_patches` if it is missing:

```bash
cd /home/chihmin/src/ComfyUI
mkdir -p models/model_patches
.venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id="kohya-ss/Anima-LLLite",
    filename="anima-lllite-any-test-like-v2.safetensors",
    local_dir="/home/chihmin/src/ComfyUI/models/model_patches",
)
PY
```

Verify the weight and node registry without manually starting ComfyUI:

```bash
test -f /home/chihmin/src/ComfyUI/models/model_patches/anima-lllite-any-test-like-v2.safetensors
curl -fsS http://127.0.0.1:8188/object_info | \
  python -c 'import json,sys; d=json.load(sys.stdin); print("ModelPatchLoader" in d, "AnimaLLLiteApply" in d)'
```

If ComfyUI is managed by `comfyui.service`, use the service; do not launch a second server manually.

#### CLI command

```bash
cd /home/chihmin/models-work/flux2
source .venv-rocm72/bin/activate
python ~/.hermes/skills/create-image/scripts/anima_lllite.py \
  "masterpiece, best quality, score_7, safe, solo 1girl, same rabbit girl character, long silver-white twin-tail hair, small red ribbons, tall white rabbit ears, golden eyes, white blouse with navy bow, red frilly cafe apron, navy pleated skirt, low-angle action shot, jumping over a rain puddle on a neon-lit street" \
  --reference /absolute/path/to/character-reference.png \
  --aspect-ratio 16:9 \
  --strength 0.4 \
  --end-percent 0.5 \
  --steps 30 \
  --seed 12345 \
  --prefix storyboard-shot-01
```

The script automatically cover-crops the reference to the generation canvas and converts it to the verified low-contrast grayscale control image. It prints JSON; attach its `final_path`. For an animation storyboard, pass the exact H3 canvas with `--output-size 864x480`; this makes both Anima generation and final output use that geometry instead of resizing afterward.

Recommended settings:

| Goal | `--strength` | `--end-percent` |
|---|---:|---:|
| Change scene, camera angle, and action | **0.35–0.45** | **0.45–0.55** |
| Preserve more silhouette and pose | 0.5–0.7 | 0.6–0.8 |
| Very strict structural copy | 0.7–1.0 | 0.8–1.0 |

Storyboard rules:
- First generate and verify a **white-background master character setting sheet**; do not use an existing scene composition as the initial identity reference.
- Use that same generated master sheet as the **reference image for every frame**.
- Repeat the full character design in every prompt; never use only “same character.”
- Keep `--steps 30`; 8-step diagnostics are visibly soft and are not production output.
- Change action, camera language, and scene explicitly: e.g. `worm-eye low angle`, `bird-eye overhead`, `Dutch-angle close-up`, `dynamic foreshortening`.
- Reuse `--seed` when testing prompt changes; vary it when the composition is stuck.
- For maximum identity fidelity beyond structural consistency, LLLite alone may still drift in face or costume details.

#### Multiple recurring characters guide

For two or more recurring characters, first generate **one white-background lineup setting sheet** containing the whole cast with plain Anima. Do not substitute a scene image or merely select an arbitrary group picture. A wide 16:9 sheet works best: exactly one full-body front view per character, no overlap, neutral poses, pure white seamless background, generous spacing, and a fixed left/center/right order. Keep that generated sheet and ordering across the storyboard whenever the scene permits.

Design the cast for visual separation rather than subtle variation:
- Give every character a distinct silhouette, height, species or ear shape, hair color/style, outfit palette, and signature accessory.
- Avoid several characters with nearly identical hair, uniforms, or body proportions; LLLite can mix those attributes.
- State the exact count near the beginning: `exactly three recurring anime girls, no extra people`.
- Repeat every character's **complete description in every prompt**. Names, pronouns, or `same three characters` are not enough.
- Assign each character an explicit position and action in separate clauses: `On the left... In the center... On the right...`.
- Keep descriptions in the same character order even if an action temporarily changes their screen positions.

Recommended prompt structure:

```text
masterpiece, best quality, score_7, safe.
Exactly three recurring anime girls, no extra people.
[VIEWPOINT + SHOT SIZE + SPATIAL RELATIONSHIP.]
On the left, [character A complete appearance, outfit, action].
In the center, [character B complete appearance, outfit, action].
On the right, [character C complete appearance, outfit, action].
[SETTING, LIGHTING, MOOD.]
Preserve all three distinct faces, species, hairstyles, outfit colors,
relative heights, and signature accessories.
```

For visibly different shots, describe both **where the view is located** and **the shot size** in natural language. Avoid merely naming a lens or writing `camera`, which can be ignored or rendered as an object.

Tested examples:
- Ground-level: `ground-level worm's-eye full-body wide view, looking sharply upward; shoes and legs closer, faces higher against the sky, strong vertical convergence`.
- Overhead: `straight-down ninety-degree bird's-eye wide view from directly above; tops of heads visible, ground plane dominates, no eye-level horizon`.
- Side tracking: `strict side-profile tracking wide shot, viewed perpendicular from their right side; all bodies and faces in profile, nobody faces the viewer`.

Multi-character settings and iteration:
- Start with `--strength 0.35 --end-percent 0.45 --steps 30`; use `0.30/0.40` for a major viewpoint or action change.
- Reuse the same seed while comparing prompt wording. Change the seed only after the spatial description has been made explicit.
- Preserve the lineup's left/center/right order for the first pass. Reordering, over-the-shoulder staging, and heavy occlusion are less reliable.
- If one character disappears, move `exactly N ... no extra people` earlier and simplify the action/background.
- If colors, ears, clothing, or weapons bleed between characters, increase visual contrast between designs and repeat the affected details next to that character's position/action.
- Inspect full-resolution faces, hands, ears, tails, costumes, and accessories before accepting a frame; a correct character count alone is not sufficient.
- For exact per-character identity, difficult occlusion, or more than three characters, use a hybrid IP-Adapter + low-strength LLLite workflow, or generate/inpaint characters separately. LLLite is structural guidance, not a per-character identity encoder.

Example three-character invocation:

```bash
python ~/.hermes/skills/create-image/scripts/anima_lllite.py \
  "masterpiece, best quality, score_7, safe. Exactly three recurring anime girls, no extra people. Straight-down ninety-degree bird's-eye wide view from directly above. On the left, a petite pink-haired fox girl with orange ears and tail, teal jacket and cream skirt studies a map. In the center, a silver-white twin-tailed rabbit barista with white ears, red ribbons, golden eyes, white blouse, red apron and navy skirt points at the route. On the right, a tall black-haired cat knight with black ears and tail, navy military coat, white trousers and sword guards the table. Warm fantasy cafe, patterned stone floor. Preserve all three distinct identities, outfits, relative heights and accessories." \
  --reference /absolute/path/to/wide-cast-lineup.png \
  --aspect-ratio 16:9 \
  --strength 0.35 \
  --end-percent 0.45 \
  --steps 30 \
  --seed 12345 \
  --prefix trio-overhead-01
```

### Photo → Anime (二次元風格化)

When the user uploads a **real photo** and asks to convert it into anime/二次元 style (e.g. 「做成二次元」、「轉動漫風」、「二次元化」), use the **Anima img2img** path — do NOT use the FLUX.2 RefControl route even though it is a photo edit.

```bash
cd /home/chihmin/models-work/flux2
source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python ~/.hermes/skills/create-image/scripts/create_image.py \
  "PROMPT" \
  --anime --image /path/to/photo.jpg --strength <value>
```

**Choose denoise (`--strength`) by how faithful to the original photo you want to be:**

| `--strength` value | Effect |
|---|---|
| 0.3–0.4 | Extremely faithful to photo, minimal change |
| 0.5–0.6 | Moderate re-paint, preserves composition |
| 0.65 | **Default** — structure preserved + style reinterpreted |
| 0.75–0.85 | Low reference influence, photo acts as inspiration only |
| 0.9+ | Almost pure text-to-image, photo barely matters |

**Guidelines:**
- To **keep original pose/composition**: use `--strength 0.5–0.65`
- To **only keep character concept** (color scheme, features): use `--strength 0.75–0.85`
- If the original photo **contaminates** the output (e.g. photographic artifacts, unwanted details): increase `--strength` toward 0.8
- **Photo sketch / hand-drawn reference → anime**: use `--strength 0.9` temporarily so the model relies mainly on the text prompt for the anime design while using the sketch only as loose compositional inspiration
- Always describe the desired anime character appearance in the prompt, not just reference the photo

**Example:**
```bash
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "masterpiece, best quality, score_7, safe, 1girl, anime rabbit girl, long fluffy rabbit ears, pink hair, large sparkling eyes, gentle smile, frilly dress, holding a carrot, pink and white pastel palette, soft warm lighting, dreamy background, sitting pose, shoujo manga style" \
  --anime --image /path/to/photo.jpg --strength 0.8
```

Examples:

```bash
# photoreal
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "editorial portrait of a jazz pianist, warm window light" --aspect-ratio 3:2

# anime
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "masterpiece, best quality, score_7, safe, 1girl, reading at a cafe window, muted colors, detailed anime background" --anime

# text-to-image analog film
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "a Tokyo street in summer, Fujifilm analog film look, warm grain" --aspect-ratio 3:2
```

## Prompting

### FLUX.2 photoreal
State subject, scene, composition, lighting, palette, and intended photographic treatment. Use `--aspect-ratio 3:2` for a conventional still-photo framing; use 16:9 only for an explicit widescreen request.

### Anima (text-to-image)
Use `--anime` for every anime/illustration output. Start with `masterpiece, best quality, score_7, safe`, then specify count, appearance, action, composition, setting, palette, and lighting. Do not ask it to render long exact text. For a named character, include a detailed researched appearance—not only their name.

Anima defaults to 2:3, `768x1152 → 1184x1776`; use `--aspect-ratio` only when a different shape is requested. `--guidance-scale 1` is faster when strong adherence is not needed. Lighting words can auto-load the lighting LoRA; avoid those terms for deliberately flat lighting.

### Anima (img2img: photo → anime)
When converting a photo to anime style, use `--strength` (denoise) to control how much the reference image influences the output (see Photo → Anime section above). Write a detailed character description in the prompt — do not rely solely on the photo as a reference. The prompt should include: count, character appearance (hair, eyes, ears, accessories), outfit, pose, expression, color palette, lighting, and background style.

## Constraints

- Do not enable `create-image-daemon.service`; keeping FLUX resident risks OOM.
- Do not start ComfyUI manually. The Anima path starts and cleans up its worker automatically.
- Do not stop or restart Qwen/Gemma MTP services for generation.
- `--fast-preview` is only for explicitly requested drafts; `--native-1080p` is only for explicitly requested high quality.
- Always attach the generated PNG in the first result reply.
