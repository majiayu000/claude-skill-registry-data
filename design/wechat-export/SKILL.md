---
name: wechat-export
description: Export WeChat chat history using chatlog server. Use when user mentions WeChat, exporting chats, chat history, or WeChat messages. Requires chatlog server running locally.
---

# WeChat Chat Export

Export WeChat chat history using the chatlog local server.

## Prerequisites

- chatlog server running (with --auto-decrypt recommended)
- Default address: http://127.0.0.1:5030

## Steps

**1. Find the contact's WeChat ID:**
```bash
curl "http://127.0.0.1:5030/api/v1/contact?keyword=<name_or_alias>"
```
Returns: UserName (wxid), Alias, Remark, NickName

**2. Export chat history:**
```bash
curl "http://127.0.0.1:5030/api/v1/chatlog?time=<start>~<end>&talker=<wxid>&limit=2000" > output.txt
```

## Parameters

| Param  | Format                | Example                    |
|--------|-----------------------|----------------------------|
| time   | YYYY-MM-DD~YYYY-MM-DD | 2025-12-01~2025-12-03      |
| talker | UserName or Alias     | Hqt798317304 or jasonhu6   |
| limit  | Number                | 2000 (increase for long chats) |

## Gotchas

- Single-day queries (`time=2025-12-02`) may return empty — use a range instead
- If recent messages are missing, manually trigger decrypt:
```bash
chatlog decrypt -d <data_dir> -k <data_key> -w <work_dir> -p darwin -v 4
```
