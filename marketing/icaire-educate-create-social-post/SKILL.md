---
name: icaire-educate-create-social-post
description: Create a complete ICAIRE Educate social_post campaign item with text content, caption, CTA, infographic, motion graphic, QR/link validation, media upload, and MCP read-back. Use when drafting, creating, updating, or packaging a social post for an ICAIRE Educate programme, cohort, workshop, registration campaign, or outreach campaign.
---

# ICAIRE Educate: Create Social Post

Create one complete `social_post` campaign item. A complete visual-led social
post includes text content, caption or description, a static infographic when
requested, and a motion graphic when requested.

## Inputs

Confirm:

- campaign item name and platform
- audience and message angle
- registration or destination URL
- planned publish date and sequence order
- CTA and QR requirement
- media mix: text-only, infographic, motion graphic, carousel, or mixed media

## Workflow

1. Read the campaign map and existing MCP campaign items.
2. Draft the post body and caption in clear ICAIRE language.
3. Use `icaire-educate-create-social-infographic` for static media.
4. Use `icaire-educate-create-social-motion-graphic` for MP4 motion media.
5. Create or update the `social_post` item through ICAIRE Educate MCP.
6. Upload media through `upload_outreach_campaign_media`.
7. Read back the item with media and verify the fields.

## Content Requirements

- Include a clear CTA in the post text.
- Include the destination link when useful, even if the visual has a QR code.
- For registration campaigns, use a confirmed registration URL and QR code when
  relevant.
- Do not treat an image-only item as complete when the campaign needs text.
- Keep claims specific, factual, and approval-safe.

## Output

Return:

- `Post Body`
- `Caption`
- `CTA URL`
- `Media`
- `MCP Item`
- `Verification`

## Guardrails

- Do not publish posts.
- Do not invent dates, URLs, approvals, handles, or partner tags.
- Do not upload media before visual or frame inspection.
- Do not create campaign items without planned dates and sequence order.
