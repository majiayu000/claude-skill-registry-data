---
name: discord-dm-digest
description: Sets up a Discord bot that sends each member their own daily.dev digest by DM, from their For You feed, the popular feed or one of their custom feeds, at the time and days they choose.
---

# daily.dev Digest by DM (Discord)

Most people mean to open daily.dev every morning and don't. This bot brings the feed to them: each member links their own daily.dev account, picks a time, days and a feed, and gets a short digest of new posts in a Discord DM. Nothing is posted in channels, and nobody sees anyone else's feed.

Every request runs as the member who set up the digest, with their own daily.dev OAuth token. There is no shared token.

You (the agent) help the bot owner deploy it from the source code and verify it works. You never post to Discord on anyone's behalf, and you only handle secrets by writing them into a local `.env` the owner asked you to create.

## Requirements

- Node.js 18.17+ and the bot source: `git clone https://github.com/pedropietro/daily-dev-discord-digest` (the code lives in `bot/`).
- A **daily.dev OAuth app**: daily.dev → Settings → API → OAuth apps → Create app. Redirect URI: `<PUBLIC_BASE_URL>/oauth/callback`. Note the client ID and the client secret (shown once).
- A public **HTTPS** URL that reaches the bot's HTTP port.
- A Discord application with a bot user: bot token and application (client) ID.
- An always-on host: the scheduler runs inside the bot process.

The bot does **not** need a personal daily.dev access token. Do not put one in the configuration.

## How the bot uses daily.dev

| Step | Call | Token |
|---|---|---|
| `/dailydev connect` | OAuth authorization code + PKCE (S256), scopes `openid profile offline_access read`, `resource=https://api.daily.dev/public/v1` | none yet |
| First `/dailydev digest on` without a `timezone` | `GET /profile/` (reads `timezone`), once | the member's own |
| Choosing a custom feed | `GET /feeds/custom/` (cached 10 min per member) | the member's own |
| Each digest | **one** of `GET /feeds/foryou`, `GET /feeds/popular`, `GET /feeds/custom/{feedId}` with `limit` = 2× posts (10–30), then posts already sent are dropped | the member's own |
| `/dailydev disconnect` | delete tokens and settings, `POST https://api.daily.dev/auth/oauth2/revoke` | client secret |

Read-only on daily.dev. Tokens and settings are encrypted at rest (AES-256-GCM); refresh tokens are rotated so digests keep arriving while members are away.

Commands and messages are in English, with Brazilian Portuguese command names and messages for members whose Discord client is set to `pt-BR` (for example `/dailydev digest ativar`).

## Steps

1. **Get the code and check the environment.** Clone the repository, `node -v` ≥ 18.17. In `bot/`: `npm install`, then `npm test`.
2. **Create the `.env`.** Copy `bot/.env.example` to `bot/.env`, ask the owner for each value, don't echo secrets back. `TOKEN_ENCRYPTION_KEY`: `openssl rand -base64 32`.
3. **Expose the callback.** `<PUBLIC_BASE_URL>/healthz` must return `ok` from the internet, and `<PUBLIC_BASE_URL>/oauth/callback` must be registered exactly on the OAuth app.
4. **Invite the bot.** Discord developer portal → OAuth2 → URL Generator: scopes `bot` and `applications.commands`. No privileged intents. Members must share a server with the bot and allow DMs from it.
5. **Register the command.** `npm run deploy-commands`.
6. **Run it.** `npm start`, or the included `Dockerfile` with a volume on `/app/data`, on a host that stays up.
7. **Test with the owner.** `/dailydev connect` → approve → "daily.dev connected". `/dailydev digest preview` → a digest DM arrives. `/dailydev digest on time:<two minutes from now>` → the scheduled DM arrives at that minute. `/dailydev status`, `/dailydev digest off`, `/dailydev disconnect`.

## Output

Report: Node version, `npm test` result, public callback URL, registration mode, and whether connect, preview, a scheduled digest, off and disconnect worked. If a step fails, show the exact error and the fix.

## Guardrails

- Never configure a shared or personal daily.dev token; digests are built only with the recipient's own token and sent only to them.
- Never post digests in channels.
- Quota: each member has their own allowance (free tier: 60 requests/minute, 200/month). A digest costs 1 request: daily ≈ 30/month, weekdays ≈ 22/month. Setup costs 1–2 more, once.
- Empty digests are not sent. After 3 failed DMs in a row the digest pauses itself.
- Don't commit `.env` or `data/`.
