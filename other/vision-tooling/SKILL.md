---
name: vision-tooling
description: Diagnose and fix the agent's OWN image-understanding (vision_analyze) when it 404s or "can't see" a sent image. Covers dead auxiliary.vision backends, PIL file-validity checks, provider-reachability tests, and the local-VLM self-hosting plan. Triggers whenever vision_analyze fails or a user reports an image isn't visible.
---

# Vision Tooling (agent's own image understanding)

## When this applies
- `vision_analyze` returns `404 Couldn't find that` or otherwise fails.
- User sends an image/GIF and you "can't see it."
- Symptom: both the Discord CDN link AND a local cache path 404.

## Diagnostic procedure (do this BEFORE concluding the image is bad)
1. **Verify the file is real & valid** — the image is often fine even when vision fails:
   - `ls -la <path>` (exists? size > 0?)
   - PIL check: `python3 -c "from PIL import Image; im=Image.open(p); print(im.format, im.size, getattr(im,'is_animated',False))"`
   - A valid JPEG/PNG with correct dimensions ⇒ the *image* is not the problem.
2. **Check the vision backend config** — `config.yaml` → `auxiliary.vision`:
   - `provider`, `model`, `api_key`, `base_url`.
   - If `provider: openrouter` with `api_key: ''` / no credits ⇒ **dead**. This is the usual cause.
3. **Understand the fallback** — the active chat model (e.g. `tencent/hy3:free`) is often **text-only**. `vision_analyze` then falls back to `auxiliary.vision`. A dead auxiliary ⇒ 404, NOT an image error.
4. **Test provider reachability** (mask the key): `curl -s -m 10 -H "Authorization: Bearer $KEY" <provider>/models` → 401/403/empty means key/credits are the issue.

See `references/diagnose-vision-404.md` for the exact copy-paste command recipe.

## Pitfalls
- Don't blame the CDN/expiry first. Expired Discord `ex=` tokens do 404, but a locally cached file may still be valid — verify with PIL before assuming the image is lost.
- Don't repeatedly retry the same failed `vision_analyze` call — it 404s identically. Diagnose the backend instead.
- Don't poke a provider the user said is empty/dead (e.g. re-curling OpenRouter after they said "no credits") — wastes a turn and can get blocked.

## Workaround (until fixed)
- Ask the user to describe the image, or use any description they already gave. Image-describing-between-us works fine.

## Future fix (Dad-approved interest, NOT yet built)
Self-host a tiny quantized VLM so the agent sees images with **no token / no credits**:
- Candidates: **Moondream 2** (~2B, edge-designed), **SmolVLM** (256M–2B, CPU-friendly, ONNX).
- Stand up a small server (FastAPI + model) on the VM, expose an OpenAI-compatible chat/visions shape.
- Point `auxiliary.vision` at it via `base_url` (provider can stay, key empty/local).
- **VM constraint:** no GPU, ~1.7GB RAM to guest, AVX2 only ⇒ only a *tiny q4* VLM fits. Alt: run on host RTX 5070 and proxy back (needs host↔VM connectivity, not currently available).
