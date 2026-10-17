---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: reading-x-posts
description: >
  Read tweets and threads from X (Twitter). Use when the user shares an
  x.com or twitter.com URL and wants to read a post or thread. Covers
  single-tweet extraction via oEmbed (no auth, instant) and full thread
  reading via Playwriter.
---

# Reading X posts

Two methods depending on what you need.

## Single tweet (oEmbed, preferred for one post)

Twitter's oEmbed endpoint returns the full text as JSON. No auth, no JS rendering, no rate limits.

```bash
curl -s 'https://publish.twitter.com/oembed?url=https://x.com/USER/status/ID' | jq -r '.html' | sed 's/<[^>]*>//g'
```

Or use `WebFetch`:

```
https://publish.twitter.com/oembed?url=https://x.com/USER/status/ID
```

The response JSON has `html` (blockquote with full tweet text), `author_name`, and `author_url`.

Limitation: oEmbed only returns the single tweet you request. It cannot fetch replies or thread continuations. You would need to know every reply's status ID upfront.

## Full thread (Playwriter)

Use Playwriter when you need the full thread, replies, or any content beyond a single post. X is JS-heavy so `webfetch`/`curl` on the page itself returns an empty shell.

```bash
# 1. Create a session
playwriter session new

# 2. Navigate to the tweet
playwriter -s <ID> -e '
state.page = await context.newPage();
await state.page.goto("https://x.com/USER/status/STATUSID", { waitUntil: "domcontentloaded" });
await waitForPageLoad({ page: state.page, timeout: 8000 });
'

# 3. Extract the full thread as markdown
playwriter -s <ID> -e '
const content = await getPageMarkdown({ page: state.page, showDiffSinceLastCall: false });
console.log(content);
'
```

`getPageMarkdown` uses Mozilla Readability (same as Firefox Reader View). It strips nav, sidebar, ads, and returns just the thread content. Much cleaner than querying individual `[data-testid="tweetText"]` elements.

## Decision rule

- **One tweet, just need the text** -> oEmbed. Instant, zero setup.
- **Full thread, replies, or visual context** -> Playwriter. Requires a session but gets everything.

Never use `webfetch` or `curl` directly on `x.com` page URLs. The HTML is an empty JS shell.
