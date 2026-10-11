---
name: setup
description: This skill should be used when the user asks to "install grammY", "create a Telegram bot", "set up my first bot", "verify grammY installation", "get a bot token", "BotFather", or needs to bootstrap a brand-new grammY project from zero to a running echo bot.
---

# grammY — Setup

Bootstrap a grammY Telegram bot from zero. Five steps: install runtime, get a bot token from BotFather, install the package, write a minimal bot, run it and verify in Telegram.

## 1. Pick a runtime

grammY runs on **Node.js**, **Deno** and **Bun**. For new projects use a supported release: **Node.js 22 LTS or 24 LTS** (Node 18 and 20 are end-of-life), **Deno 2.x**, or a current **Bun 1.x**. Pick one:

- **Node.js + TypeScript** — most common, biggest ecosystem.
- **Deno** — `npm:` imports, no `node_modules`, native TypeScript.
- **Bun** — Node-compatible, faster cold start.

## 2. Get a bot token

Open [@BotFather](https://t.me/BotFather) in Telegram and send `/newbot`. Pick a display name and a username ending in `bot` (e.g. `my_awesome_bot`). BotFather replies with an API token in the form `123456:ABC-DEF...`. **Treat this as a secret** — put it in `.env`, never commit it.

## 3. Install grammY

```bash
# Node.js / Bun
npm install grammy

# Deno — import via the npm: specifier, no install step
# import { Bot } from "npm:grammy";
```

## 4. Write a minimal bot

### TypeScript (Node.js)

```typescript
// src/bot.ts
import { Bot } from "grammy";

const bot = new Bot(process.env.BOT_TOKEN!);

bot.command("start", (ctx) => ctx.reply("Hi! I'm alive."));
bot.on("message", (ctx) => ctx.reply(`You said: ${ctx.message.text ?? "(non-text)"}`));

bot.start();
```

### JavaScript (Node.js)

```javascript
// src/bot.js
const { Bot } = require("grammy");

const bot = new Bot(process.env.BOT_TOKEN);

bot.command("start", (ctx) => ctx.reply("Hi! I'm alive."));
bot.on("message", (ctx) => ctx.reply(`You said: ${ctx.message.text ?? "(non-text)"}`));

bot.start();
```

### Deno

```typescript
// bot.ts
import { Bot } from "npm:grammy";

const bot = new Bot(Deno.env.get("BOT_TOKEN")!);

bot.command("start", (ctx) => ctx.reply("Hi! I'm alive."));
bot.on("message", (ctx) => ctx.reply(`You said: ${ctx.message.text ?? "(non-text)"}`));

bot.start();
```

## 5. Run and verify

```bash
# Node.js 22+
BOT_TOKEN=<BOT_TOKEN> npx tsx src/bot.ts

# Bun
BOT_TOKEN=<BOT_TOKEN> bun run src/bot.ts

# Deno 2.x (-I = imports, -E = env vars, -N = network)
BOT_TOKEN=<BOT_TOKEN> deno -IEN bot.ts
```

Open Telegram, find your bot by its `@username`, send `/start`. You should see "Hi! I'm alive." Send any other message — the bot echoes it back.

**Verification checklist:**
- Process logs `[grammY] You can stop me by pressing Ctrl+C` (or similar) on startup.
- `/start` returns the welcome string within 1–2 seconds.
- Sending an arbitrary text message produces an echo.

If any of these fail, open the `troubleshoot` skill.

## Quick scaffold (bundled script)

This plugin ships a helper that does steps 3–4 for you:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/init-bot.sh /path/to/my-bot
cd /path/to/my-bot
cp .env.example .env  # then paste your BOT_TOKEN
npm install
npm run dev
```

The script creates `package.json` (grammY `^1.46.0`, Node 22+), `tsconfig.json`, `src/bot.ts`, `.env.example`, and `.gitignore`. The scaffold reads `.env` through Node's `--env-file` flag, so it needs no `dotenv` dependency.

## What this skill does NOT cover

- Webhook deployment (use `deployment-hosting`).
- Sessions, conversations, or any plugin (use `plugins-catalog`, `sessions`, `conversations`).
- Telegram account automation (different concept — see the `tg-client` plugin).