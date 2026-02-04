---
name: jmap-email
description: Enables JMAP email operations using Node.js and jmap-jam library. Use when working with JMAP email servers, FastMail, Cyrus IMAP, Stalwart Mail Server, or when user mentions email search, reading, sending, or mailbox management.
---

# JMAP Email Access

Access JMAP email servers (FastMail, Cyrus IMAP, Stalwart) using pre-built scripts.

## Prerequisites

Environment variables must be set before launching Claude Code:
- `JMAP_SESSION_URL` - JMAP server session URL
- `JMAP_BEARER_TOKEN` - Authentication bearer token
- `JMAP_ACCOUNT_ID` - Account ID (optional, auto-detected)

## Available Scripts

**Choose the right script:**
- **Browse recent emails?** → Use `list-emails.ts` (supports --unread, --flagged, --mailbox, --from, --limit filters)
- **Search by sender?** → Use `list-emails.ts --from "sender@example.com"`
- **Search for multiple keywords?** → Use `search-keywords.ts keyword1 keyword2 ...`
- **Get full email content?** → Use `get-email.ts` with email ID
- **View folder structure?** → Use `list-mailboxes.ts`
- **Move emails by ID?** → Use `move-by-ids.ts --mailbox <name> <id1> <id2> ...`
- **Delete emails?** → Use `delete-emails.ts <id1> <id2> ...`

All scripts support `--help` for detailed usage.

## Common Tasks

### Browse unread emails
```bash
node scripts/list-emails.ts --unread
node scripts/list-emails.ts --unread --limit 50
```

### Find emails from specific sender
```bash
node scripts/list-emails.ts --from "sender@example.com"
node scripts/list-emails.ts --from "sender@example.com" --unread
```

### Search for receipts or specific content
```bash
node scripts/search-keywords.ts "invoice" "receipt" "order confirmation"
node scripts/search-keywords.ts --mailbox "Archive" --limit 10 "meeting" "agenda"
```
Note: Search shows previews only. For full email content, use `get-email.ts` with the email ID.

### Get full email content
```bash
node scripts/get-email.ts <email-id>
```

### Organize emails (classification workflow)
1. Search for candidates: `search-keywords.ts "keyword1" "keyword2"`
2. Review previews and identify relevant email IDs
3. (Optional) View full content: `get-email.ts <email-id>`
4. Move to target mailbox: `move-by-ids.ts --mailbox @MailboxName id1 id2 id3`

### Interactive email triage
**Workflow for processing new emails with learning:**

1. **Fetch recent emails:**
   - Use `list-emails.ts --limit 20` to get batch (optionally add `--unread` or `--mailbox "Inbox"`)
   - Review subject, sender, and preview

2. **Present classification options:**
   - Use AskUserQuestion with multiSelect for each email
   - Options should be target mailboxes (Inbox, Archive, @Reference, etc.)
   - Allow user to select destination for each email

3. **Execute moves:**
   - Group emails by target mailbox
   - Use `move-by-ids.ts --mailbox <name> <id1> <id2> ...` for each group

4. **Save routing patterns to memory:**
   - Note sender domains and subjects that map to specific mailboxes
   - Record user's classification decisions (e.g., "newsletters from X → Archive")
   - Reference these patterns in future triage sessions
   - Suggest automatic routing rules based on observed patterns

**Benefits:**
- Process inbox in batches with interactive guidance
- Build up routing knowledge over time
- Suggest classifications based on past decisions
- Gradually automate common routing patterns

### View mailbox structure
```bash
node scripts/list-mailboxes.ts
```

## Output Format

Scripts output compact, human-readable results:
```
Found 5 email(s) (unread)
================================================================================

⭐ [UNREAD] Meeting tomorrow
From: John Doe <john@example.com>
Date: 1/15/2024, 10:30:45 AM
ID: StrgucNsyw-3
Preview: Hi Jane, let's meet at 2pm to discuss the project...
--------------------------------------------------------------------------------
```

## Advanced Usage

For writing custom JMAP operations or understanding the API, see:
- **Code Examples**: [examples.md](examples.md)
- **API Reference**: [reference.md](reference.md)
- **Development Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)
