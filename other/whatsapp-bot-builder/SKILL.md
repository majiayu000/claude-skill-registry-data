---
name: whatsapp-bot-builder
description: Build WhatsApp bots with Baileys or whatsapp-web.js. Session management, multi-device, message handling, media, rate limits. Use PROACTIVELY for WhatsApp bot development or messaging automation.
stacks:
  - whatsapp
tags:
  - whatsapp
  - bot
  - baileys
  - messaging
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Building WhatsApp bots or automation
- Integrating WhatsApp messaging into applications
- Working with Baileys, whatsapp-web.js, or venom-bot
- Implementing WhatsApp Business API integration

## Do not use this skill when

- Building Telegram bots (use telegram-bot-builder)
- Working with official WhatsApp Cloud API only (basic REST)
- The task is unrelated to WhatsApp messaging

## Purpose

Expert in WhatsApp bot development using unofficial libraries (Baileys, whatsapp-web.js) and official Business API. Deep knowledge of session management, multi-device protocol, rate limiting, and media handling.

## Capabilities

### Core Libraries
- Baileys (@whiskeysockets/baileys) — lightweight, multi-device, recommended
- whatsapp-web.js — Puppeteer-based, heavier but mature
- venom-bot — alternative Puppeteer-based client
- Official WhatsApp Business API via Meta — paid, reliable, production-grade

### Message Handling
- Text messages, media (images, video, audio, documents)
- Buttons, lists, and interactive message templates
- Message reactions and replies
- Group message handling and admin operations
- Contact and location messages

### Session & Authentication
- Multi-file auth state persistence (prevent re-QR on restart)
- Multi-device protocol support (phone doesn't need to stay online)
- Session backup and restoration across restarts
- QR code generation for initial pairing

### Rate Limiting & Safety
- WhatsApp bans numbers sending >200 msgs/day to new contacts
- Warm-up period required for new numbers
- Different limits for groups vs individual chats
- Official Business API has higher limits with verified numbers

## Behavioral Traits
- Always persists auth state to prevent re-QR-scan on restart
- Uses Baileys multi-device protocol (not legacy)
- Implements graceful shutdown to save session state
- Respects rate limits — queues messages with delays
- Handles connection drops with automatic reconnection
- Validates phone number format (1234567890@s.whatsapp.net)
- Uses downloadMediaMessage() for received media

## Important Constraints
- **Unofficial libraries may break** when WhatsApp updates protocol
- **Rate limits are strict** — WhatsApp will ban numbers that spam
- **Media size limits** — 16MB for images, 64MB for video/documents
- **Business API** — for production at scale, use official Meta API (paid)
- **Groups** — bot must be admin for management operations
- **Number format** — always use `{number}@s.whatsapp.net` format
- **Multi-device** — Baileys supports natively, phone can go offline
