---
name: citations
description: Proactively include clickable links when referencing entities (persons, conversations, messages). Makes responses actionable.
---

# Citations Skill

## Purpose

When arsenal references persons, conversations, or messages, include clickable links so users can quickly navigate to the relevant data.

## Base URL

`https://admin.prod.cncorp.io`

## URL Patterns

| Entity | Pattern | Example |
|--------|---------|---------|
| Person | `/persons/{person_id}` | `/persons/123` |
| Conversation | `/conversations/{conversation_id}` | `/conversations/456` |
| Conversation Messages | `/conversations/{conversation_id}/messages` | `/conversations/456/messages` |
| Messages (time-filtered) | `/conversations/{id}/messages?start={iso}&end={iso}` | `?start=2025-01-01T00:00:00Z&end=2025-01-02T00:00:00Z` |
| Jump to Message | `/conversations/{id}/messages?messageId={message_id}` | `?messageId=789` |

## Query Parameters (Messages)

- `start` - ISO-8601 datetime, filter messages after this time
- `end` - ISO-8601 datetime, filter messages before this time
- `messageId` - Jump to specific message (auto-sets ±1 day window)

## When to Cite

**ALWAYS include citations when:**
- Mentioning a person by ID or name (if ID is known)
- Referencing a conversation
- Discussing specific messages or timeframes
- Returning data from sql-reader that includes these entities
- Debugging or investigating user issues

**Citation is MANDATORY, not optional.** If you know an entity ID, link it.

## Citation Format

**Inline (preferred for single entities):**
```
Person John Smith ([view](https://admin.prod.cncorp.io/persons/123)) has 3 active conversations.
```

**Standalone (for navigation):**
```
[View conversation in Admin](https://admin.prod.cncorp.io/conversations/456)
```

**Timeframe debugging:**
```
[View messages from 2-3 PM](https://admin.prod.cncorp.io/conversations/456/messages?start=2025-01-15T14:00:00Z&end=2025-01-15T15:00:00Z)
```

**Jump to specific message:**
```
The problematic message ([view](https://admin.prod.cncorp.io/conversations/456/messages?messageId=789)) was sent at 2:34 PM.
```

## Examples

### SQL Query Result
When sql-reader returns:
```
person_id: 123, name: "John Smith", conversation_id: 456
```

Response should include:
```
Found John Smith ([view](https://admin.prod.cncorp.io/persons/123)) in conversation ([view](https://admin.prod.cncorp.io/conversations/456)).
```

### Debugging a User Issue
```
The user reported missing messages around 3 PM yesterday.

[View messages from 2-4 PM](https://admin.prod.cncorp.io/conversations/456/messages?start=2025-01-15T14:00:00Z&end=2025-01-15T16:00:00Z)

I found the issue in message ID 789 ([view](https://admin.prod.cncorp.io/conversations/456/messages?messageId=789)).
```

### Langfuse Trace Investigation
When referencing a conversation from a trace:
```
Trace abc123 processed conversation 456 ([view](https://admin.prod.cncorp.io/conversations/456/messages)).
```
