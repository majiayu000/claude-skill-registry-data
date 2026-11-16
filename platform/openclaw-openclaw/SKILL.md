---
name: openclaw--openclaw
description: "Personal AI assistant chạy trên mọi OS/platform — 20+ channels (WhatsApp, Telegram, Zalo, WeChat, Discord, Slack...), Skills system, voice, Canvas. Dùng khi build hoặc setup personal AI assistant đa kênh."
allowed-tools: Bash, Read, Write
user-invocable: true
---

OpenClaw là personal AI assistant self-hosted, hỗ trợ 20+ messaging channels và Skills system.

## Supported channels

WhatsApp · Telegram · Slack · Discord · Signal · iMessage · LINE · WeChat · QQ · Zalo · Zalo Personal · Matrix · Mattermost · IRC · Microsoft Teams · Feishu · Nostr · Tlon · Twitch · Synology Chat

## Quick start

```bash
npm install -g openclaw
openclaw onboard   # guided setup: gateway, workspace, channels, skills
```

## Skills integration

```bash
# Install yamtam skills vào openclaw
npx skills add yanacuti1121/yana-ai
```

## Features

- Voice (macOS/iOS/Android) + live Canvas
- Skills system — portable Agent Skills format
- Memory system — persistent context
- Gateway control plane — manage channels từ một nơi

## Source

https://github.com/openclaw/openclaw · ⭐376K
