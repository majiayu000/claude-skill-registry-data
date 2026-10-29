---
name: bots
description: Use when multi-platform bot automation hub — Telegram, Twitter/X, and
  WhatsApp bots for automated engagement, content distribution, and revenue generation.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: workflow-automation
tags:
- automation
- bots
- telegram
- twitter
- whatsapp
- productivity
- messaging
- social-media
- workflow
version: 1.0.0
category: automation
---
## Overview

This skill is the hub for multi-platform bot automation — Telegram, Twitter/X, and WhatsApp — covering engagement, content distribution, and revenue workflows. Load it when you need a bot surface wired for one or more platforms. It routes to the per-platform playbooks for setup, deployment, and monetization.


# Bots — Multi-Platform Bot Automation Hub

## Money-Making Overview

| Bot Platform | Revenue Stream | Monthly Potential | Setup Time |
|---|---|---|---|
| **Telegram Bot** | Paid channels, premium content gating, affiliate link broadcasting, crypto/alpha signals | $500-$5,000 | 2-4 hours |
| **Twitter/X Bot** | Automated content publishing, engagement farming, lead magnet delivery, affiliate threads | $300-$3,000 | 1-3 hours |
| **WhatsApp Bot** | Broadcast marketing, customer support automation, order confirmation, lead qualification | $500-$4,000 | 3-6 hours |
| **Multi-Bot Cross-Pollination** | Same content auto-distributed across all 3 platforms, amplified reach | $1,000-$8,000 | 4-8 hours |

**Total Addressable Monthly Revenue: $1,000-$12,000+**

All three platforms share a core autonomous agent architecture: listen for triggers, process intent, execute action, report outcome. The money is in volume, personalization, and converting engagement into transactions.

---

## Combined Capabilities

| Capability | Telegram | Twitter/X | WhatsApp |
|---|---|---|---|
| Automated posting | Yes (channels) | Yes (tweets/threads) | Yes (broadcasts) |
| Inbound message handling | Yes | Yes (DMs) | Yes |
| Webhook/event-driven | Yes | Yes | Yes |
| Scheduled delivery | Yes | Yes | Yes |
| Media/image sharing | Yes | Yes | Yes |
| Group/channel management | Yes | N/A | Yes (groups) |
| Payment integration | Yes (paid channels) | No native | Yes (business API) |
| User segmentation | Via bot state | Via lists | Via labels |
| Analytics | Limited | Yes (native) | Limited |
| Bot-to-human handoff | Optional | Optional | Yes |
| Affiliate link support | Yes | Yes | Yes |

---

## Telegram Bot

### Overview

Telegram bots are event-driven programs that respond to user commands, inline queries, and webhook callbacks via the Telegram Bot API (`https://api.telegram.org/bot<TOKEN>/`). They can operate in channels, groups, and private chats.

### Quick Start — Python (python-telegram-bot)

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def start(update: Update, context):
    await update.message.reply_text(
        "Welcome! I'm your automation bot.\n"
        "/subscribe — Get daily deals\n"
        "/price <product> — Check price\n"
        "/affiliate — Get affiliate links"
    )

async def subscribe(update: Update, context):
    user_id = update.effective_user.id
    # Save to DB / Redis
    await update.message.reply_text("Subscribed! You'll get daily updates.")

async def handle_message(update: Update, context):
    text = update.message.text
    # Process intent — price check, affiliate, support
    await update.message.reply_text(f"Processing: {text}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("subscribe", subscribe))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
```

### Running with Webhooks

```bash
# Set webhook URL (run once)
curl -F "url=https://yourdomain.com/webhook/telegram" \
  "https://api.telegram.org/bot$TOKEN/setWebhook"

# Test webhook
curl -X POST "https://yourdomain.com/webhook/telegram" \
  -H "Content-Type: application/json" \
  -d '{"update_id":1,"message":{"message_id":1,"chat":{"id":123},"text":"/start"}}'
```

### Advanced — Telegram Userbot (Telethon)

For full account automation — DMs, voice notes, group scraping, member extraction:

```python
from telethon import TelegramClient
import os

client = TelegramClient(
    "session_name",
    os.environ["API_ID"],
    os.environ["API_HASH"]
)

async def broadcast_to_subscribers():
    await client.start()
    subscribers = [123456, 789012]  # from DB
    for uid in subscribers:
        await client.send_message(uid, "Hot deal: 50% off!")
        await asyncio.sleep(2)  # rate limit

with client:
    client.loop.run_until_complete(broadcast_to_subscribers())
```

### Money-Making Workflows

1. **Paid Signal Channel** — Charge for access (USDT/Stripe), broadcast crypto/trading signals
2. **Affiliate Broadcast** — Automated daily/weekly broadcasts with affiliate links (Shopee, Amazon, LYNK)
3. **Lead Magnet Delivery** — Users request free PDF/guide via command, bot DMs download link + upsell CTA
4. **Support Automation** — Handle 80% of FAQ, route complex issues to human; saves $500-$2,000/mo in support costs
5. **Bot-as-a-Service** — White-label bot for businesses: $50-$200/mo per client

---

## Twitter/X Bot

### Overview

Twitter bots automate posting, engagement (like/retweet/follow), DM responses, and content curation via the Twitter API v2. Use OAuth 2.0 with PKCE or OAuth 1.0a for user actions.

### Quick Start — Python (tweepy)

```python
import tweepy
import os

client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
)

# Post tweet
tweet = client.create_tweet(text="Check out this deal: https://example.com/deal")
print(f"Posted: {tweet.data['id']}")

# Reply to mentions
mentions = client.get_users_mentions(
    id=os.environ["TWITTER_USER_ID"],
    max_results=10
)
for mention in mentions.data:
    client.create_tweet(
        text="Thanks for the mention! DM me for exclusive deals.",
        in_reply_to_tweet_id=mention.id
    )

# Schedule a thread
thread = [
    "1/5 I built a bot that finds cheap flights ✈️",
    "2/5 It searches 100+ airlines every hour...",
    "3/5 When it finds a deal under $200, it tweets...",
    "4/5 Here's the open-source repo: https://github.com/...",
    "5/5 Follow for more automation tips!"
]
for i, line in enumerate(thread):
    reply_to = None if i == 0 else prev_id
    resp = client.create_tweet(text=line, in_reply_to_tweet_id=reply_to)
    prev_id = resp.data['id']
    time.sleep(5)  # avoid rate limits
```

### Scheduled Content + Engagement Loop

```bash
#!/bin/bash
# crontab: 0 */3 * * * /home/user/twitter-bot/publish.sh
python3 -c "
import tweepy, os
from datetime import datetime

client = tweepy.Client(...)
# Pull from content queue (Redis/JSON file)
posts = [
    'Morning tip: automate your DMs to capture leads 24/7',
    'Just hit $500 in affiliate commissions this week!',
    'New blog post: How I built a WhatsApp bot in 2 hours'
]
day_hour = datetime.now().hour // 8
client.create_tweet(text=posts[day_hour % len(posts)])
"
```

### Money-Making Workflows

1. **Affiliate Thread Bot** — Auto-post daily threads with affiliate links; 0.5-2% conversion rate
2. **Lead Gen Bot** — Auto-DM new followers with lead magnet link; capture email
3. **Content Curator** — Retweet/like industry content, build authority, drive bio link clicks
4. **Engagement Farmer** — Like/retweet targeted hashtags; grow audience to 10K+ for monetization
5. **Brand Monitoring** — Alert on brand mentions, auto-reply with customer support link

### Best Practices

- Stay under 50 tweets/day for new accounts; ramp up gradually
- Use 1-Click Login / OAuth for user-facing apps
- Never auto-DM aggressively — triggers spam flag
- Mix automated content with manual replies for authenticity

---

## WhatsApp Bot

### Overview

WhatsApp bots integrate via the **WhatsApp Business API** (Meta-approved) or automation tools like `whatsapp-web.js` (unofficial, browser-based). For production monetization, use the official Business API with a BSP (Business Solution Provider).

### Quick Start — whatsapp-web.js (unofficial, rapid prototyping)

```javascript
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => qrcode.generate(qr, { small: true }));

client.on('ready', () => console.log('WhatsApp bot ready!'));

client.on('message', async msg => {
    const text = msg.body.toLowerCase();

    if (text === '!deals') {
        await msg.reply('🔥 *Today\'s Hot Deals*\n1. Product A — $19 (50% off)\n2. Product B — $29 (30% off)\n\nReply "buy A" to order!');
    } else if (text.startsWith('buy ')) {
        const product = text.replace('buy ', '').toUpperCase();
        await msg.reply(`✅ Order placed for ${product}! We'll DM you payment details.`);
    } else if (text === '!help') {
        await msg.reply('Available commands:\n!deals — Today\'s deals\n!order <id> — Check order status\n!contact — Talk to human');
    }
});

client.initialize();
```

### WhatsApp Business API — Official Flow

```bash
# Step 1: Set up webhook endpoint
# Meta sends message notifications to your webhook
POST /webhook/whatsapp
{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [
          { "from": "628123456789", "text": { "body": "I want to order" } }
        ]
      }
    }]
  }]
}

# Step 2: Reply with template message or free-form
curl -X POST "https://graph.facebook.com/v18.0/$PHONE_NUMBER_ID/messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "628123456789",
    "type": "template",
    "template": {
      "name": "order_confirmation",
      "language": { "code": "id" }
    }
  }'
```

### Money-Making Workflows

1. **Order Confirmation + Upsell Bot** — Auto-send order confirmations, then upsell related products
2. **Lead Qualification** — Multi-step broadcast: "Interest?" -> "Budget?" -> "Schedule call?" -> CRM
3. **Broadcast Marketing** — Segment users, send personalized promotions (24h window; use templates for proactive)
4. **Customer Support Tier-1** — Handle returns, shipping status, FAQ; save 40-60% on support costs
5. **Course/Content Delivery** — Auto-deliver paid course modules via WhatsApp drip sequence
6. **Appointment Booking** — Calendar integration, auto-confirmation, reminders, rescheduling

### Limitations

| Constraint | Detail |
|---|---|
| 24-hour customer service window | Free-form replies only within 24h of user message |
| Proactive messages require templates | Pre-approved templates needed for outbound |
| Rate limits | 250-1M messages/day depending on tier |
| Phone number verification | Business must verify with Meta |
| BSP fees | Twilio, MessageBird, WATI charge ~$0.005-$0.05/msg |

---

## Cross-Platform Bot Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Message Queue (Redis/RabbitMQ)            │
└─────────────────────────────────────────────────────────────┘
         │               │                │
┌────────▼─────┐ ┌──────▼──────┐ ┌──────▼──────────┐
│  Telegram     │ │  Twitter/X  │ │  WhatsApp        │
│  Bot Worker   │ │  Bot Worker │ │  Bot Worker      │
└───────────────┘ └─────────────┘ └──────────────────┘
         │               │                │
┌────────▼──────────────▼────────────────▼──────────────────┐
│                    Shared Services                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ Content  │ │  CRM /   │ │  Payment │ │  Analytics  │  │
│  │ Queue    │ │  User DB │ │  Gateway │ │  Pipeline   │  │
│  └──────────┘ └──────────┘ └──────────┘ └─────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### Multi-Bot Content Pipeline (Build in Public)

```
Daily Content → Canonical JSON Store → Per-Platform Formatters
                                       ├── Telegram: Markdown + buttons
                                       ├── Twitter: 280-char threads
                                       └── WhatsApp: Rich media + CTAs
                                       → Simultaneous or staggered delivery
```

```python
# Canonical content item
content = {
    "title": "Deal of the Day",
    "body": "50% off on premium automation tools",
    "link": "https://lynk.id/affiliate/deal123",
    "media_url": "https://img.example.com/deal.jpg",
    "cta": "Buy Now",
    "scheduled_at": "2026-07-17T08:00:00Z",
    "platforms": ["telegram", "twitter", "whatsapp"]
}

# For each active platform, format and dispatch
for platform in active_platforms:
    formatter = formatters[platform]  # per-platform renderer
    message = formatter.format(content)
    dispatcher = dispatchers[platform]  # API client
    dispatcher.send(message)
    track_delivery(platform, message.id)
```

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll build one bot manually per platform" | Same message queuing, scheduling, DB logic; write once, dispatch to all three |
| "WhatsApp business API is too complex" | `whatsapp-web.js` gets you running in 30 min; upgrade to official API when revenue justifies it |
| "Bot engagement is low compared to manual" | A bot engages 24/7 while you sleep; consistent presence beats sporadic manual effort |
| "I don't want to spam my users" | Permission-based opt-in + value-first content = welcome broadcasts, not spam |
| "Platforms will ban me" | Follow platform rate limits, use official APIs, respect user opt-out; legitimate bots stay active for years |
| "I need a developer" | Each bot uses < 100 lines of Python/JS; the cross-platform shared layer is < 200 lines |

---

## First Action in 60 Minutes

1. **Pick one platform** — Start with Telegram (lowest barrier, no approval needed)
2. **Create a bot** — `/newbot` via @BotFather, copy token
3. **Deploy the start/subscribe skeleton** — Polling mode, 20 lines of Python
4. **Add one money workflow** — `/affiliate` command that returns a link
5. **Test** — Run locally, send messages, confirm responses
6. **Schedule** — Add a cron job (`*/30 * * * *`) to broadcast queued content
7. **Monetize** — Create a paid channel ($5-$20/mo) with exclusive content
8. **Day 2** — Add Twitter bot with same content queue
9. **Week 2** — Add WhatsApp bot for broadcast marketing
10. **Month 1** — Cross-pollinate: same content, 3 platforms, $500-$2,000 MRR

---

## Verification

- [ ] Each bot connects to its respective API and authenticates
- [ ] Webhook responses return correct status codes (200/202)
- [ ] Scheduled messages deliver at the correct time
- [ ] Rate limits are respected (no 429 responses in production)
- [ ] Affiliate/paid links resolve correctly
- [ ] User opt-out is instant and respected
- [ ] Error handler logs failures and retries transient errors
- [ ] Cross-platform content pipeline formats correctly for each platform
- [ ] Handoff-to-human works for all three platforms
- [ ] Analytics track message delivery and engagement


## When to Use
Use this skill when working with bots.


## Workflow
See the parent skill for authoritative workflow documentation.
