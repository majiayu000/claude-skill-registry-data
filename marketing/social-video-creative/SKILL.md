---
name: social-video-creative
description: Generate ONE on-brand short-form vertical video (Reel / Story video) for a single Aries social post at 9:16 reel scale. Use once per requested video clip. FORCES exactly one video_generate call and returns the generated_video creative_asset (localized basename + width/height/duration) plus a content_package entry stamped placement=reel / media_type=video. Paired with /social-image-creative for image posts.
---

# Social Video Creative

You generate **one** short-form vertical video for **one** social post. This skill
is the video half of Aries creative production; `/social-image-creative` is the
image half. Run this skill once per requested video clip — it is **not** optional
just because images were already generated.

## Non-negotiable execution contract

1. You **MUST call the `video_generate` tool exactly once** for this clip. Do not
   return your result until the `video_generate` call has completed (or, on
   failure, recorded the error). A requested video that produces neither a
   generated_video creative_asset nor an `artifacts.errors[]` entry is a stage
   failure — it is exactly as mandatory as `image_generate` is for an image post.
2. The video is generated **IN ADDITION TO** the requested images, never instead of
   them.
3. Render at the **vertical reel scale** below — this is a different scale from the
   feed images; never reuse a 4:5 / 1:1 image scale for video.
4. Honor the brand constraints from the brief (dark-brand near-black background,
   palette as glowing accents, no invented logo, "must avoid" list).

## Per-platform video format

| Platform / placement | Aspect | Pixels | Duration |
|---|---|---|---|
| Instagram / Facebook Reel | 9:16 vertical | 1080 × 1920 | 3–90 s (target ~15 s) |
| Instagram / Facebook Story (video) | 9:16 vertical | 1080 × 1920 | ≤ 60 s |

Always 9:16 vertical. Default to a Reel (`placement:"reel"`) unless the brief asks
for a story video.

**The video clip is always the FINAL post in the content_package** (the highest
`post_number`). The publisher links assets to posts positionally, so the reel must
be the last entry — never interleave it before the image posts.

## Workflow

1. **Read the clip brief**: concept, brand background mode + palette, target
   platform(s), and target duration (~15 s).
2. **Compose the video prompt** to 9:16, dark-brand-safe, palette accents, no
   on-screen text unless asked, no invented logo.
3. **Call `video_generate` once** with `aspect_ratio:"9:16"` and the target
   duration. Wait for it to finish. The tool returns a **localized mp4 basename**
   (a file written to the Hermes video cache) plus the rendered file's real
   metadata. **`path`, `width`, `height`, and `duration_seconds` MUST be copied
   from the `video_generate` return value — the ACTUAL localized file's basename
   and metadata, never the values you requested.** A mismatch fails closed at
   publish dispatch. Never use a remote CDN URL for `path`.
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
    "format": "reel",
    "placement": "reel",
    "media_type": "video",
    "visual_prompt": "<the video prompt you rendered>"
  },
  "creative_asset": {
    "assetId": "vid_<N>",
    "type": "generated_video",
    "media_type": "video",
    "surface": "reel",
    "path": "<basename of the localized mp4 returned by video_generate — NOT a CDN URL>",
    "width": <integer px>,
    "height": <integer px>,
    "duration_seconds": <number>,
    "mime": "video/mp4",
    "aspect_ratio": "9:16",
    "placement": <N>
  }
}
```

`width`, `height`, and `duration_seconds` are MANDATORY and must be numeric —
absent or null fails closed at publish dispatch and the clip will not publish.
`placement:"reel"` + `media_type:"video"` on the content_package entry are
load-bearing: the publisher maps the reel surface from them, so stamp them.

## Failure handling

If `video_generate` fails, record `{assetId, post_number, prompt, error}` in
`artifacts.errors[]` and continue — never discard a completed clip and never
silently omit the requested video.
