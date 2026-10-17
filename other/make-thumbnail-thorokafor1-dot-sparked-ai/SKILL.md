---
name: make-thumbnail
description: Build a finished YouTube thumbnail for a long-form video from its real frames. Use when the user asks for a thumbnail or thumbnail options.
---

# Make a thumbnail

The style rules and tools are in `thumbnail-creation/claude.md`: natural light, medium/wide framing, and minimal text.

## Steps
1. **Get the source** into `input/` (`download_source.py`). Bound the scan to the segment that matters, never the whole file.
2. **Get candidates:** the script has no window flag, so first trim to the segment (`ffmpeg -ss <s> -t <len> -i input/X.mp4 -c copy input/seg.mp4`), then run `python extract_candidates.py --video input/seg.mp4 --interval 2 --top-n 12`. Pick the strongest genuine reaction that is also sharp.
3. **Compose:** `python make_thumbnail.py ...`. Use `--frame2` for two panels when the source is vertical and pillarboxed.
4. **Export the final as JPG** (quality about 90). PNGs at 1920x1080 run 1.5-2.6MB, and YouTube rejects anything over 2MB.
5. **Gates run on `output/`** (size, 16:9, main-face sharpness of 100+, exposure). If the face is soft, fix it with a sharper frame or `restore_faces.py`. Don't reach for AI regeneration first.
6. **Run the `critic`** on the final only, then show the user **2-3 finals max**, not every draft.

## Gotchas (keep this list updated)
- **Name comparison boards `*options*`/`*grid*`** so the gates skip them.
- **ChatGPT image returns are about 614x342.** Upscale with Real-ESRGAN before use.
- **Sharpness scores:** finals picked historically score 350+, and rejected drafts score under 70.
