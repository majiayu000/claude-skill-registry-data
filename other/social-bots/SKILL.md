---
name: social-bots
description: "Reference for the studio/bot-bridge and studio/comment-bot services — Chatwoot webhook bridge for Telegram/Facebook/Instagram DMs, the AI auto-reply webhook loop, and the separate FB/IG public comment handler. Use this for any task involving Chatwoot, bot webhooks, Meta Graph API, or message/comment automation."
---

# Social Bots — Reference

The bot system is split into two completely separate services. Do not conflate them — they use different Meta webhook subscriptions, different deployment environments, and different system prompts.

## Lane A — Direct Messages (Telegram + Facebook + Instagram)

Chatwoot (official Docker image) is the unified inbox. It connects to Telegram, Facebook, and Instagram natively. The `studio/bot-bridge` service only handles the AI-reply loop on top of Chatwoot's outgoing webhook.

**The loop:**

1. Customer sends a message on any connected channel → arrives in Chatwoot as a new conversation/message
2. Chatwoot fires a webhook (`message_created` event) → `POST http://bot-bridge.railway.internal:4001/chatwoot-webhook`
3. **Critical loop-prevention check:** only proceed if `message_type === "incoming"`. If it's `"outgoing"` (i.e., the bot's own previous reply), return immediately — otherwise the bot replies to itself forever. Also ensure `sender.type === "contact"` to prevent replying when a human agent is active.
4. Fetch conversation history: `GET /api/v1/accounts/{account_id}/conversations/{id}/messages` from Chatwoot API — gives the AI Gateway context/memory.
5. `POST AI_GATEWAY_URL/ai/chat` with `{ context: "telegram-fb-ig-dm", platform: payload.inbox.channel_type, message, history }`.
6. Post the reply back: `POST /api/v1/accounts/{account_id}/conversations/{id}/messages` (Chatwoot then delivers it to whichever channel the customer used — you don't need channel-specific code for this part).

## Lane B — Public Post Comments (Facebook + Instagram only — NOT Telegram)

This is a separate service: `studio/comment-bot`. No platform (Chatwoot included) handles DMs and public comments in one place — comments use a different Meta webhook subscription (`feed`, not `messages`).

**The loop:**

1. Customer comments on a FB page post or IG post
2. Meta sends a webhook to `studio.mysite.com/webhooks/comments` (subscribed to the `feed` field — set this up separately in Meta Developer console from the messaging webhook)
3. Webhook verification: Verify the signature of Meta via `X-Hub-Signature-256` HMAC-SHA256 check.
4. Handler extracts comment text, comment ID, post ID.
5. `POST AI_GATEWAY_URL/ai/chat` with `{ context: "fb-ig-comment", platform: "facebook"|"instagram", message: commentText }` — this context uses a SHORTER, public brand-voice system prompt.
6. Reply via Graph API: `POST /{comment-id}/comments` with the AI's reply text.
7. Log the action to the `comment_log` table (Supabase) for audit.

## Webhook Verification (mandatory, see also `security-engineering` Section 3.6)

- **Meta (FB/IG, public comment-webhook):**
  - Initial setup: respond to the `hub.verify_token` challenge from Meta to prove ownership.
  - Every message: verify `X-Hub-Signature-256` header (HMAC-SHA256 of the request body using your app secret) before trusting the payload. Use constant-time comparison to prevent timing attacks.

## Shared AI Gateway & Security

- Both lanes call `AI_GATEWAY_URL/ai/chat` — never call Claude directly.
- The call must include the `x-internal-key` header matching the `INTERNAL_API_KEY` to authenticate internal service requests.
- The context values (`telegram-fb-ig-dm` and `fb-ig-comment`) map to different system prompts in the gateway.

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express (for webhook routing)
- Chatwoot connection details (account ID, API access token) in `.env`

