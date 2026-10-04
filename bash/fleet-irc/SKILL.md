---
name: fleet-irc
description: >
  Post structured messages to fleet IRC channels. Use for task events,
  PR notifications, alerts, and status updates. Messages are short,
  formatted, and include clickable URLs. The human reads IRC as their
  primary real-time fleet interface.
  Triggers on: "notify irc", "fleet irc", "post to irc", "alert irc".
user-invocable: true
---

# Fleet IRC Messaging

Post structured messages to IRC. **IRC is the human's real-time window into the fleet.**

## Message Format Reference

See `agents/_template/markdown/irc-events.md` for all standard formats.

## Channels

| Channel | Purpose | What goes here |
|---------|---------|---------------|
| #fleet | General fleet activity | Task events, PR events, status, agent messages |
| #alerts | Urgent/important only | Security alerts, critical blockers, system failures |
| #reviews | PR review queue | PR ready, QA results, review results, merge events |

## How to Send

Use the `scripts/notify-irc.sh` script:

```bash
# Structured event
bash scripts/notify-irc.sh --agent "{agent_name}" --event "PR READY" --title "{title}" --url "{pr_url}"

# Plain message
bash scripts/notify-irc.sh "message text"
```

Or call the fleet notify script from within your shell execution.

## When to Post

| Event | Channel | Format |
|-------|---------|--------|
| Task accepted | #fleet | `[{agent}] ▶️ STARTED: {title} — {task_url}` |
| Task blocked | #fleet | `[{agent}] 🚫 BLOCKED: {title} — {reason} — {task_url}` |
| PR ready | #fleet + #reviews | `[{agent}] ✅ PR READY: {title} — {pr_url}` |
| Security alert | #alerts | `🔴 [{agent}] CRITICAL: {title} — {url}` |
| Quality concern | #fleet | `🟡 [{agent}] MEDIUM: {title} — {url}` |
| Suggestion | #fleet | `💡 [{agent}] SUGGESTION: {title}` |
| Gap detected | #fleet | `💡 [{agent}] GAP: {description}` |

## Rules

- **EVERY** IRC message MUST include a URL when one exists
- **KEEP IT SHORT** — one line per message, details are in MC/GitHub
- **USE EMOJI** — for scannability (see format reference)
- Alerts go to **#alerts**, not #fleet (they have notifications on)
- PR events go to **#reviews** AND #fleet
- Don't spam — one message per event, not multiple