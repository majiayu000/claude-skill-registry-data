---
name: jpg-to-psd
description: Convert a JPG/PNG character illustration into layered PNGs, depth maps, and a Photoshop PSD with See-Through. Uses the verified isolated ROCm 7.14 / MIOpen 3.5.2 environment on gfx1151; use when the user asks to turn an image/JPG into a layered PSD.
tags: [jpg, png, psd, see-through, layerdiff, rocm]
---

# JPG → layered PSD (See-Through, gfx1151)

## Preconditions

- Project: `/home/chihmin/src/see-through`
- Isolated environment: `/home/chihmin/src/see-through/.venv-rocm7.14`
  - PyTorch `2.12.0+rocm7.14.0`, MIOpen `3.5.2`, gfx1151 support.
- **Never** replace `/opt/rocm-7.2.2`, the original `see-through/.venv`, or preload ROCm 7.14 libraries into that old venv.
- Always set `MIOPEN_DEBUG_CONV_WINOGRAD=0`; gfx1151 Winograd is known to corrupt this workload visually.

## Run

Use this wrapper, which separates LayerDiff and Marigold into two Python processes. This releases LayerDiff's GPU allocations before the depth pass.

```bash
/home/chihmin/.pi/agent/skills/jpg-to-psd/run_rocm714.sh \
  /absolute/path/to/input.jpg \
  /home/chihmin/src/see-through/workspace/my_output
```

Outputs:

- `.../my_output/<input-stem>/` — transparent body-part PNGs, `*_depth.png`, and `reconstruction.png`
- `.../my_output/<input-stem>.psd` — Photoshop layered PSD
- `.../my_output/<input-stem>_depth.psd` — depth-inclusive PSD

The tested configuration uses 1024px LayerDiff, 32 denoise steps, and 512px Marigold depth. The PSD itself remains 1024×1024; depth is upscaled to that canvas during composition.

### Body-only mode

To generate only the 13 body layers (`topwear`, `bottomwear`, limbs, hair, etc.) and skip head layers, Marigold, and PSD composition:

```bash
/home/chihmin/.pi/agent/skills/jpg-to-psd/run_rocm714.sh --body-only \
  /absolute/path/to/input.jpg \
  /home/chihmin/src/see-through/workspace/body_only_output
```

This mode uses process-local `MIOPEN_FIND_MODE=FAST` plus Winograd disabled. FAST find reduces convolution-selection startup time but can trade away kernel performance; inspect the generated body layers before delivery.

## Timing and capacity

Measured on the Ryzen AI MAX+ 395 / Radeon 8060S while other GPU services remain active:

- LayerDiff at 1024px / 32 steps: roughly **8–10 minutes**.
- Marigold at 512px with group offload plus PSD composition: roughly **1–2 minutes** once cached.
- End-to-end: budget **10–15 minutes** (first download can add time).

Do not use Marigold depth 768 while the 31GB `llama-server` is active: it requests a ~31.6GB allocation and OOMs. The 512px + `group_offload=True` configuration completed successfully and produced a visually correct PSD.

## Verify before sending

```bash
ROOT=/home/chihmin/src/see-through
OUT="$ROOT/workspace/my_output/input.psd"
"$ROOT/.venv-rocm7.14/bin/python" - "$OUT" <<'PY'
from psd_tools import PSDImage
import sys
psd = PSDImage.open(sys.argv[1])
print(psd.size, len(psd), [layer.name for layer in psd][:12])
PY
```

Then inspect `reconstruction.png` for rainbow/oil-film artifacts. If present, stop: do not fall back to the old ROCm 7.2 environment.
