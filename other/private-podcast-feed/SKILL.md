---
name: private-podcast-feed
description: >-
  Use when publishing a private MP3+RSS feed for self-subscription. Covers
  itunes:block, token-prefixed URLs, ID3 CHAP/CTOC chapters for Overcast
  skip-ahead, and the Overcast refresh ping. Triggers: private podcast, RSS
  feed for Overcast, self-hosted podcast, private audio feed, MP3 RSS, personal
  podcast, chapter markers, Overcast ping, podcast XML, itunes:block.
globs: []
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.1.0"
---

# private-podcast-feed

Publishes a private MP3+RSS feed for self-subscription in Overcast (or any
podcast client). "Private" means URL obscurity via token prefix and
`itunes:block=Yes` to keep it out of public indexes. Not cryptographic access
control — the feed URL is the only secret.

## 1. `podcast@2.0.1` Named Export

Use the **named** export — the default export does not work:

```ts
import { podcast } from "podcast";   // ✅ named — correct
import podcast from "podcast";        // ❌ default — fails at runtime (R3 gotcha)
```

## 2. `itunes:block=Yes` via `customElements`

The typed `FeedITunes` interface does not expose `itunesBlock`. The only
correct path is the `customElements` array:

```ts
const feed = new podcast({
  title: "My Private Feed",
  feedUrl,
  siteUrl: new URL(feedUrl).origin,
  customElements: [{ "itunes:block": "Yes" }],  // keeps feed out of public indexes
});
```

Without this, the feed may be discovered and indexed by Apple Podcasts search.

## 3. Token-Prefixed URL

Serve the feed at `/p/<32-hex>/feed.xml`. The 32-hex token is 128 bits of URL
obscurity — anyone with the URL can subscribe.

```
https://your-host.com/p/5042a002464df562718eef84ac1316f5/feed.xml
```

Generate a token: `openssl rand -hex 16`

Gitignore `.token` if you store the raw token on disk. Note: **this is NOT
access control** — the URL is the only barrier. Do not store sensitive content.

## 4. ID3 CHAP/CTOC Chapter Frames

Inject chapters post-ffmpeg via mutagen so Overcast shows skippable chapters:

```python
# inject_chapters.py (bundled in text-to-speech skill)
inject(mp3_path, [
    {"start_ms": 0,       "title": "Introduction"},
    {"start_ms": 125000,  "title": "Section Two"},
])
```

Chapters must be strictly increasing by `start_ms`. End time of chapter N is
set to start time of N+1; last chapter ends at the MP3's total duration.

If using the `text-to-speech` skill, chapters are injected automatically during
render when `chapters.json` is present.

## 5. Static-Hosting Pattern

The feed needs an HTTPS host returning correct content-types:

```
feed.xml   → Content-Type: text/xml
*.mp3      → Content-Type: audio/mpeg
```

Any static hosting platform works (Cloudflare R2, S3, Caddy, nginx). Podcast
clients revalidate the feed URL periodically — the URL must be stable.

## 6. Overcast Refresh Ping

After publishing a new episode, ping Overcast to trigger an immediate fetch:

```bash
${CLAUDE_SKILL_DIR}/scripts/ping-overcast.sh https://your-host.com/p/<token>/
```

The script is idempotent — safe to call on every feed regeneration. It pings
`https://overcast.fm/ping?urlprefix=<encoded-prefix>` and exits 0 on HTTP 2xx.

## 7. Sanity Verification

```bash
# Feed responds with correct type
curl -I <feed-url>

# itunes:block is set
curl -s <feed-url> | grep "itunes:block"   # must print "Yes"

# Item count
curl -s <feed-url> | xmllint --xpath 'count(//item)' -

# MP3 URL responds
curl -I <mp3-url>   # expect: HTTP/2 200, content-type: audio/mpeg
```
