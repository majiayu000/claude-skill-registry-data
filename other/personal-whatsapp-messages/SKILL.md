---
name: personal-whatsapp-messages
description: Query WhatsApp messages from the local SQLite database. Use this skill when asked to search messages, find conversations, look up chat history, check message statistics, list contacts/groups, or retrieve media messages. Triggers on queries about "whatsapp messages", "search messages", "message history", "conversation with", "chat history", "who said", "find message", or any WhatsApp data retrieval task.
---

# WhatsApp Messages Query Skill

Query WhatsApp messages stored in the local SQLite database (`data/messages.db`).

## Quick Start

1. **First, check database health** before querying:
   ```bash
   sqlite3 data/messages.db "PRAGMA integrity_check;" 2>&1 | head -1
   ```
   - If output is `ok` → proceed with MCP tools
   - If output shows errors → see [Database Recovery](#database-recovery) section

2. **Discover available tools**:
   ```
   discover_tools({ mode: "browse", category: "whatsapp" })
   ```

3. **Query messages** using the appropriate tool

## Available Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `whatsapp_search_messages` | Full-text search with filters | "What did X say about Y?" |
| `whatsapp_get_recent` | Latest messages | "Show recent messages" |
| `whatsapp_get_conversation` | Chat history with a contact | "Find my chat with X" |
| `whatsapp_get_group_messages` | Messages from a group | "Messages from group X" |
| `whatsapp_get_stats` | Database statistics | "How many messages?" |
| `whatsapp_list_contacts` | All unique contacts | "Who have I chatted with?" |
| `whatsapp_list_groups` | Groups with names | "List all groups" |
| `whatsapp_get_media` | Media messages | "Show voice messages" |

## Query Patterns

### Search Messages

```javascript
whatsapp_search_messages({
  text: "meeting",           // Full-text search
  phone: "972501234567",     // Filter by contact
  direction: "incoming",     // incoming | outgoing
  isGroup: true,             // Group messages only
  fromDate: "2024-01-01",    // ISO date range
  toDate: "2024-12-31",
  limit: 50
})
```

### Conversation History

```javascript
whatsapp_get_conversation({
  phone: "972501234567",
  limit: 100
})
```

Returns messages in **chronological order** (oldest first).

### Group Messages

```javascript
whatsapp_get_group_messages({
  groupId: "Orient Team"   // Can use group name or JID
})
```

### Media Messages

```javascript
whatsapp_get_media({
  mediaType: "audio",        // image | audio | video | document
  groupId: "...",            // Optional: filter by group
  limit: 50
})
```

## Known Contacts

**IMPORTANT**: When the user mentions these names, always use the corresponding phone number.

| Name | Aliases | Phone | Relationship | Context |
|------|---------|-------|--------------|---------|
| מורי | מור, Mor, Mori | `972524670511` | Wife/Partner | Primary family contact. Messages about kids (שי, נדב, אדר/דרי), pickups, scheduling |

### Family Members Mentioned in Messages

| Name | Aliases | Notes |
|------|---------|-------|
| שי | Shai | Eldest daughter, has activities/חוגים |
| נדב | Nadav, נדבי | Son |
| אדר | דרי, Adar, Dri | Youngest child |

### Key Groups

| Group Name | Group ID | Purpose |
|------------|----------|---------|
| תומור | `972508250700-1443686078@g.us` | Family group (Tom + Mor) |
| בוט שלי | `120363422821405641@g.us` | Bot testing |
| Genoox mobile | `972544334507-1424335267@g.us` | Work group |
| האחים | `972543259093-1510303965@g.us` | Siblings group |
| משפחת בן שמחון משתדרגת | `972508250730-1326877332@g.us` | Extended family |

## Time-Based Queries

When users ask about "this week", "next week", or upcoming events:

### Finding Upcoming Events

Search for Hebrew day names and time references:

```bash
sqlite3 data/messages.db "
SELECT timestamp, direction, text
FROM messages 
WHERE phone = '972524670511'
  AND text IS NOT NULL
  AND (text LIKE '%יום ראשון%' OR text LIKE '%יום שני%' 
       OR text LIKE '%יום שלישי%' OR text LIKE '%יום רביעי%'
       OR text LIKE '%יום חמישי%' OR text LIKE '%יום שישי%'
       OR text LIKE '%שבת%' OR text LIKE '%מחר%'
       OR text LIKE '%השבוע%' OR text LIKE '%שבוע הבא%')
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Hebrew Day Names Reference

| Hebrew | English | Abbreviation |
|--------|---------|--------------|
| יום ראשון | Sunday | א' |
| יום שני | Monday | ב' |
| יום שלישי | Tuesday | ג' |
| יום רביעי | Wednesday | ד' |
| יום חמישי | Thursday | ה' |
| יום שישי | Friday | ו' |
| שבת | Saturday | - |
| מחר | Tomorrow | - |
| מחרתיים | Day after tomorrow | - |

## Direct SQL Fallback

If MCP tools fail or return empty results, query SQLite directly:

### Recent Messages from a Contact

```bash
sqlite3 -separator ' | ' data/messages.db "
SELECT 
  datetime(timestamp) as time,
  direction,
  replace(text, char(10), ' ↵ ') as message
FROM messages 
WHERE phone = 'PHONE_NUMBER'
  AND text IS NOT NULL 
  AND text != ''
ORDER BY timestamp DESC
LIMIT 30;
"
```

### Messages Mentioning Specific Text

```bash
sqlite3 data/messages.db "
SELECT timestamp, direction, substr(text, 1, 200)
FROM messages 
WHERE text LIKE '%SEARCH_TERM%'
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Group Messages

```bash
sqlite3 data/messages.db "
SELECT timestamp, direction, phone, substr(text, 1, 200)
FROM messages 
WHERE group_id = 'GROUP_ID'
ORDER BY timestamp DESC
LIMIT 30;
"
```

## Database Recovery

### Check Database Health

```bash
cd data && sqlite3 messages.db "PRAGMA integrity_check;" 2>&1 | head -10
```

**If corrupted** (shows errors like "database disk image is malformed"):

### Recovery Procedure

```bash
cd data

# 1. Backup corrupted database
cp messages.db messages.db.corrupted

# 2. Try .recover command (better than .dump for corrupted DBs)
sqlite3 messages.db ".recover" > messages_recover.sql 2>&1

# 3. Create new database from recovered SQL
sqlite3 messages_recovered.db < messages_recover.sql

# 4. Check for lost_and_found table (contains orphaned data)
sqlite3 messages_recovered.db "SELECT COUNT(*) FROM lost_and_found;"

# 5. Restore messages from lost_and_found
sqlite3 messages_recovered.db "
INSERT OR IGNORE INTO messages 
  (message_id, direction, jid, phone, text, is_group, group_id, 
   timestamp, created_at, media_type, media_path, media_mime_type, 
   transcribed_text, transcribed_language)
SELECT c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14
FROM lost_and_found
WHERE c2 IN ('incoming', 'outgoing')
  AND c1 IS NOT NULL
  AND c8 IS NOT NULL;
"

# 6. Verify recovery
sqlite3 messages_recovered.db "SELECT COUNT(*) FROM messages;"

# 7. Replace original database
mv messages.db messages.db.corrupted.bak
mv messages_recovered.db messages.db
rm -f messages.db-wal messages.db-shm
```

### lost_and_found Column Mapping

When recovering from `lost_and_found`, columns map as:

| Column | Field |
|--------|-------|
| c1 | message_id |
| c2 | direction |
| c3 | jid |
| c4 | phone |
| c5 | text |
| c6 | is_group |
| c7 | group_id |
| c8 | timestamp |
| c9 | created_at |
| c10-c14 | media fields |

## Troubleshooting

### Problem: MCP Tools Return Empty Results

1. **Check database exists**:
   ```bash
   ls -la data/messages.db
   ```

2. **Check database integrity**:
   ```bash
   sqlite3 data/messages.db "PRAGMA integrity_check;"
   ```

3. **If corrupted**, follow [Database Recovery](#database-recovery)

4. **If OK, try direct SQL** to verify data exists

### Problem: Can't Find Contact's Messages

1. **Check phone format** - should be without `+` (e.g., `972524670511`)

2. **List all contacts** to find the exact phone:
   ```bash
   sqlite3 data/messages.db "SELECT DISTINCT phone FROM messages WHERE phone LIKE '9725%';"
   ```

3. **Check JID format** - direct messages use `@s.whatsapp.net`:
   ```bash
   sqlite3 data/messages.db "SELECT DISTINCT jid FROM messages WHERE jid LIKE '%972524670511%';"
   ```

### Problem: Database Locked

```bash
# Check for running processes
lsof data/messages.db

# Remove stale lock files if bot is not running
rm -f data/messages.db-wal data/messages.db-shm
```

## Tips

1. **Phone numbers**: Always use format without `+` prefix (e.g., `972501234567`)
2. **Group names**: The tool resolves names to JIDs automatically
3. **Date filtering**: Use ISO 8601 format (`YYYY-MM-DD` or full datetime)
4. **Full-text search**: Uses FTS5 - supports phrases in quotes
5. **Contact lookup**: ALWAYS check the "Known Contacts" table when user mentions a name
6. **Corrupted DB**: Use `.recover` not `.dump` - it handles corruption better
7. **Hebrew text**: SQLite handles UTF-8 natively, no special handling needed

## See Also- [references/schema.md](references/schema.md) - Full database schema
- [references/known-contacts.md](references/known-contacts.md) - Extended contacts list