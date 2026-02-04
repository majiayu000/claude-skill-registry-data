---
name: thymer-capture
description: Capture notes, logs, and journal entries to Thymer. Use when user says "note this", "log this", "capture this", "add to journal", "inbox this", "save this conversation", or wants to save content to their Thymer workspace.
---

# Thymer Capture

Capture content to Thymer using the `tm` CLI.

Important:
- Use just `tm` (it's in PATH at ~/.local/bin) - do NOT use full paths
- The `tm serve` daemon runs as a systemd service - do NOT try to start it

## Three Patterns

### 1. Quick one-liner (→ Journal)
For brief thoughts and quick captures:
```bash
echo "Quick thought to remember" | tm
```

### 2. Timestamped lifelog entry (→ Journal with HH:MM prefix)
For activities, meetings, events - adds bold timestamp:
```bash
echo "Met with Alice about roadmap" | tm --timestamp
```

### 3. Markdown document (→ Inbox as new note)
For longer content with structure. Title extracted from first `# heading`:
```bash
tm << 'EOF'
# Meeting Notes

## Attendees
- Alice, Bob, Charlie

## Discussion
- Discussed feature X
- Decided on approach Y

## Action Items
- [ ] Alice to draft spec
- [ ] Bob to review by Friday
EOF
```

## When to Use Each Pattern

| Pattern | Use Case | Destination |
|---------|----------|-------------|
| One-liner | Brief thoughts, quick captures | Journal (today) |
| Timestamped | Activities, meetings, events | Journal with **HH:MM** prefix |
| Markdown doc | Structured notes, summaries, meeting notes | Inbox collection |

## Targeting Specific Collections

Override auto-routing with `--collection`:
```bash
echo "Buy groceries" | tm --collection Tasks
echo "Review PR #123" | tm --collection GitHub
```

## Examples

### Log a completed activity
```bash
echo "Finished code review for authentication PR" | tm --timestamp
```

### Capture a conversation summary
```bash
tm << 'EOF'
# Claude Session: MCP Implementation

## Summary
Designed the MCP server architecture for Thymer integration.

## Key Decisions
- Use SSE + callback pattern for bidirectional communication
- One-time UUID-based callback URLs for security
- Convert Thymer's structured format to markdown for responses

## Next Steps
- Ask Thymer team about search API
- Implement server-side pending request handling
EOF
```

### Quick task capture
```bash
echo "Follow up with Thymer team about search API" | tm --collection Tasks
```

## Notes

- Content is pushed to Thymer via SSE - requires `tm serve` running
- The browser plugin routes content based on format and collection flag
- One-liners and short notes (2-5 lines) go to Journal
- Markdown with `# heading` creates new notes in Inbox
