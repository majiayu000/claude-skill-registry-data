---
name: orbit-reel
description: Portrait image cards travel around the speaker in a 3D ring, passing behind the head and across the foreground. Use for /orbit-reel or to apply this specific portrait-video treatment.
---

# /orbit-reel

Apply this treatment to a portrait clip using the included 4.2-second, 1080x1920, 30fps starter. The style and images are independent of the sample speaker’s words; follow the user’s chosen topic. [See the reviewed example](../../docs/style-showcase/orbit-reel.mp4).

## Use

Resolve this skill folder from the base directory shown when the skill loads. Its `build.py` resolves the shared kit through that real path, including when installed as a symlink. Run:

```bash
python3 /path/to/skills/orbit-reel/build.py /path/to/spec.json
```

With no spec, the command reproduces the included silent sample into the repository’s `.work/` directory. `--prepare-only` builds an editable composition without rendering. Python 3.9+, ffmpeg/ffprobe and Node.js 22+/npm are required. The first build downloads pinned GSAP 3.15.0 into the ignored vendor cache; rendering uses HyperFrames 0.8.214. No transcript or API key is needed for these short templates. [Spec and custom-footage instructions](../../docs/style-showcase/README.md).

## Adapt the treatment

Maintain a single preserve-3d scene with perspective and a frame-matched alpha presenter at z=0. Cards with negative z pass behind the speaker; positive-z cards pass across the foreground. Keep both base video and cutout on the same source offset. The example uses eight cards, a 570px horizontal orbit and 290px depth; adjust the ring to the new speaker crop. Every card’s initial pose must use an explicit timeline position of 0, so all cards exist on frame zero.

Asset keys: `banana-heels.jpg`, `blue-stairs.jpg`, `cactus.jpg`, `explainer.mp4`, `explainer_cut.webm`, `pixel-burger.jpg`, `pixel-fruit.jpg`, `red-stairs.jpg`. Full-resolution example images and source credits are in [assets/style-showcase](../../assets/style-showcase/README.md).

Supply a same-size, frame-matched alpha cutout when changing the presenter. The existing `kit/cutout.py` can create it; see the shared guide. Inspect hair and hands over both bright and dark imagery. The build helper does not perform segmentation automatically.

Keep the presenter visible from the first result frame. Use sharp photographs and clean type. Essential text and the face should clear platform overlays; let decorative imagery bleed rather than shrinking the entire composition. The sample’s captions and image anchors are starting points, not automatic tracking.

## Review and deliver

The helper validates media dimensions/duration, prepares the composition, runs the renderer check, renders and fully decodes the MP4. Inspect the first frame, the main change and the ending. Check crop anchors, text readability and matching source/cutout timing. The default is silent; preserve or add speech, SFX or music only when the user requests them. Longer edits require extending the HTML timeline and source windows; changing only the duration is insufficient.

These are local Claude Code/Codex editing workflows. The ChatGPT conversation in the showcase is an authored visual, not a built-in ChatGPT slash-command integration. Third-party image rights are documented separately from the code license in the asset directory.
