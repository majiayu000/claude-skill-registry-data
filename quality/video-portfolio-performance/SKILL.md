---
name: video-portfolio-performance
description: Review and build video portfolio websites with mixed landscape and portrait media, strong visual direction, responsive interaction, and bounded loading cost. Not for publishing, Git operations, or deployment, which is portfolio-github-workflow.
version: 1.0.1
---

# Video Portfolio Performance

Use this skill when a portfolio site contains multiple videos or needs a visual redesign without sacrificing playback quality.

## Inspect

1. Identify the real repository and preserve its public URL.
2. Inventory media dimensions, codecs, duration, and file size.
3. Separate landscape, portrait, and square media.
4. Identify template-only or third-party work.
5. Capture desktop and mobile baselines.

## Media

- Provide a poster for every video.
- Use `preload="none"` below the fold.
- Do not autoplay multiple videos.
- Defer media outside the first viewport.
- Use `contain` when the full frame matters and `cover` only for intentional crops.
- Give each media surface a stable aspect ratio.
- Prefer web-friendly H.264/AAC versions with bounded file size.

## Design and validation

Make the work the first-viewport signal. Use one clear visual direction, restrained interaction, visible focus, touch support, and reduced-motion handling. Validate desktop/mobile framing, network cost, controls, poster fallbacks, navigation, broken paths, overlap, and console errors. Report limitations honestly.

## Example

Before, every video loads on page open:

```html
<video src="a.mp4" controls></video>   <!-- 6 个视频一起下载 -->
```

After, a poster frame shows first and the file loads on interaction:

```html
<video poster="a.jpg" preload="none" controls>
  <source data-src="a.mp4" type="video/mp4">
</video>
```

Same page, first paint drops from several megabytes to a few hundred kilobytes.
