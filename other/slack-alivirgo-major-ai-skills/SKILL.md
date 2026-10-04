---
name: slack
description: "Build Slack apps with Bolt, Block Kit, events, slash commands, and scoped Web API operations."
category: productivity
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["slack", "web-api", "block-kit", "bolt", "chatops", "events-api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Slack Workspace Collaboration AI Skill Guide (Claude)

## Overview & Engine Architecture
Slack is a channel-based collaboration platform with automation via the **Web API**, **Events API**, **Interactivity**, and app frameworks like **Bolt**. Messages can be plain text or **Block Kit** layouts. Claude operates as a Principal ChatOps Engineer, specializing in **`chat.postMessage`**, **Block Kit modals**, **slash commands**, **event acknowledgements**, and **least-privilege OAuth scopes**.

### Slack Platform Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Slack Architecture                          │
│                                                             │
│  Workspace Model                                            │
│  ├── Workspaces / Channels / DMs / User groups              │
│  ├── Messages / Threads / Reactions / Files                 │
│  └── Apps / Bots / Workflows                                │
│                                                             │
│  Developer Surfaces                                         │
│  ├── Web API methods (chat.*, views.*, users.*)             │
│  ├── Events API + Interactivity + Slash commands            │
│  └── Block Kit (sections, actions, inputs)                  │
│                                                             │
│  App Runtime                                                │
│  ├── Bolt (JS/Python)                                       │
│  ├── Socket Mode / HTTP Request URLs                        │
│  └── OAuth scopes & tokens (bot xoxb-, user xoxp-)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Ack Fast**: Acknowledge Events/Interactivity within timeouts before doing slow work.
2. **Scopes Minimal**: Request only scopes required (`chat:write`, `channels:history`, etc.).
3. **Block Kit over Unformatted Walls**: Use sections/fields/buttons for actionable messages.
4. **Thread Hygiene**: Prefer `thread_ts` for follow-ups to reduce channel noise.
5. **Never Log Tokens**: Keep bot tokens in secrets managers; rotate on leak.

---

## Production Node.js: Bolt Slash Command + Block Kit Message

```javascript
// ==============================================================================
// Slack Bolt: /status command posts a Block Kit update into the channel
// npm i @slack/bolt
// ==============================================================================
const { App } = require("@slack/bolt");

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

app.command("/status", async ({ command, ack, client }) => {
  await ack();
  const service = (command.text || "api").trim();

  await client.chat.postMessage({
    channel: command.channel_id,
    text: `Status for ${service}`,
    blocks: [
      {
        type: "header",
        text: { type: "plain_text", text: `Service status: ${service}` },
      },
      {
        type: "section",
        fields: [
          { type: "mrkdwn", text: "*Environment:*\nproduction" },
          { type: "mrkdwn", text: "*Reported by:*\n<@" + command.user_id + ">" },
        ],
      },
      {
        type: "actions",
        elements: [
          {
            type: "button",
            text: { type: "plain_text", text: "Open runbook" },
            url: "https://example.com/runbooks/" + encodeURIComponent(service),
          },
        ],
      },
    ],
  });
});

(async () => {
  await app.start();
  console.log("⚡️ Slack Bolt app running");
})();
```

Web API one-liner:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C01234567","text":"Deploy completed"}'
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`not_in_channel`** | Bot not invited. | `/invite @Bot` into channel. |
| **`invalid_auth`** | Wrong/revoked token. | Reinstall app; verify `xoxb-` bot token. |
| **`missing_scope`** | Scope not granted. | Add scope + reinstall to workspace. |
| **Interactivity timeout** | Slow handler before ack. | `ack()` immediately; defer heavy work. |

---

## Best Practices

1. Use `text` fallback alongside `blocks` for notifications/accessibility.
2. Prefer Socket Mode for local/dev; HTTP endpoints for production ingress.
3. Store channel IDs in config, not brittle channel names alone.

### Essential References
- Web API: `https://slack.com/api/`
- Bolt JS: `@slack/bolt`
- Block Kit Builder for prototyping layouts

---

## Agent Operational Directive
> **MANDATORY**: Acknowledge Slack events/commands immediately. Use least-privilege scopes. Prefer Block Kit + threads for operational messages; never commit bot tokens.
