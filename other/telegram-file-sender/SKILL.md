---
name: telegram-file-sender
description: Send local files to Telegram chats through OpenClaw CLI delivery. Use when a user asks to send or forward a file (md/txt/pdf/image/video) to Telegram, especially from workspace paths. Supports direct chat targets and group/topic targets.
---

# Telegram File Sender

Send a local file as a Telegram attachment via OpenClaw CLI.

## Command

```bash
openclaw message send \
  --channel telegram \
  --target <telegram-target> \
  --media <file-path> \
  --message "<optional caption>"
```

## Target format

- Direct chat: `<numeric-chat-id>`
- Group/topic: `group:<chat-id>:topic:<topic-id>`

## Safe workflow

1. Confirm source file exists.
2. Use workspace-relative path where possible.
3. Send with `--message` caption that explains the file.
4. If needed, send a follow-up text summary separately.

## Examples

```bash
# Send markdown report to direct Telegram chat
openclaw message send --channel telegram --target 8267670204 \
  --media /root/.openclaw/workspace/staging/reports/iran-hormuz.md \
  --message "Iran-Hormuz watchboard report"

# Send image attachment
openclaw message send --channel telegram --target 8267670204 \
  --media /root/.openclaw/workspace/staging/plots/fund_011609_30d.png \
  --message "科创50 30日图"
```

## Failure handling

- If send fails, capture stderr and return actionable reason (invalid target, missing file, provider error).
- If file type is unsupported by provider, convert/zip and retry.
- For oversized files, compress or split before retrying.
