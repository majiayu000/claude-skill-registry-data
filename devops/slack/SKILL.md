---
name: slack
description: Use when slack Automation Hub — Bot, Notifier, and Slash Commands for
  team communication, DevOps alerts, and workflow automation. Monetize through integration-as-a-service.
domain: integrations
author: oyi77
license: Apache-2.0
subdomain: integrations
tags:
- api
- automation
- bot
- integrations
- notifications
- slack
- slash-commands
- third-party
- workflow
- communication
version: 1.0.0
category: integrations
---


# Slack Automation Hub

## Overview

Slack Automation Hub provides Bot, Notifier, and Slash Commands for team communication, DevOps alerts, and workflow automation. Monetize through integration-as-a-service.




## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

Slack is where work happens for millions of teams. Automating Slack interactions is a high-demand, high-ROI skill:

| Service | ROI Estimate | Market |
|---------|-------------|--------|
| Custom bot development (Ops/Sales/Support) | $3K-$15K/bot | Mid-market companies needing internal tools |
| DevOps alert integration (PagerDuty, Datadog, Grafana → Slack) | $1K-$5K/setup + $500-2K/mo | Engineering teams, SRE |
| Slash command utility suite | $2K-$6K/setup | Any team with recurring workflows (PTO, standup, approvals) |
| Multi-channel notification pipeline | $500-$2K/setup | E-commerce, SaaS, monitoring dashboards |
| Slack workflow + automation consulting | $200-$400/hr | Companies scaling their Slack usage |
| Compliance/audit Slack log archiving | $1K-$4K/mo retainer | Regulated industries (FINRA, legal) |

**Combined monthly recurring potential: $3K-$12K/client** (communication infrastructure retainer).

### Who Pays
- **Tech startups (10-50 people)** — need DevOps alerts but no SRE yet ($500-2K/mo)
- **Mid-market SaaS (50-500)** — custom bots for sales/support/customer ops ($3-8K)
- **Agencies** — client notification dashboards ($1-3K/project)
- **E-commerce** — order/shipping alerts in Slack channels ($500-2K/mo)
- **Enterprise teams** — compliance auditing, custom slash commands ($5-15K)

## Combined Capabilities

| Capability | Scope | Output |
|-----------|-------|--------|
| **Slack Bot** | Real-time messaging, event handling (message.im, app_mention, reactions), user lookup, channel management, interactive components (buttons, modals) | Python SDK apps, Bolt.js apps, event handlers |
| **Slack Notifier** | Webhook-based notifications, rich message formatting (blocks, attachments), channel routing, rate-limited streaming | Incoming webhook URLs, curl/python callers, CI/CD integration |
| **Slash Commands** | Custom `/command` handlers, parameter parsing, ephemeral vs in-channel responses, modals, command discovery | Bolt app handlers, command registrations |

## Authentication & Setup

Three auth modes, choose based on use case:

```bash
# Mode 1: Incoming Webhook (simplest — sending only)
# Create at: https://api.slack.com/apps → Your App → Incoming Webhooks
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00/B00/YOUR_WEBHOOK_ID"

# Mode 2: Bot Token (full API access)
# Create at: https://api.slack.com/apps → Your App → Bot Tokens
export SLACK_BOT_TOKEN="xoxb-YOUR_BOT_TOKEN"
export SLACK_SIGNING_SECRET="YOUR_SIGNING_SECRET"

# Mode 3: User Token (act as a user — rarely needed)
# Requires OAuth with proper scopes
export SLACK_USER_TOKEN="xoxp-YOUR_USER_TOKEN"
```

### Required Bot Scopes (by feature)

| Scope | Feature |
|-------|---------|
| `chat:write` | Send messages (core) |
| `chat:write.public` | Post to channels without being invited |
| `channels:history` | Read channel messages |
| `channels:read` | List/join channels |
| `users:read` | Look up users |
| `reactions:read` | Read reactions |
| `commands` | Register slash commands |
| `incoming-webhook` | Create webhook URLs |

```python
# Shared setup for all Slack automation
import os, json, requests

SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_USER_TOKEN")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")
HEADERS = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json",
}
API = "https://slack.com/api"
```

## Concrete Action Flows

### Flow 1: Send Rich Notification (Notifier)

The most common Slack automation — send formatted alerts from any system:

```bash
#!/usr/bin/env bash
# slack-notify.sh — Send rich Slack notification
# Usage: ./slack-notify.sh "Deploy complete" "v2.3.1" "good"

WEBHOOK_URL="${SLACK_WEBHOOK_URL:-$1}"
TITLE="${2:-Notification}"
MESSAGE="${3:-}"
COLOR="${4:-#36a64f}"  # good, warning, danger, or hex

if [ -z "$WEBHOOK_URL" ]; then
  echo "Set SLACK_WEBHOOK_URL or pass as \$1"
  exit 1
fi

curl -s -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$(cat <<EOF
{
  "attachments": [{
    "color": "$COLOR",
    "title": "$TITLE",
    "text": "$MESSAGE",
    "ts": $(date +%s),
    "footer": "Automation Bot"
  }]
}
EOF
)"
```

```python
# Python version — send rich block messages via API
def send_slack_message(channel, text, blocks=None):
    """Send a message to a Slack channel via API."""
    url = f"{API}/chat.postMessage"
    payload = {"channel": channel, "text": text}
    if blocks:
        payload["blocks"] = blocks
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")
    return data

def send_alert(channel, title, message, severity="info"):
    """Send a formatted alert with blocks."""
    color_map = {"info": "#36a64f", "warning": "#ffcc00", "error": "#ff0000", "critical": "#cc0000"}
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": title}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        {"type": "context", "elements": [
            {"type": "mrkdwn", "text": f":signal_strength: Severity: *{severity}*"}
        ]},
        {"type": "divider"},
    ]
    return send_slack_message(channel, title, blocks)

# Example: CI/CD deploy notification
send_alert(
    channel="#deployments",
    title="Deployment Complete :rocket:",
    message="*Version:* v2.3.1\n*Branch:* main\n*Environment:* production\n*Duration:* 2m 34s",
    severity="info",
)
```

### Flow 2: Slash Command Handler (Bolt.js)

Register a `/standup` command that collects daily standup reports:

```javascript
// app.js — Bolt.js Slack app with slash commands
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

// Register /standup command
app.command('/standup', async ({ command, ack, respond, client }) => {
  await ack();

  // Parse arguments: /standup yesterday "Fixed login bug" today "Working on auth"
  const params = {};
  const parts = command.text.match(/(\w+)\s+"([^"]+)"/g) || [];
  for (const p of parts) {
    const [key, ...val] = p.split(/\s+/);
    params[key.toLowerCase()] = val.join(' ').replace(/^"|"$/g, '');
  }

  const yesterday = params.yesterday || 'N/A';
  const today = params.today || 'N/A';
  const blockers = params.blockers || 'None';

  // Post to the channel as an ephemeral message (only the user sees it)
  // Then log to a private standup channel
  await respond({
    response_type: 'ephemeral',
    text: `Standup recorded! :white_check_mark:`,
  });

  await client.chat.postMessage({
    channel: '#standup-logs',
    text: `*Standup from <@${command.user_id}>*\n> *Yesterday:* ${yesterday}\n> *Today:* ${today}\n> *Blockers:* ${blockers}`,
  });
});

// Register /deploy command with buttons
app.command('/deploy', async ({ command, ack, respond, client }) => {
  await ack();

  if (!command.text) {
    await respond({ text: 'Usage: `/deploy <version> [environment=staging]`', response_type: 'ephemeral' });
    return;
  }

  const [version, env = 'staging'] = command.text.split(/\s+/);

  await respond({
    response_type: 'in_channel',
    blocks: [
      { type: 'section', text: { type: 'mrkdwn', text: `:rocket: *Deploy Request*\n*Version:* ${version}\n*Environment:* ${env}` } },
      { type: 'actions', elements: [
        { type: 'button', text: { type: 'plain_text', text: 'Approve' }, style: 'primary', value: `approve:${version}:${env}` },
        { type: 'button', text: { type: 'plain_text', text: 'Cancel' }, style: 'danger', value: `cancel:${version}:${env}` },
      ]},
    ],
  });
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log('Slack bot running...');
})();
```

### Flow 3: Event-Driven Bot (Python)

Listen for mentions and react automatically:

```python
#!/usr/bin/env python3
"""slack-event-bot.py — Listen for mentions and auto-respond."""
import os
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

bot_token = os.environ["SLACK_BOT_TOKEN"]
app_token = os.environ["SLACK_APP_TOKEN"]

client = WebClient(token=bot_token)
socket_client = SocketModeClient(
    app_token=app_token,
    web_client=client,
)

def handle_event(client: SocketModeClient, req: SocketModeRequest):
    if req.type != "events_api":
        return
    event = req.payload.get("event", {})

    # Respond to mentions
    if event.get("type") == "app_mention":
        channel = event["channel"]
        user = event["user"]
        text = event.get("text", "")

        if "help" in text.lower():
            response = ("Hi there! :wave: I can help with:\n"
                        "• `/standup` — log your daily standup\n"
                        "• `/deploy` — trigger a deployment\n"
                        "• `@bot status` — check system health")
        elif "status" in text.lower():
            response = "All systems operational :green_heart:"
        else:
            response = f"Hey <@{user}>! Not sure how to help with that. Try `@bot help`."

        client.web_client.chat_postMessage(channel=channel, text=response)

    # React to specific message keywords in monitored channels
    elif event.get("type") == "message" and "bug" in event.get("text", "").lower():
        channel = event["channel"]
        ts = event["ts"]
        client.web_client.reactions_add(channel=channel, name="bug", timestamp=ts)
        client.web_client.chat_postMessage(
            channel=channel,
            text=":warning: This sounds like a bug. <!here>",
            thread_ts=ts,
        )

socket_client.socket_mode_request_listeners.append(handle_event)
print("Event bot listening...")
socket_client.connect()

import threading
from time import sleep
try:
    while True: sleep(1)
except KeyboardInterrupt:
    socket_client.disconnect()
```

### Flow 4: Multi-Channel Notification Pipeline (CI/CD → Slack + other channels)

Route notifications to different channels based on severity:

```bash
#!/usr/bin/env bash
# pipeline-notify.sh — Route notifications to correct channels
set -euo pipefail

WEBHOOK_URL="${SLACK_WEBHOOK_URL}"
SEVERITY="${1:-info}"
SUBJECT="${2:-Notification}"
BODY="${3:-}"

notify_slack() {
  local color="$1" channel="$2" text="$3"
  curl -s -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" \
    -d "{\"channel\":\"$channel\",\"attachments\":[{\"color\":\"$color\",\"text\":\"$text\"}]}"
}

case "$SEVERITY" in
  info)
    notify_slack "#36a64f" "#deployments" "*$SUBJECT*\n$BODY"
    ;;
  warning)
    notify_slack "#ffcc00" "#ops-alerts" ":warning: *$SUBJECT*\n$BODY"
    ;;
  error)
    notify_slack "#ff0000" "#incidents" ":red_circle: *$SUBJECT*\n$BODY"
    # Also page on-call
    curl -s -X POST "$PAGERDUTY_WEBHOOK" -H "Content-Type: application/json" \
      -d "{\"routing_key\":\"$PD_KEY\",\"event_action\":\"trigger\",\"payload\":{\"summary\":\"$SUBJECT\",\"severity\":\"critical\"}}"
    ;;
  critical)
    notify_slack "#cc0000" "#incidents" ":sos: *CRITICAL: $SUBJECT*\n$BODY"
    notify_slack "#cc0000" "@here" ":sos: Team, please check the #incidents channel."
    ;;
esac
```

### Flow 5: Interactive Workflow — Approval Buttons

Handle button clicks from slash commands:

```python
#!/usr/bin/env python3
"""approval-bot.py — Handle interactive approval workflows."""
import os, json
from flask import Flask, request
from slack_sdk import WebClient

app = Flask(__name__)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

@app.route("/slack/actions", methods=["POST"])
def handle_actions():
    payload = json.loads(request.form["payload"])
    action = payload["actions"][0]
    value = action["value"]
    user = payload["user"]["id"]
    channel = payload["channel"]["id"]
    msg_ts = payload["container"]["message_ts"]

    action_type, *args = value.split(":")

    if action_type == "approve":
        version, env = args
        client.chat_update(
            channel=channel,
            ts=msg_ts,
            text=f":rocket: *Deploy Approved* by <@{user}>\nVersion: {version} | Environment: {env}",
            blocks=None,
        )
        # Trigger actual deploy
        trigger_deploy(version, env)
        client.chat_postMessage(
            channel="#deployments",
            text=f"Deploying {version} to {env} (approved by <@{user}>)",
        )

    elif action_type == "cancel":
        client.chat_update(
            channel=channel,
            ts=msg_ts,
            text=f":no_entry: Deploy *cancelled* by <@{user}>",
            blocks=None,
        )

    return "", 200

def trigger_deploy(version, env):
    """Placeholder: trigger the actual deployment."""
    import subprocess
    subprocess.Popen(["/deploy.sh", version, env])

if __name__ == "__main__":
    app.run(port=3000)
```

### Flow 6: Channel Monitor & Digest

Monitor multiple channels and send a daily digest:

```python
#!/usr/bin/env python3
"""digest-bot.py — Collect channel activity and send daily digest."""
import os, datetime
from slack_sdk import WebClient

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def get_daily_digest(channels):
    """Get messages from today in given channels."""
    today = datetime.date.today().isoformat()
    midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0).timestamp()

    digest = []
    for channel in channels:
        result = client.conversations_history(
            channel=channel,
            oldest=str(midnight),
            limit=50,
        )
        messages = result.get("messages", [])
        if messages:
            digest.append(f"\n*<#{channel}>* — {len(messages)} messages")
            for msg in messages[:5]:  # top 5
                user = msg.get("user", "?")
                text = msg.get("text", "")[:200]
                digest.append(f"  • <@{user}>: {text}")

    return "\n".join(digest)

# Example: Daily standup summary
channels_to_watch = ["#team-engineering", "#design", "#product"]
digest = get_daily_digest(channels_to_watch)

client.chat_postMessage(
    channel="#standup-logs",
    text=f"*Daily Digest — {datetime.date.today()}*\n{digest}",
)
```

## First Action in 60 Minutes

```
00:00-05:00 — Go to https://api.slack.com/apps → Create New App → From Manifest
05:00-10:00 — Add scopes: chat:write, commands, channels:history, users:read
10:00-12:00 — Install app to workspace, store BOT_TOKEN and SIGNING_SECRET
12:00-15:00 — Create an incoming webhook URL from the same app
15:00-20:00 — Test webhook: curl -X POST $WEBHOOK_URL -d '{"text":"Hello"}'
20:00-30:00 — Set up Bolt.js or Flask app skeleton with /hello command
30:00-35:00 — Register /hello slash command in Slack App settings → Slash Commands
35:00-45:00 — Run the bot (ngrok + socket mode), test /hello from Slack
45:00-50:00 — Build and test a rich notification (CI/CD deploy message)
50:00-55:00 — Add a simple event listener for mentions
55:00-60:00 — Wire up approval buttons and test end-to-end
```

**By the end of 60 minutes:**
- Slack app created and installed
- Incoming webhook tested
- Slash command handler running (socket mode)
- Rich notification formatting working
- Event listener for mentions operational
- Interactive approval workflow functional
- Reusable bot architecture to sell as a communication automation product

## Anti-Rationalization Table

| Rationalization | Reality |
|---------------|---------|
| "I'll just post plain text messages" | Rich blocks (headers, sections, buttons, images) increase engagement 3x. Always use blocks. |
| "Socket mode is optional" | Socket mode avoids hosting a public HTTPS endpoint. Use it for development and small deployments. |
| "I only need one webhook" | Different channels need different webhooks. Create one per channel + per use case. |
| "Ephemeral messages are unnecessary" | Ephemeral messages keep noise down. Use them for confirmations and errors. |
| "Slash commands are just `/do thing`" | Add modal dialogs, button chains, and multi-step workflows. Users expect interactive UIs. |
| "Rate limits won't hit me" | Slack enforces tier-based rate limits (1-20+ messages/second). Plan retry/backoff from day one. |

## Output Format

```
slack-automation/
├── bot/
│   ├── app.py              # Socket mode bot (Python)
│   └── app.js              # Socket mode bot (Bolt.js)
├── notifier/
│   ├── slack-notify.sh     # Bash webhook sender
│   └── python-notify.py    # Python block message builder
├── commands/
│   ├── standup.js          # /standup command handler
│   └── deploy.js           # /deploy with approval buttons
├── webhook-server/
│   └── app.py              # Flask interactive endpoint
├── pipeline-notify.sh      # Multi-channel routing script
└── digest-bot.py           # Daily digest automation
```

## Verification

- [ ] Webhook sends messages to correct channel with proper formatting
- [ ] Bot token can post to public channels and DMs
- [ ] Slash command handler responds within 3 seconds (Slack timeout)
- [ ] Interactive components (buttons, modals) trigger correct action handlers
- [ ] Socket mode connects without HTTPS endpoint
- [ ] Rich blocks render correctly (headers, sections, images, context)
- [ ] Event listeners fire on app_mention and message patterns
- [ ] Rate limits: scripts quit gracefully on 429 with Retry-After
- [ ] Approval workflow: approve → deploy trigger, cancel → clean abort
- [ ] Multi-channel routing sends correct content per severity
- [ ] Daily digest correctly aggregates channel activity
- [ ] Auth: invalid tokens return descriptive errors, not crashes
- [ ] Money protocol: deliverable is packaged and billable


## When to Use
Use this skill when working with slack.


## Workflow
See the parent skill for authoritative workflow documentation.
