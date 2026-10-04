---
name: chat-history
description: "Search past WhatsApp/chat conversations stored in the audit log PostgreSQL database. Use when the user asks about past conversations, what was discussed, what someone said, finding a specific message, or referencing previous discussions. Also use to reply to or quote specific past messages."
---

# Chat History Skill

Search past WhatsApp messages stored in the audit log DB (`messages` table), with file-based fallback when DB is unavailable.

## Minimum Model
Any model. Operations are lookup/query based.

---

## Step 1: Detect PA_DB_URL availability

```python
import os, sys

def get_db_conn():
    url = os.environ.get('PA_DB_URL') or os.environ.get('HELENI_DB_URL')
    if not url:
        return None
    try:
        import psycopg2
        conn = psycopg2.connect(url)
        return conn
    except Exception:
        return None

conn = get_db_conn()
DB_AVAILABLE = conn is not None
```

---

## DB Mode (PA_DB_URL available)

All queries against the `messages` table. Output format: `timestamp | sender | chat | body`.

### Full-text search
```python
import os, psycopg2

url = os.environ.get('PA_DB_URL') or os.environ.get('HELENI_DB_URL')
conn = psycopg2.connect(url)
cur = conn.cursor()

search_term = "budget"  # replace with actual term

cur.execute("""
    SELECT ts, sender_name, chat_name, body
    FROM messages
    WHERE body ILIKE %s
    ORDER BY ts DESC
    LIMIT 20
""", (f'%{search_term}%',))

for ts, sender, chat, body in cur.fetchall():
    print(f"{ts} | {sender} | {chat} | {body[:100]}")

conn.close()
```

### Search by contact name or phone
```python
cur.execute("""
    SELECT ts, sender_name, chat_name, body
    FROM messages
    WHERE sender_name ILIKE %s OR sender_phone ILIKE %s OR chat_name ILIKE %s
    ORDER BY ts DESC
    LIMIT 20
""", (f'%{contact}%', f'%{contact}%', f'%{contact}%'))
```

### Search by date range
```python
cur.execute("""
    SELECT ts, sender_name, chat_name, body
    FROM messages
    WHERE ts BETWEEN %s AND %s
    ORDER BY ts ASC
    LIMIT 100
""", ('2026-04-01', '2026-04-07'))
```

### Find recent unanswered messages (last 24h)
```python
cur.execute("""
    SELECT chat_id, chat_name, MAX(ts) as last_msg, COUNT(*) as msg_count
    FROM messages
    WHERE is_from_me = false
      AND ts > NOW() - INTERVAL '24 hours'
      AND chat_id NOT IN (
          SELECT DISTINCT chat_id FROM messages
          WHERE is_from_me = true
            AND ts > NOW() - INTERVAL '24 hours'
      )
    GROUP BY chat_id, chat_name
    ORDER BY last_msg DESC
""")

for chat_id, chat_name, last_msg, count in cur.fetchall():
    print(f"{last_msg} | {chat_name or chat_id} | {count} unanswered")
```

### DB stats (quick overview)
```python
cur.execute("""
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE ts > NOW() - INTERVAL '1 day') as today,
        MIN(ts) as first_msg,
        MAX(ts) as last_msg
    FROM messages
""")
row = cur.fetchone()
print(f"Total: {row[0]} | Today: {row[1]} | Range: {row[2]} → {row[3]}")
```

---

## File Fallback (no DB)

When `PA_DB_URL` is not set or DB is unreachable, search the file-based context files.

### Search context files with grep
```bash
SEARCH_TERM="budget"
WHATSAPP_DIR="/path/to/workspace/memory/whatsapp"

grep -r --include="*.md" -l "$SEARCH_TERM" "$WHATSAPP_DIR" | while read file; do
    echo "=== $file ==="
    grep -n "$SEARCH_TERM" "$file" | head -5
done
```

### Search by contact/group name
```bash
CONTACT="John"  # replace with actual contact name
find "$WHATSAPP_DIR" -name "meta.json" | xargs grep -l "$CONTACT" | while read meta; do
    dir=$(dirname "$meta")
    echo "=== $(cat $meta | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"name\",\"unknown\"))') ==="
    cat "$dir/context.md" | tail -20
done
```

---

## Output Format

Always present results as:
```
[2026-04-06 18:32] Daniel (Core Team) → "Can we review the budget today?"
[2026-04-06 18:45] Heleni (Core Team) → "Sure, I'll set it up"
```

If no results found → say "No messages found matching that query."
