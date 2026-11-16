---
name: bot-from-scratch
description: "Use when building a chat-platform bot (Discord/Telegram/Slack/Twitter-style) from first principles — the event loop, command routing, and platform API integration, not an LLM agent framework. Triggers on: 'build a discord bot from scratch', 'implement a telegram bot event loop', 'webhook vs polling for a bot', 'command router for a chat bot', 'rate limiting a platform API bot'. Covers polling vs webhook architecture, command parsing/routing, and state management."
origin: yana-ai — synthesized from public chat-platform bot API documentation patterns (Discord/Telegram Bot API design) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /bot-from-scratch

## When to Use

- Building a chat-platform bot's core message loop (Discord, Telegram, Slack, Twitter/X, IRC) from the platform's raw API, without a heavy bot framework.
- Deciding between polling and webhook architecture for receiving platform events.
- Implementing command parsing/routing and per-user/per-channel state for a bot.

## Do NOT use for

- Building an LLM-powered conversational agent's reasoning/tool-use loop — that's a different problem (prompting, tool orchestration, memory); see `agency-agents`, `voice-agents`, `hermes-conversation-loop`, or `openclaw-persona-forge` for AI-agent-specific patterns. This skill is about the *platform integration* layer a bot (AI-powered or not) sits behind.
- Web scraping or browser automation bots — see `browser-use`/`stealth-browser-automation` for that different category of "bot."
- General webhook infrastructure unrelated to chat platforms — see `api-gateway-engineer`/relevant backend skills for that.

---

## Architecture Decision: Polling vs Webhook

```
Simple deployment, no public HTTPS endpoint available, low message volume?
  → Polling (Step 1) — bot repeatedly asks the platform "any new events?"

Production deployment with a reachable HTTPS endpoint, want lower latency
and lower request volume?
  → Webhook (Step 2) — platform pushes events to your endpoint as they happen
```

Most platform bot APIs (Telegram, Discord's gateway, Slack) support both; polling is simpler to get running locally, webhooks are what real deployments typically use.

## Step 1: Polling Architecture

```
loop:
  events = GET platform_api/get_updates?offset=last_seen_id
  for event in events:
    handle(event)
    last_seen_id = event.id + 1
  sleep(poll_interval)   # or use long-polling if the platform supports it
```

**Long-polling** (the request itself blocks server-side for up to N seconds waiting for a new event, rather than returning immediately with an empty list) is far more efficient than short-polling with a fixed sleep — it gets near-webhook latency without needing a public endpoint. Telegram's `getUpdates` supports this via a `timeout` parameter; check whether your target platform does before defaulting to fixed-interval short polling.

**Idempotency via offset/cursor**: always track the last-processed event ID and request only events after it (`offset=last_seen_id`) — without this, a restart re-delivers already-handled events, causing duplicate responses/actions.

## Step 2: Webhook Architecture

The platform makes an HTTP POST to your public endpoint whenever an event occurs. Requirements this introduces that polling doesn't have:

- **A public HTTPS endpoint** — most platforms (Telegram, Slack, Discord interactions API) require TLS; a self-signed cert usually isn't accepted, use a real cert (Let's Encrypt) or a platform-provided tunnel for local dev (ngrok-style).
- **Verify the request is genuinely from the platform** — most platforms sign webhook payloads (a header like `X-Signature` computed as an HMAC of the body using a secret only you and the platform know); verify this signature before processing, or anyone who discovers your endpoint URL can inject fake events. See `stripe-webhook-security` for the general pattern if unfamiliar with webhook signature verification.
- **Respond fast, process async**: platforms expect a quick 200 OK (often within a few seconds) to consider the webhook delivered; if handling an event involves slow work (calling an LLM, hitting a slow API), acknowledge the webhook immediately and do the actual work in a background task/queue — a slow handler that blocks the HTTP response risks the platform treating the delivery as failed and retrying, causing duplicate processing.

## Step 3: Command Parsing & Routing

Most chat bots follow a command-router pattern regardless of platform:

```
parse: "!ban @user 3d spamming" → command="ban", args=["@user", "3d", "spamming"]
route: lookup "ban" in a command table → call ban_handler(event, args)
```

```python
COMMANDS = {
    "ban": handle_ban,
    "help": handle_help,
}

def route(event):
    if not event.text.startswith(PREFIX):
        return
    command, *args = event.text[len(PREFIX):].split()
    handler = COMMANDS.get(command.lower())
    if handler:
        handler(event, args)
    else:
        reply(event, f"Unknown command: {command}")
```

For platforms with native slash-command support (Discord interactions, Slack slash commands), the platform does the parsing and delivers structured `(command, args)` directly — prefer that over text parsing when available, since it also gets you free autocomplete/validation in the client UI.

## Step 4: State Management

Bots are usually stateless per-message but need memory across messages (conversation context, per-user settings, rate-limit counters, active game/session state). Keep state keyed by the smallest scope that's actually correct for the feature — per-user, per-channel, or per-guild/workspace are different scopes with different lifetimes, and conflating them is a common bug (e.g. a "current game" keyed globally instead of per-channel breaks the moment two channels play simultaneously).

For anything beyond a single-process toy bot, back state with persistent storage (Redis for ephemeral/fast-expiring state like rate limits, a real database for anything that must survive a restart) rather than in-memory dicts — an in-memory-only bot loses all state on every deploy/crash.

## Step 5: Rate Limiting Against the Platform API

Every chat platform enforces its own rate limits (Discord: per-route limits with `X-RateLimit-*` response headers; Telegram: ~30 messages/second global, 1/second per chat). Two directions to handle:

- **Respect the platform's limit**: read rate-limit headers when provided and back off accordingly (a `429` response usually includes a `Retry-After`); a bot that ignores this gets temporarily or permanently blocked by the platform.
- **Rate-limit your own users**: independent of the platform's limits, apply your own per-user cooldowns on expensive commands (anything that calls an LLM, hits a paid API, or does heavy compute) to prevent one user from exhausting your own resources or the platform quota for everyone.

## What NOT to Do

- Don't skip webhook signature verification — an unverified webhook endpoint accepts forged events from anyone who finds the URL, not just the real platform.
- Don't do slow work synchronously inside a webhook handler — see Step 2; this causes duplicate-delivery retries and, at scale, platform-side timeout penalties.
- Don't key shared state at the wrong scope (global instead of per-channel/per-user) — see Step 4; this is the most common multi-instance-of-the-same-feature bug.
- Don't ignore platform rate-limit response headers — a bot that gets rate-limited and keeps retrying at the same pace makes the backoff worse, not better; honor `Retry-After` explicitly.
