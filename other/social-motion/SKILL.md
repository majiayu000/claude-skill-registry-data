---
name: social-motion
description: Recompose motion graphics and source animations for LinkedIn, X, WeChat Moments, Xiaohongshu, and other aspect ratios. Re-layout the entire video using independent text, artwork, cards and motion paths; reserve framing or cropping for explicitly requested treatments.
---

# Social Motion

Make the whole video work in the requested ratio. Use the sibling `eric-intro-motion-skill` runtime for bundled recipes; custom films may use their own source renderer.

## Choose a method that matches the request

“Make this video 1:1 / 3:4 / 9:16” means **native recomposition** unless the user asks for another treatment. Re-layout each scene's text, graphics and animation paths. Adding a colored/blurred background, putting the existing landscape video inside a new frame, cropping it, or uniformly scaling the master is not completion of that request.

For an existing project or arbitrary film, read [native recomposition](references/native-recomposition.md). Recover its editable source first. Reuse its artwork, fonts and motion logic, then derive geometry from each target canvas. If only pixels remain, reconstruct the required layers and explain any fidelity limits. Do not substitute framing to save tokens or time.

For a bundled v1 story:

```sh
node scripts/pack.mjs --input /path/to/story.json --out /path/to/social-pack --presets moments,xiaohongshu,vertical
```

For a v2 component recipe, use sibling `eric-intro-motion-skill/scripts/compose.mjs --preset xiaohongshu`. These renderers cover their documented motifs, not arbitrary finished films. Preserve caches and start with `--formats png` to review every scene before encoding.

Presets include square 1080×1080, 3:4 1080×1440 and 9:16 1080×1920. Read [platform guidance](references/platforms.md) for destination-specific scope and dates. These are authoring choices, not guarantees about platform feed thumbnails.

## Explicit embedding or cropping

If the user specifically wants an inset video with an outer title/background, `frame.mjs --intent embed` provides it. If they request a blurred backdrop or crop, use `reframe.mjs --intent embed --mode backdrop` or `--intent crop --mode crop`. These utilities refuse an implicit native-adaptation request and always report `nativeReflow:false`.

Read [finished footage](references/finished-footage.md) only for those treatments. The flags express the chosen method; they do not authorize choosing it against the user's request.

## Review and deliver

Inspect all scenes and transition boundaries in every requested language/ratio, including phone-sized previews. Check text bounds, text overlap, artwork occlusion, motion paths and reading time. A filled canvas and valid output dimensions alone do not prove native re-layout.

For custom source renderers, [the measured audit format](references/native-recomposition.md#verify-before-delivering) and `scripts/native-audit.mjs` can check layout evidence and reject a uniformly scaled master. This supplements visual review; it does not replace it.

Render the complete timeline. Deliver MP4, requested GIFs, static posters, editable source and verification reports. Describe file geometry separately from platform behavior: platforms may still crop thumbnails, overlay controls, or change playback framing. Do not silently drop copy or audio. Preparing a pack does not authorize publishing, connecting accounts or changing profiles.
