---
name: telegram-integration
description: Use when user explicitly requests Telegram bot development, Mini App integration, webhook/polling setup, or debugging Telegram-specific issues. Handles Telegraf-based bots, AI chatbot integration via Telegram, and deployment to Railway/Vercel. DO NOT use unless user mentions Telegram work.
---

# Telegram Bot & Mini App Integration

## ⚠️ VERIFICATION REQUIRED

**BEFORE using this skill, verify user needs Telegram integration:**

1. **User explicitly mentions "Telegram"** in their request, OR
2. **User mentions Telegram-specific terms:**
   - "Telegram bot", "Telegram Mini App", "Telegram webhook"
   - "@BotFather", "Telegraf", "telegram-polling"
   - Debugging existing Telegram features
3. **When in doubt, ASK:** "Are you working on Telegram integration?"

**DO NOT use this skill for:**
- General chatbot or messaging work (Discord, Slack, WhatsApp)
- Generic deployment questions
- API or webhook issues unrelated to Telegram
- Just because Telegram code exists in the project

## Overview

Comprehensive skill for building Telegram bots and Mini Apps using Telegraf. Covers setup, development, debugging, and deployment with conditional workflows for local vs production environments.

**Core principle:** Use polling for local development, webhooks for production. Validate Mini App data server-side. Never mix polling and webhooks simultaneously.

## When to Use

**ONLY after verifying Telegram work**, use this skill when you see:
- "Build a Telegram bot"
- "Telegram webhook not working"
- "Add Telegram Mini App"
- "Deploy Telegram bot to Railway/Vercel"
- "Telegram bot works locally but not in production"
- "Integrate AI with Telegram"

## When NOT to Use

**NEVER use this skill for:**
- Other messaging platforms (Discord, Slack, WhatsApp, SMS)
- General webhook/API issues unrelated to Telegram
- Non-Telegram chatbot work
- Just because you see `telegram` in file names

**If uncertain about Telegram involvement, verify first.**

## Quick Start: Diagnostic Router

Start every Telegram task by routing to the correct workflow:

| What are you doing? | Workflow |
|---------------------|----------|
| Starting new Telegram integration | → [NEW_PROJECT](#new-project-workflow) |
| Webhook/polling not working | → [DEBUGGING](#debugging-workflow) |
| Adding commands/AI/Mini App | → [FEATURE_ADDITION](#feature-addition-workflow) |
| Deploying to production | → [DEPLOYMENT](#deployment-workflow) |

---

## NEW_PROJECT Workflow

**Use when:** User wants to create a new Telegram bot or Mini App.

### TodoWrite Checklist

Create these todos when starting new project:

```
- [ ] Determine project type (bot only, mini app only, or both)
- [ ] Create bot via @BotFather, save token to .env.local
- [ ] Install Telegraf: npm install telegraf
- [ ] Choose environment setup (local polling or production webhook)
- [ ] Implement bot service with singleton pattern
- [ ] Add basic command handlers (/start, /help)
- [ ] Test bot responds to commands
```

### Bot Creation (via @BotFather)

1. Open Telegram, search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to set name and username
4. Save the bot token: `TELEGRAM_BOT_TOKEN=<token>`
5. **Optional:** Configure bot settings (`/setdescription`, `/setabouttext`)

### Environment-Specific Setup

**Choose ONE based on environment:**

#### Local Development (Polling)

Use polling to avoid HTTPS requirements:

**Create `telegram-polling.js`:**
```javascript
const fetch = require('node-fetch');

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const WEBHOOK_SECRET = process.env.TELEGRAM_WEBHOOK_SECRET || 'dev-secret';
const LOCAL_WEBHOOK_URL = 'http://localhost:3000/api/webhooks/telegram';

let offset = 0;

async function pollUpdates() {
  try {
    const response = await fetch(
      `https://api.telegram.org/bot${BOT_TOKEN}/getUpdates`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ offset, timeout: 30 })
      }
    );

    const data = await response.json();

    if (data.ok && data.result.length > 0) {
      for (const update of data.result) {
        // Forward to local webhook
        await fetch(LOCAL_WEBHOOK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Telegram-Bot-Api-Secret-Token': WEBHOOK_SECRET
          },
          body: JSON.stringify(update)
        });

        offset = update.update_id + 1;
      }
    }
  } catch (error) {
    console.error('Polling error:', error);
  }

  setTimeout(pollUpdates, 1000);
}

console.log('Starting Telegram polling...');
pollUpdates();
```

**Start polling:** `node telegram-polling.js`

#### Production (Webhook)

Use webhooks for event-driven updates:

**Set webhook after deployment:**
```bash
curl -X POST https://api.telegram.org/bot${TOKEN}/setWebhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/api/webhooks/telegram",
    "secret_token": "YOUR_SECRET_TOKEN"
  }'
```

**Verify webhook:**
```bash
curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo
```

### Bot Service (Singleton Pattern)

**Create `src/services/telegram/bot-service.ts`:**

```typescript
import { Telegraf } from 'telegraf';

class TelegramBotService {
  private static instance: Telegraf | null = null;

  static getInstance(): Telegraf {
    if (!this.instance) {
      // Use dummy token for build, real token at runtime
      const token = process.env.TELEGRAM_BOT_TOKEN || 'DUMMY_BUILD_TOKEN';

      if (token === 'DUMMY_BUILD_TOKEN') {
        console.warn('Using dummy token for build phase');
      }

      this.instance = new Telegraf(token);
      this.registerCommands();
    }

    return this.instance;
  }

  private static registerCommands() {
    const bot = this.instance!;

    bot.command('start', (ctx) => {
      ctx.reply('Welcome! Use /help to see available commands.');
    });

    bot.command('help', (ctx) => {
      ctx.reply('Available commands:\n/start - Start bot\n/help - Show this message');
    });

    bot.on('text', async (ctx) => {
      // Handle text messages
      ctx.reply(`You said: ${ctx.message.text}`);
    });
  }

  static async processUpdate(update: any) {
    const bot = this.getInstance();
    await bot.handleUpdate(update);
  }
}

export default TelegramBotService;
```

### Webhook API Route

**Create `src/app/api/webhooks/telegram/route.ts`:**

```typescript
import { NextRequest } from 'next/server';
import TelegramBotService from '@/services/telegram/bot-service';

export async function POST(request: NextRequest) {
  // Verify secret token
  const secret = request.headers.get('x-telegram-bot-api-secret-token');

  if (secret !== process.env.TELEGRAM_WEBHOOK_SECRET) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const update = await request.json();
    await TelegramBotService.processUpdate(update);

    return Response.json({ ok: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return Response.json({ error: 'Internal error' }, { status: 500 });
  }
}

// Force dynamic rendering (prevents caching issues)
export const dynamic = 'force-dynamic';
```

---

## DEBUGGING Workflow

**Use when:** Telegram bot or webhook not working as expected.

### Debugging Decision Tree

```
Is webhook receiving updates?
├─ No → Check webhook configuration
│  ├─ Run: curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo
│  ├─ Check: url, pending_update_count, last_error_date, last_error_message
│  └─ See: [Webhook Troubleshooting](#webhook-troubleshooting)
├─ Yes, but errors → Check platform logs
│  ├─ Vercel: Check deployment logs and function errors
│  ├─ Railway: railway logs
│  └─ See: [Platform-Specific Issues](#platform-specific-issues)
└─ Updates received, bot not responding
   ├─ Check bot service initialization
   ├─ Verify command handlers registered
   └─ Check for errors in message processing
```

### Webhook Troubleshooting

**Common webhook issues and solutions:**

| Symptom | Cause | Solution |
|---------|-------|----------|
| 401/403 Unauthorized | Missing or wrong secret token | Verify `X-Telegram-Bot-Api-Secret-Token` header matches `setWebhook` |
| Webhook not receiving updates | Webhook not set or deleted | Run `setWebhook` with correct URL and secret |
| SSL certificate error | Non-HTTPS URL | Ensure webhook URL uses `https://` (except test environment) |
| Pending updates growing | Webhook timing out | Reduce processing time or use edge functions (Vercel) |
| Duplicate message processing | Timeout <10s, Telegram retries | Increase timeout limit or optimize response time |
| getUpdates conflict error | Polling + webhook both active | Delete webhook OR stop polling (never both) |

**Diagnostic Commands:**

```bash
# Check webhook status
curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo

# Delete webhook (switch to polling)
curl -X POST https://api.telegram.org/bot${TOKEN}/deleteWebhook

# Test bot token
curl https://api.telegram.org/bot${TOKEN}/getMe
```

### Platform-Specific Issues

#### Vercel Issues

**Issue:** Deployment Protection blocks webhooks
- **Solution:** Disable in Settings → Deployment Protection

**Issue:** 10-second timeout on Hobby plan
- **Solution:** Use edge functions or reduce processing time
- **Code:**
  ```typescript
  export const runtime = 'edge'; // Longer timeout
  ```

**Issue:** Bot not receiving updates after deploy
- **Solution:** Redeploy or set webhook again with new URL

#### Railway Issues

**Issue:** Bot works locally, fails on Railway
- **Solution:** Ensure bot initializes after build completes, use dummy token for build

**Issue:** Mini App buttons show old URL
- **Solution:** Force dynamic rendering, clear cache, check `TELEGRAM_MINI_APP_URL` env var
- **Code:**
  ```typescript
  export const dynamic = 'force-dynamic';
  ```

**Issue:** Environment variables not loaded
- **Solution:** Use `railway variables` to verify, redeploy after changes

#### Local Development Issues

**Issue:** Polling script not receiving updates
- **Solution:**
  - Verify bot token is correct
  - Delete webhook: `curl -X POST https://api.telegram.org/bot${TOKEN}/deleteWebhook`
  - Check polling script is running

**Issue:** Port conflicts
- **Solution:** Check port 3000 is free, or change `LOCAL_WEBHOOK_URL` in polling script

---

## FEATURE_ADDITION Workflow

**Use when:** Adding features to existing Telegram bot.

### Feature Type Router

**Choose feature type:**

| Feature | Guide |
|---------|-------|
| Commands (/start, /help, custom) | [Adding Commands](#adding-commands) |
| AI Integration (ChatGPT, Claude) | [AI Integration Pattern](#ai-integration-pattern) |
| Inline keyboards/buttons | [Interactive UI](#interactive-ui) |
| Mini App | [Mini App Integration](#mini-app-integration) |
| File handling (photos, voice, documents) | [File Handlers](#file-handlers) |

### Adding Commands

**Pattern:**
```typescript
// In bot-service.ts registerCommands()
bot.command('mycommand', async (ctx) => {
  // Command logic
  await ctx.reply('Response text');
});
```

**With parameters:**
```typescript
bot.command('search', async (ctx) => {
  const query = ctx.message.text.split(' ').slice(1).join(' ');

  if (!query) {
    return ctx.reply('Usage: /search <query>');
  }

  const results = await searchFunction(query);
  await ctx.reply(`Found: ${results}`);
});
```

### AI Integration Pattern

**Unified chat manager approach:**

```typescript
import { ChatManager } from '@/services/chat/chat-manager';

bot.on('text', async (ctx) => {
  try {
    // Get or create conversation for user
    const conversation = await getOrCreateConversation(ctx.from.id);

    // Process through AI
    const aiResponse = await ChatManager.processMessage(
      ctx.message.text,
      {
        platform: 'telegram',
        userId: ctx.from.id,
        context: conversation.pageContext
      }
    );

    // Reply with markdown support
    await ctx.reply(aiResponse, { parse_mode: 'Markdown' });
  } catch (error) {
    console.error('AI processing error:', error);
    await ctx.reply('Sorry, I encountered an error processing your message.');
  }
});
```

**Streaming responses (for long AI outputs):**
```typescript
bot.on('text', async (ctx) => {
  const statusMessage = await ctx.reply('Thinking...');

  let fullResponse = '';

  await ChatManager.streamMessage(ctx.message.text, {
    onChunk: async (chunk) => {
      fullResponse += chunk;

      // Update message every 20 chunks to avoid rate limits
      if (fullResponse.length % 100 === 0) {
        await ctx.telegram.editMessageText(
          ctx.chat.id,
          statusMessage.message_id,
          undefined,
          fullResponse,
          { parse_mode: 'Markdown' }
        );
      }
    },
    onComplete: async () => {
      await ctx.telegram.editMessageText(
        ctx.chat.id,
        statusMessage.message_id,
        undefined,
        fullResponse,
        { parse_mode: 'Markdown' }
      );
    }
  });
});
```

### Interactive UI

**Inline keyboard:**
```typescript
import { Markup } from 'telegraf';

bot.command('menu', async (ctx) => {
  await ctx.reply(
    'Choose an option:',
    Markup.inlineKeyboard([
      [Markup.button.callback('Option 1', 'option_1')],
      [Markup.button.callback('Option 2', 'option_2')],
      [Markup.button.url('Visit Website', 'https://example.com')]
    ])
  );
});

// Handle button callbacks
bot.action('option_1', async (ctx) => {
  await ctx.answerCbQuery();
  await ctx.editMessageText('You selected Option 1');
});
```

**Context switching with page state:**
```typescript
bot.command('training', async (ctx) => {
  // Update conversation context
  await updateConversationContext(ctx.from.id, 'training');

  await ctx.reply(
    'Switched to Training mode. Ask me anything about your workouts!',
    Markup.inlineKeyboard([
      [Markup.button.callback('View Plan', 'view_plan')],
      [Markup.button.callback('Log Workout', 'log_workout')],
      [Markup.button.callback('Back to Menu', 'main_menu')]
    ])
  );
});
```

### File Handlers

**Photo handling:**
```typescript
bot.on('photo', async (ctx) => {
  const photo = ctx.message.photo[ctx.message.photo.length - 1];
  const fileLink = await ctx.telegram.getFileLink(photo.file_id);

  // Download or process photo
  const analysis = await analyzeImage(fileLink.href);

  await ctx.reply(`Analysis: ${analysis}`);
});
```

**Voice message handling:**
```typescript
bot.on('voice', async (ctx) => {
  const voice = ctx.message.voice;
  const fileLink = await ctx.telegram.getFileLink(voice.file_id);

  // Transcribe voice (e.g., using Whisper API)
  const transcript = await transcribeAudio(fileLink.href);

  await ctx.reply(`You said: ${transcript}`);
});
```

---

## DEPLOYMENT Workflow

**Use when:** Deploying Telegram bot to production.

### Deployment Checklist

**Create these todos for production deployment:**

```
- [ ] Determine deployment platform (Railway, Vercel, other)
- [ ] Set environment variables (TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET)
- [ ] Create webhook API route (/api/webhooks/telegram)
- [ ] [VERCEL] Disable Deployment Protection in settings
- [ ] [RAILWAY] Use dummy token for build, real token at runtime
- [ ] Deploy application
- [ ] Delete existing webhook or stop polling
- [ ] Set webhook with production URL
- [ ] Verify webhook: check getWebhookInfo
- [ ] Send test message to bot
- [ ] Monitor platform logs for errors
```

### Platform-Specific Deployment

#### Vercel Deployment

**Requirements:**
- HTTPS endpoint (automatic with Vercel)
- Deployment Protection disabled
- Edge runtime for longer timeouts (optional)

**Steps:**
1. Set environment variables in Vercel dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_WEBHOOK_SECRET`
   - `TELEGRAM_MINI_APP_URL` (if using Mini Apps)

2. Disable Deployment Protection:
   - Settings → Deployment Protection → Off

3. Deploy:
   ```bash
   vercel --prod
   ```

4. Set webhook:
   ```bash
   curl -X POST https://api.telegram.org/bot${TOKEN}/setWebhook \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://your-app.vercel.app/api/webhooks/telegram",
       "secret_token": "YOUR_SECRET"
     }'
   ```

5. Test: Send message to bot, check Vercel logs

#### Railway Deployment

**Requirements:**
- HTTPS endpoint (automatic with Railway)
- Dummy token for build phase
- Environment variables set before deployment

**Steps:**
1. Set environment variables:
   ```bash
   railway variables --set "TELEGRAM_BOT_TOKEN=<token>"
   railway variables --set "TELEGRAM_WEBHOOK_SECRET=<secret>"
   ```

2. Ensure bot service handles build phase:
   ```typescript
   const token = process.env.TELEGRAM_BOT_TOKEN || 'DUMMY_BUILD_TOKEN';
   ```

3. Deploy:
   ```bash
   railway up
   ```

4. Set webhook using Railway domain:
   ```bash
   # Get Railway URL from railway status
   railway status

   # Set webhook
   curl -X POST https://api.telegram.org/bot${TOKEN}/setWebhook \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://your-app.up.railway.app/api/webhooks/telegram",
       "secret_token": "YOUR_SECRET"
     }'
   ```

5. Monitor deployment:
   ```bash
   railway logs
   ```

### Migration: Polling → Webhook

**When switching from local to production:**

1. **Stop polling script:** Kill the `telegram-polling.js` process

2. **Delete webhook** (if any exists):
   ```bash
   curl -X POST https://api.telegram.org/bot${TOKEN}/deleteWebhook
   ```

3. **Deploy to production** with webhook route

4. **Set webhook** with production URL (see platform steps above)

5. **Verify switch:**
   ```bash
   curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo
   # Should show: url (your production URL), pending_update_count (should be 0 after test)
   ```

6. **Test:** Send message to bot, check production logs

---

## MINI APP INTEGRATION

**Use when:** User wants to add Telegram Mini App (web app within Telegram).

### Mini App Checklist

```
- [ ] Create Mini App via @BotFather: /newapp or /setmenubutton
- [ ] Create Next.js page for Mini App (e.g., /app/telegram-mini-app/page.tsx)
- [ ] Include Telegram Web App SDK script
- [ ] Implement client-side initialization
- [ ] Create server-side initData validation endpoint
- [ ] Set TELEGRAM_MINI_APP_URL environment variable
- [ ] Configure bot to launch Mini App (keyboard/inline button)
- [ ] Test Mini App opens from bot
- [ ] Verify theme integration
- [ ] Test data validation
```

### Mini App Setup (via @BotFather)

**Create Mini App:**
1. Message `@BotFather`
2. Send `/myapps`
3. Select your bot
4. Choose "Bot Settings" → "Menu Button" → "Edit Menu Button URL"
5. Enter your Mini App URL: `https://your-app.com/telegram-mini-app`

**Or create standalone app:**
1. Message `@BotFather`
2. Send `/newapp`
3. Follow prompts to set name, description, photo
4. Enter app URL

### Client-Side Mini App

**Create `app/telegram-mini-app/page.tsx`:**

```typescript
'use client';

import { useEffect, useState } from 'react';

declare global {
  interface Window {
    Telegram?: {
      WebApp: any;
    };
  }
}

export default function TelegramMiniApp() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize Telegram Web App
    const tg = window.Telegram?.WebApp;

    if (!tg) {
      console.error('Telegram Web App SDK not loaded');
      return;
    }

    // Notify Telegram app is ready
    tg.ready();

    // Get user data (UNSAFE - validate server-side)
    const initDataUnsafe = tg.initDataUnsafe;
    setUser(initDataUnsafe.user);

    // Apply Telegram theme
    document.body.style.backgroundColor = tg.themeParams.bg_color || '#ffffff';
    document.body.style.color = tg.themeParams.text_color || '#000000';

    // Listen for theme changes
    tg.onEvent('themeChanged', () => {
      document.body.style.backgroundColor = tg.themeParams.bg_color;
      document.body.style.color = tg.themeParams.text_color;
    });

    setLoading(false);

    // Enable closing confirmation for unsaved changes
    tg.enableClosingConfirmation();

    return () => {
      tg.disableClosingConfirmation();
    };
  }, []);

  const sendMessage = async (message: string) => {
    const tg = window.Telegram?.WebApp;

    // Validate on server with initData
    const response = await fetch('/api/telegram-mini-app/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-telegram-init-data': tg.initData // For server validation
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    return data;
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.first_name}!</h1>
      {/* Your Mini App UI */}
    </div>
  );
}
```

**Add SDK to layout:**

```typescript
// app/telegram-mini-app/layout.tsx
export default function TelegramMiniAppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <head>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Server-Side Validation (CRITICAL)

**NEVER trust `initDataUnsafe` - always validate server-side.**

**Create validation utility:**

```typescript
// lib/telegram/validate-init-data.ts
import crypto from 'crypto';

export function validateTelegramInitData(
  initData: string,
  botToken: string
): boolean {
  const urlParams = new URLSearchParams(initData);
  const hash = urlParams.get('hash');
  urlParams.delete('hash');

  // Create data-check-string
  const dataCheckArray = Array.from(urlParams.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`);
  const dataCheckString = dataCheckArray.join('\n');

  // Compute secret key
  const secretKey = crypto
    .createHmac('sha256', 'WebAppData')
    .update(botToken)
    .digest();

  // Compute hash
  const computedHash = crypto
    .createHmac('sha256', secretKey)
    .update(dataCheckString)
    .digest('hex');

  return computedHash === hash;
}

export function parseTelegramUser(initData: string) {
  const urlParams = new URLSearchParams(initData);
  const userJson = urlParams.get('user');

  if (!userJson) return null;

  return JSON.parse(userJson);
}
```

**Use in API route:**

```typescript
// app/api/telegram-mini-app/chat/route.ts
import { validateTelegramInitData, parseTelegramUser } from '@/lib/telegram/validate-init-data';

export async function POST(request: Request) {
  const initData = request.headers.get('x-telegram-init-data');

  if (!initData) {
    return Response.json({ error: 'Missing init data' }, { status: 400 });
  }

  // VALIDATE - critical for security
  const isValid = validateTelegramInitData(
    initData,
    process.env.TELEGRAM_BOT_TOKEN!
  );

  if (!isValid) {
    return Response.json({ error: 'Invalid init data' }, { status: 401 });
  }

  // NOW safe to use
  const user = parseTelegramUser(initData);
  const { message } = await request.json();

  // Process message with validated user
  const aiResponse = await processAIMessage(message, user.id);

  return Response.json({ response: aiResponse });
}
```

### Launching Mini App from Bot

**Inline keyboard button:**
```typescript
import { Markup } from 'telegraf';

bot.command('app', async (ctx) => {
  await ctx.reply(
    'Open Mini App:',
    Markup.inlineKeyboard([
      [Markup.button.webApp(
        'Launch App',
        process.env.TELEGRAM_MINI_APP_URL || 'https://your-app.com/telegram-mini-app'
      )]
    ])
  );
});
```

**Menu button (persistent):**
Set via @BotFather as shown above, or programmatically:

```typescript
await bot.telegram.setChatMenuButton({
  menu_button: {
    type: 'web_app',
    text: 'Open App',
    web_app: {
      url: process.env.TELEGRAM_MINI_APP_URL!
    }
  }
});
```

### Mini App Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Mini App won't load | Missing HTTPS | Use https:// in production (http:// only in test environment) |
| initData validation fails | Wrong bot token or hash computation | Verify bot token, check hash algorithm matches spec |
| Theme colors wrong | Hardcoded colors | Use `tg.themeParams` dynamically, listen for `themeChanged` |
| App closes unexpectedly | Missing `ready()` call | Call `tg.ready()` early in initialization |
| Caching shows old version | Railway/Vercel cache | Force dynamic rendering: `export const dynamic = 'force-dynamic'` |
| Buttons disabled in production | Wrong URL in env var | Check `TELEGRAM_MINI_APP_URL` matches deployed URL |

---

## Problem-Solution Quick Reference

### Bot Not Responding

**Checklist:**
1. Verify bot token: `curl https://api.telegram.org/bot${TOKEN}/getMe`
2. Check webhook status: `curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo`
3. Review platform logs (Railway: `railway logs`, Vercel: dashboard)
4. Verify secret token matches in webhook and API route
5. Ensure no polling script running if using webhook

### Local Setup Issues

**Problem:** Polling not receiving updates
- **Solution:** Delete webhook: `curl -X POST https://api.telegram.org/bot${TOKEN}/deleteWebhook`

**Problem:** Port 3000 already in use
- **Solution:** Change port in polling script or kill process on port 3000

**Problem:** Updates received but bot doesn't respond
- **Solution:** Check bot service is initialized, commands are registered, no errors in console

### Production Deployment Issues

**Problem:** Works locally, fails in production
- **Cause:** Build-time token initialization or environment variable issues
- **Solution:** Use dummy token for build, ensure env vars set before deployment

**Problem:** Webhook returns 401
- **Cause:** Secret token mismatch
- **Solution:** Verify `X-Telegram-Bot-Api-Secret-Token` header matches `setWebhook` secret

**Problem:** Vercel timeout errors
- **Cause:** Function exceeds 10-second limit on Hobby plan
- **Solution:** Use edge runtime or optimize processing time

**Problem:** Railway caching issues
- **Cause:** Static optimization caching responses
- **Solution:** Force dynamic: `export const dynamic = 'force-dynamic'`

### Mini App Issues

**Problem:** initDataUnsafe shows data but validation fails
- **Cause:** Using `initDataUnsafe` instead of `initData` for validation
- **Solution:** Always validate `initData` (raw string) server-side, never trust `initDataUnsafe`

**Problem:** Mini App theme doesn't match Telegram
- **Cause:** Hardcoded colors
- **Solution:** Use `tg.themeParams` and listen for `themeChanged` event

---

## Best Practices

### Development

- **Use polling locally, webhooks in production** - simplifies local development
- **Never run polling and webhook simultaneously** - causes conflicts
- **Validate Mini App data server-side** - `initDataUnsafe` is unsafe, validate `initData`
- **Test with @BotFather commands** - use `/setcommands` to show command list in UI

### Production

- **Use environment variables** for tokens (never hardcode)
- **Set secret tokens** for webhooks (prevents unauthorized requests)
- **Monitor webhook health** with `getWebhookInfo` (check `pending_update_count`)
- **Force dynamic rendering** on Next.js to prevent caching issues
- **Use dummy token for build** on Railway/Vercel to avoid initialization errors

### Security

- **Validate webhook secret tokens** in all webhook endpoints
- **Validate Mini App initData** server-side using HMAC-SHA-256
- **Never expose bot token** in client code or logs
- **Use HTTPS** for webhooks in production (required by Telegram)

### Performance

- **Respond quickly** to webhooks (<10 seconds on Vercel Hobby)
- **Use edge functions** for longer timeout limits
- **Avoid heavy processing** in webhook endpoint (queue jobs instead)
- **Cache static responses** when possible

---

## Additional Resources

### Official Documentation

- **Bot API:** https://core.telegram.org/bots/api
- **Mini Apps (Web Apps):** https://core.telegram.org/bots/webapps
- **Telegraf Docs:** https://telegraf.js.org/

### Useful Tools

- **@BotFather:** Create and configure bots
- **ngrok:** Local webhook testing via HTTPS tunnel
- **Telegram Test Environment:** Test Mini Apps with http:// (https://docs.telegram-mini-apps.com/platform/test-environment)

### Platform Documentation

- **Vercel Deployment:** https://vercel.com/docs
- **Railway Deployment:** https://docs.railway.com/

---

## When Telegram Integration Fails

**CRITICAL: Diagnose before acting. Never guess under pressure.**

1. **Check webhook status** - `getWebhookInfo` shows errors, URL, pending updates
2. **Review platform logs** - Railway: `railway logs`, Vercel: deployment logs
3. **Verify environment variables** - Token, secret, Mini App URL
4. **Test bot token** - `curl https://api.telegram.org/bot${TOKEN}/getMe`
5. **Check Telegram status** - https://core.telegram.org/bots/api (rare outages)
6. **Verify deployment platform** - Deployment Protection (Vercel), caching (Railway)

**For webhook issues: verify → delete → redeploy → set → test**
**For Mini App issues: validate server-side → check theme → verify URL**
