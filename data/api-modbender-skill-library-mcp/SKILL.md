---
name: API (Stripe, OpenAI, Notion & 100+ more)
slug: api
version: 1.3.4
homepage: https://clawic.com/skills/api
description: REST API reference for 147 services. Authentication patterns, endpoints, rate limits, and common gotchas.
changelog: Documentation-only skill with API reference files.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---

# API

REST API reference documentation. 147 services with authentication, endpoints, and gotchas.

## Setup

On first use, read `setup.md` for usage guidelines.

## When to Use

User asks about integrating a third-party API. This skill provides:
- Authentication documentation
- Endpoint reference with curl examples
- Rate limits and pagination patterns
- Common mistakes to avoid

## Architecture

```
apis/                    # API reference files by category
  ├── ai-ml.md           # OpenAI, Anthropic, Cohere, etc.
  ├── payments.md        # Stripe, PayPal, Square, etc.
  ├── communication.md   # Twilio, SendGrid, Slack, etc.
  └── ...

~/api/                   # User preferences (optional)
  └── preferences.md     # Preferred language for examples
```

## Quick Reference

| File | Purpose |
|------|---------|
| `setup.md` | Usage guidelines |
| `credentials.md` | Multi-account credential naming (`{SERVICE}_{ACCOUNT}_{TYPE}`) |
| `auth.md` | Authentication patterns |
| `pagination.md` | Pagination patterns |
| `resilience.md` | Error handling patterns |
| `webhooks.md` | Webhook patterns |

## API Categories

| Category | File | Services |
|----------|------|----------|
| AI/ML | `apis/ai-ml.md` | anthropic, openai, cohere, groq, mistral, perplexity, huggingface, replicate, stability, elevenlabs, deepgram, assemblyai, together, anyscale |
| Payments | `apis/payments.md` | stripe, paypal, square, plaid, chargebee, paddle, lemonsqueezy, recurly, wise, coinbase, binance, alpaca, polygon |
| Communication | `apis/communication.md` | twilio, sendgrid, mailgun, postmark, resend, mailchimp, slack, discord, telegram, zoom |
| Realtime | `apis/realtime.md` | sendbird, stream-chat, pusher, ably, onesignal, courier, knock, novu |
| CRM | `apis/crm.md` | salesforce, hubspot, pipedrive, attio, close, apollo, outreach, gong |
| Marketing | `apis/marketing.md` | drift, crisp, front, customer-io, braze, iterable, klaviyo |
| Developer | `apis/developer.md` | github, gitlab, bitbucket, vercel, netlify, railway, render, fly, digitalocean, heroku, cloudflare, circleci, pagerduty, launchdarkly, split, statsig |
| Database | `apis/database.md` | supabase, firebase, planetscale, neon, upstash, mongodb, fauna, xata, convex, appwrite |
| Auth | `apis/auth-providers.md` | clerk, auth0, workos, stytch |
| Media | `apis/media.md` | cloudinary, mux, bunny, imgix, uploadthing, uploadcare, transloadit, vimeo, youtube, spotify, unsplash, pexels, giphy, tenor |
| Social | `apis/social.md` | twitter, linkedin, instagram, tiktok, pinterest, reddit, twitch |
| Productivity | `apis/productivity.md` | notion, airtable, google-sheets, google-drive, google-calendar, dropbox, linear, jira, asana, trello, monday, clickup, figma, calendly, cal, loom, typeform |
| Business | `apis/business.md` | shopify, docusign, hellosign, bitly, dub |
| Geo | `apis/geo.md` | openweather, mapbox, google-maps |
| Support | `apis/support.md` | intercom, zendesk, freshdesk, helpscout |
| Analytics | `apis/analytics.md` | mixpanel, amplitude, posthog, segment, sentry, datadog, algolia |

## How to Navigate API Files

Each category file contains multiple APIs. Use the index at the top of each file:

1. **Read the index first** — Each file starts with an index table showing API names and line numbers
2. **Jump to specific API** — Use the line number to read only that section (50-100 lines each)
3. **Example:**
   ```bash
   # Read index
   head -20 apis/ai-ml.md
   # Read specific API section
   sed -n '119,230p' apis/ai-ml.md
   ```

## Core Rules

1. **Find the right file first** — Use the API Categories table to locate the service.

2. **Read the index, then jump** — Each file has an index. Read only the section you need.

3. **Include Content-Type** — POST/PUT/PATCH requests need `Content-Type: application/json`.

4. **Handle rate limits** — Check `X-RateLimit-Remaining` header. Implement backoff on 429.

5. **Validate responses** — Some APIs return 200 with error in body. Check response structure.

6. **Use idempotency keys** — For payments and critical operations.

## Common Mistakes

- Missing `Content-Type: application/json` on POST requests
- API keys in URL query params (use headers instead)
- Ignoring pagination (most APIs default to 10-25 items)
- No retry logic for 429/5xx errors
- Assuming HTTP 200 means success

## Scope

This skill is **documentation only**. It provides:
- API endpoint reference
- Authentication patterns
- Code examples for reference

The user manages their own API keys and runs commands themselves.

## External Endpoints

This skill documents external APIs. Example endpoints shown are for the respective service providers (Stripe, OpenAI, etc.).

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `http` — HTTP request patterns
- `webhook` — Webhook handling
- `json` — JSON processing

## Feedback

- If useful: `clawhub star api`
- Stay updated: `clawhub sync`
