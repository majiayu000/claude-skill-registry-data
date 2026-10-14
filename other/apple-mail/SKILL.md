---
name: apple-mail
description: Read and send emails via Apple Mail (macOS). Use when the user wants to check emails, read messages, send emails, reply, or search inbox. Uses the dedicated mail tool — no exec needed.
---

# Apple Mail (GenosOS)

Read and send emails via the dedicated `mail` tool. Secure — the agent declares intent, the server builds the AppleScript internally.

## Actions

### List recent emails

```
mail({ action: 'list', count: 10 })
```

Returns: sender, subject, date for the N most recent messages in inbox.

### Read an email

```
mail({ action: 'read', index: 1 })
```

Returns: full content of the message at position N (1 = most recent).

### Search emails

```
mail({ action: 'search', query: 'factura' })
```

Returns: messages matching the search term in subject or sender.

### Send an email

```
mail({ action: 'send', to: 'user@example.com', subject: 'Hello', body: 'Message text' })
```

### Reply to an email

```
mail({ action: 'reply', index: 1, body: 'Thanks for your message' })
```

## Notes

- macOS only — requires Apple Mail configured with at least one account
- First run may trigger macOS permission prompt for automation
- The agent never writes AppleScript directly — the server builds it securely
- No exec needed — the mail tool handles everything
