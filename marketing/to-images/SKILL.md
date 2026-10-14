---
name: marketkit-to-images
description: Generate images for a campaign — social banners, avatars, post images, and ad creatives. Use when the campaign plan is approved and the visual assets are needed.
license: MIT
---

# To Images

Produce the visual assets for a campaign, each sized for its channel and purpose.

1. Read the campaign plan: the key messages, the voice brief, and the channels. Every image must serve a key message and fit its channel.
2. Size each asset from the [platform specs](../references/platform-specs.md) — image dimensions, aspect ratios, and safe zones per channel. Never guess a size and never reuse one channel's size for another.
3. Cover profile assets when the plan touches channel setup, launch, or rebrand. Produce the avatar and banner for each affected channel from the profile assets table, and follow its design rules: avatars render as circles and must read at 32px, banners crop per surface. Ship the pair per channel, never one without the other.
4. Respect the safe zones. On full-screen assets (stories, reels, TikTok), keep text, logos, and CTAs out of the top and bottom bands the platform's UI covers.
5. Seed each image with the campaign voice and key message so the visuals are on-brand, not generic.
6. If image generation is unavailable, say so and produce a text-only asset with a note on what the image should show. Do not fabricate an image URL.
7. Label each asset with its channel and size so it can be published without guessing.

An image that does not fit its channel's dimensions is not ready to publish. If the size is wrong, regenerate it.

Record this output in `docs/plans/` using the [doc system](../../plan-mode/references/doc-system.md).
