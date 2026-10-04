---
name: create-post-variations
description: >
  Turn one of your existing posts into several fresh variations through the Marky API. Use
  this when a post did well (or you just have one you like) and you want more posts in the
  same spirit, with new angles, new wording, or a specific call-to-action link. Lists your
  past posts, lets you pick one, and creates new drafts you can review and schedule. Reads
  auth and endpoints from the marky-api skill. Also triggers on "repurpose this post", "more like this one", "remix my best post". For a full week planned from scratch, see plan-social-content.
---

# Repurpose Posts

Squeeze more mileage out of content you already have. Pick a past post and spin it into
several new draft variations with fresh wording and angles, optionally pointing at a
specific link.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Step 1 — find the business and pick a source post

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# List recent posts so the user can choose one to repurpose.
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/posts" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Show the user a short list and let them pick. If you want the full caption and any attached
media of the chosen one:

```bash
curl https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Note the original `caption` and its `media_urls` (you can reuse the same media in the
variations, or leave it off).

## Step 2 — write the variations

Decide how many variations (5 is a good default) and what should change. Keep the core
message, vary the rest:

- **New angle.** Reframe the same idea with a different hook pattern — question, bold
  claim, story open, stat, contrarian, before/after, confession (the full named palette
  with anti-patterns lives in the `plan-social-content` skill's "Hooks" section). The
  user's brand rules and measured learnings outrank the palette.
- **New wording.** Do not just shuffle words. Each variation should read as its own post.
- **Optional CTA link.** If the user wants every variation to drive to one link, append it
  to each caption.

Ask the user for the link if they mentioned wanting one, otherwise skip it.

## Step 3 — create each variation as a draft

For each variation, create a new post with `status` `NEW` (a draft) so the user can review
before anything is scheduled:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Variation 1 caption. Different hook, same core message. https://your-link.example",
    "media_urls": ["ORIGINAL_MEDIA_URL_OR_OMIT"],
    "restrict_publish_to": ["instagram", "facebook", "linkedIn"],
    "status": "NEW"
  }'
```

Repeat for each variation. Reuse the source post's `media_urls` if it makes sense, or drop
the field for text-only variations (text-only posts can only target `facebook` and
`linkedIn`).

## Step 4 — review and hand off

List the new drafts so the user can see them all:

```bash
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/posts?status=NEW" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Show the variations and ask which to keep. To schedule the keepers, use the
`schedule-posts` skill, or schedule directly:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID/schedule \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "scheduled_publish_time": "2026-04-10T09:00:00Z" }'
```

## Tips

- Space repurposed variations out over days or weeks. Do not post five near-identical
  versions back to back.
- Each variation should stand on its own. If two read the same, rewrite one.
- Repurposing a proven post is one of the highest-leverage things you can do. Pair this
  with the `review-performance` skill to find which posts are worth repurposing.
