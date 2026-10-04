---
name: icaire-educate-create-social-motion-graphic
description: Create ICAIRE Educate social motion graphics for campaign social_post items with immediate CTA and QR visibility, gradual element reveals, Remotion/frame-driven animation, MP4 rendering, frame inspection, and media upload readiness. Use when an Educate campaign needs a motion post, video variant, animated social asset, or MP4 companion to an infographic.
---

# ICAIRE Educate: Create Social Motion Graphic

Create motion graphics for ICAIRE Educate social campaign items. The motion
graphic must be a real frame-driven animation, not a simple zoom or pan of the
static image.

## Non-Negotiables

- The CTA and QR code must be visible immediately from the opening frame when a
  registration QR is relevant.
- The animation must reveal or emphasize elements gradually, such as title,
  date, value points, partner/logo, and CTA reinforcement.
- Use Remotion or an equivalent frame-driven workflow.
- Do not create the final motion graphic with an ffmpeg-only zoom/fade pipeline.

## Workflow

1. Confirm the registration or destination URL.
2. Reuse the approved campaign visual direction or static infographic.
3. Build a Remotion composition or equivalent frame-driven animation.
4. Keep the QR and CTA visible throughout, unless the user explicitly approves a
   different treatment.
5. Render H.264 MP4 in practical social dimensions and file size.
6. Inspect representative frames, including the opening frame.
7. Upload through ICAIRE Educate MCP only after inspection.

## Inspection

Verify:

- opening-frame CTA and QR visibility
- QR remains scannable
- no text/logo collisions
- no unsupported claim appears
- animation reveals content instead of only zooming a still image
- codec, dimensions, duration, and file size are practical

## Output

Return:

- `Video Path`
- `Dimensions / Duration / Codec`
- `CTA URL`
- `Frame Inspection`
- `QR Verification`
- `Upload Note`

## Guardrails

- Do not publish posts.
- Do not commit temporary Remotion workspaces.
- Do not upload a video that has not been frame-inspected.
- Do not hide the CTA or QR behind delayed animation in registration campaigns.
