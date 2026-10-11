---
name: comfyui-headless-pixal3d
description: "Turns 2D art into 3D game assets headlessly via the local ComfyUI server (Pixal3D + TRELLIS.2): single-image to textured GLB, multi-view turnaround sheet to GLB, ModelScope (domestic, traffic-quota-safe) weight download, extra_model_paths registration, and Blender import via blender-mcp. Invoke when the user asks for 图生3D/3D模型/GLB/建模/多视图转3D, wants ComfyUI 3D templates run without the UI, or asks to convert 素材图/立绘/概念图 into 3D."
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# ComfyUI Headless Image-to-3D (Pixal3D + TRELLIS.2 game assets)

Drive the locally installed ComfyUI **without its UI** to convert 2D art into textured 3D
models (GLB). The heavy lifting is Pixal3D (Tencent ARC, SIGGRAPH 2026, MIT) running on the
TRELLIS.2 latent space (Microsoft): sparse-voxel structure → shape upsample → PBR texture,
all decoded through TRELLIS.2's structure/shape/texture VAEs, with BiRefNet matting, DINOv3
conditioning and (single-image mode) MoGe FOV estimation. All commands below run the bundled
script `scripts/comfy3d.py` (stdlib only, no deps). Verified API-format workflows live in
`workflows/`. Deep gotchas of the UI-template → API conversion are documented in
`references/converter-notes.md` — read it before touching the converter or after any
"completed but no GLB" surprise.

## 1. Path discovery — NEVER hardcode install or model paths

Identical chain to the sibling skill `comfyui-headless-image21`:

1. `COMFYUI_HOME` env var (folder containing `ComfyUI/main.py` or `main.py`).
2. `%APPDATA%\Comfy Desktop\installations.json` (Desktop app install registry).
3. Shallow scan of every existing drive root and common program directories for
   `*omfy*` folders (matched folders are scanned one level deeper — installs often nest).
   No machine-specific paths are assumed anywhere.

Model registrations are read, never assumed: `%APPDATA%\Comfy Desktop\settings.json`
(`modelsDirs`), `%APPDATA%\Comfy Desktop\shared_model_paths.yaml`, and
`<code_root>\extra_model_paths.yaml` (core mechanism, gitignored, survives ComfyUI updates).
`python scripts/comfy3d.py find` prints what is registered and which of the 8 weights are present.

## 2. Weights — 8 files, ~19.4 GiB, from ModelScope ONLY

| ComfyUI folder | file | GiB | used by |
|---|---|---|---|
| diffusion_models | pixal3d_int8_convrot.safetensors | 5.20 | single-image |
| diffusion_models | pixal3d_multiview_int8_convrot.safetensors | 5.20 | multi-view |
| diffusion_models | trellis_2_int8_convrot.safetensors | 4.89 | single-image |
| vae | trellis_2_shape_vae_bf16.safetensors | 1.02 | both |
| vae | trellis_2_texture_vae_bf16.safetensors | 0.88 | both |
| clip_vision | dino_v3_L_naf_fp32.safetensors | 1.13 | both |
| geometry_estimation | moge_2_vitl_normal_fp16.safetensors | 0.62 | single-image |
| background_removal | birefnet.safetensors | 0.41 | both |

**Download rule: ModelScope (`modelscope.cn`, Alibaba) is the only sanctioned source.**
hf-mirror.com is a FAKE domestic source for these repos: it 308-redirects `/resolve/` to
huggingface.co, which 302s to `us.aws.cdn.hf.co` (AWS international CDN, observed
`x-hf-cdn-pop: aws-eu-west-3`). Bytes served from abroad burn the user's **100 GB/month
international quota**. `scripts/comfy3d.py download` HEAD-verifies the final byte-serving
host is `modelscope.cn` before every transfer and refuses otherwise. If downloading by hand:

```
curl -sIL "<url>" -o /dev/null -w "%{url_effective}\n"   # verify final host FIRST
curl -L -C - -o "<dest>" "https://www.modelscope.cn/models/Comfy-Org/Pixal3D/resolve/master/diffusion_models/pixal3d_int8_convrot.safetensors"
```

## 3. Registration (one-time, per machine)

Add to `<code_root>\extra_model_paths.yaml` — the same file the sibling skill uses, so all
custom models live in one place. **Folder keys are ComfyUI type names**: MoGe lives in
`geometry_estimation` and BiRefNet in `background_removal`, NOT `moge`/`birefnet`.

```yaml
pixal3d_trellis2:
  base_path: '<YOUR_MODELS_ROOT>\Pixal3D-Trellis2'   # any registered root; keep the subfolder names below
  diffusion_models: 'diffusion_models'
  vae: 'vae'
  clip_vision: 'clip_vision'
  geometry_estimation: 'geometry_estimation'
  background_removal: 'background_removal'
```

`<YOUR_MODELS_ROOT>` is wherever you keep models (any drive); `scripts/comfy3d.py download`
lands files in the first registered dir found for each folder type.

Restart ComfyUI (Desktop app or headless server) after editing — search paths load once at
startup. The file is gitignored, so ComfyUI updates never clobber it.

## 4. Single image → GLB (template `3d_pixal3d_trellis2_image_to_model`)

```
python scripts/comfy3d.py run --template image --image C:\path\asset.png [--seed N] [--out DIR]
```

Pipeline: LoadImage → BiRefNet background removal → MoGe depth/FOV (single-image needs the
camera estimate) → DINOv3 conditioning → trellis_2 diffusion (structure) + pixal3d diffusion
(detail) → structure/shape/texture VAE decode → voxel→mesh → remesh 768 + decimate 700k +
UV unwrap + AO/normal bake → `Save3DAdvanced` writes the GLB. Reference run: **~4 min per
model end-to-end, ~49 MB GLB, ~700k faces** (the 700k is the template's `DecimateMesh` cap,
not a hardware property). Runtime scales with GPU speed and free VRAM — weights stream from
RAM when they exceed VRAM, trading speed for capacity.

Tips: a transparent-background PNG skips nothing (BiRefNet still runs) but works perfectly —
generate one with the sibling `comfyui-headless-image21` skill (official RGBA prompt template).
The 8 preview PNGs saved alongside are worth a glance (mask, voxel colors, baked texture atlas).

## 5. Multi-view turnaround → GLB (template `3d_pixal3d_multi_views`)

```
python scripts/comfy3d.py run --template multiview --image C:\path\turnaround_strip.png
```

Input is ONE **horizontal 4-view strip, exactly 6336x2688** — NOT a 2x2 grid. The template
crops it at fixed pixel boxes; **panel order is front, LEFT, BACK, right** (x=0/1652/3182/4728,
width 1669/1492/1476/1608, full height — verified by tracing SaveImageAdvanced titles back
through `ImageCropToMask` to the `ImageCropV2` boxes; note back and left are SWAPPED vs a
naive reading). `scripts/make_turnaround_strip.py` composes any four view images into that
geometry (contain-fit on white). The template saves
the four crops as named previews (`front_view/back_view/left_view/right_view_*.png`) — check
them if the views look permuted. It conditions `pixal3d_multiview` on all views jointly: the
back of the model is reconstructed from the back view instead of hallucinated. It uses the
separate `pixal3d_multiview` weight and needs NO trellis_2 diffusion model and NO MoGe.

**Full recipe (end-to-end verified 2026-10-05 on a corgi, ~6 min total):**

1. Keep the original art as the front view.
2. With the sibling `comfyui-headless-image21` skill `edit` command (original as reference
   = identity anchor), generate back / left / right: "Show the same dog from its left side:
   full profile view facing left..." (~35 s each). The BACK view needs an explicit
   "photographed from behind... the face is NOT visible" instruction — a plain "back view"
   prompt made the model draw a front view instead.
3. `python scripts/make_turnaround_strip.py --front <orig> --back <back> --left <left> --right <right> --out sheet.png`
4. `python scripts/comfy3d.py run --template multiview --image sheet.png`
5. Verify in Blender from 4 azimuths: front face present, back face ABSENT (that is the
   whole point of the multi-view route), left/right consistent.

## 6. Blender import (blender-mcp already runs on port 9876)

```python
import bpy
before = set(bpy.data.objects.keys())
bpy.ops.import_scene.gltf(filepath=r"<out>\ComfyUI_00001.glb")
new = [o for o in bpy.data.objects if o.name not in before]
```

Then select the imported meshes, switch shading to `MATERIAL`, `bpy.ops.view3d.view_selected`.
Two traps: (1) **the default startup Cube (2 m) encloses a ~0.8 m generated asset** — renders
and viewport shots show only the cube shell; delete `Cube` first. (2) On Blender 5.2 the MCP
area-screenshot returns an all-black image even when the scene is fine — verify with a temp
camera + `bpy.ops.render.render(write_still=True)` instead. Expect ~700k faces: decimation is
built into the template (700k cap) but the topology is still marching-cubes, not
game/rig-ready — plan a retopo pass in Blender for production assets.

## 7. Pitfalls (top 5 — full list in references/converter-notes.md)

1. **hf-mirror serves international bytes** → ModelScope + host verification (section 2).
2. **VRAM contention**: if a 3D run OOMs, thrashes, or crawls, another ComfyUI/image server
   is probably still holding VRAM — stop it first, then rerun. Find it by command line:
   `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "main\.py --port" }`
   → `taskkill //F //PID <pid>`. Each server should use its own port; the 3D script defaults
   to 8189 so it never collides with a Desktop-launched server on 8188.
3. **"Completed in 5 s" with no GLB is a fake success**: the server accepted the prompt but
   validation dropped invalid nodes ("Output will be ignored" in the server log). The script
   gates on `node_errors` in the `/prompt` response and asserts a model file in the outputs.
4. UI-template → API conversion has 4 distinct widget-spec formats + seed control words +
   dynamic-combo dotted sub-keys + the required `viewport_state` on Save3D/Load3D nodes.
   The converter in `scripts/comfy3d.py` handles all of them; don't hand-patch API JSONs.
5. `RemeshMesh`/`DecimateMesh` are COMFY_DYNAMICCOMBO_V3 nodes: the selected option's
   sub-inputs must be submitted as dotted keys (`sign_mode.qef` etc.).
6. Registration folder names are type names (`geometry_estimation`, `background_removal`).

## 8. Maintenance

After a ComfyUI update that changes the official templates, regenerate the API workflows:

```
python scripts/comfy3d.py convert --template image      # or multiview
python scripts/comfy3d.py convert --template multiview --object-info <cached object_info.json>
```

`convert` dumps a cached `GET /object_info` (any headless server run) into the converter for
offline use. Then re-run one single-image generation before trusting the new files.
