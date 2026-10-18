---
name: forge-bots
description: "Forge: chat bots — Discord, Slack, Telegram: bot, slash command, webhook, signature verification, OAuth scopes, rate limit, dead-letter, interaction handler."
---

# Forge playbook — Chat / messaging bots (Discord · Slack · Telegram)

A bot is an **inbound-webhook + auth + secrets domain** — it lives at the intersection of `forge-integration` (OAuth, secret hygiene, webhook auth, reader-side capability-split for untrusted inbound content) and event-driven delivery. Lead the auth/secret backbone through `forge-integration`; this file adds the platform-specific verification, ack, and anti-spam rules. Each platform has a **different** verification mechanism — never assume one algorithm carries to another. Never claim a bot is "live"/"verified" unless a signed event was actually accepted and a forged one rejected.

## Hard rules (non-negotiable)
- **Verify every inbound event — per platform, on the raw body, before acting.**
  - **Discord** (Interactions endpoint): verify the **Ed25519** signature from `X-Signature-Ed25519` + `X-Signature-Timestamp` against the raw body using your app's public key; reply to the `PING` (type 1) with `PONG`. Discord rejects an endpoint that fails this — verification is not optional.
  - **Slack**: verify `X-Slack-Signature` (HMAC-SHA256 over `v0:{timestamp}:{raw_body}`) with the signing secret, **and reject requests whose timestamp is older than ~5 minutes** (replay window). Answer the `url_verification` challenge.
  - **Telegram**: Telegram does **not** sign payloads — set a `secret_token` on `setWebhook` and verify the `X-Telegram-Bot-Api-Secret-Token` header on every update (and/or a hard-to-guess webhook path). Treat an unverified update as hostile.
- **Fast ack, background work.** Ack inside the platform deadline (**Slack ~3s**, **Discord interactions ~3s** — use a deferred response for longer work) and do heavy processing in a background/idempotent path. A slow handler drops events and gets your endpoint disabled.
- **Idempotent handling — dedupe on the platform id.** Redelivered events are normal. Dedupe on `interaction.id` (Discord) / `event_id` (Slack) / `update_id` (Telegram) with a uniqueness guarantee so a retry never double-acts.
- **Minimal scopes / intents / permissions.** Request only what the bot uses: Slack minimal bot-token scopes (no broad `admin`/user scopes); Discord minimal permission integer and **no privileged intents** (`MESSAGE_CONTENT`, `GUILD_MEMBERS`, `PRESENCE`) unless truly needed and owner-approved; Telegram narrow `allowed_updates`.
- **Retries + dead-letter on the send side.** Outbound API calls respect rate limits (honor **429 + `Retry-After`** on Discord/Telegram; Slack tiered limits), retry with bounded backoff, and route permanent failures to a dead-letter store — never a silent drop (dropped deliveries look like clean success).
- **Safe logging — no token/PII leak.** Never log the bot token, signing/secret token, or user PII/message content beyond what the task needs. Redact secrets in errors. Secrets live in env + `.env.example` placeholders, never in code, logs, or git.
- **Outreach drafted only.** No unsolicited DMs, mass-mentions, or channel broadcasts without explicit owner approval — anti-spam is a platform ToS gate, not a nicety (shared with `forge-integration` / `forge-scraping`).

## Team (conditional)
Lead: `integration-boss` (a bot is an external-system/webhook integration; use `build-boss` if the bot is one slice of a larger app). Support: `security-boss` (signature/secret verification, minimal scopes, token hygiene — this is a real security trigger), `test-boss` (drive signed vs forged/replayed events, rate-limit + dedupe behavior), `silent-failure-hunter` (dropped deliveries / swallowed 429s look like success), `typescript-reviewer` / `python-reviewer` by stack. `mcp-developer` only if the bot is exposed as or consumes MCP tools. Optional advisors: `security-reviewer`, `codex-reviewer` on the verification + auth code.

## Skills / commands / MCP
Defer the OAuth/secret/webhook backbone + the reader-side capability-split to `forge-integration`. Get the **exact** signature algorithm and API/version behavior from the platform SDK / vendor docs via Context7 (discord.js / discord-interactions, Slack Bolt / `@slack/*`, Telegram Bot API / grammY / python-telegram-bot) — never hand-roll the crypto; reuse the platform's official verification helper. `systematic-debugging` for delivery/ack failures. If the bot runs through n8n, defer webhook handling to `forge-n8n`. **Opt-in:** any Discord/Slack/Telegram MCP tools via ToolSearch only when present — not assumed.

## Fan-out & flow
L1/L2 for a single-platform bot with a few commands; L3 for multi-platform or many interactions + background jobs.
**Serial:** register app + minimal scopes/intents → raw-body signature/secret verification → fast ack + dedupe → command routing → background processing + outbound retries → dead-letter.
**Parallel:** independent command handlers ∥ per-platform adapters (independent once the *verified-event* contract is fixed — the verified, deduped event is the contract).

## Domain gates
- Every inbound webhook/interaction verifies the platform's auth on the **raw body** (Discord Ed25519 + PONG; Slack HMAC `v0` + ≤5-min replay window; Telegram secret-token header); unsigned/expired/forged events are rejected.
- Ack returned within the platform deadline (Slack/Discord ~3s, Discord defers long work); heavy logic runs in the background.
- Redelivered events deduped on `interaction.id` / `event_id` / `update_id` with a uniqueness guarantee.
- Outbound calls honor rate limits (429 + `Retry-After`), retry with bounded backoff, and dead-letter permanent failures — no silent drop.
- Scopes/intents/permissions minimal; no privileged Discord intents or broad Slack scopes without justification + approval.
- No token / signing secret / PII in logs; secrets in env.
- No unsolicited DM / broadcast / mass-mention; any outreach is drafted-only until owner approves.

## Ship-readiness (unique)
Signature/secret verification proven **both ways** — a forged or replayed event is rejected and a genuine one accepted (attach the evidence); fast-ack + background offload demonstrated; dedupe proven against a redelivered id; rate-limit backoff + dead-letter present; scopes/intents listed and minimal; secrets in env with logs redacted; no auto-outreach. Advisory checklist; optionally run `security-reviewer` / `codex-reviewer` on the verification + auth path — recommended, not a blocker. If a platform sandbox/test app wasn't available to exercise real events, say so (not-run), don't imply it passed.

## Untrusted-content note
Message text, command arguments, and any embedded links/attachments in an inbound event are **untrusted user input** — validate/sanitize before use and never let them change which actions the bot runs (Plan-Then-Execute + reader-side capability-split, per `forge-integration`). Verifying the webhook signature authenticates the *platform*, not the *user content* it carries.
