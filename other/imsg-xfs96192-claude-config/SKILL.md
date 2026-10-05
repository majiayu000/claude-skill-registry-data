---
name: imsg
description: "iMessage/SMS CLI for listing chats, history, watch, and sending."
description_zh: "iMessage/短信收发与历史查看"
description_en: "Send and browse iMessage/SMS history"
version: 1.0.0
display_name: "imsg"
display_name_en: "imsg"
visibility: "public"
icon: "https://codebuddy-platform-1258344699.cos.accelerate.myqcloud.com/public/45edac6b-2078-4678-89f3-6f9800cf5e5f/avatar/skill/au_82f559c4-83e.png"
---

# imsg

Use `imsg` to read and send Messages.app iMessage/SMS on macOS.

Requirements
- Messages.app signed in
- Full Disk Access for your terminal
- Automation permission to control Messages.app (for sending)

Common commands
- List chats: `imsg chats --limit 10 --json`
- History: `imsg history --chat-id 1 --limit 20 --attachments --json`
- Watch: `imsg watch --chat-id 1 --attachments`
- Send: `imsg send --to "+14155551212" --text "hi" --file /path/pic.jpg`

Notes
- `--service imessage|sms|auto` controls delivery.
- Confirm recipient + message before sending.
