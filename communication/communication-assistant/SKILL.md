---
name: communication-assistant
description: Unified lazy-mode communication assistant for Vipin across WhatsApp, WeChat, QQ, Feishu/Lark, and email. Use when Codex needs to triage messages, summarize chats in Chinese, draft replies, save reusable outbox items, prefill a chat box without sending, or route to platform-specific messaging adapters while preserving QR/login-state credentials and requiring explicit approval before any send.
---

# Communication Assistant

Use this skill as the routing layer for personal communication tasks across chat and email. It does not replace platform-specific skills; it coordinates them, keeps a shared outbox, and enforces a conservative "prefill, do not send" default.

## Defaults

- Keep normal summaries in Chinese.
- Never look for, recover, ask to store, or record account passwords.
- Use QR login, existing browser/client sessions, official OAuth/API tokens, or platform-local session files only.
- Store any sessions, tokens, configs, and message outbox data in the git-ignored runtime folder described below.
- Do not expose private chats, contacts, tokens, cookies, QR codes, or message bodies in public wiki pages, commits, or partner prompts.
- Prefer `prefilled` over `sent`. Real sending requires explicit user approval for the exact platform, target, and outbox item.
- If a platform is blocked or unsafe, mark that adapter as pending instead of pretending it works.

## Runtime Paths

Runtime data lives under `$env:COMMUNICATION_ASSISTANT_HOME` if it is set. Otherwise it
goes to `.wiki-tmp/communication-assistant/` inside the skill folder (or inside the
enclosing notes repo, if the skill sits in a folder that has both `AGENTS.md` and
`.wiki-schema.md`). Either way it has four git-ignored subfolders: `config`, `sessions`,
`outbox` and `logs`.

The helper script prints the folders in use and manages outbox items. Run it from the
skill folder:

```powershell
node scripts/outbox.js paths
node scripts/outbox.js create --platform wechat --target "Alice" --message "我晚点回复你。" --context "reply to unread message"
node scripts/outbox.js list
node scripts/outbox.js mark --id "<outbox-id>" --status prefilled
node scripts/outbox.js cancel --id "<outbox-id>"
```

## Platform Routing

Use the safest available adapter for each task:

| Platform | First choice | Fallback | Notes |
| --- | --- | --- | --- |
| Email | `gmail-skill` (third-party; see THIRD_PARTY_SKILLS.md) | browser review via `chrome-automation` | Email has real Gmail drafts; use those before chat-style outbox. |
| Feishu/Lark | `lark-im` / `feishu-bridge` | `chrome-automation` | API first, browser fallback for web-only flows. |
| WeChat | `wechat-cli` read/search if configured | `wxauto` Windows client prefill | Personal WeChat has no stable official user API; avoid password storage. |
| WhatsApp | WhatsApp Web QR session via `whatsapp-web.js`/WAHA-style adapter | OpenClaw/Warelay if the user wants a heavier gateway | Prefer isolated browser/session profile. |
| QQ | official QQ Bot/OpenClaw channel for bot flows | NapCat/OneBot only with explicit risk acceptance | Personal QQ client automation is fragile; prefer bot-style integrations. |

Read references only when needed:

- `references/adapters.md` for adapter selection and setup notes.
- `references/safety.md` for approval, secret, and live-account boundaries.
- `references/outbox.md` for the shared draft/prefill lifecycle.

## Workflow

1. Identify platform and account/session.
2. Read or search through the least intrusive safe adapter.
3. Summarize in Chinese:
   - who sent it
   - what they want
   - urgency or deadline
   - risk / hidden obligation
   - suggested response
4. Draft the response and create an outbox item.
5. If the user asks to prefill, place text in the chat input without sending when the adapter supports it.
6. If the user explicitly approves sending, verify target and text one more time, then use the platform adapter's send path.

## Useful User Prompts

```text
帮我看微信未读消息，中文讲重点。
帮我回 WhatsApp 这条，先别发。
查一下 QQ 有没有课程/签证/账单相关消息。
把刚才那条回复填到微信聊天框，不要发送。
我确认，发送 outbox 里这条。
```

## Safety Checks Before Live Actions

- Confirm the platform and target.
- Confirm whether the action is read-only, outbox-only, prefill-only, or send.
- For send, require explicit approval in the current conversation.
- Do not use delegated partners for raw private chat content unless the user explicitly approves sharing that content.
- When browser or desktop automation is needed, warn that a window may open or focus may change.
