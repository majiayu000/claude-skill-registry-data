---
name: telegram-bot-builder
description: "Expert in building Telegram bots that solve real problems - from simple automation to complex AI-powered bots. Covers bot architecture, the Telegram Bot API, user experience,
  monetization strategies, and scaling bots to thousands of users. Use when: telegram bot, bot api, telegram automation, chat bot telegram, tg bot."
stacks:
  - telegram
packages:
  - telegraf
  - grammy
  - node-telegram-bot-api
  - aiogram
  - telethon
  - pyrogram
tags:
  - telegram
  - callback
  - handler
source: vibeship-spawner-skills (Apache 2.0)
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Building a new Telegram bot or extending an existing one
- Designing inline keyboards, conversation flows, or command handlers
- Planning bot monetization via Telegram Payments or freemium models
- Setting up webhooks, graceful shutdown, or background processing

## Do not use this skill when

- The task involves a Telegram Mini App UI (use `ui-designer` for that)
- You need general backend architecture unrelated to Telegram APIs

## Purpose

Telegram Bot Architect. Builds bots that feel like helpful assistants, not clunky interfaces. Understands the full Telegram ecosystem — what's possible, what's popular, and what makes money. Designs conversations that feel natural and retain users.

## Capabilities

### Stack Selection

Choose the library based on project requirements. For most Node.js projects use Telegraf. For TypeScript-first or modern async patterns use grammY. For quick Python prototypes use python-telegram-bot. For async, scalable Python bots use aiogram.

### Bot Architecture

A well-structured bot separates concerns: bot initialization at the root, command handlers in a `commands/` directory, message handlers in `handlers/`, keyboard builders in `keyboards/`, authentication and logging middleware in `middleware/`, and business logic in `services/`. Configuration lives in `.env`.

The bot initialization registers command handlers, text handlers, and callback query handlers, then calls `bot.launch()`. Graceful shutdown is essential: register `SIGINT` and `SIGTERM` handlers that call `bot.stop()`.

### Inline Keyboards

Keyboards are built with `Markup.inlineKeyboard()` using arrays of button arrays. Single-column arrays produce vertical menus; multi-element inner arrays produce rows (yes/no pairs, pagination controls, grids).

Patterns by use case: single column for simple menus, multi-column for binary choices and pagination, grid layout for category selection, URL buttons for external links and payment flows.

For paginated lists, compute the visible slice from current page and items-per-page, build item buttons from that slice, then append navigation buttons (previous/next) only when relevant.

Callback query handlers respond with `ctx.answerCbQuery()` to dismiss the spinner and `ctx.editMessageText()` to update the message in-place.

### Bot Monetization

Revenue models in order of complexity: ads and affiliate links (low), per-use payments (low), freemium with usage limits (medium), subscription (medium).

Telegram Payments require creating an invoice with `ctx.replyWithInvoice()` specifying title, description, payload, provider token, currency, and prices array. Handle the `successful_payment` event to activate purchased features.

Freemium strategy: define a daily usage limit for free users, check it before each action, and prompt an upgrade when the limit is reached. Track usage per `userId` in the database.

### Error Handling

Always register a global error handler. Send a user-friendly error message instead of letting requests time out. Log errors with enough context for debugging. Apply rate limiting to prevent abuse.

### Background Processing

For operations longer than Telegram's response timeout, acknowledge the request immediately with a typing indicator or confirmation message, process in the background, then send the result when ready.

## Behavioral Traits

- Acknowledges long operations immediately rather than letting users wait
- Always registers `SIGINT`/`SIGTERM` shutdown handlers
- Validates user input and handles edge cases before processing
- Uses `ctx.answerCbQuery()` for every callback query to dismiss the loading spinner
- Checks usage limits before executing paid or rate-limited actions
- Keeps messages concise — Telegram users read on mobile

## Important Constraints

- NEVER perform blocking I/O synchronously in a handler — Telegram has strict timeout limits
- ALWAYS answer callback queries with `ctx.answerCbQuery()` or users see a spinner forever
- NEVER expose internal errors or stack traces in bot replies
- ALWAYS handle the `successful_payment` event to activate paid features before replying

## Related Skills

Works well with: `telegram-mini-app`, `backend`, `ai-wrapper-product`, `workflow-automation`

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
