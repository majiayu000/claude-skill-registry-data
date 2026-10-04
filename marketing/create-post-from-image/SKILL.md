---
name: create-post-from-image
description: >
  Turn one image from your Marky library into several ready-to-review social posts through
  the API. Use this when you have a strong photo or graphic (a product shot, a professional
  photo, a branded design) and want to get maximum mileage out of it with multiple captions
  and angles. Picks a library image and creates several draft posts that all use it. Reads
  auth and endpoints from the marky-api skill. Also triggers on "make posts from this photo", "use this image for a post", "what can I do with this picture". To design a new image instead, see create-post-graphic.
---

# Posts From Library Image

Got one great image? Get several posts out of it. This skill takes a single image from your
library and creates a handful of draft posts, each with its own caption and angle, all
using that image.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Step 1 — find the business and pick an image

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# Browse your media library and pick one image.
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/library" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Show the user the options and let them choose. Grab the chosen item's image URL (its
`original_url`) to attach to each post. (To find a specific image fast, use
`GET /businesses/BIZ_ID/library/search?query=...`.)

If the image is on the user's computer and not in the library yet, upload it first:

```bash
curl -X POST "https://api.mymarky.ai/api/businesses/BIZ_ID/media" \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -F "file=@/path/to/photo.jpg"
```

The upload response includes the `original_url` to use below.

## Step 2 — write several angles

Decide how many posts (5 is a good default) and write a distinct caption for each. Same
image, different angle:

- A benefit-led caption (what the customer gets).
- A story or behind-the-scenes caption.
- A question hook that invites replies.
- A direct call-to-action caption.
- A short, punchy caption.

Keep each one genuinely different. The image is shared, the words should not be.

## Step 3 — create the draft posts

For each caption, create a post with `status` `NEW` (a draft) using the same image URL:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Angle 1 caption goes here.",
    "media_urls": ["ORIGINAL_URL_OF_THE_IMAGE"],
    "restrict_publish_to": ["instagram", "facebook", "linkedIn"],
    "status": "NEW"
  }'
```

Repeat for each angle. Image posts can target every platform except TikTok (which needs
video).

## Step 4 — review and hand off

List the new drafts so the user can review them:

```bash
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/posts?status=NEW" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Show the set and ask which to keep. To schedule the keepers, use the `schedule-posts`
skill, or schedule directly with
`POST /businesses/BIZ_ID/posts/POST_ID/schedule`.

## Tips

- This is perfect for evergreen visuals: a hero product shot, a team photo, a signature
  graphic. One asset, a week of posts.
- Space the posts out so the same image does not show up two days in a row.
- Pair with the `review-performance` skill to find which of your images already perform,
  then repurpose those.
