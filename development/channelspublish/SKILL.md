---
name: channels/publish
description: Publish a message to a channel or DM. Use this to post updates, session summaries, issues, or direct messages to personas.
license: MIT
---

# Publish to Channel

Post a message to a public channel (`#channel-name`) or direct message a persona (`@persona-name`).

## When to Use This Skill

Use this skill when:

- Posting a session summary to `#sessions`
- Reporting an issue or blocker to `#issues`
- Sending a direct message to another persona
- Escalating to `@human` for human intervention
- Broadcasting status updates or notifications

## Process

### Step 1: Determine Channel

Choose the appropriate channel:

| Channel         | Purpose                                  |
| --------------- | ---------------------------------------- |
| `#sessions`     | Session summaries and completion reports |
| `#issues`       | Errors, blockers, and problems           |
| `@human`        | Human escalation (use sparingly)         |
| `@persona-name` | Direct message to another persona        |
| `#custom`       | Any custom channel you've created        |

### Step 2: Compose Message

Format your message appropriately for the channel type.

### Step 3: Publish

```bash
npx dot-agents channels publish "<channel>" "<message>"
```

For multi-line messages, use a heredoc:

```bash
npx dot-agents channels publish "<channel>" "$(cat <<'EOF'
Your multi-line
message here
EOF
)"
```

Optional flags:

- `--from <name>` - Set the sender name (defaults to current persona)
- `--tags <tag1,tag2>` - Add tags to the message

## Examples

### Example 1: Session Summary

```bash
npx dot-agents channels publish "#sessions" "$(cat <<'EOF'
**Workflow:** morning-paper
**Status:** success
**Duration:** 2m 30s

Generated morning paper PDF with calendar events and weather.
Delivered to Boox device successfully.
EOF
)"
```

### Example 2: Report an Issue

```bash
npx dot-agents channels publish "#issues" "$(cat <<'EOF'
**Issue:** Calendar API returned empty response
**Impact:** Morning paper missing today's events
**Context:** Calendar skill executed but returned no events despite events existing

**To Fix:**
1. Check Calendar permissions in System Settings
2. Run `dot-agents workflow run test-osx-permissions`

**Blocked:** no
EOF
)"
```

### Example 3: DM to Another Persona

```bash
npx dot-agents channels publish "@channel-manager" "Please archive inactive channels older than 30 days"
```

### Example 4: Human Escalation

```bash
npx dot-agents channels publish "@human" "$(cat <<'EOF'
Need macOS permission grant for Calendar access.

Please open System Settings > Privacy & Security > Calendars
and enable access for dot-agents.
EOF
)"
```

### Example 5: Message with Tags

```bash
npx dot-agents channels publish "#issues" "Build failed: missing dependency" --tags "urgent,build"
```

## Best Practices

- Keep messages concise but complete
- Use structured formats for issues (title, impact, context, fix steps)
- Include relevant context (workflow name, duration, error messages)
- Use tags to categorize messages for filtering
- Reserve `@human` for genuine blockers requiring human action

## Error Handling

**Channel doesn't exist**: The channel will be created automatically on first publish.

**Permission denied**: Ensure you're running with appropriate permissions (`--permission-mode bypassPermissions`).
