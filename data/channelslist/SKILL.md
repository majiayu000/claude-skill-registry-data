---
name: channels/list
description: List all available channels. Use when discovering what channels exist or checking channel metadata.
license: MIT
---

# List Channels

List all channels to discover available communication streams.

## When to Use This Skill

Use this skill when you need to:

- Discover what channels exist
- Check channel metadata (creator, creation date)
- Find the right channel to publish to
- Get an overview of communication streams

## Process

### Step 1: List All Channels

```bash
npx dot-agents channels list
```

### Step 2: Review Output

The output shows all channels with their metadata:

```text
Channels (4):

  #status
    Progress updates and milestone notifications
    created by system at 2025-12-10T08:00:00.000Z

  #issues
    Problems, blockers, and errors
    created by system at 2025-12-10T08:00:00.000Z

  @developer
    created by human:tnez at 2025-12-12T09:00:00.000Z
```

## Examples

### Example 1: Check Available Channels

```bash
npx dot-agents channels list
```

### Example 2: Filter Public Channels

```bash
npx dot-agents channels list | grep "^  #"
```

### Example 3: Filter DM Channels

```bash
npx dot-agents channels list | grep "^  @"
```

## Channel Types

- `#channel-name` - Public channels for topic-based communication
- `@persona-name` - Direct message inboxes for personas

## Notes

- Channels are created automatically when first message is published
- Empty result means no channels have been created yet
- Use this before publishing to discover the right channel
