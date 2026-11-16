---
name: pewdiepie-archdaemon--odysseus
description: "Self-hosted AI workspace — Chat, Agent, Email IMAP AI triage, Deep Research, Calendar, Memory/Skills. Dùng khi cần build hoặc self-host một AI assistant đầy đủ tính năng."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Odysseus là self-hosted AI workspace: local-first, privacy-first, no trojan. Chạy trên hardware của anh.

## Features

- **Chat** — vLLM, llama.cpp, Ollama, OpenRouter, OpenAI
- **Agent** — MCP, web, files, shell, skills, memory
- **Email** — IMAP/SMTP + AI triage: urgency, auto-tag, auto-summary, auto-reply drafts, spam filter
- **Deep Research** — multi-step research với visual report
- **Memory/Skills** — ChromaDB, fastembed, vector + keyword retrieval
- **Calendar** — CalDAV sync (Radicale, Nextcloud, Apple, Fastmail)
- **Notes & Tasks** — reminders, checklist, cron-style scheduled tasks
- **Mobile PWA** — responsive, installable, touch gestures
- **Cookbook** — scan hardware, recommend models, click to download + serve

## Quick start

```bash
git clone https://github.com/pewdiepie-archdaemon/odysseus
cd odysseus
# defaults work out of the box
docker compose up
# configure models/search/email in Settings
```

## Source

https://github.com/pewdiepie-archdaemon/odysseus · ⭐39K
