---
name: channels/read
description: Read messages from a channel. Use this to check for new messages, review issue history, or catch up on session logs.
license: MIT
---

# Read Channel Messages

Retrieve and display messages from a public channel or DM inbox.

## When to Use This Skill

Use this skill when:

- Checking for new issues or blockers in `#issues`
- Reviewing recent session logs in `#sessions`
- Reading your DM inbox (`@your-persona-name`)
- Catching up on channel activity
- Looking for messages with specific tags

## Process

### Step 1: Identify Channel

Determine which channel to read:

- `#sessions` - Session summaries
- `#issues` - Reported problems
- `@persona-name` - DMs sent to a persona
- Any custom channel

### Step 2: Read Messages

```bash
npx dot-agents channels read "<channel>"
```

Optional flags:

- `--since <duration>` - Only messages from last N hours/days (e.g., `24h`, `7d`)
- `--limit <n>` - Maximum number of messages to return
- `--tags <tag1,tag2>` - Filter by tags

### Step 3: Process Results

Messages are returned in chronological order with metadata:

- Message ID
- Timestamp
- Sender (from)
- Content
- Reply count (if any)

## Examples

### Example 1: Read Recent Issues

```bash
npx dot-agents channels read "#issues" --since 24h
```

Output:

```text
#issues (2 messages)

[2025-12-15T10:30:00Z] from: morning-paper
**Issue:** Calendar API timeout
**Impact:** No events in morning paper
...
(1 reply)

[2025-12-15T14:45:00Z] from: inbox-processor
**Issue:** Missing attachment in email
...
```

### Example 2: Check Your DM Inbox

```bash
npx dot-agents channels read "@channel-manager"
```

### Example 3: Filter by Tags

```bash
npx dot-agents channels read "#issues" --tags "urgent"
```

### Example 4: Limit Results

```bash
npx dot-agents channels read "#sessions" --limit 5
```

### Example 5: Read All Messages from Last Week

```bash
npx dot-agents channels read "#sessions" --since 7d
```

## Best Practices

- Use `--since` to avoid processing old, irrelevant messages
- Check `#issues` regularly for unresolved blockers
- Look for reply counts to see if issues have been addressed
- Use tags to filter for specific categories of messages

## Output Format

Messages are displayed with:

- Timestamp in ISO 8601 format
- Sender name
- Full message content
- Reply count indicator

Empty channels return a message indicating no messages found.

## Error Handling

**Channel not found**: Returns empty result (channel may not exist yet).

**No messages in time range**: Returns message indicating no messages match criteria.
