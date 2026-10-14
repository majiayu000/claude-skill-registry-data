---
name: apple-contacts
description: Search and read Apple Contacts (macOS). Use when the user wants to find a contact, look up a phone number, or get someone's email.
---

# Apple Contacts (GenosOS)

Search and read contacts via the dedicated `contacts` tool. Secure — no exec or osascript exposed.

## Actions

```
contacts({ action: 'search', query: 'Juan' })     → find by name, email, or phone
contacts({ action: 'list', count: 20 })            → list recent contacts
contacts({ action: 'get', index: 1 })               → full details of a contact
```

## Notes

- macOS only — reads from Apple Contacts app
- First run may trigger macOS permission prompt
- Search matches name, email, and phone fields
