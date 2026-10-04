---
name: ideogram4-prompting
description: Load for Kosta's local RTX GamingPC Ideogram 4 lane — structured JSON caption prompting, ComfyUI :8190 routing, typography/poster/label/infographic/design generation, and safety-placeholder debugging. Use JSON captions by default; plain text is a known failure mode.
metadata:
  targets:
    - claude
    - codex
    - hermes-default
    - hermes-gpt
    - claude-hermes
    - cursor
    - gemini
---

# Ideogram 4 Prompting

Use this for Kosta's local Ideogram 4 lane on the RTX GamingPC when the request is text/layout/design-heavy: posters, signs, labels, packaging, menus, logos, typography experiments, presentation graphics, and infographic-style layouts.

## Local lane

- Endpoint: `http://100.93.10.54:8190`
- Runner: `/Users/Kosta/.hermes/profiles/gpt/scripts/ideogram4_generate.py`
- Infographic self-evolve script: `/Users/Kosta/.hermes/profiles/gpt/scripts/ideogram4_infographic_selfevolve.py`
- GamingPC install: `C:\Users\kosta\AIProjects\ComfyUI-Ideogram4`
- Production Qwen lane stays separate on `:8188`; do not disturb it for Ideogram work.
- Current model pack: Comfy-Org Ideogram 4 NVFP4 mixed lane, non-commercial weights.

## Critical rule: use JSON captions

Ideogram 4 was trained on structured JSON captions. Plain text works sometimes, but it is the wrong default for this lane. The earlier infographic failure came from sending plain/rich prose prompts, which produced gray `Image blocked by safety filter` placeholders and pushed self-evolve into fake photographed worksheet pages.

Default behavior:

```bash
python3 /Users/Kosta/.hermes/profiles/gpt/scripts/ideogram4_generate.py \
  --prompt '<JSON caption or plain request>' \
  --json-mode auto \
  --preset default \
  --width 1024 --height 1024 \
  --output-dir /tmp/ideogram4-test
```

`--json-mode auto` wraps plain prompts into Ideogram's JSON caption shape. For serious layouts, hand-write the JSON caption instead of relying on the generic wrapper.

## JSON caption schema to use

Keep top-level key order and element key order stable:

```json
{
  "high_level_description": "One or two sentences describing the whole finished image.",
  "style_description": {
    "aesthetics": "modern editorial, clean, premium",
    "lighting": "even flat digital lighting with crisp contrast",
    "medium": "graphic_design",
    "art_style": "flat vector design, straight-on digital canvas, crisp typography",
    "color_palette": ["#FFFFFF", "#111827", "#2563EB", "#10B981"]
  },
  "compositional_deconstruction": {
    "background": "Clean straight-on digital design canvas.",
    "elements": [
      {"type": "text", "bbox": [45,70,150,930], "text": "TITLE", "desc": "Large bold title rendered verbatim."},
      {"type": "obj", "bbox": [175,65,890,935], "desc": "Main infographic/chart/icon composition."}
    ]
  }
}
```

Bounding boxes are normalized `[y_min, x_min, y_max, x_max]` coordinates from `0` to `1000`. Use `type: "text"` for every exact visible word. Use `type: "obj"` for shapes, charts, panels, icons, arrows, subjects, and backgrounds.

## Infographic prompting pattern

For real infographics, prompt as a digital design asset, not a photographed page:

- `medium`: `graphic_design`
- `art_style`: `flat vector infographic, straight-on digital canvas, aligned grid, crisp typography, charts, arrows, icons, generous whitespace`
- Title element: one large `text` object at top.
- Body visual: one broad `obj` region describing the chart/diagram system.
- Labels: 3-5 separate `text` objects with explicit boxes.
- Prefer fewer labels with larger type over dense microtext.
- Avoid product/photo framing like `printed page`, `on a table`, `poster photographed`, `paper`, `classroom worksheet`, unless Kosta explicitly wants a physical mockup.

## Safety-placeholder handling

If the output is a gray screen saying `Image blocked by safety filter`, do not try to “turn off” a ComfyUI safety node first; in this lane there may be no local toggle. Retry once with a structured JSON caption and simpler explicit elements. Ideogram's own docs say false positives are higher for non-JSON prompts.

If JSON still blocks twice on benign content, record the prompt, seed, preset, and output path, then route the job to Qwen/GPT Image instead. Do not keep burning seeds with cosmetic wording changes.

## Settings

- `default` / 20 steps: normal working default for text/design.
- `quality` / 48 steps: use after a prompt structure is proven and the output is worth polishing.
- `turbo` / 12 steps: smoke tests and rough drafts only.
- Start at `1024x1024`; use Ideogram-supported multiples of 16 up to `2048` when the workflow needs wider/portrait assets.

## Self-evolve loop

For Ideogram self-improvement runs:

1. Use JSON captions from the first iteration.
2. Score for: not blocked, not a paper/worksheet photo, exact title/labels, real infographic structure, visual hierarchy, absence of fake microtext.
3. Revise the JSON structure, not just adjectives.
4. Track prompt JSON, seed, preset, dimensions, image path, score, dominant failure, and prompt delta.
5. Stop if two consecutive JSON-structured iterations mostly block; route away rather than retrying plain text.

## Timing and lane management (measured 2026-06-11, RTX 4090, 1024×1024)

- `default` (20 steps): **~35s** per image warm; ~38s on the first generation after model load.
- `turbo` (12 steps): **~25s** including model load; roughly ~20s warm.
- `quality` (48 steps): ~70–80s extrapolated from the per-step rate.
- Lane boot: if `:8190` is down, start it with `ssh-gamingpc 'schtasks /run /tn HermesIdeogram4ComfyUI'` — it answers `/system_stats` within ~10–40s. Check `curl -m 5 http://100.93.10.54:8190/system_stats` before assuming the lane is broken; the VRAM watchdog or a crash can leave the port dead while Qwen `:8188` is fine.
- Do NOT queue jobs back-to-back without waiting for completion: 5 rapid sequential submissions crashed the ComfyUI process mid-run (port stopped listening, GPU memory dropped to idle). Sequential generations with a few seconds of gap are stable. The runner script's poll uses a 30s per-request timeout — an exact-30s failure usually means the lane died, not a slow render.
- The scheduled task runs as a **visible console window** in Kosta's desktop session — he will see terminals pop open on the GamingPC screen/stream. When the work is done, shut the lane down instead of leaving windows around: `ssh-gamingpc 'schtasks /end /tn HermesIdeogram4ComfyUI'`, then `taskkill /pid <pid> /f` any leftover Console-session `python.exe` (find via `tasklist /v /fi "imagename eq python.exe" /fo csv | findstr /i kosta`; the Qwen lane's pythons run as SYSTEM in Session 0 — leave those alone).

## Sources checked

- Ideogram 4 README: structured JSON prompting, model size/license, native 2k layout/color controls.
- Ideogram 4 `docs/prompting.md`: JSON-caption schema, key order, bbox format, magic prompt, and note that safety false positives are higher for non-JSON prompts.
- Ideogram 4 `docs/inference.md`: presets and supported resolutions.
- Ideogram 4 `docs/safety.md`: Hive runtime filters in official inference path and safety expectations.
