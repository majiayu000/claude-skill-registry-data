---
name: video-delivery-qa
description: "Inspect, validate, and prepare video deliverables for export or handoff using available local tools such as ffprobe, frame sampling, waveform/audio inspection, captions, and visual review. Use for video QA, validate an export, delivery check, subtitle sync, audio check, frame inspection, or ComfyUI/video workflow output review. Turkish triggers: videoyu teslim öncesi kontrol et, çözünürlük/ses/kare ve oynatma, kalite raporu."
---

# Video Delivery QA

Validate the delivered file before changing or publishing it. Keep source media and outputs non-destructive.

1. Identify destination, required codec/container, frame rate, resolution, aspect ratio, duration, audio/caption requirements, and authoritative source.
2. Inspect technical metadata with an available local tool; do not install encoders or overwrite files without permission.
3. Sample start, middle, end, transitions, overlays, titles, cuts, and any known-risk moments as rendered frames.
4. Check audio presence, clipping/silence, sync, channel layout, and subtitle timing where applicable.
5. Compare output with source/workflow provenance: project version, seed/workflow hash if relevant, models/assets, export settings, and any missing dependencies.
6. Report pass, fail, and uncertain checks with evidence. Create a new corrected export only when explicitly requested.

## Guardrails

- Do not claim visual quality from metadata alone.
- Do not publish, upload, or delete source media.
- Check local history/output folders before rerunning a long generation after a timeout or interrupted UI.
