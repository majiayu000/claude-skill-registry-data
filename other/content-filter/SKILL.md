---
name: content-filter
description: >
  Content safety filter for Buzz auto-posts on Twitter.
  Checks all outgoing tweets against blocked words, patterns,
  and compliance rules before posting. Prevents price predictions,
  financial advice, urgency language, and profanity.
---

# Content Filter — Twitter Auto-Post Safety

## Purpose

Every tweet Buzz auto-posts MUST pass through this filter first.
If any blocked word or pattern is detected, the tweet is REJECTED
and logged to Telegram as [🚫 FILTER BLOCKED].

## Blocked Words

```
guaranteed, moon, mooning, 100x, 1000x, pump, pumping,
not financial advice, NFA, DYOR, buy now, don't miss,
last chance, to the moon, easy money, free money,
going to explode, next [any token], [any token] killer,
rug, scam, shit, fuck, damn, hell,
guaranteed returns, passive income, get rich
```

## Blocked Patterns

- Price predictions: "will reach $X", "target $X", "price target"
- Financial advice: "you should buy", "great investment", "don't sell"
- Urgency: "hurry", "last chance", "before it's too late", "limited time"
- Comparison attacks: "better than [project]", "[project] killer", "[project] is dead"
- AI self-identification in engage replies: "I'm an AI", "I'm a bot", "I'm Buzz"
- Commission/pricing: "$15K", "$5K fee", "$10K liquidity", "$1K commission"

## Usage

```javascript
const { checkContent } = require("./content-filter");

const result = checkContent(tweetText);
if (!result.passed) {
  // REJECT — do not post
  logToTelegram(`[🚫 FILTER BLOCKED] ${result.reason}: "${result.matched}"`);
} else {
  // SAFE — proceed to post
  postTweet(tweetText);
}
```

## Rules

- Filter runs on ALL auto-posts (scan summaries, deploy confirms, engage, threads, digests)
- Filter does NOT run on drafts queued for Ogie approval (he reviews manually)
- 3+ blocks in 1 hour → auto /tweet_stop + alert Ogie
- Filter is NOT configurable by users — only by Ogie via Telegram /config command
