---
name: telegram
description: >-
  Telegram communications, bot operations, formatted reports, channel/inbox
  triage, and bot hosting strategies. One router over specialized parts:
  telegram-report, telegram-rich-messages, telegram-bot-hosting-triage,
  telegram-serverless, content-delivery-format, and tg-check.
---

# telegram — communications and operations router

> Home branch in Memora: `root/skill/telegram`.
>
> Telethon userbot sessions (a `telegram-userbot` MCP client and a local fetcher script of your own)
> are strictly **read-only**. Never send messages from the owner's personal account;
> outbound bot reports require explicit owner approval.

## Choosing a part

| Task | Part |
|---|---|
| Rich message formatting (markdown, code blocks, topics, attachments) | `parts/telegram-rich-messages/` |
| Automated bot reporting and notification delivery | `parts/telegram-report/` |
| Checking a Telegram inbox and channel feeds | `parts/tg-check/` |
| Bot architecture, hosting triage, and deployment strategy | `skills/telegram/parts/telegram-bot-hosting-triage/` |
| Running a bot on Telegram Serverless (`tgcloud`, V8 runtime, secrets) | `parts/telegram-serverless/` |
| Delivering a result in the right shape (text, rich message, PDF/HTML, splitting long answers) | `parts/content-delivery-format/` |

## Rules

- Walk `root/skill/telegram` in Memora before starting; record channel triage verdicts or bot hosting decisions as nodes.
- If `read_files` returns `[BLOCKED]` on `inbox/` files (covered by `.gitignore`), read them through the terminal (`python` / `sed`).
- Never send a Telegram message or post without the owner's explicit confirmation via `ask_questions`.

## Related

`email` (mail triage), `media` (`skills/media/parts/ru-tts-fallback/` for voice synthesis), `research` (channel-fed source collection).
