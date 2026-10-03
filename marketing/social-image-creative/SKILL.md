---
name: social-image-creative
description: Generate ONE on-brand still-image creative for a single Aries social post at the correct per-platform scale. Use once per content_package post whose media is an image (feed / story-image). FORCES exactly one image_generate call and returns the generated_image creative_asset plus a content_package entry stamped with its placement. Paired with /social-video-creative for video posts.
---

# Social Image Creative

You generate **one** still image for **one** social post. This skill is the image
half of Aries creative production; `/social-video-creative` is the video half. Run
this skill once per post that needs an image — never batch, never skip.

## Non-negotiable execution contract

1. You **MUST call the `image_generate` tool exactly once** for this post. Do not
   return your result until the `image_generate` call has completed (or, on
   `success:false`, recorded the failure). Returning a post with no rendered image
   is a failure.
2. Render at the **per-platform image scale** below — never reuse a video/vertical
   scale for a feed image.
3. Honor the brand constraints from the production brief (background mode, palette,
   logo rule, "must avoid" list). For a dark brand the background MUST be
   near-black; a light/white/studio background is a brand violation.

## Per-platform image format (pick by the post's primary platform)

| Platform / placement | Aspect | Pixels | Notes |
|---|---|---|---|
| Instagram feed | 4:5 portrait | 1080 × 1350 | Aries default feed scale |
| Facebook feed | 1:1 square | 1080 × 1080 | square reads on both feed + grid |
| Instagram / Facebook story (image) | 9:16 vertical | 1080 × 1920 | full-bleed, keep text off the edges |

If a post targets both Instagram and Facebook, render once at 4:5 (1080 × 1350) —
it crops acceptably into the Facebook feed.

## Workflow

1. **Read the brief** for this post: hook, body, CTA, brand background mode +
   palette, logo rule, and the post's platform(s)/placement.
2. **Compose the visual prompt** to the platform scale above, dark-brand-safe,
   palette as accents, no invented logo.
3. **Call `image_generate` once** at the chosen pixel size. Wait for it to finish.
4. **Return** the asset + the post copy:

```json
{
  "content_package_entry": {
    "post_number": <N>,
    "theme": "<short theme>",
    "hook": "<hook>",
    "body": "<2-4 sentences>",
    "cta": "<CTA>",
    "hashtags": ["#tag1", "#tag2", "#tag3"],
    "platforms": ["instagram", "facebook"],
    "format": "single_image",
    "placement": "feed",
    "media_type": "image",
    "visual_prompt": "<the prompt you rendered>"
  },
  "creative_asset": {
    "assetId": "img_<N>",
    "type": "generated_image",
    "media_type": "image",
    "path": "<absolute path returned by image_generate>",
    "width": <integer px you rendered>,
    "height": <integer px you rendered>,
    "placement": <N>,
    "prompt": "<the rendered prompt>"
  }
}
```

`placement` on the content_package entry is load-bearing downstream: `feed` for a
feed image, `story` for a story image. Stamp it correctly — the publisher maps the
post surface from it.

## Failure handling

If `image_generate` returns `success:false`, record `{assetId, post_number,
prompt, error}` in `artifacts.errors[]` and continue — never silently drop the
post.
