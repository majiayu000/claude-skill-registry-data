---
name: create-post-countdown
description: >
  Build a countdown campaign for an upcoming event through the Marky API: a series of
  on-brand posts, each with a different angle, scheduled at the right intervals leading up
  to the date. Use this when you have an event (launch, sale, webinar, opening, holiday
  promo) and want a sequence of posts that build anticipation and end with a final reminder.
  Reads auth and endpoints from the marky-api skill. Also triggers on "countdown to my event", "posts leading up to the launch", "build hype for my webinar". For a single event post, see schedule-posts.
---

# Event Countdown Posts

Turn one event into a sequence of posts that build excitement over time. Each post takes a
different angle (announce, tease details, build anticipation, final reminder) and gets
scheduled at a sensible interval before the event.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Step 1 — gather the event details

Ask the user for whatever is missing:

- What is the event? (launch, sale, webinar, opening, etc.)
- The exact date and time, and the timezone.
- The key details to highlight (offer, location, link, who it is for).
- How many posts they want (a 5-post countdown is a good default).
- Which connected platforms to post to.

## Step 2 — find the business and platforms

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

curl https://api.mymarky.ai/api/businesses/BIZ_ID/integrations \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Only target platforms whose `status` is `valid`.

## Step 3 — plan the schedule

Work backward from the event date. A 5-post countdown usually lands like this:

| Post | Angle | When to publish |
| :--- | :--- | :--- |
| 1 | Announce it exists | ~7 days before |
| 2 | Tease the details / the offer | ~4 days before |
| 3 | Build anticipation (why it matters) | ~2 days before |
| 4 | "Tomorrow!" reminder | 1 day before |
| 5 | "Today / last chance" final reminder | day of, a few hours before |

Adjust the spacing to how far out the event is. Confirm the plan with the user before
creating anything.

## Step 4 — create each post

You can write each caption yourself (full control) or let Marky draft on-brand copy from
the event description. Either way you end up with a post you then schedule.

Write it yourself:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Announce-angle caption for the event.",
    "restrict_publish_to": ["instagram", "facebook", "linkedIn"]
  }'
```

Or let Marky draft on-brand copy (brand voice, colors, and logo are applied automatically).
You choose target platforms later when you schedule, so `generate` only needs the idea:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/generate \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_idea": "Announce our Spring Sale, 20% off, this Saturday only.",
    "count": 1
  }'
```

`generate` returns a `job_id`. Poll `GET /businesses/BIZ_ID/jobs/{job_id}` until it is
`completed`, then list the new drafts with
`GET /businesses/BIZ_ID/posts?status=NEW` to get each new `post_id`.

## Step 5 — schedule each post at its interval

For each post, schedule it at the time you planned in Step 3 (ISO 8601, in the future):

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID/schedule \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_publish_time": "2026-04-10T09:00:00Z",
    "restrict_publish_to": ["instagram", "facebook", "linkedIn"]
  }'
```

Convert the user's local event time to UTC for `scheduled_publish_time`. Double-check the
math so a 9am-local reminder does not go out in the middle of the night.

## Step 6 — confirm

List the scheduled posts back to the user so they can see the full countdown:

```bash
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/posts?status=SCHEDULED" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Show the sequence (each angle + its publish time) and confirm it is ready.

## Tips

- Vary the angle on every post. Five "don't miss our event!" posts is noise. Announce,
  tease, explain the value, remind, last-call.
- Keep the final reminder short and direct with a clear next step.
- If the user gives you photos or video for the event, upload them first with
  `POST /businesses/{id}/media` and pass the returned `original_url` in each post's
  `media_urls`.
