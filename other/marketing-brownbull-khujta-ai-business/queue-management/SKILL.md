---
name: queue-management
description: Manage the content processing queue for batch content consumption. Use when user mentions queue, batch later, save for later, process queue, or wants to add multiple items for later analysis.
---

# Queue Management

Manage a queue of content URLs for later batch processing. Add items throughout the day, process them all at once when ready.

## When to Use

Activate this skill when the user:
- Mentions "queue", "batch later", "save for later"
- Wants to add something to process later
- Asks "what's in my queue" or "show queue"
- Says "process my queue" or "analyze everything"
- Wants to manage pending content items

## Queue Location

The queue is stored in `inbox/queue.txt`:

```
# Format: URL | type | added_timestamp
https://youtube.com/watch?v=abc123 | youtube | 2024-01-15T10:30:00
https://arxiv.org/abs/2401.12345 | arxiv | 2024-01-15T11:00:00
```

## Operations

### Adding to Queue

1. Parse the URL
2. Auto-detect content type:
   - youtube.com, youtu.be → `youtube`
   - arxiv.org → `arxiv`
   - Otherwise → `article`
3. Read existing queue (create if missing)
4. Check for duplicates
5. Append with current timestamp
6. Confirm to user

### Listing Queue

1. Read `inbox/queue.txt`
2. Display formatted list with:
   - Item number
   - Content type badge
   - URL or title
   - Time since added

### Processing Queue

1. Read all pending items
2. Process each using appropriate command:
   - youtube → `/yt`
   - arxiv → `/arxiv`
   - article → `/read`
3. Remove successful items from queue
4. Keep failed items for retry
5. Show summary

### Clearing Queue

1. Confirm before clearing
2. Create backup at `inbox/queue.txt.bak`
3. Empty the file
4. Confirm removal

## Example Interactions

**User**: "Add this to my queue: https://youtube.com/watch?v=abc123"
**Action**: Add to queue, confirm

**User**: "What's in my queue?"
**Action**: List all pending items

**User**: "Process my reading queue"
**Action**: Process all items, show results

**User**: "Save this for later: [URL]"
**Action**: Add to queue

## Error Handling

- Invalid URL: Warn, don't add
- Duplicate: Skip, inform user
- Process failure: Keep in queue, continue
- Empty queue: Inform, no action

## Related

- Slash command: `/queue`
- Queue file: `inbox/queue.txt`
- Uses: `/yt`, `/read`, `/arxiv` commands
