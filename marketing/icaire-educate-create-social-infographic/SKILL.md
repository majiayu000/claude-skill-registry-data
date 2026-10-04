---
name: icaire-educate-create-social-infographic
description: Create static ICAIRE Educate social infographics for campaign social_post items, including ICAIRE branding, clear CTA, registration QR code when relevant, visual inspection, and media-ready output. Use when an Educate campaign needs a LinkedIn/social image, poster, carousel frame, QR visual, or static companion to a motion graphic.
---

# ICAIRE Educate: Create Social Infographic

Create static social visuals for ICAIRE Educate campaign posts.

## Requirements

- Use ICAIRE brand assets from the target app or approved brand folder.
- Include the programme/event title, practical date/time/location details when
  relevant, one clear CTA, and QR code when registration is relevant.
- Generate QR codes only from a confirmed destination URL.
- Verify the QR decodes correctly before treating the asset as ready.
- Keep the ICAIRE/UNESCO lockup appropriate, undistorted, and unboxed unless
  the approved design requires otherwise.

## Production Guidance

- Prefer deterministic local rendering, such as HTML/CSS with Playwright, for
  repeatable social dimensions.
- Use common social dimensions unless the campaign specifies otherwise.
- Save review copies in the task output folder and app-ready copies under a
  stable app asset path when they need to be uploaded or served.
- Keep generated working files out of the app repo unless they are intentional
  app assets.

## Visual Inspection

Check:

- clipped text
- cramped layout
- logo distortion
- low contrast
- QR placement and scannability
- CTA visibility
- unsupported claims

## Output

Return:

- `Image Path`
- `Dimensions`
- `CTA URL`
- `QR Verification`
- `Visual Inspection`
- `Upload Note`

## Guardrails

- Do not invent campaign identity, partner logos, or co-branding.
- Do not mark the asset ready without visual inspection.
- Do not use a QR code before confirming the target URL.
