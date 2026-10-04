---
name: suggest-topics
description: >
  Suggest fresh content topics and manage your Marky content topics through the API. Use
  this when your posts feel repetitive or off-target, you want new things to post about, or
  you want to add, edit, enable, disable, or remove topics. Topics steer what Marky writes
  about, so a good topic list is the difference between focused content and random noise.
  Reads auth and endpoints from the marky-api skill. Also triggers on "what should I post about", "new content ideas", "my posts feel repetitive", "add a topic".
---

# Suggest Topics

Topics tell Marky what to write about. This skill audits your current topics, suggests new
ones that fill gaps, and lets you add, edit, or remove them through the API.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Step 1 — understand the business and what exists today

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# Read the business profile for context (what they do, who they serve).
curl https://api.mymarky.ai/api/businesses/BIZ_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# The topics they already have.
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/topics" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Read the existing topics critically. Are they specific enough? Vague topics like "industry
news" produce vague posts. Specific ones like "how HVAC maintenance saves money in winter"
produce focused posts.

## Step 2 — suggest new topics

Based on the business profile, the audience it serves, and the gaps in the current list,
suggest a handful of specific new topics. Good topics:

- Are specific, not generic ("client success stories", not "our customers").
- Map to what the audience actually cares about, not just what the business wants to sell.
- Cover a healthy mix: educational, authority-building, connection, and conversion.

If the agent running this skill can browse the web, use it to check what is trending in the
business's industry and fold that in. Present each suggestion with a one-line reason.

## Step 3 — create, edit, or remove topics

After the user approves, apply the changes.

```bash
# Create a topic. title + body are the substance; body guides what posts to write.
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/topics \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Winter HVAC maintenance tips",
    "body": "Practical tips on maintaining heating systems in winter, framed around saving money and avoiding breakdowns.",
    "enabled": true
  }'

# Edit a topic (sharpen the body, rename, or enable/disable it).
curl -X PATCH https://api.mymarky.ai/api/businesses/BIZ_ID/topics/TOPIC_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "body": "Sharper, more specific guidance here.", "enabled": true }'

# Disable a topic without deleting it (set enabled false).
curl -X PATCH https://api.mymarky.ai/api/businesses/BIZ_ID/topics/TOPIC_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "enabled": false }'

# Delete a topic for good.
curl -X DELETE https://api.mymarky.ai/api/businesses/BIZ_ID/topics/TOPIC_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Prefer disabling over deleting when a topic is just out of season. Delete only the ones
that are genuinely wrong or duplicates, and confirm first.

## Step 4 — put the topics to work

Once the topic list is solid, generate posts from it. Marky drafts on-brand copy from a
topic automatically (brand voice, colors, and logo applied server-side):

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/generate \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Winter HVAC maintenance tips",
    "count": 3
  }'
```

Or hand off to the `schedule-posts` / `plan-social-content` skill for a full batch.

## Notes and limits

- Topics can belong to a **category** (via `category_id`), and categories now have full
  CRUD: `GET|POST /businesses/{id}/categories` and
  `GET|PATCH|DELETE /businesses/{id}/categories/{category_id}` (a category takes `name`,
  optional `description`, and a hex `color`). Create a category, then pass its `id` as a
  topic's `category_id`. Most users do fine working at the topic level.
- `enabled` controls whether a topic is in rotation. There is no `is_active` field.
- A focused, specific topic list is one of the strongest levers for content quality. Pair
  this with the `review-performance` skill to see which topics actually earn engagement.
