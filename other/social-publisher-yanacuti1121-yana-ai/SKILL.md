---
name: social-publisher
description: Agent-driven social media scheduling and publishing via SocialClaw across 13 platforms — X, LinkedIn, Instagram, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, Pinterest, Facebook, Threads, Bluesky.
license: MIT
source: https://github.com/affaan-m/ECC
---

# Social Publisher

**Trigger phrases:** "publish to social", "schedule post", "cross-post", "SocialClaw", "post to LinkedIn", "distribute content"

## Platforms (13)

X · LinkedIn · Instagram · TikTok · Discord · Telegram · YouTube · Reddit · WordPress · Pinterest · Facebook · Threads · Bluesky

## SocialClaw CLI

```bash
socialclaw auth login
socialclaw post --content "Text" --platforms x,linkedin
socialclaw schedule --content "Text" --platforms x,linkedin --time "2026-06-01T09:00:00Z"
socialclaw post --file ./content.md --platforms all
socialclaw post --content "Caption" --media ./image.png --platforms instagram,x
```

## Platform Formatting

| Platform | Limit | Best time (UTC) |
|----------|-------|-----------------|
| X | 280 | 14:00–16:00 |
| LinkedIn | 3000 | 08:00–10:00 |
| Instagram | 2200 | 11:00–13:00 |
| TikTok | 2200 | 19:00–21:00 |
| Threads | 500 | 09:00–11:00 |

## Content Adaptation

Same message, different format per platform:

```
LinkedIn: Long-form, 3-5 line paragraphs, 3 hashtags max
X: Thread hook tweet + 7 insight tweets + CTA tweet
Instagram: Short caption + 10-15 hashtags
Reddit: Value-first, no pitch, matches sub culture
```

## Anti-Fake-Pass

```
❌ Same copy on all platforms — reads as spam
❌ Post all platforms simultaneously — algorithm penalizes
❌ No engagement monitoring first 2 hours
❌ More than 3 hashtags on LinkedIn
```
