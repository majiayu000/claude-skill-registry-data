---
name: icaire-educate-create-programme-campaign
description: Create or update a complete ICAIRE Educate programme, cohort, workshop, or registration campaign using the ICAIRE Educate MCP. Use when the user asks to create a programme campaign, launch campaign, registration campaign, outreach package, email/social sequence, or campaign items for ICAIRE Educate.
---

# ICAIRE Educate: Create Programme Campaign

Route and assemble a complete ICAIRE Educate campaign. Use the ICAIRE Educate
MCP as the default write path; do not seed campaign rows through SQL migrations
unless the user explicitly requests app/schema fallback work.

## Required Context

- Discover or read ICAIRE Educate MCP tools before writing. Expected tools
  include `list_outreach_campaigns`, `get_outreach_campaign`,
  `create_outreach_campaign`, `update_outreach_campaign`,
  `list_outreach_campaign_items`, `create_outreach_campaign_item`,
  `update_outreach_campaign_item`, and `upload_outreach_campaign_media`.
- If the expected MCP tools appear missing or partially loaded, use the
  `find-missing-tools` skill before concluding they are unavailable.
- Read the programme, cohort, workshop, registration page, or campaign facts
  from ICAIRE Educate MCP and ICAIRE context before drafting.
- Confirm the registration URL before generating QR codes or final CTAs.

## Campaign Map

Create a campaign map before making MCP writes:

- campaign name, programme/cohort/event, audience, objective, CTA, URL
- publishing window and registration deadline
- required item types and owners
- sequence order and planned dates
- approval questions, claims to avoid, partner dependencies

Default registration cadence:

- announcement
- one week reminder
- three day reminder
- same day reminder

Use absolute dates when planning around a real programme date.

## Item Routing

Route item creation to the focused skills:

- `icaire-educate-create-first-party-email` for ICAIRE-owned
  `sendable_email` announcement and reminder emails.
- `icaire-educate-find-campaign-partners` when partner forwarding targets are
  unknown or underspecified.
- `icaire-educate-create-third-party-email` for partner-ready
  `third_party_email` items.
- `icaire-educate-create-social-post` for each `social_post` item.

When multiple independent items are ready, spin up subagents for parallel
drafting, partner research, or media production. Keep the campaign map and final
MCP writes coordinated in the main thread.

## MCP Write Contract

- Create or update the campaign with `create_outreach_campaign` or
  `update_outreach_campaign`.
- Create child items with `create_outreach_campaign_item`.
- Use item types exactly: `sendable_email`, `third_party_email`, `social_post`.
- Set `publish_date` for scheduled posts and third-party forwarding copy.
- Preserve email send dates and filters for first-party sendable emails.
- Set `sequence_order` before creating campaign items.
- Upload image or video media through `upload_outreach_campaign_media`.
- Read back the campaign with items and media after every write batch.

## Verification

Verify:

- MCP read-back shows the expected campaign, items, dates, statuses, and media.
- every registration CTA uses the confirmed URL
- every QR code decodes to the confirmed URL
- first-party emails are not sent automatically
- third-party emails are copy-ready and contain no recipient variables
- social posts have text content as well as media when media is requested
- static and motion assets were visually inspected

## Output

Return:

- `Campaign Map`
- `Timeline`
- `MCP Writes`
- `Item Summary`
- `Verification`
- `Open Approvals`

## Guardrails

- Do not send emails, publish posts, or claim partner approval automatically.
- Do not invent dates, URLs, partner names, endorsements, seat counts, or
  registration facts.
- Do not use SQL seeding as the normal campaign creation path.
- Do not create campaign items without planned dates and sequence order.
