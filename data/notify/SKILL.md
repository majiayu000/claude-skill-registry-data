---
name: notify
description: Send push notifications to Lucas's phone via ntfy.sh. Use for system alerts, urgent notifications, critical errors, or anything that needs to reach Lucas even when away from PC.
---

# Push Notifications via ntfy.sh

Send real system-level push notifications to Lucas's Android phone. These show up in the notification shade even when the phone is locked, and can bypass Do Not Disturb.

## When to Use

- **System alerts**: Gateway down, service crashed, disk full, security issue
- **Urgent updates**: Something needs Lucas's attention NOW
- **Task completion**: Long-running job finished, build done
- **Away-from-PC**: When Lucas isn't at the computer and Telegram might be missed

## When NOT to Use

- Routine messages — use Telegram instead
- Status updates that can wait — use Telegram
- Anything that needs a conversation — use Telegram
- Never send passwords, tokens, or sensitive data via ntfy (public server)

## Topics

| Route          | Topic                        |
|----------------|------------------------------|
| Cleber → Lucas | `cleber-lucas-2f2ea57a`      |
| Romário → Lucas| `romario-lucas-I9rbtKUd`     |

## Send a Notification

```bash
curl -s \
  -H "Title: Your Title" \
  -H "Priority: default" \
  -H "Tags: robot" \
  -d "Your message body" \
  ntfy.sh/cleber-lucas-2f2ea57a
```

## Priority Levels

| Level     | Behavior                              |
|-----------|---------------------------------------|
| `min`     | No sound, no vibration               |
| `low`     | No sound                             |
| `default` | Normal notification                  |
| `high`    | Prominent notification               |
| `urgent`  | **Bypasses Do Not Disturb**          |

Use `urgent` sparingly — only for things that truly can't wait.

## Advanced Features

```bash
# With click action (opens URL when tapped)
curl -H "Title: PR Merged" -H "Click: https://github.com/..." -d "Your PR was merged" ntfy.sh/TOPIC

# With emoji tags
curl -H "Tags: warning,skull" -d "Disk is 95% full" ntfy.sh/TOPIC

# With action buttons
curl -H "Actions: view, Open Dashboard, https://dashboard.example.com" -d "Alert" ntfy.sh/TOPIC
```

## Rules

- **Telegram first, ntfy for critical.** Don't spam notifications.
- **Include context.** "Gateway crashed" not just "Error".
- **Use appropriate priority.** Most things are `default` or `high`. Reserve `urgent` for emergencies.
- **Keep it brief.** Phone notifications are small — lead with the key info.
- **Never send secrets.** ntfy.sh is a public server. No tokens, passwords, or private data.
