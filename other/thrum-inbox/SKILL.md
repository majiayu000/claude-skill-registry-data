---
name: thrum-inbox
description: Check message inbox
# source: claude-plugin/commands/inbox.md
---

# Thrum Inbox

Use this skill when the user explicitly wants the `inbox` Thrum workflow. Prefer
the umbrella `thrum` skill when the request spans multiple commands or needs
broader coordination judgment.

List messages in your inbox. `thrum inbox` shows messages; `thrum message read`
marks them read.

```bash
thrum inbox                  # All recent messages
thrum inbox --unread         # Unread only
thrum inbox --json           # Machine-readable
thrum sent --unread          # Check sent items with unread recipients
thrum message read --all --force  # Mark ALL unread as read (run `read --all` alone first — dry run)
```

**Search — do not page through it.** The default page is 10, newest-first, so
stale unread sorts LAST exactly when it has been waiting longest.

```bash
thrum message search "<term>"      # Pro: full-text across all messages
thrum inbox -q "<term>"            # Pro: same full-text search, scoped to your inbox
thrum inbox --unread --from @<sender>  # Free: narrow without full-text search
thrum message reindex              # rebuild the FTS index if search looks wrong
```
