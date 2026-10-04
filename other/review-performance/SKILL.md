---
name: review-performance
description: >
  Review how your social media content is performing through the Marky API, find what is
  working, and turn it into a concrete plan. Use this when you want to know your top posts,
  follower growth, and which topics, formats, and platforms get the best engagement, then
  get specific recommendations (and optionally act on them). Pulls per-post stats, account
  stats, and your post history. Reads auth and endpoints from the marky-api skill. Also triggers on "how are my posts doing", "what's working", "top posts last month". For a quick queue/account status, use /marky-status.
---

# Review Performance

Find out what is actually working on your socials and what to do more of. This skill reads
your real engagement numbers through the Marky API, looks for patterns, and gives you
specific, data-backed recommendations.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

Everything here uses only read endpoints, so it is safe to run anytime.


## Cut by metadata tags

Posts created by agents carry `metadata` (media_type / format / hook / topic — see
"Tag every post" in the marky-api skill). When enough tagged posts have stats, group
engagement by each key and report which values win — "diagrams out-engage photos 2:1",
"question hooks beat bold claims". This is the highest-signal section of the review;
lead with it when tags exist, and note when the sample is too small to trust (<5 posts
per bucket is directional only).

## Step 1 — find your business and connected accounts

Two MCP tools: `list_businesses` (copy the id you want as `business_id`), then
`list_connected_social_accounts` on that business (copy each integration `id`, and note
its `platform` and `status`).

If no accounts are connected, stop and tell the user to connect a social account in the
[dashboard](https://app.mymarky.ai) first. Stats only exist for connected platforms.

## Step 2 — pull the numbers

Pull three things: account-level stats, the posts published on each platform (with their
engagement), and per-post detail when you want to go deeper.

- `get_integration_stats(business_id, integration_id)` — account-level audience stats
  (followers, growth) for one connected account.
- `list_integration_posts(business_id, integration_id)` — posts published on that
  platform, each with its engagement numbers. This includes posts published OUTSIDE
  Marky, so it is the true account picture; `get_external_post_stats` drills into one
  of those external posts.
- `get_post_analytics(business_id, post_id)` — engagement for one specific Marky post
  (across the platforms it went to).

Repeat the account/posts calls for each connected integration so you can compare platforms.

To tie performance back to what you posted about, also list your posts and topics:

`list_posts(business_id)` for your post history (filter by status if you like), and
`list_topics(business_id)` so you can group results by topic.

If the business has a Google Business profile connected, you can also pull customer
reviews to round out the picture (reviewer, star rating, text, and any reply):

`list_google_reviews(business_id, order_by="rating desc")` — newest first by default;
`order_by` also takes `rating`.

## Step 3 — find the patterns

Compare across a few dimensions and write down what stands out:

- **Top posts.** Which 3-5 posts got the most engagement? What do they have in common?
- **By topic.** Group posts by their `topic_id` and compare average engagement. Which
  topics pull their weight and which are dead weight?
- **By format.** Compare image posts vs video vs text. One format usually wins.
- **By platform.** Average engagement per platform. Some platforms reward different content.
- **Follower growth.** Is the audience growing, flat, or shrinking on each platform?

## Step 4 — recommend and (optionally) act

Present a four-tier action plan. Lead with the result, not the metric, and cite the
specific posts behind every recommendation — a rec with no post behind it is a guess:

- **Quick wins** — do this week, low effort ("Your how-to posts get ~3x the engagement
  of your promo posts — post two more how-tos").
- **Strategic shifts** — change the mix ("Video outperforms image on TikTok but image
  wins on LinkedIn. Match format to platform").
- **Experiments** — worth testing, not yet proven ("Topic 'client wins' is your best
  performer on 2 posts — small sample; run 3 more before concluding").
- **Stop doing** — the negative space most reviews skip ("Hashtag-wall captions are your
  bottom quartile on LinkedIn — drop them").

Benchmark against the business's OWN averages, not platform folklore — "good" is
whatever beats their last 90 days. Flag every thin sample (<5 posts per bucket is
directional only).

Then offer to act on it with the writing skills:

- **Save the learnings.** Offer to append the data-backed findings to the business's
  `performance-learnings.md` (see "Performance learnings" in the `marky-api` skill for
  the file's home and format). Creation skills read it before drafting, so a saved
  learning steers every future batch. Show the exact lines first; write only on a yes.
- Add or sharpen topics with the `suggest-topics` skill.
- Produce the next batch with the `schedule-posts` or `plan-social-content` skill, leaning
  into the winning topics and formats.

## Notes and limits

- The API gives you per-post and per-account engagement plus your post and topic lists.
  Group and compare those yourself, the API does not return pre-aggregated leaderboards.
- Posts are linked to a `topic_id`, so you can group by topic. Categories now have their
  own endpoints too (`GET /businesses/{id}/categories`), so you can roll topics up by
  category if you want a higher-level cut.
- Stats are read-only here. Acting on the findings (new topics, new posts) happens through
  the other skills.
