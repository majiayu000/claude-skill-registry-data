---
name: icaire-educate-review-social-posts
description: Run a step-by-step human review of current ICAIRE Educate social_post campaign items, showing each post with every attached media item, including both static images and motion graphics, collecting user approval or feedback before moving to the next post, and applying requested changes through the ICAIRE Educate MCP. Use when the user asks to review current social posts, walk through social campaign posts, approve campaign visuals, inspect Educate social_post items, or give feedback on planned ICAIRE Educate posts.
---

# ICAIRE Educate: Review Social Posts

Guide the user through current ICAIRE Educate `social_post` campaign items one
at a time. The core behavior is interactive review, not batch summarization.

## Required Context

- Use ICAIRE Educate MCP as the source of truth for campaigns, campaign items,
  and media.
- Expected tools include `list_outreach_campaigns`, `get_outreach_campaign`,
  `list_outreach_campaign_items`, `get_outreach_campaign_item`,
  `update_outreach_campaign_item`, and media download or signed-url access when
  available.
- If expected MCP tools are missing or only partly visible, use
  `find-missing-tools` before concluding they are unavailable.
- If the user does not specify a campaign, list candidate campaigns with counts
  of `social_post` items and ask which campaign to review.

## Review Setup

1. Fetch the selected campaign with `social_post` items and the complete media
   collection attached to each item. Do not stop after the first media result.
2. Sort by `publish_date` first, then `sequence_order`, then creation time.
3. Build a compact review queue with item name, status, platform, date, caption,
   body, and a complete media inventory for that item.
4. Do not rewrite, update, publish, archive, or delete anything before the user
   reviews the relevant item and asks for that change.

## One-At-A-Time Review Loop

For each post:

1. Show progress, such as `Post 2 of 6`.
2. Display the post details:
   - name
   - status
   - platform
   - planned date
   - caption
   - post body
   - CTA URL or QR target if known
3. Display **every media item attached to the post** inline whenever possible:
   - always show both the static image and the motion graphic when both exist
   - show all variants and attachments, not only the first result, thumbnail,
     preview, or a single representative asset
   - label each asset with its exact media name and type so the user can review
     the static and motion versions separately
   - use signed image/video URLs directly when available
   - use local downloaded files with absolute paths when the app requires local
     display
   - for motion graphics, embed or link the playable video rather than showing
     only its poster frame or thumbnail
   - if any media item cannot be displayed, still show every displayable item
     and provide the exact name, type, and access blocker for each missing item
   - if only one media type is attached, explicitly state which expected static
     image or motion graphic is missing
4. Give a short review note covering CTA clarity, QR visibility, text/media
   fit, factual risks, and obvious visual issues.
5. Stop and ask for the user's decision before moving on.

Use a simple decision prompt:

- `approve`
- `edit: ...`
- `skip`
- `stop`

Do not advance to the next post until the user responds.

## Handling Feedback

- If the user approves, record that approval in the review summary and move to
  the next post.
- If the user asks for text edits, propose the revised caption/body first unless
  the instruction is exact.
- If the user asks for media changes, route production work to
  `icaire-educate-create-social-infographic` or
  `icaire-educate-create-social-motion-graphic` as appropriate.
- Apply requested campaign-item edits through ICAIRE Educate MCP and read the
  item back before continuing.
- If media is replaced, verify the uploaded media appears on the MCP read-back
  before continuing.
- If feedback reveals a campaign-wide issue, ask whether to apply it to the
  remaining queue or only the current item.

## Review Checklist

Check each post for:

- clear CTA
- confirmed destination URL
- QR code visible and relevant for registration campaigns
- static and motion media present when expected
- motion graphic CTA and QR visible immediately when relevant
- text content present alongside visual media
- no unsupported partner, UNESCO, SDAIA, certificate, capacity, or endorsement
  claims
- no obvious typography, cropping, contrast, or logo distortion issues

## Final Summary

After the last item or when the user stops, return:

- approved posts
- edited posts and MCP read-back status
- skipped posts
- unresolved feedback
- recommended next action before publishing or sending

## Guardrails

- Do not publish social posts.
- Do not batch-approve posts.
- Do not move to the next post without the user's response.
- Do not hide media access failures behind text-only summaries.
- Do not apply changes outside the current reviewed item unless the user asks.
